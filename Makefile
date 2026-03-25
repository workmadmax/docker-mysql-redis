PYTHON = .venv/bin/python

# ════════════════════════════════════════════════
# TODOS OS CENÁRIOS
# ════════════════════════════════════════════════
all:
	@echo ""
	@echo "██████████████████████████████████████████████████████"
	@echo "   PROVA FINAL — Persistência Poliglota com Docker"
	@echo "██████████████████████████████████████████████████████"
	@echo ""
	@$(MAKE) cenario-a
	@$(MAKE) cenario-b
	@$(MAKE) cenario-c

# ════════════════════════════════════════════════
# CENÁRIO A — MySQL + Qdrant
# ════════════════════════════════════════════════
cenario-a:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║         CENÁRIO A — MySQL + Banco Vetorial           ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "[ 1/3 ] Setup — Criando tabela e vetores..."
	@$(PYTHON) scripts/cenario-a/setup.py
	@echo ""
	@echo "[ 2/3 ] Busca por similaridade semântica..."
	@$(PYTHON) scripts/cenario-a/search.py
	@echo ""
	@echo "[ 3/3 ] Atualização sincronizada MySQL + Qdrant..."
	@$(PYTHON) scripts/cenario-a/update.py

# ════════════════════════════════════════════════
# CENÁRIO B — MySQL + Redis
# ════════════════════════════════════════════════
cenario-b:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║         CENÁRIO B — MySQL + Cache Redis              ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "[ 1/4 ] Setup — Criando tabela e inserindo registros..."
	@$(PYTHON) scripts/cenario-b/setup.py
	@echo ""
	@echo "[ 2/4 ] Cache de consultas por categoria..."
	@$(PYTHON) scripts/cenario-b/cache.py
	@echo ""
	@echo "[ 3/4 ] Contador de acessos..."
	@$(PYTHON) scripts/cenario-b/counter.py
	@echo ""
	@echo "[ 4/4 ] Ranking de categorias mais acessadas..."
	@$(PYTHON) scripts/cenario-b/ranking.py

# ════════════════════════════════════════════════
# CENÁRIO C — MySQL + MinIO
# ════════════════════════════════════════════════
cenario-c:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║         CENÁRIO C — MySQL + Mídias MinIO             ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "[ 1/3 ] Setup — Upload de arquivos e registros..."
	@$(PYTHON) scripts/cenario-c/setup.py
	@echo ""
	@echo "[ 2/3 ] Listagem e acesso aos arquivos..."
	@$(PYTHON) scripts/cenario-c/listing.py
	@echo ""
	@echo "[ 3/3 ] Exclusão consistente MinIO + MySQL..."
	@$(PYTHON) scripts/cenario-c/delete.py

# ════════════════════════════════════════════════
# UTILITÁRIOS
# ════════════════════════════════════════════════
up:
	docker compose up -d

down:
	docker compose down

status:
	docker ps