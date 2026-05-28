---
title: Fetch in Server Components, Not Client
impact: CRITICAL
impactDescription: Eliminates client-server waterfalls and protects API keys
tags: server-components, data-fetching, security, performance
---

## Fetch in Server Components, Not Client

Server Components can fetch data directly without exposing API endpoints or keys to the client. Client-side fetching adds latency and security risks.

**Incorrect (client-side fetching):**

```typescript
// app/products/page.tsx
'use client'

import { useEffect, useState } from 'react'

export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // ❌ Waterfall: HTML → JS → Fetch → Render
    // ❌ API key exposed if needed
    // ❌ Extra loading state management
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        setProducts(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <Skeleton />
  return <ProductList products={products} />
}
```

**Correct (Server Component fetching):**

```typescript
// app/products/page.tsx
// No 'use client' - Server Component ✓

async function getProducts() {
  // ✓ Runs on server - API key never exposed
  // ✓ No waterfall - data fetched before HTML sent
  const res = await fetch('https://api.example.com/products', {
    headers: { Authorization: `Bearer ${process.env.API_KEY}` }
  })
  return res.json()
}

export default async function ProductsPage() {
  const products = await getProducts()

  // HTML sent with data already rendered
  return <ProductList products={products} />
}
```

**When client fetching IS appropriate:**

```typescript
// Real-time updates after initial load
'use client'
import useSWR from 'swr'

export function LivePriceDisplay({ initialPrice, productId }) {
  const { data: price } = useSWR(
    `/api/prices/${productId}`,
    fetcher,
    {
      fallbackData: initialPrice, // Server-rendered initial value
      refreshInterval: 5000       // Poll for updates
    }
  )
  return <span>${price}</span>
}

// User interactions that need fresh data
'use client'
export function SearchResults() {
  const [query, setQuery] = useState('')
  const { data } = useSWR(query ? `/api/search?q=${query}` : null)
  // Client fetch appropriate - query depends on user input
}
```

Default to Server Component fetching. Only use client fetching for real-time updates or user-driven queries.

Reference: [Server Components Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating)
