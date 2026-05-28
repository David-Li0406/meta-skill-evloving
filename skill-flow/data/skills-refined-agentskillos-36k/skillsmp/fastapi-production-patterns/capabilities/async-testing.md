# Async Testing

## Overview
Testing FastAPI async endpoints properly using `httpx.AsyncClient` and async fixtures to avoid hangs, test bleeding, and false positives.

## Problem Statement
**Testing async endpoints wrong causes:**
- Tests hang indefinitely
- Tests pass in isolation but fail together (database bleeding)
- Sync `TestClient` doesn't work with async
- Fixtures don't properly cleanup

## Pattern: Production Async Testing

### ❌ Broken (Sync TestClient)
```python
from fastapi.testclient import TestClient  # ❌ Wrong for async

def test_get_users():  # ❌ Not async
    client = TestClient(app)
    response = client.get("/users")  # May hang!
    assert response.status_code == 200
```

### ✅ Production Pattern
```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()  # Clean up after test

@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    response = await async_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Key Components

### 1. Async Client Fixture
```python
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

### 2. Database Isolation
```python
@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

    await engine.dispose()
```

### 3. Dependency Overrides
```python
@pytest.fixture
async def async_client_with_db(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

## Test Scenarios

### CRUD Testing
```python
@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient):
    # First create
    create_response = await async_client.post("/users", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    user_id = create_response.json()["id"]

    # Then get
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"

@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient):
    # Create then update
    create_response = await async_client.post("/users", json={
        "name": "Charlie",
        "email": "charlie@example.com"
    })
    user_id = create_response.json()["id"]

    response = await async_client.patch(f"/users/{user_id}", json={
        "name": "Charlie Updated"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie Updated"

@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient):
    create_response = await async_client.post("/users", json={
        "name": "Dave",
        "email": "dave@example.com"
    })
    user_id = create_response.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
```

### Parallel Request Testing
```python
@pytest.mark.asyncio
async def test_concurrent_requests(async_client: AsyncClient):
    # Test that handles concurrent requests correctly
    tasks = [
        async_client.get("/users/1")
        for _ in range(10)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in responses)
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Using `TestClient` (sync) | Tests hang | Use `AsyncClient` |
| Missing `@pytest.mark.asyncio` | Tests don't run | Add decorator |
| No database rollback | Tests affect each other | Rollback in fixture cleanup |
| Forgetting to clear overrides | Overrides leak | Always clear in `finally` |
| Not `await`-ing async calls | Coroutine never executes | `await` all async calls |

## Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
```

## Running Tests

```bash
# Run all async tests
pytest

# Run with output
pytest -v

# Run specific test
pytest tests/test_users.py::test_get_user

# Run with coverage
pytest --cov=app tests/
```

## Performance Tips

1. **Use pytest-xdist for parallel tests:**
   ```bash
   pytest -n auto  # Run tests in parallel
   ```

2. **Database connection pooling in tests:**
   ```python
   @pytest.fixture(scope="session")
   async def test_engine():
       return create_async_engine(TEST_DATABASE_URL, pool_size=5)
   ```

3. **Mock external APIs:**
   ```python
   @pytest.fixture
   async def mock_external_api(mocker):
       async def mock_get(url):
           return MockResponse({"data": "mocked"})
       mocker.patch("httpx.AsyncClient.get", mock_get)
   ```

## See Also
- [Database Lifecycle Management](database-lifecycle-management.md)
- [Dependency Injection](dependency-injection.md)
