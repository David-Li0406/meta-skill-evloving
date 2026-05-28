---
name: supabase-patterns
description: "Supabase client setup, Row Level Security (RLS), edge functions, and real-time. Use when working with Supabase database, auth, or edge functions."
---

# Supabase Patterns

## Overview

Decision guide for Supabase patterns focusing on client setup, RLS policies, and edge functions.

## Client Setup

### Server vs Browser Client

```typescript
// lib/supabase/server.ts - Server Component / Server Action
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookies) => cookies.forEach(c => cookieStore.set(c)),
      },
    }
  );
}

// lib/supabase/client.ts - Client Component
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### Decision Matrix

| Context | Client Type | Use Case |
|---------|-------------|----------|
| Server Component | Server | Data fetching |
| Server Action | Server | Mutations |
| Route Handler | Server | API routes |
| Client Component | Browser | Real-time, user interactions |
| Middleware | Server | Auth checks |

## Row Level Security (RLS)

### Essential Policies

```sql
-- Enable RLS (REQUIRED)
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users read own data"
ON todos FOR SELECT
USING (auth.uid() = user_id);

-- Users can only insert their own data
CREATE POLICY "Users insert own data"
ON todos FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can only update their own data
CREATE POLICY "Users update own data"
ON todos FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can only delete their own data
CREATE POLICY "Users delete own data"
ON todos FOR DELETE
USING (auth.uid() = user_id);
```

### Multi-Tenant RLS

```sql
-- Organization-based access
CREATE POLICY "Org members access"
ON documents FOR ALL
USING (
  org_id IN (
    SELECT org_id FROM org_members
    WHERE user_id = auth.uid()
  )
);

-- Role-based within org
CREATE POLICY "Admins can delete"
ON documents FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM org_members
    WHERE user_id = auth.uid()
    AND org_id = documents.org_id
    AND role = 'admin'
  )
);
```

## Query Patterns

```typescript
// Basic CRUD
const { data, error } = await supabase
  .from('todos')
  .select('*')
  .eq('user_id', userId)
  .order('created_at', { ascending: false });

// Joins (foreign key relationship)
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:users(name, avatar),
    comments(id, content)
  `);

// Upsert
await supabase
  .from('profiles')
  .upsert({ id: userId, name }, { onConflict: 'id' });

// Transaction-like (use RPC)
await supabase.rpc('transfer_funds', { from_id, to_id, amount });
```

## Edge Functions

```typescript
// supabase/functions/my-function/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  // Get auth header
  const authHeader = req.headers.get('Authorization')!;

  // Create client with user's JWT
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: authHeader } } }
  );

  // RLS applies automatically
  const { data } = await supabase.from('todos').select('*');

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  });
});
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| RLS disabled | Security vulnerability | Always enable RLS |
| Service role in browser | Bypasses RLS | Use anon key client-side |
| `SELECT *` without filters | Performance | Select specific columns |
| No error handling | Silent failures | Check `error` always |
| Auth in RLS without index | Slow queries | Index `user_id` columns |

```typescript
// BAD: Ignoring errors
const { data } = await supabase.from('todos').select('*');

// GOOD: Handle errors
const { data, error } = await supabase.from('todos').select('*');
if (error) throw new Error(error.message);
```

## Real-time Patterns

```typescript
// Subscribe to changes
const channel = supabase
  .channel('todos')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'todos' },
    (payload) => console.log(payload)
  )
  .subscribe();

// Cleanup
useEffect(() => {
  return () => { supabase.removeChannel(channel); };
}, []);
```

## Red Flags

- RLS not enabled on tables with user data
- Service role key exposed in client code
- Missing `auth.uid()` checks in policies
- No indexes on columns used in RLS policies
- Real-time subscriptions without cleanup

## Quick Reference

```sql
-- Check if RLS enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- View policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Helper function for org membership
CREATE FUNCTION is_org_member(org_id uuid)
RETURNS boolean AS $$
  SELECT EXISTS (
    SELECT 1 FROM org_members WHERE user_id = auth.uid() AND org_id = $1
  );
$$ LANGUAGE sql SECURITY DEFINER;
```
