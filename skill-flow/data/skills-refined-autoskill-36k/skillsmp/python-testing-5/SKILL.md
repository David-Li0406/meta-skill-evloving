---
name: python-testing
description: |
  Use when writing pytest tests, creating fixtures, mocking dependencies, or testing async code - provides patterns that verify actual behavior with proper fixtures and parametrization; prevents testing mocks instead of code (plugin:dev-python@pproenca)
allowed-tools: Bash(pytest:*), Bash(uv:*), Read, Edit, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Python Testing Patterns

Robust testing with pytest.

## Before Writing Tests

1. Read `${CLAUDE_PLUGIN_ROOT}/references/pythonic-style.md` for naming and style conventions
2. **TDD workflow**: Write failing test first, then implement
3. Test behavior, not implementation details

## Reference Files

| Topic | When to Load | File |
|-------|--------------|------|
| Pythonic style | Before writing code | `${CLAUDE_PLUGIN_ROOT}/references/pythonic-style.md` |

## Basic Test Structure

```python
import pytest

def test_function_returns_expected_value():
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = process(input_data)

    # Assert
    assert result == expected_output
```

## Fixtures

### Basic Fixture

```python
@pytest.fixture
def sample_user():
    return User(name="Test", email="test@example.com")

def test_user_has_email(sample_user):
    assert sample_user.email == "test@example.com"
```

### Fixture with Cleanup

```python
@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    yield file_path
    # Cleanup happens automatically with tmp_path
```

### Fixture Scopes

```python
@pytest.fixture(scope="session")
def db_engine():
    """Shared across all tests in session."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")  # Default
def db_session(db_engine):
    """Fresh session per test."""
    with Session(db_engine) as session:
        yield session
        session.rollback()
```

### Parameterized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request):
    db_type = request.param
    return create_database(db_type)
```

## Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

# Multiple parameters
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(x, y, expected):
    assert add(x, y) == expected
```

## Mocking

### Basic Mock

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_service = Mock()
    mock_service.get_data.return_value = {"id": 1}

    result = process_data(mock_service)

    mock_service.get_data.assert_called_once()
    assert result["id"] == 1
```

### Patching

```python
@patch('mymodule.external_api')
def test_with_patch(mock_api):
    mock_api.fetch.return_value = {"status": "ok"}

    result = my_function()

    assert result == "ok"

# Context manager
def test_with_context_patch():
    with patch('mymodule.get_config') as mock_config:
        mock_config.return_value = {"debug": True}
        result = initialize()
        assert result.debug is True
```

### Mock Side Effects

```python
def test_mock_raises():
    mock = Mock()
    mock.method.side_effect = ValueError("error")

    with pytest.raises(ValueError):
        mock.method()

# Multiple calls
def test_mock_sequence():
    mock = Mock()
    mock.method.side_effect = [1, 2, 3]

    assert mock.method() == 1
    assert mock.method() == 2
    assert mock.method() == 3
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/api")
    assert response.status_code == 200
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_models.py
│   └── test_services.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    └── test_workflows.py
```

### conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    return create_app(testing=True)

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()
```

## Naming Conventions

```python
# File: test_<module>.py
# Function: test_<behavior>_<scenario>

def test_user_creation_with_valid_email():
    ...

def test_user_creation_raises_on_invalid_email():
    ...

def test_user_update_changes_name():
    ...
```

## Markers

```python
# Custom markers in pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]

# Usage
@pytest.mark.slow
def test_large_dataset():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

Run specific markers:
```bash
pytest -m "not slow"
pytest -m integration
```

## Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
asyncio_mode = "auto"
```

## TDD Workflow

1. **Write failing test first**
   ```python
   def test_calculate_discount():
       assert calculate_discount(100, 0.2) == 80
   ```

2. **Run test, see it fail**
   ```bash
   uv run pytest tests/test_pricing.py -v
   ```

3. **Write minimal code to pass**
   ```python
   def calculate_discount(price, rate):
       return price * (1 - rate)
   ```

4. **Run test, see it pass**

5. **Refactor if needed, tests still pass**

## Workflow Integration

If the `dev-workflow` plugin is installed, use these skills:

| Task | Skill |
|------|-------|
| Full TDD methodology | `dev-workflow:test-driven-development` |
| Debug test failures | `dev-workflow:systematic-debugging` |
| Before claiming done | `dev-workflow:verification-before-completion` |

## Best Practices

1. One assertion per test when possible
2. Descriptive names explaining behavior
3. Independent tests without shared mutable state
4. Fixtures for setup/teardown
5. Mock external dependencies appropriately
6. Parametrize to reduce duplication
7. Test edge cases and error conditions
8. Run tests in CI on every commit
9. Measure coverage focusing on quality
10. Write tests first (TDD) when possible
