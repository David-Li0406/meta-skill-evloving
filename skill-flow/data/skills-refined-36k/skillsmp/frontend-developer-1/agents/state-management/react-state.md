---
name: React State Expert
description: Expert en gestion d'état React - useState, Context, Redux, Zustand
workflows:
  - id: state-setup
    template: wf-creation
    phase: Production
    name: Setup gestion d'état
    duration: 0.5-1 jour
  - id: state-refactor
    template: wf-refonte
    phase: Migration
    name: Refactoring state management
    duration: 1-3 jours
---

# Agent React State

## Responsabilité

Maîtriser les solutions de gestion d'état pour React.

## Tu NE fais PAS

- ❌ Implémenter les hooks React généraux (useEffect, useRef, custom hooks) → skill `react-expert`
- ❌ Gérer le server state (React Query, SWR) → `server-state.md`
- ❌ Tester le state et les reducers → `testing/`
- ❌ Gérer le state backend (sessions, database) → skill `backend-developer`

## État Local

### useState pour valeurs simples

```tsx
const [count, setCount] = useState(0);
const [name, setName] = useState('');
const [isOpen, setIsOpen] = useState(false);

// Mise à jour basée sur état précédent
setCount((prev) => prev + 1);

// Lazy initialization
const [data, setData] = useState(() => computeExpensiveValue());
```

### useReducer pour état complexe

```tsx
interface State {
  items: Item[];
  isLoading: boolean;
  error: Error | null;
  filter: string;
}

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Item[] }
  | { type: 'FETCH_ERROR'; payload: Error }
  | { type: 'SET_FILTER'; payload: string }
  | { type: 'ADD_ITEM'; payload: Item }
  | { type: 'REMOVE_ITEM'; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, items: action.payload };
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'SET_FILTER':
      return { ...state, filter: action.payload };
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter((i) => i.id !== action.payload),
      };
    default:
      return state;
  }
}

const initialState: State = {
  items: [],
  isLoading: false,
  error: null,
  filter: '',
};

function ItemList() {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    dispatch({ type: 'FETCH_START' });
    fetchItems()
      .then((items) => dispatch({ type: 'FETCH_SUCCESS', payload: items }))
      .catch((error) => dispatch({ type: 'FETCH_ERROR', payload: error }));
  }, []);

  return (/* ... */);
}
```

## Context API

### Pattern recommandé

```tsx
// contexts/AuthContext.tsx
interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Vérifier la session au montage
    checkSession()
      .then(setUser)
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (email: string, password: string) => {
    const user = await authAPI.login(email, password);
    setUser(user);
  };

  const logout = async () => {
    await authAPI.logout();
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
    }),
    [user, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Optimiser les re-renders

```tsx
// Séparer les contextes par fréquence de mise à jour
const UserContext = createContext<User | null>(null);
const UserActionsContext = createContext<UserActions | null>(null);

function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Actions stables (ne changent pas)
  const actions = useMemo(
    () => ({
      updateName: (name: string) => setUser((u) => u ? { ...u, name } : null),
      clear: () => setUser(null),
    }),
    []
  );

  return (
    <UserActionsContext.Provider value={actions}>
      <UserContext.Provider value={user}>{children}</UserContext.Provider>
    </UserActionsContext.Provider>
  );
}

// Composants qui n'ont besoin que des actions ne re-render pas
// quand user change
function UserActions() {
  const { updateName } = useContext(UserActionsContext)!;
  return <button onClick={() => updateName('New')}>Update</button>;
}
```

## Zustand

### Installation

```bash
npm install zustand
```

### Store de base

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

// Usage
function Counter() {
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);

  return (
    <button onClick={increment}>
      Count: {count}
    </button>
  );
}
```

### Store complexe avec middleware

```tsx
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

interface TodoStore {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  removeTodo: (id: string) => void;
  setFilter: (filter: TodoStore['filter']) => void;
}

const useTodoStore = create<TodoStore>()(
  devtools(
    persist(
      immer((set) => ({
        todos: [],
        filter: 'all',

        addTodo: (text) =>
          set((state) => {
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
            state.todos = state.todos.filter((t) => t.id !== id);
          }),

        setFilter: (filter) => set({ filter }),
      })),
      { name: 'todo-storage' }
    ),
    { name: 'TodoStore' }
  )
);

// Sélecteurs dérivés
const useFilteredTodos = () =>
  useTodoStore((state) => {
    switch (state.filter) {
      case 'active':
        return state.todos.filter((t) => !t.completed);
      case 'completed':
        return state.todos.filter((t) => t.completed);
      default:
        return state.todos;
    }
  });
```

### Slices pattern

```tsx
// stores/authSlice.ts
interface AuthSlice {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

const createAuthSlice: StateCreator<AuthSlice> = (set) => ({
  user: null,
  isAuthenticated: false,
  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
});

// stores/uiSlice.ts
interface UISlice {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  toggleTheme: () => void;
  toggleSidebar: () => void;
}

const createUISlice: StateCreator<UISlice> = (set) => ({
  theme: 'light',
  sidebarOpen: true,
  toggleTheme: () =>
    set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
});

// stores/index.ts
type StoreState = AuthSlice & UISlice;

const useStore = create<StoreState>()((...a) => ({
  ...createAuthSlice(...a),
  ...createUISlice(...a),
}));
```

## Redux Toolkit

### Configuration

```tsx
// store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';
import todosReducer from './todosSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    todos: todosReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// hooks/store.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Slice avec createSlice

```tsx
// store/todosSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

interface TodosState {
  items: Todo[];
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: TodosState = {
  items: [],
  status: 'idle',
  error: null,
};

// Async thunk
export const fetchTodos = createAsyncThunk('todos/fetchTodos', async () => {
  const response = await fetch('/api/todos');
  return response.json() as Promise<Todo[]>;
});

const todosSlice = createSlice({
  name: 'todos',
  initialState,
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      state.items.push({
        id: crypto.randomUUID(),
        text: action.payload,
        completed: false,
      });
    },
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.items.find((t) => t.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed;
      }
    },
    removeTodo: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter((t) => t.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message ?? 'Unknown error';
      });
  },
});

export const { addTodo, toggleTodo, removeTodo } = todosSlice.actions;
export default todosSlice.reducer;

// Sélecteurs
export const selectAllTodos = (state: RootState) => state.todos.items;
export const selectTodosStatus = (state: RootState) => state.todos.status;
export const selectActiveTodos = (state: RootState) =>
  state.todos.items.filter((t) => !t.completed);
```

## Mots-clés de routage

`state`, `useState`, `useReducer`, `Context`, `Redux`, `Redux Toolkit`, `Zustand`, `Jotai`, `Recoil`, `store`, `dispatch`, `reducer`, `slice`

## Livrables

| Livrable | Description |
|----------|-------------|
| Store de state global | Configuration Zustand ou Redux avec slices et selectors |
| Context providers | Providers React Context pour state partagé localement |
| Hooks de state management | Custom hooks pour accès au state et actions |
