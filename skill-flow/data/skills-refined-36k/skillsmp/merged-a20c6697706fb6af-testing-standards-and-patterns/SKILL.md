---
name: testing-standards-and-patterns
description: Use this skill when you need guidance on testing methodologies, test organization, coverage requirements, and best practices for writing maintainable tests.
---

# Testing Standards and Patterns

This skill provides comprehensive guidance for implementing effective testing strategies that meet software development lifecycle (SDLC) requirements.

## Tooling

> **Available Tools**: If using Claude Code, the `pr-review-toolkit:pr-test-analyzer` agent reviews test coverage and identifies gaps. Use after creating PRs to ensure adequate test coverage.

## Test Organization

### Required Test Categories (MUST)

Projects MUST maintain these test categories:

| Category            | Location                 | Purpose                           |
| ------------------- | ------------------------ | --------------------------------- |
| Unit tests          | Alongside source code    | Test individual functions/methods |
| Integration tests   | Dedicated test directory | Test component interactions       |
| Documentation tests | Within doc comments      | Verify examples work              |
| End-to-end tests    | Dedicated e2e directory  | Test full system behavior         |

### Naming Convention (MUST)

Test files MUST be clearly identifiable by naming convention:

| Language   | Unit Tests               | Integration Tests       |
| ---------- | ------------------------ | ----------------------- |
| Rust       | `mod tests` in source    | `tests/` directory      |
| TypeScript | `*.test.ts`, `*.spec.ts` | `tests/integration/`    |
| Python     | `test_*.py`, `*_test.py` | `tests/integration/`    |
| Java       | `*Test.java`             | `*IntegrationTest.java` |
| Go         | `*_test.go`              | `*_integration_test.go` |

## Test Coverage

### Coverage Requirements

| Requirement          | Level                                |
| -------------------- | ------------------------------------ |
| New functionality    | MUST include tests                   |
| Bug fixes            | MUST include regression tests        |
| Coverage measurement | MUST be tracked                      |
| Minimum coverage     | SHOULD target 80%                    |
| Critical paths       | MUST have 95%+ coverage              |
| Coverage reports     | MUST be uploaded to tracking service |

### Regression Tests (MUST)

Bug fixes MUST include regression tests that:

1. Fail before the fix is applied
2. Pass after the fix is applied
3. Document the bug being fixed

### Critical Path Coverage (MUST)

Critical paths requiring 95%+ coverage include:

- Authentication and authorization
- Data validation and sanitization
- Financial calculations
- Security-sensitive operations
- Data persistence operations

## Test Execution

### Pre-Merge Requirements (MUST)

1. All tests MUST pass before code can be merged
2. Tests MUST be deterministic (no flaky tests)
3. Tests MUST be isolated (no shared state between tests)
4. Tests MUST run on all supported platforms in CI

### Performance Guidelines (SHOULD)

| Test Type         | Target Duration   |
| ----------------- | ----------------- |
| Unit tests        | < 1 second each   |
| Integration tests | < 30 seconds each |
| Full test suite   | < 10 minutes      |

### Flaky Test Policy

Flaky tests MUST be:

1. Identified and tracked
2. Fixed or quarantined immediately
3. Never ignored or re-run until green

## Testing Methodologies

### Concepts

- **Unit Tests**: Test individual functions/methods in isolation. Characteristics: Fast, isolated, deterministic. Use for business logic and utility functions.
- **Integration Tests**: Test interaction between components. Characteristics: Slower, may use real dependencies. Use for API endpoints and service interactions.
- **End-to-End Tests**: Test complete user workflows. Characteristics: Slowest, tests real user scenarios. Use for critical user journeys.

### Patterns

- **Arrange-Act-Assert**: A three-phase test structure for clear organization.
- **Given-When-Then**: BDD-style test structure focusing on behavior.
- **Stub**: Provide canned responses for dependencies.
- **Mock**: Verify interactions occurred with dependencies.
- **Spy**: Record calls while using real implementation.
- **Fake**: A working implementation suitable for testing.
- **Descriptive Naming**: Test names that clearly describe scenario and outcome.
- **Should Naming**: BDD-style naming that reads like natural language.

## Best Practices

- Test happy path first.
- Test edge cases and error cases.
- Isolate tests to ensure independence.
- Make tests readable and descriptive.
- Use test fixtures and factories for common data setup.
- Avoid magic numbers in tests.

## Compliance Verification

```bash
# Run all tests
make test

# Check coverage
make coverage

# Verify no flaky tests (run multiple times)
for i in {1..5}; do make test || exit 1; done

# Check critical path coverage (language-specific)
coverage report --include="src/auth/*,src/security/*" --fail-under=95
```

## Additional Resources

### Reference Files

- **`references/test-patterns.md`** - Common test patterns and anti-patterns
- **`references/coverage-config.md`** - Coverage tool configuration

### Examples

- **`examples/rust-test-setup.md`** - Rust test organization
- **`examples/typescript-jest.config.js`** - Jest configuration
- **`examples/python-pytest.ini`** - Pytest configuration