---
name: react
description: React hooks + performance patterns. Use for useEffect, useMemo, useCallback, memo, rerender, derived state, performance, bundle, optimize, hooks, state, useTransition, Promise.all, waterfall, async
---

# React Fundamentals

## Core Philosophy

**Effects are escape hatches.** They synchronize React with external systems. If no external system is involved, you likely don't need one.

**Performance optimization is targeted.** Don't memoize everything. Profile first, optimize measurable bottlenecks.

## useEffect Decision Tree

```text
Do I need useEffect?

Is there an external system involved?
├── No → Don't use useEffect
│   ├── Derived state? → Calculate during render
│   ├── Event response? → Handle in event handler
│   └── Data fetching? → Use TanStack Query
└── Yes → Maybe use useEffect
    ├── Browser APIs (focus, scroll, localStorage)
    ├── Third-party widgets (maps, charts)
    ├── Network connections (WebSockets)
    └── Analytics/logging
```

## Derived State (No Effect Needed)

```tsx
// ❌ Bad - useEffect for derived state
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// ✅ Good - calculate during render
const fullName = `${firstName} ${lastName}`;

// ✅ With memoization (only if expensive)
const sortedItems = useMemo(
  () => items.toSorted((a, b) => a.name.localeCompare(b.name)),
  [items],
);
```

## Event Handlers (No Effect Needed)

```tsx
// ❌ Bad - effect chain for event response
useEffect(() => {
  if (submitted) {
    navigate('/success');
  }
}, [submitted]);

// ✅ Good - handle in event
const handleSubmit = async () => {
  await submitForm();
  navigate('/success');
};
```

## Performance Patterns

### useMemo - Expensive Calculations Only

```tsx
// ❌ Bad - memoizing cheap operations
const doubled = useMemo(() => value * 2, [value]);

// ✅ Good - memoizing expensive operations
const sortedItems = useMemo(
  () => items.toSorted((a, b) => a.price - b.price),
  [items],
);

// ✅ Good - maintaining referential equality for deps
const filterFn = useMemo(() => (item) => item.active, []);
```

### useCallback - For Memoized Children Only

```tsx
// ❌ Bad - useCallback without memoized child
const handleClick = useCallback(() => doSomething(), []);
return <button onClick={handleClick}>Click</button>;

// ✅ Good - useCallback for memoized child
const handleClick = useCallback(() => doSomething(id), [id]);
return <MemoizedChild onClick={handleClick} />;
```

### Avoiding Re-renders

```tsx
// ❌ Bad - object literal creates new reference every render
<Child style={{ color: 'red' }} />;

// ✅ Good - stable reference
const style = useMemo(() => ({ color: 'red' }), []);
<Child style={style} />;

// ✅ Better - define outside component if static
const style = { color: 'red' };
function Parent() {
  return <Child style={style} />;
}
```

## Async Patterns

### Parallel Fetches

```tsx
// ❌ Bad - sequential (waterfall)
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);

// ✅ Good - parallel with Promise.all
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id),
]);
```

### useTransition for Non-Urgent Updates

```tsx
const [isPending, startTransition] = useTransition();

const handleSearch = (query: string) => {
  // Urgent: update input immediately
  setQuery(query);

  // Non-urgent: can be interrupted
  startTransition(() => {
    setFilteredResults(filterItems(query));
  });
};
```

### Lazy State Initialization

```tsx
// ❌ Bad - expensive function runs every render
const [items, setItems] = useState(parseExpensiveData(raw));

// ✅ Good - lazy initialization runs once
const [items, setItems] = useState(() => parseExpensiveData(raw));
```

## Set/Map for O(1) Lookups

```tsx
// ❌ Bad - O(n) on every render
const isSelected = (id: string) => selectedIds.includes(id);

// ✅ Good - O(1) lookups with Set
const selectedSet = useMemo(() => new Set(selectedIds), [selectedIds]);
const isSelected = (id: string) => selectedSet.has(id);
```

## Common Mistakes

| Mistake                    | Fix                                 |
| -------------------------- | ----------------------------------- |
| Derived state in useEffect | Calculate during render             |
| Effect chains (A→B→C)      | Derive all values directly          |
| useMemo for simple values  | Only memoize expensive computations |
| useCallback everywhere     | Only for memoized child components  |
| Object literals as props   | Define outside component or useMemo |
| Manual data fetching       | Use TanStack Query                  |
| Sequential awaits          | Use Promise.all for parallel ops    |
| Array.includes in loops    | Use Set with useMemo for O(1)       |
| useState(expensiveInit())  | Use useState(() => expensiveInit()) |

## Delegation

- **Data fetching**: For queries and caching, see [tanstack-query](../tanstack-query/SKILL.md) skill
- **Form state**: For form handling, see [tanstack-form](../tanstack-form/SKILL.md) skill
- **URL state**: For routing and params, see [tanstack-router](../tanstack-router/SKILL.md) skill
- **Error handling**: For error boundaries, see [error-boundaries](../error-boundaries/SKILL.md) skill
- **Full-stack flows**: For integrated patterns, see [integration-patterns](../integration-patterns/SKILL.md) skill
- **Code review**: After optimizing components, delegate to `code-reviewer` agent
