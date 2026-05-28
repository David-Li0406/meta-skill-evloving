---
name: api-data-repository
description: Generate repository extending BaseRepository with multi-tenancy support, Testcontainers, and transaction patterns. Use when creating data access layer or adding tenant-scoped queries.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Data Repository

## Purpose

Generate a repository class that extends `BaseRepository` from `@starter/foundation-repositories` with multi-tenancy support, transaction patterns, and Testcontainers for integration testing.

## When to Use

- Creating data access layer for new entities
- Adding complex query methods to repositories
- Implementing tenant-scoped data access
- Creating repositories with proper test coverage

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/repositories/
├── {entity}.repository.ts
└── index.ts
```

## Patterns Enforced

### BaseRepository Extension

Repositories must extend `BaseRepository<T>` from `@starter/foundation-repositories`:

- Inherits CRUD methods (findById, findAll, create, update, delete)
- All methods accept `tenantId` parameter
- Transaction support via `db.transaction()`

### Multi-Tenancy

- All queries include `WHERE organization_id = tenantId`
- All methods validate tenant access
- Cross-tenant queries throw `ForbiddenException`

### Transaction Support

- Multi-step writes use `db.transaction(async (tx) => {...})`
- All operations within transaction use `tx` instead of `db`
- Transactions rollback on error

### Testcontainers Testing

- Integration tests use real PostgreSQL via Testcontainers
- Unique test data per test
- Cleanup after each test
- Tenant isolation tests

## Usage Example

```bash
/skill data-repository --name=User --table=users --methods='findByEmail,searchByName,findByIdWithProfile'
```

## Related Files

- [Feature CQRS](../feature-cqrs/SKILL.md) - Complete CQRS feature with repository
- [Data Migration](../data-migration/SKILL.md) - Database schema for repository
- [Test Integration](../../testing/test-integration/SKILL.md) - Integration tests
