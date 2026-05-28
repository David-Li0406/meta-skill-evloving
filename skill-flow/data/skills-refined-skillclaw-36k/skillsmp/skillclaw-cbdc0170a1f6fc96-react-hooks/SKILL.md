---
name: react-hooks
description: Use this skill when you want to implement best practices for React Hooks and create custom hooks effectively.
---

# React Hooks

## **Priority: P1 (OPERATIONAL)**

Effective usage of React Hooks.

## Implementation Guidelines

- **Rules**: Use hooks only at the top level and within React function components.
- **`useEffect`**: Use for syncing with external systems only, and always include cleanup logic.
- **`useRef`**: Utilize for mutable state that does not trigger re-renders (e.g., DOM elements, timers).
- **`useMemo`/`useCallback`**: Measure performance first; use these hooks for stable references or heavy computations.
- **Dependencies**: Always specify exhaustive dependencies to avoid stale closures; do not disable linter warnings.
- **Custom Hooks**: Extract shared logic into custom hooks, prefixed with `use*`.
- **Refs as Escape Hatch**: Use refs to access imperative APIs (e.g., focus, scroll).
- **Stability**: Implement the `useLatest` pattern for event handlers to prevent issues with dependency changes.
- **Concurrency**: Use `useTransition` and `useDeferredValue` for non-blocking UI updates.
- **Initialization**: Use lazy initialization with `useState(() => expensive())` for expensive computations.

## Anti-Patterns

- **No Effects for Data Flow**: Avoid deriving state directly in the render method.
- **No Missing Dependencies**: Always include dependencies to prevent stale closures.
- **No Complex Effects**: Break complex effects into multiple simpler effects.
- **No Oversubscription**: Utilize tools like `why-did-you-render` to check for unnecessary re-renders.

## Code Examples

```tsx
// Custom Hook
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

// Lazy Initialization
const [state, setState] = useState(() => computeExpensiveValue());
```

## Reference & Examples

See [references/REFERENCE.md](references/REFERENCE.md).