---
name: performance-optimization
version: 1.0.0
lastUpdated: 2026-01-18
description: Performance optimization patterns for Next.js applications. Covers bundle analysis, React rendering optimization, database query optimization, Core Web Vitals, image optimization, and caching strategies.
tags: [performance, bundle, react, optimization, core-web-vitals, caching]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to reduce bundle size
  - Optimize React rendering
  - Fix slow database queries
  - Improve Core Web Vitals
  - Implement virtualized lists
---

# Performance Optimization Skill

Performance optimization patterns for Next.js applications.

> **Reference Files:**
> - [bundle-analysis.md](./bundle-analysis.md) - Bundle size optimization
> - [react-rendering.md](./react-rendering.md) - React performance patterns
> - [database-optimization.md](./database-optimization.md) - Query optimization
> - [examples.md](./examples.md) - Practical examples

## Performance Philosophy

**Principles:**
1. **Measure first** - Never optimize without metrics
2. **Target bottlenecks** - Focus on the biggest impact areas
3. **User-centric** - Prioritize perceived performance
4. **Iterative** - Small, measurable improvements

## Quick Reference

### Bundle Size

```bash
# Analyze bundle
npm run analyze

# Targets
# - Total: < 200KB gzipped (first load)
# - Per-route: < 100KB gzipped
```

**Quick Wins:**
```typescript
// Dynamic imports for heavy components
const Chart = dynamic(() => import("./Chart"), { ssr: false });

// Tree-shakeable imports
import { debounce } from "lodash-es";  // ✅
import _ from "lodash";                 // ❌
```

### React Rendering

```typescript
// With React Compiler - usually automatic optimization
// Manual memoization only for:

// 1. External library callbacks
const stableHandler = useCallback(() => {}, []);

// 2. Context values
const value = useMemo(() => ({ state, dispatch }), [state]);

// 3. Virtualized lists (50+ items)
import { useVirtualizer } from "@tanstack/react-virtual";
```

### Database Queries

```typescript
// Always use limits
const query = db.collection("items")
  .where("userId", "==", userId)
  .limit(20);

// Parallel fetching
const [users, posts] = await Promise.all([
  getUsers(),
  getPosts()
]);
```

### Core Web Vitals

| Metric | Target | Optimization |
|--------|--------|--------------|
| **LCP** | < 2.5s | `priority` on hero image, preload fonts |
| **INP** | < 200ms | `startTransition`, defer non-critical JS |
| **CLS** | < 0.1 | Fixed dimensions, skeleton loaders |

## Performance Targets

### Bundle Size Targets

| Category | Target (gzipped) |
|----------|------------------|
| First Load JS | < 100KB |
| Per-page JS | < 50KB |
| Total app | < 300KB |
| Single dependency | < 30KB |

### Runtime Targets

| Metric | Good | Needs Work |
|--------|------|------------|
| Time to Interactive | < 3s | > 5s |
| First Contentful Paint | < 1.8s | > 3s |
| Server Response | < 200ms | > 500ms |
| Database Query | < 100ms | > 500ms |

## Analysis Commands

```bash
# Bundle analysis
npm run analyze

# Build output
npm run build
# Check .next/static/chunks sizes

# Lighthouse (via Chrome DevTools)
# Performance tab → Lighthouse

# React Profiler
# React DevTools → Profiler tab
```

## Decision Tree

```
Performance Issue?
    │
    ├─ Slow page load?
    │   ├─ Large bundle → Bundle analysis
    │   ├─ Slow API → Database optimization
    │   └─ Render blocking → Code splitting
    │
    ├─ Slow interactions?
    │   ├─ Long lists → Virtualization
    │   ├─ Heavy computation → Web Worker / useMemo
    │   └─ Frequent re-renders → React Profiler
    │
    └─ Layout shifts?
        ├─ Images → Set dimensions
        ├─ Fonts → Font preloading
        └─ Dynamic content → Skeleton loaders
```

## Common Issues & Solutions

| Issue | Detection | Solution |
|-------|-----------|----------|
| Large bundle | > 100KB first load | Dynamic imports, tree shaking |
| Slow renders | React Profiler > 16ms | Memoization, virtualization |
| N+1 queries | Multiple sequential DB calls | Batch queries, denormalization |
| Layout shift | CLS > 0.1 | Fixed dimensions, skeletons |
| Unoptimized images | Large image files | next/image, WebP, responsive |

## Related Skills

- `react-19-compiler` - React Compiler optimization guidance
- `firebase-firestore` - Database query patterns
- `structured-logging` - Performance logging
