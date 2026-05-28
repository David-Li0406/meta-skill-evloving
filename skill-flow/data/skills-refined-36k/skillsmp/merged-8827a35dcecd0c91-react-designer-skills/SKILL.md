---
name: react-designer-skills
description: Use this skill for best practices and patterns in React 18 development within the LlamaFarm Designer subsystem, covering components, hooks, state management, and styling.
---

# React Designer Skills for LlamaFarm

This document outlines best practices and patterns for React 18 development in the Designer subsystem, which includes frameworks like TanStack Query, TailwindCSS, and Radix UI.

## Overview

The Designer is a browser-based project workbench for building AI applications, providing config editing, chat testing, dataset management, RAG configuration, and model selection.

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
| framer-motion | 12.x | Animations |

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
- Apply `displayName` to `forwardRef` components for DevTools.

### State Management

- **Local UI state**: `useState`, `useReducer`.
- **Server state**: TanStack Query (`useQuery`, `useMutation`).
- **Shared UI state**: React Context with custom hooks.
- **Form state**: Controlled components with validation.

### Hooks

- Follow Rules of Hooks (top-level, consistent order).
- Create custom hooks for reusable logic.
- Use query key factories for TanStack Query.
- Memoize expensive computations with `useMemo`.
- Stabilize callbacks with `useCallback`.

### API Client Configuration

```typescript
// Centralized client with interceptors
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
})

// Error handling interceptor
apiClient.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    if (error.response?.status === 422) {
      throw new ValidationError('Validation error', error.response.data)
    }
    throw new NetworkError('Request failed', error)
  }
)
```

### Query Client Configuration

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      gcTime: 5 * 60_000,
      retry: 2,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30_000),
      refetchOnWindowFocus: false,
    },
    mutations: { retry: 1 },
  },
})
```

### Styling

- Use `cn()` from `lib/utils` to merge Tailwind classes.
- Use `cva` (class-variance-authority) for component variants.
- Follow dark mode conventions with `dark:` prefix.

## Testing

```typescript
// Use MSW for API mocking
import { server } from '@/test/mocks/server'
import { renderWithProviders } from '@/test/utils'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('renders with query data', async () => {
  renderWithProviders(<MyComponent />)
  await screen.findByText('Expected text')
})
```

## Checklist Summary

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| TanStack Query | 3 | 4 | 3 | 2 |
| TailwindCSS | 2 | 3 | 4 | 2 |
| Radix UI | 3 | 3 | 2 | 1 |
| Performance | 2 | 4 | 3 | 2 |

## Related Guides

- [components.md](./components.md) - Component patterns
- [hooks.md](./hooks.md) - Hook patterns and rules
- [state.md](./state.md) - State management patterns
- [performance.md](./performance.md) - Performance optimization
- [security.md](./security.md) - Security best practices