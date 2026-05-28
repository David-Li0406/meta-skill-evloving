---
name: react-nextjs-performance-optimization
description: Use this skill when writing, reviewing, or refactoring React and Next.js code to ensure optimal performance patterns and reduce bottlenecks.
---

# React and Next.js Performance Optimization

Comprehensive performance optimization guide for React and Next.js applications, containing 45 rules across 8 categories. These rules are prioritized by impact to guide automated refactoring and code generation.

## When to Use This Skill

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Eliminating Waterfalls | CRITICAL |
| 2 | Bundle Size Optimization | CRITICAL |
| 3 | Server-Side Performance | HIGH |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH |
| 5 | Re-render Optimization | MEDIUM |
| 6 | Rendering Performance | MEDIUM |
| 7 | JavaScript Performance | LOW-MEDIUM |
| 8 | Advanced Patterns | LOW |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- **Defer await until needed**: Move await into branches where they're used.
- **Use Promise.all()**: Parallelize independent async operations.
- **Start promises early, await late**: Optimize API routes to prevent blocking.
- **Use Suspense boundaries**: Stream content while loading.

### 2. Bundle Size Optimization (CRITICAL)

- **Avoid barrel imports**: Import directly from source files to enable tree-shaking.
- **Use dynamic imports**: Lazy-load heavy components with `next/dynamic`.
- **Defer non-critical libraries**: Load analytics or logging after hydration.
- **Preload based on user intent**: Improve perceived speed by preloading resources.

### 3. Server-Side Performance (HIGH)

- **Use React.cache()**: Deduplicate requests across components.
- **Implement LRU caching**: Optimize cross-request caching.
- **Minimize serialization**: Reduce data passed to client components.
- **Parallelize data fetching**: Restructure components to fetch data concurrently.

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- **Use SWR for deduplication**: Automatically deduplicate requests.
- **Deduplicate global event listeners**: Optimize event handling.

### 5. Re-render Optimization (MEDIUM)

- **Extract expensive computations**: Use memoization to avoid unnecessary recalculations.
- **Stabilize callback references**: Use functional updates for state management.
- **Colocate state**: Keep state close to where it's used to minimize updates.

### 6. Rendering Performance (MEDIUM)

- **Animate wrappers instead of elements**: Optimize animations for better performance.
- **Use content-visibility**: Improve rendering of long lists.
- **Prevent hydration mismatch**: Use inline scripts for client-only data.

### 7. JavaScript Performance (LOW-MEDIUM)

- **Batch DOM changes**: Group CSS changes to minimize reflows.
- **Cache repeated lookups**: Use Maps for efficient data access.
- **Optimize loops**: Use efficient array methods and early exits.

### 8. Advanced Patterns (LOW)

- **Store event handlers in refs**: Avoid unnecessary re-renders.
- **Use stable callback refs**: Implement `useLatest` for consistent references.

## Implementation Approach

1. **Profile first**: Use React DevTools and browser performance tools to identify bottlenecks.
2. **Focus on critical paths**: Start with eliminating waterfalls and reducing bundle size.
3. **Measure impact**: Verify improvements with metrics like Time to Interactive (TTI) and Largest Contentful Paint (LCP).
4. **Apply incrementally**: Avoid over-optimizing prematurely.
5. **Test thoroughly**: Ensure optimizations do not break functionality.

## Common Pitfalls to Avoid

- **Don't** use barrel imports from large libraries.
- **Don't** block parallel operations with sequential awaits.
- **Do** use Promise.all() for independent operations.
- **Do** memoize expensive components and lazy-load non-critical code.

## Resources

- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
- [SWR Documentation](https://swr.vercel.app)

## Conclusion

These guidelines are designed to help you optimize React and Next.js applications effectively. By following the prioritized rules and focusing on measurable improvements, you can enhance performance and user experience significantly.