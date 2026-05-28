---
name: create-migration
description: Generate SQL migration files from natural language descriptions
allowed-tools: Bash, Read, Write, Glob
disable-model-invocation: true
argument-hint: [description of changes]
---

# Generate Database Migration

Create a new SQL migration file based on a natural language description.

## Usage

- `/devflow-create-migration add user preferences table`
- `/devflow-create-migration add email_verified column to users`
- `/devflow-create-migration create index on orders.customer_id`
- `/devflow-create-migration rename column name to full_name in users`

## Description

$ARGUMENTS

## Workflow Steps

### Step 1: Understand Current Schema

First, look at existing migrations to understand the current database schema:

```bash
devflow db status --env local --json
```

Read recent migration files to understand:
- Existing tables and their structure
- Naming conventions used (snake_case, etc.)
- Common patterns (timestamps, soft deletes, UUIDs vs integers)

Find migration files:
```
migrations/*.sql
supabase/migrations/*.sql
```

### Step 2: Analyze the Request

Parse the natural language description to determine:
- **Operation type**: CREATE TABLE, ALTER TABLE, CREATE INDEX, etc.
- **Target objects**: Which tables/columns are involved
- **Data types**: Infer appropriate types from context
- **Constraints**: NOT NULL, UNIQUE, FOREIGN KEY, etc.

### Step 3: Create Migration File

```bash
devflow db create <migration_name>
```

Use a descriptive snake_case name derived from the description:
- "add user preferences table" → `add_user_preferences_table`
- "add email_verified to users" → `add_email_verified_to_users`

### Step 4: Write Migration SQL

Write the migration file with:

1. **Header comment** explaining the change
2. **Up migration** (the change)
3. **Down migration** (commented, for reference)

Example structure:
```sql
-- Migration: Add user preferences table
-- Description: Creates a table for storing user preferences like theme and notifications

-- Up Migration
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'system',
    email_notifications BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- Down Migration (for rollback reference)
-- DROP TABLE IF EXISTS user_preferences;
```

### Step 5: Validate Migration

Show the user the generated SQL and ask for confirmation.

Check for common issues:
- Missing foreign key references
- Missing indexes on frequently queried columns
- Missing NOT NULL where appropriate
- Missing ON DELETE behavior for foreign keys

### Step 6: Test with Dry Run

```bash
devflow db migrate --env local --dry-run
```

## SQL Patterns to Follow

### Table Creation
```sql
CREATE TABLE table_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- or: id SERIAL PRIMARY KEY,

    -- Foreign keys
    related_id UUID NOT NULL REFERENCES other_table(id) ON DELETE CASCADE,

    -- Data columns
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',

    -- Timestamps (always include)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Adding Columns
```sql
ALTER TABLE table_name
ADD COLUMN column_name TYPE [NOT NULL] [DEFAULT value];
```

### Creating Indexes
```sql
-- Regular index
CREATE INDEX idx_table_column ON table_name(column_name);

-- Unique index
CREATE UNIQUE INDEX idx_table_column ON table_name(column_name);

-- Composite index
CREATE INDEX idx_table_col1_col2 ON table_name(col1, col2);
```

### Adding Constraints
```sql
ALTER TABLE table_name
ADD CONSTRAINT constraint_name UNIQUE (column_name);

ALTER TABLE table_name
ADD CONSTRAINT fk_name FOREIGN KEY (column_id) REFERENCES other_table(id);
```

## Naming Conventions

- **Tables**: plural, snake_case (`user_preferences`, `order_items`)
- **Columns**: singular, snake_case (`user_id`, `created_at`)
- **Indexes**: `idx_table_column` or `idx_table_col1_col2`
- **Foreign keys**: `fk_table_referenced_table`
- **Constraints**: `chk_table_description` or `uq_table_column`

## Common Mistakes to Avoid

1. Forgetting to add indexes on foreign key columns
2. Missing ON DELETE/ON UPDATE behavior
3. Using VARCHAR without length for variable strings
4. Forgetting created_at/updated_at timestamps
5. Not considering NULL vs NOT NULL carefully
6. Missing default values where appropriate
