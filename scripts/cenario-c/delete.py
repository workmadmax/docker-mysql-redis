
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
ARQUIVO_EXCLUIR = "trabalho_so.txt"

print("\n" + "█"*55)
print("  CENÁRIO C — Exclusão Consistente")
print("█"*55)

cursor = mysql_conn.cursor(dictionary=True)

# ─── Estado ANTES ────────────────────────────────────────
print("\n📋 Estado ANTES da exclusão:\n")
cursor.execute("SELECT id, titulo, referencia_arquivo FROM documento")
for doc in cursor.fetchall():
    print(f"  ID {doc['id']} | {doc['titulo']:<40} | {doc['referencia_arquivo']}")

objetos = list(minio_client.list_objects(BUCKET))
print(f"\n📦 Arquivos no MinIO: {[o.object_name for o in objetos]}")

# ─── Exclusão consistente ────────────────────────────────
print(f"\n🗑️  Excluindo '{ARQUIVO_EXCLUIR}' do MinIO e MySQL...\n")

# 1. Remove do MinIO
minio_client.remove_object(BUCKET, ARQUIVO_EXCLUIR)
print(f"  ✅ Arquivo removido do MinIO!")

# 2. Remove do MySQL
cursor.execute(
    "DELETE FROM documento WHERE referencia_arquivo = %s",
    (f"{BUCKET}/{ARQUIVO_EXCLUIR}",)
)
mysql_conn.commit()
print(f"  ✅ Registro removido do MySQL!")

# ─── Estado DEPOIS ───────────────────────────────────────
print("\n📋 Estado DEPOIS da exclusão:\n")
cursor.execute("SELECT id, titulo, referencia_arquivo FROM documento")
for doc in cursor.fetchall():
    print(f"  ID {doc['id']} | {doc['titulo']:<40} | {doc['referencia_arquivo']}")

objetos = list(minio_client.list_objects(BUCKET))
print(f"\n📦 Arquivos no MinIO: {[o.object_name for o in objetos]}")

print("\n" + "█"*55)
print("  ✅ Exclusão consistente concluída!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()