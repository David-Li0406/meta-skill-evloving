---
name: dqx-code-standards
description: Quick reference for DQX Python code standards
compatibility: opencode
metadata:
  audience: implementation-agents
  domain: python-standards
---

## What I provide

Concise code standards checklist for writing DQX Python code. This skill provides focused guidance without loading the full AGENTS.md document.

---

## Import order

Always follow this order (separated by blank lines):

```python
from __future__ import annotations  # Always first for forward references

import logging  # Standard library
import threading
from collections.abc import Callable, Sequence
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import pyarrow as pa  # Third-party
import sympy as sp

from dqx import functions, setup_logger  # Local imports
from dqx.analyzer import AnalysisReport, Analyzer
from dqx.common import DQXError, ResultKey

if TYPE_CHECKING:  # Circular dependency resolution
    from dqx.orm.repositories import MetricDB
```

**Key rules**:
- `from __future__ import annotations` at the very top
- Use `TYPE_CHECKING` for circular imports
- Use `collections.abc` for abstract types (Callable, Sequence, etc.)
- Prefer specific imports over wildcard imports

---

## Type hints

**STRICT MODE - All functions must have complete type annotations**

```python
def validate_tags(tags: set[str] | frozenset[str] | None) -> frozenset[str]:
    """Validate and convert tags to frozenset."""
    if tags is None:
        return frozenset()
    # ...


# Use Protocol for structural typing
@runtime_checkable
class SqlDataSource(Protocol):
    def execute(self, query: str) -> pa.Table: ...
```

**Key rules**:
- MyPy strict mode: `disallow_untyped_defs = true`
- Target Python 3.11
- Use `|` for union types (not `Union`)
- Use `Protocol` for structural subtyping
- Always use `from __future__ import annotations` at top
- Use `TYPE_CHECKING` for circular imports

---

## Docstrings

**Google style required for all public APIs**

```python
def where(
    self,
    *,
    name: str,
    severity: SeverityLevel = "P1",
    tags: frozenset[str] | set[str] | None = None,
    experimental: bool = False,
) -> AssertionReady:
    """Create an AssertionReady bound to this expression.

    Args:
        name: Descriptive name for the assertion (1–255 characters).
        severity: Severity level (e.g., "P0", "P1", "P2", "P3").
        tags: Optional set of tags for categorization.
        experimental: If True, marks assertion as removable by algorithms.

    Returns:
        AssertionReady: A ready-to-use assertion object.

    Raises:
        ValueError: If name is empty or longer than 255 characters.
    """
```

**Key sections**: Summary, Args, Returns, Raises (when applicable)

---

## Naming conventions

- **Classes**: PascalCase (`MetricProvider`, `AnalysisReport`)
- **Functions/methods**: snake_case (`validate_tags`, `add_assertion`)
- **Constants**: UPPER_SNAKE_CASE (`TAG_PATTERN`)
- **Private**: Leading underscore (`_actual`, `_context`)
- **Type aliases**: PascalCase (`DatasetName`, `ExecutionId`)

---

## Dataclasses

**Use frozen dataclasses for immutable data**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultKey:
    yyyy_mm_dd: datetime.date
    tags: Tags

    def __hash__(self) -> int:
        return hash((self.yyyy_mm_dd, tuple(self.tags)))
```

**Key rule**: Always use `frozen=True` for immutability

---

## Formatting

**Ruff configuration** (enforced by pre-commit):
- Line length: 120 characters
- Indentation: 4 spaces
- Target: Python 3.11
- Docstring convention: Google style

---

## Error handling

Use `returns` library for functional error handling:

```python
from returns.result import Result, Success, Failure


def compute_metric() -> Result[float, str]:
    """Return Success(value) or Failure(error_msg)."""
    try:
        value = perform_calculation()
        return Success(value)
    except Exception as e:
        return Failure(f"Calculation failed: {e}")
```

**Custom exceptions**:
```python
class DQXError(Exception): ...


# Raise with descriptive messages
raise DQXError(f"Invalid tag '{tag}': must contain only alphanumerics")
```

---

## When to use me

Load this skill when:
- Implementing new features (need code standards)
- Fixing code style issues (naming, imports, typing)
- Writing documentation (need docstring format)
- Unsure about formatting conventions
- Need quick standards lookup without full AGENTS.md

---

## Verification

All standards are enforced by pre-commit hooks:
- **ruff format** - Auto-fixes formatting
- **ruff check** - Auto-fixes linting issues
- **mypy** - Type checking (must fix manually)

Run: `uv run pre-commit run --all-files`

---

## Reference

Complete details: **AGENTS.md §code-standards**

This skill provides focused excerpts. For comprehensive guidance including testing patterns, quality gates, and workflows, refer to the full AGENTS.md document.
