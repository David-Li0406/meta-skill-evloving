---
name: supabase-development
description: Use this skill for comprehensive Supabase development, including database management, authentication, real-time features, and Edge Functions.
---

# Supabase Development

You are an expert in Supabase development, covering database design, authentication, real-time features, and Edge Functions.

## Core Principles

- Use the Supabase client for all database interactions.
- Implement Row Level Security (RLS) policies for data protection.
- Write secure, performant, and efficient code.
- Leverage Supabase's real-time capabilities when appropriate.
- Implement comprehensive error handling and loading states for data-fetching components.

## Database Design

### Schema Best Practices
- Use proper PostgreSQL types and constraints.
- Implement foreign key relationships.
- Create indexes for frequently queried columns.
- Use views for complex queries.
- Implement soft deletes where appropriate.
- Use migrations for schema changes.

### Row Level Security
- Always enable RLS on tables with user data.
- Write policies for SELECT, INSERT, UPDATE, DELETE.
- Test policies thoroughly before deployment.
- Use service role only for admin operations.

## Authentication

- Implement OAuth providers (Google, GitHub, etc.) and handle auth state changes reactively.
- Use JWT validation for API endpoints.
- Implement proper session management, including password reset and email verification.
- Handle auth state changes properly.

## Real-Time Features

- Use subscriptions for live data updates and implement presence for user online status.
- Handle connection state changes and optimize subscription filters for performance.
- Implement proper cleanup for subscriptions.

## Edge Functions

- Write functions in TypeScript/Deno and handle CORS properly.
- Implement proper error responses and use environment variables for secrets.
- Test locally before deployment.

## Storage

- Organize files in buckets by purpose and implement proper access policies.
- Use signed URLs for private files and handle file uploads with proper validation.

## Client Integration Patterns

### Next.js
- Use `@supabase/ssr` for server-side auth and implement middleware for protected routes.
- Handle data fetching with proper caching and use React Server Components where appropriate.

### SvelteKit
- Use `@supabase/auth-helpers-sveltekit` and implement hooks for auth handling.
- Leverage SSR features and use Svelte stores for state management.

## Performance

- Use connection pooling for high traffic and implement caching strategies.
- Optimize queries with proper indexes and use pagination for large datasets.

## Example Database Operations

### Run SQL Query
```sql
SELECT * FROM trades WHERE symbol = '<symbol>' ORDER BY created_at DESC LIMIT <limit>;
```

### Create Table
```sql
CREATE TABLE <table_name> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    strength NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Trading Platform Tables

| Table      | Purpose            |
|------------|--------------------|
| `users`    | User accounts       |
| `trades`   | Trade history       |
| `signals`  | Generated signals    |
| `positions`| Open positions      |
| `watchlists`| User watchlists    |