---
name: react-best-practices
description: React 19 + Next.js App Router performance and best practices for this codebase (TypeScript + Tailwind CSS 4). Use when writing/reviewing/refactoring components, deciding server vs client boundaries, building forms with server actions, preventing re-renders, and keeping the client bundle small.
---

# React Best Practices

Performance optimization and conventions for React 19 in a Next.js App Router codebase.

## Codebase Conventions (This Repo)

### TypeScript & File Types

- Prefer TypeScript everywhere:
  - `.tsx` for React components
  - `.ts` for non-React logic (services, utilities, server actions)

### Tailwind Class Composition

- Prefer the local `cn(...)` helper from `src/lib/design-utils.ts` for conditional class names.
- Avoid “computed Tailwind” like `` `bg-${color}-500` `` (Tailwind can’t see it reliably).

## Quick Reference

### Server vs Client Components

- **Default to Server Components** for pages/layouts/data widgets.
- Use `"use client"` only for:
  - Local state / effects
  - Browser-only APIs (`window`, `localStorage`)
  - Event handlers (`onClick`, etc.)
- Keep client components as leaf nodes; pass in plain serializable props.

### Mutations: Prefer Server Actions

- Put server mutations in `src/app/actions/*` with `"use server"`.
- Authenticate early via `auth()` (see `src/lib/auth.ts`).
- If the mutation affects a server-rendered page, revalidate via `revalidatePath(...)`.

### Client-Side Performance (Only When You’re In `"use client"`)

- Avoid unnecessary re-renders:
  - Don’t create new inline objects/arrays/functions in JSX unless needed
  - Use `useCallback`/`useMemo` when it materially reduces renders
  - Split large components; memoize leaf components when props are stable
- Avoid long effect chains and “derived state” stored in state.

## Impact Priority Guide

| Priority | Topic                              | Reference                                                       |
| -------- | ---------------------------------- | --------------------------------------------------------------- |
| CRITICAL | Waterfall elimination, bundle size | [critical-patterns.md](references/critical-patterns.md)         |
| HIGH     | Re-render prevention               | [rerender-optimization.md](references/rerender-optimization.md) |
| MEDIUM   | Rendering perf, JS optimizations   | [performance-patterns.md](references/performance-patterns.md)   |
| MEDIUM   | Tailwind CSS patterns              | [tailwind-patterns.md](references/tailwind-patterns.md)         |

## Common Anti-patterns

### Avoid: Overusing Barrel Imports

- Small, curated barrels are fine (this repo uses `@/components/help`), but avoid creating “mega barrels” that hide expensive imports or create circular deps.

### Avoid: Sequential Awaits

```javascript
// Bad - waterfall
const data1 = await fetchData1();
const data2 = await fetchData2();

// Good - parallel
const [data1, data2] = await Promise.all([fetchData1(), fetchData2()]);
```

### Avoid: Inline Objects in JSX

```javascript
// Bad - new object every render
<Component style={{ margin: 10 }} config={{ enabled: true }} />;

// Good - stable references
const style = useMemo(() => ({ margin: 10 }), []);
const config = useMemo(() => ({ enabled: true }), []);
<Component style={style} config={config} />;
```

### Avoid: Missing Dependencies

```javascript
// Bad - stale closure
useEffect(() => {
  fetchData(userId);
}, []);

// Good - correct dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

### Avoid: Conditional Rendering with &&

```javascript
// Bad - renders "0" if count is 0
{
  count && <Badge count={count} />;
}

// Good - explicit boolean
{
  count > 0 && <Badge count={count} />;
}
// Or ternary
{
  count ? <Badge count={count} /> : null;
}
```
