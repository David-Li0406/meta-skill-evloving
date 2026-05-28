---
id: unit-testing
name: "Unit Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Unit Testing

## Overview

Unit testing involves testing individual components in isolation to verify they work correctly. This methodology covers test structure, assertions, mocking, and best practices for writing maintainable, reliable unit tests.

## When to Use

- Testing individual functions, methods, or classes
- Verifying business logic correctness
- Catching regressions during refactoring
- Documenting expected behavior
- Test-driven development (TDD)

## Key Principles

- **Test one thing**: Each test should verify a single behavior
- **Fast and isolated**: No external dependencies, milliseconds to run
- **Deterministic**: Same input always produces same result
- **Self-documenting**: Test names describe expected behavior
- **Arrange-Act-Assert**: Clear structure for readability

## Best Practices

### Test Structure (AAA Pattern)

```python
import pytest
from decimal import Decimal

# System under test
class PriceCalculator:
    def __init__(self, tax_rate: Decimal):
        self.tax_rate = tax_rate

    def calculate_total(self, price: Decimal, quantity: int) -> Decimal:
        subtotal = price * quantity
        tax = subtotal * self.tax_rate
        return subtotal + tax

# Tests following AAA pattern
class TestPriceCalculator:

    def test_calculate_total_with_single_item(self):
        # Arrange
        calculator = PriceCalculator(tax_rate=Decimal("0.10"))

        # Act
        result = calculator.calculate_total(
            price=Decimal("100.00"),
            quantity=1
        )

        # Assert
        assert result == Decimal("110.00")

    def test_calculate_total_with_multiple_items(self):
        # Arrange
        calculator = PriceCalculator(tax_rate=Decimal("0.10"))

        # Act
        result = calculator.calculate_total(
            price=Decimal("25.00"),
            quantity=4
        )

        # Assert
        assert result == Decimal("110.00")  # 100 + 10 tax

    def test_calculate_total_with_zero_tax(self):
        # Arrange
        calculator = PriceCalculator(tax_rate=Decimal("0.00"))

        # Act
        result = calculator.calculate_total(
            price=Decimal("50.00"),
            quantity=2
        )

        # Assert
        assert result == Decimal("100.00")
```

### Naming Conventions

```python
# Pattern: test_<method>_<scenario>_<expected_result>

def test_calculate_total_with_zero_quantity_returns_zero():
    pass

def test_validate_email_with_invalid_format_raises_validation_error():
    pass

def test_get_user_when_not_found_returns_none():
    pass

# BDD-style: test_should_<expected_behavior>_when_<condition>

def test_should_return_empty_list_when_no_orders_exist():
    pass

def test_should_send_notification_when_order_is_placed():
    pass
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123abc", "123ABC"),
])
def test_uppercase_conversion(input_value, expected):
    assert input_value.upper() == expected

@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("user.name@domain.co.uk", True),
    ("invalid", False),
    ("@no-local.com", False),
    ("no-at-sign.com", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    result = validate_email(email)
    assert result == is_valid

# Named test cases for better readability
@pytest.mark.parametrize("a,b,expected", [
    pytest.param(1, 2, 3, id="positive_numbers"),
    pytest.param(-1, 1, 0, id="mixed_signs"),
    pytest.param(0, 0, 0, id="zeros"),
    pytest.param(-5, -3, -8, id="negative_numbers"),
])
def test_addition(a, b, expected):
    assert add(a, b) == expected
```

### Testing Exceptions

```python
import pytest

class InsufficientFundsError(Exception):
    def __init__(self, balance: Decimal, amount: Decimal):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}, balance is {balance}")

class BankAccount:
    def __init__(self, balance: Decimal):
        self.balance = balance

    def withdraw(self, amount: Decimal) -> Decimal:
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

class TestBankAccount:

    def test_withdraw_more_than_balance_raises_error(self):
        account = BankAccount(balance=Decimal("100.00"))

        with pytest.raises(InsufficientFundsError) as exc_info:
            account.withdraw(Decimal("150.00"))

        assert exc_info.value.balance == Decimal("100.00")
        assert exc_info.value.amount == Decimal("150.00")

    def test_withdraw_exact_balance_succeeds(self):
        account = BankAccount(balance=Decimal("100.00"))

        result = account.withdraw(Decimal("100.00"))

        assert result == Decimal("0.00")
        assert account.balance == Decimal("0.00")
```

### Fixtures for Setup

```python
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User",
        created_at=datetime.utcnow()
    )

@pytest.fixture
def expired_user():
    """Create a user with expired subscription."""
    return User(
        id="user-456",
        email="expired@example.com",
        subscription_end=datetime.utcnow() - timedelta(days=1)
    )

@pytest.fixture
def user_service(sample_user):
    """Create user service with sample data."""
    repo = InMemoryUserRepository()
    repo.add(sample_user)
    return UserService(repo)

# Using fixtures
class TestUserService:

    def test_find_user_by_id(self, user_service, sample_user):
        result = user_service.find_by_id(sample_user.id)
        assert result == sample_user

    def test_find_nonexistent_user_returns_none(self, user_service):
        result = user_service.find_by_id("nonexistent")
        assert result is None

# Fixture with cleanup
@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file that's cleaned up after test."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    yield file_path
    # Cleanup happens automatically with tmp_path
```

### Testing Async Code

```python
import pytest
import asyncio

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_async_fetch_user():
    service = AsyncUserService()

    result = await service.get_user("user-123")

    assert result.id == "user-123"

@pytest.mark.asyncio
async def test_async_operation_timeout():
    service = SlowService()

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            service.slow_operation(),
            timeout=0.1
        )

# Testing async generators
@pytest.mark.asyncio
async def test_async_stream():
    results = []
    async for item in async_generator():
        results.append(item)

    assert len(results) == 10
```

### TypeScript/Jest Testing

```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';

// System under test
class OrderService {
  constructor(
    private readonly repository: OrderRepository,
    private readonly paymentGateway: PaymentGateway
  ) {}

  async placeOrder(order: Order): Promise<OrderResult> {
    const saved = await this.repository.save(order);
    const payment = await this.paymentGateway.charge(order.total);
    return { orderId: saved.id, paymentId: payment.id };
  }
}

describe('OrderService', () => {
  let service: OrderService;
  let mockRepository: jest.Mocked<OrderRepository>;
  let mockPaymentGateway: jest.Mocked<PaymentGateway>;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
    };
    mockPaymentGateway = {
      charge: jest.fn(),
    };
    service = new OrderService(mockRepository, mockPaymentGateway);
  });

  describe('placeOrder', () => {
    it('should save order and process payment', async () => {
      // Arrange
      const order: Order = { items: [], total: 100 };
      mockRepository.save.mockResolvedValue({ id: 'order-1', ...order });
      mockPaymentGateway.charge.mockResolvedValue({ id: 'payment-1' });

      // Act
      const result = await service.placeOrder(order);

      // Assert
      expect(result.orderId).toBe('order-1');
      expect(result.paymentId).toBe('payment-1');
      expect(mockRepository.save).toHaveBeenCalledWith(order);
      expect(mockPaymentGateway.charge).toHaveBeenCalledWith(100);
    });

    it('should throw when payment fails', async () => {
      // Arrange
      mockRepository.save.mockResolvedValue({ id: 'order-1' });
      mockPaymentGateway.charge.mockRejectedValue(new Error('Payment declined'));

      // Act & Assert
      await expect(service.placeOrder({ items: [], total: 100 }))
        .rejects.toThrow('Payment declined');
    });
  });
});
```

### Test Doubles

```python
from unittest.mock import Mock, MagicMock, patch, AsyncMock

# Stub: Returns canned responses
def test_with_stub():
    repo = Mock()
    repo.find_by_id.return_value = User(id="123", name="Test")

    service = UserService(repo)
    result = service.get_user("123")

    assert result.name == "Test"

# Mock: Verifies interactions
def test_with_mock():
    notifier = Mock()
    service = OrderService(notifier=notifier)

    service.complete_order("order-123")

    notifier.send_notification.assert_called_once_with(
        "order-123", "Order completed"
    )

# Spy: Wraps real object
def test_with_spy():
    real_calculator = Calculator()
    spy = Mock(wraps=real_calculator)

    result = spy.add(2, 3)

    assert result == 5  # Real behavior
    spy.add.assert_called_with(2, 3)  # Interaction verified

# Fake: Working implementation for testing
class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

def test_with_fake():
    fake_repo = FakeUserRepository()
    service = UserService(fake_repo)

    service.create_user(User(id="123", name="Test"))
    result = service.get_user("123")

    assert result.name == "Test"
```

## Anti-patterns

- **Testing implementation details**: Tests break when refactoring
- **Over-mocking**: Testing mocks instead of behavior
- **Shared mutable state**: Tests affect each other
- **Testing private methods**: Test through public interface
- **Flaky tests**: Random failures due to timing or order
- **Giant test methods**: Hard to understand what's being tested
- **No assertions**: Tests that always pass

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [xUnit Test Patterns](http://xunitpatterns.com/)
- [Testing Python - Harry Percival](https://www.obeythetestinggoat.com/)
