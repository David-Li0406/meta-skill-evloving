---
name: zustand-patterns
description: Zustand patterns for predictable client-side state management
---

# Zustand State Management Patterns

## Basic Store

### Simple Store

```tsx
// stores/counter.ts
import { create } from 'zustand';

interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

### Usage

```tsx
'use client';

import { useCounterStore } from '@/stores/counter';

export function Counter() {
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

## Store Patterns

### Slice Pattern

Split large stores into focused slices:

```tsx
// stores/app-store.ts
import { create } from 'zustand';

// Auth slice
interface AuthSlice {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

const createAuthSlice = (set): AuthSlice => ({
  user: null,
  isAuthenticated: false,
  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
});

// UI slice
interface UISlice {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

const createUISlice = (set): UISlice => ({
  sidebarOpen: true,
  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen })),
});

// Combined store
type AppState = AuthSlice & UISlice;

export const useAppStore = create<AppState>()((...a) => ({
  ...createAuthSlice(...a),
  ...createUISlice(...a),
}));
```

### Computed Values

Derive values from state:

```tsx
interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  // Computed value as function
  total: () => number;
  itemCount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),
  total: () => {
    return get().items.reduce((sum, item) => sum + item.price, 0);
  },
  itemCount: () => get().items.length,
}));

// Usage
function CartSummary() {
  const total = useCartStore((state) => state.total());
  const itemCount = useCartStore((state) => state.itemCount());

  return <div>Total: ${total} ({itemCount} items)</div>;
}
```

## Selectors

### Optimized Selectors

Prevent unnecessary re-renders:

```tsx
import { useCartStore } from '@/stores/cart';
import { shallow } from 'zustand/shallow';

// Bad: Entire store subscribed
function BadComponent() {
  const store = useCartStore();
  return <div>{store.items.length}</div>;
}

// Good: Only subscribe to needed value
function GoodComponent() {
  const itemCount = useCartStore((state) => state.items.length);
  return <div>{itemCount}</div>;
}

// Better: Multiple values with shallow comparison
function BetterComponent() {
  const { items, addItem } = useCartStore(
    (state) => ({ items: state.items, addItem: state.addItem }),
    shallow
  );

  return <div>{items.length}</div>;
}
```

### Custom Selectors

```tsx
// stores/selectors.ts
import { useUserStore } from './user';

export const useIsAdmin = () =>
  useUserStore((state) => state.user?.role === 'admin');

export const useUserName = () =>
  useUserStore((state) => state.user?.name ?? 'Guest');

export const useHasPermission = (permission: string) =>
  useUserStore((state) =>
    state.user?.permissions.includes(permission)
  );

// Usage
function AdminPanel() {
  const isAdmin = useIsAdmin();
  if (!isAdmin) return null;
  return <div>Admin Panel</div>;
}
```

## Async Actions

### Fetch Data

```tsx
interface PostsState {
  posts: Post[];
  isLoading: boolean;
  error: string | null;
  fetchPosts: () => Promise<void>;
}

export const usePostsStore = create<PostsState>((set) => ({
  posts: [],
  isLoading: false,
  error: null,
  fetchPosts: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('/api/posts');
      const posts = await response.json();
      set({ posts, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));

// Usage
function PostList() {
  const { posts, isLoading, error, fetchPosts } = usePostsStore();

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  if (isLoading) return <Loading />;
  if (error) return <Error message={error} />;
  return <div>{posts.map((post) => <PostCard post={post} />)}</div>;
}
```

## Middleware

### Persist

Persist state to localStorage:

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface UserPreferences {
  theme: 'light' | 'dark';
  language: string;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: string) => void;
}

export const usePreferencesStore = create<UserPreferences>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'user-preferences', // localStorage key
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }), // Only persist these fields
    }
  )
);
```

### Devtools

Redux DevTools integration:

```tsx
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export const useAppStore = create<AppState>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
      decrement: () => set((state) => ({ count: state.count - 1 }), false, 'decrement'),
    }),
    { name: 'AppStore' }
  )
);
```

### Immer

Use Immer for immutable updates:

```tsx
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface TodoState {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
}

export const useTodoStore = create<TodoState>()(
  immer((set) => ({
    todos: [],
    addTodo: (text) =>
      set((state) => {
        state.todos.push({ id: Date.now().toString(), text, done: false });
      }),
    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        if (todo) todo.done = !todo.done;
      }),
  }))
);
```

### Combined Middleware

```tsx
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

export const useStore = create<State>()(
  devtools(
    persist(
      immer((set) => ({
        // store implementation
      })),
      { name: 'app-storage' }
    ),
    { name: 'AppStore' }
  )
);
```

## Store Organization

### Structure

```
stores/
├── index.ts              # Export all stores
├── auth-store.ts         # Authentication state
├── cart-store.ts         # Shopping cart
├── ui-store.ts           # UI state (modals, sidebar, etc.)
├── preferences-store.ts  # User preferences
└── selectors/
    ├── auth-selectors.ts
    └── cart-selectors.ts
```

### Index File

```tsx
// stores/index.ts
export { useAuthStore } from './auth-store';
export { useCartStore } from './cart-store';
export { useUIStore } from './ui-store';
export { usePreferencesStore } from './preferences-store';
```

## TypeScript Patterns

### Typed Actions

```tsx
interface UserState {
  user: User | null;
  status: 'idle' | 'loading' | 'success' | 'error';
  error: string | null;
  setUser: (user: User) => void;
  clearUser: () => void;
  fetchUser: (id: string) => Promise<void>;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  status: 'idle',
  error: null,
  setUser: (user) => set({ user, status: 'success', error: null }),
  clearUser: () => set({ user: null, status: 'idle', error: null }),
  fetchUser: async (id) => {
    set({ status: 'loading' });
    try {
      const user = await api.fetchUser(id);
      set({ user, status: 'success', error: null });
    } catch (error) {
      set({ status: 'error', error: error.message });
    }
  },
}));
```

## Testing

### Test Setup

```tsx
// __tests__/stores/counter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounterStore } from '@/stores/counter';

describe('useCounterStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useCounterStore.setState({ count: 0 });
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounterStore());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounterStore());

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(-1);
  });
});
```

## Best Practices

### Do

- Keep stores focused on specific domains
- Use selectors to prevent unnecessary re-renders
- Use middleware for cross-cutting concerns
- Type all stores with TypeScript
- Extract complex logic to separate functions
- Use shallow comparison for object selections
- Persist only necessary state

### Don't

- Don't put all state in one store
- Don't select entire store when only part is needed
- Don't mutate state directly (use set or Immer)
- Don't use Zustand for server state (use React Query)
- Don't persist sensitive data
- Don't forget to reset state when needed

## When to Use

### Use Zustand

- Client-side UI state (modals, sidebar, theme)
- Form state (multi-step forms)
- Global app state (user preferences, settings)
- Temporary state shared across components

### Use React Query

- Server state (API data)
- Caching and revalidation
- Background updates
- Optimistic updates with server sync

### Use React State

- Local component state
- Form inputs
- Toggle states
- State not shared with other components

## Performance

### Optimization

- Use selective subscriptions (don't select entire store)
- Use shallow comparison for object selections
- Batch updates when possible
- Split large stores into smaller, focused stores
- Use computed values (functions) instead of derived state

### Monitoring

- Use Redux DevTools middleware in development
- Monitor render counts in React DevTools
- Profile component re-renders
- Check localStorage size if using persist
