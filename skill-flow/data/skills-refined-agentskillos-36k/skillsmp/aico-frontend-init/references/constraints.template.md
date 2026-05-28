# Frontend Constraints

> Project: [PROJECT_NAME]
> Created: [CREATED_DATE]
> Last Updated: [UPDATED_DATE]

## Tech Stack

### Framework

- **Framework**: React 18+
- **Language**: TypeScript (strict mode)
- **Build Tool**: Vite

### Styling

- **CSS Framework**: Tailwind CSS
- **Component Library**: shadcn/ui
- **Icons**: Lucide React

### State Management

- **Local State**: React useState/useReducer
- **Server State**: TanStack Query (React Query)
- **Global State**: Zustand (if needed)

### Testing

- **Unit Testing**: Vitest + React Testing Library
- **E2E Testing**: Playwright
- **Coverage Target**: 80%

## Directory Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/              # shadcn/ui components
│   └── [Feature]/       # Feature-specific components
├── pages/               # Page components (or app/ for Next.js)
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions
├── services/            # API services
├── stores/              # State stores (Zustand)
├── types/               # TypeScript types
└── styles/              # Global styles
```

## Naming Conventions

### Files

- Components: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useAuth.ts`)
- Utils: `camelCase.ts` (e.g., `formatDate.ts`)
- Types: `camelCase.ts` (e.g., `user.ts`)
- Tests: `[name].test.tsx` (e.g., `UserProfile.test.tsx`)

### Components

- Component names: PascalCase
- Props interface: `[ComponentName]Props`
- Event handlers: `handle[Event]` (e.g., `handleClick`)
- Boolean props: `is/has/should` prefix (e.g., `isLoading`)

### CSS Classes

- Use Tailwind utility classes
- Custom classes: kebab-case
- Component variants: use `cva` (class-variance-authority)

## Code Patterns

### Component Structure

```tsx
import React from 'react'
import { cn } from '@/lib/utils'

interface ComponentProps {
  // Props here
}

export function Component({ ...props }: ComponentProps) {
  // Hooks first
  // Event handlers
  // Render
  return (
    // JSX
  )
}
```

### Custom Hooks

```tsx
export function useCustomHook() {
  // State
  // Effects
  // Callbacks
  // Return object with named properties
  return { data, isLoading, error };
}
```

### API Calls

```tsx
// Use TanStack Query for data fetching
const { data, isLoading, error } = useQuery({
  queryKey: ['resource', id],
  queryFn: () => fetchResource(id),
});
```

## Component Guidelines

### Accessibility

- All interactive elements must be keyboard accessible
- Use semantic HTML elements
- Include ARIA labels where needed
- Ensure color contrast meets WCAG AA

### Performance

- Use `React.memo` for expensive components
- Use `useMemo` and `useCallback` appropriately
- Lazy load routes and heavy components
- Optimize images (next/image or similar)

### Error Handling

- Always handle loading, error, and empty states
- Use Error Boundaries for component errors
- Show user-friendly error messages

## Testing Requirements

### Unit Tests

- Test component rendering
- Test user interactions
- Test edge cases (loading, error, empty)
- Mock external dependencies

### E2E Tests

- Test critical user flows
- Test form submissions
- Test navigation

## Git Conventions

### Commit Messages

```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
Scope: component name or feature area
```

### Branch Naming

```
feature/[feature-name]
fix/[bug-description]
refactor/[area]
```

## Dependencies

### Approved Packages

- `date-fns` for date manipulation
- `zod` for validation
- `react-hook-form` for forms
- `@tanstack/react-query` for server state

### Avoid

- moment.js (use date-fns instead)
- jQuery (use React patterns)
- CSS-in-JS runtime libraries (use Tailwind)
