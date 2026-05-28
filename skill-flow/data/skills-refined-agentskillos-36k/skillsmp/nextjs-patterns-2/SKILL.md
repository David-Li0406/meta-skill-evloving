---
name: nextjs-patterns
description: Next.js App Router patterns, Server Components, and best practices
license: MIT
---

# Next.js Patterns Skill

Modern Next.js development patterns focusing on App Router, Server Components, and production best practices.

## When to Use

- Building new Next.js 13+ applications
- Migrating from Pages Router to App Router
- Implementing Server Components patterns
- Optimizing Next.js performance

## App Router Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── global-error.tsx    # Global error boundary
├── (auth)/             # Route group (no URL impact)
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx
│   └── [id]/           # Dynamic route
│       └── page.tsx
└── api/
    └── route.ts        # API route handler
```

## Server Components (Default)

```tsx
// app/users/page.tsx - Server Component by default
import { db } from '@/lib/db'

// Direct database access - no API needed
export default async function UsersPage() {
  const users = await db.user.findMany()
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

## Client Components

```tsx
// components/counter.tsx
'use client' // Required directive

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

## Server Actions

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const schema = z.object({
  title: z.string().min(1),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  const validated = schema.parse({
    title: formData.get('title'),
    content: formData.get('content'),
  })
  
  await db.post.create({ data: validated })
  
  revalidatePath('/posts')
  redirect('/posts')
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Data Fetching Patterns

### Parallel Data Fetching

```tsx
// Fetch in parallel - don't await sequentially
export default async function Page() {
  const [users, posts] = await Promise.all([
    getUsers(),
    getPosts(),
  ])
  
  return <Dashboard users={users} posts={posts} />
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react'
import { UserList, UserListSkeleton } from '@/components/user-list'
import { PostList, PostListSkeleton } from '@/components/post-list'

export default function Page() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
      <Suspense fallback={<PostListSkeleton />}>
        <PostList />
      </Suspense>
    </div>
  )
}
```

## Caching Strategies

```tsx
// Default: cached indefinitely (static)
fetch('https://api.example.com/data')

// Revalidate every 60 seconds
fetch('https://api.example.com/data', { 
  next: { revalidate: 60 } 
})

// No cache (dynamic)
fetch('https://api.example.com/data', { 
  cache: 'no-store' 
})

// Tag-based revalidation
fetch('https://api.example.com/posts', { 
  next: { tags: ['posts'] } 
})

// In server action:
import { revalidateTag } from 'next/cache'
revalidateTag('posts')
```

## Metadata

```tsx
// Static metadata
export const metadata = {
  title: 'My App',
  description: 'App description',
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.id)
  return {
    title: post.title,
    openGraph: {
      images: [post.image],
    },
  }
}
```

## Route Handlers (API)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')
  
  const users = await db.user.findMany({
    where: query ? { name: { contains: query } } : undefined,
  })
  
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await db.user.create({ data: body })
  
  return NextResponse.json(user, { status: 201 })
}
```

## Middleware

```tsx
// middleware.ts (root level)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  // Add headers
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')
  
  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Error Handling

```tsx
// app/dashboard/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

## Loading UI

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="h-4 bg-gray-200 rounded w-full mb-2" />
      <div className="h-4 bg-gray-200 rounded w-3/4" />
    </div>
  )
}
```

## Best Practices

### Component Composition

```tsx
// Server Component wrapping Client Component
import { Counter } from '@/components/counter'

export default async function Page() {
  const initialCount = await getCount()
  
  return <Counter initialCount={initialCount} />
}
```

### Colocate Related Files

```
app/
└── dashboard/
    ├── page.tsx
    ├── loading.tsx
    ├── error.tsx
    ├── actions.ts        # Server actions
    ├── queries.ts        # Data fetching
    └── _components/      # Route-specific components
        ├── chart.tsx
        └── stats.tsx
```

### Environment Variables

```bash
# .env.local
DATABASE_URL="..."          # Server only
NEXT_PUBLIC_API_URL="..."   # Exposed to client (NEXT_PUBLIC_ prefix)
```

## Common Pitfalls

1. **Don't import server-only code in client components**
   ```tsx
   // Use 'server-only' package to prevent mistakes
   import 'server-only'
   import { db } from './db'
   ```

2. **Don't pass non-serializable props to client components**
   ```tsx
   // Wrong: passing function from server to client
   <ClientComponent onClick={handleClick} />
   
   // Right: define handler in client component
   ```

3. **Use `next/navigation` not `next/router`**
   ```tsx
   // App Router
   import { useRouter, usePathname, useSearchParams } from 'next/navigation'
   ```

## Performance Checklist

- [ ] Use Server Components by default
- [ ] Implement Suspense boundaries for streaming
- [ ] Parallel fetch with `Promise.all`
- [ ] Use `next/image` for images
- [ ] Use `next/font` for fonts
- [ ] Configure appropriate caching
- [ ] Use route groups to organize without URL impact
- [ ] Implement proper error boundaries
