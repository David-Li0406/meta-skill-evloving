---
name: supabase-migration-writer
description: Use this skill when creating and managing database migrations for the KR92 Bible Voice Supabase project, including adding tables, modifying schemas, creating RPC functions, and writing rollback scripts.
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

## Migration File Structure

### Naming Convention
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

## Migration Best Practices

1. **Use IF NOT EXISTS / IF EXISTS**
   ```sql
   CREATE TABLE IF NOT EXISTS table_name (...);
   DROP TABLE IF EXISTS table_name;
   ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name type;
   ```

2. **Add Timestamps**
   ```sql
   created_at TIMESTAMPTZ DEFAULT now(),
   updated_at TIMESTAMPTZ DEFAULT now()
   ```

3. **Foreign Key Constraints**
   ```sql
   user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE
   ```

4. **Indexes for Performance**
   ```sql
   CREATE INDEX idx_table_user_id ON table_name(user_id);
   ```

5. **Comments for Documentation**
   ```sql
   COMMENT ON TABLE table_name IS 'Description of table purpose';
   COMMENT ON COLUMN table_name.column_name IS 'Description of column';
   ```

6. **RLS Always**
   ```sql
   ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
   ```

7. **Updated At Trigger**
   ```sql
   CREATE TRIGGER set_updated_at
   BEFORE UPDATE ON table_name
   FOR EACH ROW
   EXECUTE FUNCTION public.handle_updated_at();
   ```

8. **Security Definer for Functions**
   ```sql
   CREATE FUNCTION function_name(...)
   LANGUAGE sql
   SECURITY DEFINER
   SET search_path TO 'public'
   AS $$...$$;
   ```

## Testing Migrations

### Local Testing
```bash
# Apply migration
supabase db push

# Reset and reapply
supabase db reset
```

## Documentation Updates

After creating migration, update:
1. `Docs/03-API.md` - Add new tables/functions
2. `Docs/02-DESIGN.md` - Update architecture if needed
3. `CLAUDE.MD` - Update schema reference if major change

## Advanced PostgreSQL Features

For advanced PostgreSQL-specific guidance, you can leverage the **pg-aiguide plugin** with these specialized skills:

### Available PostgreSQL Skills

1. **`pg:design-postgres-tables`**
2. **`pg:setup-timescaledb-hypertables`**
3. **`pg:find-hypertable-candidates`**
4. **`pg:migrate-postgres-tables-to-hypertables`**

### When to Use pg-aiguide

- **Complex indexing requirements**
- **Time-series data**
- **Performance optimization**
- **Advanced data types**
- **PostgreSQL-specific features**

## Related Documentation
- See `Docs/03-API.md` for current schema
- See `Docs/02-DESIGN.md` for architecture
- See `Docs/04-DEV-WORKFLOW.md` for deployment process