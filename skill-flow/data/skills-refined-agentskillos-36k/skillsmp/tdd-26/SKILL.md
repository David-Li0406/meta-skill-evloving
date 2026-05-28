---
name: tdd
description: Test-Driven Development workflow with RED-GREEN-REFACTOR cycle
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## What I Do

- Guide you through the RED-GREEN-REFACTOR cycle
- Write failing tests first, then implementation
- Ensure tests are meaningful and not just passing
- Prevent common TDD anti-patterns

## When to Use Me

Use this skill when:
- Implementing new features
- Fixing bugs (write a failing test that reproduces the bug first)
- Refactoring existing code (ensure tests exist first)

## The TDD Cycle

### 1. RED - Write a Failing Test

```
1. Write a test for the NEXT small piece of functionality
2. Run the test - it MUST fail
3. If it passes, either:
   - The functionality already exists, or
   - The test is wrong
```

**The test should:**
- Test ONE thing
- Have a descriptive name explaining the behavior
- Follow Arrange-Act-Assert pattern

### 2. GREEN - Make It Pass

```
1. Write the MINIMUM code to make the test pass
2. Don't worry about elegance yet
3. Hardcoding is acceptable temporarily
4. Run the test - it MUST pass
```

**Rules:**
- Only write code that makes a failing test pass
- Don't add functionality without a test
- Keep changes small

### 3. REFACTOR - Clean Up

```
1. Improve code quality while keeping tests green
2. Remove duplication
3. Improve naming
4. Extract methods/functions
5. Run tests after EVERY change
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Writing tests after code | Tests validate implementation, not behavior | Always write test first |
| Testing implementation details | Brittle tests that break on refactor | Test public behavior only |
| Large test steps | Hard to identify what broke | Smaller increments |
| Skipping refactor phase | Technical debt accumulates | Always refactor after green |
| Testing trivial code | Wasted effort | Focus on logic and edge cases |

## Test Structure

```
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange - set up test data
      // Act - call the method
      // Assert - verify the result
    });
  });
});
```

## Commit Rhythm

```
1. RED: Don't commit (test is failing)
2. GREEN: Commit with "test: add test for X"
3. REFACTOR: Commit with "refactor: improve X"
```
