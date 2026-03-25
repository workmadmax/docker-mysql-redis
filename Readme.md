# 🗄️ Persistência Poliglota com Docker

> Prova Final — Disciplina de Banco de Dados  
> Implementação de múltiplas tecnologias de armazenamento integradas via Docker

---

## 📋 Sobre o Projeto

Este projeto demonstra a integração de diferentes tecnologias de banco de dados em três cenários práticos, todos orquestrados com Docker Compose e implementados em Python.

---

## 🏗️ Arquitetura

```
srcs/
├── docker-compose.yml          # Todos os containers
├── Makefile                    # Execução automatizada
├── requirements.txt            # Dependências Python
├── .venv/                      # Ambiente virtual Python
└── scripts/
    ├── cenario-a/              # MySQL + Qdrant
    │   ├── setup.py
    │   ├── search.py
    │   └── update.py
    ├── cenario-b/              # MySQL + Redis
    │   ├── setup.py
    │   ├── cache.py
    │   ├── counter.py
    │   └── ranking.py
    └── cenario-c/              # MySQL + MinIO
        ├── setup.py
        ├── listing.py
        └── delete.py
```

---

## 🐳 Containers Docker

| Container | Imagem | Porta | Cenário |
|---|---|---|---|
| `mysql_cenario` | mysql:8.0 | 3307 | A, B e C |
| `qdrant_cenario_a` | qdrant/qdrant | 6333 | A |
| `redis_cenario_b` | redis:7.0 | 6379 | B |
| `minio_cenario_c` | minio/minio | 9000/9001 | C |

---

## ⚙️ Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.12+
- `make`

---

## 🚀 Como Executar

### 1. Suba os containers

```bash
make up
# ou
docker compose up -d
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Execute os cenários

```bash
# Todos os cenários de uma vez
make all

# Ou individualmente
make cenario-a
make cenario-b
make cenario-c
```

### 4. Verifique os containers

```bash
make status
# ou
docker ps
```

### 5. Para os containers

```bash
make down
```

---

## 📦 Cenários

### Cenário A — MySQL + Qdrant (Banco Vetorial)

**Problema:** Buscas por palavras exatas não retornam resultados semânticos relevantes.

**Solução:** O MySQL armazena os dados estruturados e o Qdrant permite buscas por similaridade semântica usando embeddings gerados pelo modelo `all-MiniLM-L6-v2`.

| Script | Descrição |
|---|---|
| `setup.py` | Cria tabela `item_vetorial` no MySQL, gera vetores e insere no Qdrant |
| `search.py` | Realiza buscas semânticas — encontra conteúdos por significado |
| `update.py` | Atualiza um item no MySQL e sincroniza o vetor no Qdrant |

---

### Cenário B — MySQL + Redis (Cache)

**Problema:** Consultas repetitivas geram sobrecarga no banco relacional.

**Solução:** O MySQL mantém os dados oficiais e o Redis armazena resultados em cache e contadores de acesso.

| Script | Descrição |
|---|---|
| `setup.py` | Cria tabela `item` no MySQL com 10 registros acadêmicos |
| `cache.py` | Demonstra CACHE MISS (vai ao MySQL) e CACHE HIT (vem do Redis) |
| `counter.py` | Registra acessos por categoria usando `INCR` do Redis |
| `ranking.py` | Exibe ranking das categorias mais acessadas usando `SCAN` |

---

### Cenário C — MySQL + MinIO (Mídias/Objetos)

**Problema:** Arquivos grandes não devem ser armazenados diretamente no banco relacional.

**Solução:** O MinIO armazena os arquivos e o MySQL mantém os metadados e referências.

| Script | Descrição |
|---|---|
| `setup.py` | Cria bucket no MinIO, tabela `documento` no MySQL e faz upload de 5 arquivos |
| `listing.py` | Lista arquivos no MinIO e registros no MySQL, acessa conteúdo de um arquivo |
| `delete.py` | Remove arquivo do MinIO e registro do MySQL de forma consistente |

---

## 📚 Dependências

```
mysql-connector-python  # Conexão com MySQL
redis                   # Conexão com Redis
qdrant-client           # Conexão com Qdrant
sentence-transformers   # Geração de embeddings vetoriais
minio                   # Conexão com MinIO
```

---

## 🔐 Credenciais (ambiente local)

| Serviço | Usuário | Senha |
|---|---|---|
| MySQL | admin | admin123 |
| MinIO | admin | admin123 |

---

## 📝 Conclusão

O **MySQL** atuou como fonte principal e oficial dos dados em todos os cenários, garantindo integridade e consistência através de tabelas bem definidas.

O **Qdrant** complementou o MySQL com buscas semânticas por similaridade, permitindo encontrar conteúdos por significado mesmo com palavras diferentes.

O **Redis** reduziu a sobrecarga no MySQL armazenando consultas em cache e contadores de acesso em tempo real com estruturas de chave-valor.

O **MinIO** separou o armazenamento de arquivos do banco relacional, funcionando como repositório de objetos compatível com S3 enquanto o MySQL manteve apenas os metadados.