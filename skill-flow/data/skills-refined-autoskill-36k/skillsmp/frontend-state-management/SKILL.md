---
name: frontend-state-management
description: Provides comprehensive state management patterns for React applications. This skill should be used when deciding how to manage different types of state, choosing state management solutions, or implementing state logic.
---

# Frontend State Management

This skill provides patterns for managing state effectively in React applications by categorizing state into different types and using appropriate solutions for each.

## Core Principle

**Don't store all state in a single centralized repository.** Instead, categorize state based on usage and manage each category with the most appropriate solution.

## State Categories

### 1. Component State

**What**: State specific to individual components that doesn't need to be shared globally.

**When to use**:
- UI state (open/closed, selected tab, form input values)
- State only needed by one component and its children
- Temporary state that doesn't persist

**Solutions**:
- `useState` - For simple, independent state
- `useReducer` - For complex state where one action updates multiple values

**Example** (useState):

```typescript
function Accordion() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Open'}
      </button>
      {isOpen && <div>Accordion content</div>}
    </div>
  );
}
```

**Example** (useReducer):

```typescript
interface DashboardState {
  sidebarOpen: boolean;
  selectedView: 'grid' | 'list';
  filters: Record<string, string>;
}

type DashboardAction =
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_VIEW'; view: 'grid' | 'list' }
  | { type: 'SET_FILTER'; key: string; value: string }
  | { type: 'RESET_FILTERS' };

function dashboardReducer(state: DashboardState, action: DashboardAction): DashboardState {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarOpen: !state.sidebarOpen };
    case 'SET_VIEW':
      return { ...state, selectedView: action.view };
    case 'SET_FILTER':
      return { ...state, filters: { ...state.filters, [action.key]: action.value } };
    case 'RESET_FILTERS':
      return { ...state, filters: {} };
    default:
      return state;
  }
}

function DashboardLayout() {
  const [state, dispatch] = useReducer(dashboardReducer, {
    sidebarOpen: true,
    selectedView: 'grid',
    filters: {},
  });

  return (
    <div>
      <button onClick={() => dispatch({ type: 'TOGGLE_SIDEBAR' })}>
        Toggle Sidebar
      </button>
      {/* ... */}
    </div>
  );
}
```

### 2. Application State

**What**: Global state that needs to be accessed across multiple components (e.g., theme, notifications, modals).

**When to use**:
- State needed by many unrelated components
- Global UI state (theme, language, notifications)
- User preferences

**Solutions**:
- **Context + Hooks** - Built-in React solution, good for simple global state
- **Zustand** - Lightweight, simple API, great for most use cases
- **Redux Toolkit** - For complex state with many actions and middleware needs
- **Jotai** - Atomic state management
- **XState** - State machines for complex state logic

**Example** (Context + Hooks):

```typescript
// src/stores/notifications-store.tsx
import { createContext, useContext, useState } from 'react';

interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface NotificationsContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
}

const NotificationsContext = createContext<NotificationsContextType | null>(null);

export function NotificationsProvider({ children }: { children: React.ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (notification: Omit<Notification, 'id'>) => {
    const id = Math.random().toString(36);
    setNotifications((prev) => [...prev, { ...notification, id }]);
    
    // Auto-remove after 5 seconds
    setTimeout(() => removeNotification(id), 5000);
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <NotificationsContext.Provider value={{ notifications, addNotification, removeNotification }}>
      {children}
    </NotificationsContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationsContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationsProvider');
  }
  return context;
}
```

**Example** (Zustand):

```typescript
// src/stores/theme-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ThemeStore {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: 'light',
      toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'theme-storage',
    }
  )
);

// Usage in component
function ThemeToggle() {
  const { theme, toggleTheme } = useThemeStore();
  return <button onClick={toggleTheme}>{theme} mode</button>;
}
```

### 3. Server Cache State

**What**: Data fetched from the server that needs to be cached locally.

**When to use**:
- Any data fetched from an API
- Data that needs caching, background refetching, or optimistic updates
- Server-side data that multiple components need

**Solutions**:
- **TanStack Query** (React Query) - Best for REST and GraphQL (recommended)
- **SWR** - Alternative to React Query
- **Apollo Client** - For GraphQL only
- **RTK Query** - Redux Toolkit's data fetching solution

**Why not Redux/Zustand**: Server cache has unique requirements (caching, refetching, invalidation) that are better handled by specialized libraries.

**Example** (TanStack Query):

```typescript
// Already covered in frontend-api-layer skill
// See that skill for detailed examples
import { useQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <LoadingSpinner />;
  return <div>{user.name}</div>;
}
```

### 4. Form State

**What**: State for managing form inputs, validation, and submission.

**When to use**:
- Any form with validation
- Multi-step forms
- Forms with complex validation logic

**Solutions**:
- **React Hook Form** - Lightweight, great performance (recommended)
- **Formik** - More features, slightly heavier
- **React Final Form** - Alternative option

**Integration with validation**:
- **Zod** - TypeScript-first validation (recommended)
- **Yup** - Popular alternative

**Example** (React Hook Form + Zod):

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define validation schema
const registerSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    await registerUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <input type="password" {...register('confirmPassword')} />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

### 5. URL State

**What**: State stored in the URL (query parameters, route parameters).

**When to use**:
- Shareable state (filters, search, pagination)
- State that should persist on page refresh
- State that should be bookmarkable

**Solutions**:
- **TanStack Router** - Type-safe routing with URL state (recommended for Eridu)
- **React Router** - Popular routing library
- **URLSearchParams** - Native browser API

**Example** (TanStack Router):

```typescript
import { useNavigate, useSearch } from '@tanstack/react-router';

// Define search params schema
const searchSchema = z.object({
  page: z.number().default(1),
  search: z.string().default(''),
  filter: z.enum(['all', 'active', 'archived']).default('all'),
});

function ProductsList() {
  const navigate = useNavigate();
  const search = useSearch({ from: '/products' }); // Type-safe!

  const updateSearch = (newSearch: string) => {
    navigate({
      search: (prev) => ({ ...prev, search: newSearch, page: 1 }),
    });
  };

  return (
    <div>
      <input
        value={search.search}
        onChange={(e) => updateSearch(e.target.value)}
      />
      {/* Products list using search.page, search.filter, etc. */}
    </div>
  );
}
```

## State Colocation

**Principle**: Keep state as close as possible to where it's used.

**Benefits**:
- Easier to understand and maintain
- Better performance (smaller re-render scope)
- Easier to test

```typescript
// ❌ BAD: Global state for component-specific UI
const useGlobalStore = create((set) => ({
  isModalOpen: false,
  setModalOpen: (open) => set({ isModalOpen: open }),
}));

function MyComponent() {
  const { isModalOpen, setModalOpen } = useGlobalStore();
  // ...
}

// ✅ GOOD: Local state for component-specific UI
function MyComponent() {
  const [isModalOpen, setModalOpen] = useState(false);
  // ...
}
```

## Decision Tree

Use this decision tree to choose the right state management solution:

1. **Is it server data?** → Use TanStack Query
2. **Is it form data?** → Use React Hook Form + Zod
3. **Should it be in the URL?** → Use TanStack Router search params
4. **Is it only used in one component?** → Use useState/useReducer
5. **Is it shared across many components?** → Use Context or Zustand

## Best Practices

1. **Start local, lift when needed** - Begin with component state, only lift to global when necessary
2. **Separate concerns** - Don't mix server cache with application state
3. **Use the right tool** - Each state category has optimal solutions
4. **Colocate state** - Keep state close to where it's used
5. **Avoid prop drilling** - Use Context or global state for deeply nested props
6. **Type everything** - Use TypeScript for type-safe state management

## Checklist

- [ ] Server data is managed with TanStack Query (not Redux/Zustand)
- [ ] Forms use React Hook Form with Zod validation
- [ ] Component state uses useState or useReducer
- [ ] Global state uses Context or Zustand (not Redux unless needed)
- [ ] URL state is used for shareable/bookmarkable state
- [ ] State is colocated as close as possible to usage
- [ ] No unnecessary global state
- [ ] All state is properly typed with TypeScript
