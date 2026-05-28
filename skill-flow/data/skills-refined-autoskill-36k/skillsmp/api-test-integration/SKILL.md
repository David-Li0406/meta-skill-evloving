---
name: api-test-integration
description: Generate integration tests for CQRS handlers with mocked dependencies and co-located fixtures using Jest. Use when testing handlers, database operations, or event publishing in isolation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Integration Tests

## Purpose

Generate co-located integration tests for CQRS handlers with mocked dependencies, test fixtures, and real database operations using **Jest + Testcontainers**.

## Why Jest Instead of node:test?

This repository uses **Jest** for ALL testing instead of Node.js's built-in `node:test` runner:

- **Issue**: [nestjs/nest#14130](https://github.com/nestjs/nest/issues/14130) - NestJS `@nestjs/testing` is incompatible with `node:test`
- **Impact**: `node:test` cannot properly inject `QueryBus`, `CommandBus`, or other NestJS providers
- **Solution**: Jest provides full compatibility with NestJS's testing utilities and DI system

## When to Use

- Testing command/query handlers in isolation
- Testing database operations with real PostgreSQL
- Testing event publishing
- Multi-tenancy isolation tests
- Testing with co-located fixtures

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/__tests__/
├── fixtures/
│   ├── {feature}.fixture.ts
│   └── database.fixture.ts
├── handlers/
│   ├── commands/
│   │   └── {command}.integration.test.ts
│   └── queries/
│       └── {query}.integration.test.ts
└── {feature}.integration.test.ts
```

**Integration vs E2E Tests**:

- **Integration Tests** (`src/modules/{feature}/__tests__/`): Module-level, co-located fixtures, direct imports
- **E2E Tests** (`test/`): Full application stack, Testcontainers, HTTP requests

## Patterns Enforced

### Co-located Fixtures

Fixtures defined alongside tests:

- Reusable test data builders
- Database setup helpers
- Tenant isolation helpers

### Mocked Dependencies

- Mock external services
- Mock event bus (unless testing events)
- Mock cache (unless testing cache)

### Real Database

- Use Testcontainers PostgreSQL
- Run migrations before tests
- Clean up after each test

## Usage Example

```bash
/skill test-integration --name=CreateUserHandler --type=command --withFixtures=true
```

## Related Files

- [Feature CQRS](../../core/feature-cqrs/SKILL.md) - Handlers to test
- [Test Unit](../test-unit/SKILL.md) - Unit tests
- [Test E2E](../test-e2e/SKILL.md) - E2E tests
