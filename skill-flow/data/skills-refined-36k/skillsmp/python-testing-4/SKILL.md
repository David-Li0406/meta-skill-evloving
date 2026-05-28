---
name: python-testing
description: Testing strategies, pytest patterns, fixtures, mocking, coverage
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: testing
---

## What I do

I provide guidance on testing Python applications, including:

- pytest fixtures and parametrization
- Test organization and structure
- Mocking and patching strategies
- Coverage tools and thresholds
- Property-based testing with hypothesis
- Async testing (pytest-asyncio)
- Integration vs unit testing
- Test doubles and factories
- Test databases and external dependencies

## When to use me

Use me when:
- Writing tests for Python code
- Designing test fixtures and test data
- Mocking external dependencies
- Setting up test coverage
- Testing async code
- Writing property-based tests
- Organizing test suites
- Testing database interactions

## Best Practices

### ✅ Use Fixtures for Reusable Test Components

```python
import pytest
from typing import Generator
from myapp import create_app, db
from myapp.models import User

@pytest.fixture
def app() -> Generator:
    """Create and configure a test app."""
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def sample_user(app) -> User:
    """Create a test user."""
    user = User(name="Alice", email="alice@example.com")
    db.session.add(user)
    db.session.commit()
    return user
```

### ✅ Parametrize Tests for Multiple Cases

```python
import pytest
from myapp.validators import validate_email

@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("user.name@example.co.uk", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
])
def test_validate_email(email: str, expected: bool) -> None:
    """Test email validation with multiple inputs."""
    assert validate_email(email) == expected
```

### ✅ Use Test Factories for Complex Data

```python
from dataclasses import dataclass
from typing import Optional
import random
import string

@dataclass
class UserFactory:
    """Factory for creating test users."""

    name: str = "Test User"
    email: Optional[str] = None

    def build(self) -> dict[str, str]:
        """Build a user dict."""
        if self.email is None:
            suffix = "".join(random.choices(string.ascii_lowercase, k=5))
            self.email = f"test{suffix}@example.com"

        return {
            "name": self.name,
            "email": self.email,
        }

    def create(self) -> User:
        """Create and save a user."""
        user_dict = self.build()
        return User(**user_dict)

# Usage in tests
def test_with_factory(user_factory: UserFactory) -> None:
    user = user_factory.create()
    assert user.email is not None
```

### ✅ Mock External Dependencies

```python
from unittest.mock import Mock, patch
import requests

def test_fetch_data() -> None:
    """Test data fetching with mocked HTTP."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}

    with patch("requests.get", return_value=mock_response):
        result = fetch_data("https://api.example.com")

    assert result == {"data": "test"}
```

### ✅ Test Async Code

```python
import pytest
from httpx import AsyncClient
from myapp.main import app

@pytest.mark.asyncio
async def test_async_endpoint() -> None:
    """Test async endpoint with pytest-asyncio."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### ✅ Use Context Managers for Test Setup

```python
from contextlib import contextmanager
import tempfile
from pathlib import Path

@contextmanager
def temp_database(db_name: str):
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / db_name
        # Setup database
        yield db_path
        # Cleanup happens automatically

def test_with_temp_db() -> None:
    """Test using temporary database."""
    with temp_database("test.db") as db_path:
        # Run tests with temporary database
        results = run_queries(db_path)
        assert results is not None
```

### ✅ Property-Based Testing

```python
from hypothesis import given, strategies as st
from myapp.utils import calculate_total

@given(
    items=st.lists(
        st.fixed_dictionaries({
            "price": st.floats(min_value=0, allow_nan=False),
            "quantity": st.integers(min_value=0, max_value=1000),
        }),
        min_size=1,
        max_size=10
    )
)
def test_calculate_total(items: list[dict]) -> None:
    """Test total calculation with random inputs."""
    total = calculate_total(items)
    expected = sum(item["price"] * item["quantity"] for item in items)
    assert total == expected
```

### ✅ Test Database Interactions

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from myapp.models import Base, User

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

def test_create_user(db_session: Session) -> None:
    """Test creating a user in the database."""
    user = User(name="Bob", email="bob@example.com")
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).filter_by(name="Bob").first()
    assert retrieved is not None
    assert retrieved.email == "bob@example.com"
```

## Test Organization

### ✅ Structure Your Tests

```
tests/
├── unit/
│   ├── test_utils.py
│   ├── test_models.py
│   └── test_validators.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_endpoints.py
├── conftest.py          # Shared fixtures
└── __init__.py
```

### ✅ Use conftest.py for Shared Fixtures

```python
# tests/conftest.py
import pytest
from myapp import create_app

@pytest.fixture(scope="session")
def app():
    """Shared app for all tests."""
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture(scope="session")
def client(app):
    """Shared test client."""
    return app.test_client()
```

## Coverage

### ✅ Configure Coverage

```ini
# .coveragerc
[run]
source = myapp
omit =
    */tests/*
    */venv/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### ✅ Run Coverage

```bash
# Run coverage with pytest
pytest --cov=myapp --cov-report=html --cov-report=term

# Generate coverage report
coverage report -m

# HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Testing Patterns

### ✅ AAA Pattern (Arrange, Act, Assert)

```python
def test_user_creation() -> None:
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # Act
    user = User(**user_data)

    # Assert
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

### ✅ Test Exception Handling

```python
import pytest
from myapp.exceptions import ValidationError

def test_invalid_data_raises_error() -> None:
    """Test that invalid data raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_email("invalid")

    assert "Invalid email format" in str(exc_info.value)
```

### ✅ Test Time-Dependent Code

```python
from unittest.mock import patch
from datetime import datetime, timezone

def test_timestamp() -> None:
    """Test timestamp generation with frozen time."""
    test_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with patch("myapp.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = test_time
        timestamp = get_timestamp()

    assert timestamp == test_time
```

## Common Pitfalls

### ❌ Don't Test Implementation Details

```python
# BAD: Tests implementation
def test_sorting() -> None:
    data.sort()  # Tests specific algorithm
    assert data[0] == "a"

# GOOD: Tests behavior
def test_sorted_order() -> None:
    sorted_data = sort_data(data)
    assert sorted_data[0] == "a"
```

### ❌ Don't Use Shared State Between Tests

```python
# BAD: Shared state causes flaky tests
global_var = None

def test_one():
    global global_var
    global_var = "value"

def test_two():
    assert global_var == "value"  # Depends on test_one

# GOOD: Each test is independent
def test_one():
    local_var = "value"
    assert local_var == "value"
```

### ❌ Don't Ignore Coverage

```python
# BAD: Low coverage leaves bugs hidden
def complex_function(x):
    if x > 10:  # Never tested
        return x * 2
    return x

# GOOD: Write tests for all branches
def test_complex_function():
    assert complex_function(5) == 5
    assert complex_function(20) == 40
```

## Testing Best Practices

1. **Test one thing per test function**
2. **Use descriptive test names** (`test_user_can_login_with_valid_credentials`)
3. **Keep tests fast and isolated**
4. **Use fixtures for setup and teardown**
5. **Mock external dependencies** (APIs, databases, file system)
6. **Aim for >80% coverage** on critical code
7. **Run tests in CI/CD**
8. **Use property-based testing** for edge cases
9. **Test async code properly** with pytest-asyncio
10. **Document complex test scenarios**

## References

- pytest documentation: https://docs.pytest.org/
- pytest-asyncio documentation: https://pytest-asyncio.readthedocs.io/
- hypothesis documentation: https://hypothesis.readthedocs.io/
- Real Python pytest guide: https://realpython.com/pytest-python-testing/
- pytest fixtures guide: https://docs.pytest.org/en/stable/fixture.html
