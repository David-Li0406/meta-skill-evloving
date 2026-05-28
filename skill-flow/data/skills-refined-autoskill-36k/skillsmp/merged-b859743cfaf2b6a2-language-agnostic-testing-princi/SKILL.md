---
name: language-agnostic-testing-principles
description: Use this skill when writing tests, designing test strategies, or reviewing test quality, covering TDD, test quality, coverage standards, and test design patterns.
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
- Test multiple components together.
- May include database, file system, or APIs.
- Slower than unit tests.
- Verify contracts between modules.
- Smaller portion of test suite.

### End-to-End (E2E) Tests

**Purpose**: Test complete workflows from the user perspective.

**Characteristics**:
- Test entire application stack.
- Simulate real user interactions.
- Slowest test type.
- Fewest in number.
- Highest confidence level.

### Test Pyramid

Follow the test pyramid structure:
```
    /\    ← Few E2E Tests (High confidence, slow)
   /  \
  /    \  ← Some Integration Tests (Medium confidence, medium speed)
 /      \
/________\ ← Many Unit Tests (Fast, foundational)
```

## Test Design Principles

### AAA Pattern (Arrange-Act-Assert)

Structure every test in three clear phases:

```
// Arrange: Setup test data and conditions
user = createTestUser()
validator = createValidator()

// Act: Execute the code under test
result = validator.validate(user)

// Assert: Verify expected outcome
assert(result.isValid == true)
```

### One Assertion Per Concept

- Test one behavior per test case.
- Multiple assertions OK if testing a single concept.
- Split unrelated assertions into separate tests.

### Descriptive Test Names

Test names should clearly describe:
- What is being tested.
- Under what conditions.
- What the expected outcome is.

**Recommended format**: `"should [expected behavior] when [condition]"`.

## Test Independence

### Isolation Requirements

- **No shared state**: Each test creates its own data.
- **No execution order dependency**: Tests pass in any order.
- **Clean up after tests**: Reset state, close connections.
- **Avoid global variables**: Use local test data.

### Setup and Teardown

- Use setup hooks to prepare the test environment.
- Use teardown hooks to clean up resources.
- Keep setup minimal and focused.
- Ensure teardown runs even if the test fails.

## Mocking and Test Doubles

### When to Use Mocks

- **Mock external dependencies**: APIs, databases, file systems.
- **Mock slow operations**: Network calls, heavy computations.
- **Mock unpredictable behavior**: Random values, current time.
- **Mock unavailable services**: Third-party services.

### Mocking Principles

- Mock at boundaries, not internally.
- Keep mocks simple and focused.
- Verify mock expectations when relevant.

### Types of Test Doubles

- **Stub**: Returns predetermined values.
- **Mock**: Verifies it was called correctly.
- **Spy**: Records information about calls.
- **Fake**: Simplified working implementation.
- **Dummy**: Passed but never used.

## Test Quality Practices

### Keep Tests Active

- **Fix or delete failing tests**: Resolve failures immediately.
- **Remove commented-out tests**: Fix them or delete entirely.
- **Keep tests running**: Broken tests lose value quickly.
- **Maintain test suite**: Refactor tests as needed.

### Test Code Quality

- Apply the same standards as production code.
- Use descriptive variable names.
- Extract test helpers to reduce duplication.
- Keep tests readable and maintainable.

## What to Test

### Focus on Behavior

**Test observable behavior, not implementation**.

### Test Public APIs

- Test through public interfaces.
- Avoid testing private methods directly.
- Test return values, outputs, exceptions.

### Test Edge Cases

Always test:
- **Boundary conditions**: Min/max values, empty collections.
- **Error cases**: Invalid input, null values, missing data.
- **Edge cases**: Special characters, extreme values.

## Verification Requirements

### Before Commit

- ✓ All tests pass.
- ✓ No tests skipped or commented.
- ✓ No debug code left in tests.
- ✓ Test coverage meets standards.
- ✓ Tests run in reasonable time.

### Zero Tolerance Policy

- **Zero failing tests**: Fix immediately.
- **Zero skipped tests**: Delete or fix.
- **Zero flaky tests**: Make deterministic.
- **Zero slow tests**: Optimize or split.

## Test Organization

### File Structure

- **Mirror production structure**: Tests follow code organization.
- **Clear naming conventions**: Follow project's test file patterns.
- **Logical grouping**: Group related tests together.
- **Separate test types**: Unit, integration, e2e in separate directories.

### Test Suite Organization

```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # Integration tests
├── e2e/            # End-to-end tests
├── fixtures/       # Test data and fixtures
└── helpers/        # Shared test utilities
```

## Performance Considerations

### Test Speed

- **Unit tests**: < 100ms each.
- **Integration tests**: < 1s each.
- **Full suite**: Should run frequently (< 10 minutes).

### Optimization Strategies

- Run tests in parallel when possible.
- Use in-memory databases for tests.
- Mock expensive operations.
- Split slow test suites.

## Continuous Integration

### CI/CD Requirements

- Run full test suite on every commit.
- Block merges if tests fail.
- Run tests in isolated environments.

### Test Reports

- Generate coverage reports.
- Track test execution time.
- Identify flaky tests.

## Common Anti-Patterns to Avoid

### Test Smells

- ✗ Tests that test nothing (always pass).
- ✗ Tests that depend on execution order.
- ✗ Tests that depend on external state.
- ✗ Tests with complex logic (tests shouldn't need tests).
- ✗ Excessive mocking (mocking everything).

### Flaky Tests

Eliminate tests that fail intermittently:
- Remove timing dependencies.
- Avoid random data in tests.
- Ensure proper cleanup.

## Regression Testing

### Prevent Regressions

- Add test for every bug fix.
- Maintain comprehensive test suite.
- Run full suite regularly.

### Legacy Code

- Add characterization tests before refactoring.
- Test existing behavior first.
- Gradually improve coverage.

## Testing Best Practices by Language Paradigm

### Type System Utilization

**For languages with static type systems**:
- Leverage compile-time verification for correctness.

**For languages with dynamic typing**:
- Add comprehensive runtime validation tests.

### Programming Paradigm Considerations

**Functional approach**:
- Test pure functions thoroughly.

**Object-oriented approach**:
- Test behavior through public interfaces.

## Documentation and Communication

### Tests as Documentation

- Tests document expected behavior.
- Use clear, descriptive test names.

### Test Failure Messages

- Provide clear, actionable error messages.

## Continuous Improvement

### Review and Refactor Tests

- Refactor tests as you refactor code.
- Remove obsolete tests.
- Improve test clarity.

### Learn from Failures

- Analyze test failures thoroughly.
- Add tests for discovered edge cases.