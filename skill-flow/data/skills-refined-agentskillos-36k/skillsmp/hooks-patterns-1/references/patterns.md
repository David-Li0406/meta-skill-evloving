# React Hooks Implementation Patterns

Implementation patterns and anti-patterns for React hooks with TypeScript.

## Pattern: Custom Hook Naming with "use" Prefix

Always prefix custom hooks with "use".

✅ **Good:**
```typescript
export const useReviews = (numberOfReviews: number): Review[] => {
  const { translateRaw } = useT9n(APPLANGA_GROUP);

  const reviews: Review[] = [];
  for (let i = 1; i <= numberOfReviews; i++) {
    const text = translateRaw(`review-${i}.text`);
    if (text) reviews.push({ text });
  }

  return reviews;
};

export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  // ...
  return { data };
}
```

❌ **Bad:**
```typescript
// Missing "use" prefix
export const getReviews = (numberOfReviews: number) => {
  const { translateRaw} = useT9n(APPLANGA_GROUP); // Using hooks but not named "use"
  // ...
};

// Wrong prefix
export function fetchData<T>(url: string) {
  const [data, setData] = useState<T | null>(null); // Using hooks but wrong name
  return { data };
}
```

**Why:** The "use" prefix:
- Signals the function follows hooks rules
- Enables ESLint hooks linting
- Standard React convention
- IDE recognizes it as a hook

## Pattern: useState with Function Updaters

Use function updaters when new state depends on previous state.

✅ **Good:**
```typescript
function Counter() {
  const [count, setCount] = useState(0);

  // Function updater - always gets latest state
  const increment = () => {
    setCount((prev) => prev + 1);
  };

  // Works correctly even if called multiple times
  const incrementTwice = () => {
    setCount((prev) => prev + 1);
    setCount((prev) => prev + 1); // prev is updated from first call
  };

  // Object updates
  const [user, setUser] = useState({ name: '', age: 0 });

  const updateName = (name: string) => {
    setUser((prev) => ({ ...prev, name }));
  };

  return <button onClick={increment}>Count: {count}</button>;
}
```

❌ **Bad:**
```typescript
function Counter() {
  const [count, setCount] = useState(0);

  // Direct value - can use stale state
  const increment = () => {
    setCount(count + 1); // Uses captured count value
  };

  // Doesn't work correctly
  const incrementTwice = () => {
    setCount(count + 1); // Uses same count
    setCount(count + 1); // Uses same count - only increments by 1!
  };

  return <button onClick={increment}>Count: {count}</button>;
}
```

**Why:** Function updaters:
- Always use latest state value
- Prevent stale closure issues
- Work correctly with multiple updates
- More reliable in async code

## Pattern: useEffect with Complete Dependencies

Always include all dependencies in the dependency array.

✅ **Good:**
```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const apiKey = useApiKey();

  useEffect(() => {
    async function fetchUser() {
      const data = await fetch(`/api/users/${userId}`, {
        headers: { Authorization: apiKey },
      });
      setUser(await data.json());
    }

    fetchUser();
  }, [userId, apiKey]); // All external values included

  return <div>{user?.name}</div>;
}
```

❌ **Bad:**
```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const apiKey = useApiKey();

  useEffect(() => {
    async function fetchUser() {
      const data = await fetch(`/api/users/${userId}`, {
        headers: { Authorization: apiKey }, // Using apiKey but not in deps!
      });
      setUser(await data.json());
    }

    fetchUser();
  }, [userId]); // Missing apiKey dependency

  return <div>{user?.name}</div>;
}
```

**Why:** Complete dependencies:
- Effect runs when any dependency changes
- Prevents stale closure bugs
- ESLint exhaustive-deps rule catches missing deps
- Makes effect behavior predictable

## Pattern: useEffect Cleanup Functions

Always clean up side effects (event listeners, subscriptions, timers).

✅ **Good:**
```typescript
function WindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);

    // Cleanup function
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <div>{size.width} x {size.height}</div>;
}

// Timer cleanup
function Timer() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      console.log('Tick');
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);
}

// Subscription cleanup
function DataStream() {
  useEffect(() => {
    const subscription = dataSource.subscribe((data) => {
      setData(data);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);
}
```

❌ **Bad:**
```typescript
// No cleanup - memory leak!
function WindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    // Missing cleanup!
  }, []);
}

// No cleanup - interval keeps running after unmount
function Timer() {
  useEffect(() => {
    setInterval(() => {
      console.log('Tick');
    }, 1000);
    // Missing clearInterval cleanup!
  }, []);
}
```

**Why:** Cleanup functions:
- Prevent memory leaks
- Remove event listeners on unmount
- Cancel pending requests
- Clear timers and intervals
- Unsubscribe from subscriptions

## Pattern: useMemo for Expensive Operations Only

Only use useMemo for truly expensive computations.

✅ **Good:**
```typescript
function ProductList({ products }: { products: Product[] }) {
  // Expensive: filtering + sorting large array
  const filteredProducts = useMemo(() => {
    return products
      .filter((p) => p.inStock)
      .sort((a, b) => b.rating - a.rating);
  }, [products]);

  // Simple: don't memoize
  const count = filteredProducts.length;
  const firstProduct = filteredProducts[0];

  return (
    <div>
      <p>Found {count} products</p>
      <ul>
        {filteredProducts.map((p) => <li key={p.id}>{p.name}</li>)}
      </ul>
    </div>
  );
}
```

❌ **Bad:**
```typescript
// Over-using useMemo for simple operations
function Component({ count }: { count: number }) {
  // Too simple to memoize
  const doubled = useMemo(() => count * 2, [count]);
  const isEven = useMemo(() => count % 2 === 0, [count]);
  const message = useMemo(() => `Count is ${count}`, [count]);

  // Just do this:
  // const doubled = count * 2;
  // const isEven = count % 2 === 0;
  // const message = `Count is ${count}`;

  return <div>{message}</div>;
}
```

**Why:** useMemo guidelines:
- Only for expensive operations (large array ops, heavy computations)
- Only for referential equality (objects passed to children)
- Don't use for simple math or string concatenation
- useMemo has overhead - use sparingly

## Pattern: useCallback for Functions Passed as Props

Use useCallback when passing functions to memoized child components.

✅ **Good:**
```typescript
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState<Item[]>([]);

  // Memoized callback - stable reference
  const handleItemClick = useCallback((id: string) => {
    console.log('Item clicked:', id);
  }, []); // Empty deps - never changes

  const handleDelete = useCallback((id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []); // Empty deps - uses function updater

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>

      {items.map((item) => (
        <ExpensiveItem
          key={item.id}
          item={item}
          onClick={handleItemClick}    // Stable reference
          onDelete={handleDelete}      // Stable reference
        />
      ))}
    </div>
  );
}

// Memoized child component
const ExpensiveItem = React.memo<ItemProps>(({ item, onClick, onDelete }) => {
  console.log('Rendering ExpensiveItem:', item.id);
  return (
    <div>
      <span onClick={() => onClick(item.id)}>{item.name}</span>
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </div>
  );
});
```

❌ **Bad:**
```typescript
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState<Item[]>([]);

  // New function every render - causes ExpensiveItem to re-render
  const handleItemClick = (id: string) => {
    console.log('Item clicked:', id);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>

      {items.map((item) => (
        <ExpensiveItem
          key={item.id}
          item={item}
          onClick={handleItemClick}    // New reference every render!
          onDelete={(id) => setItems(items.filter((i) => i.id !== id))} // New inline function!
        />
      ))}
    </div>
  );
}
```

**Why:** useCallback:
- Stable function reference prevents child re-renders
- Essential with React.memo
- Use when passing functions to children
- Don't use for functions not passed as props

## Pattern: Custom Hooks with Typed Return Values

Provide explicit return types for custom hooks.

✅ **Good:**
```typescript
// Return object with explicit type
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(url);
      setData(await response.json());
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Return tuple with explicit type
export function useToggle(
  initialValue: boolean
): [boolean, () => void, () => void] {
  const [value, setValue] = useState(initialValue);

  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return [value, setTrue, setFalse];
}
```

❌ **Bad:**
```typescript
// No explicit return type - consumers don't know what to expect
export function useFetch(url: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  // ...
  return { data, loading }; // Implicit return type
}

// Inconsistent return format
export function useToggle(initialValue: boolean) {
  const [value, setValue] = useState(initialValue);
  // Sometimes returns object, sometimes tuple - confusing!
  if (initialValue) {
    return [value, () => setValue(!value)];
  }
  return { value, toggle: () => setValue(!value) };
}
```

**Why:** Explicit return types:
- Clear API for consumers
- Better IntelliSense
- Type checking in hook implementation
- Self-documenting code

## Pattern: Preventing State Updates After Unmount

Use `isMounted` flag to prevent state updates after unmount.

✅ **Good:**
```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });
        const data = await response.json();

        // Only update state if still mounted
        if (isMounted) {
          setUser(data);
        }
      } catch (error) {
        if (isMounted && error.name !== 'AbortError') {
          console.error(error);
        }
      }
    }

    fetchUser();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [userId]);

  return user ? <div>{user.name}</div> : <div>Loading...</div>;
}
```

❌ **Bad:**
```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function fetchUser() {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();

      // Warning: Can't perform a React state update on an unmounted component
      setUser(data); // No check if component is still mounted!
    }

    fetchUser();
    // No cleanup!
  }, [userId]);

  return user ? <div>{user.name}</div> : <div>Loading...</div>;
}
```

**Why:** Unmount protection:
- Prevents "Can't perform state update on unmounted component" warnings
- Avoids memory leaks
- Cancels pending requests with AbortController
- Clean async handling

## Pattern: SSR-Safe Window Access

Check for `window` existence for Next.js SSR compatibility.

✅ **Good:**
```typescript
export function useWindowSize(): WindowSize {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // SSR guard
    if (typeof window === 'undefined') {
      return;
    }

    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return windowSize;
}
```

❌ **Bad:**
```typescript
// Crashes during SSR - window is not defined
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,  // ReferenceError: window is not defined
    height: window.innerHeight,
  });

  useEffect(() => {
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

**Why:** SSR safety:
- Next.js renders on server (no `window`)
- Check `typeof window !== 'undefined'`
- useEffect is client-only (safe for window access)
- Prevents SSR hydration errors

## Anti-Pattern: Calling Hooks Conditionally

Never call hooks inside conditions or loops.

❌ **Bad:**
```typescript
function Component({ shouldFetch }: { shouldFetch: boolean }) {
  // Conditional hook call - breaks rules!
  if (shouldFetch) {
    const [data, setData] = useState(null); // Error!
  }

  // Loop hook call - breaks rules!
  for (let i = 0; i < 3; i++) {
    const [item, setItem] = useState(null); // Error!
  }

  return <div>Content</div>;
}
```

✅ **Good:**
```typescript
function Component({ shouldFetch }: { shouldFetch: boolean }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Conditional logic INSIDE hook
    if (shouldFetch) {
      fetchData().then(setData);
    }
  }, [shouldFetch]);

  return <div>Content</div>;
}
```

**Why:** Hooks must be called:
- At the top level
- In the same order every render
- React relies on call order to track state
- Conditional calls break React's state tracking

## Anti-Pattern: Missing useEffect Dependencies

Don't omit dependencies from useEffect.

❌ **Bad:**
```typescript
function SearchComponent({ query }: { query: string }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    // Uses `query` but doesn't list it in deps
    searchAPI(query).then(setResults);
  }, []); // Missing query dependency!

  return <div>{results.length} results</div>;
}
```

✅ **Good:**
```typescript
function SearchComponent({ query }: { query: string }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    searchAPI(query).then(setResults);
  }, [query]); // Include query dependency

  return <div>{results.length} results</div>;
}
```

**Why:** Missing dependencies cause:
- Stale closures (using old values)
- Effect not running when it should
- Unpredictable behavior
- ESLint exhaustive-deps warns about this

## Anti-Pattern: Forgetting Cleanup

Always clean up effects that create subscriptions or listeners.

❌ **Bad:**
```typescript
// Memory leak - no cleanup!
function Component() {
  useEffect(() => {
    window.addEventListener('resize', handleResize);
    // Missing cleanup!
  }, []);
}

// Memory leak - interval keeps running
function Timer() {
  useEffect(() => {
    setInterval(() => {
      console.log('Tick');
    }, 1000);
    // Missing clearInterval!
  }, []);
}
```

✅ **Good:**
```typescript
function Component() {
  useEffect(() => {
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);
}

function Timer() {
  useEffect(() => {
    const intervalId = setInterval(() => {
      console.log('Tick');
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);
}
```

**Why:** Cleanup prevents:
- Memory leaks
- Multiple listeners/subscriptions
- Stale event handlers
- Performance issues

## Summary

**Key Patterns:**
- Custom hooks start with "use" prefix
- useState with function updaters for dependent state
- useEffect with complete dependencies
- useEffect cleanup for listeners/subscriptions
- useMemo only for expensive operations
- useCallback for functions passed to children
- Explicit return types on custom hooks
- `isMounted` flag prevents unmounted updates
- SSR-safe window access with typeof check

**Anti-Patterns to Avoid:**
- Calling hooks conditionally or in loops
- Missing dependencies in useEffect/useMemo/useCallback
- Not cleaning up side effects
- Direct state updates without function updaters
- Over-using useMemo/useCallback
- Forgetting "use" prefix on custom hooks
- Window access without SSR guard
- State updates after unmount
