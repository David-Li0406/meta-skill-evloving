---
name: react
description: React coding standards. Use when working on React components to ensure proper hooks usage, state management, and performance patterns.
---

# React

Critical rules for React development.

---

## Hooks

- Hooks first, top-level only (no loops/conditions/nested fns)
- Order: hooks → derived values → handlers → JSX return
- Group by concern: state/store → data/query → memo → effects
- Never select entire store (e.g. Zustand); always use selectors + shallow

## State & Data

- State minimal, normalized; derive instead of duplicate
- Prefer local state; global only for truly cross-cutting data
- Use query libraries (React Query/SWR) for server data; never raw fetch in components
- Query cache = source of truth; don't mirror to local state

## Props & Composition

- Minimize props; prefer whole objects over many primitives
- No prop drilling; use composition or context
- Access global stores via hooks, not props

## Effects & Render

- Avoid useEffect when possible; use only for external sync
- All dependencies listed; restructure instead of silencing lints
- Cleanup always (timers, subscriptions)
- Render pure: no side-effects, no mutation
- Stable keys in lists (real IDs, not array index)
- Final conditional render (`if (!data) return null;`) just before JSX, never between hooks

## Performance

- No premature optimization; memoize only for real perf issues
- Avoid inline objects/functions in JSX that cause re-renders
