import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def registrar_acesso(categoria: str):
    chave = f"acessos:{categoria}"
    total = redis_client.incr(chave)
    print(f"  📊 '{categoria}' — total de acessos: {total}")


# Simulando acessos de diferentes usuários ao longo do dia
acessos_simulados = [
    "Horários", "Notas", "Horários", "Requerimentos",
    "Notas", "Horários", "Calendário", "Notas",
    "Documentos", "Horários", "Notas", "Requerimentos",
    "Calendário", "Horários",
]

print("\n" + "="*45)
print(" Simulando acessos de usuários...")
print("="*45)

for cat in acessos_simulados:
    registrar_acesso(cat)