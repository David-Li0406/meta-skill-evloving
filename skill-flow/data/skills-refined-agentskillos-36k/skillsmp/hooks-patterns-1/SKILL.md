---
name: hooks-patterns
description: "WHAT: React hooks patterns for web with useState, useEffect, and custom hooks. WHEN: managing state, side effects, data fetching, routing, window events. KEYWORDS: hooks, useState, useEffect, useMemo, useCallback, useRouter, custom hooks, web, Next.js."
---

# Hooks Patterns - Web

React hooks patterns for web applications with TypeScript, custom hooks, and Next.js integration.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use hooks for:
- Component state management
- Side effects (data fetching, subscriptions)
- Extracting reusable logic
- Accessing context
- Web-specific functionality (routing, window events)

## Core Principles

### 1. Custom Hook Naming

**Always prefix custom hooks with "use".**

✅ **Good:**
```typescript
// app/unified-spaces/registration-page/testimonials/useReviews.ts:6
import { useT9n } from '@/libs/translation';

export const useReviews = (
  numberOfReviews: number
): TestimonialsFeatureProps['reviews'] => {
  const { translateRaw } = useT9n(APPLANGA_GROUP);

  const reviews = [];

  for (let i = 1; i <= numberOfReviews; i++) {
    const displayName = translateRaw(`review-${i}.displayName`);
    const text = translateRaw(`review-${i}.text`);
    text && reviews.push({ displayName, text });
  }

  return reviews;
};
```

**Why:** The "use" prefix signals that the function follows hooks rules and enables linting.

### 2. Custom Hook TypeScript

**Type return values and parameters explicitly.**

✅ **Good:**
```typescript
// app/state/cart/cartSku/useCartSkuState.ts:5
import { useAtom, SetStateAction } from 'jotai';
import { CartSku, cartSkuState } from './cartSkuState';

const useCartSkuState = (): [
  CartSku,
  (update: SetStateAction<CartSku>) => void
] => useAtom(cartSkuState);

export default useCartSkuState;
```

**Why:** Explicit types provide better IDE support and catch errors at compile time.

### 3. useState Hook

**Use useState for component-local state.**

✅ **Good:**
```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState<number>(0);
  const [isActive, setIsActive] = useState(false);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setIsActive(!isActive)}>
        {isActive ? 'Deactivate' : 'Activate'}
      </button>
    </div>
  );
}
```

**Function updater:**
```typescript
// When new state depends on old state
setCount((prevCount) => prevCount + 1);

// With objects
setUser((prevUser) => ({ ...prevUser, name: 'New Name' }));
```

**Why:** useState is the simplest way to manage component state. Function updaters prevent stale closure issues.

### 4. useEffect Hook

**Use useEffect for side effects like data fetching and subscriptions.**

✅ **Good:**
```typescript
import { useEffect, useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchUser() {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();

      if (isMounted) {
        setUser(data);
      }
    }

    fetchUser();

    // Cleanup function
    return () => {
      isMounted = false;
    };
  }, [userId]); // Dependency array

  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

**Why:** useEffect runs after render. The cleanup function prevents memory leaks. Dependencies ensure effects run when needed.

### 5. useMemo Hook

**Use useMemo to memoize expensive computations.**

✅ **Good:**
```typescript
import { useMemo } from 'react';

function ProductList({ products }: { products: Product[] }) {
  const expensiveFiltered = useMemo(() => {
    console.log('Filtering products...');
    return products
      .filter(p => p.inStock)
      .sort((a, b) => b.rating - a.rating);
  }, [products]);

  return (
    <ul>
      {expensiveFiltered.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}
```

❌ **Bad:**
```typescript
// Don't memoize simple operations
const doubled = useMemo(() => count * 2, [count]); // Too simple!

// Better
const doubled = count * 2;
```

**Why:** useMemo prevents expensive calculations on every render. Only use for truly expensive operations.

### 6. useCallback Hook

**Use useCallback to memoize functions passed as props.**

✅ **Good:**
```typescript
import { useCallback, useState } from 'react';

function ParentComponent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount((c) => c + 1);
  }, []); // Empty deps - function never changes

  return <ExpensiveChild onClick={handleClick} />;
}
```

**Why:** useCallback prevents child components from re-rendering when the function reference doesn't change.

### 7. Custom Hooks for Reusable Logic

**Extract reusable logic into custom hooks.**

✅ **Good:**
```typescript
// useLocalStorage.ts
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Usage
function App() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle Theme
    </button>
  );
}
```

**Why:** Custom hooks make logic reusable across components and keep components clean.

## Web-Specific Hooks

### useRouter (Next.js)

```typescript
import { useRouter } from 'next/router';

function ProductPage() {
  const router = useRouter();
  const { id } = router.query;

  const handleNavigate = () => {
    router.push('/products');
  };

  return (
    <div>
      <h1>Product {id}</h1>
      <button onClick={handleNavigate}>Back to Products</button>
    </div>
  );
}
```

### useEffect with Window Events

```typescript
import { useEffect, useState } from 'react';

function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}

// Usage
function App() {
  const { width, height } = useWindowSize();

  return <div>Window size: {width} x {height}</div>;
}
```

## Advanced Patterns

### Custom Hook with State and Effects

```typescript
import { useState, useEffect } from 'react';

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        const json = await response.json();

        if (isMounted) {
          setData(json);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError(err as Error);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useFetch<User>(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data?.name}</div>;
}
```

### Combining Multiple Hooks

```typescript
function useAuthenticatedApi(url: string) {
  const { user } = useAuth();
  const { data, loading } = useFetch(url, {
    headers: {
      Authorization: `Bearer ${user?.token}`,
    },
  });

  return { data, loading };
}
```

## File Organization

```
hooks/
├── useLocalStorage.ts    # Reusable custom hook
├── useFetch.ts
├── useWindowSize.ts
└── useAuth.ts

components/
└── UserProfile/
    ├── UserProfile.tsx
    └── useUserData.ts   # Component-specific hook
```

## Common Mistakes

1. **Not using "use" prefix** - All custom hooks must start with "use"
2. **Calling hooks conditionally** - Hooks must be called in the same order every render
3. **Missing dependencies** - Always include all dependencies in useEffect/useMemo/useCallback
4. **Forgetting cleanup** - Clean up subscriptions and event listeners in useEffect
5. **Overusing useMemo/useCallback** - Only use for expensive operations or referential equality
6. **Not typing custom hooks** - Always provide explicit TypeScript types

## Quick Reference

### Basic Hooks

```typescript
// useState
const [value, setValue] = useState<string>('initial');

// useEffect
useEffect(() => {
  // Side effect
  return () => {
    // Cleanup
  };
}, [dependencies]);

// useMemo
const memoized = useMemo(() => expensiveOperation(a, b), [a, b]);

// useCallback
const callback = useCallback(() => doSomething(), [deps]);
```

### Custom Hook Template

```typescript
import { useState, useEffect } from 'react';

export function useCustomHook<T>(param: string): {
  data: T | null;
  loading: boolean;
  error: Error | null;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Custom logic

    return () => {
      // Cleanup
    };
  }, [param]);

  return { data, loading, error };
}
```

### Web-Specific

```typescript
// Next.js router
import { useRouter } from 'next/router';
const router = useRouter();
router.push('/path');

// Window event
useEffect(() => {
  const handler = () => { /* ... */ };
  window.addEventListener('event', handler);
  return () => window.removeEventListener('event', handler);
}, []);
```
