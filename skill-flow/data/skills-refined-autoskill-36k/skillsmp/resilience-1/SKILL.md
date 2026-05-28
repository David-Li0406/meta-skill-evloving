---
name: resilience
description: >
  Standardizes how the application handles asynchronous states, errors, and feedback using TanStack Query/Router patterns.
  Trigger: Apply when building async UIs to implement Suspense, Skeletons, and Error Boundaries instead of manual loading states.
license: Apache-2.0
metadata:
  author: jmgomezdev
  version: '1.0'
---

## 🧠 implementation Patterns

### 1. Data Loading (Read Operations)

- **Pattern:** **Suspense**.
- **Rule:** Components must NOT handle `isLoading` explicitly.
- **Action:**
  - Wrap Route Components (or parts of them) in `<Suspense fallback={<Skeleton />}>`.
  - Create granular Skeletons matching the UI layout (e.g., `ProductCardSkeleton`).

### 2. Route Errors (Page Level)

- **Pattern:** **Error Boundaries**.
- **Rule:** Loaders should usually throw errors to trigger the boundary.
- **Action:**
  - Define `errorComponent` in `createRoute`.
  - Handle `404 Not Found` (Typed errors) vs `500 Server Error` (Generic).
  - Provide "Retry" buttons using `router.invalidate()`.

### 3. Mutation Errors (Write Operations)

- **Pattern:** **Side Effects (Toasts)**.
- **Rule:** Do not crash the page on a failed form submission.
- **Action:**
  - Use `onError` in `useMutation` hook.
  - Trigger a Toast Notification (e.g., `toast.error("Failed to update product")`).
  - Keep the form data (do not reset) so the user can retry.

### 4. Code Example (Route Error)

```typescript
// interface/router/routes/products/detail.route.ts
export const productDetailRoute = createRoute({
  // ...
  errorComponent: ({ error, reset }) => {
    if (error.message.includes('404')) return <NotFoundPage />;
    return <ErrorPage error={error} retry={reset} />;
  },
  loader: async ({ context }) => {
     try {
       await context.queryClient.ensureQueryData(...);
     } catch (e) {
       // Transform API 404 to explicit error
       if (isAxios404(e)) throw new Error('404');
       throw e;
     }
  }
});
```

## Keywords

`suspense`, `error-boundary`, `skeletons`, `loading-state`, `404`, `500`, `toast`, `mutation-error`.
