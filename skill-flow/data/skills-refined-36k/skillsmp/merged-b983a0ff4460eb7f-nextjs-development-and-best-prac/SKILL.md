---
name: nextjs-development-and-best-practices
description: Use this skill when developing Next.js applications, focusing on best practices for App Router, Server Components, data fetching, and server actions.
---

# Next.js Development and Best Practices Skill

## 📋 Table of Contents

### Basics
1. [Overview](#overview)
2. [When to Use](#when-to-use)
3. [App Router Basics](#app-router-basics)
4. [Server Components vs Client Components](#server-components-vs-client-components)
5. [Data Fetching](#data-fetching)
6. [Caching Strategies](#caching-strategies)
7. [Implementation Examples](#implementation-examples)
8. [Anti-Patterns](#anti-patterns)
9. [Agent Integration](#agent-integration)

### Detailed Guides
1. [Complete Guide to Server Components](./guides/app-router/server-components-complete.md)
2. [Complete Guide to Data Fetching Strategies](./guides/data-fetching/data-fetching-strategies.md)
3. [Complete Guide to Caching and Revalidation](./guides/caching/caching-revalidation.md)

---

## Overview

This skill covers the development of Next.js applications using the App Router, focusing on:

- **App Router** - File-based routing
- **Server Components** - Server-side rendering
- **Data Fetching** - Using fetch, Prisma, ORMs
- **Caching** - Automatic caching, revalidation
- **API Routes** - RESTful API
- **Deployment** - Vercel, self-hosting

---

## 📚 Official Documentation and Resources

**What you will learn**: App Router patterns, Server Components design, caching strategies.
**Official resources to check**: Latest APIs, new features in Next.js, deployment options, migration guides.

### Key Official Documentation

- **[Next.js Documentation](https://nextjs.org/docs)** - Official Next.js documentation
  - [App Router Guide](https://nextjs.org/docs/app) - Complete guide to App Router
  - [Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching) - Details on data fetching
  - [Caching](https://nextjs.org/docs/app/building-your-application/caching) - Details on caching mechanisms
  - [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) - Complete guide to Server Actions
  - [API Reference](https://nextjs.org/docs/app/api-reference) - Full API reference

- **[Next.js Learn](https://nextjs.org/learn)** - Official tutorials
  - Interactive learning courses
  - Step-by-step project building

### Related Resources

- **[Vercel Documentation](https://vercel.com/docs)** - Deployment platform
- **[Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)** - 100+ official examples
- **[Awesome Next.js](https://github.com/unicodeveloper/awesome-nextjs)** - List of libraries and plugins
- **[Next.js Conf](https://nextjs.org/conf)** - Annual conference videos

---

## When to Use

### 🎯 Essential Timing

- [ ] When creating a new Next.js project
- [ ] When adding pages or layouts
- [ ] When adding API routes
- [ ] When implementing data fetching

---

## App Router Basics

### File-based Routing

```
app/
├── page.tsx                  # / (root)
├── about/page.tsx            # /about
├── blog/
│   ├── page.tsx              # /blog
│   └── [slug]/page.tsx       # /blog/hello-world
├── dashboard/
│   ├── layout.tsx            # /dashboard layout
│   ├── page.tsx              # /dashboard
│   └── settings/page.tsx     # /dashboard/settings
└── api/
    └── users/route.ts        # /api/users
```

### Creating Pages

```tsx
// app/page.tsx (root page)
export default function Home() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  )
}
```

### Creating Layouts

```tsx
// app/layout.tsx (root layout)
export const metadata = {
  title: 'My App',
  description: 'App description',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>
        <nav>Navigation</nav>
        {children}
        <footer>Footer</footer>
      </body>
    </html>
  )
}
```

---

## Server Components vs Client Components

### Server Components (Default)

```tsx
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // 1 hour cache
  })
  return res.json()
}

export default async function PostsPage() {
  const posts = await getPosts() // Can await directly

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Client Components

```tsx
// components/Counter.tsx
'use client' // Required

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

### Mixed Patterns

```tsx
// app/page.tsx (Server Component)
import { Counter } from '@/components/Counter' // Client Component

async function getInitialCount() {
  return 42
}

export default async function Home() {
  const initialCount = await getInitialCount()

  return (
    <div>
      <h1>Server Component</h1>
      <Counter initialValue={initialCount} />
    </div>
  )
}
```

---

## Data Fetching

### Fetch API

```tsx
// With cache (default)
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

// Without cache
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  })
  return res.json()
}

// Time-based revalidation
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // 1 hour
  })
  return res.json()
}
```

### Prisma Example

```tsx
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// app/users/page.tsx
import { prisma } from '@/lib/prisma'

export default async function UsersPage() {
  const users = await prisma.user.findMany()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

---

## Caching Strategies

### Revalidation

#### Time-based

```tsx
// Revalidate every 60 seconds
fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
})
```

#### On-demand

```tsx
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const path = request.nextUrl.searchParams.get('path')

  if (path) {
    revalidatePath(path)
    return Response.json({ revalidated: true, now: Date.now() })
  }

  return Response.json({ revalidated: false })
}
```

---

## Implementation Examples

### Example 1: Blog Application

```tsx
// app/blog/page.tsx
import Link from 'next/link'

async function getPosts() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts', {
    next: { revalidate: 3600 }
  })
  return res.json()
}

export default async function BlogPage() {
  const posts = await getPosts()

  return (
    <div>
      <h1>Blog</h1>
      <ul>
        {posts.map((post: any) => (
          <li key={post.id}>
            <Link href={`/blog/${post.id}`}>
              {post.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### Example 2: API Route (CRUD)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/users
export async function GET() {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

// POST /api/users
export async function POST(request: NextRequest) {
  const body = await request.json()

  const user = await prisma.user.create({
    data: {
      name: body.name,
      email: body.email,
    },
  })

  return NextResponse.json(user, { status: 201 })
}
```

### Example 3: Form Submission (Server Actions)

```tsx
// app/create-post/page.tsx
import { redirect } from 'next/navigation'
import { prisma } from '@/lib/prisma'

async function createPost(formData: FormData) {
  'use server' // Server Action

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await prisma.post.create({
    data: { title, content },
  })

  redirect('/posts')
}

export default function CreatePostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

---

## Anti-Patterns

### ❌ 1. Direct DB Access in Client Component

```tsx
'use client'
// ❌ Bad Example
import { prisma } from '@/lib/prisma'

export function UserList() {
  const users = await prisma.user.findMany() // Error!
}
```

```tsx
// ✅ Good Example (Server Component)
import { prisma } from '@/lib/prisma'

export default async function UserList() {
  const users = await prisma.user.findMany()
  return <ul>{/* ... */}</ul>
}
```

### ❌ 2. Unnecessary 'use client'

```tsx
// ❌ Bad Example
'use client' // Unnecessary (not interactive)

export function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>
}
```

```tsx
// ✅ Good Example (Server Component)
export function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>
}
```

---

## Agent Integration

### 📖 Example Instructions for Agents

**Create a new page**
```
Create an /about page.
Include company overview, mission, and team introduction.
```

**Create an API Route**
```
Create a CRUD API for /api/posts.
Use Prisma to support GET, POST, PUT, DELETE.
```

**Implement Server Actions**
```
Implement a user creation form using Server Actions.
Include validation as well.
```

---

## Summary

### Best Practices for Next.js

1. **Prioritize Server Components** - Use by default
2. **Implement Appropriate Caching** - Utilize revalidate
3. **Ensure Type Safety** - TypeScript + Prisma
4. **Leverage Server Actions** - For form submissions

---

_Last updated: 2025-12-26_