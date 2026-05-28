---
name: testing-standards-and-patterns
description: Use this skill when you need guidance on testing methodologies, including test organization, coverage requirements, and best practices for unit, integration, and end-to-end tests.
---

# Skill body

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

1. 

## Testing Patterns

### Unit Tests

- **Description**: Test individual functions/methods in isolation.
- **Scope**: Single function, class, or module.
- **Characteristics**: Fast, isolated, deterministic.
- **When to Use**: Business logic, utility functions, transformations.

### Integration Tests

- **Description**: Test interaction between components.
- **Scope**: Multiple components working together.
- **Characteristics**: Slower, may use real dependencies.
- **When to Use**: API endpoints, database operations, service interactions.

### End-to-End Tests

- **Description**: Test complete user workflows.
- **Scope**: Full application stack.
- **Characteristics**: Slowest, tests real user scenarios.
- **When to Use**: Critical user journeys, smoke tests.

### Testing Patterns

#### Arrange-Act-Assert

- **Description**: Three-phase test structure for clear test organization.
- **When to Use**: For unit or integration tests.
- **Example**:
  - **Arrange**: Set up test data and preconditions.
  - **Act**: Execute the code under test.
  - **Assert**: Verify expected outcomes.

#### Given-When-Then

- **Description**: BDD-style test structure focusing on behavior.
- **When to Use**: When the test is focused on business behavior rather than technical implementation.
- **Example**:
  - **Given**: Initial conditions.
  - **When**: Action taken.
  - **Then**: Expected outcome.