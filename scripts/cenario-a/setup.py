# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mdouglas <mdouglas@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/25 18:50:23 by mdouglas          #+#    #+#              #
#    Updated: 2026/03/25 18:51:04 by mdouglas         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import mysql.connector
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# ─── Conexões ───────────────────────────────────────────
mysql_conn = mysql.connector.connect(
    host="localhost", port=3307,
    user="admin", password="admin123",
    database="secretaria"
)
qdrant = QdrantClient(host="localhost", port=6333)
model  = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "portal_academico"

print("\n" + "█"*55)
print("  CENÁRIO A — Setup: MySQL + Qdrant")
print("█"*55)

# ─── Cria tabela no MySQL ────────────────────────────────
cursor = mysql_conn.cursor()
cursor.execute("DROP TABLE IF EXISTS item_vetorial")
cursor.execute("""
    CREATE TABLE item_vetorial (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200),
        descricao TEXT,
        categoria VARCHAR(100)
    )
""")
mysql_conn.commit()
print("\n✅ Tabela 'item_vetorial' criada no MySQL!")

# ─── 10 registros acadêmicos ────────────────────────────
registros = [
    ("Introdução a Algoritmos",         "Estudo de algoritmos básicos de ordenação e busca.",          "Algoritmos"),
    ("Estruturas de Dados",             "Listas, filas, pilhas e árvores binárias.",                   "Algoritmos"),
    ("Banco de Dados Relacional",       "Modelagem com entidades, relacionamentos e SQL.",              "Banco de Dados"),
    ("Banco de Dados NoSQL",            "Conceitos de documentos, chave-valor e grafos.",               "Banco de Dados"),
    ("Redes de Computadores",           "Protocolos TCP/IP, camadas OSI e roteamento.",                 "Redes"),
    ("Segurança em Redes",              "Criptografia, firewalls e ataques comuns.",                    "Redes"),
    ("Sistemas Operacionais",           "Gerenciamento de processos, memória e arquivos.",              "Sistemas"),
    ("Virtualização e Containers",      "Conceitos de VMs, Docker e orquestração.",                    "Sistemas"),
    ("Inteligência Artificial",         "Aprendizado de máquina, redes neurais e NLP.",                "IA"),
    ("Processamento de Linguagem Natural", "Tokenização, embeddings e modelos de linguagem.",          "IA"),
]

cursor.executemany(
    "INSERT INTO item_vetorial (titulo, descricao, categoria) VALUES (%s, %s, %s)",
    registros
)
mysql_conn.commit()
print("✅ 10 registros inseridos no MySQL!")

# ─── Cria collection no Qdrant ───────────────────────────
if qdrant.collection_exists(COLLECTION):
    qdrant.delete_collection(COLLECTION)

qdrant.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
print("✅ Collection criada no Qdrant!")

# ─── Gero os vetores e insiro no Qdrant ────────────────────
print("\n🔢 Gerando vetores e inserindo no Qdrant...\n")
cursor.execute("SELECT id, titulo, descricao, categoria FROM item_vetorial")
rows = cursor.fetchall()

points = []
for row in rows:
    id_sql, titulo, descricao, categoria = row
    vetor = model.encode(f"{titulo} {descricao}").tolist()
    points.append(PointStruct(
        id=id_sql,
        vector=vetor,
        payload={"categoria": categoria, "titulo": titulo}
    ))
    print(f"  🔹 Vetor gerado: [{titulo[:45]}]")

qdrant.upsert(collection_name=COLLECTION, points=points)

print("\n" + "█"*55)
print("  ✅ Setup Cenário A concluído!")
print("█"*55 + "\n")

cursor.close()
mysql_conn.close()