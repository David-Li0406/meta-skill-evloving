# Project Structure

A well-organized project structure is fundamental to building scalable, maintainable React applications. This guide covers proven patterns for organizing code, enforcing architectural boundaries, and maintaining consistency across teams.

## Table of Contents

- [Feature-Based Organization](#feature-based-organization)
- [Shared Code Structure](#shared-code-structure)
- [Unidirectional Architecture](#unidirectional-architecture)
- [Import Strategies](#import-strategies)
- [File Naming Conventions](#file-naming-conventions)
- [Monorepo Considerations](#monorepo-considerations)

## Feature-Based Organization

### Core Principle

Organize code by **feature** (business domain) rather than by technical type (components, hooks, utils). This colocation approach keeps all code related to a feature together, making it easier to understand, modify, and test.

###Feature Folder Structure

```
src/
├── app/                    # App-level routing and layouts
│   ├── routes/            # Route definitions
│   ├── layouts/           # Shared layouts
│   └── providers.tsx      # Global providers
├── features/              # Feature modules
│   ├── authentication/
│   │   ├── api/          # API calls for auth
│   │   │   ├── login.ts
│   │   │   ├── logout.ts
│   │   │   └── index.ts
│   │   ├── components/   # Auth-specific components
│   │   │   ├── LoginForm.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── index.ts
│   │   ├── hooks/        # Auth-specific hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useLogin.ts
│   │   │   └── index.ts
│   │   ├── stores/       # Auth state management
│   │   │   └── authStore.ts
│   │   ├── types/        # Auth-specific types
│   │   │   └── index.ts
│   │   ├── utils/        # Auth utilities
│   │   │   ├── tokenStorage.ts
│   │   │   └── validateToken.ts
│   │   └── index.ts      # Public API
│   ├── users/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── types/
│   │   └── index.ts
│   └── dashboard/
│       └── ...
├── components/            # Shared components
│   ├── ui/               # Base UI components
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Modal/
│   └── layout/           # Layout components
│       ├── Header/
│       ├── Sidebar/
│       └── Footer/
├── hooks/                 # Shared hooks
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── index.ts
├── lib/                   # Third-party integrations
│   ├── react-query.ts    # React Query setup
│   ├── axios.ts          # Axios configuration
│   └── i18n.ts           # Internationalization
├── stores/                # Global state stores
│   ├── themeStore.ts
│   └── appStore.ts
├── types/                 # Shared TypeScript types
│   ├── api.ts
│   ├── models.ts
│   └── index.ts
├── utils/                 # Shared utilities
│   ├── format.ts
│   ├── validation.ts
│   └── index.ts
├── testing/               # Test utilities and mocks
│   ├── mocks/
│   ├── setup.ts
│   └── test-utils.tsx
└── assets/                # Static assets
    ├── images/
    ├── fonts/
    └── styles/
```

### Feature Module Guidelines

**Each feature should be self-contained:**

1. **Public API** - Export only what other features need via `index.ts`
2. **Private Implementation** - Keep internal components, hooks, utils private
3. **Clear Boundaries** - Features should not directly import from other features' internals
4. **Independent Testing** - Features should be testable in isolation

**Example feature index.ts:**

```ts
// features/authentication/index.ts

// Only export public API
export { LoginForm } from './components/LoginForm';
export { ProtectedRoute } from './components/ProtectedRoute';
export { useAuth } from './hooks/useAuth';
export type { User, AuthState } from './types';

// Internal components, hooks, and utils are NOT exported
// This prevents other features from depending on implementation details
```

### When to Create a Feature

Create a new feature when:
- The functionality represents a distinct business domain
- The code will be used by multiple parts of the application
- The feature has its own state, API calls, and business logic
- The feature is large enough to benefit from isolation (>5 components typically)

**Don't** create features for:
- Single components used in one place (keep them local)
- Purely presentational UI with no business logic (use shared components)
- Code that's tightly coupled to a parent feature (keep it nested)

## Shared Code Structure

### Component Organization

**`components/ui/`** - Base design system components:
```
components/ui/
├── Button/
│   ├── Button.tsx        # Component
│   ├── Button.test.tsx   # Tests
│   ├── Button.stories.tsx # Storybook stories (optional)
│   ├── types.ts          # Component-specific types
│   └── index.ts          # Exports
├── Input/
└── Select/
```

**`components/layout/`** - Layout components:
```
components/layout/
├── Header/
├── Sidebar/
├── Footer/
└── PageContainer/
```

### Hooks Organization

**Shared hooks** should be highly reusable and domain-agnostic:

```ts
// hooks/useLocalStorage.ts
export function useLocalStorage<T>(key: string, initialValue: T) {
  // Implementation
}

// hooks/useDebounce.ts
export function useDebounce<T>(value: T, delay: number) {
  // Implementation
}

// hooks/useMediaQuery.ts
export function useMediaQuery(query: string) {
  // Implementation
}
```

### Library Setup (`lib/`)

Centralize third-party library configuration:

```ts
// lib/react-query.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// lib/axios.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptors
apiClient.interceptors.request.use(/* ... */);
apiClient.interceptors.response.use(/* ... */);
```

## Unidirectional Architecture

### Dependency Flow

Enforce a **one-way dependency flow** to prevent circular dependencies and maintain predictability:

```
app → features → shared (components, hooks, lib, utils, types)
```

**Rules:**
1. `app/` can import from `features/` and `shared`
2. `features/` can import from `shared` but NOT from other features' internals
3. `shared` code (components, hooks, lib, utils) cannot import from `features/` or `app/`

**✅ Good:**
```ts
// features/users/components/UserProfile.tsx
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/features/authentication'; // Via public API
```

**❌ Bad:**
```ts
// components/ui/Button.tsx
import { useAuth } from '@/features/authentication'; // Shared component depends on feature
```

### Enforcing with ESLint

Use `eslint-plugin-import` to enforce boundaries:

```js
// .eslintrc.js
{
  rules: {
    'import/no-restricted-paths': [
      'error',
      {
        zones: [
          // Prevent shared code from importing features
          {
            target: './src/components',
            from: './src/features',
            message: 'Shared components cannot import from features',
          },
          {
            target: './src/hooks',
            from: './src/features',
            message: 'Shared hooks cannot import from features',
          },
          {
            target: './src/lib',
            from: './src/features',
            message: 'Library setup cannot import from features',
          },
          {
            target: './src/utils',
            from: './src/features',
            message: 'Shared utils cannot import from features',
          },
          // Prevent features from importing each other's internals
          {
            target: './src/features/*/!(index).{ts,tsx}',
            from: './src/features',
            message: 'Features can only import from other features via their index.ts',
          },
        ],
      },
    ],
  },
}
```

## Import Strategies

### Absolute Imports

Configure absolute imports to avoid messy relative paths:

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/features/*": ["./src/features/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"],
      "@/utils/*": ["./src/utils/*"]
    }
  }
}
```

**Vite config:**
```ts
// vite.config.ts
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**Usage:**
```ts
// ✅ Good - Absolute imports
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/features/authentication';
import { formatDate } from '@/utils/format';

// ❌ Bad - Relative imports
import { Button } from '../../../components/ui/Button';
import { useAuth } from '../../features/authentication';
```

### Index Files

Use index files to create clean public APIs:

```ts
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Select } from './Select';

// Usage
import { Button, Input, Select } from '@/components/ui';
```

**Avoid barrel file pitfalls:**
- Don't re-export everything indiscriminately
- Only export what's meant to be public
- Be mindful of bundle size (barrel files can prevent tree-shaking)

## File Naming Conventions

### Component Files

**PascalCase for components:**
```
UserProfile.tsx
LoginForm.tsx
DashboardLayout.tsx
```

**Colocation:**
```
Button/
├── Button.tsx          # Component
├── Button.test.tsx     # Tests
├── Button.module.css   # Styles (if using CSS modules)
├── types.ts            # Component types
└── index.ts            # Exports
```

### Non-Component Files

**camelCase for utilities, hooks, and helpers:**
```
formatDate.ts
useLocalStorage.ts
validateEmail.ts
apiClient.ts
```

### Consistency Rules

1. **Components**: PascalCase (`UserCard.tsx`)
2. **Hooks**: camelCase starting with `use` (`useDebounce.ts`)
3. **Utilities**: camelCase (`formatCurrency.ts`)
4. **Types**: camelCase (`userTypes.ts` or `types.ts`)
5. **Constants**: UPPERCASE (`API_ENDPOINTS.ts`) or camelCase (`constants.ts`)
6. **Stores**: camelCase ending with `Store` (`authStore.ts`)

### ESLint Enforcement

```js
// .eslintrc.js
{
  rules: {
    // Enforce naming conventions
    'react/jsx-pascal-case': ['error', { allowAllCaps: false }],
  },
}
```

## Monorepo Considerations

### Workspace Structure

For monorepos using pnpm/yarn/npm workspaces:

```
packages/
├── web/                  # Main web app
│   └── src/
│       ├── app/
│       ├── features/
│       └── ...
├── mobile/               # Mobile app (React Native)
│   └── src/
├── shared/               # Shared code
│   ├── components/      # Shared components
│   ├── hooks/          # Shared hooks
│   ├── types/          # Shared types
│   └── utils/          # Shared utilities
├── design-system/        # UI component library
│   └── src/
│       └── components/
└── api-client/           # API client package
    └── src/
```

### Package Dependencies

**Clear dependency hierarchy:**
```
web → shared, design-system, api-client
mobile → shared, design-system, api-client
design-system → (no internal dependencies)
shared → (no internal dependencies)
api-client → shared (types only)
```

### Cross-Package Imports

```json
// packages/web/package.json
{
  "dependencies": {
    "@myapp/shared": "workspace:*",
    "@myapp/design-system": "workspace:*",
    "@myapp/api-client": "workspace:*"
  }
}
```

```ts
// packages/web/src/features/users/components/UserCard.tsx
import { Button } from '@myapp/design-system';
import { formatDate } from '@myapp/shared/utils';
import { fetchUser } from '@myapp/api-client';
```

## Best Practices Summary

1. **Feature Isolation** - Keep features self-contained with clear public APIs
2. **Unidirectional Flow** - Enforce dependency direction (app → features → shared)
3. **Absolute Imports** - Use path aliases to avoid relative import hell
4. **Consistent Naming** - PascalCase for components, camelCase for everything else
5. **Colocation** - Keep related files together (tests, styles, types)
6. **Index Files** - Create clean public APIs, but don't over-use barrel files
7. **ESLint Enforcement** - Automate architectural rules with linting
8. **Monorepo Boundaries** - Maintain clear package dependencies in workspaces

By following these patterns, you create a codebase that's intuitive to navigate, easy to maintain, and scales smoothly as the team and application grow.
