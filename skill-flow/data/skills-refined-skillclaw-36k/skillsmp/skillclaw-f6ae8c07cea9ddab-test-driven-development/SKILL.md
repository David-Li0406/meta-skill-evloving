---
name: test-driven-development
description: Use this skill when implementing any feature or bugfix, before writing implementation code. Enforces a strict test-first discipline with the RED-GREEN-REFACTOR cycle.
---

# Test-Driven Development (TDD)

## Overview

Test-Driven Development (TDD) is a software development process that relies on writing tests before writing the corresponding code. The core principle is that if you didn't watch the test fail, you don't know if it tests the right thing.

## The RED-GREEN-REFACTOR Cycle

### 1. RED - Write a Failing Test First
- Write the smallest test that fails for the right reason.
- The test should fail because the feature doesn't exist yet.
- Run the test and verify it fails.

### 2. GREEN - Make It Pass (Minimum Code)
- Write the minimum code necessary to make the test pass.
- Avoid writing more than necessary; no optimizations or refactoring at this stage.

### 3. REFACTOR - Improve the Code
- Clean up the code, remove duplication, improve naming, and extract methods/functions.
- Ensure all tests still pass after refactoring.

## Forbidden Rationalizations

If you catch yourself thinking any of the following, STOP:
- "This is just a simple function" → WRONG. Simple functions need tests.
- "I'll write tests after" → WRONG. That's not TDD.
- "Let me just get it working first" → WRONG. Tests first.
- "This doesn't need a test" → WRONG. Everything needs tests.
- "I'll test it manually" → WRONG. Write automated tests.
- "The test is obvious" → WRONG. Write it anyway.

## Test Quality Guidelines

### Good Tests Are:
- **Fast** - Tests should run in milliseconds.
- **Isolated** - No dependencies between tests.
- **Repeatable** - Same result every time.
- **Self-validating** - Pass or fail, no interpretation.
- **Timely** - Written before the code.

### Test Structure (Arrange-Act-Assert):
```javascript
// Arrange - Set up the test conditions
const input = createTestInput();

// Act - Execute the code under test
const result = functionUnderTest(input);

// Assert - Verify the expected outcome
expect(result).toBe(expectedValue);
```

## When to Use This Skill

- Starting any new feature.
- Fixing any bug (write a test that reproduces the bug first).
- Refactoring existing code (ensure tests exist first).
- Any code change that could break existing functionality.

## Exceptions
- Throwaway prototypes.
- Generated code.
- Configuration files.

## YAGNI (You Aren't Gonna Need It)
Don't write code you don't need yet:
- No speculative features.
- No "just in case" abstractions.
- No premature optimization.
- Build what's needed now, nothing more.

## DRY (Don't Repeat Yourself)
But only during the REFACTOR phase.