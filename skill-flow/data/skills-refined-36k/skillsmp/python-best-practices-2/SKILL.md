---
name: python-best-practices
description: Production-grade Python playbook (src/ architecture, OOP, typing, docs, tests, uv+taskipy+ruff, CI gates, security, performance).
license: MIT
---

Use this skill to bootstrap, refactor, or review Python projects with modern production practices.

## Non-negotiables
- Code comments MUST be ONLY essential and in ENGLISH.
- Prefer explicit dependencies (DI/composition root) over hidden global state (Singleton anti-pattern).
- Make changes minimal and behavior-preserving unless the user requests breaking changes.

## Standard Tooling Baseline (uv + taskipy + ruff + mypy + pytest)
This skill standardizes `uv run task lint_fix` using the provided template:
- `assets/templates/pyproject.toml.tmpl`

### Default expectation
- Project uses `uv` with `pyproject.toml` + `uv.lock`.
- Tasks exist under `[tool.taskipy.tasks]`, including `lint_fix`.
- Lint/format is enforced via:
  - `ruff check --fix .`
  - `ruff format .`
  - plus optional `black .` (kept for compatibility).

### When to adjust the template
Adjust ONLY if necessary:
- Python version differs from `>=3.14,<3.15`
- Ruff target differs from `py314`
- line-length differs from 121
- build backend differs (e.g., hatchling/poetry) — keep src layout as-is

## Workflow (apply in order)

### 1) Identify boundaries
- Project type: library / CLI / service / data pipeline.
- Composition root: where dependencies are wired (e.g., `main.py`, `app/__init__.py`, `cli.py`).
- I/O boundaries: API routes, CLI args, job runners, external clients.

### 2) Enforce project layout
Recommended baseline:
- `src/<package>/...`
- `tests/`
- `scripts/` (project tooling only)
- Avoid `utils.py` dumping grounds; prefer domain/feature modules.

### 3) Dependency management with uv
Principles:
- Commit `uv.lock` for reproducibility.
- CI should install exactly from the lockfile:
  - `uv sync --frozen`

Common commands:
- `uv add <pkg>`
- `uv remove <pkg>`
- `uv lock`
- `uv sync`

### 4) Enforce lint/format via taskipy
Required:
- `uv run task lint_fix`
- `uv run task lint`
- `uv run task test`

If missing, add tasks using the provided template (`assets/templates/pyproject.toml.tmpl`).

### 5) OOP and data modeling
Use classes intentionally:
- Prefer functions by default.
- Use classes when you need state, invariants, resource lifecycle, or polymorphism.

Rules:
- Prefer composition over deep inheritance.
- For data containers, prefer `@dataclass` with:
  - no mutable defaults (use `default_factory`)
  - `frozen=True` when immutability helps
  - `slots=True` only if you measured and it matters

Interfaces:
- Prefer `Protocol` for decoupled interfaces.
- Use `ABC` only when you need runtime enforcement.

### 6) Typing as contracts
- Type boundaries first: public APIs, domain models, adapters.
- Avoid `Any` unless unavoidable (and document why).
- Keep typing policy consistent (gradual typing is OK).

### 7) Documentation (minimal but useful)
- Docstrings for public APIs.
- Document exceptions for boundaries.
- Avoid redundant comments. Comments only when they add non-obvious intent.

### 8) Testing
- Use pytest; keep tests deterministic.
- Prefer fixtures + parametrization.
- Split unit vs integration when needed.

### 9) Logging + error handling
- No `print()` in production codepaths.
- Use `logging.getLogger(__name__)`.
- Never swallow exceptions silently.
- Use `raise X from e` when wrapping.

### 10) Async/concurrency (when applicable)
- Never block the event loop with sync I/O.
- Always use timeouts and cancellation-aware code.
- Add retries/backoff only at boundaries (external calls), not deep inside core logic.

### 11) Performance (only if justified)
- Choose correct data structures (e.g., deque for queues).
- Measure before optimizing (timeit/profilers).
- Use caching carefully and with limits.

### 12) Security baseline
- Never unpickle untrusted input.
- Avoid `shell=True` unless strictly required.
- Use `secrets` for tokens.

## Output format (when applying this skill)
Provide:
1) Gaps found (tooling/layout/typing/tests/security).
2) A small-step plan.
3) Concrete diffs (pyproject/ruff/mypy/pytest) + minimal code changes.
4) Conventional commit messages (one line, English).
5) Final reminder: run `uv run task lint_fix` before commit.