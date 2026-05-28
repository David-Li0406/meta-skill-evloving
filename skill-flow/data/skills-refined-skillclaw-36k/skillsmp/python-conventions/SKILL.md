---
name: python-conventions
description: Enforce Python 3.12+ coding conventions when editing or creating Python code. Use for tasks that touch .py files, focusing on style, naming, typing, error handling, and performance-oriented idioms.
---

# Python Conventions

## Overview

Apply consistent Python conventions for code edits and new code. These conventions ensure readability, maintainability, and consistency across Python 3.12+ projects. Prefer existing project patterns unless they conflict with the conventions below.

For complete project workflows including tooling setup, see the `python-project` skill.

## Core Conventions

**Language Features:**
- Use Python 3.12+ features and standard library first
- Use built-in generics: `list[X]`, `dict[K, V]`, `X | Y` for unions
- Use `match`/`case` and walrus operator (`:=`) only when they improve readability

**Code Quality:**
- Follow PEP 8 for style and layout (see `references/pep8.md` for summary)
- Write descriptive names and single-responsibility functions
- Prefer readability and simplicity; follow "The Zen of Python" (`import this`)

**Modern Python Idioms:**
- Use `pathlib.Path` instead of `os.path` for file operations
- Use f-strings for string formatting
- Use context managers (`with` statements) for resource handling
- Prefer `dataclasses` or Pydantic for data models
- Use `isinstance(x, int | float)` instead of `isinstance(x, (int, float))` (UP038)

**Documentation:**
- Use Google- or NumPy-style docstrings for public APIs
- Write comments about "why" rather than "what"

**Error Handling:**
- Use specific exception types; avoid bare `except`
- Create custom exceptions for domain errors
- Include enough context to debug without leaking secrets

## Style Guidelines

**Indentation and Line Length:**
- Indent with 4 spaces; never use tabs
- Keep lines at or under 79 characters (or project standard if different)
- Use implicit line continuation in parentheses/brackets/braces

**Naming Conventions:**
- Variables and functions: `snake_case`
- Classes: `CamelCase`
- Constants: `UPPER_CASE_WITH_UNDERSCORES`
- Private attributes: prefix with single underscore `_private`

**Import Organization:**
- One import per line (except `from ... import ...` forms)
- Order: standard library, third-party, local application
- Separate groups with blank lines
- Example:
  ```python
  import os
  from pathlib import Path

  import requests
  from loguru import logger

  from myapp.utils import helper
  ```

**Whitespace and Layout:**
- Two blank lines around top-level functions and classes
- One blank line around class methods
- Use blank lines sparingly within functions for logical sections
- Avoid extraneous whitespace inside brackets or before commas

## Type Hints

**When to Add Types:**
- Always add type hints for new code
- Add types when updating existing interfaces
- Use `from __future__ import annotations` for forward references

**Modern Type Syntax (Python 3.12+):**
```python
def process_items(items: list[str], limit: int | None = None) -> dict[str, int]:
    """Process items and return counts."""
    result: dict[str, int] = {}
    for item in items[:limit]:
        result[item] = result.get(item, 0) + 1
    return result
```

**Key Patterns:**
- Use `list[X]`, `dict[K, V]`, `set[X]` instead of `List`, `Dict`, `Set`
- Use `X | Y | None` instead of `Optional[X]` or `Union[X, Y]`
- Use `type` aliases for complex types: `UserID = int | str`
- Use `Protocol` for structural subtyping when appropriate

## Performance Guidelines

**Memory Efficiency:**
- Use generators and iterators for large datasets
- Prefer `itertools` and `functools` for common patterns
- Use comprehensions for simple transformations

**I/O Operations:**
- Use `async`/`await` for I/O-bound workloads
- Use context managers to ensure resource cleanup
- Consider connection pooling for repeated operations

**When Performance Matters:**
- Profile hot paths before optimizing
- Use appropriate data structures (`set` for membership, `dict` for lookups)
- Consider `lru_cache` for expensive pure functions

## When to Read References

- **PEP 8 details**: See `references/pep8.md` for comprehensive style guide
- **Project setup**: See `python-project` skill for tooling and workflows
