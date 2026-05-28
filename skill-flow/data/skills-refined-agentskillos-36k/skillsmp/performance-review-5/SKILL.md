---
name: performance-review
description: Analyze React/Next.js performance issues, N+1 queries, bundle size, and Core Web Vitals. Use when optimizing components, checking for slow renders, reviewing data fetching patterns, or when the app feels sluggish.
---

# Performance Review

Analyze code for performance issues targeting Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1).

## Scope

Review the specified files or components for:

### 1. React/Next.js Performance
- Unnecessary client components (should be server components)
- Missing `React.memo()`, `useMemo()`, `useCallback()` where beneficial
- Large component re-renders (check dependency arrays)
- Missing Suspense boundaries for async components
- Heavy components that should use `next/dynamic`
- Improper use of `use client` directive

### 2. Data Fetching
- N+1 query patterns in Drizzle queries
- Missing `Promise.all()` for parallel fetches
- Overfetching data (selecting unused columns)
- Missing React `cache()` for request deduplication
- Unnecessary waterfalls in data loading
- Missing or improper TanStack Query configuration

### 3. Bundle Size
- Large dependencies imported synchronously
- Missing code splitting opportunities
- Importing entire libraries vs. specific modules
- Dead code that should be removed

### 4. Database Performance
- Missing indexes on filtered/joined columns
- Inefficient query patterns
- Large result sets without pagination
- Missing connection pooling considerations

### 5. Rendering Performance
- Layout thrashing (reading then writing DOM)
- Missing virtualization for long lists (TanStack Virtual)
- Large images without optimization
- Missing `loading="lazy"` on images
- CSS that causes reflows

### 6. Caching
- Missing cache headers on API routes
- Opportunities for static generation
- Missing revalidation strategies
- Inefficient cache invalidation

## Output Format

For each finding:
```
[IMPACT: HIGH|MEDIUM|LOW]
File: path/to/file.ts:lineNumber
Issue: Brief description
Current: What's happening now
Recommended: How to optimize
Estimated Impact: Expected improvement
```

## Actions

1. Analyze component render patterns
2. Review Drizzle queries for N+1 patterns
3. Check for proper server/client component split
4. Identify parallelization opportunities
5. Review image and asset loading

## Post-Review

Generate a summary with:
- Quick wins (low effort, high impact)
- Medium-term optimizations
- Architectural improvements for long-term
