
import mysql.connector
import time

print(" ⏳ Aguardando o MySQL iniciar...")
time.sleep(20)

conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="admin",
    password="admin123",
    database="secretaria"
)

cursor = conn.cursor()

print(" 🗂️ Criando tabela 'alunos'...")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS item (
        id INT AUTO_INCREMENT PRIMARY KEY,
        categoria VARCHAR(100),
        conteudo TEXT
    )
""")
conn.commit()
print(" ✅ Tabela 'item' criada com sucesso!")

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
conn.commit()
print(" ✅ Registros inseridos com sucesso!")

# exibir os dados inseridos \n
cursor.execute("SELECT * FROM item")
print("\n 📋 Dados inseridos na tabela 'alunos':\n")

print(f"{'ID':<5} {'CATEGORIA':<15} CONTEÚDO")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:<5} {row[1]:<15} {row[2]}")

cursor.close()
conn.close()