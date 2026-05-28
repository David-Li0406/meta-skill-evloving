---
name: test-driven-development
description: Use when implementing any feature or bugfix before writing implementation code
---

# Test-Driven Development

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

## Red-Green-Refactor Cycle

### RED - Write Failing Test

Write ONE minimal test showing what should happen.

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

**Verify it fails correctly:**
- Run the test
- Confirm it fails for the RIGHT reason
- If it passes → your test is wrong

### GREEN - Minimal Code

Write the MINIMUM code to make the test pass.

- Don't optimize
- Don't handle edge cases yet
- Don't make it pretty
- Just make it pass

### REFACTOR - Clean Up

Only after green:
- Improve code quality
- Remove duplication
- Improve naming
- Stay green (run tests after each change)

## Test Quality Checklist

- [ ] Test name describes the behavior
- [ ] Tests ONE thing
- [ ] Fails for the right reason
- [ ] Fast (< 100ms typically)
- [ ] No test interdependencies
- [ ] Readable without comments

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Test too big | Split into smaller tests |
| Testing implementation | Test behavior instead |
| Not watching it fail | Always run test before writing code |
| Skipping refactor | Technical debt accumulates |
| Multiple behaviors per test | One assertion focus per test |

## The Discipline

Thinking "skip TDD just this once"? Stop. That's rationalization.

TDD is not about testing. It's about design. Tests-first forces you to think about the interface before the implementation.
