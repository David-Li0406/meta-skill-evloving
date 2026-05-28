---
name: nextjs-app-router-development
description: Use this skill when building or reviewing Next.js applications with the App Router, focusing on Server and Client Components, data fetching, and routing patterns.
---

# Skill body

## When to Use

- Creating new pages or layouts in Next.js App Router
- Implementing Server and Client Component patterns
- Setting up data fetching with Server Components
- Building API route handlers
- Implementing navigation and routing
- Debugging Next.js-specific issues
- Working with dynamic routes and params
- Reviewing and refactoring Next.js frontend projects for production readiness

## Defaults

- Next.js App Router (`app/`)
- TypeScript
- Server Components by default; add `"use client"` only when needed
- CSS: Tailwind if already present; otherwise follow existing styling approach

## Workflow

1. **Identify Project Mode**
   - New app: decide between App Router vs Pages Router (prefer App Router unless constrained).
   - Existing app: follow current structure, conventions, and tooling.

2. **Establish App Structure (App Router)**
   - `app/layout.tsx`: global shell (providers, fonts, nav).
   - `app/page.tsx`: landing page.
   - Route groups for domains: `app/(dashboard)/...`, `app/(marketing)/...`.
   - Shared UI: `components/` (reusable), `app/**/_components/` (route-scoped).
   - Types/utilities: `lib/` (fetchers, helpers), `types/`.

3. **Server vs Client Boundaries**
   - Prefer Server Components for data loading and initial render.
   - Use Client Components for: event handlers, stateful UI, browser APIs, client-only libraries.
   - Keep props serializable across the boundary; avoid passing functions/classes.

4. **Data Fetching Patterns**
   - Prefer colocated server fetchers in `lib/` and call them from Server Components.
   - Use `fetch()` with Next caching semantics when appropriate.
   - Handle loading and errors with `loading.tsx` / `error.tsx` per route segment.

5. **Forms and Validation**
   - Use server actions when appropriate; otherwise route handlers (`app/api/...`) + client submit.
   - Validate on server; optionally mirror on client.

6. **Environment Variables & Config**
   - Document required env vars; use `process.env.X`.
   - Only expose public vars with `NEXT_PUBLIC_` prefix.

7. **Quality Gates**
   - Run `lint` and `typecheck` (and tests if present).
   - Ensure accessibility basics: labels, focus states, keyboard navigation.
   - Avoid breaking route segments/URLs; add redirects when changing paths.

## Critical Patterns

### Server vs Client Components (CRITICAL)

In Next.js App Router, components are **Server Components by default**.

**Server Components:**
- Default behavior (no directive needed)
- Render on server only
- Can be async for data fetching
- Cannot use React hooks (useState, useEffect, etc.)
- Cannot use browser APIs
- Better performance (smaller bundle size)

**Client Components:**
- Require `"use client"` directive at top of file
- Render on both server and client
- Can use React hooks (useState, useEffect, etc.)
- Can use browser APIs
- Required for interactivity

```typescript
// Server Component (default)
async function ServerPage() {
  const data = await fetchData(); // Can be async
  return <div>{data}</div>;
}

// Client Component
"use client";
import { useState } from "react";

function ClientComponent() {
  const [count, setCount] = useState(0); // Can use hooks
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Rule**: Use Server Components by default, only use Client Components when you need:
- React hooks (useState, useEffect, etc.)
- Event handlers (onClick, onChange, etc.)
- Browser APIs (window, localStorage, etc.)
- Third-party libraries that use hooks

### Async Server Components for Data Fetching

Server Components can be async, enabling direct data fetching:

```typescript
// ✅ Correct - async Server Component
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId);
  return <div>{user.name}</div>;
}

// ❌ Wrong - using useEffect in Server Component
function UserProfile({ userId }: { userId: string }) {
  // Incorrect usage
}
```