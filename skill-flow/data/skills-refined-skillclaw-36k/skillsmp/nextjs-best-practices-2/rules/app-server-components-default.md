---
title: Use Server Components by Default
impact: CRITICAL
impactDescription: Reduces client bundle size and enables streaming
tags: server-components, app-router, bundle-size, performance
---

## Use Server Components by Default

Server Components run on the server, reducing JavaScript sent to the client. Only add 'use client' when you need browser APIs, event handlers, or React hooks.

**Incorrect (unnecessary client components):**

```typescript
// app/products/page.tsx
'use client' // ❌ Unnecessary - no client features used

import { getProducts } from '@/lib/api'

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  )
}
```

**Correct (Server Component by default):**

```typescript
// app/products/page.tsx
// No directive = Server Component ✓

import { getProducts } from '@/lib/api'
import { AddToCartButton } from './add-to-cart-button'

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name}
          {/* Only this button needs to be a Client Component */}
          <AddToCartButton productId={product.id} />
        </li>
      ))}
    </ul>
  )
}

// app/products/add-to-cart-button.tsx
'use client' // ✓ Required - uses onClick handler

export function AddToCartButton({ productId }: { productId: string }) {
  const handleClick = () => {
    // Client-side interaction
  }

  return <button onClick={handleClick}>Add to Cart</button>
}
```

**When to use 'use client':**

```typescript
// ✓ Event handlers (onClick, onChange, onSubmit)
// ✓ React hooks (useState, useEffect, useContext)
// ✓ Browser APIs (localStorage, window, navigator)
// ✓ Third-party client libraries (analytics, animations)
```

Server Components can directly import and render Client Components, but not vice versa.

Reference: [Next.js Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
