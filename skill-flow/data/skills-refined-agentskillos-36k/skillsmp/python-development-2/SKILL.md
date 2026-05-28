---
name: python-development
description: Use when writing Python code for clean, performant, and idiomatic implementations
---

# Python Development

Guidelines for clean, performant, and idiomatic Python code.

## When to Use

- Writing new Python modules
- Refactoring Python code
- Implementing Python best practices
- Code review of Python files

## Core Principles

- **Idiomatic Python** - Follow PEP 8 and community conventions
- **Type Safety** - Use type hints throughout
- **Test-Driven** - Write tests alongside implementation
- **Explicit Error Handling** - Fail fast with clear messages

## Code Standards

### Type Hints
```python
from typing import Callable, TypeVar

T = TypeVar('T')

def process(items: list[str], transform: Callable[[str], T]) -> list[T]:
    """Process items with a transformation function."""
    return [transform(item) for item in items]
```

### Docstrings (Google Style)
```python
def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Calculate total price including tax.

    Args:
        items: List of items with 'price' and 'quantity' keys.
        tax_rate: Tax rate as decimal (0.1 = 10%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If tax_rate is negative.
    """
    if tax_rate < 0:
        raise ValueError("tax_rate cannot be negative")
    subtotal = sum(i['price'] * i['quantity'] for i in items)
    return subtotal * (1 + tax_rate)
```

## Best Practices Checklist

- [ ] Type hints on all function signatures
- [ ] Docstrings on public functions/classes
- [ ] PEP 8 compliant (use ruff/black)
- [ ] No mutable default arguments
- [ ] Context managers for resources
- [ ] Generators for memory efficiency
- [ ] Custom exceptions for domain errors
- [ ] Test coverage > 90%
- [ ] mypy --strict passes

## Patterns

### Decorator with Type Safety
```python
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def retry(attempts: int = 3) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator with configurable attempts."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == attempts - 1:
                        raise
            raise RuntimeError("Unreachable")
        return wrapper
    return decorator
```

### Protocol for Structural Typing
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """Protocol for serializable objects."""
    def to_dict(self) -> dict: ...
    def from_dict(cls, data: dict) -> 'Serializable': ...
```

### Context Manager
```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def timer(name: str) -> Iterator[None]:
    """Context manager to time code execution."""
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.4f}s")
```

### Custom Exceptions
```python
class ValidationError(Exception):
    """Base exception for validation errors."""
    pass

class InvalidEmailError(ValidationError):
    """Raised when email format is invalid."""
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Invalid email: {email}")
```

## Testing

### Test Structure (AAA Pattern)
```python
import pytest

class TestUserService:
    def test_create_user_with_valid_data(self) -> None:
        # Arrange
        service = UserService()
        data = {"email": "test@example.com", "name": "Test"}

        # Act
        user = service.create(data)

        # Assert
        assert user.email == "test@example.com"
        assert user.name == "Test"

    def test_create_user_with_invalid_email_raises(self) -> None:
        service = UserService()

        with pytest.raises(InvalidEmailError, match="Invalid email"):
            service.create({"email": "invalid", "name": "Test"})

    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("invalid", False),
        ("", False),
    ])
    def test_email_validation(self, email: str, expected: bool) -> None:
        assert validate_email(email) == expected
```

### Fixtures
```python
@pytest.fixture
def db_session():
    """Provide a database session for tests."""
    session = create_session()
    yield session
    session.rollback()
    session.close()
```

## Performance

### Memory-Efficient Processing
```python
from typing import Iterator

def process_large_file(path: str) -> Iterator[dict]:
    """Process file without loading into memory."""
    with open(path) as f:
        for line in f:
            yield parse_line(line)
```

### Use Generators
```python
# Memory-efficient
def squares(n: int) -> Iterator[int]:
    for i in range(n):
        yield i ** 2

# Instead of
def squares_list(n: int) -> list[int]:
    return [i ** 2 for i in range(n)]  # Allocates full list
```

## Common Anti-Patterns

### Avoid Mutable Defaults
```python
# ❌ Wrong
def append(item, lst=[]):
    lst.append(item)
    return lst

# ✅ Correct
def append(item, lst: list | None = None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Use Explicit Imports
```python
# ❌ Avoid
from module import *

# ✅ Prefer
from module import specific_function, SpecificClass
```

## Decision Priority

1. **Testability** - Can it be tested in isolation?
2. **Readability** - Will others understand it?
3. **Consistency** - Matches existing patterns?
4. **Simplicity** - Least complex solution?
5. **Reversibility** - Easy to change later?
