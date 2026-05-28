---
title: Enable RLS on ALL Tables with Data
impact: CRITICAL
impactDescription: Without RLS, all data is publicly accessible via the API
tags: rls, security, policies, access-control
---

## Enable RLS on ALL Tables with Data

Supabase exposes your database via REST API. Without RLS enabled, anyone with your anon key can read/write all data.

**Incorrect (RLS disabled):**

```sql
-- ❌ Table without RLS - ALL data exposed publicly!
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    full_name TEXT,
    avatar_url TEXT
);

-- Anyone can:
-- - Read all profiles
-- - Create fake profiles
-- - Modify any profile
-- - Delete profiles
```

**Correct (RLS enabled with policies):**

```sql
-- ✓ Enable RLS on the table
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    full_name TEXT,
    avatar_url TEXT
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- ✓ Create specific policies
-- Users can view their own profile
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = user_id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
    ON profiles FOR INSERT
    WITH CHECK (auth.uid() = user_id);
```

**Default deny - no policy = no access:**

```sql
-- With RLS enabled and NO policies:
-- - auth.uid() requests: NO ACCESS
-- - anon requests: NO ACCESS
-- - service_role: FULL ACCESS (bypasses RLS)

-- This is secure by default!
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;
-- No policies needed if only accessed via service_role
```

**Check all tables have RLS:**

```sql
-- Find tables without RLS enabled
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND rowsecurity = false;
```

Reference: [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
