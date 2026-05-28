---
name: react-state-management
description: Use this skill when managing local, global, and server state in React applications.
---

# React State Management

## **Priority: P0 (CRITICAL)**

Choosing the right tool for state scope.

## Implementation Guidelines

- **Local**: Use `useState`. Opt for `useReducer` if the state is complex (state machine).
- **Derived**: Calculate derived state directly, e.g., `const fullName = first + last`. Avoid state synchronization.
- **Context**: Utilize for Dependency Injection (DI), theming, and authentication, but not for high-frequency data.
- **Global**: Implement Zustand or Redux for complex app-wide state management.
- **Server Cache**: Use `React.cache` (RSC) to deduplicate requests per render.
- **Server State**: Manage server state with React Query, SWR, or Apollo; remember that cache does not equal UI state.
- **URL**: Store filter and sort parameters in the URL as the source of truth.
- **Immutability**: Never mutate state directly; use spread operators or Immer.

## Anti-Patterns

- **No Prop Drilling > 2**: Avoid prop drilling beyond two levels; use Context or composition instead.
- **No Mirroring Refs**: Do not copy props to state.
- **No Multi-Source**: Maintain a single source of truth.
- **No Context Abuse**: Be cautious with Context as it can cause full-tree re-renders.

## Code Examples

```tsx
// Derived State (Efficient)
function List({ items, filter }) {
  // Correct: Calculated on the fly
  const visible = items.filter((i) => i.includes(filter));
  return (
    <ul>
      {visible.map((i) => (
        <li key={i}>{i}</li>
      ))}
    </ul>
  );
}

// Zustand (Global)
const useStore = create((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
}));
```

## Related Topics

hooks | component-patterns | performance