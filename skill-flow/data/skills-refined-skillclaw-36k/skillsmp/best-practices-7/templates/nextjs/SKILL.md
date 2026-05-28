---
name: best-practices
description: Next.js performance optimization guidelines (Vercel official patterns)
license: MIT
metadata:
  author: devnogari
  project_type: nextjs
  extends: vercel-react-best-practices
---

# Next.js Best Practices

Performance optimization and best practices for Next.js applications, **powered by Vercel Engineering's official guidelines**.

## Primary Reference

**This skill extends `/vercel-react-best-practices`** - Vercel's official 45-rule guide for React & Next.js performance.

Since Next.js is Vercel's framework, **always invoke `/vercel-react-best-practices` first** for comprehensive patterns. This skill provides Next.js App Router-specific extensions.

## Routing to Vercel Best Practices

For these patterns, **use `/vercel-react-best-practices` directly**:

| Pattern | Vercel Rule Category | Key Rules |
|---------|---------------------|-----------|
| Async waterfalls | `async-*` | `async-parallel`, `async-suspense-boundaries` |
| Bundle optimization | `bundle-*` | `bundle-barrel-imports`, `bundle-dynamic-imports` |
| Server performance | `server-*` | `server-cache-react`, `server-serialization` |
| Re-render prevention | `rerender-*` | `rerender-memo`, `rerender-transitions` |
| JavaScript perf | `js-*` | `js-set-map-lookups`, `js-early-exit` |

## Activation Triggers

This skill activates when:
- Writing new pages, layouts, or components
- Implementing data fetching (Server Components, API routes)
- Optimizing bundle size or Core Web Vitals
- Reviewing or refactoring Next.js code
- Debugging performance or hydration issues

## Rule Categories

### Priority Order

| # | Category | Priority | Typical Impact |
|---|----------|----------|----------------|
| 1 | Eliminating Waterfalls | CRITICAL | 2-10x improvement |
| 2 | Bundle Size Optimization | CRITICAL | 200-800ms LCP reduction |
| 3 | Server-Side Performance | HIGH | TTFB improvement |
| 4 | Client-Side Optimization | MEDIUM-HIGH | INP improvement |
| 5 | Caching Strategies | MEDIUM | Server load reduction |

## Quick Reference

### Eliminating Waterfalls (CRITICAL)

**Parallel data fetching:**
```typescript
// ❌ INCORRECT - sequential fetches (3 round trips)
async function Page() {
  const user = await getUser()
  const posts = await getPosts(user.id)
  const comments = await getComments(posts[0].id)
  return <Content user={user} posts={posts} comments={comments} />
}

// ✅ CORRECT - parallel fetches (1 round trip)
async function Page() {
  const [user, posts] = await Promise.all([
    getUser(),
    getPosts()
  ])
  const comments = await getComments(posts[0].id)
  return <Content user={user} posts={posts} comments={comments} />
}
```

**Use Suspense boundaries:**
```typescript
// ❌ INCORRECT - blocks entire page
async function Page() {
  const data = await slowFetch()  // blocks render
  return <Content data={data} />
}

// ✅ CORRECT - stream with Suspense
async function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <SlowContent />
    </Suspense>
  )
}

async function SlowContent() {
  const data = await slowFetch()
  return <Content data={data} />
}
```

### Bundle Optimization (CRITICAL)

**Configure optimizePackageImports:**
```typescript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-icons',
      '@mui/material',
      'lodash-es'
    ]
  }
}
```

**Dynamic imports for heavy components:**
```typescript
// ❌ INCORRECT - imports in main bundle
import { Chart } from 'chart.js'
import { Editor } from '@monaco-editor/react'

// ✅ CORRECT - dynamic imports
const Chart = dynamic(() => import('./Chart'), { ssr: false })
const Editor = dynamic(() => import('@monaco-editor/react'), {
  loading: () => <EditorSkeleton />
})
```

### Server Components (HIGH)

**Default to Server Components:**
```typescript
// ❌ INCORRECT - unnecessary 'use client'
'use client'
export function UserProfile({ user }) {
  return <div>{user.name}</div>  // no interactivity needed
}

// ✅ CORRECT - Server Component
export function UserProfile({ user }) {
  return <div>{user.name}</div>
}
```

**Push 'use client' to leaves:**
```typescript
// ❌ INCORRECT - entire tree becomes client
'use client'
export function ProductPage({ product }) {
  return (
    <div>
      <ProductDetails product={product} />
      <AddToCartButton />
    </div>
  )
}

// ✅ CORRECT - only button is client
export function ProductPage({ product }) {
  return (
    <div>
      <ProductDetails product={product} />
      <AddToCartButton />  {/* only this is 'use client' */}
    </div>
  )
}
```

### Caching (MEDIUM)

**Use React cache for deduplication:**
```typescript
import { cache } from 'react'

// ❌ INCORRECT - duplicate fetches
async function getUser(id) {
  return fetch(`/api/users/${id}`)
}

// ✅ CORRECT - cached and deduplicated
const getUser = cache(async (id: string) => {
  return fetch(`/api/users/${id}`)
})
```

**Configure fetch caching:**
```typescript
// Static data (default)
fetch('https://api.example.com/data')

// Revalidate every hour
fetch('https://api.example.com/data', { next: { revalidate: 3600 } })

// Dynamic data
fetch('https://api.example.com/data', { cache: 'no-store' })
```

## Detailed Rules

See individual rule files in `rules/` directory:
- `eliminating-waterfalls.md`
- `bundle-optimization.md`
- `server-components.md`
- `client-components.md`
- `caching-strategies.md`
- `image-optimization.md`

## App Router Patterns

**Layouts for shared UI:**
```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>{children}</main>
    </div>
  )
}
```

**Loading states:**
```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />
}
```

**Error boundaries:**
```typescript
// app/dashboard/error.tsx
'use client'
export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

## Workflow Integration

When implementing Next.js features:

1. **First**: Invoke `/vercel-react-best-practices` for Vercel's official patterns
2. **Then**: Apply App Router-specific patterns from this file
3. **Review**: Check against Vercel's `server-*` and `async-*` rules

```
/vercel-react-best-practices → Core React + Next.js patterns (45 rules)
     ↓
This skill → App Router specifics (layouts, loading, error handling)
```

## Quick Vercel Rules Reference

Most impactful rules for Next.js (from `/vercel-react-best-practices`):

| Rule | Impact | When to Apply |
|------|--------|---------------|
| `async-suspense-boundaries` | CRITICAL | Slow async components |
| `server-cache-react` | HIGH | Repeated data fetches |
| `bundle-dynamic-imports` | CRITICAL | Heavy client components |
| `server-serialization` | HIGH | Large props to client |
| `async-parallel` | CRITICAL | Multiple independent fetches |
