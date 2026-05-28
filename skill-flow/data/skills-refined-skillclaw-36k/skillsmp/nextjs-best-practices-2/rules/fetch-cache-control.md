---
title: Set Appropriate Cache Options
impact: CRITICAL
impactDescription: Controls data freshness and performance
tags: caching, fetch, revalidation, performance
---

## Set Appropriate Cache Options

Next.js extends fetch with caching options. Choose the right strategy based on how often your data changes.

**Incorrect (ignoring cache behavior):**

```typescript
// Default behavior may not match your needs
export default async function Page() {
  // This is cached forever by default in production
  const data = await fetch('https://api.example.com/data')

  // Or accidentally making everything dynamic
  const config = await fetch('https://api.example.com/config', {
    cache: 'no-store' // ❌ Config rarely changes, don't refetch every request
  })
}
```

**Correct (explicit cache strategies):**

```typescript
// Static data - cache forever (default)
const staticContent = await fetch('https://api.example.com/static', {
  cache: 'force-cache' // Explicit: cached until redeployed
})

// Time-based revalidation
const products = await fetch('https://api.example.com/products', {
  next: { revalidate: 3600 } // Revalidate every hour
})

// Always fresh data
const stockPrices = await fetch('https://api.example.com/prices', {
  cache: 'no-store' // Never cache - always fresh
})

// Tag-based revalidation
const user = await fetch(`https://api.example.com/users/${id}`, {
  next: { tags: ['user', `user-${id}`] } // Revalidate via tag
})
```

**Cache strategy guide:**

```typescript
// Static content (docs, blog posts) → force-cache or long revalidate
const docs = await fetch(url, { next: { revalidate: 86400 } }) // 24h

// Semi-dynamic (product catalog) → medium revalidate
const products = await fetch(url, { next: { revalidate: 3600 } }) // 1h

// User-specific but cacheable → short revalidate + tags
const profile = await fetch(url, {
  next: { revalidate: 60, tags: [`user-${id}`] }
})

// Real-time data (stock prices, live scores) → no-store
const live = await fetch(url, { cache: 'no-store' })

// Mutations → no-store + revalidate related tags
const update = await fetch(url, {
  method: 'POST',
  cache: 'no-store'
})
await revalidateTag('products')
```

Reference: [Data Fetching, Caching, and Revalidating](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating)
