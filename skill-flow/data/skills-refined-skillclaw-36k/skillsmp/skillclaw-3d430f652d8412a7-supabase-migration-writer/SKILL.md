---
name: supabase-migration-writer
description: Use this skill when creating database migrations, adding or modifying tables, creating RPC functions, or writing rollback scripts for Supabase projects.
---

# Skill body

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
Example: `20250124120000_add_user_notes_table.sql`

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

## Usage Examples

### Example: Create New Table Migration
**User:** "Create a migration for user_notes table to store Bible study notes"

**Assistant:**
```sql
-- Migration: 20250124120000_add_user_notes_table.sql

-- Create user_notes table
CREATE TABLE IF NOT EXISTS public.user_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  verse_id UUID REFERENCES bible_schema.verses(id) ON DELETE CASCADE,
  osis TEXT,
  note_text TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  is_private BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add indexes for performance
CREATE INDEX idx_user_notes_user_id ON public.user_notes(user_id);
CREATE INDEX idx_user_notes_verse_id ON public.user_notes(verse_id);
CREATE INDEX idx_user_notes_created_at ON public.user_notes(created_at DESC);
CREATE INDEX idx_user_notes_tags ON public.user_notes USING GIN(tags);

-- Enable RLS
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can insert own notes"
ON public.user_notes
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own notes"
ON public.user_notes
FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own notes"
ON public.user_notes
FOR DELETE
TO authenticated
USING (user_id = auth.uid());

-- Trigger for updated_at
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.user_notes
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();

-- Comments for documentation
COMMENT ON TABLE public.user_notes IS 'Table to store user notes for Bible study';
```