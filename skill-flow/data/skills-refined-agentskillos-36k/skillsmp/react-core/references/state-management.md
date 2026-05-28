# State Management

State management is one of the most critical aspects of building React applications. Choosing the right approach for each type of state directly impacts performance, maintainability, and developer experience.

## Table of Contents

- [State Categories](#state-categories)
- [Component State](#component-state)
- [Application State](#application-state)
- [Server Cache State](#server-cache-state)
- [Form State](#form-state)
- [URL State](#url-state)
- [Decision Framework](#decision-framework)
- [Best Practices](#best-practices)

## State Categories

React applications manage five distinct categories of state, each requiring different approaches:

| State Type | Scope | Tools | Example |
|------------|-------|-------|---------|
| **Component State** | Local to component | useState, useReducer | Form inputs, toggles, modals |
| **Application State** | Global, client-side | Context, Zustand, Jotai | Theme, user preferences, UI state |
| **Server Cache** | Remote data cache | React Query, SWR | API responses, database queries |
| **Form State** | Form-specific | React Hook Form, Formik | Form values, validation, errors |
| **URL State** | Browser location | React Router, Tanstack Router | Route params, query strings |

**Golden Rule**: Use the most specific state type for your use case. Don't use global state for local concerns.

## Component State

Component state is data that only affects a single component and its children.

### When to Use

- UI state local to component (expanded/collapsed, active tab)
- Transient state that doesn't need to persist
- State not shared with sibling components
- Simple state without complex update logic

### `useState` - Simple State

For straightforward state values:

```tsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**Best practices:**
- Initialize with appropriate default values
- Use functional updates when new state depends on previous state
- Split complex state into multiple `useState` calls

```tsx
// ❌ Bad - depending on stale closure
setCount(count + 1);

// ✅ Good - functional update
setCount(prev => prev + 1);

// ❌ Bad - one large state object
const [state, setState] = useState({ name: '', email: '', age: 0, ... });

// ✅ Good - split related state
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [age, setAge] = useState(0);
```

### `useReducer` - Complex State Logic

For state with complex update logic or multiple related values:

```tsx
type State = {
  status: 'idle' | 'loading' | 'success' | 'error';
  data: User | null;
  error: Error | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; payload: Error };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { status: 'loading', data: null, error: null };
    case 'FETCH_SUCCESS':
      return { status: 'success', data: action.payload, error: null };
    case 'FETCH_ERROR':
      return { status: 'error', data: null, error: action.payload };
    default:
      return state;
  }
}

function UserProfile({ userId }: { userId: string }) {
  const [state, dispatch] = useReducer(reducer, {
    status: 'idle',
    data: null,
    error: null,
  });

  useEffect(() => {
    dispatch({ type: 'FETCH_START' });
    fetchUser(userId)
      .then(user => dispatch({ type: 'FETCH_SUCCESS', payload: user }))
      .catch(error => dispatch({ type: 'FETCH_ERROR', payload: error }));
  }, [userId]);

  // Render based on state.status
}
```

**When to use `useReducer` over `useState`:**
- Multiple related state values that change together
- Complex state update logic
- Next state depends on previous state in non-trivial ways
- You want to separate state update logic from component

### State Colocation

Keep state as close as possible to where it's used:

```tsx
// ❌ Bad - state too high in tree
function App() {
  const [modalOpen, setModalOpen] = useState(false); // Only used deep in tree

  return (
    <Layout>
      <Content>
        <DeepNested>
          <Modal open={modalOpen} onClose={() => setModalOpen(false)} />
        </DeepNested>
      </Content>
    </Layout>
  );
}

// ✅ Good - state colocated with usage
function DeepNested() {
  const [modalOpen, setModalOpen] = useState(false);

  return <Modal open={modalOpen} onClose={() => setModalOpen(false)} />;
}
```

## Application State

Application state is global client-side state shared across multiple unrelated components.

### When to Use

- Theme preferences (light/dark mode)
- User authentication status
- Language/locale settings
- Global UI state (sidebar open/closed)
- Settings and preferences

### Context + Hooks Pattern

For simple global state without complex logic:

```tsx
// stores/themeStore.tsx
type Theme = 'light' | 'dark';

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
} | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <MyApp />
    </ThemeProvider>
  );
}

function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle Theme
    </button>
  );
}
```

**Context Pitfalls:**
- Every context value change re-renders all consumers
- Split context by update frequency to avoid unnecessary renders

```tsx
// ❌ Bad - all consumers re-render on any change
const AppContext = createContext({ user, theme, settings, ... });

// ✅ Good - separate contexts by update frequency
const UserContext = createContext(user); // Changes rarely
const ThemeContext = createContext(theme); // Changes occasionally
const SettingsContext = createContext(settings); // Changes frequently
```

### Zustand - Lightweight State Management

For more complex global state with better performance than Context:

```tsx
// stores/authStore.ts
import { create } from 'zustand';

type AuthState = {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: () => boolean;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,

  login: async (email, password) => {
    const { user, token } = await api.login(email, password);
    set({ user, token });
  },

  logout: () => {
    set({ user: null, token: null });
  },

  isAuthenticated: () => {
    return get().token !== null;
  },
}));

// Usage - components only re-render when selected state changes
function UserProfile() {
  const user = useAuthStore(state => state.user); // Only re-renders on user change
  return <div>{user?.name}</div>;
}

function LoginButton() {
  const login = useAuthStore(state => state.login); // Never re-renders
  return <button onClick={() => login('email', 'pass')}>Login</button>;
}
```

**Benefits of Zustand:**
- No Provider boilerplate
- Component re-renders only when selected state changes
- DevTools support
- Small bundle size (~1KB)

### Jotai - Atomic State Management

For fine-grained reactive state:

```tsx
// stores/atoms.ts
import { atom } from 'jotai';

export const userAtom = atom<User | null>(null);
export const themeAtom = atom<Theme>('light');

// Derived atom
export const isAuthenticatedAtom = atom(
  (get) => get(userAtom) !== null
);

// Usage
import { useAtom, useAtomValue, useSetAtom } from 'jotai';

function UserProfile() {
  const [user, setUser] = useAtom(userAtom);
  return <div>{user?.name}</div>;
}

function AuthStatus() {
  const isAuthenticated = useAtomValue(isAuthenticatedAtom); // Read-only
  return <div>{isAuthenticated ? 'Logged in' : 'Logged out'}</div>;
}
```

**When to choose:**
- **Context + Hooks**: Simple, infrequent global state
- **Zustand**: Most application state needs, great DX
- **Jotai**: Atomic state updates, derived state, complex dependencies
- **Redux**: Large apps with complex state logic (consider Zustand/Jotai first)

## Server Cache State

Server cache state is data fetched from APIs that needs caching, synchronization, and invalidation.

### Why Not Application State?

❌ **Don't** manage server data with `useState` or global state:

```tsx
// ❌ Bad - manual server state management
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  // Missing: caching, refetching, deduplication, stale data handling
}
```

### React Query (Tanstack Query)

The recommended approach for server state:

```tsx
// api/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(res => res.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => fetch(`/api/users/${id}`).then(res => res.json()),
    enabled: !!id, // Only fetch if id is provided
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UserInput) =>
      fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(data),
      }).then(res => res.json()),

    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}

// Usage
function UserList() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

function CreateUserForm() {
  const createUser = useCreateUser();

  const handleSubmit = (data: UserInput) => {
    createUser.mutate(data);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

**React Query handles:**
- ✅ Caching
- ✅ Background refetching
- ✅ Stale data revalidation
- ✅ Request deduplication
- ✅ Pagination and infinite scroll
- ✅ Optimistic updates
- ✅ Error handling and retries
- ✅ DevTools

### SWR Alternative

Similar to React Query, lighter weight:

```tsx
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(res => res.json());

function useUsers() {
  return useSWR('/api/users', fetcher);
}

function UserList() {
  const { data: users, error, isLoading } = useUsers();
  // Same pattern as React Query
}
```

**Choose React Query over SWR if:**
- You need more advanced features (mutations, infinite queries)
- You want better TypeScript support
- You prefer explicit cache invalidation control

## Form State

Form state includes values, validation, errors, touched fields, and submission status.

### React Hook Form

The recommended solution for forms:

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema validation
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof schema>;

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await api.signup(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email')}
        type="email"
        placeholder="Email"
      />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        {...register('password')}
        type="password"
        placeholder="Password"
      />
      {errors.password && <span>{errors.password.message}</span>}

      <input
        {...register('confirmPassword')}
        type="password"
        placeholder="Confirm Password"
      />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

**Benefits:**
- Minimal re-renders (uncontrolled inputs by default)
- Built-in validation with error handling
- Easy integration with Zod/Yup
- Async validation support
- Field arrays and dynamic forms
- Small bundle size

## URL State

URL state persists state in the URL for shareability and browser history.

### React Router

```tsx
import { useSearchParams, useParams } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const page = searchParams.get('page') || '1';
  const sortBy = searchParams.get('sortBy') || 'name';

  const updateFilters = (newFilters: Record<string, string>) => {
    setSearchParams(prev => {
      const params = new URLSearchParams(prev);
      Object.entries(newFilters).forEach(([key, value]) => {
        params.set(key, value);
      });
      return params;
    });
  };

  return (
    <div>
      <select
        value={sortBy}
        onChange={e => updateFilters({ sortBy: e.target.value })}
      >
        <option value="name">Name</option>
        <option value="price">Price</option>
      </select>
      {/* URL updates to ?page=1&sortBy=price */}
    </div>
  );
}

function ProductDetail() {
  const { productId } = useParams(); // From /products/:productId

  const { data } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => fetchProduct(productId),
  });
}
```

**When to use URL state:**
- Filters and sorting
- Pagination
- Search queries
- Selected tabs
- Any state that should be shareable via URL

## Decision Framework

```
┌─ Is this server data? ───────────────────────┐
│  YES → Use React Query or SWR                │
└───────────────────────────────────────────────┘
                    ↓ NO
┌─ Is this form data? ─────────────────────────┐
│  YES → Use React Hook Form                   │
└───────────────────────────────────────────────┘
                    ↓ NO
┌─ Should it be in the URL? ───────────────────┐
│  YES → Use useSearchParams / useParams       │
└───────────────────────────────────────────────┘
                    ↓ NO
┌─ Is it shared across unrelated components? ──┐
│  YES → Use Zustand, Jotai, or Context        │
└───────────────────────────────────────────────┘
                    ↓ NO
┌─ Use component state (useState/useReducer) ──┐
└───────────────────────────────────────────────┘
```

## Best Practices

### 1. Keep State Local

Only lift state when necessary:

```tsx
// ❌ Bad - lifted state unnecessarily
function App() {
  const [modalOpen, setModalOpen] = useState(false);
  return <DeepComponent modalOpen={modalOpen} setModalOpen={setModalOpen} />;
}

// ✅ Good - state where it's used
function DeepComponent() {
  const [modalOpen, setModalOpen] = useState(false);
  return <Modal open={modalOpen} onClose={() => setModalOpen(false)} />;
}
```

### 2. Use Selectors to Prevent Re-renders

```tsx
// ❌ Bad - component re-renders on any store change
const { user, theme, settings } = useStore();

// ✅ Good - only re-renders when user changes
const user = useStore(state => state.user);
```

### 3. Normalize State Shape

```tsx
// ❌ Bad - nested arrays make updates difficult
const [users, setUsers] = useState([
  { id: 1, name: 'Alice', posts: [...] },
  { id: 2, name: 'Bob', posts: [...] },
]);

// ✅ Good - normalized state
const [users, setUsers] = useState({
  '1': { id: 1, name: 'Alice' },
  '2': { id: 2, name: 'Bob' },
});
const [posts, setPosts] = useState({
  '1': { id: 1, userId: 1, content: '...' },
  '2': { id: 2, userId: 1, content: '...' },
});
```

### 4. Avoid Prop Drilling

```tsx
// ❌ Bad - prop drilling through many layers
<App>
  <Layout theme={theme}>
    <Content theme={theme}>
      <Component theme={theme} />
    </Content>
  </Layout>
</App>

// ✅ Good - context or state management
<ThemeProvider>
  <App>
    <Layout>
      <Content>
        <Component /> {/* Accesses theme via useTheme() */}
      </Content>
    </Layout>
  </App>
</ThemeProvider>
```

### 5. Separate Server and Client State

Never mix server state management with application state. Use React Query/SWR for all server data.

### 6. Use Derived State

Don't store computed values:

```tsx
// ❌ Bad - storing derived state
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState(''); // Derived!

// ✅ Good - compute on render
const fullName = `${firstName} ${lastName}`;

// Or with useMemo if expensive
const fullName = useMemo(
  () => expensiveComputation(firstName, lastName),
  [firstName, lastName]
);
```

By following these patterns and choosing the right tool for each state category, you'll build React applications that are performant, maintainable, and easy to reason about.
