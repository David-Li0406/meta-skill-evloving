---
name: zustand
description: Zustand lightweight state management implementation
workflows:
  - id: zustand-setup
    template: wf-creation
    phase: Production
    name: Setup Zustand store
    duration: 0.5 jour
---

# Zustand - State Management Léger

## Rôle

Implémentation de stores Zustand pour la gestion d'état global dans React.

## Tu NE fais PAS

- ❌ Gérer le server state (préférer React Query/SWR) → `../data/`
- ❌ Implémenter l'UI des composants → `../components/`
- ❌ Implémenter le backend → `backend-developer`
- ❌ Définir la stratégie de tests → `testing-process`

## Installation

```bash
npm install zustand
```

## Store de Base

### Création

```tsx
import { create } from 'zustand';

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
```

### Usage

```tsx
function Counter() {
  // Sélection complète
  const { count, increment, decrement } = useCounterStore();

  // Ou sélection partielle (optimisé)
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

## Store Typé Complet

```tsx
import { create } from 'zustand';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

type AuthStore = AuthState & AuthActions;

const useAuthStore = create<AuthStore>((set, get) => ({
  // State
  user: null,
  isLoading: false,
  error: null,

  // Actions
  login: async (credentials) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
      const user = await response.json();
      set({ user, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Login failed',
        isLoading: false,
      });
    }
  },

  logout: () => {
    set({ user: null });
    // Accès à l'état actuel avec get()
    console.log('Logged out user:', get().user);
  },

  clearError: () => set({ error: null }),
}));
```

## Sélecteurs Optimisés

### Shallow comparison

```tsx
import { useShallow } from 'zustand/react/shallow';

// ❌ Re-render quand n'importe quelle partie du store change
const { user, settings } = useStore();

// ✅ Re-render seulement quand user OU settings change
const { user, settings } = useStore(
  useShallow((state) => ({
    user: state.user,
    settings: state.settings,
  }))
);
```

### Sélecteurs dérivés

```tsx
// Créer des sélecteurs réutilisables
const selectUser = (state: AuthStore) => state.user;
const selectIsLoggedIn = (state: AuthStore) => state.user !== null;
const selectUserName = (state: AuthStore) => state.user?.name ?? 'Guest';

// Usage
function Header() {
  const isLoggedIn = useAuthStore(selectIsLoggedIn);
  const userName = useAuthStore(selectUserName);

  return <div>Hello, {userName}</div>;
}
```

## Middleware

### Persist

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsStore {
  theme: 'light' | 'dark';
  language: string;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: string) => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => localStorage),
      // Sélectionner ce qui est persisté
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    }
  )
);
```

### Immer

```tsx
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface TodoStore {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  removeTodo: (id: string) => void;
}

const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],

    addTodo: (text) =>
      set((state) => {
        // Mutation directe grâce à Immer
        state.todos.push({
          id: crypto.randomUUID(),
          text,
          completed: false,
        });
      }),

    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        if (todo) {
          todo.completed = !todo.completed;
        }
      }),

    removeTodo: (id) =>
      set((state) => {
        const index = state.todos.findIndex((t) => t.id === id);
        if (index !== -1) {
          state.todos.splice(index, 1);
        }
      }),
  }))
);
```

### DevTools

```tsx
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const useStore = create<Store>()(
  devtools(
    (set) => ({
      // ...state and actions
    }),
    {
      name: 'MyStore', // Nom dans Redux DevTools
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

### Combiner les middlewares

```tsx
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

const useStore = create<Store>()(
  devtools(
    persist(
      immer((set) => ({
        // ...
      })),
      { name: 'store' }
    ),
    { name: 'Store' }
  )
);
```

## Slices Pattern

### Séparer le store en tranches

```tsx
// userSlice.ts
interface UserSlice {
  user: User | null;
  setUser: (user: User | null) => void;
}

const createUserSlice = (set: SetState<Store>): UserSlice => ({
  user: null,
  setUser: (user) => set({ user }),
});

// cartSlice.ts
interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
}

const createCartSlice = (set: SetState<Store>): CartSlice => ({
  items: [],
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
});

// store.ts
type Store = UserSlice & CartSlice;

const useStore = create<Store>()((...args) => ({
  ...createUserSlice(...args),
  ...createCartSlice(...args),
}));
```

## Actions Asynchrones

```tsx
interface ProductStore {
  products: Product[];
  isLoading: boolean;
  error: string | null;
  fetchProducts: () => Promise<void>;
  createProduct: (data: CreateProductInput) => Promise<Product>;
}

const useProductStore = create<ProductStore>((set, get) => ({
  products: [],
  isLoading: false,
  error: null,

  fetchProducts: async () => {
    set({ isLoading: true, error: null });
    try {
      const products = await api.getProducts();
      set({ products, isLoading: false });
    } catch (error) {
      set({
        error: 'Failed to fetch products',
        isLoading: false,
      });
    }
  },

  createProduct: async (data) => {
    const product = await api.createProduct(data);
    set((state) => ({
      products: [...state.products, product],
    }));
    return product;
  },
}));
```

## Accès Hors React

```tsx
// Lire l'état
const user = useAuthStore.getState().user;

// Mettre à jour l'état
useAuthStore.setState({ user: newUser });

// Souscrire aux changements
const unsubscribe = useAuthStore.subscribe(
  (state) => console.log('State changed:', state)
);

// Avec sélecteur
const unsubscribe = useAuthStore.subscribe(
  (state) => state.user,
  (user) => console.log('User changed:', user),
  { fireImmediately: true }
);
```

## Bonnes Pratiques

1. **Sélecteurs atomiques** - Un selector = une valeur
2. **useShallow** pour objets/arrays
3. **Immer pour état imbriqué** - Évite les spreads profonds
4. **DevTools en dev** - Debugging facilité
5. **Slices pour gros stores** - Séparation des préoccupations

## Voir aussi

- `context.md` - Alternative native React
- `redux-toolkit.md` - Pour cas très complexes
- `../data/react-query.md` - Pour le server state

## Livrables

| Livrable | Description |
|----------|-------------|
| Store Zustand | Configuration store avec types et actions |
| Types d'état | Interfaces pour state, actions et slices |
| Sélecteurs | Fonctions sélectrices optimisées avec useShallow |
