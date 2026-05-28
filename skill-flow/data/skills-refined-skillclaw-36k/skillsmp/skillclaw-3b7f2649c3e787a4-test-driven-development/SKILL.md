---
name: test-driven-development
description: Use this skill when implementing any feature or bugfix, before writing implementation code.
---

# Test-Driven Development (TDD)

## Overview

Test-Driven Development (TDD) is a software development process where you write tests before writing the corresponding code. The cycle consists of writing a failing test, implementing the minimal code to pass the test, and then refactoring the code.

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

Implement fresh from tests. Period.

## Red-Green-Refactor Cycle

1. **RED - Write Failing Test**
   - Write one minimal test showing what should happen.
   - **Good Example:**
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
   - **Bad Example:**
     ```typescript
     test('retry works', async () => {
       const mock = jest.fn()
         .mockRejectedValueOnce(new Error())
         .mockRejectedValueOnce(new Error())
         .mockResolvedValueOnce('success');
       await retryOperation(mock);
     });
     ```

2. **GREEN - Write Minimal Code**
   - Write the minimum code necessary to make the test pass.
   - Avoid optimizations and edge cases at this stage.

3. **REFACTOR - Clean Up**
   - After achieving a passing test, improve the code quality.
   - Remove duplication, improve naming, and ensure all tests still pass after changes.

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

Thinking "skip TDD just this once"? Stop. That's rationalization. TDD is not just about testing; it's about design. Tests-first forces you to think about the interface before the implementation.