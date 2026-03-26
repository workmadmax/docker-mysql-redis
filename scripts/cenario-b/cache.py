
import mysql.connector
import redis
import json

# Conexões
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="admin",
    password="admin123",
    database="secretaria"
)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

CACHE_TTL = 180

def buscar_por_categoria(categoria: str):
    cache_key = f"consulta:{categoria}"

    cached = redis_client.get(cache_key)
    if cached:
        print(f"  [CACHE HIT] ✅ Dados vieram do Redis")
        return json.loads(cached)

    print(f"  [CACHE MISS] 🔍 Buscando no MySQL...")
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM item WHERE categoria = %s", (categoria,))
    resultado = cursor.fetchall()
    cursor.close()
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(resultado))
    print(f"  [CACHE SET] 💾 Salvo no Redis por {CACHE_TTL}s")

    return resultado
# --- Demonstração ---
categoria = "Horários"

print(f"\n{'='*50}")
print(f" 1ª consulta: '{categoria}' — deve ir ao MySQL")
print(f"{'='*50}")
dados = buscar_por_categoria(categoria)
for item in dados:
    print(f"  ID {item['id']} | {item['categoria']} | {item['conteudo']}")

print(f"\n{'='*50}")
print(f" 2ª consulta: '{categoria}' — deve vir do cache")
print(f"{'='*50}")
dados = buscar_por_categoria(categoria)
for item in dados:
    print(f"  ID {item['id']} | {item['categoria']} | {item['conteudo']}")