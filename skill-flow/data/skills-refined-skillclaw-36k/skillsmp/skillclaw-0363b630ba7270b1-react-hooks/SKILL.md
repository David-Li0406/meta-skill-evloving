---
name: react-hooks
description: Use this skill when implementing React hooks for managing state, side effects, memoization, and creating custom hooks.
---

# React Hooks Guide

## Core Principles

Use hooks to manage state, effects, memoization, and callbacks with proper dependency arrays. Follow React's rules of hooks to prevent memory leaks, stale closures, and unnecessary re-renders.

## Basic Hooks

### useState

Manage local component state.

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(prev => prev + 1);

  return <button onClick={increment}>{count}</button>;
}
```

### useEffect

Perform side effects in function components.

```typescript
import { useState, useEffect } from 'react';

function OnlineStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return <span>{isOnline ? '✅ Online' : '❌ Offline'}</span>;
}
```

### useMemo

Memoize expensive computations to optimize performance.

```typescript
import { useMemo } from 'react';

function ExpensiveList({ items, filter }) {
  const filteredItems = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter]
  );

  return <ul>{filteredItems.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

### useCallback

Memoize functions to maintain stable references.

```typescript
import { useCallback } from 'react';

function TodoList({ todos, onToggle }) {
  const handleToggle = useCallback(
    (id) => onToggle(id),
    [onToggle]
  );

  return todos.map(todo => (
    <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} />
  ));
}
```

### useRef

Persist values without causing re-renders.

```typescript
import { useRef, useEffect } from 'react';

function TextInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} />;
}
```

## Custom Hooks

Create reusable logic by composing custom hooks.

### Example: useFormInput

```typescript
import { useState } from 'react';

function useFormInput(initialValue) {
  const [value, setValue] = useState(initialValue);
  
  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return {
    value,
    onChange: handleChange,
  };
}
```