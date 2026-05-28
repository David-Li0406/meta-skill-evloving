---
name: react-state-management
description: Use this skill when you need to manage local, global, and server state in a React application.
---

# React State Management

## **Priority: P0 (CRITICAL)**

Choosing the right tool for state scope.

## Implementation Guidelines

- **Local**: Use `useState`. Opt for `useReducer` if the state management is complex (state machine).
- **Derived**: Calculate derived state directly, e.g., `const fullName = first + last`. Avoid state synchronization.
- **Context**: Utilize for Dependency Injection (DI), theming, and authentication. Avoid for high-frequency data updates.
- **Global**: Use Zustand or Redux for managing complex app-wide state flows.
- **Server Cache**: Implement `React.cache` (RSC) to deduplicate requests per render.
- **Server State**: Use libraries like React Query, SWR, or Apollo for server state management. Remember, cache does not equal UI state.
- **URL**: Store filter and sort parameters in the URL as the source of truth.
- **Immutability**: Never mutate state directly. Use spread operators or libraries like Immer.

## Anti-Patterns

- **No Prop Drilling > 2**: Avoid prop drilling beyond two levels; use Context or composition instead.
- **No Mirroring Refs**: Do not copy props to state unnecessarily.
- **No Multi-Source**: Maintain a single source of truth for state.
- **No Context Abuse**: Be cautious with Context as it can lead to full-tree re-renders.

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

// Zustand (Global State Management)
const useStore = create((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
}));
```