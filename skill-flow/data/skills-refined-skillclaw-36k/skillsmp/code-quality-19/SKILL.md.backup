---
name: code-quality
description: Use when refactoring functions, extracting helpers, splitting large files, improving naming conventions, or reducing complexity. Use when functions exceed 30 lines, have too many parameters, or contain magic numbers. NOT for React/backend/database-specific patterns.
---

# Code Quality

## Overview

Clean code reveals intent and minimizes complexity. Every function should do one thing, have a clear name, and fit on one screen.

## When to Use

- Writing any new function or module
- Reviewing code for clarity
- Refactoring messy code
- Under time pressure (especially then)

**When NOT to use:** Quick prototypes explicitly marked as throwaway (rare).

## The Iron Rules

### 1. Function Length: Max 30 Lines

Functions over 30 lines are doing too much. Extract helpers.

**Exception:** Orchestration functions (calling other functions, minimal logic) may reach 50 lines. If you have conditionals or loops, max is 30.

**Cyclomatic Complexity:** Max 10 branches per function. Count: `if`, `else`, `case`, `&&`, `||`, `?:`, `catch`.

```typescript
// ❌ BAD: 100+ line processOrder doing everything
async function processOrder(order: Order) {
  // validation...
  // pricing...
  // inventory...
  // payment...
  // email...
  // analytics...
}

// ✅ GOOD: Orchestrator with extracted concerns
async function processOrder(order: Order) {
  const validation = validateOrder(order);
  if (!validation.valid) return failure(validation.error);

  const pricing = calculateOrderTotal(order);
  const reservation = await reserveInventory(order);

  const payment = await processPayment(order, pricing.total);
  if (!payment.success) {
    await releaseInventory(reservation);
    return failure(payment.error);
  }

  await sendConfirmationEmail(order, pricing);
  await recordAnalytics(order, pricing);

  return success(order.id, pricing.total);
}
```

### 2. No Magic Numbers

Every number with meaning needs a name.

```typescript
// ❌ BAD: What do these numbers mean?
if (totalItems >= 10) {
  total = total * 0.90;
}
if (password.length < 8) { }

// ✅ GOOD: Self-documenting
const BULK_DISCOUNT_THRESHOLD = 10;
const BULK_DISCOUNT_RATE = 0.10;
const MIN_PASSWORD_LENGTH = 8;

if (totalItems >= BULK_DISCOUNT_THRESHOLD) {
  total = total * (1 - BULK_DISCOUNT_RATE);
}
if (password.length < MIN_PASSWORD_LENGTH) { }
```

### 3. DRY: Extract Repeated Logic

If you copy-paste, extract.

```typescript
// ❌ BAD: Rollback logic repeated 5 times
if (!paymentInfo) {
  for (const item of order.items) {
    inventoryDb[item.productId] += item.quantity;
  }
  delete reservedInventory[order.id];
  return { success: false, error: 'Payment required' };
}
// ...same rollback code repeated 4 more times...

// ✅ GOOD: Extracted once
function rollbackInventory(orderId: string, items: OrderItem[]) {
  for (const item of items) {
    inventoryDb[item.productId] += item.quantity;
  }
  delete reservedInventory[orderId];
}

// Then use: rollbackInventory(order.id, order.items);
```

### 4. Single Responsibility

One function = one reason to change.

| Bad | Good |
|-----|------|
| `validateAndProcessOrder()` | `validateOrder()` + `processOrder()` |
| `fetchDataAndRender()` | `fetchData()` + `renderData()` |
| `parseAndValidateAndSave()` | `parse()` + `validate()` + `save()` |

### 5. Naming Conventions

| Type | Convention | Examples |
|------|------------|----------|
| Functions | camelCase, verb-first | `validateEmail()`, `calculateTotal()` |
| Booleans | `is`, `has`, `should`, `can` | `isValid`, `hasPermission`, `shouldRetry` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT_MS` |
| Classes/Types | PascalCase | `OrderProcessor`, `ValidationResult` |

### 6. Comments: WHY, Not WHAT

```typescript
// ❌ BAD: Describes what code does (obvious)
// Check if user is admin
if (user.role === 'admin') { }

// ✅ GOOD: Explains why (not obvious)
// Admins bypass rate limiting per security policy SEC-2024-001
if (user.role === 'admin') { }
```

## Automated Enforcement

### ESLint Configuration (Flat Config - v9+)

ESLint 9+ uses flat config (`eslint.config.js`). Enforce code quality automatically:

```javascript
// eslint.config.js (ESLint v9+ flat config)
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      // Max function length
      'max-lines-per-function': ['error', {
        max: 30,
        skipBlankLines: true,
        skipComments: true,
      }],

      // Cyclomatic complexity
      'complexity': ['error', { max: 10 }],

      // Max file length
      'max-lines': ['error', {
        max: 300,
        skipBlankLines: true,
        skipComments: true,
      }],

      // Max function params
      'max-params': ['error', 3],

      // Max nested callbacks
      'max-nested-callbacks': ['error', 2],

      // No magic numbers
      'no-magic-numbers': ['error', {
        ignore: [0, 1, -1],
        ignoreArrayIndexes: true,
      }],
    },
  },
  {
    // Ignore patterns (replaces .eslintignore)
    ignores: ['node_modules/', 'dist/', '*.config.js'],
  }
);
```

**Legacy config?** ESLint 9+ still supports `.eslintrc.js` via `ESLINT_USE_FLAT_CONFIG=false`, but flat config is the future.

### TypeScript-Specific Patterns

```typescript
// ✅ GOOD: Type-safe options object (not 5 params)
interface CreateUserOptions {
  email: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
  sendWelcomeEmail?: boolean;
}

function createUser(options: CreateUserOptions): User {
  // Single param, clear structure
}

// ✅ GOOD: Discriminated union for type-safe control flow
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function processOrder(order: Order): Result<OrderConfirmation> {
  if (!isValid(order)) {
    return { success: false, error: 'Invalid order' };
  }

  const confirmation = executeOrder(order);
  return { success: true, data: confirmation };
}

// ✅ GOOD: Branded types for type safety
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function getUser(id: UserId): User { /* ... */ }

// Won't compile - prevents mixing up IDs
const orderId: OrderId = '123' as OrderId;
getUser(orderId); // Type error!
```

## Testing Strategy

```typescript
// Test function length and complexity
describe('Code Quality', () => {
  it('functions stay under 30 lines', () => {
    const functionSource = processOrder.toString();
    const lines = functionSource.split('\n').filter(l => l.trim()).length;
    expect(lines).toBeLessThanOrEqual(30);
  });

  it('maintains low cyclomatic complexity', () => {
    // Use eslint-plugin-complexity or similar
    const complexity = calculateComplexity(processOrder);
    expect(complexity).toBeLessThanOrEqual(10);
  });
});

// Test extracted helpers
describe('Helper Functions', () => {
  it('validateOrder handles invalid input', () => {
    const result = validateOrder({ items: [] });
    expect(result.valid).toBe(false);
  });

  it('calculateOrderTotal sums items correctly', () => {
    const total = calculateOrderTotal(mockOrder);
    expect(total).toBe(99.99);
  });
});
```

## Quick Reference

| Smell | Fix | ESLint Rule |
|-------|-----|-------------|
| Function > 30 lines | Extract helpers | `max-lines-per-function` |
| Cyclomatic complexity > 10 | Extract conditionals | `complexity` |
| Repeated code block | Extract function | Manual review |
| Magic number | Named constant | `no-magic-numbers` |
| `validateAndProcess()` | Split into two functions | Manual review |
| Nested callbacks > 2 levels | Extract or use async/await | `max-nested-callbacks` |
| Parameter list > 3 | Use options object | `max-params` |

## Red Flags - STOP and Refactor

These thoughts mean you're about to write bad code:

| Thought | Reality |
|---------|---------|
| "It's faster to write it all in one function" | It's faster to read small functions. Write for the reader. |
| "We'll refactor later" | Later never comes. Write it right the first time. |
| "It's just prototype code" | Prototypes become production. No excuse. |
| "The deadline is tight" | Bad code slows you down MORE. Clean code is faster. |
| "I'll add helpers if it gets complex" | It's already complex. Extract NOW. |
| "This is a special case" | There are no special cases for quality. |
| "It's only 35 lines, close enough" | The limit exists for a reason. Extract a helper. |
| "The user specifically asked for one function" | Push back. Explain why splitting is better. |
| "I need all this context in one place" | That's what orchestrator functions are for. |

## Pressure Response

When someone says "just make it work fast":

1. **Small functions ARE faster** - easier to debug, test, modify
2. **Tech debt has interest** - every shortcut costs 10x later
3. **Extract as you go** - takes 30 seconds, saves hours

**Violating code quality under pressure is violating code quality.**

## References

- [ESLint Flat Config](https://eslint.org/docs/latest/use/configure/configuration-files-new) - ESLint 9+ configuration
- [ESLint Complexity Rule](https://eslint.org/docs/latest/rules/complexity) - Cyclomatic complexity enforcement
- [typescript-eslint](https://typescript-eslint.io/) - TypeScript ESLint integration
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/) - Advanced type patterns
- [Clean Code (Martin)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - Function length rationale

**Version Notes:**
- ESLint 9+: Flat config (`eslint.config.js`), replaces `.eslintrc.*`
- TypeScript 5+: Improved discriminated union narrowing, const type parameters
- typescript-eslint 8+: Native flat config support
- Cyclomatic complexity: Default threshold 20, recommended 10

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| God function | Untestable, unreadable | Max 30 lines, single responsibility |
| Copy-paste code | Bugs multiply | Extract shared logic |
| Cryptic names | Confusion | Descriptive, verb-first names |
| No constants | Magic numbers everywhere | SCREAMING_SNAKE_CASE for all config |
| No ESLint enforcement | Quality drifts over time | Add `complexity` and `max-lines-per-function` rules |
| 5+ function parameters | Hard to call, hard to test | Use options object pattern |
| Comments describe WHAT | Redundant, unmaintained | Comment WHY, not WHAT |
| Mixing ID types (string) | Runtime bugs | Use branded types for type safety |