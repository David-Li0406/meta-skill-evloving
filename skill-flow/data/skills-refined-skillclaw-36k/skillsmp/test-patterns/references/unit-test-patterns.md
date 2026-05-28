# Unit Test Patterns

Patterns for writing effective unit tests across languages.

## Mocking Patterns

### Dependency Injection for Testability

**Before (hard to test):**
```python
class OrderService:
    def complete(self, order_id):
        order = Order.find(order_id)  # Direct DB call
        EmailService().send(order.user.email)  # Hard-coded dependency
```

**After (testable):**
```python
class OrderService:
    def __init__(self, order_repo, email_service):
        self.order_repo = order_repo
        self.email_service = email_service

    def complete(self, order_id):
        order = self.order_repo.find(order_id)
        self.email_service.send(order.user.email)
```

### Mock vs Stub vs Spy

| Type | Purpose | Verification |
|------|---------|--------------|
| **Stub** | Provide canned answers | None |
| **Mock** | Verify interactions | Called with specific args |
| **Spy** | Record calls for later verification | Call history |

**Stub Example:**
```python
# Just returns a value, no verification
user_repo = Mock()
user_repo.find.return_value = User(name="Alice")
```

**Mock Example:**
```python
# Verifies it was called correctly
email_service = Mock()
service.notify(user)
email_service.send.assert_called_once_with("alice@example.com")
```

**Spy Example:**
```python
# Records all calls for flexible verification
logger = Mock()
service.process(items)
assert logger.info.call_count == len(items)
```

### Partial Mocking

When you need to mock only some methods:

```python
@patch.object(Order, 'save')
def test_save_is_called(mock_save):
    order = Order(items=[item])
    order.complete()  # Uses real methods except save
    mock_save.assert_called_once()
```

## Fixture Patterns

### Factory Pattern

Create objects with sensible defaults:

```python
def create_user(**overrides):
    defaults = {
        "name": "Test User",
        "email": "test@example.com",
        "status": "active"
    }
    return User(**{**defaults, **overrides})

# Usage
user = create_user(status="pending")
```

### Builder Pattern

For complex objects:

```python
class OrderBuilder:
    def __init__(self):
        self._items = []
        self._user = None
        self._discount = 0

    def with_items(self, *items):
        self._items = list(items)
        return self

    def for_user(self, user):
        self._user = user
        return self

    def with_discount(self, percent):
        self._discount = percent
        return self

    def build(self):
        order = Order(user=self._user, items=self._items)
        if self._discount:
            order.apply_discount(self._discount)
        return order

# Usage
order = (OrderBuilder()
    .with_items(item1, item2)
    .for_user(user)
    .with_discount(10)
    .build())
```

### Shared Fixtures (pytest)

```python
# conftest.py
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()

@pytest.fixture
def user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.flush()
    return user
```

## Assertion Patterns

### Custom Matchers

```python
def assert_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    assert re.match(pattern, email), f"Invalid email: {email}"

# Usage
assert_valid_email(user.email)
```

### Soft Assertions (collect all failures)

```python
from pytest_check import check

def test_user_attributes():
    user = create_user()
    with check:
        assert user.name == "Expected Name"
    with check:
        assert user.email == "expected@example.com"
    with check:
        assert user.status == "active"
    # All assertions run, failures collected
```

### Snapshot Testing

```python
def test_api_response(snapshot):
    response = api.get_user(1)
    snapshot.assert_match(response.json(), 'user_response')
```

## Edge Case Patterns

### Boundary Testing

```python
@pytest.mark.parametrize("value,expected", [
    (0, "zero"),
    (1, "positive"),
    (-1, "negative"),
    (float('inf'), "overflow"),
    (None, "null"),
])
def test_classify_number(value, expected):
    assert classify(value) == expected
```

### Error Condition Testing

```python
def test_raises_on_invalid_input():
    with pytest.raises(ValueError) as exc_info:
        process_order(None)

    assert "Order cannot be None" in str(exc_info.value)
```

### Timeout Testing

```python
@pytest.mark.timeout(5)
def test_slow_operation_completes():
    result = potentially_slow_operation()
    assert result is not None
```

## Test Organization

### Given-When-Then Comments

```python
def test_order_completion_sends_notification():
    # Given an order ready for completion
    order = create_order(status="pending")
    notification_service = Mock()

    # When the order is completed
    complete_order(order, notification_service)

    # Then a notification is sent
    notification_service.send.assert_called_once()
```

### Test Class Organization

```python
class TestOrderService:
    """Tests for OrderService"""

    class TestCreate:
        """Tests for create method"""

        def test_creates_with_valid_data(self):
            pass

        def test_raises_on_missing_items(self):
            pass

    class TestComplete:
        """Tests for complete method"""

        def test_marks_order_complete(self):
            pass

        def test_sends_confirmation_email(self):
            pass
```

## Anti-Patterns to Avoid

### 1. Testing Implementation Details

```python
# WRONG - Tests internal state
def test_order_internal():
    order = Order()
    order.add_item(item)
    assert order._items == [item]  # Testing private attribute

# RIGHT - Tests behavior
def test_order_contains_item():
    order = Order()
    order.add_item(item)
    assert item in order.items
```

### 2. Excessive Mocking

```python
# WRONG - Mocking everything
def test_over_mocked():
    mock_order = Mock()
    mock_user = Mock()
    mock_item = Mock()
    # Test is just verifying mock configuration

# RIGHT - Mock only external dependencies
def test_appropriately_mocked():
    order = Order(items=[real_item])
    email_service = Mock()  # Only mock external service
```

### 3. Test Interdependence

```python
# WRONG - Tests depend on each other
class TestOrder:
    order = None  # Shared state!

    def test_create(self):
        TestOrder.order = Order.create()

    def test_add_item(self):
        TestOrder.order.add_item(item)  # Fails if test_create didn't run
```

### 4. Non-Deterministic Tests

```python
# WRONG - Uses real time
def test_expiry():
    order = Order()
    time.sleep(2)
    assert order.is_expired()

# RIGHT - Controls time
def test_expiry(freezer):
    order = Order()
    freezer.move_to(order.created_at + timedelta(days=30))
    assert order.is_expired()
```
