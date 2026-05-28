<overview>
Cache Components in Next.js 16 provide explicit, opt-in caching using `use cache` directive, `cacheLife()`, and `cacheTag()`. Caching is NOT automatic - you must opt in.
</overview>

<setup>
**Enable Cache Components:**

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

This enables:
- `'use cache'` directive
- `cacheLife()` function
- `cacheTag()` function
- Partial Pre-Rendering (PPR)
</setup>

<use_cache>
**The `'use cache'` directive marks functions/components for caching:**

```tsx
// Cache an entire component
async function ProductList() {
  'use cache'

  const products = await db.products.findMany()
  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  )
}

// Cache a data fetching function
async function getProducts() {
  'use cache'

  return await db.products.findMany()
}

// Cache at page level
export default async function Page() {
  'use cache'

  const data = await fetchData()
  return <div>{data}</div>
}
```

**Rules:**
- Can only be used in Server Components/functions
- Must be at the top of the function body
- Works with async functions
- Cache key is automatically derived from function inputs
</use_cache>

<cache_life>
**Control cache duration with `cacheLife()`:**

```tsx
import { cacheLife } from 'next/cache'

async function getProducts() {
  'use cache'
  cacheLife('hours')  // Cache for hours

  return await db.products.findMany()
}
```

**Built-in profiles:**

| Profile | Stale | Revalidate | Expire |
|---------|-------|------------|--------|
| `'seconds'` | 0 | 1s | 60s |
| `'minutes'` | 5m | 1m | 1h |
| `'hours'` | 5m | 1h | 1d |
| `'days'` | 5m | 1d | 1w |
| `'weeks'` | 5m | 1w | 1mo |
| `'max'` | 5m | 1mo | indefinite |

**Custom profiles:**

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  cacheLife: {
    dashboard: {
      stale: 60,       // 1 minute - serve stale while revalidating
      revalidate: 300, // 5 minutes - background revalidation interval
      expire: 3600,    // 1 hour - max cache lifetime
    },
    realtime: {
      stale: 0,
      revalidate: 5,
      expire: 60,
    },
  },
}

// Usage
async function getDashboardData() {
  'use cache'
  cacheLife('dashboard')

  return await fetchDashboard()
}
```
</cache_life>

<cache_tag>
**Tag cached data for targeted revalidation:**

```tsx
import { cacheTag, cacheLife } from 'next/cache'

async function getProducts(categoryId: string) {
  'use cache'
  cacheLife('hours')
  cacheTag('products', `category-${categoryId}`)

  return await db.products.findMany({ where: { categoryId } })
}

async function getProduct(id: string) {
  'use cache'
  cacheLife('hours')
  cacheTag('products', `product-${id}`)

  return await db.products.findUnique({ where: { id } })
}
```

**Revalidating by tag:**

```tsx
'use server'

import { revalidateTag, updateTag } from 'next/cache'

export async function updateProduct(id: string, data: ProductData) {
  await db.products.update({ where: { id }, data })

  // Option 1: Eventual consistency (background revalidation)
  revalidateTag(`product-${id}`)
  revalidateTag('products')

  // Option 2: Immediate refresh (same request)
  updateTag(`product-${id}`)
  updateTag('products')
}
```

**`updateTag` vs `revalidateTag`:**
- `updateTag`: Expires cache and refreshes immediately in same request
- `revalidateTag`: Marks cache stale, refreshes in background on next request
</cache_tag>

<patterns>
<pattern name="conditional-caching">
**Different cache durations based on data:**

```tsx
async function getPost(slug: string) {
  'use cache'

  const post = await db.posts.findUnique({ where: { slug } })

  if (!post) {
    cacheLife('minutes')  // Cache "not found" briefly
    return null
  }

  if (post.status === 'draft') {
    cacheLife('seconds')  // Drafts need frequent updates
  } else {
    cacheLife('days')     // Published content stable
  }

  cacheTag('posts', `post-${slug}`)
  return post
}
```
</pattern>

<pattern name="partial-caching">
**Cache expensive parts, keep others dynamic:**

```tsx
export default async function Dashboard() {
  return (
    <div>
      {/* Dynamic - user-specific, always fresh */}
      <UserGreeting />

      {/* Cached - expensive aggregation */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <CachedAnalytics />
      </Suspense>

      {/* Cached - rarely changes */}
      <Suspense fallback={<AnnouncementsSkeleton />}>
        <CachedAnnouncements />
      </Suspense>
    </div>
  )
}

async function CachedAnalytics() {
  'use cache'
  cacheLife('minutes')
  cacheTag('analytics')

  const data = await computeExpensiveAnalytics()
  return <AnalyticsChart data={data} />
}
```
</pattern>

<pattern name="nested-caching">
**Nested cache directives:**

```tsx
async function getCategory(id: string) {
  'use cache'
  cacheLife('hours')
  cacheTag(`category-${id}`)

  const category = await db.categories.findUnique({ where: { id } })

  // This has its own cache, independent of parent
  const products = await getProductsForCategory(id)

  return { category, products }
}

async function getProductsForCategory(categoryId: string) {
  'use cache'
  cacheLife('minutes')  // Products update more frequently
  cacheTag('products', `category-${categoryId}`)

  return await db.products.findMany({ where: { categoryId } })
}
```

**Note:** When outer cache hits, it returns complete cached output including nested data. Nested caches only run when outer cache misses.
</pattern>

<pattern name="cache-with-server-actions">
**Passing Server Actions through cached components:**

```tsx
export default async function Page() {
  async function handleSubmit(formData: FormData) {
    'use server'
    await db.items.create({ ... })
    updateTag('items')
  }

  return <CachedForm action={handleSubmit} />
}

async function CachedForm({
  action,
}: {
  action: (formData: FormData) => Promise<void>
}) {
  'use cache'
  cacheLife('hours')

  // Don't call the action inside cached function!
  // Just pass it through to client
  return <ClientForm action={action} />
}
```
</pattern>
</patterns>

<remote_caching>
**For distributed deployments, use remote caching:**

```tsx
async function getData() {
  'use cache: remote'  // Cache in distributed cache (e.g., Redis)
  cacheLife('hours')

  return await expensiveOperation()
}
```

Requires configuring remote cache provider in deployment.
</remote_caching>

<anti_patterns>
<anti_pattern name="cache-user-specific">
**Problem:** Caching user-specific data

```tsx
async function getUserDashboard() {
  'use cache'  // BAD - same cache for all users!

  const user = await getUser()
  return await getDashboardFor(user.id)
}
```

**Fix:** Include user identifier in cache key or don't cache

```tsx
async function getUserDashboard(userId: string) {
  'use cache'
  cacheTag(`user-${userId}`)  // Per-user cache

  return await getDashboardFor(userId)
}
```
</anti_pattern>

<anti_pattern name="forget-revalidation">
**Problem:** Data updates but cache shows stale data

**Fix:** Always revalidate after mutations

```tsx
'use server'
export async function createProduct(data: ProductData) {
  await db.products.create({ data })
  updateTag('products')  // Don't forget this!
}
```
</anti_pattern>

<anti_pattern name="over-caching">
**Problem:** Caching data that changes frequently

**Fix:** Match cache duration to data volatility
- Real-time data: `'seconds'` or no cache
- User actions: `'minutes'`
- Reference data: `'hours'` or `'days'`
</anti_pattern>
</anti_patterns>
