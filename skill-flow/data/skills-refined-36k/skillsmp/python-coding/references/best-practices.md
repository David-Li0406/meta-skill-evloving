# Python Best Practices

## Code Style (PEP 8)

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Name mangling**: `__double_leading_underscore`

### Formatting

- Use 4 spaces for indentation (never tabs)
- Maximum line length: 88 characters (Black default) or 79 (strict PEP 8)
- Two blank lines before top-level definitions
- One blank line between methods in a class

### Imports

```python
# Standard library imports
import os
import sys
from typing import Optional

# Third-party imports
import requests
from pydantic import BaseModel

# Local imports
from myproject.utils import helper
```

## Type Hints

### Basic Type Annotations

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def process_items(items: list[str], count: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items[:count]}
```

### Complex Types

```python
from typing import Optional, Union, TypeVar, Generic

# Optional types
def find_user(user_id: int) -> Optional[User]:
    ...

# Union types (Python 3.10+)
def parse_input(value: str | int) -> str:
    ...

# Generics
T = TypeVar('T')
class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
```

## Documentation Strings

### Function Docstrings

```python
def calculate_total(items: list[float], tax_rate: float = 0.1) -> float:
    """
    Calculate the total price including tax.

    Args:
        items: List of item prices.
        tax_rate: Tax rate as a decimal (default: 0.1 for 10%).

    Returns:
        Total price with tax applied.

    Raises:
        ValueError: If tax_rate is negative.
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### Class Docstrings

```python
class OrderProcessor:
    """
    Processes customer orders and manages inventory.

    Attributes:
        inventory: Current inventory levels.
        pending_orders: Queue of orders awaiting processing.

    Example:
        >>> processor = OrderProcessor()
        >>> processor.add_order(Order(item="widget", quantity=5))
        >>> processor.process_all()
    """
```

## Error Handling

### Use Specific Exceptions

```python
# Good: Specific exception handling
try:
    value = data["key"]
except KeyError:
    value = default_value

# Avoid: Catching all exceptions
try:
    value = data["key"]
except Exception:  # Too broad!
    value = default_value
```

### Custom Exceptions

```python
class ValidationError(Exception):
    """Raised when data validation fails."""
    
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")
```

### Context Managers for Cleanup

```python
from contextlib import contextmanager

@contextmanager
def database_transaction(connection):
    """Ensure transaction is committed or rolled back."""
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
```

## Testing Practices

### Test Structure

```python
import pytest

class TestUserService:
    """Tests for the UserService class."""

    @pytest.fixture
    def user_service(self):
        """Create a UserService instance for testing."""
        return UserService(database=MockDatabase())

    def test_create_user_with_valid_data(self, user_service):
        """Should create a new user when data is valid."""
        result = user_service.create_user("alice", "alice@example.com")
        assert result.username == "alice"
        assert result.email == "alice@example.com"

    def test_create_user_with_duplicate_email_raises_error(self, user_service):
        """Should raise ValueError when email already exists."""
        user_service.create_user("alice", "alice@example.com")
        with pytest.raises(ValueError, match="Email already registered"):
            user_service.create_user("bob", "alice@example.com")
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

def test_fetch_user_data():
    """Should return user data from external API."""
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    
    with patch("requests.get", return_value=mock_response):
        result = fetch_user_data(user_id=1)
        assert result["name"] == "Alice"
```

