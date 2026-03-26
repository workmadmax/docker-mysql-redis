import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def ranking_categorias():
    contagens = []
    # SCAN itera em lotes sem bloquear o Redis
    cursor = 0
    while True:
        cursor, chaves = redis_client.scan(cursor, match="acessos:*", count=100)
        for chave in chaves:
            categoria = chave.replace("acessos:", "")
            total = int(redis_client.get(chave))
            contagens.append((categoria, total))
        if cursor == 0:
            break
    if not contagens:
        print("Nenhum acesso registrado ainda.")
        return
    contagens.sort(key=lambda x: x[1], reverse=True)

    print("\n" + "="*45)
    print(" 🏆 Ranking de categorias mais acessadas")
    print("="*45)
    for pos, (categoria, total) in enumerate(contagens, start=1):
        barra = "█" * total
        print(f"  {pos}º {categoria:<15} {barra} ({total})")
    print("="*45)


ranking_categorias()