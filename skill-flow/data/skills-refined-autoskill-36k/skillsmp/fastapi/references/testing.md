# Testing Patterns for FastAPI

Comprehensive guide for testing FastAPI applications with pytest.

## Table of Contents

1. [Setup](#setup)
2. [Test Client](#test-client)
3. [Testing Endpoints](#testing-endpoints)
4. [Testing with Database](#testing-with-database)
5. [Async Tests](#async-tests)
6. [Fixtures](#fixtures)
7. [Mocking](#mocking)
8. [Testing Authentication](#testing-authentication)
9. [Testing File Uploads](#testing-file-uploads)
10. [Coverage](#coverage)

---

## Setup

### Installation

```bash
pip install pytest pytest-asyncio httpx
```

### Project Structure

```
project/
├── app/
│   ├── main.py
│   └── api/
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Shared fixtures
│   ├── test_main.py        # Test main app
│   └── test_endpoints.py   # Test API endpoints
└── pytest.ini              # Pytest configuration
```

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = -v --tb=short
```

---

## Test Client

### Basic Test Client

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
```

### Using Test Client

```python
# tests/test_main.py
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

---

## Testing Endpoints

### GET Requests

```python
def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_list_items_with_pagination(client):
    response = client.get("/items?skip=0&limit=10")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) <= 10
```

### POST Requests

```python
def test_create_item(client):
    payload = {
        "name": "Test Item",
        "description": "A test item",
        "price": 29.99,
        "tax": 2.99
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data


def test_create_item_validation_error(client):
    payload = {
        "name": "",  # Invalid: empty name
        "price": -10  # Invalid: negative price
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 422  # Validation error
    errors = response.json()["detail"]
    assert any(err["loc"] == ["body", "name"] for err in errors)
    assert any(err["loc"] == ["body", "price"] for err in errors)
```

### PUT Requests

```python
def test_update_item(client):
    # First create an item
    create_response = client.post("/items/", json={
        "name": "Original",
        "price": 10.0
    })
    item_id = create_response.json()["id"]

    # Then update it
    update_response = client.put(f"/items/{item_id}", json={
        "name": "Updated",
        "price": 15.0
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated"
    assert data["price"] == 15.0
```

### DELETE Requests

```python
def test_delete_item(client):
    # Create item
    create_response = client.post("/items/", json={
        "name": "To Delete",
        "price": 10.0
    })
    item_id = create_response.json()["id"]

    # Delete item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
```

---

## Testing with Database

### Test Database Setup

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Create test database and tables."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create test client with test database."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

### Testing Database Operations

```python
# tests/test_database.py
from app.models.user import User


def test_create_user_in_db(db):
    user = User(email="test@example.com", hashed_password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"


def test_user_crud_through_api(client, db):
    # Create
    response = client.post("/users/", json={
        "email": "api@example.com",
        "password": "secret123"
    })
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Read
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "api@example.com"

    # Verify in database
    user = db.query(User).filter(User.id == user_id).first()
    assert user is not None
    assert user.email == "api@example.com"
```

---

## Async Tests

### Setup for Async Tests

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
```

### Async Test Examples

```python
# tests/test_async.py
import pytest


@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    response = await async_client.get("/items/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_create_item(async_client):
    response = await async_client.post(
        "/items/",
        json={"name": "Async Item", "price": 19.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Async Item"
```

### Async Database Tests

```python
@pytest_asyncio.fixture
async def async_db():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_async_database_operation(async_db):
    user = User(email="async@test.com", hashed_password="hashed")
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)

    assert user.id is not None
```

---

## Fixtures

### Reusable Test Data

```python
# tests/conftest.py
@pytest.fixture
def sample_item():
    return {
        "name": "Sample Item",
        "description": "A sample item for testing",
        "price": 99.99,
        "tax": 9.99
    }


@pytest.fixture
def sample_user():
    return {
        "email": "user@example.com",
        "password": "secret123"
    }


@pytest.fixture
def created_item(client, sample_item):
    """Fixture that creates an item and returns its data."""
    response = client.post("/items/", json=sample_item)
    return response.json()


@pytest.fixture
def multiple_items(client):
    """Fixture that creates multiple items."""
    items = []
    for i in range(5):
        response = client.post("/items/", json={
            "name": f"Item {i}",
            "price": 10.0 * (i + 1)
        })
        items.append(response.json())
    return items
```

### Using Fixtures

```python
def test_with_sample_data(client, sample_item):
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 201


def test_with_created_item(client, created_item):
    item_id = created_item["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200


def test_with_multiple_items(client, multiple_items):
    assert len(multiple_items) == 5
    response = client.get("/items/")
    assert len(response.json()) >= 5
```

---

## Mocking

### Mocking External Services

```python
from unittest.mock import patch, MagicMock


def test_with_mocked_external_api(client):
    with patch('app.services.external_api.fetch_data') as mock_fetch:
        # Configure mock
        mock_fetch.return_value = {"status": "success", "data": [1, 2, 3]}

        # Make request
        response = client.get("/external-data")

        # Assertions
        assert response.status_code == 200
        mock_fetch.assert_called_once()


@pytest.fixture
def mock_email_service():
    with patch('app.services.email.send_email') as mock:
        yield mock


def test_user_registration_sends_email(client, mock_email_service):
    response = client.post("/register", json={
        "email": "new@example.com",
        "password": "secret123"
    })
    assert response.status_code == 201
    mock_email_service.assert_called_once()
```

### Mocking Database

```python
def test_with_mocked_db_query(client):
    with patch('app.services.user_service.get_user') as mock_get_user:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "mock@example.com"
        mock_get_user.return_value = mock_user

        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["email"] == "mock@example.com"
```

---

## Testing Authentication

### JWT Token Tests

```python
# tests/conftest.py
@pytest.fixture
def auth_headers(client):
    """Returns authentication headers with valid token."""
    # Login to get token
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def authenticated_user(client, db):
    """Creates a user and returns auth headers."""
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("testpass")
    )
    db.add(user)
    db.commit()

    response = client.post("/token", data={
        "username": "testuser@example.com",
        "password": "testpass"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### Protected Endpoint Tests

```python
def test_protected_endpoint_without_auth(client):
    response = client.get("/protected")
    assert response.status_code == 401


def test_protected_endpoint_with_auth(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200


def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
```

---

## Testing File Uploads

```python
from io import BytesIO


def test_file_upload(client):
    file_content = b"Test file content"
    files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert "filename" in response.json()


def test_multiple_file_upload(client):
    files = [
        ("files", ("file1.txt", BytesIO(b"Content 1"), "text/plain")),
        ("files", ("file2.txt", BytesIO(b"Content 2"), "text/plain")),
    ]

    response = client.post("/upload-multiple", files=files)
    assert response.status_code == 200
    assert len(response.json()["files"]) == 2


def test_invalid_file_type(client):
    files = {"file": ("test.exe", BytesIO(b"exe content"), "application/x-msdownload")}

    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
```

---

## Coverage

### Running Tests with Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/

# View report
open htmlcov/index.html
```

### Coverage Configuration

```ini
# pytest.ini or .coveragerc
[coverage:run]
source = app
omit =
    */tests/*
    */venv/*
    */__init__.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## Best Practices

1. **Use fixtures** for reusable test data and setup
2. **Test one thing** per test function
3. **Use descriptive test names** (test_create_user_with_invalid_email)
4. **Test edge cases** and error conditions
5. **Mock external dependencies** (APIs, email services)
6. **Use test database** separate from development/production
7. **Clean up after tests** (fixtures should handle cleanup)
8. **Test authentication** separately from business logic
9. **Aim for high coverage** but focus on critical paths
10. **Run tests before commits** and in CI/CD pipeline
11. **Test async code** with pytest-asyncio
12. **Use parametrize** for testing multiple scenarios

### Parametrized Tests Example

```python
import pytest


@pytest.mark.parametrize("name,price,expected_status", [
    ("Valid Item", 10.0, 201),
    ("", 10.0, 422),  # Empty name
    ("Item", -5.0, 422),  # Negative price
    ("Item", 0, 422),  # Zero price
])
def test_create_item_validation(client, name, price, expected_status):
    response = client.post("/items/", json={"name": name, "price": price})
    assert response.status_code == expected_status
```
