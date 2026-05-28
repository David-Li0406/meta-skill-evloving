---
name: react-best-practices
description: Use when writing, reviewing, or refactoring React/Next.js components, pages, or data fetching where performance, bundle size, or render efficiency is a concern.
---

# React Best Practices (Vercel)

## Overview
Use this skill to apply Vercel’s React/Next.js performance rules. The goal is to eliminate waterfalls, reduce bundle size, and keep server/client work efficient.

## When to Use
- Building or reviewing React components or Next.js pages
- Adding data fetching (server or client)
- Optimizing bundle size or load time
- Investigating rendering or re-render performance issues

## Quick Reference (Rule Categories)

| Priority | Category | Focus |
| --- | --- | --- |
| 1 | Eliminating Waterfalls | Parallelize async work, defer awaits |
| 2 | Bundle Size Optimization | Avoid barrels, use dynamic import |
| 3 | Server-Side Performance | Cache, parallelize server fetches |
| 4 | Client-Side Data Fetching | Deduplicate requests and listeners |
| 5 | Re-render Optimization | Memoization and stable dependencies |
| 6 | Rendering Performance | Hoist static JSX, avoid expensive renders |
| 7 | JavaScript Performance | Reduce loops and lookups |
| 8 | Advanced Patterns | Stable handler refs, useLatest |

## Core Checks (Most Common)
- **Waterfalls**: Look for sequential `await` where operations are independent → use `Promise.all`.
- **Bundle size**: Avoid barrel imports, dynamically import heavy components.
- **Server fetches**: Start promises early, await late; use React cache where applicable.
- **Re-renders**: Memoize expensive components and avoid derived-state subscriptions.

## Rule Pointers (Most Used)
- `async-parallel`, `async-defer-await`, `async-api-routes`
- `bundle-barrel-imports`, `bundle-dynamic-imports`, `bundle-defer-third-party`
- `server-cache-react`, `server-parallel-fetching`, `server-serialization`
- `client-swr-dedup`, `rerender-memo`, `rerender-dependencies`

Full reference: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices

## Example Application
If a Next.js server component does:
- `await getUser()`
- `await getNotes()`

and these are independent, apply `async-parallel` and fetch with `Promise.all`.

## Common Mistakes
- Treating sequential `await` as harmless when requests are independent.
- Importing from barrel files for convenience and shipping unused code.
- Passing large objects to client components instead of slimming data.

## Red Flags (Stop and Apply This Skill)
- “This page feels slow but I can’t see why.”
- “We have multiple awaits in a row.”
- “Bundle size grew after adding a component.”
- “This component re-renders more than expected.”
