---
name: defining-typescript-types
description: Define TypeScript types and interfaces for React components, Inertia props, and Laravel models. Use when creating types, defining interfaces, typing props, or when user mentions TypeScript types, interfaces, models, or type definitions.
---

# Define TypeScript Types

Define TypeScript types and interfaces for React components, Inertia page props, and Laravel model representations. Organize types by purpose in dedicated files, ensuring frontend type definitions stay synchronized with backend API responses.

## File Structure

Type definitions are organized by purpose:

```
resources/js/types/
├── index.d.ts          # Inertia types, PageProps
├── models.d.ts         # Laravel model types
└── global.d.ts         # Global types and module augmentation
```

**Key files:**

- `index.d.ts` - Inertia-specific types (`PageProps`, pagination)
- `models.d.ts` - Laravel model TypeScript interfaces
- `global.d.ts` - Global declarations (window, route helper)

## Core Conventions

### 1. Model Type Definitions

Define Laravel models in `resources/js/types/models.d.ts`:

```ts
export interface User {
  id: number
  name: string
  first_name: string
  email: string
  email_verified_at: string | null
  two_factor_confirmed_at: string | null
  language: string
  avatar_url: string | null
}

export interface Post {
  id: number
  title: string
  content: string
  user_id: number
  user?: User
  created_at: string
  updated_at: string
}
```

**Key Requirements:**

- Use `export interface` for all models
- Match Laravel model properties exactly
- Use `snake_case` to match Laravel conventions
- Mark nullable fields with `| null`
- Use `?` for optional relationships
- Use `string` for dates (ISO 8601 format from API)

### 2. Inertia PageProps Type

Define shared page props in `resources/js/types/index.d.ts`:

```ts
import type { User } from '@/types/models'

export interface SupportedLocale {
  name: string
  native_name: string
  regional: string
}

export type PageProps<
  T extends Record<string, unknown> = Record<string, unknown>,
> = T & {
  user: User | null
  supportedLocales: Record<string, SupportedLocale>
}
```

Use `PageProps<T>` for page-specific props:

```tsx
import type { PageProps } from '@/types'
import type { User } from '@/types/models'

interface UsersIndexProps extends PageProps {
  users: User[]
}

export default function UsersIndex() {
  const { users, user } = usePage<UsersIndexProps>().props
  // `users` is typed, `user` is inherited from PageProps
}
```

### 3. Global Type Declarations

Define global types in `resources/js/types/global.d.ts`:

```ts
import type { PageProps as InertiaPageProps } from '@inertiajs/core'
import type { AxiosInstance, AxiosStatic } from 'axios'
import { route as ziggyRoute } from 'ziggy-js'
import type { PageProps as AppPageProps } from './'

declare global {
  interface Window {
    axios: AxiosInstance
    Pusher: typeof Pusher
    Echo: typeof Echo
  }

  const axios: AxiosStatic
  const Pusher: typeof Pusher
  const Echo: typeof Echo
  const route: typeof ziggyRoute
}

declare module '@inertiajs/core' {
  interface PageProps extends InertiaPageProps, AppPageProps {}
}
```

**Purpose:**

- Augment `Window` interface for global variables
- Declare global constants (`route`, `axios`)
- Extend Inertia's `PageProps` with app-specific props

### 4. Utility Types

Define reusable utility types:

```ts
export interface PaginationMeta {
  current_page: number
  from: number
  last_page: number
  path: string
  per_page: number
  to: number
  total: number
  links: {
    url: string | null
    label: string
    active: boolean
  }[]
}

export interface PaginatedData<TData> {
  data: TData[]
  meta: PaginationMeta
}
```

Usage:

```tsx
import type { PaginatedData } from '@/types'
import type { User } from '@/types/models'

interface UsersIndexProps extends PageProps {
  users: PaginatedData<User>
}
```

## Examples

### Example 1: Model Types

```ts
// resources/js/types/models.d.ts

export interface User {
  id: number
  name: string
  email: string
  email_verified_at: string | null
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  content: string
  user_id: number
  post_id: number
  user?: User
  created_at: string
  updated_at: string
}

export interface Post {
  id: number
  title: string
  content: string
  user_id: number
  user?: User
  comments?: Comment[]
  comments_count?: number
  created_at: string
  updated_at: string
}
```

### Example 2: Page Props

```ts
// resources/js/types/index.d.ts

import type { User } from '@/types/models'

export interface SupportedLocale {
  name: string
  native_name: string
  regional: string
}

export type PageProps<
  T extends Record<string, unknown> = Record<string, unknown>,
> = T & {
  user: User | null
  supportedLocales: Record<string, SupportedLocale>
  flash?: {
    success?: string
    error?: string
  }
}

export interface PaginationMeta {
  current_page: number
  last_page: number
  per_page: number
  total: number
}

export interface PaginatedData<TData> {
  data: TData[]
  meta: PaginationMeta
}
```

### Example 3: Enum Types

```ts
// resources/js/types/models.d.ts

export type UserRole = 'admin' | 'user' | 'guest'

export type PostStatus = 'draft' | 'published' | 'archived'

export interface User {
  id: number
  name: string
  email: string
  role: UserRole
}

export interface Post {
  id: number
  title: string
  status: PostStatus
}
```

### Example 4: Component Props Types

```ts
// Inline with component
interface UserCardProps {
  user: User
  showEmail?: boolean
  onEdit?: (user: User) => void
}

export function UserCard({ user, showEmail, onEdit }: UserCardProps) {
  // ...
}
```

Or in separate types file for shared props:

```ts
// resources/js/types/components.d.ts

import type { User } from '@/types/models'

export interface UserCardProps {
  user: User
  showEmail?: boolean
  onEdit?: (user: User) => void
}
```

## Anti-Patterns

### ❌ Don't Do This

```ts
// Don't use `any`
export interface User {
  data: any // ❌ Type it properly
}

// Don't use `type` for models (use `interface`)
export type User = {
  // ❌ Use interface
  id: number
}

// Don't use camelCase for Laravel properties
export interface User {
  emailVerifiedAt: string | null // ❌ Use email_verified_at
}

// Don't forget nullable fields
export interface User {
  email_verified_at: string // ❌ Should be string | null
}

// Don't use default exports for types
export default interface User {} // ❌ Use named export

// Don't define component props in global types
// resources/js/types/index.d.ts
export interface ButtonProps {} // ❌ Define inline with component
```

### ✅ Do This Instead

```ts
// Use proper types
export interface User {
  data: UserData
}

// Use interface for models
export interface User {
  id: number
}

// Use snake_case to match Laravel
export interface User {
  email_verified_at: string | null
}

// Mark nullable fields
export interface User {
  email_verified_at: string | null
  avatar_url: string | null
}

// Use named exports
export interface User {}

// Define component props inline
interface ButtonProps {
  label: string
}

export function Button({ label }: ButtonProps) {}
```

## Type Importing

Use `import type` for type-only imports:

```tsx
import type { User } from '@/types/models'
import type { PageProps } from '@/types'
import { usePage } from '@inertiajs/react'

interface DashboardProps extends PageProps {
  users: User[]
}

export default function Dashboard() {
  const { users } = usePage<DashboardProps>().props
}
```

**Why `import type`?**

- Ensures types are stripped during compilation
- Makes it clear the import is only for types
- Prevents runtime imports for type-only dependencies

## Generic Types

Use generics for reusable types:

```ts
export interface ApiResponse<TData> {
  data: TData
  message: string
  success: boolean
}

export interface ResourceCollection<TResource> {
  data: TResource[]
  links: {
    first: string
    last: string
    next: string | null
    prev: string | null
  }
  meta: PaginationMeta
}
```

Usage:

```tsx
import type { ApiResponse } from '@/types'
import type { User } from '@/types/models'

const response: ApiResponse<User> = await fetch('/api/user').then((r) =>
  r.json()
)
```

## Quality Standards

- All types must be explicitly defined (no `any`)
- Use `interface` for object types
- Use `type` for unions, intersections, and aliases
- Use `import type` for type-only imports
- Match Laravel model properties exactly (snake_case)
- Mark nullable fields with `| null`
- Use generics for reusable types
- Document complex types with JSDoc comments
- Keep types organized by file purpose
