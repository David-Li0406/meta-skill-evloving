# 🏗️ FastAPI Architect Skill

A **Codex/Claude skill** to **scaffold, audit, and refactor** FastAPI services using **uv**, a clean **`src/` layout**, **versioned routers** (`/v1`, `/v2`), and **optional singleton external clients** under `src/services/clients` **only when the project actually needs them**.

* ✅ Opinionated, production-ready defaults
* ✅ Minimal, essential English comments only
* ✅ Thin endpoints, business logic in `src/services`
* ✅ Consistent versioning + tags + naming conventions
* ✅ Optional external clients (HTTP/DB/etc) with enforced singleton pattern
* ✅ After any major change, always finish with: `uv run task lint_fix`

---

## ✨ What this skill does

### 🧱 Scaffold a new FastAPI service

Generates a ready-to-run project with:

* `uv` + `pyproject.toml`
* `src/` package layout
* API versioning (`/v1` ready)
* **Project-relevant router naming** (no generic `v1_router`)
* `pydantic-settings` configuration
* Structured logging templates
* Health endpoint + test
* Dockerfile built around `uv`

✅ **External clients are NOT created by default.**  
If your service needs an external client (HTTP APIs, DB, Redis, etc.), you opt in (see usage).

### 🔍 Audit an existing FastAPI service

Produces an **objective, numbered plan** with:

* Missing files/folders vs the blueprint
* Router versioning checks (`/v1`, `/v2`)
* **Project-relevant router alias + tags recommendations**
* External clients checks **only if client usage is detected**
* Final quality-gate recommendations (lint + tests)

---

## 📁 Repository layout

This repo is meant to be copied into your **Codex** or **Claude** skills directory:

```

fastapi-architect/
├─ SKILL.md
├─ scripts/
│  ├─ scaffold_fastapi_uv.py
│  └─ audit_fastapi_project.py
├─ references/
│  ├─ fastapi_notes.md
│  └─ uv_notes.md
└─ assets/
└─ templates/
├─ Dockerfile.tmpl
├─ README.md.tmpl
├─ env.example.tmpl
├─ python-version.tmpl
├─ pyproject_no_clients.tmpl
├─ pyproject_with_httpx.tmpl
├─ src_main_no_clients.py.tmpl
├─ src_main_with_httpx.py.tmpl
├─ src_core_config.py.tmpl
├─ src_core_log_config.py.tmpl
├─ src_core_logger_func.py.tmpl
├─ src_core_errors.py.tmpl
├─ src_api_deps_no_clients.py.tmpl
├─ src_api_deps_with_httpx.py.tmpl
├─ src_api_v1_router.py.tmpl
├─ src_api_v1_health.py.tmpl
├─ src_services_clients_httpx.py.tmpl
├─ tests_conftest.py.tmpl
└─ tests_test_health.py.tmpl

```

---

## ✅ Output project structure (scaffold result)

### Default scaffold (no external clients)

```

<project>/
├─ pyproject.toml
├─ .python-version
├─ Dockerfile
├─ README.md
├─ .env.example
├─ src/
│  ├─ **init**.py
│  ├─ main.py                       # includes /v1 routers with project-relevant alias + tags
│  ├─ core/
│  │  ├─ **init**.py
│  │  ├─ config.py
│  │  ├─ log_config.py
│  │  ├─ logger_func.py
│  │  └─ errors.py
│  ├─ api/
│  │  ├─ **init**.py
│  │  ├─ deps.py
│  │  ├─ v1/
│  │  │  ├─ **init**.py
│  │  │  ├─ router.py
│  │  │  └─ endpoints/
│  │  │     ├─ **init**.py
│  │  │     └─ health.py            # /v1/health
│  │  └─ v2/
│  │     └─ **init**.py             # placeholder by default
│  ├─ schemas/
│  │  └─ **init**.py
│  ├─ services/
│  │  └─ **init**.py
│  └─ utils/
│     └─ **init**.py
└─ tests/
├─ **init**.py
├─ conftest.py                   # ensures src/ is importable in tests
└─ test_health.py

```

### Scaffold with HTTP client (optional)

If you scaffold with `--with-http-client`, it additionally creates:

```

src/
└─ services/
└─ clients/
├─ **init**.py
└─ httpx_client.py            # singleton factory (e.g., @lru_cache)

```

📌 Note: `/v2` is created as a placeholder directory by default. If you want `/v2` fully scaffolded (router + endpoints + include in `main.py`), add templates and update the scaffold script accordingly.

---

## 🛠️ Installation

### ✅ Codex CLI

1) Create the skills directory:
- `~/.codex/skills/`

2) Clone:
- `git clone <YOUR_REPO_URL> ~/.codex/skills/fastapi-architect`

3) Restart Codex CLI so it discovers the new skill.

---

### ✅ Claude Code

You can install the skill **globally** or **per project**.

#### Option A — Global install
1) Create the skills directory:
- `~/.claude/skills/`

2) Clone:
- `git clone <YOUR_REPO_URL> ~/.claude/skills/fastapi-architect`

#### Option B — Per-project install
1) From your project root, create:
- `.claude/skills/`

2) Clone into it:
- `git clone <YOUR_REPO_URL> .claude/skills/fastapi-architect`

---

## 🚀 Usage

### 🧱 Scaffold a new FastAPI service (default: no clients)

Run with `uv`:

* `uv run python scripts/scaffold_fastapi_uv.py --project-dir <path> --service-name <name> --app-title "<title>"`

Example:

* `uv run python scripts/scaffold_fastapi_uv.py --project-dir ~/projects/my-api --service-name my-api --app-title "My API"`

Then inside the generated project:

* `uv sync`
* `uv run task lint_fix`
* `uv run task test`
* `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src`

✅ After any major change (refactor, routing, dependencies, clients, settings), always finish with:
- `uv run task lint_fix`

---

### 🌐 Scaffold with an HTTP client (only if needed)

Use this when your service calls external APIs:

* `uv run python scripts/scaffold_fastapi_uv.py --project-dir <path> --service-name <name> --app-title "<title>" --with-http-client`

This adds:

* `src/services/clients/httpx_client.py` (singleton)
* `httpx` dependency
* lifespan wiring in `src/main.py` to close the client cleanly

---

### 🔍 Audit an existing FastAPI project

* `uv run python scripts/audit_fastapi_project.py --project-dir <path>`

Example:

* `uv run python scripts/audit_fastapi_project.py --project-dir .`

✅ The audit will **only enforce clients rules** if it detects client usage (dependencies/imports) or the `src/services/clients` folder already exists.

---

### 🤖 Using via assistants (Codex / Claude)

You can ask Codex CLI or Claude Code things like:

- “Use fastapi-architect to scaffold a FastAPI service named `<name>` in `<path>`.”
- “Audit this project and give me a step-by-step refactor plan.”
- “Add `/v2` versioning and keep router aliases project-relevant.”

Tip: In Claude Code, you can typically invoke the skill by name (e.g., `/fastapi-architect`) or explicitly request “apply the fastapi-architect skill”.

---

## 📐 Design principles (opinionated rules)

✅ **Versioned APIs**
* Routers must be included via `prefix="/v1"` (and optionally `/v2`) in `src/main.py`.

✅ **Project-relevant router naming + tags**
* Avoid generic names like `v1_router`.
* Prefer `<service>_router` and tags aligned with the service/domain, e.g.:
  * `app.include_router(my_service_router, prefix="/v1", tags=["my_service"])`

✅ **Thin endpoints**
* Endpoints should be minimal orchestration.
* Business logic goes into `src/services/`.

✅ **External clients are optional**
* Create `src/services/clients/` only if the project actually needs it.
* If clients exist, enforce the singleton pattern (default uses `@lru_cache`).
* Close clients via FastAPI `lifespan`.

✅ **Utilities in `src/utils`**
* Keep helpers small and focused.

✅ **Essential comments only (English)**
* No verbose commentary.
* Only include the minimum that improves correctness/maintainability.

---

## 🧪 Quality gates

The scaffolded project includes Taskipy tasks:

- Lint & type-check:
  - `uv run task lint`

- Auto-fix (required after major changes):
  - `uv run task lint_fix`

- Tests:
  - `uv run task test`

✅ Rule: After any major change (structure, routers, deps, clients, settings), always run `uv run task lint_fix` as the final step.

---

## 🐳 Docker

The scaffold includes a uv-based Dockerfile. Build & run:

* `docker build -t <service-name> .`
* `docker run --rm -p 8000:8000 <service-name>`

---

## 🧩 Extending the skill

Common improvements you might add:

* ✅ Fully scaffold `/v2` (router + endpoints + include in `main.py`)
* ✅ Add `pre-commit` hooks (ruff/black/mypy)
* ✅ Add structured JSON logging for Loki/ELK
* ✅ Add DB client singletons (Postgres/Redis) templates
* ✅ Add CI workflow for linting templates and scripts

---

## 📚 References

* FastAPI Documentation (project structure, APIRouter, lifespan, settings patterns)
* OpenAI Codex Skills documentation (skill layout, SKILL.md conventions)
* uv documentation (dependency management + Docker patterns)

---

## 🤝 Contributing

PRs are welcome! Suggested contribution flow:

1) Create a feature branch  
2) Keep diffs small and focused  
3) Update templates + scripts together  
4) Add/adjust tests if you change generated behavior