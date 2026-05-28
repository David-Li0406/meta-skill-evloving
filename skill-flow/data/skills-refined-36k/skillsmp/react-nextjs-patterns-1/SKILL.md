---
name: React & Next.js Patterns
description: Modern React 19 and Next.js 15 patterns for FrankX applications
version: 1.0.0
source: Adapted from vercel-labs/react-best-practices
---

# React & Next.js Patterns

## FrankX Stack

```
Framework: Next.js 15 (App Router)
React: 19 (with Server Components)
Styling: Tailwind CSS 4 + shadcn/ui
State: React hooks + Server Actions
Validation: Zod
Testing: Vitest + Playwright
```

## Server Components (Default)

In Next.js App Router, components are Server Components by default.

```tsx
// app/products/page.tsx - Server Component (default)
import { db } from '@/lib/db';

export default async function ProductsPage() {
  // Direct database access - no API needed
  const products = await db.product.findMany();

  return (
    <main>
      <h1>Products</h1>
      <ProductList products={products} />
    </main>
  );
}
```

**When to use Server Components:**
- Fetching data
- Accessing backend resources
- Keeping sensitive info server-side
- Large dependencies (keep off client bundle)

## Client Components

Add `'use client'` when you need interactivity:

```tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

**When to use Client Components:**
- Event handlers (onClick, onChange)
- useState, useEffect, useRef
- Browser APIs (localStorage, window)
- Third-party client libraries

## Component Composition Pattern

```tsx
// Server Component (page)
import { getUser } from '@/lib/auth';
import { UserProfile } from './UserProfile'; // Client

export default async function ProfilePage() {
  const user = await getUser(); // Server-side fetch

  return (
    <main>
      {/* Pass server data to client component */}
      <UserProfile initialData={user} />
    </main>
  );
}

// Client Component
'use client';

export function UserProfile({ initialData }: { initialData: User }) {
  const [user, setUser] = useState(initialData);
  // Client-side interactivity with server-fetched data
}
```

## Server Actions

Replace API routes for mutations:

```tsx
// app/actions/subscribe.ts
'use server';

import { z } from 'zod';
import { db } from '@/lib/db';

const schema = z.object({
  email: z.string().email(),
});

export async function subscribeAction(formData: FormData) {
  const parsed = schema.safeParse({
    email: formData.get('email'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  await db.subscriber.create({
    data: { email: parsed.data.email },
  });

  return { success: true };
}
```

```tsx
// app/components/SubscribeForm.tsx
'use client';

import { subscribeAction } from '@/app/actions/subscribe';
import { useActionState } from 'react';

export function SubscribeForm() {
  const [state, action, pending] = useActionState(subscribeAction, null);

  return (
    <form action={action}>
      <input name="email" type="email" disabled={pending} />
      <button type="submit" disabled={pending}>
        {pending ? 'Subscribing...' : 'Subscribe'}
      </button>
      {state?.error && <p className="text-red-500">{state.error.email}</p>}
      {state?.success && <p className="text-green-500">Subscribed!</p>}
    </form>
  );
}
```

## Data Fetching Patterns

### Parallel Fetching
```tsx
export default async function DashboardPage() {
  // Fetch in parallel, not waterfall
  const [user, posts, analytics] = await Promise.all([
    getUser(),
    getPosts(),
    getAnalytics(),
  ]);

  return <Dashboard user={user} posts={posts} analytics={analytics} />;
}
```

### Streaming with Suspense
```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <main>
      <h1>Dashboard</h1>

      {/* Fast content renders immediately */}
      <WelcomeMessage />

      {/* Slow content streams in */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics />
      </Suspense>

      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations />
      </Suspense>
    </main>
  );
}
```

### Caching and Revalidation
```tsx
// Fetch with cache control
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: {
      revalidate: 3600, // Revalidate every hour
      tags: ['products'], // For on-demand revalidation
    },
  });
  return res.json();
}

// On-demand revalidation (in Server Action)
import { revalidateTag } from 'next/cache';

export async function updateProduct() {
  await db.product.update(...);
  revalidateTag('products'); // Invalidate cache
}
```

## Error Handling

### Error Boundaries
```tsx
// app/products/error.tsx
'use client';

export default function ProductsError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="text-center py-10">
      <h2>Something went wrong!</h2>
      <p className="text-neutral-500">{error.message}</p>
      <button onClick={reset} className="mt-4 btn">
        Try again
      </button>
    </div>
  );
}
```

### Not Found
```tsx
// app/products/[id]/page.tsx
import { notFound } from 'next/navigation';

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.id);

  if (!product) {
    notFound(); // Renders not-found.tsx
  }

  return <ProductDetails product={product} />;
}
```

## Performance Patterns

### Dynamic Imports
```tsx
import dynamic from 'next/dynamic';

// Load heavy component only when needed
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Client-only
});
```

### Image Optimization
```tsx
import Image from 'next/image';

export function ProductImage({ src, alt }: Props) {
  return (
    <Image
      src={src}
      alt={alt}
      width={400}
      height={300}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
      priority={false} // true for above-fold images
    />
  );
}
```

### Metadata
```tsx
// app/products/[id]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id);

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      images: [product.image],
    },
  };
}
```

## FrankX-Specific Patterns

### Glassmorphic Server Component
```tsx
// Server component with glassmorphic styling
export async function FeaturedProducts() {
  const products = await getFeaturedProducts();

  return (
    <section className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-aurora-1 bg-clip-text text-transparent">
        Featured
      </h2>
      <div className="grid grid-cols-3 gap-6 mt-6">
        {products.map(p => <ProductCard key={p.id} product={p} />)}
      </div>
    </section>
  );
}
```

### Loading States
```tsx
// app/products/loading.tsx
export default function ProductsLoading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-white/10 rounded w-1/4 mb-6" />
      <div className="grid grid-cols-3 gap-6">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-64 bg-white/5 rounded-xl" />
        ))}
      </div>
    </div>
  );
}
```

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| `'use client'` at page level | Keep pages as Server Components |
| Fetching in useEffect | Fetch in Server Components |
| Props drilling through many levels | Use composition or context |
| Giant components | Extract into smaller pieces |
| Inline styles everywhere | Use Tailwind utilities |
| Ignoring loading/error states | Always handle both |

## When to Use This Skill

- Building new pages/features
- Refactoring class components
- Optimizing performance
- Code reviews for React/Next.js

## Related Skills

- `shadcn-ui-patterns` - Component implementation
- `test-driven-development` - Test components
- `webapp-testing` - E2E testing
