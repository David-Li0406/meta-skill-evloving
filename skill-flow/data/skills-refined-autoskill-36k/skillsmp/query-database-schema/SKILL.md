---
name: query-database-schema
description: Inspects database schema and metadata (tables, columns, indexes, constraints, relationships). Use when exploring an unfamiliar database, writing joins, debugging query behavior, or documenting schema.
---

# Query Database Schema

## Quick Start

Use this skill to quickly answer: what tables exist, what columns/types they have, how tables relate, and what constraints/indexes affect query behavior.

## When to use this skill

- onboarding onto an unfamiliar database
- before writing joins, aggregations, or migrations
- when app behavior suggests bad assumptions (nullability, defaults, constraints)
- when documenting schema for teammates

Before running queries, collect:

- database engine (postgres/mysql/sqlite)
- database + schema name (if applicable)
- target tables (or suspected domain area)

## Common Database Queries

### PostgreSQL

**list schemas:**

```sql
SELECT schema_name
FROM information_schema.schemata
ORDER BY schema_name;
```

**List all tables:**

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

**Get table structure:**

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'your_table_name'
ORDER BY ordinal_position;
```

**list indexes (including uniqueness):**

```sql
SELECT
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'your_table_name'
ORDER BY indexname;
```

**list constraints (pk/unique/check/fk):**

```sql
SELECT
  tc.constraint_type,
  tc.constraint_name,
  kcu.column_name
FROM information_schema.table_constraints tc
LEFT JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
WHERE tc.table_schema = 'public'
  AND tc.table_name = 'your_table_name'
ORDER BY tc.constraint_type, tc.constraint_name, kcu.ordinal_position;
```

**Find foreign key relationships:**

```sql
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### MySQL

**list databases:**

```sql
SHOW DATABASES;
```

**list tables (current database):**

```sql
SHOW TABLES;
```

**Get table structure:**

```sql
DESCRIBE table_name;
-- or
SHOW COLUMNS FROM table_name;
```

**list indexes:**

```sql
SHOW INDEX FROM table_name;
```

**Find foreign key relationships:**

```sql
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE()
    AND REFERENCED_TABLE_NAME IS NOT NULL;
```

### SQLite

**List all tables:**

```sql
SELECT name FROM sqlite_master WHERE type='table';
```

**Get table structure:**

```sql
PRAGMA table_info(table_name);
```

**list indexes:**

```sql
PRAGMA index_list(table_name);
```

**inspect index columns:**

```sql
PRAGMA index_info(index_name);
```

**Find foreign key relationships:**

```sql
SELECT
    m.name AS table_name,
    p.*
FROM sqlite_master m
JOIN pragma_foreign_key_list(m.name) p
WHERE m.type = 'table';
```

## Workflow

1. identify engine + schema/db
2. list tables, then pick 1–3 candidate tables
3. inspect columns + constraints for each table
4. map relationships (fk), then validate join keys
5. check indexes on join keys + filter columns
6. document a minimal schema summary for the task at hand

## Best Practices

- scope queries to schema/db to avoid noise
- prefer `information_schema` for portable metadata; drop to engine-specific views for indexes/details
- confirm join keys are unique (or accept multiplicity) before aggregations
- check constraints + defaults to avoid incorrect assumptions in app code

## Output Format

When documenting schema findings, use this structure:

```markdown
## Database: [database_name]

### Tables

- `table_name` (description)
  - Columns: column1 (type), column2 (type)
  - Relationships: references `other_table.column`
  - Indexes: idx_name (columns, unique?)

### Key Relationships

- `table1.column` → `table2.column`
```
