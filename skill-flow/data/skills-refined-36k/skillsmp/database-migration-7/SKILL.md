---
name: database-migration
description: Create and apply database migrations using Drizzle ORM and Testcontainers for testing
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Database Migration

## Purpose

Create and apply database migrations using Drizzle ORM and Testcontainers for testing.

## When to Use

- Adding new tables or columns to database
- Modifying existing database schema
- Creating indexes or constraints
- Seeding initial data

## Capabilities

1. Creates Drizzle schema with proper types in packages/db-[domain]
2. Adds indexes for common queries
3. Creates foreign key relationships
4. Generates up/down migration files
5. Runs migration against database
6. Creates seed data if needed
7. Adds Testcontainers tests for migration verification

## Multi-Database Pattern

This monorepo uses a multi-database DDD pattern:

```
packages/
├── db-main/     # Shared entities (organizations, settings)
├── db-auth/     # Auth domain (users, sessions, credentials)
└── db-[domain]/ # Per-domain schemas
```

**Each domain owns its database schema package.**

## Migration Workflow

```bash
# 1. Add schema to packages/db-[domain]/src/schema/
# 2. Export from package index
# 3. Generate and apply
pnpm db:generate && pnpm db:migrate
```

### Schema Example

```typescript
// packages/db-main/src/schema/organizations.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const organizations = pgTable('organizations', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

// packages/db-main/src/index.ts
export * from './schema/organizations';
```

### Testcontainers Test

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { migrate } from 'drizzle-kit/node';

describe('Database Migration', () => {
  let postgres;
  before(async () => {
    postgres = await new PostgreSqlContainer('postgres:18').start();
  });
  after(async () => {
    await postgres.stop();
  });
  test('should apply migration successfully', async () => {
    await migrate({ connectionString: postgres.getConnectionUri() });
  });
});
```

## Commands Reference

| Command                         | Purpose                         |
| ------------------------------- | ------------------------------- |
| `pnpm db:generate [db-package]` | Generate migration files        |
| `pnpm db:migrate [db-package]`  | Apply migration to database     |
| `pnpm db:push [db-package]`     | Push schema directly (dev only) |
| `pnpm db:studio [db-package]`   | Open Drizzle Studio             |

## Rules

1. **Always test migrations** with Testcontainers before applying
2. **Use domain-specific packages** - don't mix domains in one schema
3. **Export types** for tRPC inference
4. **Add indexes** for frequently queried columns
5. **Use transactions** for multi-table changes

## Configuration Example

Each database package has its own `drizzle.config.ts`:

```typescript
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/schema',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```
