---
name: drizzle-orm
description: Use this skill when building type-safe SQL queries, schema definitions, migrations, and relations in TypeScript applications with Drizzle ORM.
---

# Drizzle ORM Development Guidelines

You are an expert in Drizzle ORM, TypeScript, and SQL database design with a focus on type safety and performance.

## Core Principles

- Drizzle embraces SQL - if you know SQL, you know Drizzle.
- Schema-as-code serves as the single source of truth.
- Type safety is enforced at compile time, catching errors before runtime.
- Lightweight with minimal runtime overhead (~7.4kb min+gzip).
- Serverless-ready: works with Node.js, Bun, Deno, Cloudflare Workers.

## Quick Start

### Installation

```bash
# Core ORM
npm install drizzle-orm

# Database driver (choose one)
npm install pg            # PostgreSQL
npm install mysql2        # MySQL
npm install better-sqlite3 # SQLite

# Drizzle Kit (migrations)
npm install -D drizzle-kit
```

### Basic Setup

```typescript
// db/schema.ts
import { pgTable, serial, text, timestamp, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

// db/client.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

## Schema Design

### Basic Table Definition

```typescript
import { pgTable, serial, text, varchar, timestamp, boolean, integer } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  name: text("name"),
  isActive: boolean("is_active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});
```

### Defining Relations

```typescript
import { relations } from "drizzle-orm";

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));
```

## Query Patterns

### Select Queries

```typescript
// Select all columns
const allUsers = await db.select().from(users);

// Select specific columns
const userEmails = await db.select({ email: users.email }).from(users);
```

### Insert Operations

```typescript
// Single insert
const newUser = await db
  .insert(users)
  .values({
    email: "user@example.com",
    name: "John Doe",
  })
  .returning();
```

### Update Operations

```typescript
await db
  .update(users)
  .set({ name: "Jane Doe", updatedAt: new Date() })
  .where(eq(users.id, 1));
```

### Delete Operations

```typescript
await db.delete(users).where(eq(users.id, 1));
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx
    .insert(users)
    .values({ email: "user@example.com", name: "User" })
    .returning();

  await tx.insert(posts).values({
    title: "First Post",
    authorId: user.id,
  });
});
```

## Migrations

### Generate Migrations

```bash
# Generate migration based on schema changes
npx drizzle-kit generate

# Apply migrations to database
npx drizzle-kit migrate
```

### Migration Configuration

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

## Type Safety Best Practices

### Infer Types from Schema

```typescript
import { InferSelectModel, InferInsertModel } from "drizzle-orm";

// Infer types from table definitions
export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;
```

## Performance Best Practices

### Use Indexes Appropriately

Always add indexes for columns used in WHERE clauses and JOINs.

### Select Only Needed Columns

```typescript
// Good: Fetches only needed columns
const userNames = await db
  .select({ id: users.id, name: users.name })
  .from(users);
```

### Avoid N+1 Queries

```typescript
// Good: Use relational queries or joins
const usersWithPosts = await db.query.users.findMany({
  with: { posts: true },
});
```

## Common Mistakes to Avoid

1. **Not defining indexes** - Always add indexes for frequently queried columns.
2. **Fetching too much data** - Select only the columns you need.
3. **Missing foreign key constraints** - Define proper relationships in schema.
4. **Not using transactions** - Wrap related operations in transactions for data integrity.

## Related Skills

When using Drizzle, these skills enhance your workflow:
- **prisma**: Alternative ORM comparison: Drizzle vs Prisma trade-offs
- **typescript**: Advanced TypeScript patterns for type-safe queries
- **nextjs**: Drizzle with Next.js Server Actions and API routes
- **sqlalchemy**: SQLAlchemy patterns for Python developers learning Drizzle

[Full documentation available in these skills if deployed in your bundle]