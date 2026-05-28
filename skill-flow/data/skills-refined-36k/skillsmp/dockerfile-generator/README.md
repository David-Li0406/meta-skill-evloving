# Dockerfile Generator - Documentação Completa

**Sistema para geração automática de Dockerfiles, entrypoints, Makefiles e .dockerignore seguindo as melhores práticas.**

---

## 📋 Visão Geral

Esta skill permite gerar automaticamente artefatos Docker seguindo as melhores práticas do cursor-multiagent-system:

- **Dockerfile** multi-stage otimizado
- **entrypoint.sh** robusto com múltiplos comandos
- **Makefile** com targets padronizados
- **.dockerignore** otimizado
- **docker-compose.yml** (opcional)

---

## 🎯 Métodos de Geração

### 1. Templates Existentes (Recomendado - Atual)

**Copiar templates prontos de `core/templates/`:**

```bash
# Django
cp core/templates/django/Dockerfile ./Dockerfile
cp core/templates/django/.dockerignore ./.dockerignore
cp core/templates/django/Makefile ./Makefile
cp core/templates/django/entrypoint.sh ./entrypoint.sh

# FastAPI (basic)
cp core/templates/fastapi-project/basic/Dockerfile ./Dockerfile
cp core/templates/fastapi-project/basic/entrypoint.sh ./entrypoint.sh
cp core/templates/fastapi-project/basic/.dockerignore ./.dockerignore

# FastAPI (with-framework)
cp core/templates/fastapi-project/with-framework/Dockerfile ./Dockerfile
cp core/templates/fastapi-project/with-framework/entrypoint.sh ./entrypoint.sh
```

**Vantagens:**
- ✅ Templates testados e validados
- ✅ Seguem todas as melhores práticas
- ✅ Documentação completa incluída
- ✅ Prontos para uso imediato

### 2. Skill Generator Service (Futuro)

**Micro-serviço HTTP para geração dinâmica:**

```bash
# Exemplo de chamada
curl -X POST http://localhost:4000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "django",
    "package_manager": "poetry",
    "python_version": "3.11",
    "project_name": "myapp",
    "tests": true,
    "healthcheck": true,
    "non_root": true,
    "artifacts": ["dockerfile", "entrypoint", "makefile", "dockerignore"]
  }'
```

**Resposta:**
```json
{
  "artifacts": {
    "dockerfile": "...",
    "entrypoint.sh": "...",
    "Makefile": "...",
    ".dockerignore": "..."
  },
  "metadata": {
    "framework": "django",
    "package_manager": "poetry",
    "python_version": "3.11"
  }
}
```

---

## 📚 Templates Disponíveis

### Django

**Localização:** `core/templates/django/`

**Arquivos:**
- `Dockerfile` - Multi-stage (builder, test, runtime)
- `.dockerignore` - Exclusões otimizadas
- `Makefile` - Targets padronizados
- `entrypoint.sh` - Comandos: dev, prod, migrate, test, shell, health
- `DOCKERFILE_GUIDE.md` - Documentação completa

**Características:**
- ✅ Suporte a Poetry e pip/requirements.txt
- ✅ Auto-detecção de WSGI module
- ✅ Collectstatic no builder
- ✅ Healthcheck configurado
- ✅ Usuário não-root

**Uso:**
```bash
# Copiar todos os arquivos
cp -r core/templates/django/* ./

# Ajustar para projeto específico
# - Ajustar WSGI_MODULE se necessário
# - Ajustar variáveis no Makefile
```

### FastAPI

**Localização:** `core/templates/fastapi-project/`

**Versões:**
- `basic/` - Template básico (FastAPI + SQLAlchemy + Alembic)
- `with-framework/` - Template com framework library (CQRS ready)

**Arquivos:**
- `Dockerfile` - Multi-stage otimizado
- `entrypoint.sh` - Comandos: dev, prod, test, migrate, downgrade, shell, health
- `.dockerignore` - Exclusões otimizadas
- `docker-compose.yml` - Setup completo com PostgreSQL e Redis
- `README.md` - Documentação completa

**Características:**
- ✅ Suporte a Poetry e pip
- ✅ Alembic migrations
- ✅ Healthcheck configurado
- ✅ Usuário não-root
- ✅ Netcat para wait_for_db

### Node.js / Express

**Localização:** `core/templates/entrypoint/nodejs-entrypoint.sh`

**Características:**
- ✅ Comandos: dev, prod, test, migrate, shell, health
- ✅ Wait for database
- ✅ Suporte a TypeScript
- ✅ NPM e Yarn

### React (Vite)

**Localização:** `core/templates/entrypoint/react-entrypoint.sh`

**Características:**
- ✅ Build stage com Node
- ✅ Serve stage com nginx
- ✅ Otimização de assets
- ✅ SPA routing

---

## 🔧 Parâmetros de Geração

### Framework

| Framework | Package Manager | Versões |
|-----------|----------------|---------|
| `django` | `poetry`, `pip` | Python 3.11, 3.12 |
| `fastapi` | `poetry`, `pip` | Python 3.11, 3.12 |
| `node` | `npm`, `yarn` | Node 18, 20 |
| `react` | `npm`, `yarn` | Node 18, 20 |

### Features

| Feature | Descrição | Padrão |
|---------|-----------|--------|
| `tests` | Incluir stage de testes | `true` |
| `healthcheck` | Incluir HEALTHCHECK | `true` |
| `non_root` | Usar usuário não-root | `true` |
| `multi_stage` | Usar multi-stage build | `true` |

---

## 📝 Exemplos de Uso

### Exemplo 1: Gerar Dockerfile Django com Poetry

```bash
# Copiar template
cp core/templates/django/Dockerfile ./Dockerfile
cp core/templates/django/.dockerignore ./.dockerignore
cp core/templates/django/Makefile ./Makefile
cp core/templates/django/entrypoint.sh ./entrypoint.sh

# Ajustar Makefile
sed -i 's/IMAGE_NAME = django-app/IMAGE_NAME = myapp/' Makefile

# Verificar se pyproject.toml existe
test -f pyproject.toml && echo "✅ Poetry configurado" || echo "⚠️  Criar pyproject.toml"
```

### Exemplo 2: Gerar Dockerfile FastAPI com pip

```bash
# Copiar template básico
cp core/templates/fastapi-project/basic/Dockerfile ./Dockerfile
cp core/templates/fastapi-project/basic/entrypoint.sh ./entrypoint.sh
cp core/templates/fastapi-project/basic/.dockerignore ./.dockerignore

# Verificar se requirements.txt existe
test -f requirements.txt && echo "✅ requirements.txt encontrado" || echo "⚠️  Criar requirements.txt"
```

### Exemplo 3: Prompt para Claude Code

```
Gere Dockerfile multi-stage, entrypoint.sh e Makefile para um projeto Django usando Poetry.

Parâmetros:
- project_name: portal
- python_version: 3.11
- tests: true
- package_manager: poetry

Use os templates de core/templates/django/ e ajuste:
1. WSGI_MODULE para portal.wsgi:application
2. IMAGE_NAME no Makefile para portal
3. Verifique se pyproject.toml existe
```

### Exemplo 4: Prompt para Cursor

```
Crie um Dockerfile multi-stage para este projeto Django seguindo as melhores práticas:

1. Usar template de core/templates/django/Dockerfile
2. Ajustar para usar Poetry (pyproject.toml)
3. Incluir stage de testes
4. Configurar usuário não-root
5. Adicionar healthcheck para /health/
6. Criar .dockerignore e Makefile também
```

---

## ✅ Checklist de Validação

Após gerar os arquivos, validar:

### Dockerfile
- [ ] Multi-stage build (builder, test, runtime)
- [ ] Dependências instaladas antes de copiar código
- [ ] Usuário não-root configurado
- [ ] Healthcheck presente
- [ ] Labels OCI configurados
- [ ] Sem ferramentas de build no runtime
- [ ] Sem segredos hardcoded

### Entrypoint.sh
- [ ] `set -euo pipefail` no início
- [ ] `exec "$@"` no final
- [ ] Função `wait_for_db()` (se aplicável)
- [ ] Função `check_dependencies()`
- [ ] Comandos: dev, prod, test, migrate, health

### Makefile
- [ ] Target `build`
- [ ] Target `test`
- [ ] Target `run` ou `run-dev`
- [ ] Target `help` com documentação
- [ ] Variáveis configuráveis (IMAGE_NAME, TAG)

### .dockerignore
- [ ] Exclui `__pycache__`, `venv`, `.git`
- [ ] Exclui `.env`, `*.log`
- [ ] Exclui `tests/` (se não necessário no build)
- [ ] Otimiza contexto de build

---

## 🚀 Roadmap (Futuro)

### Skill Generator Service

**Micro-serviço Node.js/Express:**

```javascript
// Estrutura proposta
skill-generator-service/
├── src/
│   ├── server.js          # Express server
│   ├── generators/
│   │   ├── dockerfile.js   # Gerador de Dockerfile
│   │   ├── entrypoint.js   # Gerador de entrypoint
│   │   ├── makefile.js     # Gerador de Makefile
│   │   └── dockerignore.js # Gerador de .dockerignore
│   └── templates/          # Templates Mustache
├── openapi.yaml            # OpenAPI spec
├── Dockerfile              # Container do serviço
└── README.md
```

**Endpoints:**
- `POST /generate` - Gerar artefatos
- `GET /frameworks` - Listar frameworks suportados
- `GET /templates/{framework}` - Ver template de um framework

**Integração:**
- Claude Code pode chamar via HTTP
- Cursor pode criar action que chama a API
- Validação automática de boas práticas

---

## 📖 Referências

- **Skill:** `skills/infrastructure/dockerfile-generator/SKILL.md`
- **Docker Entrypoint:** `skills/infrastructure/docker-entrypoint/SKILL.md`
- **Docker Compose:** `skills/infrastructure/docker-compose/SKILL.md`
- **Django Guide:** `core/templates/django/DOCKERFILE_GUIDE.md`
- **Templates:** `core/templates/`

---

**Última Atualização:** 2026-01-21

