---
title: Server Components
impact: HIGH
impactDescription: Optimal rendering strategy - reduces client bundle, improves TTFB, enables streaming
tags: server-components, rsc, app-router, nextjs, rendering
---

# Server Components (HIGH)

Server Components patterns for Next.js App Router.

## Rule 1: Default to Server Components

**Only add 'use client' when necessary:**

```typescript
// ❌ INCORRECT - unnecessary client component
'use client'
export function UserProfile({ user }: { user: User }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}

// ✅ CORRECT - Server Component (default)
export function UserProfile({ user }: { user: User }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

**When to use 'use client':**
- Event handlers (onClick, onChange, etc.)
- useState, useEffect, useReducer
- Browser-only APIs (window, document)
- React Context consumers
- Third-party client libraries

## Rule 2: Push 'use client' to Leaves

**Minimize client component boundaries:**

```typescript
// ❌ INCORRECT - entire page becomes client
'use client'
export default function ProductPage({ product }: Props) {
  const [quantity, setQuantity] = useState(1)

  return (
    <div>
      <ProductInfo product={product} />      {/* Static - should be server */}
      <ProductReviews reviews={product.reviews} />  {/* Static */}
      <QuantitySelector value={quantity} onChange={setQuantity} />
      <AddToCartButton productId={product.id} quantity={quantity} />
    </div>
  )
}

// ✅ CORRECT - only interactive parts are client
export default function ProductPage({ product }: Props) {
  return (
    <div>
      <ProductInfo product={product} />      {/* Server Component */}
      <ProductReviews reviews={product.reviews} />  {/* Server Component */}
      <AddToCartSection product={product} />  {/* Client boundary here */}
    </div>
  )
}

// components/AddToCartSection.tsx
'use client'
export function AddToCartSection({ product }: Props) {
  const [quantity, setQuantity] = useState(1)
  return (
    <>
      <QuantitySelector value={quantity} onChange={setQuantity} />
      <AddToCartButton productId={product.id} quantity={quantity} />
    </>
  )
}
```

## Rule 3: Data Fetching in Server Components

**Fetch data directly in Server Components:**

```typescript
// ❌ INCORRECT - client-side fetching for static data
'use client'
export function UserList() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])

  return <List items={users} />
}

// ✅ CORRECT - Server Component with direct fetch
export async function UserList() {
  const users = await fetch('https://api.example.com/users', {
    next: { revalidate: 3600 } // Cache for 1 hour
  }).then(r => r.json())

  return <List items={users} />
}

// ✅ CORRECT - with database access
import { db } from '@/lib/db'

export async function UserList() {
  const users = await db.user.findMany()
  return <List items={users} />
}
```

## Rule 4: Streaming with Suspense

**Use Suspense for async Server Components:**

```typescript
// ❌ INCORRECT - blocks entire page
export default async function Page() {
  const slowData = await fetchSlowData()  // Blocks everything
  const fastData = await fetchFastData()

  return (
    <div>
      <FastSection data={fastData} />
      <SlowSection data={slowData} />
    </div>
  )
}

// ✅ CORRECT - stream with Suspense
export default function Page() {
  return (
    <div>
      <Suspense fallback={<FastSkeleton />}>
        <FastSection />
      </Suspense>
      <Suspense fallback={<SlowSkeleton />}>
        <SlowSection />  {/* Streams in when ready */}
      </Suspense>
    </div>
  )
}

async function SlowSection() {
  const data = await fetchSlowData()
  return <Content data={data} />
}
```

## Rule 5: Passing Data to Client Components

**Serialize only what's needed:**

```typescript
// ❌ INCORRECT - passing entire object with methods
export default async function Page() {
  const user = await getUser()  // Has methods, dates, etc.
  return <ClientComponent user={user} />  // Serialization fails
}

// ✅ CORRECT - pass only serializable data
export default async function Page() {
  const user = await getUser()

  return (
    <ClientComponent
      user={{
        id: user.id,
        name: user.name,
        email: user.email,
        createdAt: user.createdAt.toISOString(),  // Serialize dates
      }}
    />
  )
}

// ✅ BETTER - define a DTO type
type UserDTO = {
  id: string
  name: string
  email: string
  createdAt: string
}

function toUserDTO(user: User): UserDTO {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    createdAt: user.createdAt.toISOString(),
  }
}
```

## Rule 6: Composition Pattern

**Pass Server Components as children:**

```typescript
// ❌ INCORRECT - Server Component inside Client
'use client'
export function ClientWrapper() {
  return (
    <div>
      <ServerComponent />  {/* Won't work as expected */}
    </div>
  )
}

// ✅ CORRECT - children/slots pattern
'use client'
export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}  {/* Server Component passed as children */}
    </div>
  )
}

// In Server Component
export default function Page() {
  return (
    <ClientWrapper>
      <ServerComponent />  {/* This works! */}
    </ClientWrapper>
  )
}
```

## Rule 7: Server Actions for Mutations

**Use Server Actions for form handling:**

```typescript
// ✅ CORRECT - Server Action
// app/actions.ts
'use server'

export async function createUser(formData: FormData) {
  const name = formData.get('name')
  const email = formData.get('email')

  const user = await db.user.create({
    data: { name, email }
  })

  revalidatePath('/users')
  return user
}

// In Server Component
export default function Page() {
  return (
    <form action={createUser}>
      <input name="name" />
      <input name="email" />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Rule 8: Error and Loading States

**Use file conventions:**

```typescript
// app/users/loading.tsx
export default function Loading() {
  return <UserListSkeleton />
}

// app/users/error.tsx
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
      <button onClick={reset}>Try again</button>
    </div>
  )
}

// app/users/not-found.tsx
export default function NotFound() {
  return <div>User not found</div>
}
```

## Compliance Checklist

Before submitting code:

- [ ] Default to Server Components (no 'use client' unless needed)
- [ ] 'use client' pushed to leaf components
- [ ] Data fetching in Server Components
- [ ] Suspense for async components
- [ ] Only serializable data passed to Client Components
- [ ] Children pattern for Server/Client composition
- [ ] loading.tsx and error.tsx for route segments
