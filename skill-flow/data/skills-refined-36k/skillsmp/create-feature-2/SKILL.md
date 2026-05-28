---
name: create-feature
description: Generate a new full-stack feature with database schema, CQRS handlers, API endpoints, and frontend components using node:test and Testcontainers
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Create Feature

When to use this skill:

- Creating a new domain feature with full stack implementation
- Adding CRUD operations for a new entity
- Building features that require database + API + frontend

What this skill does:

1. Creates database schema in appropriate packages/db-\* package (e.g., db-main, db-auth)
2. Generates Drizzle migration
3. Creates CQRS command/query handlers in apps/api
4. Creates tRPC router for type-safe API
5. Generates frontend components (Server + Client)
6. Adds tests using node:test for unit tests and Testcontainers for E2E
7. Updates documentation

## Testing Requirements

**ALL features must include tests:**

### Backend (apps/api)

**Unit Tests (node:test):**

```typescript
// apps/api/src/modules/users/users.service.test.ts
import { test, describe, mock } from 'node:test';
import assert from 'node:assert';

describe('UserService', () => {
  test('should create a user', async () => {
    const service = new UserService();
    const result = await service.create({
      name: 'Test User',
      email: 'test@example.com',
    });
    assert.equal(result.name, 'Test User');
  });
});
```

**E2E Tests (Testcontainers):**

```typescript
// apps/api/src/modules/users/users.service.e2e.test.ts
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { describe, test, before, after } from 'node:test';
import assert from 'node:assert';

describe('UserService E2E', () => {
  let postgres;
  let connectionString;

  before(async () => {
    postgres = await new PostgreSqlContainer('postgres:18').start();
    connectionString = postgres.getConnectionUri();
  });

  after(async () => {
    await postgres.stop();
  });

  test('should persist user to database', async () => {
    // Test with real database
  });
});
```

### Frontend (apps/web)

**Playwright E2E Tests:**

```typescript
// apps/web-e2e/src/features/users.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test('should create a new user', async ({ page }) => {
    await page.goto('/users');
    await page.click('button:has-text("Add User")');
    await page.fill('[name="name"]', 'Test User');
    await page.fill('[name="email"]', 'test@example.com');
    await page.click('button:has-text("Save")');
    await expect(page.locator('text=Test User')).toBeVisible();
  });
});
```

## Package Structure

When creating database schemas:

- Use `packages/db-main` for shared entities (organizations, settings)
- Create new `packages/db-[domain]` for domain-specific schemas
- Each schema package exports types for tRPC inference

## Commands

```bash
# After creating a feature, run appropriate tests:
pnpm run test:api:unit    # Backend unit tests
pnpm run test:api:e2e     # Backend E2E tests (Testcontainers)
pnpm run test:web:e2e     # Frontend E2E tests (Playwright)
```

Usage:

```
"Create a feature for managing users with name, email, and role"
"Add a product catalog feature with categories and inventory"
```
