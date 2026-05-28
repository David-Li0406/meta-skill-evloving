---
name: testing-fastapi
description: Use this skill for implementing Test-Driven Development (TDD) patterns in FastAPI projects using pytest.
---

# Testing FastAPI with pytest

This skill provides patterns for writing tests BEFORE implementation in FastAPI projects using pytest, along with comprehensive testing strategies.

## The TDD Cycle

```
┌─────────────────────────────────────────────────────────┐
│  1. RED: Write a failing test                           │
│     - Test must fail initially (proves it tests something)│
│     - Test should be minimal, focused on one behavior   │
│                                                         │
│  2. GREEN: Write minimal code to pass                   │
│     - Only enough code to make the test pass            │
│     - Don't optimize yet                                │
│                                                         │
│  3. REFACTOR: Improve the code                          │
│     - Clean up while keeping tests green                │
│     - DRY, readability, performance                     │
└─────────────────────────────────────────────────────────┘
```

## Overview of pytest for FastAPI

pytest is the industry-standard testing framework for Python, providing powerful features like fixtures, parametrization, and plugins. It integrates seamlessly with FastAPI for testing endpoints, including async support.

### Key Features
- Fixture system for dependency injection
- Parametrization for data-driven tests
- Rich assertion introspection
- Plugin ecosystem (pytest-cov, pytest-asyncio)
- Async/await support for testing asynchronous code

## Basic Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock MongoDB collection."""
    mock = AsyncMock()
    return mock
```

## Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_todo_async():
    """Test async endpoint with httpx AsyncClient."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/todos/",
            json={"title": "Test Todo", "description": "Test"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"
```

## Mocking Database Operations

```python
from unittest.mock import patch, AsyncMock, MagicMock
from bson import ObjectId


@patch("app.routers.todo.request.app.todo")
def test_get_todos(mock_collection, client):
    """Mock MongoDB find() with cursor."""
    # Create mock cursor that behaves like MongoDB cursor
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=[
        {"_id": ObjectId(), "title": "Todo 1", "user_id": "test_user"},
        {"_id": ObjectId(), "title": "Todo 2", "user_id": "test_user"},
    ])
    mock_collection.find.return_value = mock_cursor

    response = client.get("/todos/")

    assert response.status_code == 200
    assert len(response.json()) == 2
```

## Testing Authentication

```python
import pytest
from app.routers.auth import create_access_token, verify_password


class TestAuthentication:
    """TDD tests for authentication flow."""

    def test_password_verification_correct(self):
        """GREEN: Correct password should verify."""
        hashed = "$argon2id$..."  # Pre-computed hash
        assert verify_password("correct_password", hashed) is True

    def test_password_verification_incorrect(self):
        """RED first: Wrong password should fail."""
        hashed = "$argon2id$..."
        assert verify_password("wrong_password", hashed) is False

    def test_access_token_contains_user_id(self):
        """Token should contain user_id in payload."""
        token = create_access_token(user_id="user123", username="testuser")
        # Decode and verify payload
        # Note: decode_token would be a project utility you implement
        payload = decode_token(token)
        assert payload["user_id"] == "user123"
```

## Testing Error Cases

```python
def test_todo_not_found_returns_404(client, mock_db):
    """Specific error case for non-existent todo."""
    mock_db.find_one.return_value = None

    response = client.get("/todos/nonexistent_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_unauthorized_returns_401(client):
    """Missing token should return 401."""
    response = client.get("/todos/")  # No Authorization header

    assert response.status_code == 401
```

## Testing with Fixtures (conftest.py patterns)

```python
# conftest.py
import pytest
from unittest.mock import patch, AsyncMock


@pytest.fixture
def authenticated_client(client):
    """Client with valid auth token."""
    with patch("app.main.decode_token") as mock_decode:
        mock_decode.return_value = {
            "user_id": "test_user_id",
            "username": "testuser"
        }
        yield client


@pytest.fixture
def mock_user_collection():
    """Pre-configured user collection mock."""
    mock = AsyncMock()
    mock.find_one.return_value = {
        "_id": ObjectId(),
        "username": "testuser",
        "email": "test@example.com"
    }
    return mock
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Test passes without implementation | Make test more specific, check exact values |
| Mock not applied correctly | Use full import path in `@patch()` |
| Async tests not running | Add `@pytest.mark.asyncio` decorator |
| ObjectId comparison fails | Compare string representations |
| Test depends on execution order | Use fixtures for isolation |

## Best Practices

### 1. Test Organization
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── services.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_models.py       # Model tests
│   ├── test_services.py     # Service tests
│   ├── test_api.py          # API tests
│   └── integration/
│       ├── __init__.py
│       └── test_workflows.py
└── pytest.ini
```

### 2. Naming Conventions
```python
# ✅ GOOD: Clear test names
def test_user_creation_with_valid_email():
    pass

def test_user_creation_raises_error_for_duplicate_email():
    pass

# ❌ BAD: Vague names
def test_user1():
    pass

def test_case2():
    pass
```

### 3. Arrange-Act-Assert Pattern
```python
def test_user_service_creates_user():
    # Arrange: Setup test data and dependencies
    service = UserService(database=mock_db)
    user_data = {"email": "test@example.com", "name": "Test"}

    # Act: Perform the action being tested
    result = service.create_user(user_data)

    # Assert: Verify the outcome
    assert result.email == "test@example.com"
    assert result.id is not None
```

### 4. Use Fixtures for Common Setup
```python
# ❌ BAD: Repeated setup
def test_user_creation():
    db = setup_database()
    user = create_user(db)
    assert user.id is not None
    db.close()

def test_user_deletion():
    db = setup_database()
    user = create_user(db)
    delete_user(db, user.id)
    db.close()

# ✅ GOOD: Fixture-based setup
@pytest.fixture
def db():
    database = setup_database()
    yield database
    database.close()

@pytest.fixture
def user(db):
    return create_user(db)

def test_user_creation(user):
    assert user.id is not None

def test_user_deletion(db, user):
    delete_user(db, user.id)
    assert not user_exists(db, user.id)
```

### 5. Parametrize Similar Tests
```python
# ❌ BAD: Duplicate test code
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(0, 0) == 0

# ✅ GOOD: Parametrized tests
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-2, -3, -5),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 6. Test One Thing Per Test
```python
# ❌ BAD: Testing multiple things
def test_user_workflow():
    user = create_user()
    assert user.id is not None

    updated = update_user(user.id, name="New Name")
    assert updated.name == "New Name"

    deleted = delete_user(user.id)
    assert deleted is True

# ✅ GOOD: Separate tests
def test_user_creation():
    user = create_user()
    assert user.id is not None

def test_user_update():
    user = create_user()
    updated = update_user(user.id, name="New Name")
    assert updated.name == "New Name"

def test_user_deletion():
    user = create_user()
    result = delete_user(user.id)
    assert result is True
```

### 7. Use Markers for Test Organization
```python
@pytest.mark.unit
def test_pure_function():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_database_integration():
    pass

@pytest.mark.smoke
def test_critical_path():
    pass
```

### 8. Mock External Dependencies
```python
# ✅ GOOD: Mock external API
def test_fetch_user_data(mocker):
    mocker.patch("requests.get", return_value=mock_response)
    result = fetch_user_data(user_id=1)
    assert result["name"] == "Alice"

# ❌ BAD: Real API call in test
def test_fetch_user_data():
    result = fetch_user_data(user_id=1)  # Real HTTP request!
    assert result["name"] == "Alice"
```

## Quick Reference

### Common Commands
```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Show print statements
pytest -s

# Run specific file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_create_user

# Run by marker
pytest -m unit
pytest -m "not slow"

# Run with coverage
pytest --cov=app --cov-report=html

# Parallel execution
pytest -n auto  # Requires pytest-xdist

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run failed tests first
pytest --ff
```

### pytest.ini Template
```ini
[pytest]
# Minimum pytest version
minversion = 7.0

# Test discovery patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Test paths
testpaths = tests

# Command line options
addopts =
    -v
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    smoke: Smoke tests for critical paths

# Django settings (if using Django)
DJANGO_SETTINGS_MODULE = myproject.settings

# Asyncio mode
asyncio_mode = auto
```

### conftest.py Template
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

# FastAPI client fixture
@pytest.fixture
def client():
    return TestClient(app)

# Database fixture
@pytest.fixture
def db():
    database = setup_test_database()
    yield database
    database.close()

# Mock user fixture
@pytest.fixture
def mock_user():
    return {"id": 1, "email": "test@example.com", "name": "Test User"}

# Custom pytest configuration
def pytest_configure(config):
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "db: Database tests")
```

## Resources
- **Official Documentation**: https://docs.pytest.org/
- **pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **pytest-cov**: https://pytest-cov.readthedocs.io/
- **pytest-mock**: https://pytest-mock.readthedocs.io/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

## Related Skills
When using pytest with FastAPI, consider these complementary skills:
- **fastapi-local-dev**: FastAPI development server patterns and test fixtures
- **systematic-debugging**: Root cause investigation for failing tests

### Quick TDD Workflow Reference (Inlined for Standalone Use)
**RED → GREEN → REFACTOR Cycle:**
1. **RED Phase: Write Failing Test**
   ```python
   def test_should_authenticate_user_when_credentials_valid():
       # Test that describes desired behavior
       user = User(username='alice', password='secret123')
       result = authenticate(user)
       assert result.is_authenticated is True
       # This test will fail because authenticate() doesn't exist yet
   ```

2. **GREEN Phase: Make It Pass**
   ```python
   def authenticate(user):
       # Minimum code to pass the test
       if user.username == 'alice' and user.password == 'secret123':
           return AuthResult(is_authenticated=True)
       return AuthResult(is_authenticated=False)
   ```

3. **REFACTOR Phase: Improve Code**
   ```python
   def authenticate(user):
       # Clean up while keeping tests green
       hashed_password = hash_password(user.password)
       stored_user = database.get_user(user.username)
       return AuthResult(
           is_authenticated=(stored_user.password_hash == hashed_password)
       )
   ```

**Test Structure: Arrange-Act-Assert (AAA)**
```python
def test_user_creation():
    # Arrange: Set up test data
    user_data = {'username': 'alice', 'email': 'alice@example.com'}

    # Act: Perform the action
    user = create_user(user_data)

    # Assert: Verify outcome
    assert user.username == 'alice'
    assert user.email == 'alice@example.com'
```

### Quick Debugging Reference (Inlined for Standalone Use)
**Phase 1: Root Cause Investigation**
- Read error messages completely (stack traces, line numbers)
- Reproduce consistently (document exact steps)
- Check recent changes (git log, git diff)
- Understand what changed and why it might cause failure

**Phase 2: Isolate the Problem**
```python
# Use pytest's built-in debugging
pytest tests/test_auth.py -vv --pdb  # Drop into debugger on failure
pytest tests/test_auth.py -x         # Stop on first failure
pytest tests/test_auth.py -k "auth"  # Run only auth-related tests

# Add strategic print/logging
def test_complex_workflow():
    user = create_user({'username': 'test'})
    print(f"DEBUG: Created user {user.id}")  # Visible with pytest -s
    result = process_user(user)
    print(f"DEBUG: Result status {result.status}")
    assert result.success
```

**Phase 3: Fix Root Cause**
- Fix the underlying problem, not symptoms
- Add regression test to prevent recurrence
- Verify fix doesn't break other tests

**Phase 4: Verify Solution**
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Verify specific test patterns
pytest -k "auth