# Server-Side Performance

**Impact: HIGH** | Optimizing server-side rendering and data fetching eliminates waterfalls and reduces response times.

---

## 1. Per-Request Deduplication with React.cache()

Deduplicate server-side queries within a single request.

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({ where: { id: session.user.id } })
})

// Multiple calls execute query only once per request
```

---

## 2. Cross-Request LRU Caching

`React.cache()` only works within one request. Use LRU cache for data shared across requests.

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000 // 5 minutes
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}
```

> For serverless, consider Redis for cross-process caching.

---

## 3. Parallel Data Fetching with Component Composition

React Server Components execute sequentially. Restructure with composition to parallelize.

```tsx
// BAD: Sidebar waits for Page's fetch
export default async function Page() {
  const header = await fetchHeader()
  return <div><div>{header}</div><Sidebar /></div>
}

// GOOD: both fetch simultaneously
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

export default function Page() {
  return <div><Header /><Sidebar /></div>
}
```

---

## 4. Minimize Serialization at RSC Boundaries

Only pass fields that the client actually uses.

```tsx
// BAD: serializes all 50 user fields
async function Page() {
  const user = await fetchUser()
  return <Profile user={user} />
}

// GOOD: serializes only 1 field
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```
