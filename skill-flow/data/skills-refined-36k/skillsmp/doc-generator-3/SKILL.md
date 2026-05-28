---
name: doc-generator
description: Add Google-style docstrings to modules. Use for documentation requests.
allowed-tools: Read, Glob, Grep, Edit
---

# Documentation Generator

Add Google-style docstrings to cvp/ modules.

## Format

```python
def func(param1: int, param2: str) -> bool:
    """Brief description.

    Args:
        param1: Description.
        param2: Description.

    Returns:
        Description.

    Raises:
        ValueError: When invalid.
    """
```

## Scope

- **Required**: All public functions, classes, methods
- **Optional**: Private functions (`_` prefix) - brief only
- **Skip**: `__init__.py` re-exports, simple getters/setters

## Line Width

All docstrings and comments must not exceed **88 characters** per line.

## Validation

Ensure docstrings match type hints.
