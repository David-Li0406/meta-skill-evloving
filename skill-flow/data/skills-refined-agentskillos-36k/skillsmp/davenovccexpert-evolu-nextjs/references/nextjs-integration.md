# Next.js Integration

Best practices for Next.js App Router integration with Evolu.

## Architecture Overview

```
app/
├── layout.tsx          # Server Component - imports Providers
├── providers.tsx       # Client Component - EvoluProvider + Suspense
├── page.tsx            # Server Component - renders Client Components
└── components/
    └── TodoApp.tsx     # Client Component - uses Evolu
```

## Complete Setup

### 1. Providers (Client Component)

```tsx
// app/providers.tsx
"use client";

import { EvoluProvider, evolu } from "@/lib/evolu";
import { Suspense } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <EvoluProvider value={evolu}>
      <Suspense fallback={<LoadingSpinner />}>
        {children}
      </Suspense>
    </EvoluProvider>
  );
}
```

### 2. Layout (Server Component)

```tsx
// app/layout.tsx
import { Providers } from "./providers";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 3. Page (Server Component)

```tsx
// app/page.tsx
import { TodoApp } from "@/components/TodoApp"; // Client Component

export default function Page() {
  return (
    <main>
      <h1>My Todos</h1>
      <TodoApp /> {/* Client Component with Evolu */}
    </main>
  );
}
```

### 4. Evolu Component (Client Component)

```tsx
// components/TodoApp.tsx
"use client";

import { useQuery } from "@evolu/react";
import { todosQuery } from "@/lib/evolu";

export function TodoApp() {
  const { rows } = useQuery(todosQuery);

  // Data is loaded client-side after hydration
  // Suspense handles the loading state
  return (
    <ul>
      {rows.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

## Key Considerations

| Consideration | Guidance |
|---------------|----------|
| Client-side only | Evolu runs entirely client-side (local-first) |
| No SSR data | No server-side data fetching for Evolu data |
| Suspense required | Use Suspense boundaries for loading states |
| Component composition | Server Components can render Client Components that use Evolu |

## Hydration Issues

If you see hydration errors with Evolu:

1. Ensure all Evolu code is in Client Components (`"use client"`)
2. Use Suspense boundaries to handle loading states
3. Consider `next/dynamic` with `ssr: false` for problematic components:

```tsx
import dynamic from "next/dynamic";

const TodoApp = dynamic(
  () => import("@/components/TodoApp").then((mod) => mod.TodoApp),
  { ssr: false }
);
```
