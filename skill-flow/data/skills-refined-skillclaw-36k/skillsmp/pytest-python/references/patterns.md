# Common Testing Patterns

## Table of Contents

1. [Test Organization](#test-organization)
2. [Mocking Patterns](#mocking-patterns)
3. [Database Testing](#database-testing)
4. [API Testing](#api-testing)
5. [File System Testing](#file-system-testing)
6. [Time-Dependent Tests](#time-dependent-tests)
7. [Error Handling Tests](#error-handling-tests)
8. [Performance Testing](#performance-testing)

## Test Organization

### Arrange-Act-Assert (AAA)

```python
def test_user_discount():
    # Arrange
    user = User(membership="premium")
    product = Product(price=100)

    # Act
    total = calculate_total(user, product)

    # Assert
    assert total == 90  # 10% discount
```

### Given-When-Then (BDD Style)

```python
def test_premium_user_gets_discount():
    # Given a premium user
    user = User(membership="premium")
    product = Product(price=100)

    # When calculating total
    total = calculate_total(user, product)

    # Then 10% discount is applied
    assert total == 90
```

### Test Classes for Grouping

```python
class TestUserAuthentication:
    """Group related authentication tests."""

    def test_valid_credentials(self, auth_service):
        result = auth_service.login("user", "password")
        assert result.success

    def test_invalid_password(self, auth_service):
        result = auth_service.login("user", "wrong")
        assert not result.success

    def test_locked_account(self, auth_service, locked_user):
        result = auth_service.login(locked_user.email, "password")
        assert result.error == "account_locked"
```

## Mocking Patterns

### External API Calls

```python
def test_weather_service(monkeypatch):
    mock_response = {"temp": 72, "condition": "sunny"}

    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return mock_response
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    weather = get_weather("NYC")
    assert weather["temp"] == 72
```

### Class Methods

```python
def test_email_notification(monkeypatch):
    sent_emails = []

    def mock_send(self, to, subject, body):
        sent_emails.append({"to": to, "subject": subject})

    monkeypatch.setattr(EmailService, "send", mock_send)

    notify_user(User(email="test@example.com"))
    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == "test@example.com"
```

### Using unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_db = Mock()
    mock_db.query.return_value = [{"id": 1, "name": "Test"}]

    service = UserService(mock_db)
    users = service.get_all()

    mock_db.query.assert_called_once()
    assert len(users) == 1

@patch("mymodule.external_api")
def test_with_patch(mock_api):
    mock_api.fetch.return_value = {"data": "test"}
    result = process_data()
    assert result == "test"
```

## Database Testing

### Transaction Rollback

```python
@pytest.fixture
def db_session(database):
    """Rollback after each test."""
    session = database.create_session()
    session.begin_nested()  # Savepoint
    yield session
    session.rollback()
    session.close()

def test_user_creation(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.flush()
    assert user.id is not None
    # Rolled back automatically
```

### Test Data Builders

```python
class UserBuilder:
    def __init__(self):
        self._email = "default@example.com"
        self._role = "user"

    def with_email(self, email):
        self._email = email
        return self

    def with_role(self, role):
        self._role = role
        return self

    def build(self):
        return User(email=self._email, role=self._role)

@pytest.fixture
def user_builder():
    return UserBuilder()

def test_admin_permissions(user_builder):
    admin = user_builder.with_role("admin").build()
    assert admin.can_delete_users()
```

## API Testing

### HTTP Client Testing

```python
@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_create_user(client):
    response = client.post("/api/users", json={
        "email": "new@example.com",
        "name": "New User"
    })
    assert response.status_code == 201
    assert response.json["email"] == "new@example.com"

def test_authentication_required(client):
    response = client.get("/api/protected")
    assert response.status_code == 401
```

### Response Validation

```python
def test_user_response_schema(client):
    response = client.get("/api/users/1")

    assert response.status_code == 200
    data = response.json

    # Validate structure
    assert "id" in data
    assert "email" in data
    assert "created_at" in data

    # Validate types
    assert isinstance(data["id"], int)
    assert "@" in data["email"]
```

## File System Testing

### Using tmp_path

```python
def test_file_processing(tmp_path):
    # Create test file
    input_file = tmp_path / "input.txt"
    input_file.write_text("line1\nline2\nline3")

    # Process
    output_file = tmp_path / "output.txt"
    process_file(input_file, output_file)

    # Verify
    assert output_file.exists()
    content = output_file.read_text()
    assert "PROCESSED" in content

def test_directory_creation(tmp_path):
    config_dir = tmp_path / "config"
    initialize_config(config_dir)

    assert config_dir.exists()
    assert (config_dir / "settings.json").exists()
```

### File Fixtures

```python
@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,value\ntest,123\n")
    return csv_file

def test_csv_import(sample_csv, database):
    import_csv(sample_csv, database)
    assert database.count("records") == 1
```

## Time-Dependent Tests

### Freezing Time

```python
from freezegun import freeze_time

@freeze_time("2024-01-15 12:00:00")
def test_subscription_expiry():
    user = User(subscription_end="2024-01-14")
    assert user.is_expired()

@freeze_time("2024-01-13 12:00:00")
def test_subscription_active():
    user = User(subscription_end="2024-01-14")
    assert not user.is_expired()
```

### Mocking datetime

```python
def test_daily_report(monkeypatch):
    import datetime

    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime.datetime(2024, 1, 15, 9, 0, 0)

    monkeypatch.setattr("mymodule.datetime", MockDatetime)

    report = generate_daily_report()
    assert report.date == "2024-01-15"
```

## Error Handling Tests

### Exception Messages

```python
def test_validation_error_message():
    with pytest.raises(ValidationError) as exc_info:
        validate_email("invalid")

    assert "Invalid email format" in str(exc_info.value)
    assert exc_info.value.field == "email"
```

### Multiple Exception Types

```python
@pytest.mark.parametrize("input,expected_error", [
    ("", ValueError),
    (None, TypeError),
    (-1, ValueError),
])
def test_invalid_inputs(input, expected_error):
    with pytest.raises(expected_error):
        process_input(input)
```

### Error Recovery

```python
def test_graceful_degradation(monkeypatch):
    def mock_fail(*args):
        raise ConnectionError("Service unavailable")

    monkeypatch.setattr("mymodule.external_service.call", mock_fail)

    # Should return cached/default value instead of crashing
    result = get_data_with_fallback()
    assert result == DEFAULT_VALUE
```

## Performance Testing

### Timing Tests

```python
import time

def test_query_performance():
    start = time.perf_counter()
    result = expensive_query()
    duration = time.perf_counter() - start

    assert duration < 1.0  # Should complete in under 1 second
    assert len(result) > 0
```

### Memory Testing

```python
import tracemalloc

def test_memory_efficiency():
    tracemalloc.start()

    process_large_dataset()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Peak memory should be under 100MB
    assert peak < 100 * 1024 * 1024
```

### Benchmark with pytest-benchmark

```python
def test_sorting_performance(benchmark):
    data = list(range(10000, 0, -1))

    result = benchmark(sorted, data)

    assert result == list(range(1, 10001))
```

## Parametrized Edge Cases

```python
@pytest.mark.parametrize("input,expected", [
    # Normal cases
    ("hello", "HELLO"),
    ("World", "WORLD"),
    # Edge cases
    ("", ""),
    ("a", "A"),
    # Unicode
    ("cafe", "CAFE"),
    # Already uppercase
    ("HELLO", "HELLO"),
    # Mixed
    ("HeLLo", "HELLO"),
])
def test_uppercase(input, expected):
    assert to_uppercase(input) == expected
```
