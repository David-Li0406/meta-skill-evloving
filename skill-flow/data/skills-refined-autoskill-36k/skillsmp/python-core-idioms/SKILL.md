---
name: python-core-idioms
description: Modern Python 3.12+ patterns, type hinting, and iconic constructs.
---

# Python Core Idioms (3.12+)

## When to use this skill
- Writing new Python code.
- Refactoring legacy Python scripts.
- Configuring linters (Ruff, MyPy).

## 1. Modern Syntax (3.10 - 3.12+)
- **Type Hinting**: Mandatory for function signatures. Use `list[str]`, `dict[str, int]` (builtin generics) instead of `List`, `Dict` from `typing`.
- **Union Types**: Use `str | None` instead of `Optional[str]`.
- **Pattern Matching**: Use `match / case` for complex control flow (structural pattern matching).
- **Walrus Operator**: Use `:=` for assignment expression in `if/while` conditions when it improves readability (e.g., regex matching).
- **f-strings**: Use for all string interpolation.

## 2. Data Structures
- **Dataclasses**: Use `@dataclass` for data holding classes instead of strict dictionaries or raw classes.
  - `frozen=True` for immutability.
- **TypedDict**: For legacy JSON schemas where classes don't fit.
- **Enum**: Inherit from `StrEnum` (3.11+) if string behavior is needed.

## 3. Project Structure
- **pyproject.toml**: Standard for configuration (ruff, pytest, mypy).
- **Virtual Envs**: Always use a venv or uv/poetry environment.
