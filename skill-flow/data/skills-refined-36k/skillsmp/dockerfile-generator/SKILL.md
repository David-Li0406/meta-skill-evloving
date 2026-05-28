---
name: dockerfile-generator
description: Skill para gerar Dockerfiles, entrypoints, Makefiles e .dockerignore automaticamente seguindo melhores práticas.
triggers: [generate dockerfile, create dockerfile, docker template, entrypoint generator, makefile generator]
---

# Dockerfile Generator Skill

**Geração automática de Dockerfiles multi-stage, entrypoints, Makefiles e .dockerignore seguindo as melhores práticas do cursor-multiagent-system.**

---

## Quando Usar

Aplicar esta skill quando:
- Iniciando um novo projeto que precisa de Docker
- Migrando projeto existente para Docker
- Padronizando Dockerfiles em múltiplos projetos
- Gerando templates seguindo as melhores práticas do sistema

---

## Opções de Geração

### 1. Usar Templates Existentes (Recomendado)

**Templates disponíveis em `core/templates/`:**
- **Django:** `core/templates/django/Dockerfile`
- **FastAPI:** `core/templates/fastapi-project/basic/Dockerfile` e `with-framework/Dockerfile`
- **Node.js:** `core/templates/entrypoint/nodejs-entrypoint.sh` (entrypoint)
- **React:** `core/templates/entrypoint/react-entrypoint.sh` (entrypoint)

**Uso:**
```bash
# Copiar template Django
cp core/templates/django/Dockerfile ./Dockerfile
cp core/templates/django/.dockerignore ./.dockerignore
cp core/templates/django/Makefile ./Makefile
cp core/templates/django/entrypoint.sh ./entrypoint.sh
```

### 2. Usar Skill Generator Service (Futuro)

**Quando implementado, usar API HTTP para geração dinâmica:**

```bash
# Exemplo de chamada à API
curl -X POST http://localhost:4000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "django",
    "package_manager": "poetry",
    "python_version": "3.11",
    "project_name": "myapp",
    "tests": true,
    "artifacts": ["dockerfile", "entrypoint", "makefile", "dockerignore"]
  }'
```

---

## Parâmetros de Geração

### Framework
- `django` - Django com gunicorn
- `fastapi` - FastAPI com uvicorn/gunicorn
- `node` - Node.js/Express
- `react` - React (Vite) com nginx

### Package Manager (Python)
- `poetry` - Poetry (pyproject.toml)
- `pip` - pip (requirements.txt)

### Versões
- `python_version`: `3.11`, `3.12` (padrão: `3.11`)
- `node_version`: `18`, `20` (padrão: `18`)

### Features
- `tests`: `true`/`false` - Incluir stage de testes
- `healthcheck`: `true`/`false` - Incluir healthcheck
- `non_root`: `true`/`false` - Usar usuário não-root (padrão: `true`)

---

## Estrutura Gerada

### Dockerfile Multi-Stage

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
# Instala dependências, roda testes, coleta static files

# Stage 2: Test (opcional)
FROM builder AS test
# Roda testes isoladamente

# Stage 3: Runtime
FROM python:3.11-slim AS runtime
# Imagem final minimalista
```

### Entrypoint.sh

- `set -euo pipefail`
- Funções: `wait_for_db()`, `check_dependencies()`
- Comandos: `dev`, `prod`, `test`, `migrate`, `shell`, `health`
- `exec "$@"` para forward de sinais

### Makefile

- Targets: `build`, `build-test`, `test`, `run`, `run-dev`, `scan`, `clean`
- Help automático: `make help`
- Variáveis configuráveis: `IMAGE_NAME`, `TAG`, `REGISTRY`

### .dockerignore

- Exclui: `__pycache__`, `venv`, `.git`, `.env`, `tests/`, `*.log`
- Otimiza contexto de build

---

## Regras Obrigatórias

### Dockerfile

1. **Multi-stage build obrigatório:**
   - Stage `builder`: Dependências e build
   - Stage `runtime`: Imagem final minimalista

2. **Otimização de cache:**
   - Copiar `requirements.txt`/`pyproject.toml` primeiro
   - Instalar dependências antes de copiar código

3. **Segurança:**
   - Usuário não-root (`appuser`)
   - Sem ferramentas de build no runtime
   - Sem segredos hardcoded

4. **Healthcheck:**
   - Configurar HEALTHCHECK para `/health/` endpoint

5. **Labels OCI:**
   - `org.opencontainers.image.title`
   - `org.opencontainers.image.description`
   - `org.opencontainers.image.vendor`

### Entrypoint.sh

1. **Sempre usar:**
   - `set -euo pipefail`
   - `exec "$@"` no final

2. **Funções obrigatórias:**
   - `wait_for_db()` - Aguardar banco (opcional)
   - `check_dependencies()` - Verificar dependências

3. **Comandos padrão:**
   - `dev` - Desenvolvimento
   - `prod` - Produção
   - `test` - Testes
   - `migrate` - Migrations
   - `health` - Health check

### Makefile

1. **Targets obrigatórios:**
   - `build` - Build da imagem
   - `test` - Rodar testes
   - `run` - Executar container
   - `help` - Mostrar ajuda

2. **Documentação:**
   - Cada target com comentário `##`

3. **Variáveis:**
   - `IMAGE_NAME` - Nome da imagem
   - `TAG` - Tag da imagem (padrão: `latest`)

---

## Exemplos de Uso

### Gerar Dockerfile Django

```bash
# Opção 1: Copiar template
cp core/templates/django/Dockerfile ./Dockerfile

# Opção 2: Gerar via API (quando disponível)
curl -X POST http://localhost:4000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "django",
    "package_manager": "poetry",
    "python_version": "3.11",
    "project_name": "myapp",
    "tests": true
  }'
```

### Gerar Entrypoint FastAPI

```bash
# Copiar template
cp core/templates/entrypoint/fastapi-entrypoint.sh ./entrypoint.sh

# Ajustar para projeto específico
# - Ajustar WSGI_MODULE se necessário
# - Ajustar comandos de migration (alembic)
```

### Gerar Makefile

```bash
# Copiar template Django
cp core/templates/django/Makefile ./Makefile

# Ajustar variáveis
# IMAGE_NAME=myapp
# PYTHON_VERSION=3.11
```

---

## Integração com Claude Code / Cursor

### Prompt para Claude Code

```
Gere Dockerfile multi-stage, entrypoint.sh e Makefile para um projeto Django usando Poetry.

Parâmetros:
- project_name: portal
- python_version: 3.11
- tests: true
- package_manager: poetry

Use os templates de core/templates/django/ e ajuste conforme necessário.
```

### Prompt para Cursor

```
Crie um Dockerfile multi-stage para este projeto Django seguindo as melhores práticas:
- Usar template de core/templates/django/Dockerfile
- Ajustar para usar Poetry (pyproject.toml)
- Incluir stage de testes
- Configurar usuário não-root
- Adicionar healthcheck
```

---

## Checklist de Validação

Após gerar os arquivos, validar:

- [ ] Dockerfile usa multi-stage build
- [ ] Dependências instaladas antes de copiar código
- [ ] Usuário não-root configurado
- [ ] Healthcheck presente
- [ ] Entrypoint.sh com `set -euo pipefail` e `exec "$@"`
- [ ] Makefile com targets essenciais
- [ ] .dockerignore exclui arquivos desnecessários
- [ ] Nenhum segredo hardcoded
- [ ] Labels OCI configurados
- [ ] Documentação atualizada

---

## Referências

- **Templates Django:** `core/templates/django/`
- **Templates FastAPI:** `core/templates/fastapi-project/`
- **Templates Entrypoint:** `core/templates/entrypoint/`
- **Docker Skill:** `skills/infrastructure/docker-entrypoint/SKILL.md`
- **Docker Compose Skill:** `skills/infrastructure/docker-compose/SKILL.md`
- **Django Guide:** `core/templates/django/DOCKERFILE_GUIDE.md`

---

## Roadmap (Futuro)

### Skill Generator Service

**Micro-serviço HTTP para geração dinâmica:**

```javascript
// Exemplo de implementação futura
POST /generate
{
  "framework": "django",
  "package_manager": "poetry",
  "python_version": "3.11",
  "project_name": "myapp",
  "tests": true,
  "artifacts": ["dockerfile", "entrypoint", "makefile", "dockerignore"]
}
```

**Benefícios:**
- Geração dinâmica baseada em parâmetros
- Integração com Claude Code / Cursor via API
- Templates atualizados centralmente
- Validação automática de boas práticas

---

**Última Atualização:** 2026-01-21

