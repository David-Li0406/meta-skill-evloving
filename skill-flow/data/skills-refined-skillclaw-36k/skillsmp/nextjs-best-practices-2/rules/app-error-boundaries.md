---
title: Add error.tsx for Graceful Failures
impact: CRITICAL
impactDescription: Prevents full page crashes and enables recovery
tags: errors, error-boundary, recovery, resilience
---

## Add error.tsx for Graceful Failures

error.tsx creates an error boundary that catches errors in route segments, preventing the entire app from crashing and allowing users to recover.

**Incorrect (no error handling):**

```typescript
// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)
  // If this throws, user sees generic error page
  // No way to recover without full page reload
  return <Product data={product} />
}
```

**Correct (error.tsx with recovery):**

```typescript
// app/products/[id]/error.tsx
'use client' // Error components must be Client Components

import { useEffect } from 'react'

export default function ProductError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log to error reporting service
    console.error('Product error:', error)
  }, [error])

  return (
    <div className="p-4 text-center">
      <h2 className="text-xl font-bold text-red-600">
        Something went wrong loading this product
      </h2>
      <p className="mt-2 text-gray-600">
        {error.message || 'Please try again'}
      </p>
      <button
        onClick={() => reset()}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Try again
      </button>
    </div>
  )
}

// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id) // Error caught by boundary
  return <Product data={product} />
}
```

**Global error handling (app/global-error.tsx):**

```typescript
// app/global-error.tsx - Catches root layout errors
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

**Error boundary hierarchy:**

```
app/
├── global-error.tsx     # Root layout errors
├── error.tsx            # App-wide errors
├── products/
│   ├── error.tsx        # Product section errors
│   └── [id]/
│       └── error.tsx    # Individual product errors
```

Reference: [Error Handling](https://nextjs.org/docs/app/building-your-application/routing/error-handling)
