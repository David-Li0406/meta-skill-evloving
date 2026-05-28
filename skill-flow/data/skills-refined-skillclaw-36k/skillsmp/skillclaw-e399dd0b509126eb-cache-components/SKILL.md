---
name: cache-components
description: Use this skill when working in Next.js projects that have `cacheComponents: true` in their `next.config.ts` or `next.config.js` to apply best practices for Cache Components and Partial Prerendering (PPR).
---

# Next.js Cache Components

## Proactive Activation
This skill activates automatically when `cacheComponents: true` is detected in the Next.js configuration file. It guides all component authoring, data fetching, and caching decisions.

## Detection
At the start of a session in a Next.js project, check for `cacheComponents: true` in `next.config`. If enabled, apply this skill's patterns proactively when:
- Writing React Server Components
- Implementing data fetching
- Creating Server Actions with mutations
- Optimizing page performance
- Reviewing existing component code

## Use Cases
- Implementing the `'use cache'` directive
- Configuring cache lifetimes with `cacheLife()`
- Tagging cached data with `cacheTag()`
- Invalidating caches with `updateTag()` / `revalidateTag()`
- Optimizing static vs dynamic content boundaries
- Debugging cache issues
- Reviewing Cache Component implementations

## Project Detection Command
To check if Cache Components are enabled, run:
```bash
# Check next.config.ts or next.config.js for cacheComponents
grep -r "cacheComponents" next.config.* 2>/dev/null
```

## Philosophy: Code Over Configuration
Cache Components represent a shift from segment-based configuration to compositional code:
- **Before (Deprecated)**: `export const revalidate = 3600`
- **After**: `cacheLife('hours')` inside `'use cache'`
- **Before (Deprecated)**: `export const dynamic = 'force-static'`
- **After**: Use `'use cache'` and Suspense boundaries

**Key Principle**: Components co-locate their caching, not just their data. Next.js provides build-time feedback to guide you toward optimal patterns.