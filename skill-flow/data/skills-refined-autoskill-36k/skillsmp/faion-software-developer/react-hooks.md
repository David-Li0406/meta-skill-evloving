---
id: react-hooks
name: "React Hooks Best Practices"
domain: DEV
skill: faion-software-developer
category: "development"
---

# React Hooks Best Practices

## Overview

React Hooks enable functional components to use state, effects, and other React features. This methodology covers hook patterns, custom hooks, performance optimization, and common pitfalls to avoid.

## When to Use

- All React functional components
- Extracting reusable logic
- Managing component state
- Side effects and data fetching
- Performance optimization

## Key Principles

1. **Rules of Hooks** - Only call at top level, only in React functions
2. **Complete dependencies** - Include all values used in effects
3. **Custom hooks for reuse** - Extract common patterns
4. **Memoization wisely** - Don't over-optimize
5. **Cleanup effects** - Prevent memory leaks

## Best Practices

### useState Patterns

```tsx
// Basic state
const [count, setCount] = useState(0);

// Object state - update immutably
const [user, setUser] = useState<User>({ name: '', email: '' });

const updateName = (name: string) => {
  setUser(prev => ({ ...prev, name }));
};

// Lazy initialization - for expensive computations
const [data, setData] = useState(() => {
  return computeExpensiveInitialValue();
});

// State with type
const [items, setItems] = useState<Item[]>([]);

// Multiple related states - consider useReducer
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);
const [data, setData] = useState<Data | null>(null);
```

### useEffect Best Practices

```tsx
// Basic effect with cleanup
useEffect(() => {
  const subscription = api.subscribe(handleUpdate);

  return () => {
    subscription.unsubscribe();  // Cleanup
  };
}, [handleUpdate]);

// Data fetching with abort
useEffect(() => {
  const controller = new AbortController();

  async function fetchData() {
    try {
      const response = await fetch(url, { signal: controller.signal });
      const data = await response.json();
      setData(data);
    } catch (error) {
      if (error instanceof Error && error.name !== 'AbortError') {
        setError(error);
      }
    }
  }

  fetchData();

  return () => {
    controller.abort();
  };
}, [url]);

// Effect with ref - no dependency needed
const callbackRef = useRef(callback);
callbackRef.current = callback;

useEffect(() => {
  const handler = () => callbackRef.current();
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);  // Empty deps OK - uses ref
```

### useCallback and useMemo

```tsx
// useCallback - memoize functions passed to children
const handleClick = useCallback((id: string) => {
  setSelectedId(id);
}, []);  // No dependencies - stable reference

// useCallback with dependencies
const handleSubmit = useCallback(async (data: FormData) => {
  await api.submit(userId, data);
  onSuccess();
}, [userId, onSuccess]);

// useMemo - memoize expensive computations
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// useMemo for object/array references
const options = useMemo(() => ({
  endpoint: '/api',
  timeout: 5000,
}), []);

// Don't overuse - measure first
// BAD - unnecessary memoization
const doubled = useMemo(() => count * 2, [count]);

// GOOD - just calculate
const doubled = count * 2;
```

### useRef Patterns

```tsx
// DOM reference
const inputRef = useRef<HTMLInputElement>(null);

const focusInput = () => {
  inputRef.current?.focus();
};

return <input ref={inputRef} />;

// Mutable value that doesn't trigger re-render
const renderCount = useRef(0);
renderCount.current += 1;

// Previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Stable callback reference
function useEvent<T extends (...args: any[]) => any>(callback: T): T {
  const ref = useRef(callback);
  ref.current = callback;

  return useCallback(
    ((...args) => ref.current(...args)) as T,
    []
  );
}
```

### Custom Hooks

```tsx
// Data fetching hook
interface UseFetchResult<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, isLoading, error, refetch: fetchData };
}

// Usage
const { data: user, isLoading, error } = useFetch<User>('/api/user/1');
```

### useReducer for Complex State

```tsx
type State = {
  items: Item[];
  isLoading: boolean;
  error: Error | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Item[] }
  | { type: 'FETCH_ERROR'; payload: Error }
  | { type: 'ADD_ITEM'; payload: Item }
  | { type: 'REMOVE_ITEM'; payload: string };

const initialState: State = {
  items: [],
  isLoading: false,
  error: null,
};

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, items: action.payload };
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload),
      };
    default:
      return state;
  }
}

function ItemList() {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    dispatch({ type: 'FETCH_START' });

    fetchItems()
      .then(items => dispatch({ type: 'FETCH_SUCCESS', payload: items }))
      .catch(error => dispatch({ type: 'FETCH_ERROR', payload: error }));
  }, []);

  // ...
}
```

### Context with Hooks

```tsx
interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (credentials: Credentials) => {
    const user = await authApi.login(credentials);
    setUser(user);
  }, []);

  const logout = useCallback(() => {
    authApi.logout();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: user !== null,
      login,
      logout,
    }),
    [user, login, logout]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Debounce and Throttle Hooks

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      performSearch(debouncedQuery);
    }
  }, [debouncedQuery]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
    />
  );
}
```

## Anti-patterns

### Avoid: Hooks in Conditions/Loops

```tsx
// BAD - hooks must be called unconditionally
function Component({ enabled }: { enabled: boolean }) {
  if (enabled) {
    const [value, setValue] = useState('');  // Error!
  }
}

// GOOD - call hook unconditionally
function Component({ enabled }: { enabled: boolean }) {
  const [value, setValue] = useState('');

  if (!enabled) {
    return null;
  }

  return <input value={value} onChange={e => setValue(e.target.value)} />;
}
```

### Avoid: Missing Effect Dependencies

```tsx
// BAD - stale closure
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1);  // count is stale!
  }, 1000);
  return () => clearInterval(timer);
}, []);  // Missing count dependency

// GOOD - functional update
useEffect(() => {
  const timer = setInterval(() => {
    setCount(prev => prev + 1);  // Uses previous value
  }, 1000);
  return () => clearInterval(timer);
}, []);
```

### Avoid: Object Dependencies

```tsx
// BAD - new object every render
useEffect(() => {
  fetchData(options);
}, [options]);  // { page: 1 } !== { page: 1 }

// GOOD - primitive dependencies
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);

// Or memoize the object
const options = useMemo(() => ({ page, limit }), [page, limit]);
```

## References

- [React Hooks Documentation](https://react.dev/reference/react)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [useHooks](https://usehooks.com/)
