---
id: python-type-hints
name: "Python Type Hints"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Python Type Hints

## Overview

Type hints enable static type checking, better IDE support, and self-documenting code. This methodology covers modern Python typing patterns, mypy configuration, and best practices for type-safe Python development.

## When to Use

- All Python projects (Python 3.9+)
- Public APIs and function signatures
- Complex data structures
- Code that will be maintained long-term
- Libraries and shared packages

## Key Principles

1. **Type all public interfaces** - Functions, methods, class attributes
2. **Use modern syntax** - `list[int]` not `List[int]` (Python 3.9+)
3. **Prefer `|` over Optional** - `str | None` not `Optional[str]`
4. **Be specific** - `list[User]` not `list`
5. **Use Protocol for duck typing** - Structural subtyping

## Best Practices

### Basic Type Hints

```python
# Variables
name: str = "John"
age: int = 30
is_active: bool = True
score: float = 95.5

# Collections (Python 3.9+)
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
unique_ids: set[int] = {1, 2, 3}
coordinates: tuple[float, float] = (10.5, 20.3)

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}"


def process_items(items: list[str]) -> None:
    for item in items:
        print(item)


def calculate_total(prices: list[float]) -> float:
    return sum(prices)
```

### Optional and Union Types

```python
# Python 3.10+ - use | for union
def get_user(user_id: int) -> User | None:
    """Return user or None if not found."""
    return User.objects.filter(id=user_id).first()


def process_value(value: int | str) -> str:
    """Accept int or str, return str."""
    return str(value)


# Multiple optional parameters
def create_user(
    email: str,
    name: str,
    *,
    age: int | None = None,
    role: str | None = None,
) -> User:
    """Create user with optional fields."""
    ...
```

### Generic Types

```python
from typing import TypeVar, Generic
from collections.abc import Sequence, Mapping

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


# Generic function
def first(items: Sequence[T]) -> T | None:
    """Return first item or None."""
    return items[0] if items else None


def get_value(mapping: Mapping[K, V], key: K, default: V) -> V:
    """Get value from mapping with default."""
    return mapping.get(key, default)


# Generic class
class Repository(Generic[T]):
    """Generic repository pattern."""

    def __init__(self, model_class: type[T]):
        self.model_class = model_class

    def get(self, id: int) -> T | None:
        raise NotImplementedError

    def list(self) -> list[T]:
        raise NotImplementedError

    def create(self, data: dict) -> T:
        raise NotImplementedError


# Usage
class UserRepository(Repository[User]):
    def get(self, id: int) -> User | None:
        return User.objects.filter(id=id).first()
```

### Callable Types

```python
from collections.abc import Callable, Awaitable


# Function that takes callback
def apply_operation(
    values: list[int],
    operation: Callable[[int], int],
) -> list[int]:
    """Apply operation to each value."""
    return [operation(v) for v in values]


# Usage
def double(x: int) -> int:
    return x * 2


result = apply_operation([1, 2, 3], double)


# Async callable
AsyncHandler = Callable[[Request], Awaitable[Response]]


async def handle_request(
    request: Request,
    handler: AsyncHandler,
) -> Response:
    return await handler(request)


# Callable with optional args
Callback = Callable[[str, int], bool] | None
```

### TypedDict for Structured Dicts

```python
from typing import TypedDict, NotRequired, Required


class UserData(TypedDict):
    """Typed dictionary for user data."""
    id: int
    email: str
    name: str
    is_active: NotRequired[bool]  # Optional field


class CreateUserData(TypedDict, total=False):
    """All fields optional by default."""
    email: Required[str]  # But this one required
    name: str
    age: int


def process_user(data: UserData) -> None:
    """Type-safe dict access."""
    print(data["email"])  # OK - email is required
    print(data.get("is_active", True))  # OK - optional field


# Usage
user: UserData = {
    "id": 1,
    "email": "test@example.com",
    "name": "Test",
    # is_active is optional
}
```

### Protocol for Duck Typing

```python
from typing import Protocol, runtime_checkable


class Sendable(Protocol):
    """Protocol for objects that can send messages."""

    def send(self, message: str) -> bool:
        """Send a message."""
        ...


class Closeable(Protocol):
    """Protocol for closeable resources."""

    def close(self) -> None:
        ...


# Classes don't need to inherit - structural subtyping
class EmailClient:
    def send(self, message: str) -> bool:
        # Send email
        return True


class SMSClient:
    def send(self, message: str) -> bool:
        # Send SMS
        return True


def notify(client: Sendable, message: str) -> bool:
    """Works with any Sendable."""
    return client.send(message)


# Both work - they implement the protocol
notify(EmailClient(), "Hello")
notify(SMSClient(), "Hello")


# Runtime checkable protocol
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None:
        ...


def is_drawable(obj: object) -> bool:
    return isinstance(obj, Drawable)
```

### Type Aliases

```python
from typing import TypeAlias

# Simple alias
UserId: TypeAlias = int
Email: TypeAlias = str

# Complex alias
UserDict: TypeAlias = dict[str, str | int | bool]
Handler: TypeAlias = Callable[[Request], Response]

# Generic alias
Result: TypeAlias = tuple[T, str | None]


def get_user(user_id: UserId) -> Result[User]:
    """Return user and optional error message."""
    try:
        user = User.objects.get(id=user_id)
        return (user, None)
    except User.DoesNotExist:
        return (None, "User not found")  # type: ignore
```

### Type Guards

```python
from typing import TypeGuard


def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """Check if all items are strings."""
    return all(isinstance(x, str) for x in val)


def process(items: list[object]) -> None:
    if is_string_list(items):
        # Type narrowed to list[str]
        for item in items:
            print(item.upper())  # str method OK


# Assertion function
def assert_not_none(val: T | None) -> T:
    """Assert value is not None."""
    if val is None:
        raise ValueError("Value cannot be None")
    return val


# Usage
user: User | None = get_user(1)
verified_user = assert_not_none(user)  # Type is User
```

### mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
strict = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

# Third-party packages without stubs
[[tool.mypy.overrides]]
module = "some_untyped_package.*"
ignore_missing_imports = true
```

### Django Type Hints

```python
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet


class User(models.Model):
    email: models.EmailField = models.EmailField(unique=True)
    name: models.CharField = models.CharField(max_length=100)

    # Typed related manager
    orders: "models.Manager[Order]"


def get_active_users() -> QuerySet[User]:
    """Return queryset of active users."""
    return User.objects.filter(is_active=True)


def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """View with typed parameters."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, "user_detail.html", {"user": user})
```

## Anti-patterns

### Avoid: Using `Any` Excessively

```python
# BAD - defeats purpose of typing
def process(data: Any) -> Any:
    return data.something()

# GOOD - use specific types or generics
def process(data: UserData) -> ProcessedData:
    return ProcessedData(data.name)
```

### Avoid: Ignoring Type Errors

```python
# BAD - hiding real issues
result = some_function()  # type: ignore

# GOOD - fix the type issue or use proper assertion
result = some_function()
if result is None:
    raise ValueError("Expected result")
```

### Avoid: Inconsistent Optional Handling

```python
# BAD - implicit None
def get_user(id: int) -> User:  # Can return None!
    return User.objects.filter(id=id).first()

# GOOD - explicit
def get_user(id: int) -> User | None:
    return User.objects.filter(id=id).first()
```

## References

- [Python typing Documentation](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 604 - Union Syntax](https://peps.python.org/pep-0604/)
- [django-stubs](https://github.com/typeddjango/django-stubs)
