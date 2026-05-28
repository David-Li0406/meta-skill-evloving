---
name: remixjs-best-practices
description: Use this skill when you want to implement best practices for building scalable applications with Remix, focusing on server-first data patterns and error handling.
---

# Remix Best Practices (2025-2026 Edition)

This skill outlines modern best practices for building scalable, high-performance applications with Remix, specifically focusing on the transition to React Router v7 and future-proofing for Remix v3.

## 🚀 Key Trends (2025+)

*   **React Router v7 is Remix:** All Remix features are now part of React Router v7. New projects should start with React Router v7.
*   **Server-First Mental Model:** Loaders and Actions run *only* on the server.
*   **"Future Flags" Adoption:** Always enable v7 future flags in `remix.config.js` or `vite.config.ts` to ensure smooth migration.
*   **Codemod Migration:** Use `npx codemod remix/2/react-router/upgrade` to migrate existing v2 apps.

## 🏗️ Architecture & Data Loading

### 1. Server-First Data Flow
Avoid client-side fetching (`useEffect`) unless absolutely necessary.
*   **Loaders:** Fetch data server-side.
*   **Actions:** Mutate data server-side.
*   **Components:** Render *what* the loader provides.

```typescript
// ✅ Good: Typed loader with single strict return
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const user = await getUser(request);
  if (!user) throw new Response("Unauthorized", { status: 401 });
  return json({ user });
};

// Component gets fully typed data
export default function Dashboard() {
  const { user } = useLoaderData<typeof loader>(); 
  return <h1>Hello, {user.name}</h1>;
}
```

### 2. Form Actions over `onClick`
Use HTML Forms (or Remix `<Form>`) for mutations. This works without JS and handles race conditions automatically.

```tsx
// ✅ Good: Descriptive, declarative mutation
<Form method="post" action="/update-profile">
  <button type="submit">Save</button>
</Form>
```

### 3. Progressive Enhancement
Design features to work without JavaScript first. Remix handles the "hydration" to make it interactive (SPA feel) automatically.

## 🛡️ Error Handling Patterns

### 1. Granular Error Boundaries
Do not rely solely on a root ErrorBoundary. Place boundaries in nested routes to prevent a partial failure from crashing the entire page.

```tsx
// routes/dashboard.tsx (Nested Route)
export function ErrorBoundary() {
  const error = useRouteError();
  return <div className="p-4 bg-red-50">Widget crashed: {error.message}</div>;
}
```

### 2. Expected vs. Unexpected Errors
Implement error handling strategies that differentiate between expected and unexpected errors to provide better user feedback and recovery options.