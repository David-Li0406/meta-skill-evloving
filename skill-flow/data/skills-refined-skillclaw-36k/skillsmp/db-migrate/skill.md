---
name: db-migrate
description: Create and run database migrations for PostgreSQL using Drizzle ORM
allowed-tools: [Write, Bash, Read, Edit]
---

## Purpose
Create migration scripts for database schema changes in the learning-cards PostgreSQL database using Drizzle ORM.

## Guidelines

### 1. Migration Workflow with Drizzle Kit

**Primary Approach: Use Drizzle Kit (Recommended)**

Drizzle Kit automatically generates migrations by comparing schema changes:

```bash
# 1. Update schema files in src/infrastructure/database/schema/
# 2. Generate migration
npx drizzle-kit generate

# 3. Apply migration
npx drizzle-kit push

# Or use push for prototyping (applies changes directly without migration files)
npx drizzle-kit push
```

### 2. Schema File Structure

Schema files are located in `src/infrastructure/database/schema/`:
- `auth.schema.ts` - Authentication tables
- `content.schema.ts` - Content management tables
- `groups.schema.ts` - Group/organization tables
- `gamification.schema.ts` - Gamification features
- `analytics.schema.ts` - Analytics and tracking
- `learning-path.schema.ts` - Learning paths
- `index.ts` - Schema exports

### 3. Drizzle Schema Pattern

```typescript
import { pgTable, text, integer, timestamp, boolean, varchar, uuid } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// Define table
export const exampleTable = pgTable('example_table', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  description: text('description'),
  count: integer('count').default(0).notNull(),
  isActive: boolean('is_active').default(true).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Define relations (optional)
export const exampleTableRelations = relations(exampleTable, ({ one, many }) => ({
  // Define relationships here
}));

// Export types
export type ExampleTable = typeof exampleTable.$inferSelect;
export type NewExampleTable = typeof exampleTable.$inferInsert;
```

### 4. Common Schema Patterns

**Primary Keys:**
```typescript
// Auto-incrementing integer
id: serial('id').primaryKey()

// UUID (recommended for PostgreSQL)
id: uuid('id').defaultRandom().primaryKey()
```

**Common Column Types:**
```typescript
// Text fields
name: varchar('name', { length: 255 }).notNull()
description: text('description')
email: varchar('email', { length: 255 }).notNull().unique()

// Numbers
count: integer('count').default(0).notNull()
score: real('score') // for decimals

// Booleans
isActive: boolean('is_active').default(true).notNull()

// Timestamps
createdAt: timestamp('created_at').defaultNow().notNull()
updatedAt: timestamp('updated_at').defaultNow().notNull()

// JSON
metadata: jsonb('metadata')

// Enums
status: text('status', { enum: ['active', 'inactive', 'pending'] }).notNull()
```

**Foreign Keys:**
```typescript
userId: uuid('user_id')
  .notNull()
  .references(() => users.id, { onDelete: 'cascade' })
```

**Indexes:**
```typescript
import { index, uniqueIndex } from 'drizzle-orm/pg-core';

export const exampleTable = pgTable('example_table', {
  // ... columns
}, (table) => ({
  emailIdx: index('email_idx').on(table.email),
  userIdIdx: index('user_id_idx').on(table.userId),
  emailUnique: uniqueIndex('email_unique').on(table.email),
}));
```

### 5. Manual Migrations (When Needed)

For complex migrations that Drizzle Kit can't handle automatically, create manual SQL migration files in `drizzle/migrations/`:

```sql
-- drizzle/migrations/0005_add_custom_logic.sql

-- Add complex data transformations
UPDATE users SET normalized_email = LOWER(email);

-- Add triggers or functions
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_example_updated_at
  BEFORE UPDATE ON example_table
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### 6. Migration Testing

```bash
# Check migration status
npx drizzle-kit check

# Generate migration (dry run to see what would change)
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit push

# Introspect existing database (generates schema from DB)
npx drizzle-kit introspect
```

### 7. Database Operations in Code

```typescript
import { db } from '@/infrastructure/database/drizzle';
import { users } from '@/infrastructure/database/schema';
import { eq, and, or, like, gte } from 'drizzle-orm';

// Select
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, userId));

// Insert
await db.insert(users).values({
  email: 'test@example.com',
  name: 'Test User',
});

// Update
await db.update(users)
  .set({ name: 'New Name', updatedAt: new Date() })
  .where(eq(users.id, userId));

// Delete
await db.delete(users).where(eq(users.id, userId));

// Transactions
await db.transaction(async (tx) => {
  await tx.insert(users).values({ ... });
  await tx.insert(profiles).values({ ... });
});
```

## Example Usage

When user asks: "Add a new column to track user preferences"

1. Edit the appropriate schema file (e.g., `src/infrastructure/database/schema/auth.schema.ts`)
2. Add the new column:
```typescript
preferences: jsonb('preferences').$type<UserPreferences>(),
```
3. Generate migration: `npx drizzle-kit generate`
4. Review the generated migration in `drizzle/migrations/`
5. Apply migration: `npx drizzle-kit push`
6. Update TypeScript types if needed (Drizzle auto-generates types)

## Safety Checks
- ✅ Always test schema changes locally first
- ✅ Review generated migrations before applying
- ✅ Use transactions for complex multi-table changes
- ✅ Add `notNull()` constraints carefully on existing tables
- ✅ Use `onDelete: 'cascade'` or `'set null'` for foreign keys appropriately
- ✅ Backup database before destructive operations
- ⚠️ Never delete data without explicit user confirmation
- ⚠️ Consider data migration scripts for column renames or type changes
- ⚠️ Be careful with unique constraints on existing data
