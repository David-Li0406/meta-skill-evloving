# Project File Structure Guide

This document defines the complete file structure for React + TanStack + TakeOff UI enterprise applications.

## Complete Structure

```
project-root/
├── src/
│   ├── api/                          # API Layer
│   │   ├── client.ts                 # Axios/Fetch instance with interceptors
│   │   ├── config.ts                 # API configuration (base URL, timeout, etc.)
│   │   ├── endpoints/                # API endpoint definitions
│   │   │   ├── users.ts              # User-related endpoints and hooks
│   │   │   ├── products.ts           # Product-related endpoints and hooks
│   │   │   ├── auth.ts               # Auth endpoints (login, logout, refresh)
│   │   │   └── index.ts              # Export all endpoints
│   │   ├── types/                    # API types
│   │   │   ├── requests.ts           # Request DTOs
│   │   │   ├── responses.ts          # Response DTOs
│   │   │   └── common.ts             # Shared API types
│   │   └── schemas/                  # Zod schemas for validation
│   │       ├── user.schema.ts
│   │       └── product.schema.ts
│   │
│   ├── auth/                         # Authentication Layer
│   │   ├── AuthProvider.tsx          # Auth context provider
│   │   ├── useAuth.ts                # Auth hook
│   │   ├── oauth/                    # OAuth 2.0 implementation
│   │   │   ├── OAuthProvider.tsx
│   │   │   ├── flows.ts              # Authorization code, PKCE flows
│   │   │   └── config.ts             # OAuth config (client ID, scopes, etc.)
│   │   ├── jwt/                      # JWT implementation
│   │   │   ├── JWTProvider.tsx
│   │   │   ├── tokens.ts             # Token management (get, set, refresh)
│   │   │   └── storage.ts            # Secure token storage
│   │   ├── guards/                   # Route guards
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── GuestRoute.tsx
│   │   │   └── RoleGuard.tsx
│   │   └── types.ts                  # Auth types (User, AuthState, etc.)
│   │
│   ├── hooks/                        # Custom React Hooks (non-API)
│   │   ├── useLocalStorage.ts        # LocalStorage hook
│   │   ├── useDebounce.ts            # Debounce hook
│   │   ├── useMediaQuery.ts          # Responsive breakpoint hook
│   │   ├── useClickOutside.ts        # Click outside detector
│   │   ├── useToggle.ts              # Boolean toggle hook
│   │   └── index.ts                  # Export all hooks
│   │
│   ├── components/                   # Reusable UI Components
│   │   ├── DataTable/                # Generic data table
│   │   │   ├── DataTable.tsx
│   │   │   ├── DataTableFilters.tsx
│   │   │   ├── DataTablePagination.tsx
│   │   │   ├── DataTableRow.tsx
│   │   │   ├── types.ts
│   │   │   └── index.ts
│   │   ├── DynamicForm/              # Schema-driven form
│   │   │   ├── DynamicForm.tsx
│   │   │   ├── FieldRenderer.tsx     # Renders fields based on schema
│   │   │   ├── fields/               # Field type components
│   │   │   │   ├── TextField.tsx
│   │   │   │   ├── SelectField.tsx
│   │   │   │   ├── DateField.tsx
│   │   │   │   └── index.ts
│   │   │   ├── types.ts
│   │   │   └── index.ts
│   │   ├── Layout/                   # Layout components
│   │   │   ├── AppLayout.tsx         # Main app layout
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── index.ts
│   │   ├── ErrorBoundary/            # Error boundary
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── ErrorFallback.tsx
│   │   │   └── index.ts
│   │   ├── Loading/                  # Loading states
│   │   │   ├── Spinner.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   └── index.ts
│   │   └── index.ts                  # Export all components
│   │
│   ├── pages/                        # Page Components (Routes)
│   │   ├── Dashboard/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── components/           # Page-specific components
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   └── RecentActivity.tsx
│   │   │   └── index.ts
│   │   ├── Users/
│   │   │   ├── UsersPage.tsx         # User list
│   │   │   ├── UserDetailPage.tsx    # User detail
│   │   │   ├── UserCreatePage.tsx    # User create
│   │   │   ├── components/
│   │   │   │   └── UserForm.tsx
│   │   │   └── index.ts
│   │   ├── Products/
│   │   │   ├── ProductsPage.tsx
│   │   │   ├── ProductDetailPage.tsx
│   │   │   └── index.ts
│   │   ├── Auth/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── ForgotPasswordPage.tsx
│   │   │   └── index.ts
│   │   ├── Settings/
│   │   │   ├── SettingsPage.tsx
│   │   │   ├── ProfileTab.tsx
│   │   │   ├── SecurityTab.tsx
│   │   │   └── index.ts
│   │   └── NotFoundPage.tsx
│   │
│   ├── routes/                       # TanStack Router Configuration
│   │   ├── index.tsx                 # Root route and router instance
│   │   ├── __root.tsx                # Root layout route
│   │   ├── _authenticated.tsx        # Authenticated layout
│   │   ├── _guest.tsx                # Guest layout
│   │   └── routes.gen.ts             # Generated route types (if using file-based routing)
│   │
│   ├── lib/                          # Utilities and Helpers
│   │   ├── cn.ts                     # Tailwind class merger (clsx + tailwind-merge)
│   │   ├── validators.ts             # Common validators
│   │   ├── formatters.ts             # Date, number, currency formatters
│   │   ├── constants.ts              # App constants
│   │   └── utils.ts                  # General utilities
│   │
│   ├── types/                        # Shared TypeScript Types
│   │   ├── models.ts                 # Domain models
│   │   ├── enums.ts                  # Enums
│   │   ├── globals.d.ts              # Global type declarations
│   │   └── index.ts
│   │
│   ├── styles/                       # Global Styles (Minimal)
│   │   └── globals.css               # Only @tailwind directives and :root variables
│   │
│   ├── App.tsx                       # App root component
│   └── main.tsx                      # Entry point
│
├── public/                           # Static Assets
│   ├── favicon.ico
│   └── assets/
│       └── images/
│
├── tests/                            # Tests (if separate from src)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env.example                      # Environment variables template
├── .env                              # Environment variables (gitignored)
├── .gitignore
├── index.html                        # HTML entry point
├── package.json
├── tsconfig.json                     # TypeScript config
├── tsconfig.node.json                # TypeScript config for Vite
├── vite.config.ts                    # Vite configuration
├── tailwind.config.ts                # Tailwind configuration
├── postcss.config.js                 # PostCSS configuration
├── eslint.config.js                  # ESLint configuration
└── README.md
```

## Directory Descriptions

### `/src/api/`

**Purpose:** Centralized API layer for all backend communication.

**Rules:**
- All API calls go through `client.ts`
- Organize endpoints by domain (`users.ts`, `products.ts`)
- Include TanStack Query hooks in endpoint files
- Use Zod schemas for validation
- Never import API functions directly in components (use hooks)

**Example:**

```ts
// src/api/endpoints/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '../client'
import { userSchema } from '../schemas/user.schema'

export const usersApi = {
  getAll: () => apiClient.get('/users'),
  getById: (id: string) => apiClient.get(`/users/${id}`),
  create: (data: CreateUserDto) => apiClient.post('/users', data),
  update: (id: string, data: UpdateUserDto) => apiClient.put(`/users/${id}`, data),
  delete: (id: string) => apiClient.delete(`/users/${id}`),
}

export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: usersApi.getAll,
  })
}

export const useUser = (id: string) => {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => usersApi.getById(id),
  })
}

export const useCreateUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: usersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}
```

### `/src/auth/`

**Purpose:** Authentication and authorization logic.

**Rules:**
- Separate OAuth and JWT implementations
- Provide context via `AuthProvider`
- Export `useAuth` hook for consuming components
- Implement route guards for protected routes
- Never store sensitive tokens in localStorage (use httpOnly cookies or secure storage)

### `/src/hooks/`

**Purpose:** Reusable React hooks that are NOT API-related.

**Rules:**
- Only non-API hooks (API hooks go in `/src/api/endpoints/`)
- Generic, reusable logic
- Well-tested and documented
- Export via `index.ts`

### `/src/components/`

**Purpose:** Reusable UI components used across multiple pages.

**Rules:**
- Each complex component gets its own folder
- Include `index.ts` for clean imports
- Page-specific components stay in `/src/pages/[PageName]/components/`
- Use TakeOff UI components as base
- Only Tailwind for styling (no CSS files)

### `/src/pages/`

**Purpose:** Page-level components mapped to routes.

**Rules:**
- One page per route
- Page-specific components in `components/` subfolder
- Pages orchestrate components and hooks
- Minimal business logic (delegate to hooks/services)

### `/src/routes/`

**Purpose:** TanStack Router configuration.

**Rules:**
- Define all routes in `index.tsx`
- Use route guards for protected routes
- Implement layouts in `__root.tsx`, `_authenticated.tsx`, `_guest.tsx`
- Lazy load pages for code splitting

### `/src/lib/`

**Purpose:** Utility functions, helpers, and constants.

**Rules:**
- Pure functions only
- Well-tested
- No React-specific code (use `/src/hooks/` for that)
- Export via named exports

### `/src/types/`

**Purpose:** Shared TypeScript types and interfaces.

**Rules:**
- Domain models
- Shared enums
- Global type declarations
- Export via `index.ts`

### `/src/styles/`

**Purpose:** MINIMAL global styles.

**Rules:**
- **ONLY** include:
  - `@tailwind base;`
  - `@tailwind components;`
  - `@tailwind utilities;`
  - `:root` CSS variables (for TakeOff UI theming)
- **NO** custom CSS classes
- **NO** component styles

## File Naming Conventions

### Components

- **React components:** PascalCase (e.g., `UserCard.tsx`)
- **Component folders:** PascalCase (e.g., `DataTable/`)
- **Hooks:** camelCase with `use` prefix (e.g., `useAuth.ts`)
- **Utils:** camelCase (e.g., `formatDate.ts`)
- **Types:** camelCase with `.types.ts` or `.d.ts` suffix
- **Tests:** Same name with `.test.ts` or `.spec.ts` suffix

### Barrels (index.ts)

Use `index.ts` to re-export from folders:

```ts
// src/components/DataTable/index.ts
export { DataTable } from './DataTable'
export type { DataTableProps } from './types'
```

## Import Aliases

Configure path aliases in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/api/*": ["./src/api/*"],
      "@/components/*": ["./src/components/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"]
    }
  }
}
```

**Usage:**

```tsx
// ❌ WRONG - Relative imports
import { useUsers } from '../../../api/endpoints/users'

// ✅ CORRECT - Alias imports
import { useUsers } from '@/api/endpoints/users'
```

## Separation of Concerns Enforcement

### ❌ ANTI-PATTERNS

```tsx
// WRONG: API logic in component
function UsersPage() {
  const [users, setUsers] = useState([])
  
  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(setUsers)
  }, [])
  
  return <div>...</div>
}

// WRONG: Business logic in component
function ProductPage() {
  const calculateDiscount = (price: number) => {
    // Complex business logic here
  }
  
  return <div>...</div>
}

// WRONG: Component in API file
// src/api/endpoints/users.ts
export function UserCard() {
  return <div>...</div>
}
```

### ✅ CORRECT PATTERNS

```tsx
// CORRECT: API logic in endpoint file
// src/api/endpoints/users.ts
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => apiClient.get('/users'),
  })
}

// CORRECT: Business logic in hook
// src/hooks/useDiscountCalculator.ts
export function useDiscountCalculator() {
  const calculateDiscount = (price: number) => {
    // Complex business logic here
  }
  
  return { calculateDiscount }
}

// CORRECT: Component uses hooks
// src/pages/Users/UsersPage.tsx
function UsersPage() {
  const { data: users, isLoading } = useUsers()
  
  return <div>...</div>
}
```

## Environment Variables

```env
# .env.example
VITE_API_BASE_URL=https://api.example.com
VITE_APP_NAME=My App
VITE_OAUTH_CLIENT_ID=your-client-id
VITE_OAUTH_REDIRECT_URI=http://localhost:5173/auth/callback
```

Access in code:

```ts
// src/api/config.ts
export const apiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
}
```

## Code Splitting Strategy

```tsx
// src/routes/index.tsx
import { createRouter, createRoute } from '@tanstack/react-router'
import { lazy } from 'react'

const DashboardPage = lazy(() => import('@/pages/Dashboard'))
const UsersPage = lazy(() => import('@/pages/Users'))

// Route definitions with lazy loading...
```

## Summary

This structure ensures:

1. **Scalability** - Easy to find and add new features
2. **Maintainability** - Clear separation of concerns
3. **Type Safety** - Centralized types and schemas
4. **Testability** - Pure functions and isolated components
5. **Performance** - Code splitting and lazy loading
6. **Security** - Centralized auth and API client

Follow this structure strictly for all projects. Deviations require explicit justification and approval.