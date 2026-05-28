# React Best Practices Reference

## Component Design Principles

### Single Responsibility
Each component should have one clear purpose. Split components when they handle multiple concerns.

### Composition over Inheritance
Build complex UIs from simple, composable pieces. Use children and render props instead of inheritance.

### Colocation
Keep related code together:
- Tests next to components
- Styles next to components
- Types next to components

## Hooks Guidelines

### Rules of Hooks
1. Only call hooks at the top level (not in loops, conditions, or nested functions)
2. Only call hooks from React functions (components or custom hooks)
3. Custom hooks must start with "use"

### Common Hooks Usage

**useState** - Local component state
```jsx
const [value, setValue] = useState(initialValue);
```

**useEffect** - Side effects and lifecycle
```jsx
useEffect(() => {
  // Effect code
  return () => { /* cleanup */ };
}, [dependencies]);
```

**useCallback** - Memoize callbacks passed to children
```jsx
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

**useMemo** - Memoize expensive computations
```jsx
const sortedItems = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

## Performance Optimization

### Avoid Unnecessary Re-renders

1. **Memoize components** with React.memo for expensive renders
2. **Memoize callbacks** with useCallback when passed to children
3. **Memoize values** with useMemo for expensive calculations
4. **Use stable references** - avoid inline objects/arrays in JSX

### Code Splitting

```jsx
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>
```

### Virtualization
For long lists, use virtualization libraries like react-virtual or react-window.

## State Management

### When to Use What

| Scenario | Solution |
|----------|----------|
| Component-local UI state | useState |
| Complex component state | useReducer |
| Shared state (few consumers) | Lift state up |
| Shared state (many consumers) | Context |
| Server data | React Query, SWR |
| Global app state | Zustand, Redux Toolkit |

### Context Best Practices
- Split contexts by domain (AuthContext, ThemeContext)
- Memoize provider values to prevent re-renders
- Consider context only for truly global data

## Testing

### Testing Library Philosophy
- Test behavior, not implementation
- Query by accessibility roles first
- Avoid testing internal state

### Query Priority
1. getByRole (most accessible)
2. getByLabelText
3. getByPlaceholderText
4. getByText
5. getByDisplayValue
6. getByTestId (last resort)

## Accessibility (a11y)

### Key Requirements
- All images need alt text
- All form inputs need labels
- Color contrast must be sufficient (4.5:1 for text)
- All functionality keyboard accessible
- Proper heading hierarchy (h1, h2, h3...)

### Common ARIA Usage
```jsx
<button aria-label="Close dialog" onClick={onClose}>
  <CloseIcon aria-hidden="true" />
</button>

<div role="alert" aria-live="polite">
  {errorMessage}
</div>
```

## Project Structure

### Feature-Based Organization
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── index.ts
│   └── products/
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── app/
    └── routes/
```

## TypeScript Integration

### Component Props
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  children: React.ReactNode;
  onClick?: () => void;
}

const Button = ({ variant, size = 'medium', children, onClick }: ButtonProps) => {
  // ...
};
```

### Generic Components
```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```
