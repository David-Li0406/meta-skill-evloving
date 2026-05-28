---
name: drizzle-orm
description: Use this skill when developing with Drizzle ORM, a lightweight type-safe TypeScript ORM optimized for SQL-like syntax and serverless environments.
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
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
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

## Schema Definition

### Basic Table Definition

```typescript
import { pgTable, serial, text, timestamp, boolean, integer } from "drizzle-orm/pg-core";

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  authorId: integer("author_id").references(() => users.id),
  publishedAt: timestamp("published_at"),
  createdAt: timestamp("created_at").defaultNow(),
});
```

### Naming Conventions

Use the `casing` option for automatic camelCase to snake_case mapping:

```typescript
import { drizzle } from "drizzle-orm/node-postgres";

const db = drizzle(pool, {
  casing: "snake_case", // Automatically maps camelCase to snake_case
});
```

## Migration-First Development Workflow

### Core Principle: Migration-First Development

**Critical Rule**: Schema changes ALWAYS start with migrations, never code-first.

### Why Migration-First?
- SQL migrations are the single source of truth.
- Prevents schema drift between environments.
- Enables rollback and versioning.
- Forces explicit schema design decisions.
- TypeScript types generated from migrations.
- CI/CD can validate schema changes.

### Complete Migration Workflow

1. **Design Schema in SQL Migration**: Create descriptive SQL migration files.
2. **Run Migrations**: Apply migrations to the database.
3. **Update TypeScript Definitions**: Ensure TypeScript types reflect the latest schema.

### Example Migration

```sql
-- drizzle/0001_create_users_table.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## First Query

```typescript
import { db } from './db/client';
import { users } from './db/schema';
import { eq } from 'drizzle-orm';

// Insert
const newUser = await db.insert(users).values({
  email: 'user@example.com',
  name: 'John Doe',
}).returning();

// Select
const allUsers = await db.select().from(users);

// Where
const user = await db.select().from(users).where(eq(users.id, 1));

// Update
await db.update(users).set({ name: 'Jane Doe' }).where(eq(users.id, 1));

// Delete
await db.delete(users).where(eq(users.id, 1));
```