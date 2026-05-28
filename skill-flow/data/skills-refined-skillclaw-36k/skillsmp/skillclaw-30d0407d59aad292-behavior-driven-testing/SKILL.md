---
name: behavior-driven-testing
description: Use this skill when writing tests to ensure they focus on behavior rather than implementation details.
---

# Skill body

## Core Principle

**Test behavior, not implementation.** Aim for 100% coverage through business behavior, not implementation details.

**Example:** Validation code in `payment-validator.ts` gets 100% coverage by testing `processPayment()` behavior, NOT by directly testing validator functions.

## Test Through Public API Only

Never test implementation details. Always test behavior through public APIs.

### Why This Matters:
- Tests remain valid when refactoring.
- Tests document intended behavior.
- Tests catch real bugs, not just implementation changes.

### Examples

#### ❌ **WRONG - Testing implementation:**
```typescript
// ❌ Testing HOW (implementation detail)
it('should call validateAmount', () => {
  const spy = jest.spyOn(validator, 'validateAmount');
  processPayment(payment);
  expect(spy).toHaveBeenCalled(); // Tests HOW, not WHAT
});

// ❌ Testing private methods
it('should validate CVV format', () => {
  const result = validator._validateCVV('123'); // Private method!
  expect(result).toBe(true);
});

// ❌ Testing internal state
it('should set isValidated flag', () => {
  processPayment(payment);
  expect(processor.isValidated).toBe(true); // Internal state
});
```

#### ✅ **CORRECT - Testing behavior through public API:**
```typescript
it('should reject negative amounts', () => {
  const payment = getMockPayment({ amount: -100 });
  const result = processPayment(payment);
  expect(result.success).toBe(false);
  expect(result.error).toContain('Amount must be positive');
});

it('should reject invalid CVV', () => {
  const payment = getMockPayment({ cvv: '12' }); // Only 2 digits
  const result = processPayment(payment);
  expect(result.success).toBe(false);
  expect(result.error).toContain('Invalid CVV');
});

it('should process valid payments', () => {
  const payment = getMockPayment({ amount: 100, cvv: '123' });
  const result = processPayment(payment);
  expect(result.success).toBe(true);
  expect(result.data.transactionId).toBeDefined();
});
```

## Coverage Through Behavior

Ensure validation code gets 100% coverage by testing the behavior it protects:

```typescript
// Tests covering validation WITHOUT testing validator directly
describe('processPayment', () => {
  it('should reject negative amounts', () => {
    const payment = getMockPayment({ amount: -100 });
    const result = processPayment(payment);
    expect(result.success).toBe(false);
    expect(result.error).toContain('Amount must be positive');
  });
});
```