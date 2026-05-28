---
name: python
description: Python patterns for backend development, testing, and async programming. Use when writing Python code.
---

# Python

## Type Hints & Dataclasses

```python
from dataclasses import dataclass
from typing import Optional, TypeVar, Generic

@dataclass
class User:
    name: str
    email: str
    id: Optional[str] = None

# Generic types
T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Result(Generic[T, E]):
    value: Optional[T] = None
    error: Optional[E] = None

    @property
    def ok(self) -> bool:
        return self.error is None
```

## Testing (pytest)

```python
import pytest
from unittest.mock import Mock, AsyncMock, patch

# Fixtures
@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def user_service(mock_db):
    return UserService(mock_db)

# Parameterized tests
@pytest.mark.parametrize("email,valid", [
    ("test@example.com", True),
    ("invalid", False),
])
def test_validate_email(email, valid):
    assert validate_email(email) == valid

# Async tests
@pytest.mark.asyncio
async def test_fetch_user(user_service, mock_db):
    mock_db.find.return_value = {"id": "1", "name": "Test"}
    result = await user_service.get("1")
    assert result.name == "Test"

# Mocking
@patch("myapp.services.external_api")
def test_with_mock(mock_api):
    mock_api.fetch.return_value = {"status": "ok"}
```

## Async Patterns

```python
import asyncio
from contextlib import asynccontextmanager

# Gather with error handling
async def fetch_all(urls: list[str]) -> list[Result]:
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Async context manager
@asynccontextmanager
async def get_connection():
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)

# Semaphore for rate limiting
sem = asyncio.Semaphore(10)
async def limited_fetch(url):
    async with sem:
        return await fetch(url)
```

## Error Handling

```python
# Custom exceptions
class AppError(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code

class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404)

# Result pattern
def find_user(id: str) -> Result[User, str]:
    user = db.users.get(id)
    if not user:
        return Result(error="User not found")
    return Result(value=user)
```

## Best Practices

- Use type hints everywhere, validate with mypy
- Prefer dataclasses/Pydantic for data structures
- Use pytest fixtures for test setup
- Handle async errors with try/except in gather
- Use `logging` module, not print
- Virtual environments mandatory (venv/uv)
- Format with ruff/black, lint with ruff
