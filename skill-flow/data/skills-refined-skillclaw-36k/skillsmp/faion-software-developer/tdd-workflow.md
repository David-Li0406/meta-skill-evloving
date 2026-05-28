---
id: tdd-workflow
name: "TDD Workflow"
domain: DEV
skill: faion-software-developer
category: "development"
---

# TDD Workflow

## Overview

Test-Driven Development (TDD) is a software development practice where tests are written before implementation code. The cycle of Red-Green-Refactor ensures code is testable by design, meets requirements, and maintains high quality through continuous refactoring.

## When to Use

- Building new features with well-defined requirements
- Fixing bugs (write failing test first, then fix)
- Complex business logic requiring verification
- API design (tests define the interface)
- When learning a new codebase or language

## Key Principles

- **Red-Green-Refactor**: Write failing test, make it pass, improve code
- **Write minimal code**: Only enough to pass the current test
- **One test at a time**: Focus on single behavior
- **Refactor with confidence**: Tests protect against regression
- **Tests as documentation**: Tests describe expected behavior

## Best Practices

### The TDD Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                     TDD CYCLE                                │
│                                                              │
│   ┌───────┐         ┌───────┐         ┌──────────┐         │
│   │  RED  │ ──────► │ GREEN │ ──────► │ REFACTOR │         │
│   └───────┘         └───────┘         └──────────┘         │
│       ▲                                     │               │
│       │                                     │               │
│       └─────────────────────────────────────┘               │
│                                                              │
│   RED:      Write a failing test                            │
│   GREEN:    Write minimal code to pass                      │
│   REFACTOR: Improve code without changing behavior          │
└─────────────────────────────────────────────────────────────┘
```

### Example: Building a Password Validator

```python
# Step 1: RED - Write failing test for first requirement
# test_password_validator.py

import pytest
from password_validator import PasswordValidator

class TestPasswordValidator:

    def test_password_too_short_is_invalid(self):
        validator = PasswordValidator()

        result = validator.validate("short")

        assert result.is_valid is False
        assert "at least 8 characters" in result.errors

# Run: pytest test_password_validator.py
# Result: FAIL (PasswordValidator doesn't exist)

# Step 2: GREEN - Minimal code to pass
# password_validator.py

from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)

class PasswordValidator:
    def validate(self, password: str) -> ValidationResult:
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

# Run: pytest test_password_validator.py
# Result: PASS

# Step 3: RED - Add next requirement
class TestPasswordValidator:

    def test_password_too_short_is_invalid(self):
        # ... existing test

    def test_password_without_uppercase_is_invalid(self):
        validator = PasswordValidator()

        result = validator.validate("lowercase123")

        assert result.is_valid is False
        assert "uppercase letter" in str(result.errors)

# Run: pytest - FAIL

# Step 4: GREEN - Add uppercase check
class PasswordValidator:
    def validate(self, password: str) -> ValidationResult:
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

# Run: pytest - PASS

# Step 5: Continue cycle for remaining requirements...

    def test_password_without_lowercase_is_invalid(self):
        validator = PasswordValidator()
        result = validator.validate("UPPERCASE123")
        assert result.is_valid is False

    def test_password_without_digit_is_invalid(self):
        validator = PasswordValidator()
        result = validator.validate("NoDigitsHere")
        assert result.is_valid is False

    def test_valid_password_passes_all_checks(self):
        validator = PasswordValidator()
        result = validator.validate("ValidPass123")
        assert result.is_valid is True
        assert len(result.errors) == 0

# Step 6: REFACTOR - Improve code structure
class PasswordValidator:
    MIN_LENGTH = 8

    def __init__(self):
        self.rules = [
            (self._check_length, f"Password must be at least {self.MIN_LENGTH} characters"),
            (self._check_uppercase, "Password must contain at least one uppercase letter"),
            (self._check_lowercase, "Password must contain at least one lowercase letter"),
            (self._check_digit, "Password must contain at least one digit"),
        ]

    def validate(self, password: str) -> ValidationResult:
        errors = [
            message for check, message in self.rules
            if not check(password)
        ]
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _check_length(self, password: str) -> bool:
        return len(password) >= self.MIN_LENGTH

    def _check_uppercase(self, password: str) -> bool:
        return any(c.isupper() for c in password)

    def _check_lowercase(self, password: str) -> bool:
        return any(c.islower() for c in password)

    def _check_digit(self, password: str) -> bool:
        return any(c.isdigit() for c in password)

# Run: pytest - Still PASS (refactoring didn't break anything)
```

### TDD for API Design

```python
# TDD helps design clean APIs - tests define the interface

# Step 1: Write test describing desired API
class TestOrderService:

    def test_create_order_with_valid_items(self):
        # Arrange
        service = OrderService(
            inventory=FakeInventory({"SKU-001": 10}),
            payment=FakePaymentGateway()
        )

        # Act
        order = service.create_order(
            customer_id="cust-123",
            items=[
                OrderItem(sku="SKU-001", quantity=2, price=Decimal("25.00"))
            ]
        )

        # Assert
        assert order.id is not None
        assert order.status == OrderStatus.PENDING
        assert order.total == Decimal("50.00")

    def test_create_order_fails_when_insufficient_inventory(self):
        service = OrderService(
            inventory=FakeInventory({"SKU-001": 1}),
            payment=FakePaymentGateway()
        )

        with pytest.raises(InsufficientInventoryError):
            service.create_order(
                customer_id="cust-123",
                items=[OrderItem(sku="SKU-001", quantity=5, price=Decimal("25.00"))]
            )

# The test defines:
# - Constructor dependencies (inventory, payment)
# - Method signature (create_order)
# - Input format (OrderItem dataclass)
# - Output format (Order with id, status, total)
# - Error handling (InsufficientInventoryError)

# Step 2: Implement to satisfy tests
@dataclass
class OrderItem:
    sku: str
    quantity: int
    price: Decimal

@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem]
    status: OrderStatus
    total: Decimal

class OrderService:
    def __init__(self, inventory: InventoryService, payment: PaymentGateway):
        self.inventory = inventory
        self.payment = payment

    def create_order(self, customer_id: str, items: list[OrderItem]) -> Order:
        # Validate inventory
        for item in items:
            available = self.inventory.check_availability(item.sku)
            if available < item.quantity:
                raise InsufficientInventoryError(item.sku, item.quantity, available)

        # Calculate total
        total = sum(item.price * item.quantity for item in items)

        # Create order
        return Order(
            id=str(uuid4()),
            customer_id=customer_id,
            items=items,
            status=OrderStatus.PENDING,
            total=total
        )
```

### Bug Fix with TDD

```python
# Step 1: Reproduce bug with failing test
def test_discount_calculation_with_zero_quantity():
    """
    BUG: Division by zero when calculating per-item discount
    with zero quantity items in cart.
    Issue: #1234
    """
    calculator = DiscountCalculator()
    cart = Cart(items=[
        CartItem(sku="A", quantity=0, price=Decimal("10.00")),  # Zero quantity!
        CartItem(sku="B", quantity=2, price=Decimal("20.00")),
    ])

    # Should not raise ZeroDivisionError
    result = calculator.apply_percentage_discount(cart, Decimal("10"))

    assert result.total == Decimal("36.00")  # 10% off of 40

# Step 2: Run test - confirms bug
# ZeroDivisionError: division by zero

# Step 3: Fix the bug
class DiscountCalculator:
    def apply_percentage_discount(self, cart: Cart, percentage: Decimal) -> Cart:
        discount_rate = percentage / Decimal("100")
        new_items = []

        for item in cart.items:
            if item.quantity > 0:  # Fix: Skip zero quantity items
                discounted_price = item.price * (1 - discount_rate)
                new_items.append(CartItem(
                    sku=item.sku,
                    quantity=item.quantity,
                    price=discounted_price
                ))

        return Cart(items=new_items)

# Step 4: Run test - passes
# Step 5: Ensure existing tests still pass
```

### TypeScript TDD Example

```typescript
// Step 1: RED - Define expected behavior
// __tests__/emailService.test.ts
import { EmailService, EmailValidationError } from '../emailService';

describe('EmailService', () => {
  let service: EmailService;

  beforeEach(() => {
    service = new EmailService();
  });

  describe('validateEmail', () => {
    it('should accept valid email addresses', () => {
      expect(service.validateEmail('user@example.com')).toBe(true);
      expect(service.validateEmail('user.name@domain.co.uk')).toBe(true);
    });

    it('should reject email without @ symbol', () => {
      expect(() => service.validateEmail('userexample.com'))
        .toThrow(EmailValidationError);
    });

    it('should reject email without domain', () => {
      expect(() => service.validateEmail('user@'))
        .toThrow(EmailValidationError);
    });
  });

  describe('normalizeEmail', () => {
    it('should lowercase the email', () => {
      expect(service.normalizeEmail('User@Example.COM'))
        .toBe('user@example.com');
    });

    it('should trim whitespace', () => {
      expect(service.normalizeEmail('  user@example.com  '))
        .toBe('user@example.com');
    });
  });
});

// Step 2: GREEN - Implement to pass tests
// emailService.ts
export class EmailValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'EmailValidationError';
  }
}

export class EmailService {
  private readonly emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  validateEmail(email: string): boolean {
    if (!email.includes('@')) {
      throw new EmailValidationError('Email must contain @ symbol');
    }

    const [, domain] = email.split('@');
    if (!domain || domain.length === 0) {
      throw new EmailValidationError('Email must have a domain');
    }

    if (!this.emailRegex.test(email)) {
      throw new EmailValidationError('Invalid email format');
    }

    return true;
  }

  normalizeEmail(email: string): string {
    return email.trim().toLowerCase();
  }
}

// Step 3: REFACTOR - Improve without breaking tests
export class EmailService {
  private readonly emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  validateEmail(email: string): boolean {
    this.assertContainsAt(email);
    this.assertHasDomain(email);
    this.assertValidFormat(email);
    return true;
  }

  normalizeEmail(email: string): string {
    return email.trim().toLowerCase();
  }

  private assertContainsAt(email: string): void {
    if (!email.includes('@')) {
      throw new EmailValidationError('Email must contain @ symbol');
    }
  }

  private assertHasDomain(email: string): void {
    const domain = email.split('@')[1];
    if (!domain?.length) {
      throw new EmailValidationError('Email must have a domain');
    }
  }

  private assertValidFormat(email: string): void {
    if (!this.emailRegex.test(email)) {
      throw new EmailValidationError('Invalid email format');
    }
  }
}
```

### TDD Best Practices Summary

```markdown
## TDD Guidelines

### Before Writing Tests
1. Understand the requirement clearly
2. Break down into small, testable behaviors
3. Start with the simplest case

### Writing Tests
1. Test name describes the behavior
2. One assertion concept per test
3. Use Arrange-Act-Assert structure
4. Write the test you wish you had

### During GREEN Phase
1. Write minimal code to pass
2. It's OK if code is ugly initially
3. Don't optimize prematurely
4. Don't add code for future tests

### During REFACTOR Phase
1. Keep tests passing at all times
2. Small steps, run tests frequently
3. Remove duplication
4. Improve naming and structure
5. Extract methods/classes if needed

### Common Mistakes to Avoid
1. Writing multiple tests before implementation
2. Making tests pass with hardcoded values
3. Skipping the refactor step
4. Testing implementation details
5. Writing tests that are too large
```

## Anti-patterns

- **Test after**: Writing tests after code defeats TDD benefits
- **Big steps**: Writing too much test code before implementing
- **Skipping refactor**: Accumulating technical debt
- **Testing implementation**: Tests coupled to internal details
- **Gold plating**: Adding features not required by tests
- **Ignoring failures**: Commenting out failing tests

## References

- [Test-Driven Development by Example - Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [TDD Manifesto](https://tddmanifesto.com/)
- [Uncle Bob - The Three Laws of TDD](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
