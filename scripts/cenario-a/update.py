import mysql.connector
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

mysql_conn = mysql.connector.connect(
    host="localhost", port=3307,
    user="admin", password="admin123",
    database="secretaria"
)
qdrant = QdrantClient(host="localhost", port=6333)
model  = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "portal_academico"
ID_ATUALIZAR = 1  # Introdução a Algoritmos

print("\n" + "█"*55)
print("  CENÁRIO A — Atualização Sincronizada")
print("█"*55)

cursor = mysql_conn.cursor(dictionary=True)

# ─── Estado ANTES ────────────────────────────────────────
print("\n📋 Estado ANTES da atualização:\n")
cursor.execute("SELECT * FROM item_vetorial WHERE id = %s", (ID_ATUALIZAR,))
item = cursor.fetchone()
print(f"  Título:    {item['titulo']}")
print(f"  Descrição: {item['descricao']}")
print(f"  Categoria: {item['categoria']}")

# ─── Novos dados ─────────────────────────────────────────
novo_titulo    = "Algoritmos Avançados e Complexidade"
nova_descricao = "Análise de complexidade, algoritmos gulosos e programação dinâmica."
nova_categoria = "Algoritmos"

# ─── Atualiza no MySQL ───────────────────────────────────
cursor.execute("""
    UPDATE item_vetorial
    SET titulo = %s, descricao = %s, categoria = %s
    WHERE id = %s
""", (novo_titulo, nova_descricao, nova_categoria, ID_ATUALIZAR))
mysql_conn.commit()
print("\n  ✅ MySQL atualizado!")

# ─── Atualiza vetor no Qdrant ────────────────────────────
novo_vetor = model.encode(f"{novo_titulo} {nova_descricao}").tolist()
qdrant.upsert(
    collection_name=COLLECTION,
    points=[PointStruct(
        id=ID_ATUALIZAR,
        vector=novo_vetor,
        payload={"categoria": nova_categoria, "titulo": novo_titulo}
    )]
)
print("  ✅ Qdrant atualizado!")

# ─── Estado DEPOIS ───────────────────────────────────────
print("\n📋 Estado DEPOIS da atualização:\n")
cursor.execute("SELECT * FROM item_vetorial WHERE id = %s", (ID_ATUALIZAR,))
item = cursor.fetchone()
print(f"  Título:    {item['titulo']}")
print(f"  Descrição: {item['descricao']}")
print(f"  Categoria: {item['categoria']}")

# ─── Confirma nova busca semântica ───────────────────────
print("\n🔍 Verificando busca com novo conteúdo...\n")
vetor_consulta = model.encode("programação dinâmica e complexidade").tolist()
response = qdrant.query_points(
    collection_name=COLLECTION,
    query=vetor_consulta,
    limit=2
)
for r in response.points:
    cursor.execute("SELECT titulo FROM item_vetorial WHERE id = %s", (r.id,))
    row = cursor.fetchone()
    print(f"  📌 Score: {r.score:.4f} | {row['titulo']}")

print("\n" + "█"*55)
print("  ✅ Atualização sincronizada concluída!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()