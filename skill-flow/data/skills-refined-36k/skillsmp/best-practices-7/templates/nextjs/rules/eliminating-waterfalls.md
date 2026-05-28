---
title: Eliminating Waterfalls
impact: CRITICAL
impactDescription: 2-10x performance improvement
tags: async, fetch, parallel, suspense, streaming
---

# Eliminating Waterfalls

Prevent sequential data loading that blocks rendering.

## Rule 1: Parallel Data Fetching with Promise.all

```typescript
// ❌ INCORRECT - sequential: 3 round trips = 3x latency
async function Page({ params }) {
  const user = await getUser(params.id)
  const orders = await getOrders(params.id)
  const recommendations = await getRecommendations(params.id)

  return <Dashboard user={user} orders={orders} recommendations={recommendations} />
}

// ✅ CORRECT - parallel: 1 round trip
async function Page({ params }) {
  const [user, orders, recommendations] = await Promise.all([
    getUser(params.id),
    getOrders(params.id),
    getRecommendations(params.id)
  ])

  return <Dashboard user={user} orders={orders} recommendations={recommendations} />
}
```

## Rule 2: Use Suspense for Streaming

```typescript
// ❌ INCORRECT - entire page waits for slow data
async function Page() {
  const slowData = await getSlowData()  // blocks everything
  const fastData = await getFastData()

  return (
    <div>
      <FastSection data={fastData} />
      <SlowSection data={slowData} />
    </div>
  )
}

// ✅ CORRECT - stream slow content
async function Page() {
  const fastData = await getFastData()

  return (
    <div>
      <FastSection data={fastData} />
      <Suspense fallback={<SlowSectionSkeleton />}>
        <SlowSection />
      </Suspense>
    </div>
  )
}

async function SlowSection() {
  const data = await getSlowData()
  return <div>{/* render data */}</div>
}
```

## Rule 3: Preload Data Before Navigation

```typescript
// lib/data.ts
import { preload } from 'react-dom'

export function preloadProductData(id: string) {
  preload(`/api/products/${id}`, { as: 'fetch' })
}

// components/ProductLink.tsx
'use client'
import { preloadProductData } from '@/lib/data'

export function ProductLink({ id, children }) {
  return (
    <Link
      href={`/products/${id}`}
      onMouseEnter={() => preloadProductData(id)}
    >
      {children}
    </Link>
  )
}
```

## Rule 4: Avoid Client-Side Fetch Waterfalls

```typescript
// ❌ INCORRECT - waterfall in useEffect
'use client'
function Dashboard() {
  const [user, setUser] = useState(null)
  const [posts, setPosts] = useState([])

  useEffect(() => {
    getUser().then(u => {
      setUser(u)
      getPosts(u.id).then(setPosts)  // waits for user
    })
  }, [])
}

// ✅ CORRECT - fetch on server, no waterfall
async function Dashboard() {
  const user = await getUser()
  const posts = await getPosts(user.id)
  return <DashboardContent user={user} posts={posts} />
}

// OR if client-side needed:
'use client'
function Dashboard({ userId }) {
  const { data } = useSWR(`/api/dashboard/${userId}`, fetcher)
  // Single endpoint returns all needed data
}
```

## Rule 5: Use generateStaticParams for Build-Time Fetching

```typescript
// app/products/[id]/page.tsx

// Fetch all product IDs at build time
export async function generateStaticParams() {
  const products = await getProducts()
  return products.map(p => ({ id: p.id }))
}

// Each page is statically generated
async function ProductPage({ params }) {
  const product = await getProduct(params.id)
  return <Product data={product} />
}
```

## Detection Checklist

Look for these waterfall patterns:

- [ ] Sequential `await` statements in Server Components
- [ ] `useEffect` chains that depend on each other
- [ ] Parent-child data dependencies without Suspense
- [ ] Multiple API calls without Promise.all
- [ ] Route changes without preloading
