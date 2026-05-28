---
name: python-backend
description: Best-practice workflow and guardrails for Python backend work (APIs/services, data access, background jobs, CLIs). Use when Codex is writing or refactoring Python application code, setting up Python tooling, improving performance, adding tests, or making packaging/lint/type-check decisions (uv, Ruff, mypy, pytest), including data tooling choices (prefer polars) and secure config patterns (.env).
---

# Python Backend

Apply these rules when producing or modifying Python backend code. Optimize for correctness, performance, and maintainability while keeping changes small and reversible.

## Defaults

- Prefer clarity first, then optimize hotspots based on evidence (profiling/benchmarks) rather than blanket micro-optimizations.
- Avoid unnecessary abstractions; keep code minimal and easy to review.
- Use descriptive names; avoid one-letter names outside tight comprehensions.

## Tooling

- Use `uv` for dependency management and virtual environments (`.venv`) when appropriate for the repo.
- Use Ruff for formatting + linting (do not mix with Black/isort unless the repo already does).
- Use mypy for static type checking when the repo is typed; match the repo's existing strictness.
- Use pytest for tests; follow Arrange-Act-Assert for readability.
- For notebooks, install `ipykernel`/`ipywidgets` into the local `.venv` when needed, but do not add them to runtime requirements.

## Code style

- Follow PEP 8; default to 4-space indentation.
- Prefer `pathlib.Path` over raw string paths for file operations (unless the repo standard differs).
- Use f-strings for formatting; use `enumerate()` over manual counters.
- Avoid mutable default arguments.

## Types and APIs

- Type all public function signatures (params + return types).
- Avoid `Any`; if unavoidable, isolate it at the boundary (e.g., parsing/IO) and convert to typed structures quickly.
- Prefer dataclasses (or `pydantic` models if the repo already uses them) for structured data.

## Errors and logging

- Catch specific exceptions; never use bare `except:`.
- Do not swallow exceptions silently; log and re-raise or translate to a domain-appropriate error.
- Prefer structured logging; use `logger.exception(...)` when handling unexpected failures.

## Data work

- Prefer `polars` over `pandas` for new dataframe work unless the repo standardizes on pandas.
- When printing a `polars` DataFrame, do not redundantly print both schema and row counts unless explicitly requested.

## Security and config

- Never hardcode secrets/tokens/credentials; load from environment variables or `.env` for local dev.
- Ensure `.env` is excluded via `.gitignore` when relevant.
- Avoid logging secrets or URLs containing secrets.

## Testing expectations

- Add unit tests for new logic (pure functions and business rules first).
- Mock external dependencies (network, databases, filesystem) at the boundary.
- Do not generate "tests" inside production modules; place them in dedicated test files matching repo conventions.

## Pre-PR checklist

- Run Ruff and relevant tests for changed modules.
- Run mypy if the project uses it and types were touched.
- Confirm no debug prints/breakpoints or commented-out code is introduced.
