---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# React Best Practices

## Overview

Comprehensive performance optimization guide for React and Next.js applications, containing 40+ rules across 8 categories. Rules are prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Priority-Ordered Guidelines

Rules are prioritized by impact:

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

**Eliminate Waterfalls:**
- Defer await until needed (move into branches)
- Use `Promise.all()` for independent async operations
- Start promises early, await late
- Use `better-all` for partial dependencies
- Use Suspense boundaries to stream content

**Reduce Bundle Size:**
- Avoid barrel file imports (import directly from source)
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
- Use lazy state initialization for expensive values
- Use derived state subscriptions
- Apply `startTransition` for non-urgent updates

### Rendering Patterns

- Animate SVG wrappers, not SVG elements directly
- Use `content-visibility: auto` for long lists
- Prevent hydration mismatch with inline scripts
- Use explicit conditional rendering (`? :` not `&&`)

### JavaScript Patterns

- Batch DOM CSS changes via classes
- Build index maps for repeated lookups
- Cache repeated function calls
- Use `toSorted()` instead of `sort()` for immutability
- Early length check for array comparisons

## References

Full documentation with code examples:

- `references/react-performance-guidelines.md` - Complete guide with all patterns
- `references/rules/` - Consolidated rules by category:
  - `01-async-waterfalls.md` - CRITICAL: Eliminating waterfalls
  - `02-bundle-optimization.md` - CRITICAL: Bundle size optimization
  - `03-server-performance.md` - HIGH: Server-side performance
  - `04-client-fetching.md` - MEDIUM-HIGH: Client-side data fetching
  - `05-rerender-optimization.md` - MEDIUM: Re-render optimization
  - `06-rendering-performance.md` - MEDIUM: DOM rendering performance
  - `07-js-performance.md` - LOW-MEDIUM: JavaScript micro-optimizations
  - `08-advanced-patterns.md` - LOW: Advanced patterns
