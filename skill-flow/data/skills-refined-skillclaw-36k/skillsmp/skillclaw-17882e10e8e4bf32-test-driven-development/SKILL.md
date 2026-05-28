---
name: test-driven-development
description: Use this skill when you want to implement features or fix bugs using Test-Driven Development (TDD) principles, ensuring that tests are written before code and that the development follows the Red-Green-Refactor cycle.
---

# TDD (Test-Driven Development) Guide

## Overview

This skill provides a structured approach to implementing features and fixing bugs using Test-Driven Development (TDD). It emphasizes writing tests before code and following a systematic cycle of Red, Green, and Refactor.

## Basic Workflow

1. **Red**: Write a failing test for the desired functionality.
2. **Red Confirmation**: Ensure the test fails for the expected reason.
3. **Green**: Write the minimum code necessary to pass the test.
4. **Green Confirmation**: Verify that all tests pass.
5. **Refactor**: Improve the code structure while keeping all tests passing.
6. Repeat the cycle for each new behavior.

## Principles

- **Test First**: Always write tests before implementing functionality.
- **Small Steps**: Make incremental changes and test frequently.
- **Continuous Feedback**: Run tests regularly to catch issues early.

## TDD Cycle Steps

### 1. Red (Write a Failing Test)

- Define the expected behavior and write a test case that will fail.
- Example:
  ```typescript
  test("adds two numbers", () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5);
  });
  ```

### 2. Green (Make the Test Pass)

- Implement the simplest code necessary to pass the test.
- Example:
  ```typescript
  class Calculator {
    add(a: number, b: number): number {
      return a + b; // Simple implementation
    }
  }
  ```

### 3. Refactor (Improve the Code)

- Clean up the code while ensuring all tests still pass.
- Focus on eliminating duplication, improving naming, and enhancing readability.

## Best Practices

- Write clear and descriptive test names.
- Keep tests focused on a single behavior.
- Avoid premature optimization; implement the simplest solution that works.

## Verification Checklist

- Ensure a failing test is written before any implementation.
- Confirm that the test fails for the expected reason.
- Verify that all tests pass after implementing the minimum code.
- Maintain all tests passing after refactoring.

## Common Pitfalls

- Implementing code without a failing test.
- Writing overly broad tests that cover too much functionality.
- Skipping the refactor step, leading to technical debt.

## Conclusion

Use this skill to guide your development process with TDD, ensuring that you maintain high code quality and responsiveness to changes in requirements.