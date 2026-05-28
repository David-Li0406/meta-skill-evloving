---
name: react-19-compiler
version: 1.0.0
lastUpdated: 2026-01-18
description: React 19 patterns and React Compiler optimization guidance. Understand when to use manual memoization vs letting the compiler optimize, and leverage new hooks like useActionState and useFormStatus.
tags: [react, react-19, react-compiler, memoization, useActionState, useFormStatus, server-components]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - When should I use useMemo with React Compiler enabled
  - How to use useActionState for form handling
  - Implement form with useFormStatus for pending state
  - Should I use React.memo with the compiler
---

# React 19 & React Compiler Skill

React 19 patterns and React Compiler optimization guidance for Next.js applications.

> **Reference Files:**
> - [compiler-guide.md](./compiler-guide.md) - React Compiler capabilities and optimization
> - [when-to-memoize.md](./when-to-memoize.md) - When manual memoization is still needed
> - [hooks.md](./hooks.md) - useActionState, useFormStatus patterns
> - [server-components.md](./server-components.md) - Server vs Client Components

## Project Configuration

This project has React Compiler enabled:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  experimental: {
    reactCompiler: true
  }
};
```

With React Compiler enabled, **you can safely remove most manual memoization** (`useMemo`, `useCallback`, `React.memo`).

## Quick Start

### Let the Compiler Optimize

```typescript
// ✅ Good - Let compiler handle optimization
function Component({ items, sortBy }) {
  const sorted = [...items].sort((a, b) => a[sortBy] - b[sortBy]);
  return <List items={sorted} />;
}

// ❌ Unnecessary with compiler
function Component({ items, sortBy }) {
  const sorted = useMemo(() => {
    return [...items].sort((a, b) => a[sortBy] - b[sortBy]);
  }, [items, sortBy]);
  return <List items={sorted} />;
}
```

### Form Handling with useActionState

```typescript
"use client";

import { useActionState } from "react";
import { submitForm } from "./actions";

function ContactForm() {
  const [error, submitAction, isPending] = useActionState(
    async (previousState, formData) => {
      const result = await submitForm(formData);
      if (!result.success) {
        return result.error;
      }
      return null;
    },
    null
  );

  return (
    <form action={submitAction}>
      <input type="text" name="message" />
      <SubmitButton />
      {error && <p className="text-red-500">{error}</p>}
    </form>
  );
}

// ✅ useFormStatus must be in child component
function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Sending..." : "Send"}
    </button>
  );
}
```

## Key Concepts

### React Compiler Benefits

The React Compiler:
- **Automatically memoizes** components and values at build time
- **Eliminates need** for manual `useMemo`, `useCallback`, `React.memo`
- **Identifies bottlenecks** and applies optimizations intelligently
- **Reduces boilerplate** and potential dependency-related bugs

### When Manual Memoization IS Still Needed

See [when-to-memoize.md](./when-to-memoize.md) for details. Key scenarios:

1. **External library callbacks** - Non-React code expecting stable references
2. **Complex context values** - When context updates trigger cascading re-renders
3. **Performance-critical loops** - Thousands of items with expensive computations

### New React 19 Hooks

| Hook | Purpose | Key Caveat |
|------|---------|------------|
| `useActionState` | Form state management | Accepts async action, returns `[state, action, isPending]` |
| `useFormStatus` | Form submission status | **Must be called from child component inside `<form>`** |
| `useOptimistic` | Optimistic UI updates | For instant feedback before server confirmation |

## File Locations

| Purpose | Location |
|---------|----------|
| Client components | `features/*/components/*.tsx` with `"use client"` |
| Server components | `app/**/*.tsx`, `features/*/components/*.tsx` (default) |
| Server actions | `features/*/server/actions/*.ts` |

## React Compiler Configuration

The compiler is enabled in `next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    reactCompiler: true
  }
};

export default nextConfig;
```

## Migration Checklist

When working on this codebase:

1. **Remove unnecessary memoization** - Let compiler handle it
2. **Keep memoization for external libs** - Document why it's needed
3. **Use useActionState for forms** - Replaces manual state + useTransition
4. **useFormStatus in child components** - Not in same component as form
5. **Default to Server Components** - Only add "use client" when needed

## Running and Testing

```bash
# Type check
npm run type-check

# Dev server (compiler active)
npm run dev

# Production build (full optimization)
npm run build
```

## Related Skills

- `server-actions` - For implementing server actions with React 19 patterns
- `storybook-testing` - For testing components with play functions
