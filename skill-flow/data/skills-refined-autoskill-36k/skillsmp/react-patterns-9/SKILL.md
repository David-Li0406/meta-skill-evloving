---
name: react-patterns
description: "React component patterns, hooks, server components, and composition. Use when building React components or deciding between patterns."
---

# React Patterns

## Overview

Decision guide for React patterns focusing on component architecture, hooks, and the server/client component model.

## Server vs Client Components

### Decision Matrix

| Need | Component Type | Directive |
|------|---------------|-----------|
| Data fetching | Server | (none) |
| Direct DB access | Server | (none) |
| Static content | Server | (none) |
| Event handlers | Client | `'use client'` |
| useState/useEffect | Client | `'use client'` |
| Browser APIs | Client | `'use client'` |

### Pattern: Composition for Interactivity

```typescript
// Server component (default) - does data fetching
async function UserProfile({ id }: { id: string }) {
  const user = await db.user.findUnique({ where: { id } });
  return (
    <div>
      <h1>{user.name}</h1>
      <FollowButton userId={id} /> {/* Client component island */}
    </div>
  );
}

// Client component - handles interactivity
'use client';
function FollowButton({ userId }: { userId: string }) {
  const [following, setFollowing] = useState(false);
  return <button onClick={() => setFollowing(!following)}>Follow</button>;
}
```

## Component Composition

### Compound Components (for related UI)

```typescript
function Tabs({ children }: { children: React.ReactNode }) {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
}

Tabs.List = TabsList;
Tabs.Panel = TabsPanel;

// Usage: <Tabs><Tabs.List>...</Tabs.List></Tabs>
```

### Render Props (for behavior sharing)

```typescript
function DataFetcher<T>({
  url,
  children
}: {
  url: string;
  children: (data: T | null, loading: boolean) => ReactNode
}) {
  const { data, loading } = useFetch<T>(url);
  return children(data, loading);
}
```

## Hook Patterns

### Custom Hook Structure

```typescript
function useAsync<T>(asyncFn: () => Promise<T>) {
  const [state, setState] = useState<{
    data: T | null;
    error: Error | null;
    loading: boolean;
  }>({ data: null, error: null, loading: true });

  useEffect(() => {
    asyncFn()
      .then(data => setState({ data, error: null, loading: false }))
      .catch(error => setState({ data: null, error, loading: false }));
  }, [asyncFn]);

  return state;
}
```

### useEffect Dependencies

```typescript
// GOOD: Stable reference with useCallback
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// GOOD: Object dependencies via useMemo
const options = useMemo(() => ({ page, limit }), [page, limit]);
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Props drilling 3+ levels | Hard to maintain | Context or composition |
| useEffect for derived state | Extra renders | useMemo or compute in render |
| Inline object/array props | Breaks memoization | useMemo or extract constant |
| Giant components (300+ lines) | Hard to test/read | Extract sub-components |
| useEffect for data sync | Race conditions | Use query library (TanStack) |

```typescript
// BAD: Derived state in useEffect
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${first} ${last}`);
}, [first, last]);

// GOOD: Compute during render
const fullName = `${first} ${last}`;
```

## Performance Decisions

| Situation | Tool |
|-----------|------|
| Expensive calculation | `useMemo` |
| Callback passed to child | `useCallback` |
| Prevent child re-render | `React.memo` |
| Non-blocking update | `useTransition` |
| Show stale during load | `useDeferredValue` |

**Rule:** Profile first. Don't prematurely optimize.

## Form Patterns

```typescript
// Prefer controlled with form library
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { name: '' },
});

// Uncontrolled for simple cases
const inputRef = useRef<HTMLInputElement>(null);
const handleSubmit = () => console.log(inputRef.current?.value);
```

## Red Flags

- `'use client'` at top of every file (server components are default)
- useEffect with empty deps that should run once on mount
- State that could be URL params (use `useSearchParams`)
- Fetching in useEffect (use server components or TanStack Query)
- Context for frequently changing values (causes re-renders)

## Quick Reference

```typescript
// ForwardRef pattern
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

// Error boundary (class required)
class ErrorBoundary extends Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
}
```
