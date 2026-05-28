---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code.
---

# React Best Practices

Performance optimization guide with 40+ rules across 8 categories. For detailed rules with code examples, see [references/react-performance-guidelines.md](references/react-performance-guidelines.md).

## Priority by Impact

| Priority | Category                  | Impact      |
| -------- | ------------------------- | ----------- |
| 1        | Eliminating Waterfalls    | CRITICAL    |
| 2        | Bundle Size Optimization  | CRITICAL    |
| 3        | Server-Side Performance   | HIGH        |
| 4        | Client-Side Data Fetching | MEDIUM-HIGH |
| 5        | Re-render Optimization    | MEDIUM      |
| 6        | Rendering Performance     | MEDIUM      |
| 7        | JavaScript Performance    | LOW-MEDIUM  |

## Critical Patterns (Apply First)

**Eliminate Waterfalls:**

- Defer await until needed (move into branches)
- Use `Promise.all()` for independent async operations
- Start promises early, await late
- Use Suspense boundaries to stream content

**Reduce Bundle Size:**

- Avoid barrel file imports (import directly from source)
- Use `next/dynamic` for heavy components
- Defer non-critical third-party libraries
- Preload based on user intent

## High-Impact Server Patterns

- Use `React.cache()` for per-request deduplication
- Minimize serialization at RSC boundaries
- Parallelize data fetching with component composition

## Medium-Impact Client Patterns

- Use SWR for automatic request deduplication
- Defer state reads to usage point
- Use lazy state initialization for expensive values
- Apply `startTransition` for non-urgent updates

## Rendering Patterns

- Animate SVG wrappers, not SVG elements directly
- Use `content-visibility: auto` for long lists
- Prevent hydration mismatch with inline scripts
- Use explicit conditional rendering (`? :` not `&&`)

## JavaScript Patterns

- Batch DOM CSS changes via classes
- Build index maps for repeated lookups
- Use `toSorted()` instead of `sort()` for immutability
- Early length check for array comparisons
