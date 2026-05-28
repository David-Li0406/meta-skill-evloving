---
name: react-hooks-patterns
description: Use this skill when managing state, side effects, and reusable logic in React applications using hooks.
---

# React Hooks Patterns

## Overview

This skill provides patterns for using React hooks, including `useState`, `useEffect`, `useMemo`, `useCallback`, and custom hooks. It is applicable for managing component state, handling side effects, optimizing performance, and creating reusable logic across components.

## Core Principles

1. **Custom Hook Naming**: Always prefix custom hooks with "use" to signal that they follow React's hooks rules.
2. **TypeScript Usage**: Explicitly type return values and parameters in custom hooks for better IDE support and error checking.
3. **State Management**: Use `useState` for local component state and function updaters to prevent stale closures.
4. **Side Effects**: Use `useEffect` for side effects like data fetching and subscriptions, ensuring to include all dependencies and provide cleanup functions.
5. **Memoization**: Use `useMemo` for expensive calculations and `useCallback` for stable function references to prevent unnecessary re-renders.

## Basic Hooks

### useState

Manage local component state.

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
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

### useEffect

Handle side effects such as data fetching.

```typescript
import { useEffect, useState } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchUser() {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      if (isMounted) setUser(data);
    }

    fetchUser();
    return () => { isMounted = false; }; // Cleanup
  }, [userId]);

  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

### useMemo

Memoize expensive calculations.

```typescript
import { useMemo } from 'react';

function ProductList({ products }) {
  const expensiveFiltered = useMemo(() => {
    return products.filter(p => p.inStock).sort((a, b) => b.rating - a.rating);
  }, [products]);

  return (
    <ul>
      {expensiveFiltered.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}
```

### useCallback

Memoize functions to prevent unnecessary re-renders.

```typescript
import { useCallback, useState } from 'react';

function ParentComponent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return <ExpensiveChild onClick={handleClick} />;
}
```

## Custom Hooks

### Creating Custom Hooks

Extract reusable logic into custom hooks.

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = value => {
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

## Advanced Patterns

### useRouter (Next.js)

Utilize routing in Next.js applications.

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

### useWindowSize

Track window size with a custom hook.

```typescript
import { useEffect, useState } from 'react';

function useWindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

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

## Common Mistakes

1. **Not using "use" prefix**: All custom hooks must start with "use".
2. **Calling hooks conditionally**: Hooks must be called in the same order every render.
3. **Missing dependencies**: Always include all dependencies in `useEffect`, `useMemo`, and `useCallback`.
4. **Forgetting cleanup**: Clean up subscriptions and event listeners in `useEffect`.
5. **Overusing `useMemo`/`useCallback`**: Only use for expensive operations or referential equality.
6. **Not typing custom hooks**: Always provide explicit TypeScript types.

## Quick Reference

### Basic Hooks

```typescript
// useState
const [value, setValue] = useState('initial');

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