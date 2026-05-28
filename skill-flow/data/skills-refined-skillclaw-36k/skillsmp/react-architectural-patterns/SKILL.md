---
name: react-architectural-patterns
description: React 19 architectural patterns, component design, and best practices
---

# React Architectural Patterns

## Architecture

### Component Types

#### Server Components

Default in React 19 - rendered on server only.

**Use Cases:**
- Data fetching from databases or APIs
- Accessing backend resources directly
- Keeping sensitive information on server
- Large dependencies that don't need client-side

**Characteristics:**
- Cannot use hooks (useState, useEffect, etc.)
- Cannot use browser APIs
- Can be async functions
- Better performance (less JavaScript to client)

#### Client Components

Interactive components that run on client.

**Use Cases:**
- Components using React hooks
- Event listeners and interactivity
- Browser APIs (localStorage, geolocation, etc.)
- Custom hooks usage

**Characteristics:**
- Must be marked with 'use client' directive
- Can use all React hooks
- Re-render on state changes
- Increases client bundle size

### Composition Patterns

#### Component Composition

- Prefer composition over inheritance
- Use children prop for flexible layouts
- Compound components for related functionality
- Higher-order components (HOCs) for cross-cutting concerns
- Render props for dynamic behavior

#### State Management

- Lift state up to common ancestor
- Use Context for deeply nested props
- External state manager (Zustand) for global state
- Server state manager (React Query) for API data
- Separate UI state from server state

#### Data Flow

- Unidirectional data flow (top-down)
- Props for component configuration
- Callbacks for child-to-parent communication
- Context for implicit prop threading

## Design Patterns

### Container/Presenter

Separate data fetching from presentation.

**Structure:**
- **Container:** Handles data fetching and business logic (Server Component)
- **Presenter:** Pure presentation component (can be Client Component)

**Benefits:**
- Easier testing of presentation logic
- Better performance with Server Components
- Clear separation of concerns

### Custom Hooks

Extract reusable stateful logic.

**Naming:** Always prefix with 'use' (useAuth, useLocalStorage)

**Guidelines:**
- One responsibility per hook
- Return arrays for multiple values [value, setValue]
- Return objects for named values { data, error, isLoading }
- Document hook behavior and dependencies

### Error Boundaries

Catch and handle React errors gracefully.

**Implementation:**
- Wrap entire app or route segments
- Provide fallback UI for errors
- Log errors to monitoring service
- Use error.tsx in Next.js for route-level boundaries

### Suspense Boundaries

Handle async operations with loading states.

**Usage:**
- Wrap async Server Components
- Show loading fallback during data fetch
- Nest Suspense for granular loading states
- Use loading.tsx in Next.js for route-level loading

## Code Organization

### File Structure

#### Component Files

- `ComponentName.tsx` - Main component
- `ComponentName.module.css` - Scoped styles (if needed)
- `ComponentName.test.tsx` - Component tests
- `ComponentName.stories.tsx` - Storybook stories (if used)
- `index.ts` - Barrel export

#### Feature Structure

```
features/feature-name/
├── components/    # Feature-specific components
├── hooks/         # Feature-specific hooks
├── types/         # TypeScript types
├── utils/         # Helper functions
└── index.ts       # Public API
```

### Import Organization

**Order:**
1. React and framework imports
2. External library imports
3. Internal module imports (using @/ alias)
4. Relative imports
5. Style imports
6. Type imports (using 'import type')

## Performance

### Optimization Techniques

- Use React.memo for expensive pure components
- Implement useMemo for expensive calculations
- Use useCallback for stable function references
- Code splitting with dynamic imports
- Lazy load components not needed immediately
- Virtualize long lists (react-window, react-virtuoso)

### Anti-Patterns

**Avoid:**
- Inline function definitions in JSX
- Creating objects/arrays in render
- Excessive use of Context causing re-renders
- Not memoizing context values
- Premature optimization without profiling

## Accessibility

### Requirements

- Use semantic HTML elements
- Provide ARIA labels where needed
- Ensure keyboard navigation works
- Maintain proper heading hierarchy
- Sufficient color contrast ratios
- Screen reader friendly text alternatives
