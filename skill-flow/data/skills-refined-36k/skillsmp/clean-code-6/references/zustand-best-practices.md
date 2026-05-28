# Zustand v5 Best Practices

## Store Creation (v5 Syntax)

### Basic Store with TypeScript

```typescript
import { create } from "zustand";

interface BearState {
  bears: number;
  increase: () => void;
  decrease: () => void;
  reset: () => void;
}

// Use curried syntax for TypeScript
const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
  reset: () => set({ bears: 0 }),
}));
```

### Usage in Components

```typescript
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  return <h1>{bears} bears</h1>;
}

function Controls() {
  const increase = useBearStore((state) => state.increase);
  return <button onClick={increase}>Add bear</button>;
}
```

### External Access (Outside React)

```typescript
// Get current state
const bears = useBearStore.getState().bears;

// Update state
useBearStore.setState({ bears: 10 });

// Subscribe to changes
const unsub = useBearStore.subscribe((state) => console.log(state));
unsub(); // Unsubscribe
```

---

## Slices Pattern

Split large stores into composable slices:

```typescript
import { create, StateCreator } from "zustand";

interface UserSlice {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  clearCart: () => void;
}

const createUserSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  UserSlice
> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
});

const createCartSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  CartSlice
> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  clearCart: () => set({ items: [] }),
});

// Combine slices
const useStore = create<UserSlice & CartSlice>()((...args) => ({
  ...createUserSlice(...args),
  ...createCartSlice(...args),
}));
```

---

## Selectors & Performance

### Always Use Selectors

```typescript
// ❌ BAD - Re-renders on ANY store change
function UserName() {
  const store = useUserStore();
  return <span>{store.user?.name}</span>;
}

// ✅ GOOD - Only re-renders when user.name changes
function UserName() {
  const name = useUserStore((state) => state.user?.name);
  return <span>{name}</span>;
}
```

### useShallow for Multiple Values

```typescript
import { useShallow } from 'zustand/react/shallow';

function UserInfo() {
  // Only re-renders when these specific values change
  const { name, email } = useUserStore(
    useShallow((state) => ({
      name: state.user?.name,
      email: state.user?.email
    }))
  );

  return <div>{name} - {email}</div>;
}

// Array destructuring
function BearFood() {
  const [nuts, honey] = useBearStore(
    useShallow((state) => [state.nuts, state.honey])
  );
  return <div>Nuts: {nuts}, Honey: {honey}</div>;
}
```

---

## Persist Middleware

### Basic Persistence

```typescript
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

interface SettingsStore {
  theme: "light" | "dark";
  setTheme: (theme: "light" | "dark") => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: "light",
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: "settings-storage", // localStorage key
    },
  ),
);
```

### Selective Persistence

```typescript
const useStore = create(
  persist(
    (set) => ({
      user: null,
      tempData: "not persisted",
      setUser: (user) => set({ user }),
    }),
    {
      name: "app-storage",
      partialize: (state) => ({ user: state.user }), // Only persist user
    },
  ),
);
```

### Migration Between Versions

```typescript
const useStore = create(
  persist(
    (set) => ({
      version: 2,
      data: {},
    }),
    {
      name: "app-storage",
      version: 2,
      migrate: (persistedState, version) => {
        if (version === 1) {
          // Migrate from v1 to v2
          return { ...persistedState, newField: "default" };
        }
        return persistedState;
      },
    },
  ),
);
```

---

## Devtools Integration

```typescript
import { create } from "zustand";
import { devtools } from "zustand/middleware";

const useBearStore = create<BearState>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: () =>
        set(
          (state) => ({ bears: state.bears + 1 }),
          undefined,
          "bears/increase", // Action name in devtools
        ),
    }),
    {
      name: "BearStore",
      enabled: process.env.NODE_ENV !== "production",
    },
  ),
);
```

---

## Immer Middleware

For easy nested state updates:

```typescript
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface TodoStore {
  todos: Record<string, Todo>;
  toggleTodo: (id: string) => void;
  updateTitle: (id: string, title: string) => void;
}

const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: {},
    toggleTodo: (id) =>
      set((state) => {
        state.todos[id].done = !state.todos[id].done;
      }),
    updateTitle: (id, title) =>
      set((state) => {
        state.todos[id].title = title;
      }),
  })),
);
```

---

## Combining Middleware

```typescript
import { create } from "zustand";
import { devtools, persist, subscribeWithSelector } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";

const useStore = create<State>()(
  devtools(
    persist(
      subscribeWithSelector(
        immer((set) => ({
          // Store definition
        })),
      ),
      { name: "app-storage" },
    ),
    { name: "AppStore" },
  ),
);
```

---

## Subscribe to Specific Changes

```typescript
import { create } from "zustand";
import { subscribeWithSelector } from "zustand/middleware";
import { shallow } from "zustand/vanilla/shallow";

const useStore = create(
  subscribeWithSelector((set) => ({
    paw: true,
    fur: "brown",
    age: 5,
  })),
);

// Subscribe to specific property
useStore.subscribe(
  (state) => state.age,
  (age, prevAge) => console.log("Age changed:", prevAge, "->", age),
);

// Subscribe with shallow comparison
useStore.subscribe(
  (state) => ({ paw: state.paw, fur: state.fur }),
  (current, prev) => console.log("Changed"),
  { equalityFn: shallow },
);

// Fire immediately on subscribe
useStore.subscribe(
  (state) => state.age,
  (age) => console.log("Current age:", age),
  { fireImmediately: true },
);
```

---

## When to Use Zustand vs TanStack Query

| Use Case           | Zustand | TanStack Query |
| ------------------ | ------- | -------------- |
| API data           | ❌      | ✅             |
| UI state           | ✅      | ❌             |
| Theme/preferences  | ✅      | ❌             |
| Shopping cart      | ✅      | ❌             |
| Auth token         | ✅      | ❌             |
| User profile (API) | ❌      | ✅             |
| WebSocket data     | ✅      | ❌             |
| Form state         | ❌      | ❌ (use React) |

### Hybrid Pattern

```typescript
// TanStack Query for server state
function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => api.getUser(id),
  });
}

// Zustand for UI state
const useUIStore = create<UIStore>()((set) => ({
  selectedUserId: null,
  setSelectedUser: (id) => set({ selectedUserId: id }),
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));

// Use both together
function UserList() {
  const { data: users } = useUsers();
  const { selectedUserId, setSelectedUser } = useUIStore();

  return (
    <ul>
      {users?.map((user) => (
        <li
          key={user.id}
          onClick={() => setSelectedUser(user.id)}
          className={selectedUserId === user.id ? 'selected' : ''}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

---

## React 19 / Next.js Compatibility

### Client Components Only

```typescript
// ❌ Won't work in Server Components
import { useBearStore } from './store';

export default async function ServerComponent() {
  const bears = useBearStore((state) => state.bears); // Error!
}

// ✅ Use in Client Components
'use client';

import { useBearStore } from './store';

export default function ClientComponent() {
  const bears = useBearStore((state) => state.bears);
  return <div>{bears}</div>;
}
```

### SSR Hydration Safety

```typescript
import { useState, useEffect } from 'react';

function useHydratedStore<T, R>(
  store: (selector: (state: T) => R) => R,
  selector: (state: T) => R
): R | undefined {
  const value = store(selector);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setHydrated(true);
  }, []);

  return hydrated ? value : undefined;
}

// Usage - prevents hydration mismatch
function ThemeToggle() {
  const theme = useHydratedStore(useSettingsStore, (s) => s.theme);

  if (!theme) return null; // SSR placeholder
  return <button>{theme}</button>;
}
```

---

## Testing

### Jest/Vitest Mock Setup

```typescript
// __mocks__/zustand.ts
import { act } from "@testing-library/react";
import * as zustand from "zustand";

const storeResetFns = new Set<() => void>();

const createMock = (createState) => {
  const store = zustand.create(createState);
  const initialState = store.getState();
  storeResetFns.add(() => store.setState(initialState, true));
  return store;
};

afterEach(() => {
  act(() => storeResetFns.forEach((reset) => reset()));
});

export const create = createMock;
```

### Reset Pattern

```typescript
const initialState = { bears: 0 };

const useBearStore = create<BearState>()((set, get, store) => ({
  ...initialState,
  increase: () => set((s) => ({ bears: s.bears + 1 })),
  reset: () => set(store.getInitialState()),
}));
```

---

## Best Practices Summary

### Do's ✅

- Use separate stores for different domains
- Always use selectors to prevent re-renders
- Use `useShallow` for multiple values
- Use Zustand for client/UI state only
- Use TanStack Query for server state
- Mark stores with `'use client'` in Next.js

### Don'ts ❌

- Don't store server data in Zustand
- Don't subscribe to entire store
- Don't create one giant store
- Don't mutate state directly
- Don't use in React Server Components
