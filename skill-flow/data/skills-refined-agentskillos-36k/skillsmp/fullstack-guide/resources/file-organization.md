# File Organization

Proper file and directory structure for maintainable, scalable frontend code.

---

## features/ vs components/ Distinction

### features/ Directory

**Purpose**: Domain-specific features with their own logic, API, and components

**When to use:**
- Feature has multiple related components
- Feature has its own API endpoints
- Feature has domain-specific logic
- Feature has custom hooks/utilities

**Examples:**
- `features/posts/` - Post management
- `features/auth/` - Authentication flows
- `features/dashboard/` - Dashboard feature

**Structure:**
```
features/
  my-feature/
    api/
      myFeatureApi.ts         # API service layer
    components/
      MyFeatureMain.tsx       # Main component
      SubComponents/          # Related components
    hooks/
      useMyFeature.ts         # Custom hooks
      useSuspenseMyFeature.ts # Suspense hooks
    helpers/
      myFeatureHelpers.ts     # Utility functions
    types/
      index.ts                # TypeScript types
    index.ts                  # Public exports
```

### components/ Directory

**Purpose**: Truly reusable UI components that can be used anywhere

**When to use:**
- Component is generic and reusable
- Component has no domain-specific logic
- Component can be used across multiple features

**Examples:**
- `components/SuspenseLoader/`
- `components/CustomAppBar/`
- `components/ErrorBoundary/`
- `components/LoadingOverlay/`

**Structure:**
```
components/
  ComponentName/
    ComponentName.tsx       # Main component
    ComponentName.styles.ts # Styles (if > 100 lines)
    index.ts                # Export
```

---

## Import Aliases

### Available Aliases

```typescript
// Root imports
import { apiClient } from '@/lib/apiClient';

// Type imports
import type { User } from '~types/user';

// Component imports
import { SuspenseLoader } from '~components/SuspenseLoader';

// Feature imports
import { useAuth } from '~features/auth';
```

### Configuration

```json
// tsconfig.json
{
    "compilerOptions": {
        "paths": {
            "@/*": ["./src/*"],
            "~types/*": ["./src/types/*"],
            "~components/*": ["./src/components/*"],
            "~features/*": ["./src/features/*"]
        }
    }
}
```

---

## Naming Conventions

### Files and Directories

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase with use prefix | `useAuth.ts` |
| Utils/Helpers | camelCase | `formatDate.ts` |
| Types | camelCase | `user.ts` |
| API Services | camelCase with Api suffix | `userApi.ts` |
| Styles | Same name + .styles | `UserProfile.styles.ts` |
| Tests | Same name + .test | `UserProfile.test.tsx` |

### Directories

| Type | Convention | Example |
|------|------------|---------|
| Features | kebab-case | `user-management/` |
| Components | PascalCase | `UserProfile/` |
| Routes | kebab-case | `project-catalog/` |

---

## Feature Index Exports

### Public API Pattern

```typescript
// features/users/index.ts
// Export only what should be public

// Components
export { UserList } from './components/UserList';
export { UserProfile } from './components/UserProfile';

// Hooks
export { useUsers } from './hooks/useUsers';

// Types
export type { User, CreateUserDTO } from './types';

// API (usually internal, but export if needed)
export { userApi } from './api/userApi';
```

---

## Complete Directory Structure

```
src/
├── features/                    # Domain features
│   ├── auth/
│   ├── users/
│   └── posts/
│
├── components/                  # Shared components
│   ├── SuspenseLoader/
│   ├── CustomAppBar/
│   ├── ErrorBoundary/
│   └── LoadingOverlay/
│
├── routes/                      # TanStack Router routes
│   ├── __root.tsx
│   ├── index.tsx
│   ├── users/
│   │   ├── index.tsx
│   │   └── $userId.tsx
│   └── posts/
│
├── hooks/                       # Shared hooks
│   ├── useAuth.ts
│   ├── useMuiSnackbar.ts
│   └── useDebounce.ts
│
├── lib/                         # Shared utilities
│   ├── apiClient.ts
│   └── utils.ts
│
├── types/                       # Shared TypeScript types
│   ├── user.ts
│   ├── post.ts
│   └── common.ts
│
├── config/                      # Configuration
│   └── theme.ts
│
└── App.tsx                      # Root component
```

---

## Summary

**Key Principles:**
1. **features/** for domain-specific code
2. **components/** for truly reusable UI
3. Use subdirectories: api/, components/, hooks/, helpers/, types/
4. Import aliases for clean imports
5. Consistent naming conventions
6. Export public API from feature index.ts

**See Also:**
- [component-patterns.md](component-patterns.md) - Component structure
- [data-fetching.md](data-fetching.md) - API service patterns
