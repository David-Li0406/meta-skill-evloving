---
name: react-19
description: React 19.3+ patterns. Use for forms, async data, pre-rendering, transitions, refs, context, metadata.
---

# React 19.3+

## Avoid → Use

- `useState` + `onChange` for forms → `useActionState` → `examples/form-action.tsx`
- `await` in server components → pass promise, `use()` in client → `examples/use-server-promise.tsx`
- `forwardRef` → `ref` as prop
- `useCallback` / `useMemo` → compiler handles it
- `useContext` → `use(Context)`
- `Context.Provider` → `<Context value={}>`
- Manual state reset on prop change → `key` prop

## Patterns

- **Forms**: `useActionState(fn, init)` + `useOptimistic` + `useFormStatus` → `examples/form-action.tsx`
- **Pre-rendering**: `<Activity mode="hidden">` → `examples/activity-prerender.tsx`
- **Effect events**: `useEffectEvent()` for non-reactive logic in effects → `examples/effect-event.tsx`
- **Async data**: pass promise from server, unwrap with `use()` → `examples/use-server-promise.tsx`
- **ViewTransition**: wrap elements, use `startTransition()` + `addTransitionType()` → `examples/view-transition.tsx`
- **Mutations outside forms**: `useTransition` + Server Action → `examples/server-action-mutation.tsx`
- **Suspense**: `<Suspense fallback={...}>` wraps async components
- **Deferred value**: `useDeferredValue(value, initialValue)`
- **Request memoization**: `cache(async fn)` with `cacheSignal()`
- **Server Action**: `"use server"` + `revalidatePath()` / `revalidateTag()`
- **Metadata**: `<title>`, `<meta>`, `<link>` hoisted to `<head>`
- **Refs**: `ref` as prop, cleanup via return function

## Component structure

- One component per file
- Inner functions use arrow syntax: `const handleX = () => {}`


