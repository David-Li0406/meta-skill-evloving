---
title: Choose Time-Based or On-Demand Revalidation
impact: CRITICAL
impactDescription: Balance data freshness with performance
tags: revalidation, isr, cache, freshness
---

## Choose Time-Based or On-Demand Revalidation

Time-based revalidation (ISR) refreshes data periodically. On-demand revalidation refreshes immediately when data changes. Choose based on your data characteristics.

**Time-based revalidation (ISR):**

```typescript
// Good for: content that changes on a schedule or acceptable staleness

// Page-level revalidation
export const revalidate = 3600 // Revalidate every hour

export default async function BlogPage() {
  const posts = await getPosts()
  return <BlogList posts={posts} />
}

// Fetch-level revalidation
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 } // Revalidate every minute
  })
  return res.json()
}
```

**On-demand revalidation:**

```typescript
// Good for: data that changes unpredictably (user actions, webhooks)

// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache'

export async function POST(request: Request) {
  const { path, tag, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 })
  }

  if (tag) {
    revalidateTag(tag)
  } else if (path) {
    revalidatePath(path)
  }

  return Response.json({ revalidated: true, now: Date.now() })
}

// In Server Action after mutation
'use server'

import { revalidateTag, revalidatePath } from 'next/cache'

export async function updateProduct(id: string, data: FormData) {
  await db.products.update({ where: { id }, data })

  // Revalidate specific product
  revalidateTag(`product-${id}`)

  // Revalidate product listing
  revalidateTag('products')

  // Or revalidate by path
  revalidatePath('/products')
  revalidatePath(`/products/${id}`)
}
```

**Strategy guide:**

```typescript
// Blog posts: Time-based (readers can see slightly stale content)
export const revalidate = 3600 // 1 hour

// E-commerce inventory: On-demand (accuracy matters)
await revalidateTag('inventory')

// User dashboard: Combination
const profile = await fetch(url, {
  next: {
    revalidate: 300,        // Background refresh every 5 min
    tags: [`user-${id}`]    // Instant update on profile change
  }
})
```

Reference: [Revalidating Data](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating#revalidating-data)
