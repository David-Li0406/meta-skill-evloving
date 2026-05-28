---
name: react-hooks-best-practices
description: Use this skill when implementing React Hooks and optimizing component performance through best practices and custom hook creation.
---

# React Hooks Best Practices

## When to use this skill
- Creating functional components.
- Designing custom hooks.
- Optimizing re-renders and component performance.

## Implementation Guidelines

### 1. Hooks Rules
- **Top Level**: Only call hooks at the top level of the component or custom hook.
- **Dependencies**: Be honest with dependency arrays in `useEffect`, `useCallback`, and `useMemo`. Always use exhaustive dependencies to avoid stale closures.

### 2. Effect Management
- **`useEffect`**: Use for syncing with external systems only. Always include cleanup logic.
- **`useRef`**: Utilize for mutable state that does not trigger re-renders (e.g., DOM elements, timers).
- **Stability**: Use the `useLatest` pattern for event handlers to avoid issues with stale closures.

### 3. Memoization
- **`useMemo`/`useCallback`**: Use these hooks for expensive calculations or when passing functions/objects as props to memoized children. Avoid over-memoization as it can add unnecessary overhead.
- **Stable References**: Remember that objects and arrays defined inside the component body are new references on every render.

### 4. Component Composition
- **Props**: Prefer passing `children` instead of prop drilling complex state.
- **Container/Presenter Pattern**: Separate logic (like data fetching) from UI rendering for better maintainability.

### 5. State Management
- **Local vs Global State**: Keep state as local as possible. Lift state up only when necessary for sibling components.
- **Context**: Use Context for low-velocity global data (e.g., theme, user information). For high-velocity data, consider using a signal-based library or optimized subscriber pattern.

## Anti-Patterns
- **No Effects for Data Flow**: Avoid deriving state directly in the render method.
- **No Missing Dependencies**: Always include all dependencies in hooks to prevent stale closures.
- **No Complex Effects**: Split complex effects into multiple simpler effects.
- **No Oversubscription**: Use tools like `why-did-you-render` to check for unnecessary re-renders.

## Code Examples

```tsx
// Custom Hook for Window Size
function useWindowSize() {
  const [size, setSize] = useState({ w: 0, h: 0 });

  useEffect(() => {
    const handleResize = () => {
      setSize({ w: window.innerWidth, h: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []); // Empty array means this effect runs once on mount

  return size;
}

// Lazy Initialization of State
const [state, setState] = useState(() => computeExpensiveValue());
```

## Reference & Examples
See [references/REFERENCE.md](references/REFERENCE.md) for additional resources and examples.