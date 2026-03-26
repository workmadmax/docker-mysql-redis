import mysql.connector
from minio import Minio
from datetime import datetime
import io

# ─── Conexões ───────────────────────────────────────────
mysql_conn = mysql.connector.connect(
    host="localhost", port=3307,
    user="admin", password="admin123",
    database="secretaria"
)
minio_client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
)

BUCKET = "materiais-academicos"

# ════════════════════════════════════════════════════════
print("\n" + "█"*55)
print("  CENÁRIO C — Setup: MinIO + MySQL")
print("█"*55)

# ─── Cria bucket no MinIO ────────────────────────────────
if not minio_client.bucket_exists(BUCKET):
    minio_client.make_bucket(BUCKET)
    print(f"\n✅ Bucket '{BUCKET}' criado no MinIO!")
else:
    print(f"\n✅ Bucket '{BUCKET}' já existe!")

# ─── Cria tabela no MySQL ────────────────────────────────
cursor = mysql_conn.cursor()
cursor.execute("DROP TABLE IF EXISTS documento")
cursor.execute("""
    CREATE TABLE documento (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200),
        disciplina VARCHAR(100),
        categoria VARCHAR(100),
        referencia_arquivo VARCHAR(300),
        data_upload DATETIME
    )
""")
mysql_conn.commit()
print("✅ Tabela 'documento' criada no MySQL!")

# ─── Arquivos simulados para upload ─────────────────────
arquivos = [
    {
        "nome":       "ementa_banco_dados.txt",
        "titulo":     "Ementa de Banco de Dados",
        "disciplina": "Banco de Dados",
        "categoria":  "Ementa",
        "conteudo":   "Ementa oficial da disciplina de Banco de Dados 2025/1."
    },
    {
        "nome":       "lista_algoritmos.txt",
        "titulo":     "Lista de Exercícios — Algoritmos",
        "disciplina": "Algoritmos",
        "categoria":  "Lista",
        "conteudo":   "Lista de exercícios sobre ordenação e busca."
    },
    {
        "nome":       "prova_estrutura_dados.txt",
        "titulo":     "Prova — Estrutura de Dados",
        "disciplina": "Estrutura de Dados",
        "categoria":  "Prova",
        "conteudo":   "Prova sobre listas, filas e pilhas."
    },
    {
        "nome":       "slides_redes.txt",
        "titulo":     "Slides — Redes de Computadores",
        "disciplina": "Redes",
        "categoria":  "Slides",
        "conteudo":   "Slides da aula sobre protocolos TCP/IP."
    },
    {
        "nome":       "trabalho_so.txt",
        "titulo":     "Trabalho Final — Sistemas Operacionais",
        "disciplina": "Sistemas Operacionais",
        "categoria":  "Trabalho",
        "conteudo":   "Trabalho sobre escalonamento de processos."
    },
]

# ─── Upload + registro ───────────────────────────────────
print("\n📤 Fazendo upload dos arquivos...\n")
for arq in arquivos:
    conteudo_bytes = arq["conteudo"].encode("utf-8")
    minio_client.put_object(
        BUCKET,
        arq["nome"],
        io.BytesIO(conteudo_bytes),
        length=len(conteudo_bytes),
        content_type="text/plain"
    )
    cursor.execute("""
        INSERT INTO documento (titulo, disciplina, categoria, referencia_arquivo, data_upload)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        arq["titulo"],
        arq["disciplina"],
        arq["categoria"],
        f"{BUCKET}/{arq['nome']}",
        datetime.now()
    ))
    print(f"  ✅ Upload: {arq['nome']}")

mysql_conn.commit()

# ─── registros no MySQL ────────────────────────────
print("\n📋 Registros na tabela 'documento':\n")
cursor.execute("SELECT id, titulo, disciplina, categoria, referencia_arquivo FROM documento")
print(f"  {'ID':<4} {'TÍTULO':<40} {'DISCIPLINA':<25} {'CATEGORIA':<12} REFERÊNCIA")
print("  " + "-"*110)
for row in cursor.fetchall():
    print(f"  {row[0]:<4} {row[1]:<40} {row[2]:<25} {row[3]:<12} {row[4]}")

print("\n" + "█"*55)
print("  ✅ Setup Cenário C concluído!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()