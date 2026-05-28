---
name: supabase
description: Supabase open-source Firebase alternative with PostgreSQL database, authentication, storage, real-time subscriptions, and edge functions
---

# Supabase Skill

Comprehensive assistance with Supabase development - the open-source Firebase alternative with PostgreSQL database, Auth, Storage, Realtime, and Edge Functions.

## When to Use This Skill

This skill should be triggered when:
- Working with Supabase database, auth, storage, or realtime
- Building full-stack applications with PostgreSQL
- Implementing user authentication and authorization
- Working with Row Level Security (RLS)
- Building real-time features with subscriptions
- Deploying Edge Functions (Deno)
- Using Supabase with React, Next.js, Vue, Flutter, etc.

## Quick Reference

### Initialize Supabase Client (JavaScript)

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

### Initialize for Server-Side (Next.js)

```javascript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}
```

### Authentication

```javascript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123'
})

// Sign in with email/password
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

// Sign in with OAuth (Google, GitHub, etc.)
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:3000/auth/callback'
  }
})

// Sign out
await supabase.auth.signOut()

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  console.log(event, session)
})
```

### Database Queries

```javascript
// SELECT
const { data, error } = await supabase
  .from('posts')
  .select('*')

// SELECT with relations
const { data, error } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    author:users(name, email)
  `)

// INSERT
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'Hello', content: 'World' })
  .select()

// UPDATE
const { data, error } = await supabase
  .from('posts')
  .update({ title: 'Updated' })
  .eq('id', 1)
  .select()

// DELETE
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', 1)

// UPSERT
const { data, error } = await supabase
  .from('posts')
  .upsert({ id: 1, title: 'Upserted' })
  .select()
```

### Query Filters

```javascript
// Equality
.eq('column', 'value')

// Not equal
.neq('column', 'value')

// Greater than / Less than
.gt('column', 10)
.lt('column', 100)
.gte('column', 10)
.lte('column', 100)

// Pattern matching
.like('column', '%pattern%')
.ilike('column', '%pattern%')  // case insensitive

// IN / NOT IN
.in('column', ['a', 'b', 'c'])

// IS NULL / IS NOT NULL
.is('column', null)
.not('column', 'is', null)

// Full text search
.textSearch('column', 'search terms')

// Ordering
.order('created_at', { ascending: false })

// Pagination
.range(0, 9)  // First 10 rows
.limit(10)
```

### Row Level Security (RLS)

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own posts
CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);

-- Allow users to insert their own posts
CREATE POLICY "Users can insert own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Allow users to update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id);

-- Allow users to delete their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = user_id);

-- Public read access
CREATE POLICY "Public read access"
ON posts FOR SELECT
TO anon
USING (true);
```

### Storage

```javascript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('user1/avatar.png', file)

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('user1/avatar.png')

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user1/avatar.png')

// Create signed URL (temporary access)
const { data, error } = await supabase.storage
  .from('private-bucket')
  .createSignedUrl('path/to/file.pdf', 3600) // 1 hour

// Delete file
const { error } = await supabase.storage
  .from('avatars')
  .remove(['user1/avatar.png'])

// List files
const { data, error } = await supabase.storage
  .from('avatars')
  .list('user1', { limit: 100 })
```

### Realtime Subscriptions

```javascript
// Subscribe to database changes
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()

// Subscribe to specific events
const channel = supabase
  .channel('posts-inserts')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => console.log('New post:', payload.new)
  )
  .subscribe()

// Broadcast (for presence/custom events)
const channel = supabase.channel('room1')

// Send message
channel.send({
  type: 'broadcast',
  event: 'cursor-pos',
  payload: { x: 100, y: 200 }
})

// Listen to broadcasts
channel.on('broadcast', { event: 'cursor-pos' }, (payload) => {
  console.log(payload)
})

// Presence (track who's online)
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({ user_id: 'user1', online_at: new Date() })
    }
  })

// Unsubscribe
supabase.removeChannel(channel)
```

### Edge Functions (Deno)

```typescript
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Get auth token from request
  const authHeader = req.headers.get('Authorization')!

  // Create Supabase client with user's auth
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    { global: { headers: { Authorization: authHeader } } }
  )

  // Get user
  const { data: { user } } = await supabase.auth.getUser()

  return new Response(
    JSON.stringify({ message: `Hello ${user?.email}!` }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

### Call Edge Function

```javascript
const { data, error } = await supabase.functions.invoke('hello', {
  body: { name: 'World' }
})
```

### RPC (Remote Procedure Calls)

```sql
-- Create a function in Postgres
CREATE OR REPLACE FUNCTION get_user_posts(user_id uuid)
RETURNS SETOF posts AS $$
  SELECT * FROM posts WHERE posts.user_id = $1;
$$ LANGUAGE sql;
```

```javascript
// Call from client
const { data, error } = await supabase
  .rpc('get_user_posts', { user_id: 'uuid-here' })
```

## Environment Variables

```bash
# Public (safe for client-side)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Private (server-side only)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## CLI Commands

```bash
# Initialize project
supabase init

# Start local development
supabase start

# Stop local development
supabase stop

# Link to remote project
supabase link --project-ref your-project-ref

# Push database migrations
supabase db push

# Pull remote schema
supabase db pull

# Create new migration
supabase migration new migration_name

# Generate TypeScript types
supabase gen types typescript --local > types/supabase.ts

# Deploy Edge Functions
supabase functions deploy function-name

# Serve Edge Functions locally
supabase functions serve
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **getting_started.md** - Quickstarts and tutorials (83 pages)
- **database.md** - PostgreSQL, tables, queries, extensions (192 pages)
- **auth.md** - Authentication, OAuth, SSO, MFA (176 pages)
- **storage.md** - File uploads, buckets, CDN (68 pages)
- **realtime.md** - Subscriptions, broadcast, presence (17 pages)
- **edge_functions.md** - Deno functions, deployment (51 pages)
- **ai_vectors.md** - pgvector, embeddings, semantic search (48 pages)
- **api.md** - REST API, Management API (241 pages)
- **cli.md** - Supabase CLI commands (3 pages)
- **self_hosting.md** - Docker, self-hosted setup (14 pages)

Use `view` to read specific reference files when detailed information is needed.

## Key Concepts

### Service Role Key vs Anon Key
- **Anon Key**: Safe for client-side, respects RLS policies
- **Service Role Key**: Bypasses RLS, server-side only, never expose to client

### Row Level Security (RLS)
- Enabled per-table with `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
- Policies define who can SELECT/INSERT/UPDATE/DELETE
- Use `auth.uid()` to get current user's ID in policies

### Realtime
- Enable on tables: Dashboard > Database > Replication
- Uses Postgres logical replication under the hood

## Resources

- **Dashboard**: https://supabase.com/dashboard
- **Documentation**: https://supabase.com/docs
- **GitHub**: https://github.com/supabase/supabase
- **Discord**: https://discord.supabase.com

## Notes

- This skill was automatically generated from 938 pages of official Supabase documentation
- Reference files contain detailed examples for each feature area
- Code examples use the latest Supabase JavaScript client (v2)
