---
name: zustand-5
description: Use this skill when managing React state with Zustand, including creating stores, selectors, and using middleware for persistence.
---

# Skill body

## Basic Store

```typescript
import { create } from "zustand";

interface CounterStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// Usage
function Counter() {
  const { count, increment, decrement } = useCounterStore();
  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

## Persist Middleware

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsStore {
  theme: "light" | "dark";
  language: string;
  setTheme: (theme: "light" | "dark") => void;
  setLanguage: (language: string) => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: "light",
      language: "en",
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: "settings-storage",  // localStorage key
    }
  )
);
```

## Selectors

```typescript
import { useShallow } from "zustand/shallow";

// Select specific fields to prevent unnecessary re-renders
function UserName() {
  const name = useUserStore((state) => state.name);
  return <span>{name}</span>;
}

// For multiple fields, use useShallow
function UserInfo() {
  const { name, email } = useUserStore(
    useShallow((state) => ({ name: state.name, email: state.email }))
  );
  return <div>{name} - {email}</div>;
}

// AVOID: Selecting entire store (causes re-render on any change)
const store = useUserStore();  // Re-renders on ANY state change
```

## Async Actions

```typescript
interface UserStore {
  user: User | null;
  loading: boolean;
  error: string | null;
  fetchUser: (id: string) => Promise<void>;
}

const useUserStore = create<UserStore>((set) => ({
  user: null,
  loading: false,
  error: null,

  fetchUser: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`/api/users/${id}`);
      const user = await response.json();
      set({ user, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
}));
```