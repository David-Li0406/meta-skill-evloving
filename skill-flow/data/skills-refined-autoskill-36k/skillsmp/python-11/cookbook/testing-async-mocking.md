# Testing Cookbook: Async and Mocking

Parameterized fixtures, async tests, and mocking patterns.

---
## Run Tests with Multiple Backend Implementations

**Problem**: Need to verify code works with different database backends or configurations.

**Solution**:
```python
@pytest.fixture(params=["postgres", "mysql", "sqlite"])
def database(request):
    """Run tests with multiple database backends."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.close()
```

**Tip**: Parameterized fixtures automatically run all tests using the fixture multiple times, once per parameter value.

---

## Create Factory Fixtures

**Problem**: Need to create multiple instances of an object with different attributes in a single test.

**Solution**:
```python
@pytest.fixture
def make_user():
    """Factory fixture for creating users with custom attributes."""
    def _make_user(name: str = "Test", age: int = 25):
        return User(name=name, age=age)
    return _make_user

def test_multiple_users(make_user):
    alice = make_user(name="Alice", age=30)
    bob = make_user(name="Bob", age=25)
    assert alice.name != bob.name
```

**Tip**: Factory fixtures return a callable function, allowing flexible object creation with custom parameters in each test.

---

## Test with Multiple Input Values

**Problem**: Need to test the same function with many different input/output combinations.

**Solution**:
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double(input, expected):
    assert double(input) == expected
```

**Tip**: Parametrize creates a separate test for each tuple, making it easy to spot which specific inputs fail.

---

## Test All Combinations of Parameters

**Problem**: Need to test a function with every combination of two or more parameter sets.

**Solution**:
```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    # Runs 6 times: (1,10), (1,20), (2,10), (2,20), (3,10), (3,20)
    assert multiply(x, y) == x * y
```

**Tip**: Stacking multiple `@pytest.mark.parametrize` decorators creates the cartesian product of all parameters.

---

## Add Descriptive Test IDs

**Problem**: Parametrized test names like `test_age[0]` don't clearly indicate what's being tested.

**Solution**:
```python
@pytest.mark.parametrize("age,valid", [
    pytest.param(18, True, id="adult"),
    pytest.param(17, False, id="minor"),
    pytest.param(65, True, id="senior"),
    pytest.param(-1, False, id="negative"),
])
def test_age_validation(age, valid):
    if valid:
        user = User(name="Test", age=age)
        assert user.age == age
    else:
        with pytest.raises(ValueError):
            User(name="Test", age=age)
```

**Tip**: Custom IDs make test output readable: `test_age_validation[adult]` instead of `test_age_validation[18-True]`.

---

## Test Async Functions

**Problem**: Need to test asynchronous functions and coroutines.

**Solution**:
```python
# tests/test_async.py
import pytest
from my_project.services import AsyncUserService

@pytest.mark.asyncio
async def test_fetch_user():
    service = AsyncUserService()
    user = await service.get_user(1)
    assert user.name == "Alice"

@pytest.mark.asyncio
async def test_fetch_multiple_users():
    service = AsyncUserService()
    users = await service.get_users([1, 2, 3])
    assert len(users) == 3
```

**Tip**: With `asyncio_mode = "auto"` in config, you can omit the `@pytest.mark.asyncio` decorator.

---

## Create Async Fixtures

**Problem**: Tests need async setup like HTTP clients or database connections.

**Solution**:
```python
@pytest.fixture
async def async_client():
    import httpx
    async with httpx.AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_api_call(async_client):
    response = await async_client.get("https://api.example.com/users")
    assert response.status_code == 200
```

**Tip**: Async fixtures automatically handle async context managers and cleanup with async generators.

---

## Mock External Dependencies

**Problem**: Tests shouldn't call real databases or external APIs.

**Solution**:
```python
from unittest.mock import Mock, patch, AsyncMock

def test_with_mock():
    mock_db = Mock()
    mock_db.query.return_value = [{"id": 1, "name": "Alice"}]

    service = UserService(db=mock_db)
    result = service.get_users()

    assert len(result) == 1
    mock_db.query.assert_called_once()
```

**Tip**: Use `return_value` to set what the mock returns, and `assert_called_once()` to verify it was used correctly.

---

## Patch Module-Level Functions

**Problem**: Need to mock imported functions like `requests.get` without modifying the code under test.

**Solution**:
```python
@patch("my_project.services.requests.get")
def test_external_api(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}

    result = call_external_api()

    assert result["status"] == "ok"
    mock_get.assert_called_once()

def test_with_context_manager():
    with patch("my_project.services.database") as mock_db:
        mock_db.query.return_value = []
        result = get_users()
        assert result == []
```

**Tip**: Use the full import path where the function is used, not where it's defined: `my_project.services.requests`, not `requests`.

---

## Mock Async Functions

**Problem**: Need to mock async functions and verify they were awaited.

**Solution**:
```python
@pytest.fixture
async def mock_api():
    api = AsyncMock()
    api.fetch.return_value = {"status": "ok"}
    return api

@pytest.mark.asyncio
async def test_async_service(mock_api):
    service = AsyncService(api=mock_api)
    result = await service.process()

    assert result["status"] == "ok"
    mock_api.fetch.assert_awaited_once()
```

**Tip**: Use `AsyncMock` instead of `Mock` for async functions, and `assert_awaited_once()` instead of `assert_called_once()`.

---

## Mock Context Managers

**Problem**: Need to mock objects that use `__enter__` and `__exit__` like file handles.

**Solution**:
```python
from unittest.mock import MagicMock

def test_context_manager():
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = "content"

    with mock_file as f:
        assert f.read() == "content"
```

**Tip**: `MagicMock` automatically implements magic methods like `__enter__`, `__exit__`, `__len__`, and `__iter__`.

---

## Spy on Real Objects

**Problem**: Want to verify a method was called while still executing the real implementation.

**Solution**:
```python
from unittest.mock import patch

def test_spy_on_method():
    user = User(name="Alice")

    with patch.object(user, "validate", wraps=user.validate) as spy:
        user.save()
        spy.assert_called_once()
```

**Tip**: The `wraps` parameter creates a spy that tracks calls but still executes the original method.

---
