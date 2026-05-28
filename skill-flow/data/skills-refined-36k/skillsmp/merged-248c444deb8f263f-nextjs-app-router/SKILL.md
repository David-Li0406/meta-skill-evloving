---
name: nextjs-app-router
description: Use this skill when building production-ready Next.js 14+ applications with App Router, focusing on Server Components, routing, data fetching, and performance optimization.
---

# Next.js App Router

Comprehensive guide for building production applications using Next.js 14+ with the App Router paradigm.

## Core Concepts

### Server vs Client Components

```tsx
// app/components/ServerComponent.tsx
async function ServerComponent() {
  const data = await db.query('SELECT * FROM users');
  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// app/components/ClientComponent.tsx
'use client';
import { useState } from 'react';

export function ClientComponent() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### File-Based Routing

#### Route Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   ├── loading.tsx     # Dashboard loading
│   └── [id]/
│       └── page.tsx    # /dashboard/[id]
├── api/
│   └── users/
│       └── route.ts    # API route handler
└── (marketing)/        # Route group (no URL segment)
    ├── about/
    │   └── page.tsx    # /about
    └── contact/
        └── page.tsx    # /contact
```

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

### Data Fetching

#### Server Component Data Fetching

```tsx
// app/users/page.tsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 3600 },
  });
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Server Actions

```tsx
// app/actions.ts
'use server';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  if (!name || !email) {
    return { error: 'Name and email required' };
  }

  const user = await db.user.create({ data: { name, email } });
  return { success: true, user };
}
```

### API Routes

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}
```

### Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
```

## Performance Optimization

### Image Optimization

```tsx
import Image from 'next/image';

function ProductImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      placeholder="blur"
      priority={false}
      loading="lazy"
    />
  );
}
```

### Best Practices

1. **Default to Server Components** - Use 'use client' only when necessary.
2. **Colocate Data Fetching** - Fetch data where it's used.
3. **Use Streaming** - Wrap slow components in Suspense.
4. **Handle Errors Gracefully** - Use error boundaries.
5. **Optimize Images** - Always use next/image.

## When to Use

- Building new Next.js applications with App Router.
- Migrating from Pages Router to App Router.
- Implementing Server Components and streaming.
- Setting up parallel and intercepting routes.
- Optimizing data fetching and caching.
- Building full-stack features with Server Actions.