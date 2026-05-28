---
name: react-performance
description: React and Next.js performance optimization from Vercel Engineering. 45 rules across 8 categories covering async waterfalls, bundle size, server-side performance, re-renders, and rendering optimization. Use when writing, reviewing, or optimizing React/Next.js code.
---

# React Performance Optimization

**Philosophy:** Performance is a feature. Every millisecond matters for user experience and conversion. Prevent performance regressions through systematic rule application, not reactive optimization.

---

## Rule Categories by Priority

| Priority | Category | Prefix | Rules | Impact |
|----------|----------|--------|-------|--------|
| CRITICAL | Eliminating Waterfalls | `async-` | 5 | Blocks rendering, causes cascading delays |
| CRITICAL | Bundle Size Optimization | `bundle-` | 5 | Affects initial load, TTI, LCP |
| HIGH | Server-Side Performance | `server-` | 5 | RSC efficiency, caching, streaming |
| HIGH | Re-render Optimization | `rerender-` | 8 | UI responsiveness, CPU usage |
| MEDIUM | Rendering Performance | `render-` | 7 | Paint performance, layout thrashing |
| MEDIUM | JavaScript Performance | `js-` | 12 | Runtime efficiency, memory |
| LOW | Network Optimization | `network-` | 2 | Request efficiency |
| LOW | Memory Management | `memory-` | 1 | Memory leaks, GC pressure |

---

## Quick Reference

### Eliminating Waterfalls (async-)

| Rule | Description |
|------|-------------|
| `async-parallel` | Use Promise.all for independent operations |
| `async-preload` | Preload data before navigation |
| `async-streaming` | Stream responses with Suspense boundaries |
| `async-prefetch` | Prefetch likely next pages |
| `async-deferred` | Defer non-critical data fetching |

### Bundle Size Optimization (bundle-)

| Rule | Description |
|------|-------------|
| `bundle-barrel-imports` | Use direct imports, avoid barrel files |
| `bundle-dynamic-imports` | Lazy load with next/dynamic |
| `bundle-tree-shaking` | Ensure proper tree-shaking |
| `bundle-external-deps` | Analyze and minimize dependencies |
| `bundle-code-splitting` | Split by route and feature |

### Server-Side Performance (server-)

| Rule | Description |
|------|-------------|
| `server-cache-react` | Use React.cache for request deduplication |
| `server-cache-next` | Use unstable_cache for cross-request caching |
| `server-streaming` | Stream long-running operations |
| `server-edge` | Use Edge Runtime when possible |
| `server-ppr` | Enable Partial Prerendering |

### Re-render Optimization (rerender-)

| Rule | Description |
|------|-------------|
| `rerender-memo` | Extract expensive computations |
| `rerender-callback` | Stabilize callback references |
| `rerender-context` | Split contexts by update frequency |
| `rerender-state-colocation` | Keep state close to usage |
| `rerender-derived` | Derive state instead of syncing |
| `rerender-ref` | Use refs for values that don't need renders |
| `rerender-children` | Use children prop for composition |
| `rerender-key` | Use stable, meaningful keys |

### Rendering Performance (render-)

| Rule | Description |
|------|-------------|
| `render-virtualize` | Virtualize long lists |
| `render-css-containment` | Use CSS containment |
| `render-layout-thrashing` | Batch DOM reads and writes |
| `render-transform` | Prefer transform over layout properties |
| `render-will-change` | Use will-change sparingly |
| `render-layers` | Manage compositor layers |
| `render-paint` | Minimize paint areas |

### JavaScript Performance (js-)

| Rule | Description |
|------|-------------|
| `js-debounce` | Debounce frequent events |
| `js-throttle` | Throttle continuous events |
| `js-web-worker` | Offload heavy computation |
| `js-idle-callback` | Schedule non-urgent work |
| `js-intersection` | Use IntersectionObserver |
| `js-resize` | Use ResizeObserver |
| `js-passive` | Use passive event listeners |
| `js-delegation` | Use event delegation |
| `js-loop` | Optimize loop operations |
| `js-object-pooling` | Reuse objects in hot paths |
| `js-string-concat` | Use template literals |
| `js-array-methods` | Choose optimal array methods |

---

## Critical Rule Patterns

### async-parallel: Promise.all for Independent Operations

```typescript
// BAD: Sequential waterfall
async function loadDashboard() {
  const user = await fetchUser()
  const posts = await fetchPosts()
  const notifications = await fetchNotifications()
  return { user, posts, notifications }
}

// GOOD: Parallel execution
async function loadDashboard() {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchNotifications(),
  ])
  return { user, posts, notifications }
}
```

### bundle-barrel-imports: Direct Imports

```typescript
// BAD: Barrel import pulls entire module
import { Button } from '@/components'
import { formatDate } from '@/utils'

// GOOD: Direct imports enable tree-shaking
import { Button } from '@/components/ui/button'
import { formatDate } from '@/utils/date'
```

### bundle-dynamic-imports: next/dynamic

```typescript
// BAD: Static import of heavy component
import { CodeEditor } from '@/components/code-editor'

// GOOD: Dynamic import with loading state
import dynamic from 'next/dynamic'

const CodeEditor = dynamic(
  () => import('@/components/code-editor'),
  {
    loading: () => <EditorSkeleton />,
    ssr: false, // Client-only component
  }
)
```

### server-cache-react: React.cache for Deduplication

```typescript
import { cache } from 'react'

// Deduplicated across component tree in single request
export const getUser = cache(async (id: string) => {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
})

// Multiple components can call getUser(id) - only one fetch
```

### rerender-memo: Extract Expensive Work

```typescript
// BAD: Recalculates on every render
function Dashboard({ items }) {
  const sorted = items.sort((a, b) => b.priority - a.priority)
  const filtered = sorted.filter(item => item.active)
  const total = filtered.reduce((sum, item) => sum + item.value, 0)
  
  return <DashboardView items={filtered} total={total} />
}

// GOOD: Memoized expensive computation
function Dashboard({ items }) {
  const { filtered, total } = useMemo(() => {
    const sorted = [...items].sort((a, b) => b.priority - a.priority)
    const filtered = sorted.filter(item => item.active)
    const total = filtered.reduce((sum, item) => sum + item.value, 0)
    return { filtered, total }
  }, [items])
  
  return <DashboardView items={filtered} total={total} />
}
```

---

## Adherence Checklist

Before completing your task, verify:

- [ ] **Waterfalls:** Are independent async operations parallelized?
- [ ] **Imports:** Are imports direct (not barrel) for tree-shaking?
- [ ] **Dynamic:** Are heavy/optional components dynamically imported?
- [ ] **Caching:** Is React.cache used for request deduplication?
- [ ] **Memoization:** Are expensive computations memoized?
- [ ] **State:** Is state colocated near its usage?
- [ ] **Lists:** Are long lists virtualized?
- [ ] **Events:** Are frequent events debounced/throttled?

---

## Extended Reference

See [references/rules.md](references/rules.md) for complete rule explanations with code examples for all 45 rules.
