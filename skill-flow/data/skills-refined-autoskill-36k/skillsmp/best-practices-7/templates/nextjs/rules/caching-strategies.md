---
title: Caching Strategies
impact: MEDIUM
impactDescription: Optimal caching - reduces server load, improves response times, balances freshness vs performance
tags: caching, revalidation, fetch, nextjs, performance
---

# Caching Strategies (MEDIUM)

Next.js caching patterns for optimal performance and data freshness.

## Rule 1: Fetch Caching Defaults

**Understand fetch caching behavior:**

```typescript
// Static - cached indefinitely (default in App Router)
const data = await fetch('https://api.example.com/data')

// Time-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }  // Revalidate every hour
})

// No caching - always fresh
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// ✅ CORRECT - choose based on data characteristics
// Static content (rarely changes)
const categories = await fetch('/api/categories')  // Default cache

// User-specific data (changes often)
const user = await fetch('/api/user', { cache: 'no-store' })

// Time-sensitive but cacheable
const posts = await fetch('/api/posts', {
  next: { revalidate: 60 }  // Fresh every minute
})
```

## Rule 2: React Cache for Deduplication

**Use cache() for request deduplication:**

```typescript
// ❌ INCORRECT - duplicate fetches in same request
async function UserProfile({ userId }: Props) {
  const user = await getUser(userId)  // Fetch 1
  return <Profile user={user} />
}

async function UserPosts({ userId }: Props) {
  const user = await getUser(userId)  // Fetch 2 (duplicate!)
  return <Posts userId={user.id} />
}

// ✅ CORRECT - cached function (deduplicated)
import { cache } from 'react'

export const getUser = cache(async (userId: string) => {
  const res = await fetch(`/api/users/${userId}`)
  return res.json()
})

// Now both components share the same fetch
async function UserProfile({ userId }: Props) {
  const user = await getUser(userId)  // Fetch 1
  return <Profile user={user} />
}

async function UserPosts({ userId }: Props) {
  const user = await getUser(userId)  // Reuses Fetch 1
  return <Posts userId={user.id} />
}
```

## Rule 3: unstable_cache for Database Queries

**Cache database queries with tags:**

```typescript
import { unstable_cache } from 'next/cache'

// ❌ INCORRECT - uncached database query
export async function getUser(id: string) {
  return db.user.findUnique({ where: { id } })
}

// ✅ CORRECT - cached with tags for invalidation
export const getUser = unstable_cache(
  async (id: string) => {
    return db.user.findUnique({ where: { id } })
  },
  ['user'],  // Cache key prefix
  {
    tags: ['user'],  // For revalidation
    revalidate: 3600,  // 1 hour
  }
)

// Invalidate when user updates
export async function updateUser(id: string, data: UpdateUserInput) {
  await db.user.update({ where: { id }, data })
  revalidateTag('user')  // Invalidate all user caches
}
```

## Rule 4: Route Segment Config

**Configure caching at route level:**

```typescript
// app/dashboard/page.tsx

// Force dynamic rendering
export const dynamic = 'force-dynamic'

// Or force static
export const dynamic = 'force-static'

// Revalidate entire page
export const revalidate = 60  // seconds

// ✅ CORRECT - choose based on page needs
// Static marketing page
// app/about/page.tsx
export const dynamic = 'force-static'

// Real-time dashboard
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic'

// News page - fresh every 5 minutes
// app/news/page.tsx
export const revalidate = 300
```

## Rule 5: On-Demand Revalidation

**Revalidate when data changes:**

```typescript
// ✅ CORRECT - revalidate by path
import { revalidatePath } from 'next/cache'

export async function createPost(data: CreatePostInput) {
  await db.post.create({ data })
  revalidatePath('/posts')  // Revalidate posts list
  revalidatePath('/posts/[id]', 'page')  // Revalidate all post pages
}

// ✅ CORRECT - revalidate by tag
import { revalidateTag } from 'next/cache'

export async function updatePost(id: string, data: UpdatePostInput) {
  await db.post.update({ where: { id }, data })
  revalidateTag('posts')  // Invalidate all caches with 'posts' tag
  revalidateTag(`post-${id}`)  // Invalidate specific post cache
}
```

## Rule 6: generateStaticParams for Static Generation

**Pre-render dynamic routes:**

```typescript
// ✅ CORRECT - static generation for known paths
// app/posts/[id]/page.tsx
export async function generateStaticParams() {
  const posts = await db.post.findMany({ select: { id: true } })

  return posts.map((post) => ({
    id: post.id,
  }))
}

export default async function PostPage({ params }: Props) {
  const post = await getPost(params.id)
  return <PostContent post={post} />
}

// With limited static generation
export async function generateStaticParams() {
  // Only pre-render most popular posts
  const posts = await db.post.findMany({
    take: 100,
    orderBy: { views: 'desc' },
  })

  return posts.map((post) => ({ id: post.id }))
}

// New posts will be generated on-demand (ISR)
export const dynamicParams = true  // default
```

## Rule 7: Caching Strategy by Data Type

**Choose caching based on data characteristics:**

```typescript
// ✅ CORRECT - caching decision matrix

// 1. Static data (rarely changes)
// - Categories, settings, site config
const categories = await fetch('/api/categories')  // Cached indefinitely

// 2. Semi-static data (changes occasionally)
// - Blog posts, product listings
const posts = await fetch('/api/posts', {
  next: { revalidate: 300 }  // 5 minutes
})

// 3. Time-sensitive data (changes frequently)
// - Stock prices, live scores
const prices = await fetch('/api/prices', {
  next: { revalidate: 10 }  // 10 seconds
})

// 4. User-specific data (must be fresh)
// - Shopping cart, notifications
const cart = await fetch('/api/cart', {
  cache: 'no-store'
})

// 5. Real-time data (always fresh)
// - Chat messages, live updates
const messages = await fetch('/api/messages', {
  cache: 'no-store'
})
```

## Rule 8: Client-Side Caching with TanStack Query

**Complement server caching with client caching:**

```typescript
// ✅ CORRECT - server + client caching
// Server: Initial data with caching
export default async function Page() {
  const initialPosts = await getPosts()  // Cached on server

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList initialData={initialPosts} />
    </HydrationBoundary>
  )
}

// Client: Real-time updates
'use client'
function PostList({ initialData }: Props) {
  const { data: posts } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    initialData,
    staleTime: 60 * 1000,  // Consider fresh for 1 minute
    refetchInterval: 30 * 1000,  // Refetch every 30 seconds
  })

  return <List items={posts} />
}
```

## Compliance Checklist

Before submitting code:

- [ ] Appropriate fetch caching per data type
- [ ] React cache() for request deduplication
- [ ] unstable_cache for database queries with tags
- [ ] On-demand revalidation after mutations
- [ ] generateStaticParams for known dynamic routes
- [ ] Route segment config where appropriate
