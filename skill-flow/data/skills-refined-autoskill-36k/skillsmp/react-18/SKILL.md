---
name: react-18
description: >
  React 18 component patterns and best practices.
  Trigger: When writing React 18 components/hooks in .tsx (components, hooks, context, memo, useRef, etc.).
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Writing React components'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Imports (REQUIRED)

```typescript
// ✅ ALWAYS: Named imports
import { useState, useEffect, useRef, forwardRef } from 'react';

// ❌ NEVER
import React from 'react';
import * as React from 'react';
```

## Component Pattern

```typescript
// ✅ ALWAYS: Named exports (except pages)
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, ...props }, ref) => {
    return <button ref={ref} {...props}>{children}</button>;
  }
);

Button.displayName = 'Button';

// ❌ NEVER: Default export (except pages)
export default function Button() { } // NO for components
export default function Page() { }  // OK for pages
```

## forwardRef for Component Refs

```typescript
// ✅ Use forwardRef for components that need refs
export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, ...props }, ref) => {
    return (
      <div>
        {label && <label>{label}</label>}
        <input ref={ref} {...props} />
      </div>
    );
  }
);
```

## useState

```typescript
// ✅ Simple state
const [count, setCount] = useState(0);

// ✅ Functional updates
setCount(prev => prev + 1);

// ✅ Lazy initialization
const [data, setData] = useState(() => computeExpensiveValue());

// ✅ Object state
const [form, setForm] = useState({ name: '', email: '' });

// ✅ Update object state
setForm(prev => ({ ...prev, email: 'new@example.com' }));
```

## useEffect

```typescript
// ✅ Run on mount
useEffect(() => {
  fetchData();
}, []);

// ✅ Run when dependencies change
useEffect(() => {
  fetchData(searchTerm);
}, [searchTerm]);

// ✅ Cleanup
useEffect(() => {
  const socket = io(SOCKET_URL);

  return () => {
    socket.disconnect();
  };
}, []);
```

## useRef

```typescript
// ✅ DOM ref
const inputRef = useRef<HTMLInputElement>(null);

inputRef.current?.focus();

// ✅ Persist value across renders
const timerRef = useRef<NodeJS.Timeout>();

useEffect(() => {
  timerRef.current = setTimeout(() => {}, 1000);
  return () => clearTimeout(timerRef.current);
}, []);
```

## Context

```typescript
// ✅ Create context
const AuthContext = createContext<AuthContextType | null>(null);

// ✅ Provide context
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// ✅ Use context hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

## Custom Hooks

```typescript
// ✅ Custom hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

// ✅ Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

## Conditional Rendering

```typescript
// ✅ Ternary
{isLoading ? <Spinner /> : <Data />}

// ✅ Logical AND
{error && <Alert message={error} />}

// ✅ Early return
if (isLoading) return <Spinner />;
if (error) return <Alert message={error} />;
return <Data />;
```

## Lists and Keys

```typescript
// ✅ Stable keys (id)
{clients.map(client => (
  <ClientCard key={client.id} client={client} />
))}

// ❌ Index as key (unless list is static)
{clients.map((client, index) => (
  <ClientCard key={index} client={client} /> // NO!
))}
```

## Event Handlers

```typescript
// ✅ Direct handler
const handleClick = () => {
  console.log('clicked');
};

// ✅ With event
const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// ✅ With arguments
const handleDelete = (id: string) => () => {
  deleteClient(id);
};
```

## Related Skills

- `migestion-web` - MiGestion Web-specific patterns
- `zustand-4` - State management with Zustand
- `vite` - Vite build patterns
