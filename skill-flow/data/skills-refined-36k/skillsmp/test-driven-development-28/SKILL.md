---
name: Test-Driven Development
description: Enforce RED-GREEN-REFACTOR cycle for reliable, maintainable code
version: 1.0.0
source: Adapted from obra/superpowers
---

# Test-Driven Development (TDD)

## The Fundamental Rule

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

This is non-negotiable. Code written before tests must be deleted and rewritten with tests first.

## Why TDD Matters

Testing after implementation provides **false confidence**:
- Tests pass immediately (proves nothing)
- No verification that tests catch regressions
- Untested edge cases slip through

TDD ensures every line of production code is **proven necessary** by a failing test.

## The RED-GREEN-REFACTOR Cycle

### 1. RED - Write a Failing Test
```typescript
// Write the test FIRST
describe('calculateTotal', () => {
  it('should sum items with tax', () => {
    const items = [{ price: 100 }, { price: 50 }];
    const result = calculateTotal(items, 0.08);
    expect(result).toBe(162); // 150 + 12 tax
  });
});
```

Run the test. It MUST fail. If it passes, you're testing existing code (wrong).

### 2. Verify RED
Confirm failure is for the **right reason**:
- ✅ "calculateTotal is not defined" - Correct, function doesn't exist
- ❌ "SyntaxError in test file" - Fix test, not production code

### 3. GREEN - Minimal Implementation
Write the **simplest code** that makes the test pass:
```typescript
function calculateTotal(items: Item[], taxRate: number): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal + (subtotal * taxRate);
}
```

### 4. Verify GREEN
- All tests pass
- No regressions introduced
- Coverage increased

### 5. REFACTOR
Improve code quality while keeping tests green:
- Extract functions
- Rename for clarity
- Remove duplication
- Improve performance

## Common Rationalizations (Reject All)

| Excuse | Reality |
|--------|---------|
| "I'll test after" | Tests passing immediately prove nothing |
| "Already manually tested" | Manual testing isn't systematic or repeatable |
| "Deleting work is wasteful" | Sunk cost fallacy; unverified code is debt |
| "Too simple to test" | Simple code breaks too; testing takes seconds |
| "Keep existing as reference" | You'll adapt it; that's testing after |

## Red Flags - Stop Immediately

- Writing code before tests
- Tests passing on first run
- Any "just this once" rationalization
- Skipping the verify steps

## FrankX Application

### For Next.js Components
```typescript
// 1. RED - Write test first
describe('EmailSignup', () => {
  it('should show error for invalid email', async () => {
    render(<EmailSignup />);
    await userEvent.type(screen.getByRole('textbox'), 'invalid');
    await userEvent.click(screen.getByRole('button'));
    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });
});

// 2. GREEN - Implement component
// 3. REFACTOR - Clean up
```

### For API Routes
```typescript
// 1. RED
describe('POST /api/subscribe', () => {
  it('should return 400 for invalid email', async () => {
    const response = await POST({ json: () => ({ email: 'bad' }) });
    expect(response.status).toBe(400);
  });
});

// 2. GREEN - Implement route
// 3. REFACTOR
```

## Test File Organization

```
project/
├── app/
│   └── api/
│       └── subscribe/
│           └── route.ts
├── tests/
│   ├── unit/           # Fast, isolated tests
│   │   └── api/
│   │       └── subscribe.test.ts
│   ├── integration/    # Cross-component tests
│   └── e2e/           # Playwright tests
│       └── subscribe.spec.ts
```

## Commands

```bash
# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- api/subscribe.test.ts

# Run with coverage
npm test -- --coverage
```

## When to Use This Skill

- Writing any new feature
- Fixing bugs (write failing test FIRST)
- Refactoring (ensure tests exist)
- Code reviews (verify TDD was followed)

## Related Skills

- `systematic-debugging` - When tests reveal bugs
- `webapp-testing` - For Playwright e2e tests
- `implementation-planning` - Plans include TDD steps
