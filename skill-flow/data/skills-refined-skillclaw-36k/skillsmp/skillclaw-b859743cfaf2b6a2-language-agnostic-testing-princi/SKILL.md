---
name: language-agnostic-testing-principles
description: Use this skill when writing tests, designing test strategies, or reviewing test quality to ensure effective and reliable testing practices.
---

# Language-Agnostic Testing Principles

## Core Testing Philosophy

1. **Tests are First-Class Code**: Maintain test quality equal to production code.
2. **Fast Feedback**: Tests should run quickly and provide immediate feedback.
3. **Reliability**: Tests should be deterministic and reproducible.
4. **Independence**: Each test should run in isolation.

## Test-Driven Development (TDD)

### The RED-GREEN-REFACTOR Cycle

**Always follow this cycle:**

1. **RED**: Write a failing test first.
   - Write the test before implementation.
   - Ensure the test fails for the right reason.
   - Verify the test can actually fail.

2. **GREEN**: Write minimal code to pass.
   - Implement just enough to make the test pass.
   - Don't optimize prematurely.
   - Focus on making it work.

3. **REFACTOR**: Improve code structure.
   - Clean up implementation.
   - Eliminate duplication.
   - Improve naming and clarity.
   - Keep all tests passing.

4. **VERIFY**: Ensure all tests still pass.
   - Run the full test suite.
   - Check for regressions.
   - Validate refactoring didn't break anything.

### TDD Benefits

- Better design through testability requirements.
- Comprehensive test coverage by default.
- Living documentation of expected behavior.
- Confidence to refactor.

## Quality Requirements

### Coverage Standards

- **Minimum 80% code coverage** for production code.
- Prioritize critical paths and business logic.
- Don't sacrifice quality for coverage percentage.
- Use coverage as a guide, not a goal.

### Test Characteristics

All tests must be:

- **Independent**: No dependencies between tests.
- **Reproducible**: Same input always produces the same output.
- **Fast**: Complete test suite runs in a reasonable time.
- **Self-checking**: Clear pass/fail without manual verification.
- **Timely**: Written close to the code they test.

## Test Types

### Unit Tests

**Purpose**: Test individual components in isolation.

**Characteristics**:
- Test single function, method, or class.
- Fast execution (milliseconds).
- No external dependencies.
- Mock external services.
- Majority of your test suite.

### Integration Tests

**Purpose**: Test interactions between components.

**Characteristics**:
- Validate the behavior of multiple components working together.
- Ensure data flows correctly between modules.
- Typically slower than unit tests due to external dependencies.