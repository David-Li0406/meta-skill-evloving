# Testing Standards

Guidelines for writing effective, maintainable tests.

## Core Principles

### Tests Are Documentation

Good tests explain what the code should do. A developer should be able to understand the feature by reading its tests.

### Tests Are Specification

Write tests that specify behavior, not implementation. Tests should survive refactoring.

### Tests Prevent Regression

Every bug fix should include a test that would have caught it.

---

## Test Structure

### Naming Convention

```
test_[unit]_[scenario]_[expected result]
```

Or in describe/it style:

```
describe('functionName') {
  it('should [expected behavior] when [condition]')
}
```

**Examples:**

```python
# Python
def test_calculate_total_with_empty_cart_returns_zero():
    ...

def test_user_login_with_invalid_password_raises_auth_error():
    ...
```

```javascript
// JavaScript
describe('calculateTotal', () => {
  it('should return zero when cart is empty', () => {
    ...
  });
  
  it('should apply discount when coupon is valid', () => {
    ...
  });
});
```

### Arrange-Act-Assert (AAA)

Every test should have three distinct sections:

```python
def test_apply_discount_reduces_price():
    # Arrange
    original_price = 100.00
    discount_percent = 20
    
    # Act
    final_price = apply_discount(original_price, discount_percent)
    
    # Assert
    assert final_price == 80.00
```

Use blank lines to separate sections. For very short tests, this can be compressed, but the mental model should always be AAA.

---

## Test Quality

### One Assertion Per Test (Preferred)

Each test should verify one behavior. Multiple assertions are okay if they verify the same logical concept:

```python
# Good - single concept
def test_create_user_returns_user_with_correct_fields():
    user = create_user(name="Alice", email="alice@test.com")
    
    assert user.name == "Alice"
    assert user.email == "alice@test.com"
    assert user.id is not None  # All part of "correct fields"

# Bad - multiple concepts
def test_user_creation_and_retrieval():
    user = create_user(name="Alice")
    assert user.name == "Alice"  # Concept 1: creation
    
    retrieved = get_user(user.id)
    assert retrieved.name == "Alice"  # Concept 2: retrieval
```

### Test Behavior, Not Implementation

```python
# Good - tests behavior
def test_shopping_cart_total_includes_all_items():
    cart = ShoppingCart()
    cart.add(Item(price=10))
    cart.add(Item(price=20))
    
    assert cart.total == 30

# Bad - tests implementation
def test_shopping_cart_adds_to_internal_list():
    cart = ShoppingCart()
    cart.add(Item(price=10))
    
    assert len(cart._items) == 1  # Testing private implementation
```

### Clear Failure Messages

When a test fails, the message should tell you what went wrong:

```python
# Good
assert result == expected, f"Expected {expected}, got {result}"

# Better with pytest
def test_user_age_must_be_positive():
    with pytest.raises(ValidationError) as exc_info:
        create_user(age=-1)
    
    assert "age" in str(exc_info.value).lower()
```

---

## Test Organization

### File Structure

```
src/
├── users/
│   ├── user_service.py
│   └── user_model.py
tests/
├── users/
│   ├── test_user_service.py
│   └── test_user_model.py
├── conftest.py           # Shared fixtures
└── fixtures/
    └── users.json        # Test data
```

### Test Categories

Organize tests by type with markers or directories:

| Type | Runs | Speed | Scope |
|------|------|-------|-------|
| Unit | Every commit | Fast (<100ms) | Single function/class |
| Integration | PR/merge | Medium | Multiple components |
| E2E | Deploy/nightly | Slow | Full system |

```python
import pytest

@pytest.mark.unit
def test_calculate_tax():
    ...

@pytest.mark.integration
def test_checkout_flow_with_payment():
    ...

@pytest.mark.e2e
def test_complete_user_journey():
    ...
```

---

## Fixtures & Setup

### Use Fixtures for Reusable Setup

```python
import pytest

@pytest.fixture
def user():
    """Provide a standard test user."""
    return User(id="123", name="Test User", email="test@example.com")

@pytest.fixture
def authenticated_client(user):
    """Provide an authenticated API client."""
    client = TestClient()
    client.login(user)
    return client

def test_get_profile(authenticated_client, user):
    response = authenticated_client.get("/profile")
    assert response.json()["name"] == user.name
```

### Fixture Scope

| Scope | When to Use |
|-------|-------------|
| `function` (default) | Fresh setup per test |
| `class` | Shared across test class |
| `module` | Shared across file |
| `session` | Shared across entire run |

```python
@pytest.fixture(scope="session")
def database():
    """Create database once for all tests."""
    db = create_test_database()
    yield db
    db.cleanup()
```

### Factory Fixtures

For when you need variations:

```python
@pytest.fixture
def make_user():
    """Factory for creating test users."""
    def _make_user(name="Test", email=None, **kwargs):
        email = email or f"{name.lower()}@test.com"
        return User(name=name, email=email, **kwargs)
    return _make_user

def test_admin_permissions(make_user):
    admin = make_user("Admin", is_admin=True)
    regular = make_user("Regular", is_admin=False)
    
    assert admin.can_delete_users()
    assert not regular.can_delete_users()
```

---

## Mocking

### Mock External Dependencies, Not Your Code

```python
# Good - mock external service
@patch('myapp.services.payment_gateway.charge')
def test_checkout_calls_payment_gateway(mock_charge):
    mock_charge.return_value = {"status": "success"}
    
    result = checkout(cart, payment_info)
    
    mock_charge.assert_called_once()
    assert result.success

# Bad - mocking everything
@patch('myapp.services.cart.calculate_total')
@patch('myapp.services.cart.validate')
@patch('myapp.services.cart.save')
def test_checkout(mock_save, mock_validate, mock_total):
    ...  # Testing nothing real
```

### Use Dependency Injection

Design for testability:

```python
class OrderService:
    def __init__(self, payment_gateway, inventory_service):
        self.payment = payment_gateway
        self.inventory = inventory_service
    
    def place_order(self, order):
        if not self.inventory.check(order.items):
            raise OutOfStockError()
        return self.payment.charge(order.total)

# In tests
def test_place_order_checks_inventory():
    mock_inventory = Mock()
    mock_inventory.check.return_value = True
    mock_payment = Mock()
    
    service = OrderService(mock_payment, mock_inventory)
    service.place_order(order)
    
    mock_inventory.check.assert_called_with(order.items)
```

---

## Edge Cases

### Always Test

| Category | Examples |
|----------|----------|
| Empty inputs | Empty string, empty list, None |
| Boundary values | 0, 1, -1, max, min |
| Invalid inputs | Wrong type, malformed data |
| Error conditions | Network failure, timeout, missing data |

```python
class TestCalculateAverage:
    def test_with_normal_list(self):
        assert calculate_average([1, 2, 3]) == 2.0
    
    def test_with_empty_list_raises(self):
        with pytest.raises(ValueError):
            calculate_average([])
    
    def test_with_single_element(self):
        assert calculate_average([5]) == 5.0
    
    def test_with_negative_numbers(self):
        assert calculate_average([-1, 1]) == 0.0
    
    def test_with_floats(self):
        assert calculate_average([1.5, 2.5]) == 2.0
```

---

## Anti-Patterns to Avoid

### Flaky Tests

Tests that sometimes pass and sometimes fail. Causes:
- Time-dependent logic without mocking
- Order-dependent tests
- Shared mutable state
- Network calls

### Slow Tests

Unit tests should be fast (<100ms). If slow:
- Mock external services
- Use in-memory databases
- Reduce fixture setup

### Testing Private Methods

Test through the public API:

```python
# Bad
def test_internal_validation():
    assert obj._validate(data)

# Good
def test_create_validates_input():
    with pytest.raises(ValidationError):
        obj.create(invalid_data)
```

### Over-Mocking

If everything is mocked, you're testing nothing:

```python
# Bad - what is this even testing?
@patch('module.function_a')
@patch('module.function_b')
@patch('module.function_c')
def test_main(mock_c, mock_b, mock_a):
    mock_a.return_value = "a"
    mock_b.return_value = "b"
    mock_c.return_value = "c"
    
    result = main()
    
    assert result == "expected"  # This proves nothing
```

---

## Test Coverage

### Coverage Goals

- **Critical paths:** 100% (auth, payments, data mutations)
- **Business logic:** 90%+
- **Utilities:** 80%+
- **Boilerplate/glue:** Best effort

### Coverage Is Not Quality

High coverage doesn't mean good tests. A test that asserts nothing adds coverage but not confidence:

```python
# 100% coverage, 0% value
def test_process_data():
    process_data([1, 2, 3])  # No assertion!
```
