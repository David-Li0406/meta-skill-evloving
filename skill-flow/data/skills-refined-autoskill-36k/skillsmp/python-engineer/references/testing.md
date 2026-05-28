# Testing with pytest

## Test Structure

### Arrange-Act-Assert pattern
```python
def test_user_creation_with_valid_data_succeeds():
    # Arrange
    service = UserService(mock_repository)
    user_data = UserCreate(email="test@example.com", name="Test")

    # Act
    result = service.create(user_data)

    # Assert
    assert result.email == "test@example.com"
    assert result.id is not None
```

### Test naming
```
test_<unit>_<scenario>_<expected_result>
```
Examples:
- `test_create_user_with_valid_email_returns_user`
- `test_create_user_with_duplicate_email_raises_conflict_error`
- `test_get_user_with_nonexistent_id_returns_none`

## Fixtures

### Basic fixture
```python
import pytest

@pytest.fixture
def user_repository() -> UserRepository:
    return InMemoryUserRepository()

@pytest.fixture
def user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)
```

### Fixture with cleanup
```python
@pytest.fixture
def temp_database():
    db = create_test_database()
    yield db
    db.drop_all()
```

### Parametrized fixtures
```python
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    if request.param == "sqlite":
        return SQLiteDatabase()
    return PostgresDatabase()
```

## Parametrized Tests

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("user@subdomain.example.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(email: str, valid: bool):
    result = is_valid_email(email)
    assert result == valid
```

## Testing Exceptions

```python
def test_create_user_with_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        create_user(email="invalid")

    assert "email" in str(exc_info.value)
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_user_creation():
    service = AsyncUserService()
    result = await service.create(user_data)
    assert result.id is not None
```

## Mocking Best Practices

### Prefer fakes over mocks
```python
# Prefer: In-memory implementation
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, id: str) -> User | None:
        return self._users.get(id)

# Avoid: Heavy mocking
@mock.patch("app.services.user_service.UserRepository")
def test_with_mock(mock_repo):
    mock_repo.find_by_id.return_value = User(...)
```

### When mocking is appropriate
- External APIs
- Time-dependent code
- Random values
- File system operations in unit tests

```python
from unittest.mock import patch
from freezegun import freeze_time

@freeze_time("2024-01-15")
def test_subscription_expiry():
    subscription = create_subscription(days=30)
    assert subscription.expires_at == datetime(2024, 2, 14)

@patch("app.services.external_api.requests.get")
def test_external_api_integration(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_external_data()
    assert result.status == "ok"
```

## Test Coverage Guidelines

Focus on:
- Public API methods
- Business logic branches
- Error handling paths
- Edge cases (empty, None, boundary values)

Don't obsess over:
- 100% coverage metrics
- Testing trivial getters/setters
- Testing framework code
