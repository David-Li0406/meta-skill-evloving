# React Hooks - API Reference

**Version**: React 18.x with TypeScript 5.7.3

## Official Documentation

- **React Hooks**: https://react.dev/reference/react
- **Hooks Rules**: https://react.dev/reference/rules/rules-of-hooks
- **Custom Hooks**: https://react.dev/learn/reusing-logic-with-custom-hooks

## useState

Manage component state.

```typescript
const [state, setState] = useState<T>(initialState);
```

**Parameters**:
- `initialState: T | (() => T)` - Initial state value or lazy initializer function

**Returns**: `[T, Dispatch<SetStateAction<T>>]`
- `state: T` - Current state value
- `setState: (value: T | ((prev: T) => T)) => void` - State updater function

### Basic Usage

```typescript
// Simple state
const [count, setCount] = useState<number>(0);
setCount(5); // Set to value
setCount((prev) => prev + 1); // Function updater

// Boolean state
const [isOpen, setIsOpen] = useState(false);
setIsOpen(!isOpen);
setIsOpen((prev) => !prev);

// String state
const [name, setName] = useState<string>('');
setName('John');

// Object state
interface User {
  name: string;
  email: string;
}

const [user, setUser] = useState<User>({
  name: '',
  email: '',
});

setUser({ name: 'John', email: 'john@example.com' });
setUser((prev) => ({ ...prev, name: 'Jane' }));
```

### Lazy Initial State

```typescript
// Expensive computation - only runs once
const [data, setData] = useState<Data>(() => {
  return expensiveComputation();
});

// Reading from localStorage - only runs once
const [theme, setTheme] = useState<string>(() => {
  const saved = localStorage.getItem('theme');
  return saved || 'light';
});
```

### TypeScript Patterns

```typescript
// With explicit type
const [count, setCount] = useState<number>(0);

// With type inference
const [count, setCount] = useState(0); // Inferred as number

// With union type
const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

// With nullable type
const [user, setUser] = useState<User | null>(null);

// With array type
const [items, setItems] = useState<string[]>([]);
```

## useEffect

Perform side effects in function components.

```typescript
useEffect(() => {
  // Effect code
  return () => {
    // Cleanup code (optional)
  };
}, [dependencies]);
```

**Parameters**:
- `effect: () => void | (() => void)` - Effect function, optionally returns cleanup
- `dependencies?: DependencyList` - Array of dependencies that trigger re-run

**Returns**: `void`

### Basic Usage

```typescript
// Run once on mount
useEffect(() => {
  console.log('Component mounted');

  return () => {
    console.log('Component unmounted');
  };
}, []); // Empty array

// Run on every render
useEffect(() => {
  console.log('Component rendered');
}); // No dependency array

// Run when dependencies change
useEffect(() => {
  console.log('Count changed:', count);
}, [count]); // Re-run when count changes
```

### Data Fetching

```typescript
useEffect(() => {
  let isMounted = true;
  const controller = new AbortController();

  async function fetchData() {
    try {
      const response = await fetch(url, {
        signal: controller.signal,
      });
      const data = await response.json();

      if (isMounted) {
        setData(data);
      }
    } catch (error) {
      if (isMounted && error.name !== 'AbortError') {
        setError(error);
      }
    }
  }

  fetchData();

  return () => {
    isMounted = false;
    controller.abort();
  };
}, [url]);
```

### Event Listeners

```typescript
useEffect(() => {
  function handleResize() {
    setWindowWidth(window.innerWidth);
  }

  window.addEventListener('resize', handleResize);

  // Cleanup: remove listener
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []); // Empty array - run once
```

### Subscriptions

```typescript
useEffect(() => {
  const subscription = observable.subscribe((value) => {
    setData(value);
  });

  // Cleanup: unsubscribe
  return () => {
    subscription.unsubscribe();
  };
}, [observable]);
```

## useMemo

Memoize expensive computations.

```typescript
const memoizedValue = useMemo<T>(() => {
  return expensiveComputation(a, b);
}, [a, b]);
```

**Parameters**:
- `factory: () => T` - Function that returns memoized value
- `dependencies: DependencyList` - Array of dependencies

**Returns**: `T` - Memoized value

### When to Use

```typescript
// ✅ Use for expensive operations
const sortedItems = useMemo(() => {
  return items
    .filter(item => item.active)
    .sort((a, b) => b.priority - a.priority);
}, [items]);

// ✅ Use for referential equality
const options = useMemo(() => {
  return {
    width: 100,
    height: 200,
  };
}, []); // Stable reference

// ❌ Don't use for simple operations
const doubled = useMemo(() => count * 2, [count]); // Too simple!
const doubled = count * 2; // Just do this instead
```

### Complex Computations

```typescript
const filteredAndSorted = useMemo(() => {
  console.log('Computing...');

  return data
    .filter(item => item.category === selectedCategory)
    .filter(item => item.name.includes(searchQuery))
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'price') return a.price - b.price;
      return 0;
    });
}, [data, selectedCategory, searchQuery, sortBy]);
```

## useCallback

Memoize callback functions.

```typescript
const memoizedCallback = useCallback<T>(
  (arg) => {
    // Callback code
  },
  [dependencies]
);
```

**Parameters**:
- `callback: T` - Function to memoize
- `dependencies: DependencyList` - Array of dependencies

**Returns**: `T` - Memoized function

### Basic Usage

```typescript
const handleClick = useCallback(() => {
  console.log('Clicked!');
}, []); // Stable reference

const handleSubmit = useCallback(() => {
  submitForm(formData);
}, [formData]); // New function when formData changes

// With parameters
const handleItemClick = useCallback((id: string) => {
  selectItem(id);
}, []); // Stable reference
```

### Preventing Re-renders

```typescript
function ParentComponent() {
  const [count, setCount] = useState(0);

  // Without useCallback - new function every render
  const handleClick = () => {
    console.log('Clicked');
  };

  // With useCallback - stable reference
  const handleClickMemoized = useCallback(() => {
    console.log('Clicked');
  }, []);

  return (
    <>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>

      {/* Child re-renders on every parent render */}
      <ExpensiveChild onClick={handleClick} />

      {/* Child only re-renders when function changes */}
      <ExpensiveChild onClick={handleClickMemoized} />
    </>
  );
}
```

### TypeScript Patterns

```typescript
// With explicit type
const handleClick = useCallback<() => void>(() => {
  console.log('Clicked');
}, []);

// With event type
const handleChange = useCallback<React.ChangeEventHandler<HTMLInputElement>>(
  (e) => {
    setValue(e.target.value);
  },
  []
);

// With parameters
const handleItemClick = useCallback<(id: string) => void>(
  (id) => {
    selectItem(id);
  },
  []
);
```

## useRef

Create mutable ref object or DOM element reference.

```typescript
const refContainer = useRef<T>(initialValue);
```

**Parameters**:
- `initialValue: T` - Initial ref value

**Returns**: `{ current: T }` - Mutable ref object

### DOM Element Reference

```typescript
function InputComponent() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </>
  );
}
```

### Mutable Value

```typescript
function Timer() {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startTimer = () => {
    intervalRef.current = setInterval(() => {
      console.log('Tick');
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </>
  );
}
```

### Previous Value

```typescript
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

## useContext

Access React context.

```typescript
const value = useContext<T>(Context);
```

**Parameters**:
- `Context: React.Context<T>` - Context object created by `React.createContext`

**Returns**: `T` - Current context value

### Basic Usage

```typescript
// Create context
interface ThemeContext {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = React.createContext<ThemeContext | undefined>(undefined);

// Provider
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Consumer with useContext
function ThemedButton() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }

  const { theme, toggleTheme } = context;

  return (
    <button onClick={toggleTheme} className={`btn-${theme}`}>
      Toggle Theme
    </button>
  );
}
```

## Custom Hooks

Create reusable logic with custom hooks.

### Custom Hook Template

```typescript
export function useCustomHook<T>(param: string): {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/${param}`);
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [param]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
```

### useLocalStorage

```typescript
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  // State to store value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  // Return wrapped version of setState that persists
  const setValue = (value: T | ((prev: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Usage
function App() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle Theme (Current: {theme})
    </button>
  );
}
```

### useWindowSize

```typescript
interface WindowSize {
  width: number;
  height: number;
}

export function useWindowSize(): WindowSize {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}
```

### useDebounce

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timeoutId);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchComponent() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 500);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

## Web-Specific Hooks

### useRouter (Next.js)

```typescript
import { useRouter } from 'next/router';

function ProductPage() {
  const router = useRouter();

  // Query params
  const { id, category } = router.query;

  // Navigate
  router.push('/products');
  router.push({ pathname: '/products', query: { category: 'electronics' } });
  router.replace('/products'); // Replace history
  router.back(); // Go back

  // Route events
  useEffect(() => {
    const handleRouteChange = (url: string) => {
      console.log('App is changing to:', url);
    };

    router.events.on('routeChangeStart', handleRouteChange);

    return () => {
      router.events.off('routeChangeStart', handleRouteChange);
    };
  }, [router]);

  return <div>Product ID: {id}</div>;
}
```

## Hooks Rules

1. **Only call hooks at the top level** - Don't call hooks inside loops, conditions, or nested functions

```typescript
// ❌ Bad
if (condition) {
  const [state, setState] = useState(0); // Breaks rules!
}

// ✅ Good
const [state, setState] = useState(0);
if (condition) {
  setState(1);
}
```

2. **Only call hooks from React functions** - Call hooks from function components or custom hooks

```typescript
// ❌ Bad
function regularFunction() {
  const [state, setState] = useState(0); // Not allowed!
}

// ✅ Good
function MyComponent() {
  const [state, setState] = useState(0); // Allowed
}

function useMyHook() {
  const [state, setState] = useState(0); // Allowed
}
```

3. **Custom hooks must start with "use"** - Enables linting and follows convention

```typescript
// ❌ Bad
function fetchData() {
  const [data, setData] = useState(null); // Missing "use" prefix
}

// ✅ Good
function useFetchData() {
  const [data, setData] = useState(null); // Correct
}
```

## TypeScript Patterns

### Typed Custom Hooks

```typescript
// Return object
export function useData<T>(): {
  data: T | null;
  loading: boolean;
} {
  // ...
  return { data, loading };
}

// Return tuple
export function useToggle(
  initialValue: boolean
): [boolean, () => void] {
  // ...
  return [value, toggle];
}

// Generic return type
export function useFetch<T>(url: string): {
  data: T | null;
  loading: boolean;
  error: Error | null;
} {
  // ...
  return { data, loading, error };
}
```

### Typed Refs

```typescript
// DOM element
const inputRef = useRef<HTMLInputElement>(null);
const divRef = useRef<HTMLDivElement>(null);
const buttonRef = useRef<HTMLButtonElement>(null);

// Value
const countRef = useRef<number>(0);
const intervalRef = useRef<NodeJS.Timeout | null>(null);
```

## Key Considerations

- Follow hooks rules (top-level, React functions only)
- Include all dependencies in useEffect/useMemo/useCallback
- Clean up effects (event listeners, subscriptions, timers)
- Use function updaters in setState when new state depends on old
- Only use useMemo/useCallback for expensive operations or referential equality
- Custom hooks must start with "use"
- Type custom hooks with explicit return types
- Use lazy initialization for expensive initial state
- Ref changes don't trigger re-renders
