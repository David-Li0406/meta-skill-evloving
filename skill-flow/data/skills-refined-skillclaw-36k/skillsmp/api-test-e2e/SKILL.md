---
name: api-test-e2e
description: Generate E2E tests using Jest and Testcontainers for PostgreSQL, Redis, and RabbitMQ with full application stack testing. Use when testing API endpoints end-to-end or verifying multi-tenancy isolation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# E2E Tests

## Purpose

Generate end-to-end tests using **Jest + Testcontainers** for real PostgreSQL, Redis, and RabbitMQ instances with proper setup, teardown, and tenant isolation testing.

## Why Jest Instead of node:test?

This repository uses **Jest** for ALL testing instead of Node.js's built-in `node:test` runner:

- **Issue**: [nestjs/nest#14130](https://github.com/nestjs/nest/issues/14130) - NestJS `@nestjs/testing` is incompatible with `node:test`
- **Impact**: `node:test` cannot properly inject `QueryBus`, `CommandBus`, or other NestJS providers
- **Solution**: Jest provides full compatibility with NestJS's testing utilities and DI system

**Note**: These are E2E tests that test the entire application stack. For module-level integration tests with co-located test fixtures, use `test-integration`.

## When to Use

- Testing API endpoints end-to-end
- Verifying database operations
- Testing multi-tenancy isolation
- Validating integration with Redis/RabbitMQ
- Testing CQRS flows

## What It Generates

### Directory Structure

```
apps/api/test/{feature}.e2e-spec.ts
```

**E2E vs Integration Tests**:

- **E2E Tests** (`test/`): Full application stack, Testcontainers, HTTP requests
- **Integration Tests** (`src/modules/{feature}/__tests__/`): Module-level, co-located fixtures, direct imports

## Patterns Enforced

### Testcontainers Setup

- PostgreSQL container for database
- Redis container for caching
- RabbitMQ container for events
- Migrations run before tests
- Cleanup after each test

### Unique Test Data

- Random UUIDs for test entities
- Random emails to avoid conflicts
- Tenant isolation verification

### Tenant Isolation Tests

- Verify cross-tenant access is blocked
- Verify each tenant sees only their data
- Verify audit logging per tenant

## Usage Example

```bash
/skill test-e2e --name=Users --endpoints='POST /users,GET /users/:id,PATCH /users/:id,DELETE /users/:id'
```

## Related Files

- [Test Unit](../test-unit/SKILL.md) - Unit tests
- [Test Integration](../test-integration/SKILL.md) - Integration tests
- [Feature CQRS](../../core/feature-cqrs/SKILL.md) - Features to test
