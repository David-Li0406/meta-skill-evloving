---
name: nextjs-patterns
description: "Next.js App Router patterns, server actions, caching, and routing. Use when working with Next.js 14+ features."
---

# Next.js Patterns

## Overview

Decision guide for Next.js App Router patterns focusing on data fetching, caching, and server/client architecture.

## Data Fetching Strategy

### Decision Flow

```
Need data?
  ├─ Server Component → fetch() directly (default)
  ├─ Client interactivity needed → Server Action
  ├─ External API from client → Route Handler
  └─ Real-time updates → Route Handler + streaming
```

### Server Component Fetching

```typescript
// app/users/page.tsx - Server component (default)
async function UsersPage() {
  // Direct async - no useEffect needed
  const users = await db.user.findMany();

  // Parallel fetching
  const [users, stats] = await Promise.all([
    db.user.findMany(),
    db.stats.get(),
  ]);

  return <UserList users={users} />;
}
```

### Server Actions

```typescript
// actions/user.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const data = Object.fromEntries(formData);
  await db.user.create({ data });
  revalidatePath('/users');
}

// Usage in component
<form action={createUser}>
  <input name="email" />
  <button type="submit">Create</button>
</form>
```

## Caching Strategy

| Scenario | Cache Strategy | Implementation |
|----------|---------------|----------------|
| Static data | Full cache | Default behavior |
| User-specific | No store | `cache: 'no-store'` |
| Periodic refresh | Time-based | `revalidate: 3600` |
| On-demand | Tag-based | `revalidateTag('users')` |

```typescript
// Time-based revalidation
const data = await fetch(url, { next: { revalidate: 3600 } });

// Tag-based revalidation
const data = await fetch(url, { next: { tags: ['users'] } });

// In server action
revalidateTag('users');
revalidatePath('/users');
```

## Route Organization

```
app/
├── (marketing)/          # Route group (no URL segment)
│   ├── page.tsx          # /
│   └── about/page.tsx    # /about
├── (app)/
│   ├── layout.tsx        # Shared app layout
│   └── dashboard/
│       ├── page.tsx      # /dashboard
│       ├── loading.tsx   # Loading UI
│       └── error.tsx     # Error boundary
├── api/
│   └── users/
│       └── route.ts      # /api/users
└── @modal/               # Parallel route for modals
    └── (.)photo/[id]/    # Intercepting route
```

## Loading & Error Patterns

```typescript
// loading.tsx - Automatic Suspense boundary
export default function Loading() {
  return <Skeleton />;
}

// error.tsx - Must be client component
'use client';
export default function Error({ error, reset }: {
  error: Error;
  reset: () => void
}) {
  return (
    <div>
      <p>Something went wrong</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// not-found.tsx - Custom 404
export default function NotFound() {
  return <p>Page not found</p>;
}
```

## Middleware Patterns

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get('token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Client-side fetch in Server Component | Defeats SSR | Use async/await directly |
| `'use client'` on layout | Makes all children client | Push client boundary down |
| Dynamic `params` without `generateStaticParams` | Slow builds | Define static params |
| Fetch in useEffect | Race conditions, waterfalls | Server component or action |
| Ignoring cache defaults | Over-fetching | Understand cache behavior |

## Route Handlers

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

## Red Flags

- `router.push` for form submissions (use server actions)
- Fetching same data in parent and child (lift up)
- `revalidate: 0` everywhere (understand caching first)
- Route handlers for what server actions can do
- `dynamic = 'force-dynamic'` without justification

## Quick Reference

```typescript
// Generate metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return { title: product.name };
}

// Static params for dynamic routes
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}

// Streaming with Suspense
<Suspense fallback={<Loading />}>
  <SlowComponent />
</Suspense>
```
