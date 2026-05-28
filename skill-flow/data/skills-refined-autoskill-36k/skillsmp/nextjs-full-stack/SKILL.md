---
name: nextjs-full-stack
description: App Router, API routes, Server Actions, auth, and deployment patterns.
---

# Next.js Full Stack Patterns

## When to use this skill
- Building features in Next.js (App Router).
- Creating API endpoints (Route Handlers).
- Implementing Server Actions for mutations.

## 1. App Router Structure
- **Colocation**: Keep related files (helpers, components, styles) inside the route segment folder unless they are truly shared.
- **Pages**: `page.tsx` should remain light; import client/server components for the UI.
- **Layouts**: Use `layout.tsx` for shared UI (nav, unrelated to route params) and `template.tsx` if you need state reset on navigation.

## 2. Server Components (RSC)
- **Default**: All components are Server Components by default.
- **Data Fetching**: Fetch data directly in RSCs (async/await). No `useEffect` needed.
- **Secrets**: Server components can safely access `process.env` secrets.

## 3. Server Actions
- **Mutations**: Use Server Actions (`'use server'`) for form submissions and simple mutations.
- **Validation**: Validate inputs (Zod) inside the action before processing.
- **Revalidation**: Use `revalidatePath` or `revalidateTag` to update cache after mutation.

## 4. Middleware
- **Auth**: Use middleware for route protection (redirecting unauthenticated users).
- **Performance**: Keep middleware lightweight (Edge runtime compatible).
