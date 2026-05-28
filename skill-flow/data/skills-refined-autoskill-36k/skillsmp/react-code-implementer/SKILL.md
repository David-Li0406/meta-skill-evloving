---
name: react-code-implementer
description: Practical guidelines for implementing React 19 components with TypeScript
---

# React Code Implementation

## Component Implementation

### Default Approach

- Start with Server Components by default
- Add 'use client' only when needed
- Use TypeScript for all components
- Define prop types with interfaces
- Export component as named export

### Server Components

```tsx
// components/UserProfile.tsx
interface UserProfileProps {
  userId: string;
}

export async function UserProfile({ userId }: UserProfileProps) {
  const user = await fetchUser(userId); // Direct database/API call

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

**Guidelines:**
- Make async when fetching data
- Fetch data directly without useEffect
- No hooks allowed
- Can use Suspense boundaries for loading states
- Return JSX directly

### Client Components

```tsx
'use client';

import { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

export function Counter({ initialCount = 0 }: CounterProps) {
  const [count, setCount] = useState(initialCount);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**Guidelines:**
- Add 'use client' at the top
- Use hooks for state and effects
- Handle events and interactivity
- Optimize re-renders with memo/useMemo/useCallback

## State Management

### Local State

**Usage:** Component-specific state

**Tools:**
- `useState` for simple values
- `useReducer` for complex state logic

```tsx
const [isOpen, setIsOpen] = useState(false);
const [user, setUser] = useState<User | null>(null);
```

### Shared State

**Usage:** State shared across components

**Approaches:**
- **Lifting state:** Lift to common ancestor
- **Context:** Use Context for deep prop threading
- **Zustand:** Global client state management

```tsx
// Using Zustand store
import { useUserStore } from '@/stores/user';

export function UserMenu() {
  const { user, logout } = useUserStore();
  // ...
}
```

### Server State

**Usage:** Data from API/database

**Tool:** TanStack React Query

```tsx
'use client';

import { useQuery } from '@tanstack/react-query';

export function Posts() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <PostList posts={data} />;
}
```

## Hooks Implementation

### Custom Hooks

**Naming:** Always prefix with 'use'

```tsx
// hooks/useLocalStorage.ts
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

**Best Practices:**
- Return tuple [value, setValue] or object { data, error }
- Handle cleanup in useEffect return
- Memoize complex calculations
- Document dependencies and side effects

### Common Hooks

| Hook | Purpose |
|------|---------|
| useState | Local component state |
| useEffect | Side effects and subscriptions |
| useCallback | Memoize callback functions |
| useMemo | Memoize expensive calculations |
| useRef | Mutable refs and DOM access |
| useContext | Access context values |

## Error Handling

### Component Level

```tsx
'use client';

export function DataDisplay() {
  const { data, error, isLoading } = useQuery(queryOptions);

  if (error) {
    return (
      <ErrorAlert>
        <p>Failed to load data</p>
        <button onClick={() => refetch()}>Retry</button>
      </ErrorAlert>
    );
  }

  if (isLoading) return <LoadingSkeleton />;

  return <DataView data={data} />;
}
```

### Error Boundary

- **Usage:** Catch unexpected React errors
- **Implementation:** Use error.tsx in Next.js or custom boundary
- **Fallback:** Show user-friendly error message

## Styling

### Tailwind CSS

```tsx
<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Click me
</button>
```

### CSS Modules

```tsx
import styles from './Button.module.css';

<button className={styles.primary}>Click me</button>
```

### Conditional Classes

```tsx
import clsx from 'clsx';

<div className={clsx(
  'base-class',
  isActive && 'active',
  isDisabled && 'disabled'
)}>
```

## Forms

### Controlled Components

```tsx
const [email, setEmail] = useState('');

<input
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>
```

### Form Libraries

**Recommended:** React Hook Form for complex forms

```tsx
import { useForm } from 'react-hook-form';

const { register, handleSubmit, formState: { errors } } = useForm();

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('email', { required: true })} />
  {errors.email && <span>Email is required</span>}
</form>
```

## Performance

### Optimization Checklist

- Use React.memo for expensive pure components
- useMemo for expensive calculations
- useCallback for functions passed to children
- Split large components into smaller ones
- Lazy load components with dynamic imports
- Virtualize long lists

### When to Optimize

- After identifying actual performance issue
- For components that render frequently
- For expensive calculations
- Not prematurely - profile first

## Testing

### Component Tests

**Library:** React Testing Library

**Focus:** Test user behavior, not implementation

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Counter } from './Counter';

test('increments count on click', () => {
  render(<Counter />);
  const button = screen.getByRole('button');

  fireEvent.click(button);

  expect(button).toHaveTextContent('Count: 1');
});
```

## Code Quality Checklist

- [ ] All props have TypeScript types
- [ ] No 'any' types without justification
- [ ] Components are focused (single responsibility)
- [ ] Proper error handling
- [ ] Loading states for async operations
- [ ] Accessibility attributes (ARIA labels, roles)
- [ ] Tests cover main user flows
