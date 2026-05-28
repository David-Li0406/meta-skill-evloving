---
name: react-performance-optimization
description: Use this skill when you need to optimize the performance of React applications, addressing both client-side and server-side concerns.
---

# React Performance Optimization

## Activation Conditions

- Performance optimization tasks
- Component re-render issues
- Bundle size concerns
- Server-side rendering performance

## Strategies

### Elimination of Waterfalls (P0)

- **Parallel Data**: Use `Promise.all` for independent fetches. Avoid sequential `await`.
- **Preload**: Start fetches before render (in event handlers or route loaders).
- **Suspense**: Use Suspense boundaries to stream partial content.

### Bundle Optimization (P0)

- **No Barrel Files**: Import directly `import { Btn } from './Btn'` vs `import { Btn } from './components'`.
- **Lazy Load**: Use `React.lazy` / `next/dynamic` for heavy components (Charts, Modals).
- **Defer**: Load 3rd-party scripts (Analytics) after hydration.

### Rendering & Re-renders (P1)

- **Isolation**: Move state down. Isolate heavy UI updates.
- **Context Splitting**: Split Context into `StateContext` (Data) and `DispatchContext` (Actions) to prevent consumers from re-rendering just because they need a setter.
- **Stability**: Use `useMemo` for passing objects/arrays to children to preserve referential equality checks (`React.memo`).
- **Virtualization**: Use `react-window` for lists with more than 50 items.
- **Content Visibility**: Use `content-visibility: auto` for off-screen CSS content.
- **Static Hoisting**: Extract static objects/JSX outside component scope.
- **Transitions**: Use `startTransition` for non-urgent UI updates.

### Parallelization (P1)

- **Web Workers**: Move heavy computation (Encryption, Image processing, Large Data Sorting) off the main thread using `Comlink` or `Worker`.

### Server Performance (RSC) (P1)

- **Caching**: Use `React.cache` for per-request deduplication.
- **Serialization**: Minimize props passing to Client Components (only IDs/primitives).

## Anti-Patterns

- **No `export *`**: Breaks tree-shaking.
- **No Sequential Await**: Causes waterfalls.
- **No Inline Objects**: `style={{}}` breaks strict equality checks (if memoized).
- **No Heavy Libraries**: Avoid moment/lodash (use dayjs/radash).

## Code Examples

```tsx
// Parallel Fetching (Good)
const [user, posts] = await Promise.all([getUser(), getPosts()]);

// Bundle Optimized Import (Good)
import { Button } from './components/Button'; // Not from './components'

// Static Hoist (Good)
const STATIC_CONFIG = { /* configuration */ };
```