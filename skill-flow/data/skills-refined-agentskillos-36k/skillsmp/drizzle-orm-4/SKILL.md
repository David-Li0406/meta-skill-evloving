---
name: drizzle-orm
description: Drizzle ORM patterns for Neon PostgreSQL. Use when creating tables, schemas, migrations, or database queries.
---

# Drizzle ORM (Neon PostgreSQL)

## Creating a new table

1. Create file in `lib/db/schemas/{domain}.ts`
2. Define enum if needed
3. Define table with columns and indexes
4. Export types
5. Re-export from `lib/db/schema.ts`

```typescript
import { pgTable, pgEnum, index, integer, varchar, timestamp } from "drizzle-orm/pg-core"
import type { InferSelectModel, InferInsertModel } from "drizzle-orm"

// 1. Enum (if needed)
export const statusEnum = pgEnum("status", ["active", "inactive"])

// 2. Table with indexes as third argument
export const items = pgTable("items", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  name: varchar("name", { length: 255 }).notNull(),
  status: statusEnum("status").notNull(),
  created_at: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updated_at: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_items_name").on(table.name),
])

// 3. Types
export type Item = InferSelectModel<typeof items>
export type InsertItem = InferInsertModel<typeof items>
```

See `examples/schema-pattern.ts` for full pattern.

## Adding a foreign key

```typescript
author_id: integer("author_id")
  .notNull()
  .references(() => users.id, { onDelete: "cascade" })
```

Always specify `onDelete` behavior explicitly.

## Standard columns

```typescript
// Primary key
id: integer("id").primaryKey().generatedAlwaysAsIdentity()

// Timestamps (always with timezone)
created_at: timestamp("created_at", { withTimezone: true }).notNull().defaultNow()
updated_at: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow()
```

## Naming conventions

- Index: `idx_{table}_{column}` → `idx_items_name`
- One domain per schema file → `songs.ts`, `dictionary.ts`

## Avoid

- `serial()` → use `integer().generatedAlwaysAsIdentity()`
- Timestamps without `{ withTimezone: true }`
- Foreign keys without explicit `onDelete`
