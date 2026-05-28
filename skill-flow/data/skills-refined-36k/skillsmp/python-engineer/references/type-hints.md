# Type Hints Guide

## Basic Types

```python
# Primitives
name: str = "Alice"
age: int = 30
price: float = 19.99
active: bool = True

# None
def log(message: str) -> None:
    print(message)

# Optional (can be None)
from typing import Optional
user: Optional[User] = None  # or User | None (Python 3.10+)
```

## Collections

```python
from collections.abc import Sequence, Mapping, Iterable

# Lists
names: list[str] = ["Alice", "Bob"]

# Dicts
scores: dict[str, int] = {"Alice": 100}

# Sets
tags: set[str] = {"python", "typing"}

# Tuples (fixed length)
point: tuple[int, int] = (10, 20)
record: tuple[str, int, bool] = ("Alice", 30, True)

# Variable length tuple
values: tuple[int, ...] = (1, 2, 3, 4)

# Prefer abstract types for parameters
def process(items: Sequence[str]) -> list[str]:  # accepts list, tuple, etc.
    return [item.upper() for item in items]

def lookup(data: Mapping[str, int], key: str) -> int:  # accepts dict, etc.
    return data[key]
```

## Callable Types

```python
from collections.abc import Callable

# Function type
Handler = Callable[[Request], Response]

def register(handler: Handler) -> None: ...

# With keyword args
from typing import ParamSpec

P = ParamSpec("P")

def decorator(func: Callable[P, int]) -> Callable[P, int]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int:
        return func(*args, **kwargs)
    return wrapper
```

## Generics

```python
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Generic function
def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Bounded TypeVar
from collections.abc import Hashable
H = TypeVar("H", bound=Hashable)

def dedupe(items: Sequence[H]) -> list[H]:
    return list(set(items))

# Generic class
class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value
```

## Union and Literal

```python
from typing import Union, Literal

# Union types
def process(value: int | str) -> str:
    return str(value)

# Literal for specific values
Status = Literal["pending", "active", "completed"]

def update_status(status: Status) -> None: ...
```

## TypedDict

```python
from typing import TypedDict, Required, NotRequired

class UserDict(TypedDict):
    id: str
    name: str
    email: NotRequired[str]  # Optional key

# total=False makes all keys optional by default
class ConfigDict(TypedDict, total=False):
    debug: bool
    timeout: int
    required_key: Required[str]  # This one is required
```

## Protocol (Structural Typing)

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

# Any class with read() method satisfies Readable
def process_file(f: Readable) -> str:
    return f.read()
```

## Type Narrowing

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> None:
    if is_string_list(items):
        # items is now list[str]
        print(", ".join(items))
```

## Self Type (Python 3.11+)

```python
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

    def set_value(self, value: int) -> Self:
        self.value = value
        return self
```

## Overload

```python
from typing import overload

@overload
def get(key: str) -> str: ...
@overload
def get(key: str, default: str) -> str: ...
@overload
def get(key: str, default: None) -> str | None: ...

def get(key: str, default: str | None = None) -> str | None:
    return cache.get(key, default)
```

## mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_any_generics = true
```
