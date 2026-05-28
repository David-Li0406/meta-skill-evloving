---
name: database-management-drizzle-orm
description: Use this skill for managing databases with Drizzle ORM and Neon PostgreSQL, including schema definitions, queries, migrations, and performance optimization.
---

# Database Management with Drizzle ORM and Neon PostgreSQL

This skill provides expertise in managing databases using Drizzle ORM with Neon PostgreSQL.

## When to Use This Skill

- Creating or modifying database schemas
- Writing complex queries or transactions
- Running migrations and schema changes
- Optimizing query performance
- Setting up new database connections

## Key Technologies

- **Drizzle ORM**: Type-safe SQL queries and schema definitions
- **Neon PostgreSQL**: Serverless PostgreSQL database
- **Migrations**: Version-controlled schema changes

## Patterns and Conventions

### Schema Definition

- Schemas in `drizzle/` directory
- Use Drizzle's schema API with proper types
- Define relations and constraints

### Creating a New Table

1. Create a file in `lib/db/schemas/{domain}.ts`
2. Define enums if needed
3. Define the table with columns and indexes
4. Export types
5. Re-export from `lib/db/schema.ts`

```typescript
import { pgTable, pgEnum, index, integer, varchar, timestamp } from "drizzle-orm/pg-core";
import type { InferSelectModel, InferInsertModel } from "drizzle-orm";

// Enum (if needed)
export const statusEnum = pgEnum("status", ["active", "inactive"]);

// Table with indexes
export const items = pgTable("items", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  name: varchar("name", { length: 255 }).notNull(),
  status: statusEnum("status").notNull(),
  created_at: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updated_at: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_items_name").on(table.name),
]);

// Types
export type Item = InferSelectModel<typeof items>;
export type InsertItem = InferInsertModel<typeof items>;
```

### Queries

- Place in `src/server/queries/`
- Use prepared statements for performance
- Handle transactions for multi-step operations

### Migrations

- Run `npm run db:generate` to create migrations
- Run `npm run db:migrate` to apply changes
- Use `npm run db:studio` for visual schema management

### Performance Optimization

- Use indexes on frequently queried columns
- Implement connection pooling with Neon
- Monitor slow queries with `EXPLAIN ANALYZE`

## Examples

### Query with Drizzle

```typescript
// src/server/queries/getUsers.ts
import { db } from '@/server/db';
import { users } from '@/drizzle/schema';

export async function getUsers() {
  return await db.select().from(users);
}
```

### Migration Script

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Naming Conventions

- Index: `idx_{table}_{column}` → `idx_items_name`
- One domain per schema file → `songs.ts`, `dictionary.ts`

## Avoid

- `serial()` → use `integer().generatedAlwaysAsIdentity()`
- Timestamps without `{ withTimezone: true }`
- Foreign keys without explicit `onDelete`

## Resources

- [Drizzle Documentation](https://orm.drizzle.team/)
- [Neon Documentation](https://neon.tech/docs)
- Project config: `drizzle.config.ts`
- Environment: `src/env.ts`