---
name: rls-policy-validator
description: Use this skill when creating or validating Row Level Security (RLS) policies in the KR92 Bible Voice Supabase database to ensure user data protection and identify security gaps.
---

# RLS Policy Validator

## Context Files (Read First)

For tables and security patterns, read from `Docs/context/`:
- `Docs/context/db-schema-short.md` - Table structures
- `Docs/context/supabase-map.md` - Access matrix

## Capabilities
- Review and suggest RLS policies for new tables
- Validate that user data is properly protected
- Check admin role requirements
- Identify security gaps in database access
- Generate secure policy templates

## Core Principles

### 1. User Data Protection
All user-specific data MUST be protected by RLS policies that check `auth.uid()`.

### 2. Public Bible Data
Bible text, lexicons, and reference data should be publicly readable.

### 3. Admin Access
Admin operations require role checks via `has_role()` function.

### 4. Security Definer
Privileged operations use `SECURITY DEFINER` functions with role checks.

## Usage Examples

### Example 1: Create RLS Policy for New User Table
**User:** "I created a new table `user_notes` for Bible study notes. Add RLS policies."

**Assistant:**
```sql
-- Enable RLS
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view only their own notes
CREATE POLICY "Users can view own notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- Policy: Users can insert their own notes
CREATE POLICY "Users can insert own notes"
ON public.user_notes
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

-- Policy: Users can update their own notes
CREATE POLICY "Users can update own notes"
ON public.user_notes
FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

-- Policy: Users can delete their own notes
CREATE POLICY "Users can delete own notes"
ON public.user_notes
FOR DELETE
TO authenticated
USING (user_id = auth.uid());

-- Policy: Admins can view all notes
CREATE POLICY "Admins can view all notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

### Example 2: Validate Existing Policies
**User:** "Check if my bookmarks table is secure."

**Assistant:** Let me review the RLS policies:

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND tablename = 'bookmarks';

-- List existing policies
SELECT * FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'bookmarks';
```