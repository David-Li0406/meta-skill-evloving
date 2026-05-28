---
name: python-typing-and-type-hints
description: Use this skill when you need guidance on Python type hints, static typing, and best practices for type safety in your code.
---

# Python Typing and Type Hints Skill

This skill provides expert guidance on Python type hints, static typing with mypy, and best practices for ensuring type safety in your code.

## When to Use This Skill

Use this skill when:
- Adding type hints to existing code
- Designing type-safe APIs
- Configuring mypy for a project
- Working with generic types
- Creating type guards and type predicates
- Writing type stub files
- Debugging type checking errors
- Implementing protocols for duck typing
- Designing self-referential types

## Modern Type Syntax

### Future Annotations (Python 3.7+)
```python
from __future__ import annotations

def process(items: list[str]) -> dict[str, int]:
    """Modern syntax without importing List, Dict."""
    return {item: len(item) for item in items}
```

### Union Types (Python 3.10+)
```python
# Modern
def func(value: str | None = None) -> int | float:
    pass

# Old style
from typing import Optional, Union
def func(value: Optional[str] = None) -> Union[int, float]:
    pass
```

## Type Hints Best Practices

### Basic Type Hints
```python
from typing import Optional, Union, Literal
from pathlib import Path

def process_file(
    path: Path,
    encoding: Optional[str] = None,
    mode: Literal["read", "write"] = "read"
) -> Union[str, bytes]:
    """Process a file with proper type hints."""
    if mode == "read":
        return path.read_text(encoding or "utf-8")
    else:
        return path.read_bytes()
```

### Function Signatures
```python
def greet(name: str, age: int) -> str:
    return f"Hello {name}, age {age}"
```

### Collections
```python
from collections.abc import Sequence, Mapping

def process_items(items: Sequence[str]) -> Mapping[str, int]:
    """Accept any sequence, return any mapping."""
    return {item: len(item) for item in items}
```

### Callable Types
```python
from collections.abc import Callable

def apply(func: Callable[[int], str], value: int) -> str:
    return func(value)
```

## Protocols (Structural Typing)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    """Accepts any object with draw() method."""
    obj.draw()
```

## Generics

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

## Mypy Configuration

```ini
# mypy.ini or setup.cfg
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_unreachable = True
strict_equality = True
```

## Type Checking Workflow

1. **Enable mypy in CI/CD**
2. **Run mypy before committing** (pre-commit hook)
3. **Fix type errors incrementally**
4. **Use `# type: ignore` sparingly** and document why
5. **Add stub files for untyped dependencies**
6. **Keep type hints up to date** when changing code
7. **Use strict mode for new code**

## Common Pitfalls

### ❌ Don't Use Optional When Value is Required
```python
# BAD: Optional when value is always present
def get_user_id(user_id: Optional[int]) -> int:
    if user_id is None:
        raise ValueError("user_id required")
    return user_id

# GOOD: Use non-optional type
def get_user_id(user_id: int) -> int:
    return user_id
```

### ❌ Don't Overuse Any
```python
# BAD: Any hides type errors
def process_data(data: Any) -> Any:
    return data.process()

# GOOD: Use specific type or Protocol
def process_data(data: SupportsProcess) -> Result:
    return data.process()
```

### ❌ Don't Ignore Type Errors
```python
# BAD: Silencing type errors without reason
def complex_function(x: int, y: str) -> dict:  # type: ignore
    return {"result": x + int(y)}

# GOOD: Fix the type error or explain the ignore
def complex_function(x: int, y: str) -> dict[str, int]:
    return {"result": x + int(y)}
```

## References

- PEP 484 (Type Hints): https://peps.python.org/pep-0484/
- PEP 585 (Type Hinting Generics): https://peps.python.org/pep-0585/
- PEP 604 (Allow writing union types as X | Y): https://peps.python.org/pep-0604/
- PEP 673 (Self Type): https://peps.python.org/pep-0673/
- mypy documentation: https://mypy.readthedocs.io/
- Python typing module: https://docs.python.org/3/library/typing.html