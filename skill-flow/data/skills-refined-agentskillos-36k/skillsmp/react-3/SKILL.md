---
name: react
description:
  Writes React components and hooks using TypeScript. Use when creating or
  modifying React components, hooks, or JSX.
---

# React Protocol

## Component Structure

- Functional components only (no classes)
- No `import React from 'react'` — import individually
- Never use `React.*` namespace (e.g., `React.useState`, `React.ReactNode`)
- Export default in single expression
- No return types for components (TypeScript infers)

```tsx
// ✓ Good
import { useState, type ReactNode } from 'react';

export default function MyComponent() {
  return <div>Hello</div>;
}

// ✗ Bad
import React from 'react';
function MyComponent(): JSX.Element { ... }
export default MyComponent;
```

## Hooks

- `useState` generic only for unions/complex types (not for `string`, `boolean`,
  `number`)
- No `useCallback` for same-component functions
- `useCallback` acceptable for functions returned from custom hooks
- Named functions (not arrows) for async/complex logic inside hooks

```tsx
// ✓ Good
const [name, setName] = useState(''); // no generic needed
const [status, setStatus] = useState<'a' | 'b'>('a'); // union needs generic

useEffect(() => {
  async function fetchData() {
    const res = await fetch('/api');
  }
  void fetchData();
}, []);
```

## Other Rules

- Follow accessibility best practices
- `displayName` only for `forwardRef` components
- Fragment `<>` only for multiple siblings

```tsx
// ✓ forwardRef with displayName
const MyInput = forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
));
MyInput.displayName = 'MyInput';

// ✓ Fragment for siblings
return (
  <>
    <div>First</div>
    <div>Second</div>
  </>
);

// ✗ Unnecessary fragment
return (
  <>
    <div>Only child</div>
  </>
);
```
