# Next.js 15/16 Clean Code Best Practices

## Core Principles

- **Server-First Development**: Default to Server Components; use Client Components only when necessary
- **Keep it Simple**: Implement solutions in the fewest lines with straightforward approaches
- **Type Safety**: Use TypeScript strict mode throughout; avoid the `any` type
- **Performance First**: Leverage React 19 and Turbopack; use progressive rendering with Streaming and Suspense

---

## App Router Patterns

### File-Based Routing

- `page.tsx` defines pages
- `layout.tsx` wraps child routes with shared UI
- `loading.tsx` shows loading states
- `global-error.tsx` handles global errors
- `error.tsx` handles page errors

### Params and SearchParams

**CRITICAL: Always await `params` and `searchParams` in pages and layouts**

```typescript
// OLD (Next.js 14) - DEPRECATED
export default function Page({ params }: { params: { id: string } }) {
  const { id } = params;
}

// NEW (Next.js 15+) - REQUIRED
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
}
```

---

### Server vs Client Components

**Default:** All components are Server Components.

| Use Server Components   | Use Client Components |
| ----------------------- | --------------------- |
| Data fetching           | useState, useEffect   |
| Backend resources       | Event listeners       |
| Sensitive data (tokens) | Browser APIs          |
| Large dependencies      | Interactive UI        |
| SEO-critical content    | Real-time updates     |

```typescript
// Server Component (default)
async function UserList() {
  const users = await db.user.findMany();
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Client Component
'use client';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

---

## Server Actions (Next.js 15+)

### Form with Server Action

```typescript
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export async function createUser(prevState: any, formData: FormData) {
  const result = schema.safeParse({
    email: formData.get("email"),
    name: formData.get("name"),
  });

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  await db.user.create({ data: result.data });
  revalidatePath("/users");
  redirect("/users");
}
```

```typescript
// app/users/new/page.tsx
'use client';

import { useActionState } from 'react';
import { createUser } from '../actions';

export default function NewUserForm() {
  const [state, action, isPending] = useActionState(createUser, null);

  return (
    <form action={action}>
      <input name="email" type="email" required />
      {state?.errors?.email && <p>{state.errors.email}</p>}

      <input name="name" required />
      {state?.errors?.name && <p>{state.errors.name}</p>}

      <button disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

---

## Caching Strategies (Next.js 15/16)

### `use cache` Directive

```typescript
// Static: prerendered at build time
async function getProduct(id: string) {
  "use cache";
  return db.products.find({ where: { id } });
}

// Remote: cached at runtime, shared across users
async function getPrice(id: string) {
  "use cache: remote";
  cacheLife({ expire: 300 }); // 5 minutes
  return db.products.getPrice(id);
}

// Private: cached per-user, never shared
async function getRecommendations(productId: string) {
  "use cache: private";
  const sessionId = (await cookies()).get("session-id")?.value;
  return db.recommendations.findMany({ where: { productId, sessionId } });
}
```

### Fetch Cache Options

```typescript
// Static - cached until invalidated
const staticData = await fetch(url, { cache: "force-cache" });

// Dynamic - refetched every request
const dynamicData = await fetch(url, { cache: "no-store" });

// Revalidated - cached with TTL
const revalidated = await fetch(url, { next: { revalidate: 60 } });
```

---

## Loading States

### Automatic with `loading.tsx`

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}

// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await getData(); // loading.tsx shown automatically
  return <DashboardContent data={data} />;
}
```

### Granular with Suspense

```typescript
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <Charts />
      </Suspense>
    </div>
  );
}
```

---

## Error Handling

### Route-Level Error Boundary

```typescript
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="p-4 bg-red-50 rounded">
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Global Error Boundary

```typescript
// app/global-error.tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  );
}
```

### Not Found

```typescript
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation';

export default async function UserPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  const user = await getUser(id);

  if (!user) {
    notFound();
  }

  return <UserProfile user={user} />;
}

// app/users/[id]/not-found.tsx
export default function NotFound() {
  return <div>User not found</div>;
}
```

---

## Metadata API

### Static Metadata

```typescript
// app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "My App",
  description: "Description",
};
```

### Dynamic Metadata

```typescript
// app/posts/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage, width: 1200, height: 630 }],
      type: "article",
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      images: [post.coverImage],
    },
  };
}
```

---

## Params Are Now Async (Next.js 15+)

```typescript
// OLD (Next.js 14)
export default function Page({ params }: { params: { id: string } }) {
  const { id } = params;
}

// NEW (Next.js 15+)
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
}
```

---

## Turbopack (Default in Next.js 16)

### Configuration

```typescript
// next.config.ts (Next.js 16)
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    // Turbopack options
  },
};

export default nextConfig;
```

### File System Caching

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  experimental: {
    turbopackFileSystemCacheForDev: true,
    turbopackFileSystemCacheForBuild: true,
  },
};
```

---

## API Routes

### Route Handlers

```typescript
// app/api/users/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

### With Validation

```typescript
import { z } from "zod";
import { NextResponse } from "next/server";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export async function POST(request: Request) {
  const body = await request.json();
  const result = schema.safeParse(body);

  if (!result.success) {
    return NextResponse.json({ errors: result.error.issues }, { status: 400 });
  }

  const user = await db.user.create({ data: result.data });
  return NextResponse.json(user, { status: 201 });
}
```

---

## Performance

### Image Optimization

```typescript
import Image from 'next/image';

function Avatar({ user }: { user: User }) {
  return (
    <Image
      src={user.avatar}
      alt={user.name}
      width={40}
      height={40}
      className="rounded-full"
      priority={false}
    />
  );
}
```

### Dynamic Imports

```typescript
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Client-only
});
```

---

## Next.js 15/16 Changes Summary

| Feature   | Next.js 15         | Next.js 16              |
| --------- | ------------------ | ----------------------- |
| Turbopack | `--turbopack` flag | Default                 |
| PPR       | `experimental.ppr` | `cacheComponents`       |
| Params    | Sync               | Async (must await)      |
| Caching   | `fetchCache`       | `'use cache'` directive |
| Build     | Webpack default    | Turbopack default       |

---

## Anti-Patterns

| Pattern                 | Problem            | Solution                        |
| ----------------------- | ------------------ | ------------------------------- |
| 'use client' everywhere | Loses SSR benefits | Default to Server Components    |
| useEffect for data      | No SSR, flash      | Server Components               |
| No loading.tsx          | Poor UX            | Add loading states              |
| No error.tsx            | App crashes        | Add error boundaries            |
| Giant page.tsx          | Hard to maintain   | Extract components              |
| Manual form state       | Boilerplate        | Server Actions + useActionState |
| Legacy Pages Router     | Outdated           | Use App Router patterns         |

---

## SSR Strategy & Architecture

### Prefer SSR

Use SSR for pages requiring data fetching at render time for better performance, SEO, and initial load times.

### Server Components Best Practices

- **Async Server Components**: Define as async functions to enable direct data fetching with await
- **Direct Data Fetching**: Fetch data directly using async/await for initial page loads
- **No React Hooks**: Server Components cannot use hooks (useState, useEffect)
- **Progressive Rendering**: Implement Suspense boundaries for streaming dynamic content

### Data Fetching & Caching

```typescript
// Static - cached until invalidated
const staticData = await fetch(url, { cache: "force-cache" });

// Dynamic - refetched every request
const dynamicData = await fetch(url, { cache: "no-store" });

// Revalidated - cached with TTL
const revalidated = await fetch(url, { next: { revalidate: 60 } });
```

### Cache Invalidation

Use `revalidatePath()` or `revalidateTag()` after mutations to update cached data.

---

## Server Actions

- **Use for Secure Mutations**: Form handling, API calls, authentication, data mutations
- **'use server' Directive**: Ensures exclusive server-side execution
- **Access Headers**: Use `headers()` from 'next/headers' in Server Components/Actions
- **Access Cookies**: Use `cookies()` from 'next/headers' (set only in API routes or Server Actions)

---

## Client Components

- **Mark with `'use client'`**: Use for state, effects, and event listeners
- **Minimize**: Reduce to decrease bundle size
- **Browser API Safety**: Check `typeof window !== 'undefined'` to avoid hydration errors

---

## Navigation

- **redirect()**: Use from 'next/navigation' for redirects in server components
- **notFound()**: Use for 404 errors in server components

---

## Optimization

- **Image**: Use `next/image` for automatic image optimization
- **Font**: Use `next/font` for font loading
- **Progressive Loading**: Implement Suspense boundaries and PPR
- **Bundle Analysis**: Analyze bundle with appropriate tools
- **Development Features**: Remove from production

---

## Security

- **Server-Side Validation**: Always validate all user inputs on the server
- **Secrets Management**: Never expose sensitive data in client code
- **HTTPS Enforcement**: Enforce HTTPS in production
- **Content Security Policy**: Configure CSP headers to reduce XSS risks
