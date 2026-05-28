# Testing Cookbook: Basics

Core pytest setup, unit tests, exceptions, floats, and fixtures.

---
## Setup pytest with Coverage

**Problem**: Need to configure pytest with coverage reporting and best practices for a Python project.

**Solution**:
```bash
uv add --dev pytest pytest-cov pytest-asyncio
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = """
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
    -v
    --strict-markers
"""
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
asyncio_mode = "auto"
```

**Tip**: Use `asyncio_mode = "auto"` to avoid decorating every async test with `@pytest.mark.asyncio`.

---

## Write Basic Unit Tests

**Problem**: Need to test class methods, validation, and equality in a structured way.

**Solution**:
```python
# tests/test_entities.py
import pytest
from my_project.entities import User

class TestUser:
    def test_user_creation(self):
        user = User(name="Alice", email="alice@example.com")
        assert user.name == "Alice"
        assert user.email == "alice@example.com"

    def test_user_validation_raises(self):
        with pytest.raises(ValueError) as exc_info:
            User(name="", email="invalid")
        assert "name cannot be empty" in str(exc_info.value)

    def test_user_equality(self):
        user1 = User(name="Alice", email="a@b.com")
        user2 = User(name="Alice", email="a@b.com")
        assert user1 == user2
```

**Tip**: Group related tests in classes with the `Test` prefix for better organization and shared setup.

---

## Test Exceptions

**Problem**: Need to verify that code raises the correct exceptions with specific messages.

**Solution**:
```python
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_value_error_message():
    with pytest.raises(ValueError, match=r"must be positive"):
        create_user(age=-1)
```

**Tip**: Use the `match` parameter with a regex pattern to verify exception messages contain expected text.

---

## Compare Floating Point Numbers

**Problem**: Floating point arithmetic can produce slightly different results that fail equality checks.

**Solution**:
```python
def test_float_comparison():
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)

def test_with_tolerance():
    assert 2.0 == pytest.approx(2.1, abs=0.2)
    assert 2.0 == pytest.approx(2.02, rel=0.02)
```

**Tip**: Use `abs` for absolute tolerance (fixed margin) or `rel` for relative tolerance (percentage-based).

---

## Create Reusable Test Fixtures

**Problem**: Tests need shared setup objects like users or database connections with proper cleanup.

**Solution**:
```python
# tests/conftest.py
import pytest
from my_project.entities import User
from my_project.database import Database

@pytest.fixture
def user():
    """Create test user."""
    return User(name="Alice", email="alice@example.com")

@pytest.fixture
def database():
    """Create and cleanup test database."""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

# tests/test_services.py
def test_save_user(database, user):
    database.save(user)
    assert database.get_user(user.id) == user
```

**Tip**: Use `yield` in fixtures to run cleanup code after the test completes, ensuring resources are properly released.

---

## Control Fixture Scope

**Problem**: Some fixtures are expensive to create and should be shared across multiple tests.

**Solution**:
```python
@pytest.fixture(scope="session")
def app():
    """Shared across all tests in session."""
    return create_app()

@pytest.fixture(scope="module")
def client(app):
    """Shared within a test module."""
    return app.test_client()

@pytest.fixture(scope="class")
def users():
    """Shared within a test class."""
    return [User(name=f"User{i}") for i in range(10)]

@pytest.fixture  # scope="function" is default
def temp_file():
    """Created fresh for each test."""
    with tempfile.NamedTemporaryFile() as f:
        yield f
```

**Tip**: Use `scope="session"` for expensive one-time setup like database connections, and `scope="function"` (default) for test isolation.

---
