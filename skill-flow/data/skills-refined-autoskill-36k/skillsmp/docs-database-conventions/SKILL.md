---
name: docs-database-conventions
description: Use this skill when creating or modifying database schema, writing migrations, or updating docs/03_database.md. This ensures consistent naming conventions and proper documentation workflow.
---

# Database Naming Conventions Skill

Use this skill when creating or modifying database schema, writing migrations, or updating docs/03_database.md. This ensures consistent naming conventions and proper documentation workflow.

## When to Use

- Creating new database tables or columns
- Writing Supabase migration files
- Updating docs/03_database.md
- Creating PostgreSQL functions

## Table Prefix Rules

Strictly adhere to the following table prefixes:

| Prefix | Type | Description | Example |
|--------|------|-------------|---------|
| `m_` | Master tables | Basic entities, rarely deleted | `m_companies`, `m_children` |
| `r_` | Record tables | Daily transactional data | `r_activity`, `r_observation` |
| `s_` | Setting tables | Configuration and patterns | `s_attendance_schedule` |
| `h_` | History/Log tables | Audit logs, append-only | `h_login`, `h_attendance` |
| `_` | Intermediate tables | Many-to-many relationships | `_user_facility` |
| `tmp_` | Temporary tables | Work tables | `tmp_import` |

## Column Naming Rules

| Type | Convention | Example |
|------|------------|---------|
| Primary Key | `id` | `id` (UUID recommended) |
| Foreign Key | `{singular_table_name}_id` | `child_id`, NOT `children_id` |
| Timestamps | `created_at`, `updated_at`, `deleted_at` | For soft deletes |
| Booleans | `is_{state}`, `has_{attribute}` | `is_active`, `has_permission` |
| Date/Time | `{action}_at` (timestamp), `{period}_date` (date only) | `logged_in_at`, `birth_date` |

## PostgreSQL Function Rules

- Use snake_case naming (e.g., `calculate_grade`)
- Add descriptive comments explaining purpose and usage
- Use `SECURITY DEFINER` for functions that need elevated privileges
- Set `search_path = public` for security
- Grant appropriate permissions (`authenticated`, `service_role`)
- Document in `docs/03_database.md` with usage examples

### Common Function Naming Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| `calculate_*` | Calculation/computation functions | `calculate_grade` |
| `*_hook` | Supabase trigger hooks | `custom_access_token_hook` |
| `get_*` | Data retrieval functions | `get_user_facilities` |
| `update_*` | Data modification functions | `update_user_role` |

### Function Template

```sql
CREATE OR REPLACE FUNCTION public.function_name(param1 type, param2 type)
RETURNS return_type
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  -- Function logic here
END;
$$;

-- Add descriptive comment
COMMENT ON FUNCTION public.function_name IS 'Description of what the function does';

-- Grant permissions
GRANT EXECUTE ON FUNCTION public.function_name TO authenticated;
GRANT EXECUTE ON FUNCTION public.function_name TO service_role;
```

## Database Schema Change Workflow

**CRITICAL**: When creating or modifying database schema, you MUST follow this workflow:

### Step 1: Create Migration File

Create a migration file in `supabase/migrations/` with sequential numbering:

```bash
# File naming convention
supabase/migrations/NNN_description.sql
# Example: supabase/migrations/015_add_notification_table.sql
```

### Step 2: Update Documentation

Update `docs/03_database.md` with:
- New tables in the appropriate section (Master/Record/Setting/History/Intermediate)
- New columns with descriptions
- New PostgreSQL functions with usage examples
- New ENUM types

### Step 3: Test the Migration

```bash
# Option 1: Reset database with all migrations
supabase db reset

# Option 2: Apply specific migration
supabase migration up
```

### Step 4: Commit Changes Together

Always commit the migration file and documentation update together to maintain consistency.

### Step 5: Document Setup Instructions

If manual configuration is required (e.g., Supabase Hooks, Dashboard settings), add setup instructions to the relevant documentation.

## Example: Adding a New Table

### 1. Migration File

```sql
-- supabase/migrations/016_create_notifications_table.sql

CREATE TABLE IF NOT EXISTS m_notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES m_users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);

-- Create index for common queries
CREATE INDEX idx_notifications_user_id ON m_notifications(user_id);
CREATE INDEX idx_notifications_is_read ON m_notifications(is_read) WHERE deleted_at IS NULL;

-- Enable RLS
ALTER TABLE m_notifications ENABLE ROW LEVEL SECURITY;

-- RLS Policy
CREATE POLICY "Users can view their own notifications"
  ON m_notifications FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());
```

### 2. Documentation Update

Add to `docs/03_database.md` in the appropriate section:

```markdown
### m_notifications (Master Table)
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to m_users |
| title | TEXT | Notification title |
| message | TEXT | Notification content |
| is_read | BOOLEAN | Read status |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Update timestamp |
| deleted_at | TIMESTAMPTZ | Soft delete timestamp |
```

## Checklist Before Committing

- [ ] Table prefix follows convention (`m_`, `r_`, `s_`, `h_`, `_`, `tmp_`)
- [ ] Column names follow conventions (singular FK names, proper timestamp naming)
- [ ] Migration file created in `supabase/migrations/`
- [ ] `docs/03_database.md` updated with new schema
- [ ] RLS policies defined for new tables
- [ ] Indexes created for common query patterns
- [ ] PostgreSQL functions have comments and proper permissions
