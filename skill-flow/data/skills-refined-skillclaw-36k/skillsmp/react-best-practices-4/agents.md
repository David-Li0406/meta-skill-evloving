# React Best Practices

**Version 0.1.0** - Vercel Engineering

> AI-assisted React/Next.js 最適化ガイド（圧縮版）
> 詳細なコード例はContext7の`/vercel/next.js`を参照

---

## 目次

1. [Eliminating Waterfalls](#1-eliminating-waterfalls) — **CRITICAL**
2. [Bundle Size Optimization](#2-bundle-size-optimization) — **CRITICAL**
3. [Server-Side Performance](#3-server-side-performance) — **HIGH**
4. [Client-Side Data Fetching](#4-client-side-data-fetching) — **MEDIUM-HIGH**
5. [Re-render Optimization](#5-re-render-optimization) — **MEDIUM**
6. [Rendering Performance](#6-rendering-performance) — **MEDIUM**
7. [JavaScript Performance](#7-javascript-performance) — **LOW-MEDIUM**
8. [Advanced Patterns](#8-advanced-patterns) — **LOW**

---

## 1. Eliminating Waterfalls

**Impact: CRITICAL** - Waterfalls are the #1 performance killer.

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 1.1 Defer Await Until Needed | Move `await` into branches where needed | Avoid blocking unused code paths |
| 1.2 Dependency-Based Parallelization | Use `better-all` for partial dependencies | 2-10× improvement |
| 1.3 Prevent Waterfall in API Routes | Start independent operations immediately | Don't await until needed |
| 1.4 Promise.all() for Independent Ops | Execute concurrently with `Promise.all()` | 3 round trips → 1 |
| 1.5 Strategic Suspense Boundaries | Use `<Suspense>` for non-blocking UI | Faster initial paint |

**Key Pattern:**
```typescript
// Bad: sequential
const user = await fetchUser()
const posts = await fetchPosts()

// Good: parallel
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()])
```

---

## 2. Bundle Size Optimization

**Impact: CRITICAL** - Reduces TTI and LCP.

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 2.1 Avoid Barrel File Imports | Import directly from source | 200-800ms import cost savings |
| 2.2 Conditional Module Loading | Load large data when feature activated | Lazy-load on demand |
| 2.3 Defer Third-Party Libraries | Load analytics after hydration | `ssr: false` |
| 2.4 Dynamic Imports | `next/dynamic` for heavy components | Monaco: 300KB savings |
| 2.5 Preload on User Intent | Preload on hover/focus | Reduces perceived latency |

**Key Pattern:**
```typescript
// Bad: imports entire library (1,583 modules)
import { Check } from 'lucide-react'

// Good: direct import (1 module)
import Check from 'lucide-react/dist/esm/icons/check'

// Alternative: Next.js config
optimizePackageImports: ['lucide-react', '@mui/material']
```

---

## 3. Server-Side Performance

**Impact: HIGH**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 3.1 Cross-Request LRU Caching | Use LRU cache for cross-request data | `lru-cache` library |
| 3.2 Minimize RSC Serialization | Only pass fields client uses | Size matters at boundary |
| 3.3 Parallel Fetching with Composition | Restructure RSC for parallelism | Eliminate server waterfalls |
| 3.4 React.cache() | Per-request deduplication | Single request only |
| 3.5 Use after() | Non-blocking post-response work | Analytics, logging |

**Key Pattern:**
```typescript
// Minimize serialization
// Bad: passes 50 fields
return <Profile user={user} />

// Good: passes 1 field
return <Profile name={user.name} />
```

---

## 4. Client-Side Data Fetching

**Impact: MEDIUM-HIGH**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 4.1 Deduplicate Event Listeners | `useSWRSubscription()` for shared listeners | N instances = 1 listener |
| 4.2 Use SWR | Automatic deduplication & caching | Multiple instances share 1 request |

---

## 5. Re-render Optimization

**Impact: MEDIUM**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 5.1 Defer State Reads | Read on demand in callbacks | Avoid unnecessary subscriptions |
| 5.2 Extract to Memoized Components | Enable early returns before computation | Skip work when loading |
| 5.3 Narrow Effect Dependencies | Use primitives, not objects | `[user.id]` not `[user]` |
| 5.4 Subscribe to Derived State | Boolean instead of continuous values | `useMediaQuery` not `useWindowWidth` |
| 5.5 Functional setState | `setCurr => curr.filter(...)` | Stable callbacks, no stale closures |
| 5.6 Lazy State Initialization | `useState(() => expensive())` | Runs only once |
| 5.7 Use Transitions | `startTransition` for non-urgent updates | Maintains UI responsiveness |

---

## 6. Rendering Performance

**Impact: MEDIUM**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 6.1 Animate SVG Wrapper | Wrap SVG in `<div>` for animation | Hardware acceleration |
| 6.2 CSS content-visibility | `content-visibility: auto` | Skip off-screen rendering |
| 6.3 Hoist Static JSX | Extract outside components | Avoids re-creation |
| 6.4 Optimize SVG Precision | Reduce decimal places | `npx svgo --precision=1` |
| 6.5 Prevent Hydration Mismatch | Inline script for localStorage | No flicker |
| 6.6 Activity Component | `<Activity mode="hidden">` | Preserves state/DOM |
| 6.7 Explicit Conditional Rendering | `count > 0 ? ... : null` | Prevents rendering 0/NaN |

---

## 7. JavaScript Performance

**Impact: LOW-MEDIUM**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 7.1 Batch DOM CSS Changes | Use classes or `cssText` | Single reflow |
| 7.2 Build Index Maps | `new Map(users.map(...))` | O(1) lookups |
| 7.3 Cache Property Access | Hoist out of loops | `const len = arr.length` |
| 7.4 Cache Function Calls | Module-level Map cache | Avoid redundant computation |
| 7.5 Cache Storage API | Cache localStorage reads | Reduce expensive I/O |
| 7.6 Combine Array Iterations | Single loop for multiple filters | 3 iterations → 1 |
| 7.7 Early Length Check | Check `arr.length` first | Avoid expensive ops when lengths differ |
| 7.8 Early Return | Return on first error | Skip unnecessary processing |
| 7.9 Hoist RegExp | `useMemo` or module scope | Avoid recreation |
| 7.10 Loop for Min/Max | Single pass, no sort | O(n) vs O(n log n) |
| 7.11 Set/Map for Lookups | `new Set([...]).has()` | O(1) vs O(n) |
| 7.12 toSorted() | Immutable sort | Prevents React state mutation bugs |

---

## 8. Advanced Patterns

**Impact: LOW**

| Rule | Description | Key Insight |
|------|-------------|-------------|
| 8.1 Store Handlers in Refs | `useEffectEvent` or ref pattern | Stable subscriptions |
| 8.2 useLatest | Access latest values without deps | Prevents effect re-runs |

---

## Critical Patterns（必ず覚えるべき5パターン）

| # | パターン | ❌ Bad | ✅ Good |
|---|---------|--------|---------|
| 1 | Defer Await | `await fetch(); if(skip) return` | `if(skip) return; await fetch()` |
| 2 | Dynamic Import | `import { Heavy } from './heavy'` | `dynamic(() => import('./heavy'), {ssr:false})` |
| 3 | Functional setState | `setItems(items.filter(...)), [items]` | `setItems(curr => curr.filter(...)), []` |
| 4 | Lazy State Init | `useState(expensive())` | `useState(() => expensive())` |
| 5 | Parallel RSC | `const h = await fetchH(); <H data={h}/>` | `async function H() { await fetchH() }; <H/>` |

**詳細**: Context7 `/vercel/next.js` で `Promise.all`, `next/dynamic`, `useCallback functional` を検索

---

## Quick Reference

### Critical (Must Do)

1. **Promise.all()** for independent async operations
2. **Direct imports** instead of barrel files
3. **next/dynamic** for heavy components
4. **Suspense boundaries** for streaming

### High Priority

5. **React.cache()** for per-request deduplication
6. **LRU cache** for cross-request data
7. **Minimize RSC serialization**
8. **SWR** for client-side data fetching

### Medium Priority

9. **Functional setState** for stable callbacks
10. **Lazy state initialization**
11. **Narrow effect dependencies**
12. **content-visibility** for long lists

---

## References

- [React Docs](https://react.dev)
- [Next.js Docs](https://nextjs.org)
- [SWR](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [Vercel Blog: Package Imports Optimization](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [Vercel Blog: Dashboard Performance](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

> **Note:** For detailed code examples and patterns, use Context7 with `/vercel/next.js` library.
