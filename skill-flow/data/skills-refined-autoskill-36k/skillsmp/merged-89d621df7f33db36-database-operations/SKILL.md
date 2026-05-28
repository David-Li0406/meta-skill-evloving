---
name: database-operations
description: Use this skill for PostgreSQL database operations with Drizzle ORM, including schema management, queries, migrations, and performance optimization.
---

# Database Operations Skill

This skill provides expertise in managing PostgreSQL databases using Drizzle ORM.

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

### Schema Management

- Define tables in `src/db/schema.ts` or `drizzle/` directory
- Use Drizzle's schema API with proper types
- Run `npm run db:generate` to create migrations
- Apply migrations with `npm run db:migrate`
- Use `npm run db:push` for quick schema updates

### Queries

- Place query files in `src/server/queries/`
- Import `db` from `src/db`
- Use prepared statements and proper joins for performance
- Handle transactions for multi-step operations

### Performance Optimization

- Use indexes on frequently queried columns
- Implement connection pooling with Neon
- Monitor slow queries with `EXPLAIN ANALYZE`
- Implement pagination for large result sets
- Consider caching for frequently accessed data

## Examples

### Schema Definition

```typescript
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### Querying User Preferences

```typescript
import { db, userPreferences } from '@/db';
import { eq } from 'drizzle-orm';

const preferences = await db.select()
  .from(userPreferences)
  .where(eq(userPreferences.userId, userId));
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

## Resources

- [Drizzle Documentation](https://orm.drizzle.team/)
- [Neon Documentation](https://neon.tech/docs)
- Project config: `drizzle.config.ts`
- Environment: `src/env.ts`