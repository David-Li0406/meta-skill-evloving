# State Management Guide for Astro + React Projects

This guide covers state management patterns for Astro projects using React components, with a focus on 2026 best practices and islands architecture considerations.

## Table of Contents

1. [Understanding State in Astro](#understanding-state-in-astro)
2. [Local Component State](#local-component-state)
3. [Cross-Island State Management](#cross-island-state-management)
4. [Server State Management](#server-state-management)
5. [URL State](#url-state)
6. [Choosing the Right Solution](#choosing-the-right-solution)

## Understanding State in Astro

### The Islands Architecture Challenge

Astro's islands architecture means each React component hydrates in isolation. This has important implications for state management:

```astro
---
import Header from '@/components/Header.jsx';
import Sidebar from '@/components/Sidebar.jsx';
import MainContent from '@/components/MainContent.jsx';
---

<!-- ❌ Problem: React Context won't work across these islands -->
<Header client:load />
<Sidebar client:load />
<MainContent client:load />

<!-- ✅ Solution: Use external state management -->
<Header client:load />
<Sidebar client:load />
<MainContent client:load />
```

**Key Insight**: React Context API is scoped to individual islands. It cannot share state between different islands on the page.

### State Categories

1. **Local State**: Component-specific, no sharing needed
2. **Cross-Island State**: Shared between multiple React islands
3. **Server State**: Data from APIs, databases
4. **URL State**: Stored in search params, hashes
5. **Global State**: App-wide settings, themes, authentication

## Local Component State

### Use React Hooks (Best for Local State)

For component-specific state that doesn't need sharing, use React's built-in hooks:

```jsx
// src/components/Counter.jsx
import { useState, useReducer, useCallback } from 'react';

export default function Counter() {
  // ✅ useState for simple state
  const [count, setCount] = useState(0);

  // ✅ useReducer for complex state logic
  const [state, dispatch] = useReducer(counterReducer, {
    count: 0,
    step: 1,
  });

  // ✅ useCallback for memoized callbacks
  const increment = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

### When to Use Local State

- Form inputs and validation
- UI toggles (modals, dropdowns)
- Component-specific data
- Temporary states

## Cross-Island State Management

### Zustand (Recommended for Most Projects)

Zustand is the preferred choice for Astro projects in 2026 due to its simplicity and excellent cross-island support.

**Installation**:

```bash
npm install zustand
```

**Basic Setup**:

```typescript
// src/store/useStore.ts
import { create } from 'zustand';

interface StoreState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useStore = create<StoreState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

**Usage Across Islands**:

```astro
---
import Counter from '@/components/Counter.jsx';
import CountDisplay from '@/components/CountDisplay.jsx';
---

<!-- ✅ Both components share state via Zustand -->
<Counter client:load />
<CountDisplay client:load />
```

```jsx
// src/components/Counter.jsx
import { useStore } from '@/store/useStore';

export default function Counter() {
  const { increment, decrement, reset } = useStore();

  return (
    <div>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

```jsx
// src/components/CountDisplay.jsx
import { useStore } from '@/store/useStore';

export default function CountDisplay() {
  const count = useStore((state) => state.count);

  return <div>Count: {count}</div>;
}
```

**Advanced Zustand Patterns**:

```typescript
// src/store/useStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// ✅ Persist state to localStorage
export const useStore = create(
  persist(
    (set, get) => ({
      // Theme
      theme: 'light' as 'light' | 'dark',
      toggleTheme: () => {
        const currentTheme = get().theme;
        set({ theme: currentTheme === 'light' ? 'dark' : 'light' });
      },

      // User authentication
      user: null as { id: string; name: string } | null,
      setUser: (user) => set({ user }),
      logout: () => set({ user: null }),

      // Shopping cart
      cart: [] as Array<{ id: string; name: string; price: number }>,
      addToCart: (item) =>
        set((state) => ({ cart: [...state.cart, item] })),
      removeFromCart: (id) =>
        set((state) => ({
          cart: state.cart.filter((item) => item.id !== id),
        })),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// ✅ Create selectors for optimal reactivity
export const useTheme = () => useStore((state) => state.theme);
export const useUser = () => useStore((state) => state.user);
export const useCart = () => useStore((state) => state.cart);
```

### Redux Toolkit (For Large Teams)

Redux Toolkit provides structure and tooling for large teams and complex applications.

**Installation**:

```bash
npm install @reduxjs/toolkit react-redux
```

**Setup**:

```typescript
// src/store/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
}

const initialState: CounterState = {
  value: 0,
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;

export default counterSlice.reducer;
```

```typescript
// src/store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

```typescript
// src/store/hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './store';

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

**Usage in Components**:

```jsx
// src/components/Counter.jsx
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { increment, decrement } from '@/store/counterSlice';

export default function Counter() {
  const dispatch = useAppDispatch();
  const count = useAppSelector((state) => state.counter.value);

  return (
    <div>
      <div>Count: {count}</div>
      <button onClick={() => dispatch(increment())}>Increment</button>
      <button onClick={() => dispatch(decrement())}>Decrement</button>
    </div>
  );
}
```

### Jotai (For Atomic State)

Jotai provides a bottom-up approach where state is split into small atomic units.

**Installation**:

```bash
npm install jotai
```

**Setup**:

```typescript
// src/store/atoms.ts
import { atom } from 'jotai';

// ✅ Primitive atoms
export const countAtom = atom(0);
export const themeAtom = atom('light');

// ✅ Derived atoms
export const doubleCountAtom = atom((get) => get(countAtom) * 2);

// ✅ Read-write atoms with actions
export const counterWithActionsAtom = atom(
  (get) => get(countAtom),
  (get, set) => ({
    increment: () => set(countAtom, get(countAtom) + 1),
    decrement: () => set(countAtom, get(countAtom) - 1),
  })
);
```

**Usage**:

```jsx
// src/components/Counter.jsx
import { useAtom, useAtomValue, useSetAtom } from 'jotai';
import { countAtom, counterWithActionsAtom } from '@/store/atoms';

export default function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const actions = useAtomValue(counterWithActionsAtom);

  return (
    <div>
      <div>Count: {count}</div>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
      <button onClick={actions.decrement}>Decrement</button>
    </div>
  );
}
```

## Server State Management

### TanStack Query (React Query) - Recommended

For server state (data from APIs), use TanStack Query instead of global state management.

**Installation**:

```bash
npm install @tanstack/react-query
```

**Setup**:

```astro
---
// In your layout or root component
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});
---

<html>
  <body>
    <QueryClientProvider client={queryClient}>
      <slot />
      <ReactDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </body>
</html>
```

**Usage**:

```jsx
// src/components/Posts.jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export default function Posts() {
  const queryClient = useQueryClient();

  // ✅ Fetching data
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const response = await fetch('/api/posts');
      return response.json();
    },
  });

  // ✅ Mutations
  const mutation = useMutation({
    mutationFn: async (newPost) => {
      const response = await fetch('/api/posts', {
        method: 'POST',
        body: JSON.stringify(newPost),
      });
      return response.json();
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading posts</div>;

  return (
    <div>
      {data.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
      <button onClick={() => mutation.mutate({ title: 'New Post' })}>
        Add Post
      </button>
    </div>
  );
}
```

### SWR (Alternative to React Query)

```bash
npm install swr
```

```jsx
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then((r) => r.json());

export default function Posts() {
  const { data, error, isLoading } = useSWR('/api/posts', fetcher);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error</div>;

  return (
    <div>
      {data.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

## URL State

For shareable, bookmarkable state, use URL search parameters.

```jsx
// src/components/ProductList.jsx
import { useSearchParams } from 'react-router-dom';

export default function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const category = searchParams.get('category') || 'all';
  const page = parseInt(searchParams.get('page') || '1');

  const setCategory = (newCategory) => {
    setSearchParams(
      (prev) => {
        prev.set('category', newCategory);
        prev.set('page', '1'); // Reset page on category change
        return prev;
      },
      { replace: true }
    );
  };

  return (
    <div>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>
      <div>Current page: {page}</div>
    </div>
  );
}
```

## Choosing the Right Solution

### Decision Tree

```
Need state management?
│
├─ Is it component-specific only?
│  └─ YES → Use useState/useReducer
│
├─ Is it data from an API?
│  └─ YES → Use TanStack Query or SWR
│
├─ Is it URL/shareable state?
│  └─ YES → Use URL search params
│
├─ Do you need to share state across React islands?
│  ├─ Small to medium project?
│  │  └─ YES → Use Zustand
│  │
│  └─ Large team/enterprise?
│     └─ YES → Use Redux Toolkit
│
└─ Do you prefer atomic/state-splitting?
   └─ YES → Use Jotai
```

### Quick Comparison

| Solution | Best For | Bundle Size | Learning Curve | Cross-Island |
|----------|----------|-------------|----------------|--------------|
| useState | Local state | Built-in | Low | ❌ |
| Zustand | Most projects | ~1KB | Low | ✅ |
| Redux Toolkit | Large teams | ~12KB | Medium | ✅ |
| Jotai | Atomic state | ~3KB | Low | ✅ |
| TanStack Query | Server state | ~13KB | Medium | ✅ |
| SWR | Server state | ~4KB | Low | ✅ |

### 2026 Recommendations

1. **Start with useState** for component-local state
2. **Use Zustand** for cross-island state (simplest, most flexible)
3. **Use TanStack Query** for server state (caching, refetching, etc.)
4. **Use Redux Toolkit** only for large teams requiring strict patterns
5. **Consider Jotai** for atomic, composable state architecture

## Common Patterns

### Authentication State with Zustand

```typescript
// src/store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: { id: string; email: string; name: string } | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        const { user, token } = await response.json();

        set({ user, token, isAuthenticated: true });
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### Shopping Cart with Zustand

```typescript
// src/store/cartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => {
        const items = get().items;
        const existing = items.find((i) => i.id === item.id);

        if (existing) {
          set({
            items: items.map((i) =>
              i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
            ),
          });
        } else {
          set({ items: [...items, { ...item, quantity: 1 }] });
        }
      },

      removeItem: (id) => {
        set({ items: get().items.filter((i) => i.id !== id) });
      },

      updateQuantity: (id, quantity) => {
        set({
          items: get().items.map((i) =>
            i.id === id ? { ...i, quantity } : i
          ),
        });
      },

      clearCart: () => set({ items: [] }),

      total: () => {
        return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
```

## Sources

- [React State Management in 2026: Redux vs Zustand vs Jotai](https://inhaq.com/blog/react-state-management-2026-redux-vs-zustand-vs-jotai/)
- [Zustand vs Redux in 2026: Why I Switched](https://javascript.plainenglish.io/zustand-vs-redux-in-2026-why-i-switched-and-you-should-too-c119dd840ddb)
- [React Recap with Astro](https://dev.to/ingosteinke/react-recap-years-later-thanks-to-astro-2b4a)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
