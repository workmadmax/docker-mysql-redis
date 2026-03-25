

import mysql.connector
from minio import Minio

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

print("\n" + "█"*55)
print("  CENÁRIO C — Listagem e Acesso")
print("█"*55)

# ─── Lista arquivos no MinIO ─────────────────────────────
print("\n📦 Arquivos no bucket MinIO:\n")
objetos = minio_client.list_objects(BUCKET)
for obj in objetos:
    print(f"  📄 {obj.object_name} ({obj.size} bytes)")

# ─── Lista registros no MySQL ────────────────────────────
print("\n📋 Documentos registrados no MySQL:\n")
cursor = mysql_conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM documento")
docs = cursor.fetchall()

print(f"  {'ID':<4} {'TÍTULO':<40} {'DISCIPLINA':<25} DATA UPLOAD")
print("  " + "-"*90)
for doc in docs:
    print(f"  {doc['id']:<4} {doc['titulo']:<40} {doc['disciplina']:<25} {doc['data_upload']}")

# ─── Acessa conteúdo de um arquivo ──────────────────────
print("\n🔍 Acessando conteúdo do arquivo 'ementa_banco_dados.txt':\n")
response = minio_client.get_object(BUCKET, "ementa_banco_dados.txt")
conteudo = response.read().decode("utf-8")
print(f"  Conteúdo: {conteudo}")

print("\n" + "█"*55)
print("  ✅ Listagem concluída!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()