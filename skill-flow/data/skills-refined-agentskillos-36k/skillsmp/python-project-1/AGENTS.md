# Agent Instructions

Guidelines for AI agents working on this codebase.

## Code Quality

Use ruff for formatting and linting:
```bash
ruff format .
ruff check . --fix
```

Run both before committing changes.

## Package Management

Use uv, not pip:
```bash
uv add <package>    # Add dependency
uv sync             # Install dependencies
uv run <command>    # Run in venv
```

## Type Annotations

Required for all code. Use Python 3.11+ built-in generics:
```python
def process(items: list[str]) -> dict[str, int]: ...
```

Not `List`, `Dict` from typing.

## Testing

```bash
uv run pytest
```
