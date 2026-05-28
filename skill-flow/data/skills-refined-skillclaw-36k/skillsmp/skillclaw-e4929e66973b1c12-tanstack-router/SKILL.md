---
name: tanstack-router
description: Use this skill when setting up routes, implementing navigation, or configuring route loaders in React applications with TanStack Router.
---

# TanStack Router Patterns

Type-safe, file-based routing for React applications with TanStack Router.

## Installation

```bash
pnpm add @tanstack/react-router
pnpm add -D @tanstack/router-plugin
```

```typescript
// vite.config.ts
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react(),
    TanStackRouterVite(), // Generates route tree
  ],
})
```

## Bootstrap

```typescript
// src/main.tsx
import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

const router = createRouter({ routeTree })

// Register router for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
```

## File-Based Routes

```
src/routes/
├── __root.tsx                 # Root layout (Outlet, providers)
├── index.tsx                  # "/" route
├── about.tsx                  # "/about" route
├── users/
│   ├── index.tsx              # "/users" route
│   └── $userId.tsx            # "/users/:userId" route (dynamic)
└── posts/
    ├── $postId/
    │   ├── index.tsx          # "/posts/:postId" route
    │   └── edit.tsx           # "/posts/:postId/edit" route
    └── index.tsx              # "/posts" route
```

**Naming Conventions:**
- `__root.tsx` - Root layout (contains `<Outlet />`)
- `index.tsx` - Index route for that path
- `$param.tsx` - Dynamic parameter (e.g., `$userId` → `:userId`)
- `_layout.tsx` - Layout route (no URL segment)
- `route.lazy.tsx` - Lazy-loaded route

## Automatic Code Splitting (Recommended)

**TanStack Router v1.x+ (2025)** introduces automatic code splitting that separates critical route configuration from non-critical components.

```typescript
// vite.config.ts
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react(),
    TanStackRouterVite({
      autoCodeSplitting: true, // NEW: Enable automatic splitting
    }),
  ],
})
```

**What Gets Split:**

| Critical (Always Loaded) | Non-Critical (Lazy Loaded) |
|--------------------------|---------------------------|
| Route configuration | Component |
| Loaders | Error component |
| Search params validation | Pending component |
| beforeLoad | Not-found component |

**Benefits:**
- Smaller initial bundle (route config without components)
- Automatic optimization (no manual `.lazy.tsx` files needed)
- Better perceived performance (loaders start immediately)

**When to Use:**
- **Recommended for all new projects**
- Existing projects: Enable and test bundle sizes
- Large apps benefit most (many routes)