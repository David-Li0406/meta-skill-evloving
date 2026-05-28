---
name: react
description: Modern React 18+ patterns with TypeScript, hooks, state management, and performance optimization. This skill should be used when building React components, debugging frontend issues, or reviewing React code. (user)
---

# React Best Practices (2025)

## Component Patterns

### Functional Components Only

```tsx
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
}

function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <article onClick={() => onSelect?.(user)}>
      <h2>{user.name}</h2>
    </article>
  );
}
```

### Props Destructuring

- Always destructure props in function signature
- Use default values: `{ size = 'md' }: Props`
- Spread remaining props: `{ className, ...rest }`

### Composition Over Props Drilling

```tsx
// ❌ Prop drilling
<Parent user={user}>
  <Child user={user}>
    <GrandChild user={user} />
  </Child>
</Parent>

// ✅ Composition
<UserProvider user={user}>
  <Parent>
    <Child>
      <GrandChild />
    </Child>
  </Parent>
</UserProvider>
```

## Page Patterns

### Unified Create/Edit Form

Single form component handles both modes via optional entity prop:

```tsx
interface EntityFormProps {
  entity?: Entity;
  onSuccess: (entity: Entity) => void;
  onCancel: () => void;
}

function EntityForm({ entity, onSuccess, onCancel }: EntityFormProps) {
  const isEdit = Boolean(entity);
  const [formData, setFormData] = useState(entity ?? initialFormData);

  // Conditional mutation based on mode
  // Edit-only features (delete, publish) render when isEdit
}
```

Pages become thin wrappers:

```tsx
// CreatePage
<EntityForm onSuccess={(e) => navigate(`/entities/${e.id}`)} onCancel={() => navigate('/entities')} />

// EditPage - fetch data first
const { data: entity } = useEntity(id);
<EntityForm entity={entity} onSuccess={...} onCancel={...} />
```

### Reusable UI Components

Extract repeated patterns: `Pagination`, `Snackbar`, `DeleteConfirmModal`, `StatusBadge`

## Hooks Best Practices

### useState

- Use functional updates for derived state: `setCount(c => c + 1)`
- Prefer multiple states over one object
- Initialize expensive state with function: `useState(() => computeExpensive())`

### useEffect

- One effect per concern
- Always include cleanup when needed
- Avoid objects in dependency arrays (use primitives)

```tsx
// ✅ Good: Minimal dependencies
useEffect(() => {
  const handler = () => setWidth(window.innerWidth);
  window.addEventListener("resize", handler);
  return () => window.removeEventListener("resize", handler);
}, []); // Empty = mount only
```

### useMemo / useCallback

- Only for expensive computations
- Only when passing to memoized children
- Don't over-optimize prematurely

```tsx
// Memoize expensive filter
const filtered = useMemo(
  () => items.filter((i) => i.name.includes(search)),
  [items, search],
);

// Memoize callback for React.memo child
const handleClick = useCallback((id: string) => setSelected(id), []);
```

### Custom Hooks

- Extract reusable logic
- Name with `use` prefix
- Return tuple or object consistently

```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

## State Management

### Hierarchy (prefer top to bottom)

1. **Local state** - Component-specific
2. **Lifted state** - Shared between siblings
3. **Context** - Cross-cutting (theme, auth)
4. **External store** - Complex global state (Zustand, Jotai)

### When to Use Context

- Theme/appearance
- User authentication
- Locale/i18n
- Feature flags

### Zustand Pattern (Recommended)

```tsx
const useStore = create<State>((set) => ({
  items: [],
  addItem: (item) => set((s) => ({ items: [...s.items, item] })),
  removeItem: (id) =>
    set((s) => ({
      items: s.items.filter((i) => i.id !== id),
    })),
}));
```

## TypeScript Patterns

### Props Types

```tsx
interface Props {
  required: string;
  optional?: number;
  children: React.ReactNode;
  onClick: (event: React.MouseEvent) => void;
  as?: React.ElementType;
}
```

### Generic Components

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

## Performance

### React.memo

- Wrap components receiving same props repeatedly
- Combine with useCallback for function props
- Don't use everywhere (adds overhead)

### Lazy Loading

```tsx
const HeavyComponent = lazy(() => import("./HeavyComponent"));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Keys

- Use stable, unique IDs (not array index)
- Changing key forces remount

## Testing (Vitest + Testing Library)

```tsx
import { render, screen, fireEvent } from "@testing-library/react";

describe("Button", () => {
  it("calls onClick when clicked", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole("button"));

    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

## Common Mistakes

❌ **Avoid:**

- Mutating state directly
- Async operations in render
- Inline object/array creation in JSX (causes re-renders)
- Missing keys in lists
- useEffect without dependencies
- Over-abstracting too early

✅ **Do:**

- Treat state as immutable
- Use error boundaries
- Colocate state with usage
- Memoize expensive computations
- Use TypeScript strictly
