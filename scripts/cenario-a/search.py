# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    search.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mdouglas <mdouglas@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/25 18:49:57 by mdouglas          #+#    #+#              #
#    Updated: 2026/03/25 18:50:03 by mdouglas         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import mysql.connector
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

mysql_conn = mysql.connector.connect(
    host="localhost", port=3307,
    user="admin", password="admin123",
    database="secretaria"
)
qdrant = QdrantClient(host="localhost", port=6333)
model  = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "portal_academico"

print("\n" + "█"*55)
print("  CENÁRIO A — Busca por Similaridade Semântica")
print("█"*55)

def buscar(consulta: str, top: int = 3):
    print(f"\n🔍 Consulta: '{consulta}'")
    print("─"*55)

    vetor_consulta = model.encode(consulta).tolist()

    # Nova API do qdrant-client
    response = qdrant.query_points(
        collection_name=COLLECTION,
        query=vetor_consulta,
        limit=top
    )

    cursor = mysql_conn.cursor(dictionary=True)
    for r in response.points:
        cursor.execute("SELECT * FROM item_vetorial WHERE id = %s", (r.id,))
        item = cursor.fetchone()
        print(f"  📌 Score: {r.score:.4f} | {item['titulo']}")
        print(f"     Categoria: {item['categoria']}")
        print(f"     Descrição: {item['descricao']}\n")
    cursor.close()

buscar("aprendizado de máquina e inteligência")
buscar("segurança e criptografia de dados")
buscar("como funcionam os containers Docker")

print("█"*55)
print("  ✅ Busca semântica concluída!")
print("█"*55 + "\n")

mysql_conn.close()