---
name: react-hooks-components
description: Guidelines for React Hooks, memoization, and component composition.
---

# React Hooks & Components

## When to use this skill
- Creating functional components.
- Designing custom hooks.
- optimizing re-renders.

## 1. Hooks Rules
- **Top Level**: Only call hooks at the top level of the component/hook.
- **Dependencies**: Be honest with dependency arrays in `useEffect`, `useCallback`, and `useMemo`. Use linter to enforce.

## 2. Memoization
- **UseMemo/UseCallback**: Use only when the calculation is expensive OR when passing functions/objects as props to memoized children. Over-memoization adds overhead.
- **Stable References**: Remember that objects/arrays defined inside component body are new references every render.

## 3. Component Composition
- **Props**: Pass `children` (slots) instead of prop drilling complex state.
- **Container/Presenter**: Separate logic (data fetching) from UI rendering where complex.

## 4. State Management
- **Local vs Global**: Keep state as local as possible. Move up only when siblings need to share it.
- **Context**: Use Context for low-velocity global data (theme, user). For high-velocity data, use a signal-based library or optimized subscriber pattern.
