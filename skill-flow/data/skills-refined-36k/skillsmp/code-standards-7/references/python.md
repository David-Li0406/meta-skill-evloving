# Python Standards

Language-specific conventions extending the core code standards. Follows PEP 8 with practical refinements.

## Naming

| Type | Convention | Examples |
|------|------------|----------|
| Variables | snake_case | `user_id`, `order_total` |
| Functions | snake_case | `get_user_by_id`, `calculate_total` |
| Classes | PascalCase | `UserService`, `OrderProcessor` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Private | Single underscore prefix | `_internal_helper`, `_cache` |
| "Very Private" | Double underscore (rare) | `__mangled_name` |
| Modules | snake_case | `user_service.py`, `order_utils.py` |

### Boolean Naming

```python
# Yes
is_active = True
has_permission = user.check_permission('admin')
should_retry = attempt_count < MAX_RETRIES

# No
active = True
permission = user.check_permission('admin')
```

---

## Formatting

### Indentation

- 4 spaces (never tabs)
- Continuation lines: align with opening delimiter or use hanging indent

```python
# Aligned with opening delimiter
result = some_function(arg_one, arg_two,
                       arg_three, arg_four)

# Hanging indent (preferred for long arg lists)
result = some_function(
    arg_one,
    arg_two,
    arg_three,
    arg_four,
)
```

### Line Length

- **Target:** 88 characters (Black default)
- **Hard limit:** 100 characters
- **Docstrings/comments:** 72 characters

### Imports

```python
# Standard library
import os
import sys
from collections import defaultdict
from typing import Dict, List, Optional

# Third party
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local
from .models import User
from .services import UserService
from .utils import validate_email
```

One import per line for `from` imports when there are many:

```python
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)
```

---

## Type Hints

### Always Type

- Function parameters
- Return types
- Class attributes

```python
def get_user_by_id(user_id: str) -> Optional[User]:
    """Fetch a user by their ID."""
    ...

def process_orders(orders: List[Order]) -> Dict[str, int]:
    """Process orders and return counts by status."""
    ...
```

### Type Aliases for Clarity

```python
from typing import Dict, List, TypeAlias

UserId: TypeAlias = str
OrderId: TypeAlias = str
UserOrderMap: TypeAlias = Dict[UserId, List[OrderId]]

def get_user_orders(user_id: UserId) -> List[OrderId]:
    ...
```

### Generics (Python 3.9+)

```python
# Modern syntax (3.9+)
def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None

# Compatible syntax (3.8)
from typing import List, Optional, TypeVar
T = TypeVar('T')

def first_or_none(items: List[T]) -> Optional[T]:
    return items[0] if items else None
```

---

## Functions

### Docstrings

Use Google style:

```python
def calculate_discount(
    price: float,
    discount_percent: float,
    max_discount: Optional[float] = None
) -> float:
    """Calculate the discounted price.
    
    Args:
        price: Original price in dollars.
        discount_percent: Discount as a percentage (0-100).
        max_discount: Maximum discount amount, if any.
    
    Returns:
        The final price after discount.
    
    Raises:
        ValueError: If discount_percent is negative or > 100.
    
    Example:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(100, 50, max_discount=30)
        70.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError(f"Invalid discount: {discount_percent}")
    
    discount = price * (discount_percent / 100)
    if max_discount is not None:
        discount = min(discount, max_discount)
    
    return price - discount
```

### Default Arguments

Never use mutable defaults:

```python
# NO - mutable default is shared across calls
def add_item(item: str, items: list = []) -> list:
    items.append(item)
    return items

# YES - use None and create inside
def add_item(item: str, items: Optional[list] = None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Keyword-Only Arguments

Use `*` to require keyword arguments for clarity:

```python
def create_user(
    name: str,
    email: str,
    *,  # Everything after is keyword-only
    send_welcome: bool = True,
    admin: bool = False,
) -> User:
    ...

# Must call with keywords
create_user("Alice", "alice@example.com", send_welcome=False)
```

---

## Classes

### Dataclasses for Data

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

# With immutability
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

### Pydantic for Validation

```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

### Property Decorators

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
    
    @property
    def area(self) -> float:
        return self._width * self._height
    
    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
```

---

## Error Handling

### Specific Exceptions

```python
# Yes - specific
try:
    user = get_user(user_id)
except UserNotFoundError:
    return None
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise

# No - too broad
try:
    user = get_user(user_id)
except Exception:
    return None
```

### Custom Exceptions

```python
class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            f"{resource} with id '{identifier}' not found",
            code="NOT_FOUND"
        )

class ValidationError(AppError):
    """Raised when validation fails."""
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Validation failed for '{field}': {reason}",
            code="VALIDATION_ERROR"
        )
```

### Context Managers

```python
# For resource cleanup
with open('file.txt') as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{name} took {elapsed:.2f}s")

with timer("data processing"):
    process_data()
```

---

## Comprehensions & Generators

### List Comprehensions

Use for simple transformations:

```python
# Yes - clear
squares = [x ** 2 for x in range(10)]
active_users = [u for u in users if u.is_active]

# No - too complex, use a loop or function
result = [
    transform(x) 
    for x in data 
    if condition1(x) and condition2(x)
    for y in x.items
    if y.is_valid
]
```

### Generators for Large Data

```python
# Memory efficient for large datasets
def read_large_file(path: str):
    with open(path) as f:
        for line in f:
            yield line.strip()

# Generator expression
sum_of_squares = sum(x ** 2 for x in range(1000000))
```

### Dictionary Comprehensions

```python
# Transform dict
upper_keys = {k.upper(): v for k, v in data.items()}

# Filter dict
active = {k: v for k, v in users.items() if v.is_active}

# From pairs
user_map = {user.id: user for user in users}
```

---

## Testing

### Pytest Style

```python
import pytest
from myapp.services import UserService

class TestUserService:
    """Tests for UserService."""
    
    def test_create_user_with_valid_data(self):
        """Should create user when data is valid."""
        service = UserService()
        user = service.create(name="Alice", email="alice@test.com")
        
        assert user.name == "Alice"
        assert user.email == "alice@test.com"
        assert user.is_active is True
    
    def test_create_user_raises_on_invalid_email(self):
        """Should raise ValidationError for invalid email."""
        service = UserService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.create(name="Alice", email="not-an-email")
        
        assert "email" in str(exc_info.value)

@pytest.fixture
def user_service():
    """Provide a configured UserService."""
    return UserService(db=mock_database())
```

### Parameterized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected
```
