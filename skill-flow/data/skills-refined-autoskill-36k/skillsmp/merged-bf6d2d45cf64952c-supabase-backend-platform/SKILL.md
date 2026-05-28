---
name: supabase-backend-platform
description: Use this skill when building full-stack applications with Supabase, an open-source Firebase alternative that provides PostgreSQL database, authentication, storage, real-time subscriptions, and edge functions.
---

# Supabase Backend Platform Skill

## When to Use This Skill

This skill should be triggered when:
- Working with Supabase database, authentication, storage, or real-time features.
- Building full-stack applications with PostgreSQL.
- Implementing user authentication and authorization.
- Working with Row Level Security (RLS).
- Building real-time features with subscriptions.
- Deploying Edge Functions (Deno).
- Using Supabase with frameworks like React, Next.js, Vue, or Flutter.

## Quick Start

1. Create a project on the Supabase console.
2. Install the Supabase client:
   ```bash
   npm install @supabase/supabase-js
   ```
3. Initialize the Supabase client:
   ```javascript
   import { createClient } from '@supabase/supabase-js'

   const supabase = createClient(
     process.env.NEXT_PUBLIC_SUPABASE_URL!,
     process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
   )
   ```

## Supabase Fundamentals

### What is Supabase?
Supabase is an open-source Firebase alternative built on:
- **Postgres Database**: Full SQL database with PostgREST API.
- **Authentication**: Built-in auth with multiple providers.
- **Storage**: File storage with image transformations.
- **Realtime**: WebSocket subscriptions to database changes.
- **Edge Functions**: Serverless functions on Deno runtime.
- **Row Level Security**: Postgres RLS for data access control.

## Database Operations

### Basic Queries
```javascript
// SELECT
const { data, error } = await supabase
  .from('posts')
  .select('*')

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
```

### Advanced Queries
```javascript
// SELECT with filters
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(10)

// Full-text search
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', 'search terms')
```

## Authentication

### User Management
```javascript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password'
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password'
})

// Sign out
await supabase.auth.signOut()

// Get current user
const { data: { user } } = await supabase.auth.getUser()
```

## Storage

### File Operations
```javascript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.png', file)

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('public/avatar1.png')

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar1.png')
```

## Realtime Subscriptions

### Database Changes
```javascript
// Subscribe to inserts
const channel = supabase
  .channel('posts-insert')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('New post:', payload.new)
    }
  )
  .subscribe()
```

## Edge Functions

### Create and Deploy Edge Functions
```bash
# Create function
supabase functions new my-function

# Deploy
supabase functions deploy my-function
```

### Invoke Edge Function
```javascript
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { name: 'John' }
})
```

## Row Level Security (RLS)

### RLS Policies
```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read their own posts
CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);
```

## Environment Variables

### Configuration
```bash
# Public (client-side)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Private (server-side)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Summary

Supabase provides a complete backend platform with:
- **Postgres Database** with REST and GraphQL APIs.
- **Built-in Authentication** with multiple providers.
- **Row Level Security** for granular access control.
- **File Storage** with image transformations.
- **Realtime Subscriptions** for live updates.
- **Edge Functions** for serverless compute.
- **Next.js Integration** with Server and Client Components.
- **TypeScript Support** with auto-generated types.

Use Supabase when a full-featured backend with the power of Postgres, built-in auth, and realtime capabilities is needed, all with excellent TypeScript and Next.js integration.