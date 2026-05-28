---
name: test-driven-development
description: Use this skill when implementing features or fixing bugs to enforce the RED-GREEN-REFACTOR cycle, ensuring tests are written before code.
---

# Test-Driven Development (TDD)

## Overview

Test-Driven Development (TDD) is a software development process that relies on writing tests before writing the corresponding code. The core principle is: **If you didn't watch the test fail, you don't know if it tests the right thing.** This process follows the RED-GREEN-REFACTOR cycle.

## The TDD Cycle

### 1. RED - Write a Failing Test
- Write a test that describes the expected behavior of the feature.
- Ensure the test fails for the right reason (the feature is not yet implemented).
- Example:
  ```typescript
  test('should calculate discount when order total exceeds threshold', () => {
      const result = calculateDiscount(150);
      expect(result).toBe(120); // Assuming a 20% discount
  });
  ```

### 2. GREEN - Make It Pass
- Write the minimum amount of code necessary to make the test pass.
- Avoid adding unnecessary features or optimizations at this stage.
- Example:
  ```typescript
  function calculateDiscount(total) {
      return total * 0.8; // 20% discount
  }
  ```

### 3. REFACTOR - Improve the Code
- Clean up the code while ensuring all tests still pass.
- Focus on removing duplication, improving naming, and simplifying logic.
- Example:
  ```typescript
  function calculateDiscount(total) {
      return total * (1 - 0.2); // Using a constant for discount
  }
  ```

## Key Principles

- **Fast**: Tests should run quickly (ideally under 100ms).
- **Independent**: Tests should not depend on each other.
- **Repeatable**: Tests should yield the same results every time.
- **Self-validating**: Tests should clearly indicate pass or fail.
- **Timely**: Tests should be written before the code they validate.

## Common Anti-Patterns

- **Test-After**: Writing production code before any tests exist.
- **Skipping Tests for Simple Code**: Assuming simple code doesn't need tests.
- **Over-Mocking**: Using mocks excessively instead of testing real behavior.

## Commit Strategy

- Commit after each GREEN phase (when a test passes).
- Commit after each REFACTOR phase (when code is improved).

## When to Use This Skill

- When starting any new feature.
- When fixing bugs (write a test that reproduces the bug first).
- When refactoring existing code (ensure tests exist first).
- For any production code changes that could break existing functionality.

## Summary

The TDD process is a disciplined approach to software development that emphasizes writing tests first, ensuring that code is only written to pass those tests, and refactoring code while maintaining test coverage. This approach leads to better-designed, more reliable software.

**Remember:** If you wrote production code without a failing test first, you violated TDD. Delete the code and start over with a test.