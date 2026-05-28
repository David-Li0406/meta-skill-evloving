---
name: drizzle-orm-postgresql-database
description: Use this skill when working with Drizzle ORM and PostgreSQL for tasks related to database schema design, queries, migrations, and relationships.
---

# Skill body

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

## Schema Definition

### Users Table

```ts
// packages/database/src/schema/users.ts
import { pgTable, serial, varchar, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }),
  bio: text('bio'),
  isAdmin: boolean('is_admin').default(false).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Type inference
export type User = typeof users.$inferSelect;
export type UserCreate = typeof users.$inferInsert;
```

## Relationships

```ts
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  sessions: many(sessions),
  accounts: many(accounts),
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

## Queries

### Relational Queries

```ts
// Find one with relations
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { sessions: true, posts: true },
});

// Find many with filters
const activePosts = await db.query.posts.findMany({
  where: eq(posts.published, true),
  orderBy: desc(posts.createdAt),
  limit: 10,
});
```

### SQL-like API

```ts
// Select
const allUsers = await db.select().from(users);
const names = await db.select({ name: users.name }).from(users);

// With conditions
const admins = await db.select().from(users).where(eq(users.isAdmin, true));
```

## Indexes

```ts
import { pgTable, index, uniqueIndex } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
}, (table) => ({
  emailIdx: uniqueIndex('email_idx').on(table.email),
  createdAtIdx: index('created_at_idx').on(table.createdAt),
}));
```