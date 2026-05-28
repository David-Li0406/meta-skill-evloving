# Shared Feature

Cross-cutting concerns used by all features.

## Structure

```
features/shared/
├── components/
│   ├── client/           # Reusable client components
│   ├── server/           # Reusable server components
│   ├── skeletons/        # Shared loading skeletons
│   ├── ui/               # Shadcn/ui primitives
│   ├── layouts/          # Layout wrappers
│   ├── providers/        # Global providers (theme, etc.)
│   ├── ai-elements/      # AI-specific UI components
│   └── icons/            # SVG icons
├── hooks/                # Shared React hooks
├── lib/                  # Utilities (cn, etc.)
├── types/                # Shared types
├── schemas/              # Shared Zod schemas
└── constants/            # App constants
```

---

## Common Components

### Server
- `header.tsx` - Page header with breadcrumbs
- `app-sidebar.tsx` - Main sidebar
- `nav-recents-list.tsx` - Recent items with Suspense

### Client
- `theme-toggle.tsx` - Light/dark mode
- `nav-user.tsx` - User menu
- `logo.tsx` - Branding

### Skeletons
- `header-skeleton.tsx`
- `nav-recents-skeleton.tsx`
- `user-avatar-skeleton.tsx`

---

## Standard Types

### Action Response
```typescript
// features/shared/types/action-response.ts
export type ActionResponse<T> = {
  success: boolean
  data?: T
  error?: string
}
```

---

## Utilities

### Class Name Helper
```typescript
// features/shared/lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## UI Components (Shadcn)

Located in `components/ui/`. Common ones:

- `button.tsx`
- `card.tsx`
- `dialog.tsx`
- `dropdown-menu.tsx`
- `input.tsx`
- `skeleton.tsx`
- `toast.tsx`

### Usage
```typescript
import { Button } from '@/features/shared/components/ui/button'
import { Card, CardContent, CardHeader } from '@/features/shared/components/ui/card'
import { Skeleton } from '@/features/shared/components/ui/skeleton'
```

---

## Rules

1. **Base layer** - Shared imports nothing else from features
2. **Reusable only** - Only put truly shared code here
3. **No business logic** - Feature-specific logic stays in features
4. **Shadcn lives here** - All UI primitives in `components/ui/`
