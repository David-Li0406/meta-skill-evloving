---
name: fastapi-architect
description: Scaffold, review, or refactor FastAPI services using uv, a src/ layout, versioned routers (/v1, /v2), and optional singleton external clients under src/services/clients when needed.
---

# FastAPI + uv Architect Skill

## When to use
Use this skill when the user asks to:
- Create a new FastAPI service with best practices (uv + src/ layout + Dockerfile).
- Refactor an existing FastAPI codebase into a clean, versioned API layout.
- Enforce consistent conventions: settings via pydantic-settings, structured logging, thin endpoints, and external client singletons (only when required).

## Non-goals
- Do not invent domain/business logic.
- Do not add heavy abstractions or excessive comments.
- Do not introduce new frameworks unless required.

## Core standards (must follow)
1. Project uses **uv** and defines `pyproject.toml`.
2. Code lives under `src/` and is importable (Docker uses `PYTHONPATH=/app/src`).
3. API versioning is explicit in `src/main.py`:
   - `app.include_router(<project_relevant>_router, prefix="/v1", tags=["<project_relevant>"])`
   - optionally `/v2` as well.
4. External clients go in `src/services/clients/` **ONLY when the project needs them** (HTTP APIs, DB, Redis, etc.).
5. When external clients exist, `src/services/clients/*` **must use a singleton pattern**.
6. Utilities (small helpers) go in `src/utils/`.
7. Comments are **only the essentials** and **in English**.
8. After any major change, always run `uv run task lint_fix` as the final step.

## Workflow
### A) If the user does NOT have a project yet (scaffold)
1. Scaffold without clients (default):
   - `uv run python {baseDir}/scripts/scaffold_fastapi_uv.py --project-dir <path> --service-name <name> --app-title "<title>"`
2. If the project requires an HTTP client (external APIs), scaffold with clients:
   - `uv run python {baseDir}/scripts/scaffold_fastapi_uv.py --project-dir <path> --service-name <name> --app-title "<title>" --with-http-client`
3. Then in the new project directory:
   - `uv sync`
   - `uv run task lint_fix`
   - `uv run task test`
4. Run locally:
   - `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src`
5. If any major changes are applied during setup, run:
   - `uv run task lint_fix` (final step)

### B) If the user ALREADY has a project (audit + plan + refactor)
1. Run:
   - `uv run python {baseDir}/scripts/audit_fastapi_project.py --project-dir <path>`
2. Produce an **objective, numbered** plan:
   - What to move/rename
   - What to add/remove
   - What to fix (imports, routers, settings, tests)
   - External clients section is included **only if clients are actually used**
3. Apply changes incrementally:
   - Keep diffs small
   - Update imports
   - Ensure `/v1` routing works with a project-relevant router alias and tags
4. Finish with quality gates:
   - `uv run task lint_fix` (required final step after major changes)
   - `uv run task test`

## Singleton clients (only when needed)
- Implement singleton clients in `src/services/clients/*`.
- Prefer an `@lru_cache` factory to guarantee one instance per process.
- Close clients on shutdown using FastAPI `lifespan`.

## Deliverables checklist
- `pyproject.toml` with minimal runtime deps + dev tooling.
- `src/main.py` with `/v1` (and optionally `/v2`) routing using a **project-relevant router alias** and **tags**.
- `src/core/config.py` using `pydantic-settings`.
- `src/core/log_config.py` + `src/core/logger_func.py`.
- `src/api/deps.py` for shared dependencies.
- `tests/` with a basic health test (and `conftest.py` to ensure `src/` is importable).
- Dockerfile using uv.
- `src/services/clients/` only if required by the project.

## Notes
- Use `fastapi[standard]` unless the user explicitly requests otherwise.
- Prefer FastAPI `lifespan` to manage startup/shutdown resources.
