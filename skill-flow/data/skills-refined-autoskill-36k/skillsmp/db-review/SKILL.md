---
name: db-review
description: Review database schema normalization, indexing strategy, query patterns, migration safety, and column/enum usage for PostgreSQL/Drizzle. Use when adding tables, modifying schema, reviewing migrations, or auditing unused data.
---

# Database Review

Analyze database schema design, normalization, and query patterns for PostgreSQL/Drizzle.

## Scope

Review schema files and queries for:

### 1. Normalization Analysis
- First Normal Form (1NF): Atomic values, no repeating groups
- Second Normal Form (2NF): No partial dependencies on composite keys
- Third Normal Form (3NF): No transitive dependencies
- Identify intentional denormalization and validate reasoning

### 2. Schema Design
- Appropriate data types (varchar lengths, numeric precision)
- Proper use of PostgreSQL enums vs. lookup tables
- UUID vs. serial for primary keys (project uses UUIDs)
- Nullable columns that should have defaults
- Missing NOT NULL constraints
- Proper foreign key relationships

### 3. Indexing Strategy
- Missing indexes on foreign keys
- Missing indexes on frequently filtered columns
- Missing composite indexes for common query patterns
- Over-indexing (indexes that slow writes without read benefit)
- Missing partial indexes for soft-delete patterns (`WHERE deleted_at IS NULL`)

### 4. Soft Delete Consistency
- All core tables should have `deletedAt` timestamp (per CLAUDE.md)
- Queries consistently filter `WHERE deletedAt IS NULL`
- Cascade behavior on soft deletes

### 5. Relationship Patterns
- Verify relations in `lib/db/relations.ts` match schema
- Many-to-many join table design
- Proper ON DELETE/ON UPDATE behaviors
- Missing relationships that should exist

### 6. Query Patterns
- N+1 queries in `lib/queries/`
- Missing eager loading opportunities
- Inefficient joins
- Unbounded queries (missing LIMIT)

### 7. Migration Safety
- Migrations that could lock tables
- Backwards-incompatible changes
- Missing data migrations for schema changes

### 8. No Row Level Security (RLS) - CRITICAL

**This project NEVER uses RLS.** All access control is handled in the application layer.

**Flag as 🔴 CRITICAL if found:**
- `ENABLE ROW LEVEL SECURITY` in any migration
- `CREATE POLICY` statements in migrations
- `pgPolicy()` calls in `lib/db/schema.ts`
- Import of `pgPolicy` from `drizzle-orm/pg-core`
- Helper functions like `is_admin()` for RLS

**Why RLS is prohibited:**
- Application-layer access control is easier to test and debug
- RLS creates hidden complexity and hard-to-trace permission issues
- Supabase RLS requires `auth.uid()` which couples DB to auth provider
- All data access flows through permission-checked functions in `lib/auth/permissions.ts`

**If RLS is found:** Immediately flag and recommend removal. This is a blocking issue.

### 9. Column Usage Audit
**Goal:** Prevent storing data that isn't immediately being used. Every column should have a purpose.

**Exempt columns (standard audit fields):**
- `id` (primary key)
- `createdAt`, `created_at`
- `updatedAt`, `updated_at`
- `deletedAt`, `deleted_at`
- Foreign key columns (e.g., `userId`, `projectId`, `clientId`)

**For each non-exempt column, verify it is:**
- Used in a query (SELECT, WHERE, ORDER BY, GROUP BY) in `lib/queries/` or `lib/data/`
- OR displayed in a UI component (check `components/` and `app/`)
- OR used in API responses or server actions

**Flags:**
- 🔴 **UNUSED**: Column exists but no evidence of usage anywhere
- 🟡 **WRITE-ONLY**: Column is written to but never read/displayed
- 🟢 **ACTIVE**: Column is both written and read/displayed

### 10. Enum Value Usage Audit
**Goal:** Ensure all enum values are actively used. Unused enum values create confusion and maintenance burden.

**For each PostgreSQL enum type in the schema, verify:**
- All values are used in at least one of:
  - Query filters (WHERE status = 'VALUE')
  - UI rendering (status labels, colors, icons)
  - Business logic (switch statements, conditionals)
  - API responses or form options

**Flags:**
- 🔴 **UNUSED VALUE**: Enum value exists but has no usage
- 🟡 **DEPRECATED**: Value exists for historical data only (document if intentional)
- 🟢 **ACTIVE**: Value is actively used in queries and UI

**Document findings for each enum:**
```
Enum: taskStatus
Values: [BACKLOG, ON_DECK, IN_PROGRESS, IN_REVIEW, BLOCKED, DONE, ARCHIVED]
Usage Analysis:
- BACKLOG: ✅ Query filter in fetchBacklogTasks(), UI in board column
- ON_DECK: ✅ ...
```

## Output Format

For each finding:
```
[TYPE: NORMALIZATION|INDEXING|DESIGN|QUERY|MIGRATION|RLS_VIOLATION|UNUSED_COLUMN|UNUSED_ENUM]
Location: table/file reference
Issue: Brief description
Current State: What exists now
Recommendation: How to improve
Migration Required: Yes/No
```

For column/enum usage audit, include a summary table:
```
## Column Usage Summary

| Table | Column | Status | Evidence |
|-------|--------|--------|----------|
| tasks | priority | 🟢 ACTIVE | Used in TaskCard, fetchTasks WHERE clause |
| tasks | estimatedHours | 🔴 UNUSED | No usage found |
| leads | budget | 🟡 WRITE-ONLY | Set in intake webhook, never displayed |

## Enum Usage Summary

| Enum | Value | Status | Evidence |
|------|-------|--------|----------|
| taskStatus | BACKLOG | 🟢 ACTIVE | Board column, query filter |
| leadStatus | UNQUALIFIED | 🔴 UNUSED | No UI or query usage found |
```

## Actions

1. Read `lib/db/schema.ts` and `lib/db/relations.ts`
2. **Check for RLS violations** - search for `pgPolicy`, `ENABLE ROW LEVEL SECURITY`, `CREATE POLICY`
3. Analyze recent migrations in `drizzle/migrations/`
4. Review query patterns in `lib/queries/`
5. Check for missing indexes using common query patterns
6. Validate soft-delete consistency
7. **Column usage audit:**
   - Extract all column names from schema tables
   - For each non-exempt column, search for usage in:
     - `lib/queries/` (Drizzle query builders)
     - `lib/data/` (data layer functions)
     - `components/` (UI rendering)
     - `app/` (pages, server actions, API routes)
   - Flag columns with no evidence of read usage
8. **Enum value audit:**
   - Extract all PostgreSQL enum definitions from schema
   - For each enum value, search for usage in:
     - Query filters and conditions
     - UI components (labels, colors, status badges)
     - Business logic files
     - Constants/config files (e.g., `lib/projects/task-status.ts`)
   - Flag values with no evidence of usage

## Post-Review

Generate:
- Schema diagram recommendations
- Index creation SQL statements
- Migration plan for improvements
- Risk assessment for proposed changes
- **Column cleanup recommendations:** Migration SQL to drop unused columns
- **Enum cleanup recommendations:** Migration SQL to remove unused enum values (with data migration plan if values exist in historical data)
