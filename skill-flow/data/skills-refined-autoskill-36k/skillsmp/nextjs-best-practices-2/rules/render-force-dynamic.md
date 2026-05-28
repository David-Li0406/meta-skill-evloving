---
title: Use force-dynamic Only When Necessary
impact: HIGH
impactDescription: Overusing force-dynamic negates Next.js caching benefits
tags: dynamic, caching, force-dynamic, optimization
---

## Use force-dynamic Only When Necessary

force-dynamic disables all caching for a route. Only use it when every request must be fresh and unique.

**Incorrect (overusing force-dynamic):**

```typescript
// ❌ Product catalog doesn't need to be real-time
export const dynamic = 'force-dynamic'

export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductList products={products} />
}

// ❌ Blog post with rare updates
export const dynamic = 'force-dynamic'

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug)
  return <Article post={post} />
}
```

**Correct (targeted dynamic behavior):**

```typescript
// Products - use ISR instead
export const revalidate = 60 // Revalidate every minute

export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductList products={products} />
}

// Blog - use on-demand revalidation
export default async function BlogPost({ params }) {
  const post = await getPost(params.slug)
  return <Article post={post} />
}

// In CMS webhook or Server Action:
await revalidateTag(`post-${slug}`)
```

**When force-dynamic IS appropriate:**

```typescript
// Real-time stock prices - must be fresh every request
export const dynamic = 'force-dynamic'

export default async function TradingPage() {
  const prices = await getLivePrices()
  return <StockTicker prices={prices} />
}

// User-specific page that can't be cached
export const dynamic = 'force-dynamic'

export default async function AccountPage() {
  const session = await getServerSession()
  const account = await getAccount(session.userId)
  return <AccountDashboard account={account} />
}

// A/B testing requiring fresh random assignment
export const dynamic = 'force-dynamic'

export default async function LandingPage() {
  const variant = Math.random() > 0.5 ? 'A' : 'B'
  return variant === 'A' ? <VariantA /> : <VariantB />
}
```

**Alternatives to force-dynamic:**

```typescript
// Instead of force-dynamic, use specific options:

// Time-based freshness
export const revalidate = 0 // Revalidate on every request (like force-dynamic)
export const revalidate = 10 // Accept 10s staleness

// Fetch-level control
const data = await fetch(url, { cache: 'no-store' }) // Just this fetch is dynamic

// On-demand revalidation
revalidateTag('prices') // Trigger fresh fetch when needed
```

Reference: [Route Segment Config](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config)
