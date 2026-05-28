# Python Unit Testing Patterns

## pytest Patterns

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from myapp.services import OrderService
from myapp.exceptions import ValidationError


class TestOrderService:
    """Tests for OrderService."""
    
    @pytest.fixture
    def mock_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_payment_gateway(self):
        return Mock()
    
    @pytest.fixture
    def service(self, mock_repository, mock_payment_gateway):
        return OrderService(
            repository=mock_repository,
            payment_gateway=mock_payment_gateway
        )
    
    class TestCreateOrder:
        """Tests for create_order method."""
        
        def test_with_valid_input_creates_order(self, service, mock_repository):
            # Arrange
            mock_repository.save.return_value = {"id": "order-123"}
            
            # Act
            result = service.create_order(item_id="item-1", quantity=2)
            
            # Assert
            assert result["id"] == "order-123"
            mock_repository.save.assert_called_once()
        
        def test_with_negative_quantity_raises_validation_error(self, service):
            with pytest.raises(ValidationError, match="quantity must be positive"):
                service.create_order(item_id="item-1", quantity=-1)
```

### Naming Conventions

```
test_<method>_<state>_<expected>
```

Examples:
- `test_create_order_with_valid_input_saves_to_repository`
- `test_calculate_total_with_empty_cart_returns_zero`
- `test_authenticate_with_expired_token_raises_auth_error`

### Fixtures

```python
@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(id=1, name="Test User", email="test@example.com")

@pytest.fixture
def sample_users():
    """Create multiple sample users."""
    return [
        User(id=i, name=f"User {i}", email=f"user{i}@example.com")
        for i in range(1, 4)
    ]

@pytest.fixture(autouse=True)
def reset_cache():
    """Reset cache before each test."""
    cache.clear()
    yield
    cache.clear()

@pytest.fixture(scope="module")
def database_connection():
    """Module-scoped database connection."""
    conn = create_connection()
    yield conn
    conn.close()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_value,expected", [
    (0, 0),
    (1, 1),
    (5, 120),
    (10, 3628800),
])
def test_factorial_with_valid_input_returns_correct_result(input_value, expected):
    assert calculator.factorial(input_value) == expected


@pytest.mark.parametrize("invalid_input,expected_error", [
    (None, TypeError),
    ("", ValueError),
    (-1, ValueError),
])
def test_process_with_invalid_input_raises_error(invalid_input, expected_error):
    with pytest.raises(expected_error):
        processor.process(invalid_input)


# Using ids for readable test names
@pytest.mark.parametrize("status_code,expected_retry", [
    pytest.param(500, True, id="server_error_should_retry"),
    pytest.param(503, True, id="service_unavailable_should_retry"),
    pytest.param(400, False, id="client_error_should_not_retry"),
    pytest.param(200, False, id="success_should_not_retry"),
])
def test_should_retry(status_code, expected_retry):
    assert client.should_retry(status_code) == expected_retry
```

## Mocking Patterns

### unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock, PropertyMock

# Simple mock
mock_service = Mock()
mock_service.get_user.return_value = {"id": 1, "name": "Test"}

# Configure return values
mock_client = Mock()
mock_client.fetch.side_effect = [
    {"data": "first"},
    {"data": "second"},
    ConnectionError("Connection lost"),
]

# Async mock
async_mock = Mock()
async_mock.fetch = AsyncMock(return_value={"result": "data"})

# Property mock
with patch.object(User, 'is_active', new_callable=PropertyMock) as mock_active:
    mock_active.return_value = True
    assert user.is_active is True
```

### patch Decorator

```python
@patch('myapp.services.EmailClient')
def test_sends_notification(self, mock_email_client):
    mock_instance = mock_email_client.return_value
    mock_instance.send.return_value = True
    
    service.notify_user(user_id=1, message="Hello")
    
    mock_instance.send.assert_called_once_with(
        to="user@example.com",
        body="Hello"
    )

@patch('myapp.services.requests.get')
@patch('myapp.services.cache.get')
def test_fetches_from_api_when_cache_miss(self, mock_cache, mock_requests):
    mock_cache.return_value = None
    mock_requests.return_value.json.return_value = {"data": "fresh"}
    
    result = service.get_data("key")
    
    assert result == {"data": "fresh"}
    mock_requests.assert_called_once()
```

### Context Manager Patching

```python
def test_handles_connection_error(self):
    with patch('myapp.client.connect') as mock_connect:
        mock_connect.side_effect = ConnectionError("Failed")
        
        result = service.safe_connect()
        
        assert result.is_error
        assert "Failed" in result.message
```

## Assertion Patterns

### Built-in Assertions

```python
# Equality
assert result == expected
assert result != unexpected

# Truthiness
assert result is True
assert result is not None
assert items  # non-empty

# Collections
assert item in collection
assert len(items) == 3
assert set(items) == {"a", "b", "c"}

# Approximate equality (for floats)
assert result == pytest.approx(3.14159, rel=1e-5)
```

### Exception Testing

```python
# Basic exception check
with pytest.raises(ValueError):
    service.process(invalid_input)

# Check exception message
with pytest.raises(ValueError, match="must be positive"):
    service.process(-1)

# Access exception info
with pytest.raises(ValidationError) as exc_info:
    service.validate(data)

assert exc_info.value.field == "email"
assert "invalid format" in str(exc_info.value)
```

### Mock Assertions

```python
# Called assertions
mock.assert_called()
mock.assert_called_once()
mock.assert_called_with(arg1, arg2, key=value)
mock.assert_called_once_with(expected_arg)

# Call count
assert mock.call_count == 3

# Not called
mock.assert_not_called()

# Call args inspection
args, kwargs = mock.call_args
assert args[0] == expected_first_arg
assert kwargs["key"] == expected_value

# Multiple calls
assert mock.call_args_list == [
    call("first"),
    call("second"),
    call("third"),
]
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch_returns_data():
    result = await service.fetch_async("resource-id")
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_async_with_mock():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"data": "value"}
    
    service = MyService(client=mock_client)
    result = await service.process()
    
    assert result == {"data": "value"}
    mock_client.get.assert_awaited_once()
```

## Test Data Builders

```python
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class OrderBuilder:
    id: str = field(default_factory=lambda: f"order-{uuid.uuid4()}")
    customer_id: str = "customer-1"
    items: list = field(default_factory=list)
    status: str = "pending"
    
    def with_id(self, id: str) -> "OrderBuilder":
        self.id = id
        return self
    
    def with_status(self, status: str) -> "OrderBuilder":
        self.status = status
        return self
    
    def with_item(self, product_id: str, quantity: int) -> "OrderBuilder":
        self.items.append({"product_id": product_id, "quantity": quantity})
        return self
    
    def build(self) -> Order:
        return Order(
            id=self.id,
            customer_id=self.customer_id,
            items=self.items,
            status=self.status
        )


# Usage
order = (OrderBuilder()
    .with_status("shipped")
    .with_item("product-1", 2)
    .build())
```

## Markers

```python
# Skip tests
@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_syntax():
    pass

# Expected failures
@pytest.mark.xfail(reason="Known bug #123")
def test_known_issue():
    pass

# Custom markers
@pytest.mark.slow
def test_complex_integration():
    pass

@pytest.mark.integration
def test_database_connection():
    pass
```
