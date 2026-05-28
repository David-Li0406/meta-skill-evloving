# Testing Patterns

Comprehensive testing strategies for enterprise Python applications.

## Table of Contents
- [Test Organization](#test-organization)
- [Pytest Fixtures](#pytest-fixtures)
- [Mocking Patterns](#mocking-patterns)
- [Async Testing](#async-testing)
- [Property-Based Testing](#property-based-testing)
- [Integration Testing](#integration-testing)

## Test Organization

### Directory Structure
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── conftest.py       # Unit-specific fixtures
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── conftest.py       # Integration fixtures
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    └── test_workflows.py
```

### Test Naming
```python
# Function-based: test_<what>_<condition>_<expected>
def test_create_user_with_valid_email_returns_user() -> None:
    ...

def test_create_user_with_invalid_email_raises_validation_error() -> None:
    ...

# Class-based: group related tests
class TestUserService:
    def test_create_user_success(self) -> None:
        ...
    
    def test_create_user_duplicate_email_raises(self) -> None:
        ...
```

## Pytest Fixtures

### Basic Fixtures
```python
# conftest.py
import pytest
from typing import Generator

@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(id="123", email="test@example.com", name="Test User")

@pytest.fixture
def user_service(mock_repo: MockUserRepository) -> UserService:
    """Create UserService with mocked dependencies."""
    return UserService(repo=mock_repo)

@pytest.fixture(scope="session")
def database_url() -> str:
    """Database URL for testing (session-scoped for performance)."""
    return "postgresql://test:test@localhost/test_db"
```

### Fixture with Cleanup
```python
@pytest.fixture
def temp_file() -> Generator[Path, None, None]:
    """Create temporary file, clean up after test."""
    path = Path(tempfile.mktemp())
    path.write_text("test content")
    yield path
    path.unlink(missing_ok=True)

@pytest.fixture
def database_session(engine: Engine) -> Generator[Session, None, None]:
    """Create database session with rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
```

### Parameterized Fixtures
```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request: pytest.FixtureRequest) -> Database:
    """Test with multiple database backends."""
    if request.param == "sqlite":
        return SQLiteDatabase(":memory:")
    return PostgreSQLDatabase(os.environ["TEST_DATABASE_URL"])
```

## Mocking Patterns

### Basic Mocking
```python
from unittest.mock import Mock, AsyncMock, patch

def test_user_service_calls_repository() -> None:
    mock_repo = Mock(spec=UserRepository)
    mock_repo.find_by_id.return_value = User(id="1", name="Test")
    
    service = UserService(repo=mock_repo)
    result = service.get_user("1")
    
    mock_repo.find_by_id.assert_called_once_with("1")
    assert result.name == "Test"

@patch("myapp.services.external_api")
def test_with_patched_dependency(mock_api: Mock) -> None:
    mock_api.fetch.return_value = {"status": "ok"}
    result = process_data()
    assert result.success
```

### Async Mocking
```python
@pytest.fixture
def mock_http_client() -> AsyncMock:
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.return_value = Mock(
        status_code=200,
        json=Mock(return_value={"id": "123"})
    )
    return client

async def test_async_fetch(mock_http_client: AsyncMock) -> None:
    service = DataService(client=mock_http_client)
    result = await service.fetch_data("123")
    
    mock_http_client.get.assert_awaited_once()
    assert result["id"] == "123"
```

### Context Manager Mocking
```python
def test_file_processing() -> None:
    mock_file = Mock()
    mock_file.read.return_value = "file content"
    mock_file.__enter__ = Mock(return_value=mock_file)
    mock_file.__exit__ = Mock(return_value=False)
    
    with patch("builtins.open", return_value=mock_file):
        result = process_file("test.txt")
    
    assert result == "processed: file content"
```

## Async Testing

### Pytest-asyncio
```python
import pytest

@pytest.mark.asyncio
async def test_async_function() -> None:
    result = await fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_async_context_manager() -> None:
    async with managed_resource() as resource:
        result = await resource.process()
        assert result.success
```

### Async Fixtures
```python
@pytest.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client

@pytest.fixture
async def database_pool() -> AsyncGenerator[Pool, None]:
    pool = await asyncpg.create_pool(DATABASE_URL)
    yield pool
    await pool.close()
```

## Property-Based Testing

### Hypothesis Basics
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1))
def test_string_processing_never_crashes(s: str) -> None:
    result = process_string(s)
    assert isinstance(result, str)

@given(st.integers(min_value=0, max_value=1000))
def test_calculate_price_always_positive(quantity: int) -> None:
    price = calculate_price(quantity)
    assert price >= 0
```

### Complex Strategies
```python
from hypothesis import given, strategies as st
from dataclasses import dataclass

@dataclass
class Order:
    id: str
    items: list[str]
    total: float

order_strategy = st.builds(
    Order,
    id=st.uuids().map(str),
    items=st.lists(st.text(min_size=1), min_size=1, max_size=10),
    total=st.floats(min_value=0.01, max_value=10000, allow_nan=False)
)

@given(order_strategy)
def test_order_serialization_roundtrip(order: Order) -> None:
    serialized = order_to_json(order)
    deserialized = order_from_json(serialized)
    assert deserialized == order
```

## Integration Testing

### Database Integration
```python
@pytest.fixture(scope="module")
def test_database() -> Generator[Database, None, None]:
    db = Database(TEST_DATABASE_URL)
    db.create_tables()
    yield db
    db.drop_tables()

def test_user_crud(test_database: Database) -> None:
    # Create
    user = test_database.users.create(email="test@example.com")
    assert user.id is not None
    
    # Read
    found = test_database.users.find_by_id(user.id)
    assert found.email == "test@example.com"
    
    # Update
    test_database.users.update(user.id, name="Updated")
    updated = test_database.users.find_by_id(user.id)
    assert updated.name == "Updated"
    
    # Delete
    test_database.users.delete(user.id)
    assert test_database.users.find_by_id(user.id) is None
```

### API Integration
```python
from fastapi.testclient import TestClient

@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)

def test_create_user_endpoint(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/users/nonexistent")
    assert response.status_code == 404
```
