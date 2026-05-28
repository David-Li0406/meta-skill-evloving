---
name: react-19
description: Use this skill when writing React 19 components/hooks in .tsx, focusing on new patterns, hooks, and breaking changes from React 18.
---

# React 19 Patterns and Key Changes

This skill covers essential patterns and breaking changes introduced in React 19, including new hooks, server components, and best practices.

## General Guidelines

- **No Manual Memoization**: Rely on the React Compiler for optimization.
- **Named Imports**: Always use named imports instead of default imports.
- **Server Components First**: Use server components by default, only using client components when necessary.

## Key Changes from React 18

| Change | React 19 Status |
|--------|-----------------|
| `createRoot` / `hydrateRoot` | **Required** (ReactDOM.render removed) |
| Concurrent rendering | Foundation for all R19 features |
| Automatic batching | Default behavior |
| New hooks: `useId`, `useSyncExternalStore` | Stable, commonly used |
| Error Boundaries | Improved error callbacks |

### Migration Path

Upgrade to React 18.3 first to see deprecation warnings, then to 19.

## React 19 Mindset

| Old Thinking | New Thinking |
|--------------|--------------|
| Client-side by default | **Server-first** (RSC default) |
| Manual memoization | **Compiler handles it** |
| `useEffect` for data | **async Server Components** |
| `useState` for forms | **Form Actions** |

## New Hooks

### useActionState

```typescript
import { useActionState } from 'react';

function Form() {
  const [state, action, isPending] = useActionState(submitForm, null);
  return (
    <form action={action}>
      <button disabled={isPending}>
        {isPending ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

### use()

```typescript
import { use } from 'react';

function Comments({ promise }) {
  const comments = use(promise);
  return comments.map(c => <div key={c.id}>{c.text}</div>);
}
```

### useFormStatus

```typescript
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}
```

## Ref as Prop

In React 19, `ref` can be passed as a prop directly:

```typescript
function Input({ ref, ...props }) {
  return <input ref={ref} {...props} />;
}
```

## Document Metadata

Automatically manage document metadata in components:

```typescript
function BlogPost({ post }) {
  return (
    <article>
      <title>{post.title}</title>
      <meta name="description" content={post.excerpt} />
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

## Hydration Improvements

React 19 provides clearer error messages during hydration failures, showing a single error with a diff.

## Removed APIs

| Removed | Migration |
|---------|-----------|
| `ReactDOM.render()` | Use `createRoot().render()` |
| `ReactDOM.hydrate()` | Use `hydrateRoot()` |

## TypeScript Changes

- `useRef` requires an argument.
- Ref callbacks must not return values except for cleanup.

## Reference Documentation

- [paradigm-shifts.md](./references/paradigm-shifts.md)
- [anti-patterns.md](./references/anti-patterns.md)
- [new-hooks.md](./references/new-hooks.md)
- [deprecations.md](./references/deprecations.md)
- [typescript-changes.md](./references/typescript-changes.md)

This skill provides a comprehensive overview of React 19, focusing on new patterns, hooks, and best practices for building modern React applications.