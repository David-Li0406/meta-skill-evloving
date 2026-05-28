# Ruff baseline (why this skill uses it)

- `ruff check` covers common bug, style, import, and modernization rules.
- `ruff format` standardizes formatting with minimal configuration.
- This skill expects `uv run task lint_fix` to be the canonical fix step.

Expected commands:
- `uv run task lint_fix`
- `uv run task lint`
- `uv run task test`
