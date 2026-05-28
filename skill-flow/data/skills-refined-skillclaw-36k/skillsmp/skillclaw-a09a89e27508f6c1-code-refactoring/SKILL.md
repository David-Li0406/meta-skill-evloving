---
name: code-refactoring
description: Use this skill when you need to improve code quality and maintainability without changing its behavior, such as cleaning up legacy code or simplifying complex structures.
---

# Code Refactoring

## Refactoring Principles

### When to Refactor
- Before adding new features (make change easy, then make easy change)
- After getting tests passing (red-green-refactor)
- When you see code smells
- During code review feedback

### When NOT to Refactor
- Without tests covering the code
- Under tight deadlines with no safety net
- Code that will be replaced soon
- When you don't understand what the code does

## Common Code Smells and Refactoring Patterns

| Smell | Refactoring |
|-------|-------------|
| Long Methods | Extract Method |
| Deeply Nested Conditionals | Decompose Conditional |
| Primitive Obsession | Introduce Value Object |
| Feature Envy | Move Method |

### Example Refactorings

#### Long Methods
**Before:**
```typescript
function processOrder(order: Order) {
  // 100 lines of validation, calculation, notification, logging...
}
```
**After:**
```typescript
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  saveOrder(order, total);
  notifyCustomer(order);
}
```

#### Deeply Nested Conditionals
**Before:**
```typescript
function getDiscount(user: User, order: Order) {
  if (user) {
    if (user.isPremium) {
      if (order.total > 100) {
        if (order.items.length > 5) {
          return 0.2;
        }
      }
    }
  }
  return 0;
}
```
**After:**
```typescript
function getDiscount(user: User, order: Order) {
  if (!user || !user.isPremium || order.total <= 100 || order.items.length <= 5) {
    return 0;
  }
  return 0.2;
}
```

#### Primitive Obsession
**Before:**
```typescript
function createUser(name: string, email: string, phone: string) {
  if (!email.includes('@')) throw new Error('Invalid email');
}
```
**After:**
```typescript
class Email {
  constructor(private value: string) {
    if (!value.includes('@')) throw new Error('Invalid email');
  }
}

function createUser(name: string, email: Email, phone: string) {
  // Email is already validated
}
```

## Safe Refactoring Cycle
1. Ensure tests pass (never refactor without tests)
2. Make one small change
3. Run tests (must stay green)
4. Commit (save progress)
5. Repeat

### Key Takeaways
- Refactoring is about improving code structure without changing behavior.
- Always have tests in place before refactoring.
- Make small, incremental changes to ensure safety and maintainability.