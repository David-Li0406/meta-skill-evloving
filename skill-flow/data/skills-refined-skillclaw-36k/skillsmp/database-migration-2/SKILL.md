---
name: database-migration
description: Guide through safe database schema modification and migration generation for Drizzle ORM with D1 database. Use when modifying server/database/schema.ts or managing database changes.
---

# Database Migration Workflow Skill

Guides through the safe process of database schema modification and migration generation for Drizzle
ORM with D1 database.

## Purpose

USE this skill when:

- Modifying `server/database/schema.ts`
- Adding, removing, or changing table definitions
- Altering column definitions, constraints, or relationships
- After any database schema changes

DO NOT use this skill for:

- Reading database schema
- Running queries
- Data operations (INSERT, UPDATE, DELETE)

## Critical Rules (NEVER VIOLATE)

⛔ **NEVER execute `.sql` files manually** - All database changes MUST be applied through schema
modifications ⛔ **NEVER run `pnpm db:generate` automatically** - ALWAYS prompt the user to execute
this command ⛔ **NEVER edit migration files manually** - Migration files are generated and should
remain unchanged

## Workflow Steps

### Step 1: Detect Schema Modification

**Goal**: Identify when database schema has been modified.

**Actions**:

1. Monitor changes to `server/database/schema.ts`
2. Detect any of the following modifications:
   - New table definitions (`sqliteTable(...)`)
   - Column additions/removals/changes
   - Index or constraint modifications
   - Foreign key relationship changes
3. If schema modified, proceed to Step 2

**Output**: Confirmation that schema has been changed.

---

### Step 2: Prompt User for Migration Generation

**Goal**: Instruct user to generate migration files (NEVER do it automatically).

**Actions**:

1. Display formatted message to user:

```
⚠️  Database schema has been updated in server/database/schema.ts

Please run the following command to generate migration files:

    pnpm db:generate

This will:
- Analyze schema differences
- Generate SQL migration file in server/database/migrations/
- Create snapshot in server/database/migrations/meta/

After running, review the generated migration before committing.
```

2. WAIT for user confirmation that they executed the command
3. DO NOT proceed until user confirms migration generation completed

**Output**: User has executed `pnpm db:generate` and migrations are generated.

---

### Step 3: Review Generated Migration

**Goal**: Verify generated migration is safe and correct.

**Actions**:

1. Identify the newly generated migration file in `server/database/migrations/`
   - Files are named with timestamp: `XXXX_descriptive_name.sql`
   - Find the most recent file
2. Read the generated `.sql` file
3. Review SQL statements for:
   - **CREATE TABLE**: Verify table name, columns, types
   - **ALTER TABLE**: Check if modifications are as intended
   - **DROP TABLE**: ⚠️ **CRITICAL** - Confirm this is intentional (data loss!)
   - **DROP COLUMN**: ⚠️ **CRITICAL** - Confirm this is intentional (data loss!)
4. Check for potential issues:
   - Unintended table drops
   - Missing columns that should exist
   - Incorrect data types
   - Foreign key mismatches
5. Verify snapshot file updated in `server/database/migrations/meta/`

**Output**: Migration reviewed and confirmed safe.

---

### Step 4: Test Migration Locally

**Goal**: Verify migration works in development environment.

**Actions**:

1. Prompt user to test the migration:

```
✅ Migration file reviewed and appears correct.

To test the migration locally:

1. Ensure local dev environment is running (pnpm dev)
2. Migration will apply automatically in dev mode
3. Verify application functionality:
   - Check affected features still work
   - Test CRUD operations on modified tables
   - Verify TypeScript types are correct

If you encounter issues:
- Schema drift: Check server/database/schema.ts matches migrations
- Type errors: Ensure exported types are updated
- Runtime errors: Check queries using modified tables
```

2. Wait for user confirmation that testing is complete
3. Address any issues identified during testing

**Output**: Migration tested successfully in local environment.

---

### Step 5: Commit Schema and Migration Together

**Goal**: Ensure schema and migration files are committed together.

**Actions**:

1. Verify the following files are staged for commit:
   - `server/database/schema.ts` (modified schema)
   - `server/database/migrations/XXXX_*.sql` (new migration)
   - `server/database/migrations/meta/_journal.json` (updated journal)
   - `server/database/migrations/meta/XXXX_snapshot.json` (new snapshot)
2. Prompt user to commit with descriptive message:

```
✅ Ready to commit schema changes and migration.

Git add these files:
    git add server/database/schema.ts
    git add server/database/migrations/

Suggested commit message:

    feat(db): [describe schema change]

    - [Specific change 1]
    - [Specific change 2]

    Migration: [migration_file_name.sql]

Ensure all 4 types of files are included in the commit.
```

3. Confirm commit includes schema + migration + meta files

**Output**: Schema and migration committed together successfully.

---

## Common Scenarios

### Adding a New Table

```typescript
// server/database/schema.ts

export const newTable = sqliteTable("new_table", {
	id: text("id").primaryKey(),
	name: text("name").notNull(),
	createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
})

export type NewTable = typeof newTable.$inferSelect
export type NewTableInsert = typeof newTable.$inferInsert
```

**After modification**: Follow workflow → User runs `pnpm db:generate` → Review migration → Test →
Commit

### Modifying Existing Column

```typescript
// Before
email: text("email"),

// After
email: text("email").notNull(),
```

**After modification**: Follow workflow → Migration will contain `ALTER TABLE` → Review carefully →
Test → Commit

### Removing a Table (DANGEROUS)

```typescript
// Comment out or delete table definition
// export const oldTable = sqliteTable("old_table", { ... })
```

**After modification**: ⚠️ **CRITICAL** → Follow workflow → Migration will contain `DROP TABLE` →
**VERIFY DATA BACKUP** → Test → Commit

---

## Anti-Patterns (NEVER DO THIS)

❌ **Running migrations manually**:

```bash
# WRONG - Do not do this
sqlite3 .wrangler/state/v3/d1/miniflare-D1DatabaseObject/db.sqlite < server/database/migrations/0001_migration.sql
```

❌ **Executing `pnpm db:generate` automatically**:

```typescript
// WRONG - Do not do this
await $`pnpm db:generate`
```

❌ **Editing migration files**:

```sql
-- WRONG - Do not manually edit generated migrations
ALTER TABLE speakers ADD COLUMN custom_field TEXT;
```

❌ **Committing schema without migration**:

```bash
# WRONG - Do not commit only schema
git add server/database/schema.ts
git commit -m "Update schema"
# Migration files not included!
```

## Why This Workflow Matters

- **CONSISTENCY**: Schema file is single source of truth
- **SAFETY**: Manual SQL execution creates schema drift
- **AUDITABILITY**: All changes version-controlled
- **REVERSIBILITY**: Drizzle migrations support rollback
- **TYPE SAFETY**: TypeScript types inferred from schema

## References

- Database patterns: `.agents/database-patterns.md`
- Drizzle ORM documentation: Official Drizzle docs (Context7)
- Schema file: `server/database/schema.ts`
- Migrations directory: `server/database/migrations/`
