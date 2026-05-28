---
name: supabase-migration-writer
description: Use this skill when creating and managing database migrations for the Supabase project, including adding tables, modifying schemas, creating RPC functions, and writing rollback scripts.
---

# Supabase Migration Writer

## Context Files (Read First)

For schema and Supabase layout, read from `Docs/context/`:
- `Docs/context/db-schema-short.md` - Database schema overview
- `Docs/context/supabase-map.md` - Edge Functions, migrations, access matrix

## Quick Reference

- **Project ID**: `iryqgmjauybluwnqhxbg`
- **Migrations**: `supabase/migrations/`
- **Edge Functions**: `supabase/functions/`

## Migration File Convention

```
supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

## Essential Patterns

### Create Table with RLS
```sql
CREATE TABLE IF NOT EXISTS public.table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_table_user_id ON public.table_name(user_id);

ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data"
ON public.table_name FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can insert own data"
ON public.table_name FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.table_name
FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();
```

### Add Column
```sql
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS new_column TEXT DEFAULT 'value';

COMMENT ON COLUMN public.table_name.new_column IS 'Description';
```

### Create RPC Function
```sql
CREATE OR REPLACE FUNCTION public.function_name(
  p_user_id UUID DEFAULT auth.uid(),
  p_limit INT DEFAULT 20
)
RETURNS TABLE (col1 UUID, col2 TEXT)
LANGUAGE sql STABLE SECURITY DEFINER
SET search_path TO 'public', 'bible_schema'
AS $$
  SELECT col1, col2
  FROM table_name
  WHERE user_id = p_user_id
  LIMIT p_limit;
$$;

GRANT EXECUTE ON FUNCTION public.function_name TO authenticated;
```

## Data Types Quick Reference

| Use Case | Type |
|----------|------|
| ID | `UUID DEFAULT gen_random_uuid()` |
| User ref | `UUID REFERENCES auth.users(id)` |
| Text | `TEXT` |
| Boolean | `BOOLEAN DEFAULT true` |
| Timestamp | `TIMESTAMPTZ DEFAULT now()` |
| Number | `INTEGER` |
| Decimal | `NUMERIC(10,2)` |
| JSON | `JSONB DEFAULT '{}'` |
| Array | `TEXT[] DEFAULT '{}'` |
| Enum | `TEXT CHECK (col IN ('a', 'b'))` |

## Migration Best Practices Checklist

- [ ] Use `IF NOT EXISTS` / `IF EXISTS`
- [ ] Add `created_at` and `updated_at` timestamps
- [ ] Enable RLS on all tables
- [ ] Add indexes for foreign keys and filtered columns
- [ ] Use `SECURITY DEFINER` for RPC functions
- [ ] Set `search_path` in functions
- [ ] Add `COMMENT ON` for documentation
- [ ] Create rollback script for complex changes
- [ ] **Update TypeScript types after migration** (see learnings)

## Testing Migrations

```bash
# Apply locally
supabase db push

# Reset and reapply all
supabase db reset
```

## Advanced PostgreSQL Features

For advanced PostgreSQL-specific guidance, you can leverage the **pg-aiguide plugin** with these specialized skills:

### Available PostgreSQL Skills

1. **`pg:design-postgres-tables`**
   - Comprehensive PostgreSQL-specific table design reference
   - Data types, indexing strategies, constraints
   - Performance patterns and best practices
   - Advanced features (partitioning, triggers, etc.)

2. **`pg:setup-timescaledb-hypertables`**
   - Design and set up TimescaleDB hypertables
   - Configure compression, retention policies
   - Set up continuous aggregates for time-series data
   - Optimal partition and chunk configuration

3. **`pg:find-hypertable-candidates`**
   - Analyze existing tables for TimescaleDB conversion
   - Identify time-series data patterns
   - Evaluate performance improvement opportunities

4. **`pg:migrate-postgres-tables-to-hypertables`**
   - Step-by-step migration to TimescaleDB
   - Zero-downtime migration strategies
   - Performance validation and optimization

### When to Use pg-aiguide

- **Complex indexing requirements** - Multi-column indexes, partial indexes, expression indexes
- **Time-series data** - Bible reading analytics, usage logs, AI usage tracking
- **Performance optimization** - Query planning, index selection, partition strategies
- **Advanced data types** - Arrays, JSONB, full-text search, geometric types
- **PostgreSQL-specific features** - CTEs, window functions, materialized views

## Related Documentation
- See `Docs/03-API.md` for current schema
- See `Docs/02-DESIGN.md` for architecture
- See `Docs/04-DEV-WORKFLOW.md` for deployment process