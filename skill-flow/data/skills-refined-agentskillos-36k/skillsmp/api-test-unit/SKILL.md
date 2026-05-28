---
name: api-test-unit
description: Generate unit tests using Jest with mocking, AAA pattern (Arrange-Act-Assert), and 80%+ coverage target. Use when testing business logic, handlers, or services in isolation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Unit Tests

## Purpose

Generate unit tests using **Jest** with proper mocking of dependencies, AAA pattern (Arrange-Act-Assert), and descriptive test names.

## Why Jest Instead of node:test?

This repository uses **Jest** for ALL testing instead of Node.js's built-in `node:test` runner:

- **Issue**: [nestjs/nest#14130](https://github.com/nestjs/nest/issues/14130) - NestJS `@nestjs/testing` is incompatible with `node:test`
- **Impact**: `node:test` cannot properly inject `QueryBus`, `CommandBus`, or other NestJS providers
- **Solution**: Jest provides full compatibility with NestJS's testing utilities and DI system

## When to Use

- Testing business logic in isolation
- Testing command/query handlers
- Testing repository methods
- Testing service methods
- Unit testing utilities

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/__tests__/**/*.test.ts
```

Tests are co-located with source code but cleanly separated in `__tests__/` subdirectory.

## Patterns Enforced

### AAA Pattern

All tests follow Arrange-Act-Assert:

- **Arrange**: Set up test data and mocks
- **Act**: Execute the function under test
- **Assert**: Verify expected outcomes

### Descriptive Test Names

Test names should describe:

- What is being tested
- The expected outcome
- Edge cases covered

Example: `should create user when valid data provided`

### Mocking

- Mock external dependencies
- Mock database calls
- Mock event bus
- Verify mock calls

### Coverage Target

- 80%+ code coverage
- Test success and failure paths
- Test edge cases

## Usage Example

```bash
/skill test-unit --name=CreateUserHandler --type=command-handler --scenarios='success,duplicate-email,database-error'
```

## Related Files

- [Test Integration](../test-integration/SKILL.md) - Integration tests
- [Test E2E](../test-e2e/SKILL.md) - E2E tests
- [Feature CQRS](../../core/feature-cqrs/SKILL.md) - Handlers to test
