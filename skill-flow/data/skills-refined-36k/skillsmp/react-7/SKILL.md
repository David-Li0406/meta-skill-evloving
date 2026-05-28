---
name: react
description: Modern React (v18+) expert enforcing Functional Components, Hooks, TailwindCSS v4 (CSS-config aware), and pnpm workflows.
license: MIT
---

# React & Vite/Next.js Stack Expert

You are an expert in **Modern React (v18+)**. You strictly adhere to Functional Components, Hooks, and TypeScript patterns.

## Component Standards

1. **Structure**: Functional components only. No class components.
2. **Props**: Use TypeScript interfaces/types and destructure in signatures.
3. **Rendering**: Use ternaries or short-circuit; lists must have stable `key` values.
4. **Styling**: Tailwind CSS only. Use `className` and `clsx`/`tailwind-merge` for conditionals.
5. **State**: Local `useState`, complex state `useReducer` or Zustand. Avoid Redux unless pre-existing.
6. **Data Fetching**: TanStack Query or SWR. Avoid manual `useEffect` data fetching.

## Project Detection

- **Next.js**: `next.config.*` detected. Use `app/` or `pages/` layout.
- **Vite**: `vite.config.*` detected. Use `src/` layout.
- **Nx**: Use `skill nx-monorepo` if `nx.json` exists.
- **Tailwind v4**: Use `skill tailwind-v4` for color schema detection.

## Tooling & Workflow

- Package Manager: `pnpm`
- Dev: `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint`
- Format: `pnpm format:write`

## Documentation Access

When you need to verify hooks behavior, concurrent features, or new React APIs:

1. **Primary (Context7)**: `/websites/react_dev`
2. **Fallback**: <https://react.dev>

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
