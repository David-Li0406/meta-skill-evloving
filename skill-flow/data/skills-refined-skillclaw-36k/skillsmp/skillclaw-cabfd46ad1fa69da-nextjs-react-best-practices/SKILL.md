---
name: nextjs-react-best-practices
description: Use this skill when working with Next.js 16 and React 19 to implement best practices for performance, component organization, and code structure using TypeScript and Tailwind CSS.
---

# Next.js and React Best Practices

## Project Structure

This project uses Next.js 16 App Router with TypeScript and Tailwind CSS v4.

### Directory Conventions

- `app/` - App Router directory (routes, layouts, pages)
- `app/[route]/page.tsx` - Page components
- `app/[route]/layout.tsx` - Layout components
- `app/[route]/loading.tsx` - Loading UI
- `app/[route]/error.tsx` - Error boundaries
- `app/[route]/not-found.tsx` - 404 pages
- `app/api/` - API routes (Route Handlers)
- `components/` - Shared React components
- `components/[component]/[Component].test.tsx` - Component tests (colocated)
- `lib/` - Utility functions and helpers
- `lib/[util].test.ts` - Utility tests (colocated)
- `public/` - Static assets

## Component Patterns

### Server Components (Default)

Use Server Components by default. They run on the server, reducing client bundle size.

```tsx
// ✅ Server Component (default)
export default async function Page() {
  const data = await fetch('https://api.example.com/data');
  return <div>{/* render data */}</div>;
}
```

### Client Components

Use `'use client'` directive only when needed:
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect, useContext)
- Third-party libraries requiring client-side execution

```tsx
'use client';

import { useState } from 'react';

export default function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Component Organization

- Keep Server Components as the default.
- Extract interactive parts into small Client Components.
- Colocate related components in feature folders.

```tsx
// app/products/page.tsx (Server Component)
import ProductList from '@/components/products/ProductList';
import ProductFilters from '@/components/products/ProductFilters';

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <div>
      <ProductFilters /> {/* Client Component */}
      <ProductList products={products} /> {/* Server Component */}
    </div>
  );
}
```

## Codebase Conventions

### TypeScript & File Types

- Prefer TypeScript everywhere:
  - `.tsx` for React components
  - `.ts` for non-React logic (services, utilities, server actions)

### Tailwind Class Composition

- Prefer the local `cn(...)` helper for conditional class names.
- Avoid “computed Tailwind” like `` `bg-${color}-500` `` (Tailwind can’t see it reliably).

## Performance Optimization

### Server vs Client Components

- **Default to Server Components** for pages/layouts/data widgets.
- Use `"use client"` only for:
  - Local state / effects
  - Browser-only APIs (`window`, `localStorage`)
  - Event handlers (`onClick`, etc.)
- Keep client components as leaf nodes; pass in plain serializable props.

### Mutations: Prefer Server Actions

- Put server mutations in `src/app/actions/*` with `"use server"`.
- Authenticate early via `auth()`.
- If the mutation affects a server-rendered page, revalidate via `revalidatePath(...)`.

### Client-Side Performance

- Avoid unnecessary re-renders:
  - Don’t create new inline objects/arrays/functions in JSX unless needed.
  - Use `useCallback`/`useMemo` when it materially reduces renders.
  - Split large components; memoize leaf components when props are stable.
- Avoid long effect chains and “derived state” stored in state.