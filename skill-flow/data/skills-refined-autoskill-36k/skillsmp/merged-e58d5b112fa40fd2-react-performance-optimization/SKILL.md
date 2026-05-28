---
name: react-performance-optimization
description: Optimize React application performance using techniques like memoization, lazy loading, code splitting, and virtualization. Use when addressing slow renders, large bundles, or memory issues.
---

# React Performance Optimization

## When to Use This Skill

Use this skill when:
- Initial load time is too slow
- Components re-render unnecessarily
- Rendering large lists or data sets
- Bundle size is too large
- Memory usage is high

## Performance Optimization Techniques

### 1. React.memo

Prevent unnecessary re-renders by wrapping components with `React.memo`.

```typescript
import { memo } from 'react';

interface UserCardProps {
  user: User;
  onSelect: (id: string) => void;
}

export const UserCard = memo(function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <div onClick={() => onSelect(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});
```

### 2. useMemo & useCallback

#### useMemo - Memoize Values

```typescript
import { useMemo } from 'react';

function UserList({ users, filter }: Props) {
  const filteredUsers = useMemo(
    () => users.filter(u => u.name.includes(filter)),
    [users, filter]
  );

  return <ul>{filteredUsers.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

#### useCallback - Memoize Functions

```typescript
import { useCallback } from 'react';

function TodoList({ todos }: Props) {
  const handleDelete = useCallback((id: string) => {
    deleteTodo(id);
  }, []);

  return todos.map(todo => (
    <TodoItem key={todo.id} todo={todo} onDelete={handleDelete} />
  ));
}
```

### 3. Lazy Loading & Code Splitting

Use `React.lazy` and `Suspense` for lazy loading components and routes.

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### 4. Virtualization

Render only visible items in long lists to improve performance.

```typescript
import { FixedSizeList } from 'react-window';

function VirtualList({ items, onSelect }: { items: Item[]; onSelect: (id: string) => void; }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style} onClick={() => onSelect(items[index].id)}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={400}
      width="100%"
      itemCount={items.length}
      itemSize={50}
    >
      {Row}
    </FixedSizeList>
  );
}
```

### 5. Bundle Size Optimization

Analyze and reduce bundle size using tools like Webpack Bundle Analyzer.

```bash
npm install --save-dev webpack-bundle-analyzer
```

### 6. Debouncing & Throttling

Implement debouncing for input handlers to reduce the number of calls made during rapid input changes.

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

## Performance Checklist

- [ ] Use `React.memo` for pure components
- [ ] Memoize expensive calculations with `useMemo`
- [ ] Stabilize callbacks with `useCallback`
- [ ] Lazy load routes and heavy components
- [ ] Virtualize long lists (100+ items)
- [ ] Debounce input handlers
- [ ] Analyze and reduce bundle size

## Profiling

Use React DevTools Profiler to analyze component renders and identify performance bottlenecks.

1. Install React DevTools extension
2. Open Profiler tab
3. Record interactions
4. Analyze component renders

## References

- [React Optimization](https://react.dev/learn/render-and-commit#optimizing-performance)
- [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)