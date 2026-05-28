---
name: database-management
description: Use this skill for managing database schemas, queries, migrations, and relationships with Drizzle ORM and PostgreSQL.
---

# Database Management with Drizzle ORM

## Package Structure

```sh
packages/database/
├── src/
│   ├── client.ts      # Drizzle client
│   ├── schema/        # Drizzle schemas
│   │   ├── users.ts
│   │   ├── sessions.ts
│   │   ├── accounts.ts
│   │   ├── verifications.ts
│   │   └── index.ts
│   └── index.ts       # Public exports
├── drizzle.config.ts  # Drizzle config
└── package.json
```

## Database Client

```ts
// packages/database/src/client.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import * as schema from './schema';

export const db = drizzle(process.env.DATABASE_URL!, {
  casing: 'snake_case', // Auto-converts camelCase ↔ snake_case
  schema,
});
```

## Schema Design

### Table Definition

```typescript
import { pgTable, serial, varchar, text, timestamp, boolean, integer } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 100 }),
  bio: text("bio"),
  isAdmin: boolean("is_admin").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Type exports
export type User = typeof users.$inferSelect;
export type UserCreate = typeof users.$inferInsert;
```

### Relationships

```typescript
import { relations } from "drizzle-orm";

// Define relations for query builder
export const usersRelations = relations(users, ({ many }) => ({
  sessions: many(sessions),
  accounts: many(accounts),
  posts: many(posts),
}));

export const modules = pgTable("modules", {
  id: serial("id").primaryKey(),
  title: varchar("title", { length: 255 }).notNull(),
  order: integer("order").default(0).notNull(),
});

export const segments = pgTable("segments", {
  id: serial("id").primaryKey(),
  moduleId: integer("module_id")
    .references(() => modules.id, { onDelete: "cascade" })
    .notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  order: integer("order").default(0).notNull(),
});

// Define relations for segments
export const segmentsRelations = relations(segments, ({ one }) => ({
  module: one(modules, {
    fields: [segments.moduleId],
    references: [modules.id],
  }),
}));
```

## Queries

### Basic CRUD Operations

```typescript
// src/data-access/users.ts
import { db } from "~/db";
import { users } from "~/db/schema";
import { eq } from "drizzle-orm";
import type { User, UserCreate } from "~/db/schema";

export async function getUsers() {
  return db.query.users.findMany();
}

export async function getUserById(id: number) {
  const result = await db
    .select()
    .from(users)
    .where(eq(users.id, id))
    .limit(1);
  return result[0];
}

export async function createUser(user: UserCreate) {
  const result = await db.insert(users).values(user).returning();
  return result[0];
}

export async function updateUser(id: number, user: Partial<UserCreate>) {
  const result = await db
    .update(users)
    .set({ ...user, updatedAt: new Date() })
    .where(eq(users.id, id))
    .returning();
  return result[0];
}

export async function deleteUser(id: number) {
  const result = await db
    .delete(users)
    .where(eq(users.id, id))
    .returning();
  return result[0];
}
```

### Query Patterns

#### Select Specific Columns

```typescript
const users = await db
  .select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users);
```

#### Filtering

```typescript
import { eq, and, or, isNotNull } from "drizzle-orm";

// Equality
const user = await db
  .select()
  .from(users)
  .where(eq(users.email, email));

// Multiple conditions
const activeAdmins = await db
  .select()
  .from(users)
  .where(and(eq(users.isAdmin, true), isNotNull(users.lastLoginAt)));
```

#### Joins

```typescript
import { eq } from "drizzle-orm";

// Inner join
const segmentsWithModules = await db
  .select({
    segment: segments,
    moduleTitle: modules.title,
  })
  .from(segments)
  .innerJoin(modules, eq(segments.moduleId, modules.id));
```

### Transactions

```typescript
export async function reorderSegmentsUseCase(
  updates: { id: number; order: number }[]
) {
  return db.transaction(async (tx) => {
    const results = [];
    for (const update of updates) {
      const [result] = await tx
        .update(segments)
        .set({ order: update.order, updatedAt: new Date() })
        .where(eq(segments.id, update.id))
        .returning();
      results.push(result);
    }
    return results;
  });
}
```

## Migration Commands

```bash
# Generate migration from schema changes
npm run db:generate

# Run migrations
npm run db:migrate

# Push schema directly (development only)
npm run db:push

# Open Drizzle Studio
npm run db:studio

# Reset database (clear, migrate, seed)
npm run db:reset
```

## Common Patterns

### Soft Delete

```typescript
export const users = pgTable("users", {
  // ...other fields
  deletedAt: timestamp("deleted_at"),
});

// Query only non-deleted
const activeUsers = await db
  .select()
  .from(users)
  .where(isNull(users.deletedAt));

// Soft delete
await db
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, id));
```

### Check if Exists

```typescript
export async function isEmailInUse(email: string): Promise<boolean> {
  const existing = await db
    .select({ id: users.id })
    .from(users)
    .where(eq(users.email, email))
    .limit(1);
  return existing.length > 0;
}
```

## Common Mistakes

| Mistake                            | Correct Pattern                           |
| ---------------------------------- | ----------------------------------------- |
| Missing `.returning()` on mutate   | Always use `.returning()` to get results  |
| Using `any` for query results      | Use `$inferSelect` / `$inferInsert` types |
| Not using transactions             | Wrap related mutations in `transaction`   |
| Forgetting `casing: 'snake_case'`  | Set in drizzle config for auto-conversion |
| Hardcoding IDs                     | Use `crypto.randomUUID()` for UUIDs       |
| Missing indexes on foreign keys    | Add indexes for frequently queried FKs    |
| Not handling null from `findFirst` | Check for undefined before using result   |
| Using raw SQL for simple queries   | Prefer query builder for type safety      |

## Database Checklist

- [ ] Tables have appropriate indexes for queried columns
- [ ] Foreign keys use onDelete cascade where appropriate
- [ ] Data access functions use `verbNoun` naming
- [ ] Select only needed columns, not `select()`
- [ ] Use transactions for multi-step operations
- [ ] Always update `updatedAt` on modifications
- [ ] Use parameterized queries (automatic with Drizzle)
- [ ] Run `db:generate` after schema changes
- [ ] Type exports for `$inferSelect` and `$inferInsert`
- [ ] Relations defined for query builder usage