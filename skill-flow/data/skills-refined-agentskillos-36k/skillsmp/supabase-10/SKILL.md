---
name: supabase
description: >
  Implement Supabase database patterns for PhotoVault including RLS policies,
  TypeScript queries, and storage operations. Use when working with database
  schemas, Row Level Security, migrations, storage buckets, auth.uid() policies,
  or debugging empty query results. Includes PhotoVault table structure and
  client setup patterns.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\supabase-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/supabase-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/supabase-[task-name]-plan.md
   Write critique to: docs/claude/plans/supabase-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Supabase Integration

## Core Principles

### RLS First, Always

Row Level Security is not optional. Every table in the `public` schema MUST have RLS enabled.

```sql
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;
```

**Key insight:** Once RLS is enabled with no policies, the table is completely locked down. You then selectively grant access.

### Type Safety is Non-Negotiable

```bash
npx supabase gen types typescript --project-id <project-id> > src/types/supabase.ts
```

```typescript
import { createClient } from '@supabase/supabase-js'
import { Database } from '@/types/supabase'

const supabase = createClient<Database>(url, key)
```

### Understand Your Three Clients

| Client | When to Use | RLS Behavior |
|--------|-------------|--------------|
| **Browser Client** | Client components, user actions | Respects RLS based on auth.uid() |
| **Server Client** | Server components, API routes | Respects RLS based on auth.uid() |
| **Admin Client** | Webhooks, cron jobs, migrations | **Bypasses RLS entirely** |

**Never use the admin client for user-facing operations.**

## Anti-Patterns

### RLS Mistakes

**Not wrapping auth.uid() for performance**
```sql
-- WRONG: Calls auth.uid() for every row
CREATE POLICY "slow_policy" ON posts
FOR SELECT USING (auth.uid() = user_id);

-- RIGHT: Caches auth.uid() per statement
CREATE POLICY "fast_policy" ON posts
FOR SELECT USING ((SELECT auth.uid()) = user_id);
```

**Permissive policies without thinking**
```sql
-- WRONG: ALL authenticated users see ALL rows
CREATE POLICY "bad_policy" ON posts
FOR SELECT TO authenticated
USING (true);
```

### Query Mistakes

**Not handling join result types correctly**
```typescript
// WRONG: Assuming joins always return arrays
const client = gallery.clients[0]

// RIGHT: Check the type
const clientData = gallery.clients
const client = Array.isArray(clientData) ? clientData[0] : clientData
```

**Not using .single() or .maybeSingle() appropriately**
```typescript
// WRONG: Returns array when you expect one item
const { data } = await supabase.from('users').select().eq('id', id)

// RIGHT: Use .single() for guaranteed single row
const { data } = await supabase.from('users').select().eq('id', id).single()

// RIGHT: Use .maybeSingle() when row might not exist
const { data } = await supabase.from('users').select().eq('email', email).maybeSingle()
```

## RLS Policy Patterns

**Users own their data**
```sql
CREATE POLICY "users_own_data" ON user_data
FOR ALL TO authenticated
USING ((SELECT auth.uid()) = user_id)
WITH CHECK ((SELECT auth.uid()) = user_id);
```

**Photographer → Client relationship (PhotoVault pattern)**
```sql
CREATE POLICY "photographer_sees_clients" ON clients
FOR SELECT TO authenticated
USING (
  photographer_id IN (
    SELECT id FROM photographers
    WHERE user_id = (SELECT auth.uid())
  )
);

CREATE POLICY "client_own_data" ON clients
FOR SELECT TO authenticated
USING (user_id = (SELECT auth.uid()));
```

**Role-based access**
```sql
CREATE POLICY "admin_only" ON admin_settings
FOR ALL TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM user_profiles
    WHERE user_id = (SELECT auth.uid())
    AND role = 'admin'
  )
);
```

## TypeScript Query Patterns

**Fetch with joins**
```typescript
async function getGalleryWithDetails(galleryId: string) {
  const { data, error } = await supabase
    .from('photo_galleries')
    .select(`
      *,
      clients (id, name, email),
      gallery_photos (id, filename, thumbnail_url, original_url)
    `)
    .eq('id', galleryId)
    .single()

  if (error) throw error
  if (!data) return null

  const client = Array.isArray(data.clients)
    ? data.clients[0]
    : data.clients

  return { ...data, client, photos: data.gallery_photos ?? [] }
}
```

## PhotoVault Configuration

### Key Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `user_profiles` | Extended user data | `user_id`, `user_type`, `business_name` |
| `photo_galleries` | Gallery metadata | `photographer_id`, `client_id`, `status` |
| `gallery_photos` | Individual photos | `gallery_id`, `original_url`, `thumbnail_url` |
| `clients` | Client records | `photographer_id`, `user_id`, `email` |
| `commission_payments` | Payment tracking | `photographer_id`, `amount`, `status` |

### Client Setup

```typescript
// Browser client (client components)
import { createBrowserClient } from '@supabase/ssr'
import { Database } from '@/types/supabase'

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// Server client (server components, API routes)
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createServerSupabaseClient() {
  const cookieStore = await cookies()
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}

// Admin client (webhooks, cron - BYPASSES RLS)
import { createClient } from '@supabase/supabase-js'

export function createAdminClient() {
  return createClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )
}
```

### Known PhotoVault Gotchas

1. **Primary gallery table is `photo_galleries`** (not `galleries`)
2. **Join results:** Single relations return objects, not arrays - always check `Array.isArray()`
3. **Photo URLs:** Some photos may be missing `original_url` - fall back to `thumbnail_url`
4. **User types:** Stored in `user_profiles.user_type` as 'photographer', 'client', or 'admin'

## Debugging Checklist

1. Is RLS enabled? Check in Supabase Dashboard → Table → RLS toggle
2. Are there policies? Check Authentication → Policies
3. Is the user authenticated? Check `auth.uid()` is not null
4. Does the policy match? Test in SQL Editor with `SET ROLE authenticated`
5. Are you using the right client? Browser vs Server vs Admin
6. Check the Supabase logs for policy violations

**Test RLS in SQL Editor:**
```sql
SELECT set_config('request.jwt.claims', '{"sub": "user-uuid-here"}', true);
SET ROLE authenticated;
SELECT * FROM your_table;
RESET ROLE;
```
