---
name: testing-python
description: |
  Python testing best practices with pytest. Covers unit, integration, async tests, mocking, fixtures.
  Triggers: "write tests", "add tests", "test coverage", "pytest", "unit test", "integration test"
---

# Python Testing

Modern Python testing with pytest ecosystem.

## Tooling

| Tool | Purpose |
|------|-------|
| **pytest** | Testing framework |
| **pytest-cov** | Coverage reporting |
| **pytest-asyncio** | Async test support |
| **pytest-mock** | Mocking utilities |
| **respx** | HTTP mocking for httpx |

## Quick Start

### Install

```bash
uv add --dev pytest pytest-cov pytest-asyncio pytest-mock
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--strict-config",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### Directory Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── service.py
└── tests/
    ├── conftest.py          # Shared fixtures
    ├── unit/
    │   └── test_service.py
    └── integration/
        └── test_api.py
```

## Patterns

### Basic Test

```python
# tests/unit/test_calculator.py
import pytest
from mypackage.calculator import add, divide

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Fixtures

```python
# tests/conftest.py
import pytest
from mypackage.database import Database

@pytest.fixture
def sample_user():
    """Simple data fixture."""
    return {"id": 1, "name": "Test User", "email": "test@example.com"}


@pytest.fixture
def db():
    """Setup/teardown fixture."""
    database = Database(":memory:")
    database.connect()
    yield database
    database.disconnect()


@pytest.fixture(scope="module")
def expensive_resource():
    """Shared across module (use sparingly)."""
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()
```

### Async Tests

```python
import pytest
from mypackage.api import fetch_user

# With asyncio_mode = "auto", no decorator needed
async def test_fetch_user():
    user = await fetch_user(1)
    assert user["id"] == 1


# Async fixture
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client


async def test_with_async_client(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
```

### Mocking

```python
import pytest
from unittest.mock import Mock, patch

def test_with_mock(mocker):
    """Using pytest-mock."""
    mock_api = mocker.patch("mypackage.api.fetch_data")
    mock_api.return_value = {"data": "test"}
    
    result = fetch_data()
    
    assert result["data"] == "test"
    mock_api.assert_called_once()


@patch("mypackage.api.requests.get")
def test_with_patch(mock_get):
    """Using unittest.mock."""
    mock_get.return_value.json.return_value = {"id": 1}
    
    result = fetch_user(1)
    
    assert result["id"] == 1
```

### HTTP Mocking (httpx)

```python
import pytest
import httpx
import respx

@respx.mock
async def test_api_call():
    respx.get("https://api.example.com/users/1").respond(
        json={"id": 1, "name": "John"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users/1")

    assert response.json()["name"] == "John"


# Or as fixture
@pytest.fixture
def mock_api():
    with respx.mock:
        yield respx


async def test_with_fixture(mock_api):
    mock_api.get("https://api.example.com/data").respond(json={"ok": True})
    # ... test code
```

### Exception Testing

```python
import pytest

def test_raises_value_error():
    with pytest.raises(ValueError, match="invalid input"):
        process_data("bad")


def test_exception_details():
    with pytest.raises(ValueError) as exc_info:
        process_data("bad")
    
    assert "invalid" in str(exc_info.value)
    assert exc_info.value.args[0] == "invalid input"
```

### Markers

```python
import pytest

@pytest.mark.slow
def test_complex_calculation():
    """Run with: pytest -m slow"""
    result = heavy_computation()
    assert result is not None


@pytest.mark.integration
async def test_database_connection():
    """Run with: pytest -m integration"""
    async with get_connection() as conn:
        assert await conn.ping()


@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass


@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass
```

## Running Tests

```bash
# Run all
pytest

# With coverage
pytest --cov=src --cov-report=term-missing

# Specific file/test
pytest tests/test_users.py
pytest tests/test_users.py::test_create_user

# Verbose
pytest -v

# Stop on first failure
pytest -x

# Run only marked tests
pytest -m slow
pytest -m "not slow"

# Run tests matching pattern
pytest -k "test_user"

# Show print statements
pytest -s

# Parallel execution (pytest-xdist)
pytest -n auto
```

## Coverage

```bash
# Terminal report
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Fail if below threshold
pytest --cov=src --cov-fail-under=80
```

## Best Practices

### DO:
- One assertion per test (usually)
- Descriptive test names: `test_<what>_<condition>_<expected>`
- Use fixtures for setup/teardown
- Test edge cases: empty, None, negative, boundary values
- Test error paths, not just happy paths
- Keep tests fast (mock external services)
- Use `pytest.raises` for exception testing

### DON'T:
- Test implementation details
- Use `time.sleep()` in tests
- Share state between tests
- Test private methods directly
- Write tests that depend on execution order
- Mock everything (some integration is good)

## References

- [Pytest Fixtures](./references/fixtures.md)
- [Async Testing](./references/async-testing.md)
- [Mocking Patterns](./references/mocking.md)
