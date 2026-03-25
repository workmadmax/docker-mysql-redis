import mysql.connector
import redis
import json
import time

# ─── Conexões ───────────────────────────────────────────
mysql_conn = mysql.connector.connect(
    host="localhost", port=3307,
    user="admin", password="admin123",
    database="secretaria"
)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

CACHE_TTL = 60

# ════════════════════════════════════════════════════════
print("\n" + "█"*55)
print("  CENÁRIO B — Banco SQL + Cache Redis")
print("█"*55)

# ─── ETAPA 1: Setup ─────────────────────────────────────
print("\n📌 ETAPA 1 — Criando tabela e inserindo registros")
print("─"*55)

cursor = mysql_conn.cursor()
cursor.execute("DROP TABLE IF EXISTS item")
cursor.execute("""
    CREATE TABLE item (
        id INT AUTO_INCREMENT PRIMARY KEY,
        categoria VARCHAR(100),
        conteudo TEXT
    )
""")
registros = [
    ("Horários",      "Grade horária do curso de Ciência da Computação 2025/1"),
    ("Horários",      "Horários das aulas de Banco de Dados — turma A e B"),
    ("Notas",         "Notas parciais da disciplina de Algoritmos — 1º bimestre"),
    ("Notas",         "Resultado da prova final de Estrutura de Dados"),
    ("Requerimentos", "Formulário de trancamento de disciplina"),
    ("Requerimentos", "Solicitação de aproveitamento de estudos"),
    ("Calendário",    "Calendário acadêmico 2025 com datas de provas e recessos"),
    ("Calendário",    "Prazo de matrícula para o segundo semestre de 2025"),
    ("Documentos",    "Declaração de matrícula — modelo atualizado"),
    ("Documentos",    "Histórico escolar — instruções para solicitação"),
]
cursor.executemany("INSERT INTO item (categoria, conteudo) VALUES (%s, %s)", registros)
mysql_conn.commit()

cursor.execute("SELECT * FROM item")
print(f"  {'ID':<5} {'CATEGORIA':<15} CONTEÚDO")
print("  " + "-"*70)
for row in cursor.fetchall():
    print(f"  {row[0]:<5} {row[1]:<15} {row[2]}")
print("\n  ✅ Tabela criada e 10 registros inseridos!")

# ─── ETAPA 2: Cache ──────────────────────────────────────
print("\n📌 ETAPA 2 — Cache de consultas por categoria")
print("─"*55)

# Limpa cache anterior
redis_client.flushdb()

def buscar_por_categoria(categoria):
    cache_key = f"consulta:{categoria}"
    cached = redis_client.get(cache_key)
    if cached:
        print(f"  [CACHE HIT] ✅ '{categoria}' veio do Redis")
        return json.loads(cached)
    print(f"  [CACHE MISS] 🔍 '{categoria}' buscado no MySQL")
    cur = mysql_conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM item WHERE categoria = %s", (categoria,))
    resultado = cur.fetchall()
    cur.close()
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(resultado))
    print(f"  [CACHE SET] 💾 Salvo no Redis por {CACHE_TTL}s")
    return resultado

for categoria in ["Horários", "Notas", "Horários", "Notas", "Documentos"]:
    buscar_por_categoria(categoria)

# ─── ETAPA 3: Contador ───────────────────────────────────
print("\n📌 ETAPA 3 — Contador de acessos por categoria")
print("─"*55)

acessos = [
    "Horários", "Notas", "Horários", "Requerimentos",
    "Notas", "Horários", "Calendário", "Notas",
    "Documentos", "Horários", "Notas", "Requerimentos",
    "Calendário", "Horários",
]
for cat in acessos:
    total = redis_client.incr(f"acessos:{cat}")
    print(f"  📊 '{cat}' — total: {total}")

# ─── ETAPA 4: Ranking ────────────────────────────────────
print("\n📌 ETAPA 4 — Ranking de categorias mais acessadas")
print("─"*55)

contagens = []
cur_scan = 0
while True:
    cur_scan, chaves = redis_client.scan(cur_scan, match="acessos:*", count=100)
    for chave in chaves:
        categoria = chave.replace("acessos:", "")
        total = int(redis_client.get(chave))
        contagens.append((categoria, total))
    if cur_scan == 0:
        break

contagens.sort(key=lambda x: x[1], reverse=True)
print(f"  {'POS':<5} {'CATEGORIA':<15} {'ACESSOS'}")
print("  " + "-"*40)
for pos, (cat, total) in enumerate(contagens, start=1):
    barra = "█" * total
    print(f"  {pos}º     {cat:<15} {barra} ({total})")

print("\n" + "█"*55)
print("  ✅ Cenário B concluído com sucesso!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()