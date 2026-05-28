---
applyTo: "**/*.test.{py,ts,js,java}"
---

# Testing Patterns - Enterprise Standards

> These patterns are extracted from our existing test suite. Follow them for consistency.

## Test Structure

### Naming Convention

- Python: `test_<function_name>_<scenario>_<expected_result>`
- TypeScript/JavaScript: `should <expected behavior> when <condition>`
- Java: `<methodName>_<scenario>_<expectedResult>`

### Organization

```python
# Group related tests in classes
class TestOrderService:
    """Tests for OrderService class."""
    
    class TestCreateOrder:
        """Tests for create_order method."""
        
        def test_create_order_with_valid_data_returns_order(self):
            pass
            
        def test_create_order_with_empty_items_raises_validation_error(self):
            pass
```

## Arrange-Act-Assert Pattern

Every test should follow AAA:

```python
def test_calculate_discount_with_premium_customer_returns_20_percent(self):
    # Arrange
    customer = create_customer(tier="premium")
    order = create_order(subtotal=100.00)
    
    # Act
    discount = calculate_discount(customer, order)
    
    # Assert
    assert discount == 20.00
```

## Mocking Guidelines

### What to Mock

- External API calls
- Database connections
- File system operations
- Current time (use `freezegun` or similar)
- Random number generation

### What NOT to Mock

- The code under test
- Simple data transformations
- Pure functions

```python
# DO: Mock external dependency
@patch('services.payment.PaymentGateway.charge')
def test_process_payment_calls_gateway(self, mock_charge):
    mock_charge.return_value = PaymentResult(success=True)
    result = process_payment(order)
    mock_charge.assert_called_once()

# DON'T: Mock the function under test
```

## Fixture Patterns

Use our standard fixtures from `conftest.py`:

```python
@pytest.fixture
def authenticated_user(db_session):
    """Creates an authenticated user for testing."""
    user = create_user(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def sample_order(authenticated_user):
    """Creates a sample order for the authenticated user."""
    return create_order(user=authenticated_user, items=[
        OrderItem(product_id="SKU-001", quantity=2, price=29.99)
    ])
```

## Edge Cases to Always Test

1. **Empty inputs**: Empty strings, empty lists, None values
2. **Boundary values**: 0, 1, max values, negative numbers
3. **Invalid types**: Wrong type passed to function
4. **Error states**: Network failures, database errors, timeouts
5. **Concurrency**: Race conditions where applicable

## Error Handling Tests

```python
def test_get_order_with_invalid_id_raises_not_found(self):
    with pytest.raises(OrderNotFoundError) as exc_info:
        get_order("invalid-id")
    
    assert "invalid-id" in str(exc_info.value)

def test_create_order_with_invalid_data_returns_validation_errors(self):
    errors = validate_order(invalid_data)
    assert len(errors) > 0
    assert "items" in errors
```

## Coverage Requirements

- Minimum 80% line coverage for new code
- 100% coverage for critical paths (payments, auth, data mutations)
- All public methods must have at least one test
