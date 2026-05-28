# TDD Workflow Checklist

## Before Starting

- [ ] Understand the requirement completely
- [ ] Identify the smallest testable behavior
- [ ] Set up test file in correct location (`*.test.ts`)

---

## Red Phase (Write Failing Test)

- [ ] Write the test FIRST (before any implementation)
- [ ] Test describes the expected behavior clearly
- [ ] Test name reads like documentation
- [ ] Test uses Arrange-Act-Assert pattern
- [ ] Run test and confirm it FAILS (red)
- [ ] Failure message is clear and helpful

```typescript
// Example: Clear test structure
describe('calculateDiscount', () => {
  it('returns 10% discount for orders over $100', () => {
    // Arrange
    const orderTotal = 150;

    // Act
    const discount = calculateDiscount(orderTotal);

    // Assert
    expect(discount).toBe(15);
  });
});
```

---

## Green Phase (Make Test Pass)

- [ ] Write the MINIMUM code to make test pass
- [ ] Do not add extra functionality
- [ ] Do not optimize yet
- [ ] Run test and confirm it PASSES (green)
- [ ] All previous tests still pass

```typescript
// Example: Minimum implementation
function calculateDiscount(total: number): number {
  if (total > 100) {
    return total * 0.1;
  }
  return 0;
}
```

---

## Refactor Phase (Clean Up)

- [ ] Tests still pass after each change
- [ ] Remove duplication
- [ ] Improve naming
- [ ] Simplify logic
- [ ] Extract if needed
- [ ] No new functionality added
- [ ] Run tests frequently

```typescript
// Example: Refactored with constants
const DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.1;

function calculateDiscount(total: number): number {
  const isEligible = total > DISCOUNT_THRESHOLD;
  return isEligible ? total * DISCOUNT_RATE : 0;
}
```

---

## Cycle Complete

- [ ] All tests pass
- [ ] Code is clean and readable
- [ ] No dead code
- [ ] Ready for next cycle

---

## TDD Principles

### The Three Laws

1. **Don't write production code until you have a failing test**
2. **Don't write more test than is sufficient to fail**
3. **Don't write more production code than is sufficient to pass**

### Small Steps

Break work into tiny increments:

```
1. Test: Empty cart has total of 0
2. Test: Cart with one item has correct total
3. Test: Cart with multiple items sums correctly
4. Test: Cart applies quantity discounts
5. Test: Cart handles invalid items gracefully
```

### When Stuck

- Make the test smaller
- Test a simpler case first
- Check if you're testing the right thing
- Step back and reconsider the design

---

## Common TDD Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Writing code first | No safety net | Always test first |
| Testing too much at once | Hard to debug failures | Smaller tests |
| Skipping refactor | Technical debt | Always clean up |
| Testing implementation | Brittle tests | Test behavior |
| Not running tests often | Late feedback | Run after every change |
| Ignoring failing tests | Broken code | Fix immediately |

---

## Test Quality Checklist

- [ ] Test name describes behavior, not implementation
- [ ] Test is independent (no shared state)
- [ ] Test is deterministic (same result every time)
- [ ] Test is fast (milliseconds, not seconds)
- [ ] Test has one logical assertion
- [ ] Test would fail if behavior changed
- [ ] Test would NOT fail if implementation changed

---

## Edge Cases to Consider

- Empty/null inputs
- Boundary values (0, 1, max)
- Invalid inputs
- Error conditions
- Concurrent access
- Large inputs
- Unicode/special characters
