---
id: nextjs-app-router
name: "Next.js App Router"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Next.js App Router

## Overview

Next.js App Router is the modern routing system introduced in Next.js 13+, featuring React Server Components, nested layouts, streaming, and improved data fetching patterns. This methodology covers project structure, routing conventions, and best practices.

## When to Use

- New Next.js projects (Next.js 13+)
- Full-stack React applications
- Projects requiring SSR/SSG/ISR
- Applications needing SEO optimization
- Projects with complex nested layouts

## Key Principles

1. **Server Components by default** - Only use Client Components when needed
2. **Colocation** - Keep related files together in route segments
3. **Streaming** - Progressive rendering with Suspense
4. **Parallel routes** - Multiple pages in single layout
5. **Intercepting routes** - Modal patterns without navigation

## Best Practices

### Project Structure

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── loading.tsx             # Loading UI
├── error.tsx               # Error boundary
├── not-found.tsx           # 404 page
├── global-error.tsx        # Global error boundary
│
├── (marketing)/            # Route group (no URL impact)
│   ├── layout.tsx          # Marketing layout
│   ├── about/
│   │   └── page.tsx        # /about
│   └── contact/
│       └── page.tsx        # /contact
│
├── (auth)/                 # Auth route group
│   ├── layout.tsx          # Auth layout (centered)
│   ├── login/
│   │   └── page.tsx        # /login
│   └── register/
│       └── page.tsx        # /register
│
├── dashboard/
│   ├── layout.tsx          # Dashboard layout
│   ├── page.tsx            # /dashboard
│   ├── loading.tsx         # Dashboard loading
│   ├── settings/
│   │   └── page.tsx        # /dashboard/settings
│   └── [teamId]/           # Dynamic segment
│       ├── page.tsx        # /dashboard/[teamId]
│       └── members/
│           └── page.tsx    # /dashboard/[teamId]/members
│
├── api/                    # API routes
│   └── users/
│       └── route.ts        # /api/users
│
└── @modal/                 # Parallel route for modals
    └── (.)photo/[id]/
        └── page.tsx        # Intercepted modal
```

### Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '@/components/providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App',
  },
  description: 'A production Next.js application',
  metadataBase: new URL('https://example.com'),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
```

### Page Component (Server Component)

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { DashboardStats } from '@/components/dashboard/stats';
import { RecentActivity } from '@/components/dashboard/activity';
import { StatsLoading } from '@/components/dashboard/loading';

export const metadata = {
  title: 'Dashboard',
};

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session) {
    redirect('/login');
  }

  return (
    <div className="container py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      <Suspense fallback={<StatsLoading />}>
        <DashboardStats userId={session.user.id} />
      </Suspense>

      <Suspense fallback={<div>Loading activity...</div>}>
        <RecentActivity userId={session.user.id} />
      </Suspense>
    </div>
  );
}
```

### Dynamic Routes

```tsx
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation';
import { getUser } from '@/lib/api';

interface PageProps {
  params: { id: string };
}

// Generate static params for SSG
export async function generateStaticParams() {
  const users = await getUsers();
  return users.map((user) => ({ id: user.id }));
}

// Generate metadata dynamically
export async function generateMetadata({ params }: PageProps) {
  const user = await getUser(params.id);

  if (!user) {
    return { title: 'User Not Found' };
  }

  return {
    title: user.name,
    description: `Profile of ${user.name}`,
  };
}

export default async function UserPage({ params }: PageProps) {
  const user = await getUser(params.id);

  if (!user) {
    notFound();
  }

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Client Components

```tsx
// components/counter.tsx
'use client';  // Required for client-side interactivity

import { useState } from 'react';
import { Button } from '@/components/ui/button';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <Button onClick={() => setCount(count + 1)}>
        Increment
      </Button>
    </div>
  );
}
```

### Server Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { db } from '@/lib/db';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
});

export async function createPost(formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  const post = await db.post.create({
    data: parsed.data,
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}

// Usage in form
// app/posts/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### API Routes

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getServerSession } from 'next-auth';
import { db } from '@/lib/db';

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '10');

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({ users, page, limit });
}

export async function POST(request: NextRequest) {
  const session = await getServerSession();

  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  try {
    const body = await request.json();
    const parsed = CreateUserSchema.parse(body);

    const user = await db.user.create({
      data: parsed,
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.flatten() },
        { status: 400 }
      );
    }
    throw error;
  }
}
```

### Loading and Error States

```tsx
// app/dashboard/loading.tsx
import { Skeleton } from '@/components/ui/skeleton';

export default function DashboardLoading() {
  return (
    <div className="container py-8">
      <Skeleton className="h-10 w-48 mb-8" />
      <div className="grid grid-cols-3 gap-4">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
    </div>
  );
}

// app/dashboard/error.tsx
'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="container py-8 text-center">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-muted-foreground mb-4">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```

### Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });
  const isAuthPage = request.nextUrl.pathname.startsWith('/login');

  if (isAuthPage) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    return NextResponse.next();
  }

  if (!token) {
    let callbackUrl = request.nextUrl.pathname;
    if (request.nextUrl.search) {
      callbackUrl += request.nextUrl.search;
    }

    const encodedCallbackUrl = encodeURIComponent(callbackUrl);
    return NextResponse.redirect(
      new URL(`/login?callbackUrl=${encodedCallbackUrl}`, request.url)
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
};
```

## Anti-patterns

### Avoid: Using Client Components Unnecessarily

```tsx
// BAD - making everything client-side
'use client';

export default function StaticPage() {
  return <div>This doesn't need client JS</div>;
}

// GOOD - Server Component by default
export default function StaticPage() {
  return <div>Renders on server, no client JS</div>;
}
```

### Avoid: Fetching in Client Components

```tsx
// BAD - client-side fetch
'use client';

export function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users').then(res => res.json()).then(setUsers);
  }, []);
}

// GOOD - Server Component with direct DB access
export async function UserList() {
  const users = await db.user.findMany();  // No API needed!
  return <ul>{users.map(user => ...)}</ul>;
}
```

### Avoid: Prop Drilling Through Layouts

```tsx
// BAD - passing data through layouts
export default function Layout({ children, user }) {
  return <div><Header user={user} />{children}</div>;
}

// GOOD - fetch in each component that needs data
export default function Layout({ children }) {
  return <div><Header />{children}</div>;
}

// Header fetches its own data
async function Header() {
  const session = await getServerSession();
  return <header>{session?.user.name}</header>;
}
```

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [App Router](https://nextjs.org/docs/app)
- [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
