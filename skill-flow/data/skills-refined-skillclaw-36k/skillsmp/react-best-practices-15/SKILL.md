---
name: react-best-practices
description: React 19+ performance optimization guidelines for modern React applications without framework dependencies. This skill should be used when writing, reviewing, or refactoring React code to ensure optimal performance patterns. Triggers on tasks involving React components, hooks, data fetching, bundle optimization, or performance improvements.
license: MIT
metadata:
  author: do-ob
  version: "1.0.0"
---

# React 19+ Performance Best Practices

Comprehensive performance optimization guide for React 19+ applications. Contains 35+ rules across 7 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or hooks
- Implementing data fetching (client-side)
- Reviewing code for performance issues
- Refactoring existing React code
- Optimizing bundle size or load times
- Working with React 19+ features (use(), Activity, etc.)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 4 | Re-render Optimization | MEDIUM | `rerender-` |
| 5 | Rendering Performance | MEDIUM | `rendering-` |
| 6 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 7 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-suspense-boundaries` - Use Suspense + use() hook to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use React.lazy() for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR/TanStack Query for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners
- `client-passive-event-listeners` - Use passive listeners for scroll performance
- `client-localstorage-schema` - Version and minimize localStorage data

### 4. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-memo-with-default-value` - Extract default non-primitive values to constants
- `rerender-simple-expression-in-memo` - Don't wrap simple expressions in useMemo
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-transitions` - Use startTransition for non-urgent updates

### 5. Rendering Performance (MEDIUM)

- `rendering-activity` - Use Activity component for show/hide (React 19)
- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-conditional-render` - Use ternary, not && for conditionals
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-hydration-no-flicker` - Prevent hydration mismatch without flickering
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-usetransition-loading` - Use useTransition over manual loading states

### 6. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Avoid layout thrashing with batched DOM operations
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

### 7. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-use-latest` - useEffectEvent for stable callback refs (experimental)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `SKILL.md`

## Key Differences from Next.js Version

This skill focuses on pure React 19+ without framework-specific features:

- Uses `React.lazy()` instead of `next/dynamic`
- Client-side data fetching with SWR/TanStack Query
- No server-side rendering optimizations
- No API route patterns
- Emphasizes modern React 19 features (`use()` hook, `Activity` component)
- Framework-agnostic bundler configuration (Vite, webpack, etc.)

## React 19+ Specific Features

This guide includes React 19-specific optimizations:

- **`use()` hook** - For unwrapping promises in Suspense boundaries
- **`Activity` component** - For preserving state/DOM on visibility toggle
- **Async transitions** - Enhanced useTransition with async support
- **Experimental `useEffectEvent`** - For stable callback references
