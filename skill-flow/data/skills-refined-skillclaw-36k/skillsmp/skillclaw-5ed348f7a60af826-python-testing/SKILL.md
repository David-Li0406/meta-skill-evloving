---
name: python-testing
description: Use this skill when you want to implement best practices for testing Python applications using the pytest framework, including unit, integration, and async tests.
---

# Python Testing

Modern Python testing with the pytest ecosystem.

## Tooling

**ALWAYS use:**

- `pytest` — test runner
- `pytest-cov` — coverage reporting
- `pytest-asyncio` — async test support
- `pytest-mock` — mocking utilities
- `hypothesis` — property-based testing (when appropriate)
- `respx` / `pytest-httpx` — HTTP mocking for httpx
- `aioresponses` — HTTP mocking for aiohttp

**NEVER use:**

- `unittest` style (use pytest native)
- `nose` (deprecated)
- `mock` standalone (use pytest-mock)

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
    """Setup/teardown fixture for database."""
    database = Database()
    yield database
    database.close()
```