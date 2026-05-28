---
name: react-performance-optimization
description: Use this skill when optimizing React application performance, including techniques like memoization, lazy loading, and code splitting to improve load times and rendering efficiency.
---

# React Performance Optimization

## When to Use This Skill

Use this skill when:
- Initial load time is too slow.
- Components re-render unnecessarily.
- Rendering large lists or data sets.
- Bundle size is too large.
- Memory usage is high.

## Techniques

### 1. React.memo

Prevent unnecessary re-renders when props remain unchanged.

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

### 3. Lazy Loading

#### Component Lazy Loading

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Analytics = lazy(() => import('./Analytics'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}
```

### 4. Virtualization

For long lists, render only visible items to improve performance.

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35,
  });

  return (
    <div ref={parentRef}>
      {virtualizer.getVirtualItems().map(virtualRow => (
        <div key={virtualRow.index} style={{ height: virtualRow.size }}>
          {items[virtualRow.index].name}
        </div>
      ))}
    </div>
  );
}
```