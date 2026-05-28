# Testing in Python

Comprehensive guide to testing with pytest.

## pytest Basics

```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

Run: `pytest` or `pytest test_example.py`

## Fixtures

```python
import pytest

@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

## Parametrize

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

```python
from unittest.mock import Mock, patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    response = fetch_data()
    assert response["status"] == "ok"
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch()
    assert result == expected
```

## FastAPI Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
```

## Coverage

```bash
pytest --cov=myapp --cov-report=html
```

## Best Practices

1. One assert per test when possible
2. Use fixtures for setup/teardown
3. Name tests descriptively: `test_user_creation_with_invalid_email`
4. Use parametrize for multiple test cases
5. Mock external dependencies
6. Aim for 80%+ coverage on critical code
7. Test edge cases and error conditions
