---
name: llama-farm-designer-react-skills
description: Use this skill when developing applications in the LlamaFarm Designer subsystem, focusing on best practices for React 18, TanStack Query, TailwindCSS, and Radix UI.
---

# Skill body

## Overview

This skill provides best practices and patterns for developing applications in the LlamaFarm Designer subsystem using React 18, TanStack Query, TailwindCSS, and Radix UI.

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI framework with StrictMode |
| TypeScript | 5.2+ | Type safety |
| TanStack Query | v5 | Server state management |
| TailwindCSS | 3.3 | Utility-first CSS |
| Radix UI | 1.x | Accessible component primitives |
| Vite | 6.x | Build tooling and dev server |
| React Router | v7 | Client-side routing |
| Vitest | 1.x | Testing framework |
| axios | 1.x | HTTP client |

## Directory Structure

```
designer/src/
  api/          # API service modules (axios-based)
  assets/       # Static assets and icons
  components/   # Feature-organized React components
    ui/         # Radix-based primitive components
  contexts/     # React Context providers
  hooks/        # Custom hooks (TanStack Query wrappers)
  lib/          # Utilities (cn, etc.)
  types/        # TypeScript type definitions
  utils/        # Helper functions
  test/         # Test utilities, factories, mocks
```

## Core Patterns

### Component Composition

- Use composition over inheritance.
- Prefer small, focused components.
- Use `forwardRef` for components that wrap DOM elements.
- Apply `displayName` to `forwardRef` components for better DevTools visibility.

### State Management

- **Local UI state**: Use `useState` and `useReducer`.
- **Server state**: Utilize TanStack Query with `useQuery` and `useMutation`.
- **Shared UI state**: Implement React Context with custom hooks.
- **Form state**: Use controlled components with validation.

### Hooks

- Follow the Rules of Hooks (top-level, consistent order).
- Create custom hooks for reusable logic.
- Use query key factories for TanStack Query.
- Memoize expensive computations with `useMemo`.
- Stabilize callbacks with `useCallback`.

### Styling

- Use `cn()` from `lib/utils` to merge Tailwind classes.
- Use `cva` (class-variance-authority) for component variants.
- Follow dark mode conventions with the `dark:` prefix.

## Related Guides

- [tanstack-query.md](./tanstack-query.md) - Query/Mutation patterns, caching, invalidation.
- [tailwind.md](./tailwind.md) - TailwindCSS patterns, theming, responsive design.
- [radix.md](./radix.md) - Radix UI component patterns, accessibility.
- [performance.md](./performance.md) - Frontend optimizations, bundle size, lazy loading.
- [components.md](./components.md) - Component patterns.
- [hooks.md](./hooks.md) - Hook patterns and rules.
- [state.md](./state.md) - State management patterns.
- [security.md](./security.md) - Security best practices.

## Quick Reference

```typescript
// Centralized API client configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Utility for merging Tailwind classes
import { cn } from '@/lib/utils';
cn('base-class', condition && 'conditional-class', className);
```