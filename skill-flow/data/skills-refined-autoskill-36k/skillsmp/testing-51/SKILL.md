---
name: testing
description:
  Apply test-driven development and testing best practices. Use this skill when writing tests,
  implementing TDD workflows, improving test coverage, or debugging failing tests. Covers unit,
  integration, and end-to-end testing patterns across languages.
---

# Testing Best Practices

This skill provides guidance for writing effective tests and following test-driven development (TDD)
practices.

## When This Skill Applies

- Writing new tests for existing code
- Implementing features using TDD
- Improving test coverage
- Debugging or fixing failing tests
- Setting up testing infrastructure

## Test-Driven Development (TDD)

Follow the Red-Green-Refactor cycle:

1. **Red**: Write a failing test that defines expected behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Clean up the code while keeping tests green

### TDD Benefits

- Forces clear thinking about requirements before implementation
- Produces testable, modular code by design
- Creates living documentation of expected behavior
- Catches regressions immediately

## Test Structure

Use the **Arrange-Act-Assert** (AAA) pattern:

```
// Arrange: Set up test data and dependencies
// Act: Execute the code under test
// Assert: Verify the expected outcome
```

### Naming Conventions

Test names should describe the scenario and expected outcome:

- `test_user_login_with_valid_credentials_returns_token`
- `should throw error when email is invalid`
- `it("returns empty array when no items match filter")`

## Testing Pyramid

Balance your test suite:

1. **Unit Tests** (70%): Fast, isolated, test single functions/methods
2. **Integration Tests** (20%): Test component interactions, database, APIs
3. **E2E Tests** (10%): Test complete user workflows, slowest but highest confidence

## Best Practices

### Do

- Test behavior, not implementation details
- Keep tests independent—no shared mutable state
- Use descriptive assertions with clear failure messages
- Mock external dependencies (APIs, databases, file systems)
- Test edge cases: null, empty, boundary values, errors

### Don't

- Test private methods directly
- Write tests that depend on execution order
- Use production data in tests
- Ignore flaky tests—fix or remove them
- Over-mock to the point tests don't verify real behavior

## Language-Specific Patterns

### JavaScript/TypeScript

- Use Jest, Vitest, or Mocha for unit tests
- Use Testing Library for component tests
- Use Playwright or Cypress for E2E
- Mock with `jest.mock()` or `vi.mock()`

### Python

- Use pytest with fixtures for setup/teardown
- Use `unittest.mock` or `pytest-mock` for mocking
- Use `pytest.mark.parametrize` for data-driven tests
- Use `pytest-cov` for coverage reports

### Go

- Use table-driven tests with `t.Run()`
- Use `testify` for assertions and mocks
- Use `httptest` for HTTP handler tests
- Run with `-race` flag to detect race conditions

### Rust

- Use `#[cfg(test)]` module for unit tests
- Use `#[should_panic]` for expected failures
- Use `mockall` crate for mocking traits
- Integration tests go in `tests/` directory

## Coverage Guidelines

- Aim for meaningful coverage, not 100%
- Focus on critical paths and complex logic
- Exclude generated code and configuration
- Use coverage to find untested code, not as a quality metric
