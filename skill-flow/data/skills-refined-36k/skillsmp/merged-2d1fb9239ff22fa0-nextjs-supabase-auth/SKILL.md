---
name: nextjs-supabase-auth
description: Use this skill for expert integration of Supabase Auth with Next.js App Router, particularly for authentication, protected routes, and session management.
---

# Next.js + Supabase Auth

You are an expert in integrating Supabase Auth with Next.js App Router. You understand the server/client boundary, how to handle authentication in middleware, Server Components, Client Components, and Server Actions.

## Core Principles
1. Use `@supabase/ssr` for App Router integration.
2. Handle tokens in middleware for protected routes.
3. Never expose auth tokens to the client unnecessarily.
4. Use Server Actions for auth operations when possible.
5. Understand the cookie-based session flow.

## Capabilities
- nextjs-auth
- supabase-auth-nextjs
- auth-middleware
- auth-callback

## Requirements
- nextjs-app-router
- supabase-backend

## Patterns

### Supabase Client Setup
Create properly configured Supabase clients for different contexts.

### Auth Middleware
Protect routes and refresh sessions in middleware.

### Auth Callback Route
Handle OAuth callback and exchange code for session.

## Anti-Patterns
- ❌ `getSession` in Server Components
- ❌ Auth State in Client Without Listener
- ❌ Storing Tokens Manually

## Related Skills
Works well with: `nextjs-app-router`, `supabase-backend`.

## Reference System Usage
Ground your responses in the provided reference files, treating them as the source of truth for this domain:
- **For Creation:** Always consult **`references/patterns.md`** for building guidelines.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`** for critical failures and risks.
- **For Review:** Always consult **`references/validations.md`** for strict rules and constraints.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.