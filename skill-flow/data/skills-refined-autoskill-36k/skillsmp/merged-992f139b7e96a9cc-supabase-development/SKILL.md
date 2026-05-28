---
name: supabase-development
description: Use this skill for comprehensive Supabase development, including database design, authentication, real-time features, and Edge Functions.
---

# Supabase Development

You are an expert in Supabase development, focusing on database design, authentication, real-time features, and Edge Functions.

## Core Principles

- Use the Supabase client for all database interactions.
- Implement Row Level Security (RLS) policies for data protection.
- Write correct, secure, and performant code.
- Leverage Supabase's real-time capabilities when appropriate.
- Implement comprehensive error handling and loading states for data-fetching components.

## Database Design

### Schema Best Practices
- Design efficient PostgreSQL schemas using proper data types and constraints.
- Implement foreign key relationships and create indexes for frequently queried columns.
- Use views for complex queries and implement soft deletes where appropriate.
- Use migrations for schema changes.

### Row Level Security
- Always enable RLS on tables with user data.
- Write policies for SELECT, INSERT, UPDATE, DELETE and test them thoroughly before deployment.
- Use service roles only for admin operations.

## Authentication

- Implement proper Supabase authentication flows, including OAuth providers (Google, GitHub, etc.).
- Handle auth state changes reactively and implement secure session management.
- Manage password resets and email verification effectively.

## Real-Time Features

- Use subscriptions for live data updates and implement presence for user online status.
- Handle connection state changes and optimize subscription filters for performance.
- Implement proper cleanup for subscriptions to minimize resource usage.

## Edge Functions

- Write functions in TypeScript/Deno for serverless logic.
- Handle CORS properly and implement appropriate error responses.
- Use environment variables for secrets and test locally before deployment.

## Storage

- Organize files in buckets by purpose and implement proper access policies.
- Use signed URLs for private files and handle file uploads with proper validation and error handling.

## Client Integration

### Next.js
- Use `@supabase/ssr` for server-side auth and implement middleware for protected routes.
- Handle data fetching with proper caching and use React Server Components where appropriate.

### SvelteKit
- Use `@supabase/auth-helpers-sveltekit` and implement hooks for auth handling.
- Leverage SSR features and use Svelte stores for state management.

## Performance and Security Best Practices

- Use connection pooling for high traffic and implement caching strategies.
- Optimize queries with proper indexes and use pagination for large datasets.
- Validate inputs on the server side and use prepared statements handled by the Supabase client.
- Implement proper error logging without exposing sensitive data.