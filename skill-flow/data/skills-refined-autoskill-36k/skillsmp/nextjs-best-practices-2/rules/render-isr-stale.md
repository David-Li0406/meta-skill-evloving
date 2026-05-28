---
title: Use ISR for Content with Known Update Frequency
impact: HIGH
impactDescription: Combines static performance with data freshness
tags: isr, revalidation, caching, static-regeneration
---

## Use ISR for Content with Known Update Frequency

Incremental Static Regeneration (ISR) serves cached pages while regenerating them in the background. Perfect for content that changes periodically.

**Incorrect (all or nothing approach):**

```typescript
// Everything static - stale content
export default async function BlogPage() {
  const posts = await getPosts() // Cached forever
  return <BlogList posts={posts} />
}

// Everything dynamic - unnecessary load
export const dynamic = 'force-dynamic'

export default async function BlogPage() {
  const posts = await getPosts() // Fetched every request
  return <BlogList posts={posts} />
}
```

**Correct (ISR with appropriate intervals):**

```typescript
// Blog posts - check for updates every hour
export const revalidate = 3600

export default async function BlogPage() {
  const posts = await getPosts()
  return <BlogList posts={posts} />
}

// Product catalog - fresher data needed
export const revalidate = 60

export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductList products={products} />
}

// High-traffic homepage - balance freshness and cost
export const revalidate = 300 // 5 minutes

export default async function HomePage() {
  const featured = await getFeaturedContent()
  return <Home featured={featured} />
}
```

**ISR with generateStaticParams:**

```typescript
// app/blog/[slug]/page.tsx

// Pre-render top 100 posts at build time
export async function generateStaticParams() {
  const posts = await getTopPosts(100)
  return posts.map(post => ({ slug: post.slug }))
}

// Revalidate individual posts every hour
export const revalidate = 3600

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug)
  return <Article post={post} />
}

// New posts are generated on-demand on first request
// Then cached with the same revalidation
```

**ISR guidelines:**

```typescript
// Content update frequency → revalidate interval
// Real-time data → 0 or no-store
// Minutes (stock, scores) → 60
// Hourly (news, social) → 3600
// Daily (blog, docs) → 86400
// Weekly (reference) → 604800
// Never (legal, static) → false or omit
```

Reference: [Incremental Static Regeneration](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating#revalidating-data)
