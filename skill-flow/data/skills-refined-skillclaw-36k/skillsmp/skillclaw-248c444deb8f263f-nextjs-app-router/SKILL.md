---
name: nextjs-app-router
description: Use this skill when building production-ready Next.js 14+ applications with the App Router, covering server/client components, routing, data fetching, and optimization techniques.
---

# Next.js App Router

This skill provides guidance on modern Next.js development using the App Router paradigm for building full-stack applications.

## Core Concepts

### Server vs Client Components

```tsx
// app/components/ServerComponent.tsx
// Server Components are the default - no "use client" directive
async function ServerComponent() {
  const data = await db.query('SELECT * FROM users');

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// app/components/ClientComponent.tsx
'use client';

import { useState } from 'react';

export function ClientComponent() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Rendering Modes

| Mode                  | Where        | When to Use                               |
| --------------------- | ------------ | ----------------------------------------- |
| **Server Components** | Server only  | Data fetching, heavy computation, secrets |
| **Client Components** | Browser      | Interactivity, hooks, browser APIs        |
| **Static**            | Build time   | Content that rarely changes               |
| **Dynamic**           | Request time | Personalized or real-time data            |
| **Streaming**         | Progressive  | Large pages, slow data sources            |

### File-Based Routing

#### Route Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   ├── loading.tsx     # Dashboard loading
│   └── [id]/
│       └── page.tsx    # /dashboard/[id]
├── api/
│   └── users/
│       └── route.ts    # API route handler
└── (marketing)/        # Route group (no URL segment)
    ├── about/
    │   └── page.tsx    # /about
    └── contact/
        └── page.tsx    # /contact
```

### Quick Start Example

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'Built with Next.js App Router',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

// app/page.tsx - Server Component by default
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 },
  });
  const products = await res.json();
  return products;
}
```