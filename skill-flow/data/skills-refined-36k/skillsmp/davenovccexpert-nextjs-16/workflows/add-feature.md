<workflow name="add-feature">
<title>Add Feature to Next.js 16 App</title>

<required_reading>
**Read these reference files NOW:**
1. references/server-client-components.md
2. references/server-actions.md
3. references/cache-components.md
</required_reading>

<process>

<step name="1-understand-requirements">
<title>Understand Requirements</title>

Before coding, clarify:
1. **What data does the feature need?** (Database, API, user input)
2. **Is it interactive?** (Needs `'use client'`)
3. **Does it modify data?** (Needs Server Actions)
4. **Should results be cached?** (Use `'use cache'`)

**Decision tree:**
- Pure display of server data → Server Component
- User interaction (clicks, forms) → Client Component
- Data mutation → Server Action
- Expensive computation → Add `'use cache'`
</step>

<step name="2-create-server-component">
<title>Create Server Component (Default)</title>

```tsx
// components/features/ProductList.tsx
import { cacheLife, cacheTag } from 'next/cache'

interface Product {
  id: string
  name: string
  price: number
}

async function getProducts(): Promise<Product[]> {
  'use cache'
  cacheLife('hours')
  cacheTag('products')

  const products = await db.products.findMany()
  return products
}

export async function ProductList() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name} - ${product.price}
        </li>
      ))}
    </ul>
  )
}
```
</step>

<step name="3-add-client-interactivity">
<title>Add Client Interactivity (If Needed)</title>

```tsx
// components/features/AddToCartButton.tsx
'use client'

import { useState } from 'react'
import { addToCart } from '@/lib/actions'

interface Props {
  productId: string
}

export function AddToCartButton({ productId }: Props) {
  const [pending, setPending] = useState(false)

  async function handleClick() {
    setPending(true)
    await addToCart(productId)
    setPending(false)
  }

  return (
    <button onClick={handleClick} disabled={pending}>
      {pending ? 'Adding...' : 'Add to Cart'}
    </button>
  )
}
```

**Combine in page:**
```tsx
// app/products/page.tsx
import { ProductList } from '@/components/features/ProductList'
import { AddToCartButton } from '@/components/features/AddToCartButton'

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <div>
      <h1>Products</h1>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            {product.name} - ${product.price}
            <AddToCartButton productId={product.id} />
          </li>
        ))}
      </ul>
    </div>
  )
}
```
</step>

<step name="4-create-server-actions">
<title>Create Server Actions (For Mutations)</title>

```tsx
// lib/actions/cart.ts
'use server'

import { revalidateTag, updateTag } from 'next/cache'
import { getUser } from '@/lib/dal'

export async function addToCart(productId: string) {
  // Always verify auth
  const user = await getUser()
  if (!user) {
    throw new Error('Unauthorized')
  }

  // Validate input
  if (!productId) {
    return { error: 'Product ID required' }
  }

  // Perform mutation
  await db.cartItems.create({
    data: {
      userId: user.id,
      productId,
      quantity: 1,
    },
  })

  // Revalidate cached cart data
  updateTag('cart')

  return { success: true }
}

export async function removeFromCart(itemId: string) {
  const user = await getUser()
  if (!user) {
    throw new Error('Unauthorized')
  }

  await db.cartItems.delete({
    where: { id: itemId, userId: user.id },
  })

  updateTag('cart')

  return { success: true }
}
```
</step>

<step name="5-add-form-handling">
<title>Add Form Handling</title>

**Server Action with form:**
```tsx
// lib/actions/products.ts
'use server'

import { redirect } from 'next/navigation'
import { revalidateTag } from 'next/cache'
import { getUser } from '@/lib/dal'

export async function createProduct(formData: FormData) {
  const user = await getUser()
  if (!user || user.role !== 'admin') {
    throw new Error('Unauthorized')
  }

  const name = formData.get('name') as string
  const price = parseFloat(formData.get('price') as string)

  // Validate
  if (!name || name.length < 2) {
    return { error: 'Name must be at least 2 characters' }
  }
  if (isNaN(price) || price <= 0) {
    return { error: 'Price must be a positive number' }
  }

  // Create
  await db.products.create({
    data: { name, price },
  })

  revalidateTag('products')
  redirect('/products')
}
```

**Form component:**
```tsx
// components/features/CreateProductForm.tsx
'use client'

import { useActionState } from 'react'
import { createProduct } from '@/lib/actions'

export function CreateProductForm() {
  const [state, action, pending] = useActionState(createProduct, null)

  return (
    <form action={action}>
      <input name="name" placeholder="Product name" required />
      <input name="price" type="number" step="0.01" placeholder="Price" required />

      {state?.error && <p className="error">{state.error}</p>}

      <button type="submit" disabled={pending}>
        {pending ? 'Creating...' : 'Create Product'}
      </button>
    </form>
  )
}
```
</step>

<step name="6-add-loading-states">
<title>Add Loading States</title>

**Route-level loading:**
```tsx
// app/products/loading.tsx
export default function Loading() {
  return <div>Loading products...</div>
}
```

**Component-level with Suspense:**
```tsx
// app/products/page.tsx
import { Suspense } from 'react'
import { ProductList } from '@/components/features/ProductList'
import { ProductListSkeleton } from '@/components/features/ProductListSkeleton'

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductListSkeleton />}>
        <ProductList />
      </Suspense>
    </div>
  )
}
```
</step>

<step name="7-add-error-handling">
<title>Add Error Handling</title>

**Route-level error:**
```tsx
// app/products/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

**Server Action error handling:**
```tsx
export async function createProduct(formData: FormData) {
  try {
    // ... create product
    return { success: true }
  } catch (error) {
    console.error('Failed to create product:', error)
    return { error: 'Failed to create product. Please try again.' }
  }
}
```
</step>

<step name="8-verify-feature">
<title>Verify Feature</title>

```bash
# Check types
npx tsc --noEmit

# Run dev server
npm run dev

# Test the feature manually

# Build to catch any issues
npm run build
```

**Verify:**
- [ ] Feature works as expected
- [ ] Loading states show correctly
- [ ] Error states are handled
- [ ] Data updates after mutations
- [ ] No hydration errors
- [ ] Types pass
</step>

</process>

<anti_patterns>
**Avoid:**
- Adding `'use client'` to entire page when only small parts need interactivity
- Forgetting auth checks in Server Actions
- Not handling loading and error states
- Calling Server Actions from Server Components without proper boundaries
- Forgetting to revalidate cache after mutations
</anti_patterns>

<success_criteria>
Feature is complete when:
- [ ] Follows Server Component first approach
- [ ] Client Components are minimal and pushed down the tree
- [ ] Server Actions have auth checks
- [ ] Cache is properly invalidated after mutations
- [ ] Loading states are implemented
- [ ] Error handling is in place
- [ ] Types pass
- [ ] Feature works in dev and production build
</success_criteria>

</workflow>
