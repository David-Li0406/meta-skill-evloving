---
name: python-type-hints
description: Type annotations, static typing with mypy, generic types, protocols
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: typing
---

## What I do

I provide guidance on type hints and static typing in Python, including:

- Basic type hints (list, dict, tuple, Optional, Union)
- Type unions and intersection types (Literal, TypeGuard)
- Generic types and TypeVar
- Protocol types (structural subtyping)
- Self types and recursive types
- Callable and function types
- mypy configuration and strict mode
- Type narrowing and isinstance checks
- Type stub files for third-party libraries

## When to use me

Use me when:
- Adding type hints to existing code
- Designing type-safe APIs
- Configuring mypy for a project
- Working with generic types
- Creating type guards and type predicates
- Writing type stub files
- Debugging type checking errors
- Implementing protocols for duck typing
- Designing self-referential types

## Best Practices

### ✅ Basic Type Hints

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

### ✅ Use Modern Union Syntax (Python 3.10+)

```python
# Python 3.10+ union syntax
def process_value(value: str | int | float) -> str:
    """Process value using modern union syntax."""
    return str(value)

# Equivalent to old syntax (Python < 3.10)
from typing import Union

def process_value(value: Union[str, int, float]) -> str:
    """Process value using old union syntax."""
    return str(value)
```

### ✅ Use TypeGuard for Type Narrowing

```python
from typing import Protocol, TypeGuard

class SupportsRead(Protocol):
    """Protocol for readable objects."""
    def read(self, size: int = -1) -> bytes: ...

def is_binary_data(obj: object) -> TypeGuard[SupportsRead]:
    """Type guard for binary data objects."""
    return isinstance(obj, (bytes, bytearray, SupportsRead))

def process_data(data: SupportsRead | str) -> bytes:
    """Process data with type narrowing."""
    if is_binary_data(data):
        return data.read()
    return data.encode()
```

### ✅ Use Protocols for Structural Subtyping

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> None: ...

def render(objects: list[Drawable]) -> None:
    """Render all drawable objects."""
    for obj in objects:
        obj.draw()

# Usage with runtime checking
class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def can_draw(obj: object) -> bool:
    """Check if object is drawable."""
    return isinstance(obj, Drawable)
```

### ✅ Generic Types with TypeVar

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Container(Generic[T]):
    """Generic container for any type."""

    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        """Get the stored value."""
        return self.value

# Bounded TypeVar
class Animal:
    pass

class Dog(Animal):
    pass

A = TypeVar("A", bound=Animal)

def adopt(pet: A) -> A:
    """Adopt an animal."""
    return pet

# Usage
container_int = Container(42)
container_str = Container("hello")
```

### ✅ Self Types for Fluent Interfaces

```python
from typing import Self

class Builder:
    """Builder pattern with Self type."""

    def __init__(self) -> None:
        self.items: list[str] = []

    def add_item(self, item: str) -> Self:
        """Add an item and return self for chaining."""
        self.items.append(item)
        return self

    def build(self) -> list[str]:
        """Build and return the list."""
        return self.items

# Usage
result = Builder().add_item("a").add_item("b").build()
```

### ✅ Callable Types

```python
from typing import Callable

def apply_function(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    """Apply a function to two integers."""
    return func(a, b)

# With variable arguments
def process_data(
    processor: Callable[..., str],
    *args: object
) -> str:
    """Process data with a callable."""
    return processor(*args)
```

### ✅ Type Stubs for Third-Party Libraries

```python
# mymodule_stubs.pyi
# Type stub file for mymodule

from typing import List, Optional

def process_items(items: List[str]) -> Optional[dict]:
    """Process items and return optional dict."""
    ...

class DataProcessor:
    """Data processor class."""
    def __init__(self, config: dict) -> None: ...
    def run(self) -> None: ...
```

### ✅ ParamSpec and Concatenate (Python 3.10+)

```python
from typing import ParamSpec, Concatenate

P = ParamSpec("P")

def decorator(
    func: Callable[Concatenate[int, P], int]
) -> Callable[P, int]:
    """Decorator with parameter specification."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int:
        return func(42, *args, **kwargs)
    return wrapper

@decorator
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y
```

## Type Narrowing

### ✅ Use isinstance for Type Narrowing

```python
def process(value: int | str | list[str]) -> str:
    """Process value with type narrowing."""
    if isinstance(value, int):
        return f"Number: {value}"
    elif isinstance(value, str):
        return f"String: {value}"
    else:
        # value is list[str] here
        return f"List: {', '.join(value)}"
```

### ✅ Use Literal for Precise Values

```python
from typing import Literal

def set_status(status: Literal["pending", "active", "completed"]) -> None:
    """Set status to one of the literal values."""
    pass

# Works
set_status("active")

# Type error (mypy catches this)
set_status("invalid")
```

## Mypy Configuration

### ✅ Setup mypy for Your Project

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

[pytest]
ignore_missing_imports = True

[tests]
no_warn_unused_ignores = True
```

### ✅ Use Type Comments for Legacy Code

```python
# Type comments for Python 3.5-3.8 compatibility

def calculate_total(x, y):
    # type: (int, float) -> float
    """Calculate total with type comments."""
    return x + y
```

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

## Advanced Type Patterns

### ✅ Recursive Types

```python
from typing import Union, TypedDict

class Node(TypedDict):
    """Recursive tree node."""
    value: int
    left: Union["Node", None]
    right: Union["Node", None]

def sum_tree(node: Union[Node, None]) -> int:
    """Sum all values in tree."""
    if node is None:
        return 0
    return node["value"] + sum_tree(node["left"]) + sum_tree(node["right"])
```

### ✅ TypedDict for Dictionary Structure

```python
from typing import TypedDict, Required, NotRequired

class User(TypedDict):
    """User structure definition."""
    id: Required[int]
    name: Required[str]
    email: Required[str]
    age: NotRequired[int]

def process_user(user: User) -> None:
    """Process user with guaranteed structure."""
    print(f"User: {user['name']} ({user['email']})")
```

## Type Checking Workflow

1. **Enable mypy in CI/CD**
2. **Run mypy before committing** (pre-commit hook)
3. **Fix type errors incrementally**
4. **Use `# type: ignore` sparingly** and document why
5. **Add stub files for untyped dependencies**
6. **Keep type hints up to date** when changing code
7. **Use strict mode for new code**

## References

- PEP 484 (Type Hints): https://peps.python.org/pep-0484/
- PEP 585 (Type Hinting Generics): https://peps.python.org/pep-0585/
- PEP 604 (Allow writing union types as X | Y): https://peps.python.org/pep-0604/
- PEP 673 (Self Type): https://peps.python.org/pep-0673/
- PEP 646 (Variadic Generics): https://peps.python.org/pep-0646/
- mypy documentation: https://mypy.readthedocs.io/
- Python typing module: https://docs.python.org/3/library/typing.html
