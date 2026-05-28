---
name: python-testing
description: Use this skill when writing, evaluating, or debugging Python tests with pytest, including fixtures, parameterization, mocking, and coverage.
---

# Python Testing with Pytest

## When to Activate

Activate this skill when:
- Writing Python unit tests
- Creating test files or test directories
- Setting up pytest configuration
- Working with test fixtures or mocking
- Running tests or checking coverage
- Reviewing test code or debugging test failures
- Improving test coverage

## Quick Commands

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run verbose with output
pytest -v -s

# Run tests matching pattern
pytest -k "test_user"

# Run last failed
pytest --lf
```

## Test Structure: AAA Pattern

Follow **Arrange-Act-Assert** for clear, maintainable tests:

```python
def test_user_registration():
    # Arrange
    email = "test@example.com"
    password = "secure_pass123"
    user_service = UserService()

    # Act
    result = user_service.register(email, password)

    # Assert
    assert result.success is True
    assert result.user.email == email
```

## Core Principles

- Each test should be **atomic**, **self-contained**, and test **single functionality**.
- Use descriptive names that explain the scenario.

## Fixtures

### Basic Fixture

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_example(sample_data):
    assert sample_data["key"] == "value"
```

### Function-Scoped Fixture

```python
@pytest.fixture
def client():
    return Client()

def test_with_client(client):
    result = client.ping()
    assert result is not None
```

### Parametrized Fixture

```python
@pytest.fixture(params=["mysql", "postgres", "sqlite"])
def database(request):
    return create_db(request.param)
```

## Parametrization

Run tests with multiple inputs.

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

## Mocking

### Mocking Functions

```python
from unittest.mock import patch

def test_api_call(monkeypatch):
    def mock_get(*args, **kwargs):
        return {"status": "ok"}

    monkeypatch.setattr("mymodule.api.get", mock_get)
    result = mymodule.fetch_data()
    assert result["status"] == "ok"
```

### Mocking with Async

```python
from unittest.mock import AsyncMock, patch

async def test_external_api_call():
    with patch("mymodule.external_client.fetch", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "test"}
        result = await my_function()
        assert result == {"data": "test"}
```

## Running Tests

```bash
pytest -n auto              # Run all tests in parallel
pytest -n auto -x           # Stop on first failure
pytest -m "not integration" # Exclude integration tests
```

## Best Practices

1. **One assertion focus per test** - Test one behavior per function.
2. **Descriptive names** - Use names that clearly indicate what is being tested.
3. **Use fixtures** - Avoid setup duplication.
4. **Isolate tests** - No shared state between tests.
5. **Fast unit tests** - Mark slow tests with `@pytest.mark.slow`.
6. **Parametrize** - Use parametrize over copy-paste tests.
7. **Test edge cases** - Include tests for empty inputs, boundaries, and errors.

## Project Structure

Recommended layout:

```
project/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── tests/
    ├── conftest.py      # Shared fixtures
    ├── test_module.py
    └── unit/
        └── test_specific.py
```

## Configuration

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]
```

## References

- [Fixtures Guide](references/fixtures.md) - Advanced fixture patterns
- [Patterns Guide](references/patterns.md) - Common testing patterns