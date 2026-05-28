---
name: react-perf
description: "React/Next.js performance optimization guidelines from Vercel Engineering. Use when reviewing performance, optimizing bundles, or fixing waterfalls."
allowed-tools: Read, Glob, Grep, Task, TodoWrite
model: sonnet
---

# React Performance Optimization

Guidelines from Vercel Engineering for React and Next.js performance.

## Source Reference

Full rules: `~/dev/vercel-labs/agent-skills/skills/react-best-practices/rules/`

## When to Use

- User requests performance review or optimization
- Investigating slow renders or bundle size
- Fixing waterfall data fetching patterns

## Rule Categories

### Universal (Vite + Next.js)
Load these rules for any React project:
- `async-parallel.md` - Promise.all() for independent operations (CRITICAL)
- `async-defer-await.md` - Defer await until needed (HIGH)
- `bundle-barrel-imports.md` - Avoid barrel file imports (CRITICAL)
- `rerender-functional-setstate.md` - Use functional setState (MEDIUM)
- `rerender-lazy-state-init.md` - Lazy state initialization (MEDIUM)
- `rerender-transitions.md` - Use transitions for non-urgent updates (MEDIUM)
- `js-set-map-lookups.md` - Use Set/Map for O(1) lookups
- `js-early-exit.md` - Early return from functions
- `js-tosorted-immutable.md` - Use toSorted() for immutability
- `client-passive-event-listeners.md` - Passive event listeners

### Next.js Specific
Load only for Next.js projects (detected by `next.config.*` or `app/` directory):
- `server-parallel-fetching.md` - Parallel data fetching with RSC (CRITICAL)
- `server-cache-react.md` - React.cache() deduplication (MEDIUM)
- `server-serialization.md` - Minimize RSC serialization (HIGH)
- `async-suspense-boundaries.md` - Strategic Suspense boundaries (HIGH)
- `bundle-dynamic-imports.md` - next/dynamic for heavy components (CRITICAL)

### Simplicity-Safe (Low Complexity Cost)
These improve both performance AND readability:
- `async-parallel.md` - Cleaner than sequential awaits
- `js-early-exit.md` - Guard clauses improve flow
- `bundle-barrel-imports.md` - Single line fix
- `rerender-functional-setstate.md` - Prevents bugs

### Avoid for General Use (High Complexity Cost)
Only apply when profiling proves necessity:
- `async-dependencies.md` - Requires `better-all` library
- `advanced-event-handler-refs.md` - Ref indirection pattern
- `advanced-use-latest.md` - Custom hook abstraction
- `client-event-listeners.md` - Complex subscription system

## Usage

1. Detect project type (Vite vs Next.js)
2. Read relevant rule files from source
3. Apply rules that fit the optimization context
4. Defer to code-simplifier for general cleanup
