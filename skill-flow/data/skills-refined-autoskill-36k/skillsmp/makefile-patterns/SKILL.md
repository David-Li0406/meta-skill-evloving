---
name: makefile-patterns
description: Padrões e boas práticas para Makefile em todos os projetos
triggers: [makefile, make, build, test, docker, compose]
---

# Makefile - Padrões e Boas Práticas

**Makefile é padrão obrigatório em todos os projetos. Comandos principais DEVEM estar no Makefile.**

---

## Estrutura Padrão

### Comandos Obrigatórios

Todo projeto deve ter:

```makefile
.PHONY: help up down build test clean logs ps

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Subir containers
	docker compose up -d --build --remove-orphans

down: ## Parar containers
	docker compose down

build: ## Build das imagens
	docker compose build

test: ## Executar testes
	docker compose run --rm test pytest

logs: ## Ver logs
	docker compose logs -f

ps: ## Status dos containers
	docker compose ps

clean: ## Limpar containers e volumes
	docker compose down -v
```

---

## Organização por Categoria

```makefile
# ============================================
# DOCKER COMPOSE
# ============================================
.PHONY: up down build logs ps clean

up: ## Subir stack
	docker compose up -d --build --remove-orphans

down: ## Parar stack
	docker compose down

# ============================================
# TESTES
# ============================================
.PHONY: test test-cov test-watch

test: ## Executar testes
	pytest

test-cov: ## Testes com cobertura
	pytest --cov=src --cov-report=term-missing

# ============================================
# DESENVOLVIMENTO
# ============================================
.PHONY: install dev lint format

install: ## Instalar dependências
	pip install -r requirements.txt

dev: ## Modo desenvolvimento
	docker compose -f docker-compose.dev.yml up

lint: ## Linter
	black --check .
	flake8 .

format: ## Formatar código
	black .
```

---

## Variáveis e Ambientes

```makefile
# Variáveis
ENV ?= local
COMPOSE_FILE := docker-compose.yml

ifeq ($(ENV),prod)
	COMPOSE_FILE := docker-compose.prod.yml
endif

up: ## Subir stack (ENV=local|prod)
	docker compose -f $(COMPOSE_FILE) up -d --build
```

---

## Help Automático

**SEMPRE incluir help automático:**

```makefile
.PHONY: help
help: ## Mostrar ajuda
	@echo "═══════════════════════════════════════════════"
	@echo "       PROJETO - MAKEFILE COMMANDS           "
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@echo "Usage: make <target> ENV=local|prod"
	@echo ""
	@echo "Available Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
```

---

## Prioridade de Comandos

**Quando usuário pede para executar algo:**

1. **Verificar Makefile primeiro**
2. **Se comando existe no Makefile → usar Makefile**
3. **Se não existe → criar no Makefile**
4. **Depois executar via Makefile**

**Exemplo:**
- Usuário: "subir o cluster docker compose"
- Agente: Verifica Makefile → Se tem `make up` → Executa `make up`
- Se não tem → Cria `make up` no Makefile → Executa `make up`

---

## Templates por Stack

### Python/FastAPI

```makefile
.PHONY: migrate test lint format

migrate: ## Rodar migrations
	alembic upgrade head

test: ## Testes
	pytest --cov=src --cov-report=term-missing

lint: ## Linter
	black --check .
	flake8 .
	mypy src/

format: ## Formatar
	black .
	isort .
```

### Django

```makefile
.PHONY: migrate test collectstatic

migrate: ## Migrations
	python manage.py migrate

test: ## Testes
	python manage.py test

collectstatic: ## Static files
	python manage.py collectstatic --noinput
```

### Node.js

```makefile
.PHONY: install test build

install: ## Instalar dependências
	npm install

test: ## Testes
	npm test

build: ## Build
	npm run build
```

---

## Checklist

- [ ] Makefile existe no projeto
- [ ] Comandos principais estão no Makefile
- [ ] Help automático implementado
- [ ] Comandos organizados por categoria
- [ ] Variáveis de ambiente suportadas (se necessário)
- [ ] Agente verifica Makefile antes de executar comandos

