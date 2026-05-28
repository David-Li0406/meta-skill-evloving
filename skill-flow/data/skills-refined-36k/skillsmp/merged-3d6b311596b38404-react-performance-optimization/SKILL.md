---
name: react-performance-optimization
description: Use this skill for optimizing performance in React applications, both client-side and server-side.
---

# React Performance Optimization

This skill provides strategies for optimizing performance in React applications, addressing client-side and server-side concerns.

## Activation Conditions

- Performance optimization tasks
- Component re-render issues
- Bundle size concerns
- Use of `useEffect` and `useMemo` patterns

## Optimization Strategies

### Elimination of Waterfalls (Priority: P0)

- **Parallel Data**: Use `Promise.all` for independent fetches. Avoid sequential `await`.
- **Preload**: Start fetches before render (in event handlers or route loaders).
- **Suspense**: Use Suspense boundaries to stream partial content.

### Bundle Optimization (Priority: P0)

- **No Barrel Files**: Import directly (e.g., `import { Btn } from './Btn'`).
- **Lazy Load**: Use `React.lazy` or `next/dynamic` for heavy components (e.g., Charts, Modals).
- **Defer**: Load third-party scripts (e.g., Analytics) after hydration.

### Rendering & Re-renders (Priority: P1)

- **Isolation**: Move state down to isolate heavy UI updates.
- **Context Splitting**: Split Context into `StateContext` (Data) and `DispatchContext` (Actions) to prevent unnecessary re-renders.
- **Stability**: Use `useMemo` for passing objects/arrays to children to preserve referential equality checks.
- **Virtualization**: Use `react-window` for lists with more than 50 items.
- **Content Visibility**: Use `content-visibility: auto` for off-screen CSS content.
- **Static Hoisting**: Extract static objects/JSX outside component scope.
- **Transitions**: Use `startTransition` for non-urgent UI updates.

### Parallelization (Priority: P1)

- **Web Workers**: Move heavy computations (e.g., Encryption, Image processing) off the main thread using `Comlink` or `Worker`.

### Server Performance (RSC) (Priority: P1)

- **Caching**: Use `React.cache` for per-request deduplication.
- **Serialization**: Minimize props passing to Client Components (only IDs/primitives).

## Anti-Patterns

- **No `export *`**: This breaks tree-shaking.
- **No Sequential Await**: This causes waterfalls.
- **No Inline Objects**: Using `style={{}}` breaks strict equality checks if memoized.
- **No Heavy Libraries**: Avoid using libraries like moment/lodash; prefer alternatives like dayjs/radash.

## Code Examples

```tsx
// Parallel Fetching (Good)
const [user, posts] = await Promise.all([getUser(), getPosts()]);

// Bundle Optimized Import (Good)
import { Button } from './components/Button'; // Not from './components'

// Static Hoist (Good)
const STATIC_CONFIG = { theme: 'dark' };
function Component() {
  return <div config={STATIC_CONFIG} />;
}
```

## Additional Resources

See `rules/` directory for detailed guidance on best practices.