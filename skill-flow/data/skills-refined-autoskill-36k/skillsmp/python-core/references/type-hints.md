# Type Hints in Python

Modern Python uses type hints for better IDE support, documentation, and error catching.

## Basic Types

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
price: float = 19.99
is_active: bool = True
items: list[str] = ["apple", "banana"]
scores: dict[str, int] = {"alice": 95, "bob": 87}
```

## Optional and Union

```python
from typing import Optional, Union

# Python 3.10+
def process(data: str | None = None) -> int | float:
    pass

# Older syntax
def process_old(data: Optional[str] = None) -> Union[int, float]:
    pass
```

## Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content = content
    
    def get(self) -> T:
        return self.content

box = Box[int](42)
```

## Protocol (Structural Subtyping)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()
```

## TypedDict

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str

user: User = {"name": "Alice", "age": 30, "email": "alice@example.com"}
```

## Literal

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass
```

## Mypy Configuration

```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## Best Practices

1. Add type hints to all public functions
2. Use `mypy` for static type checking
3. Prefer `str | None` over `Optional[str]` (Python 3.10+)
4. Use `list[T]` over `List[T]` (Python 3.9+)
5. Leverage Pydantic for runtime validation
