---
name: testing-strategy
description: A specialist skill that designs and implements a testing strategy for a codebase. This skill should be used after code development and before code review.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Testing Strategy Skill

## Tooling Notes

This skill should only use read-only commands and avoid modifying files.

## Workflow

Copy this checklist and use it to track your progress through the testing strategy design process:

```markdown
Testing Strategy Checklist

- [ ] Understand the Codebase
  - [ ] Familiarize yourself with the codebase and its functionality.
  - [ ] Identify recent changes made by developers.
- [ ] Determine Testing Needs
  - [ ] Decide on the types of tests required (unit, integration, end-to-end, performance, security).
  - [ ] Identify critical areas of the code that need thorough testing.
- [ ] Design Test Cases
  - [ ] Create test cases that cover various scenarios, including edge cases and error handling.
  - [ ] Ensure tests are clear, concise, and maintainable.
- [ ] Implement Tests
  - [ ] Write the tests according to the designed test cases.
  - [ ] Use appropriate testing frameworks and tools.
- [ ] Execute Tests
  - [ ] Run the tests to validate the code changes.
  - [ ] Analyze test results to identify any failures or issues.
- [ ] Maintain Tests
  - [ ] Regularly update and maintain the test suite to ensure it remains relevant and effective.
```

## Testing Pyramid

When designing a testing strategy, consider the following pyramid structure to ensure a balanced approach:

```plaintext
        /\
       /  \        **E2E Tests** (10%)
      /----\       - Critical user journeys
     /      \      - Slow but comprehensive
    /--------\     **Integration Tests** (20%)
   /          \    - Component interactions
  /------------\   - API contracts
 /              \  **Unit Tests** (70%)
/________________\ - Fast, isolated
                   - Business logic focus
```

## Framework Selection

Choose appropriate testing frameworks based on the programming language and project requirements. Some popular options include:

- **JavaScript/TypeScript**: For unit, use Vitest. For integration, use Vitest with MSQ. For E2E tests, use Playwright. For component tests, use Testing Library.

- **Python**: For unit and integration tests, use Pytest. For E2E tests, use Playwright.

## Test Coverage

Ensure that your testing strategy covers the following aspects:

- **Business Logic**: Core functionalities and algorithms.
- **Edge Cases**: Unusual or extreme input scenarios.
- **Error Handling**: Proper responses to invalid inputs or failures.
- **Performance**: Critical code paths that impact performance.
- **API Contracts**: Interactions between different services or components.

## Mocking Strategy

When designing tests, implement a mocking strategy to isolate components and simulate external dependencies. Consider the following guidelines:

- **Mock External Services**: Use mocks for APIs, databases, and third-party services to ensure tests are reliable and fast.
- **Use Test Doubles**: Implement stubs, spies, or fakes as needed to simulate behavior without relying on actual implementations.
- **Isolate Units**: Ensure unit tests focus on individual components without side effects from dependencies.

## Coverage Thresholds

Set minimum coverage thresholds to ensure adequate test coverage:

- **Unit Tests**: Aim for at least 80% coverage.
- **Integration Tests**: Aim for at least 70% coverage.
- **E2E Tests**: Aim for at least 60% coverage.
