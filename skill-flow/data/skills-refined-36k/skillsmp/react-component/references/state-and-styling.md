# State Management & Styling

## Table of Contents

1. [State Management](#state-management)
2. [Styling with Tailwind v4](#styling-with-tailwind-v4)
3. [Async UX Standards](#async-ux-standards)
4. [TanStack Query Rules](#tanstack-query-rules)

---

## State Management

### Use the Right Tool for the Right Concern

| Data Type       | Use                                             |
| --------------- | ----------------------------------------------- |
| Remote/API data | **TanStack Query**                              |
| URL Params      | Router tools or **nuqs**                        |
| Local UI        | `useState` / `useReducer`                       |
| Shared UI       | Prop drilling → Context → Zustand (last resort) |
| Persistence     | Based on lifetime & UX needs                    |

### Performance Rules

- Avoid global stores for convenience
- Only subscribe to needed slices
- Don't overuse Context
- Do not put everything in a single state (triggers unnecessary re-renders)
- Split global state into multiple states according to where they are used
- Keep state as close as possible to where it is used

#### Memoization Best Practices

**Rule #1: Profile first.** Never apply memoization without first using the React DevTools Profiler to confirm that a component's re-renders are causing a legitimate performance issue.

**When to use `React.memo`:**

Wrap a component in `React.memo` only when:

1. It is a pure presentational component.
2. It re-renders often with the same props.
3. Its re-render is visibly slow (e.g., it contains complex charts, visualizations, or very large lists).

```tsx
// BAD: Unnecessary memoization on a simple component
const SimpleButton = React.memo(({ icon, children }) => <button>...</button>)

// GOOD: Memoizing a heavy component
const DataGrid = React.memo(({ rows, columns }) => {
  // ... expensive rendering logic for thousands of cells
})
```

**When to use `useCallback`:**

Use `useCallback` to preserve the identity of a function across re-renders. This is only necessary when:

1. Passing the function as a prop to a `React.memo`-wrapped child component.
2. Using the function as a dependency in a hook like `useEffect` or `useMemo`.

```tsx
// BAD: Wrapping every function "just in case"
const MyComponent = ({ value }) => {
  const handleClick = useCallback(() => {
    console.log(value)
  }, [value])
  return <button onClick={handleClick}>Click Me</button>
}

// GOOD: Preventing re-render of a memoized child
const Parent = () => {
  const [count, setCount] = useState(0)
  // Without useCallback, onUpdate would be a new function on every render,
  // causing HeavyChild to re-render unnecessarily.
  const handleUpdate = useCallback(() => {
    // ... logic
  }, [])

  return <HeavyChild onUpdate={handleUpdate} />
}
```

**When to use `useMemo`:**

Use `useMemo` to cache the result of an expensive calculation. "Expensive" means:

1. Complex data transformations on large arrays (e.g., filtering, sorting, mapping 1000+ items).
2. Intensive computational logic (e.g., cryptographic or financial calculations).

It should **not** be used for simple object or array creations.

```tsx
// BAD: Memoizing a simple object
const user = useMemo(() => ({ name: 'John', age: 30 }), [])

// GOOD: Memoizing an expensive filtering operation
const visibleTodos = useMemo(() => {
  // Imagine todos is an array of 5,000 items
  return todos.filter(t => t.status === filter)
}, [todos, filter])
```

### State Initializer Pattern

```tsx
// Incorrect: executed on every re-render
const [state, setState] = React.useState(myExpensiveFn())

// Correct: executed only once
const [state, setState] = React.useState(() => myExpensiveFn())
```

### useEffect Rules

- Only for effects that cannot happen via render, derived state, or events
- Must include a short comment explaining why it's necessary
- Prefer derived state, query state, and event handlers instead

---

## Styling with Tailwind v4

- Must use **Tailwind v4 only**
- **Never create `tailwind.config.js`** (all theme configuration lives in `styles/globals.css` using `@theme` directives)
- Tokens + config live in `styles/globals.css`
- Never hardcode values that have tokens

### Conditional Classes

Use the `cn` utility for conditional classnames:

```tsx
import { cn } from '@/lib/utils'
;<div className={cn('base-class', isActive && 'active-class')} />
```

### Responsive Design

Must support breakpoints: `sm`, `md`, `lg`, `xl` at minimum.

### Radix UI Themes

Must be an expert in [Radix UI themes](https://www.radix-ui.com/themes/docs/overview/getting-started).

---

## Async UX Standards

All remote UI must support four states:

| State   | Implementation                          |
| ------- | --------------------------------------- |
| Loading | Skeletons                               |
| Error   | Retry UI with actionable text           |
| Empty   | Clear state message (+ optional action) |
| Success | Data render                             |

Containers handle state; presenters decide which UI to show.

---

## TanStack Query Rules

- Never fetch inside `useEffect`
- Never sync query data into local state
- Query files live in `src/features/<feature>/api/`
- Use `select` for data transforms, not presenters

### Mutations Must:

- Invalidate relevant queries
- Guard against duplicate submissions

### Example Query Structure

```tsx
// src/features/revenue/api/useRevenueQuery.ts
export function useRevenueQuery() {
  return useQuery({
    queryKey: ['revenue'],
    queryFn: fetchRevenue,
    select: data => transformRevenueData(data),
  })
}
```
