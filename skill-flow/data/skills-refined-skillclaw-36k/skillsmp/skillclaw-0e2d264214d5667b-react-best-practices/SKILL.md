---
name: react-best-practices
description: Use this skill when writing, reviewing, or refactoring React and Next.js code to ensure optimal performance patterns and eliminate bottlenecks.
---

# React Best Practices - Performance Optimization

Comprehensive performance optimization guide for React and Next.js applications, containing 45 rules organized by priority and impact. This skill is designed to help developers eliminate performance bottlenecks and follow best practices.

## When to Use

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

### Critical Patterns (Apply First)

**Eliminating Waterfalls:**
- Defer await until needed (move into branches where they're used)
- Use `Promise.all()` for independent async operations
- Start promises early, await late
- Use Suspense boundaries to stream content

**Bundle Size Optimization:**
- Avoid barrel file imports (import directly from source files)
- Use `next/dynamic` for heavy components
- Defer non-critical third-party libraries
- Preload based on user intent

### High-Impact Server Patterns

- Use `React.cache()` for per-request deduplication
- Use LRU cache for cross-request caching
- Minimize serialization at RSC boundaries
- Parallelize data fetching with component composition

### Medium-Impact Client Patterns

- Use SWR for automatic request deduplication
- Defer state reads to usage point
- Use lazy loading for non-critical components

### Additional Considerations

- Prioritize user-perceived performance and developer ergonomics.
- Optimize the critical path first (waterfalls, bundle size, server-side latency), then address re-renders and micro-optimizations only when they are measurable.
- Use data to pick the smallest fix that moves the metric.