# Server vs Client Components

## Overview

Next.js App Router uses React Server Components by default. Understanding when to use Server vs Client Components is crucial.

## Server Components (Default)

Server Components render on the server and send HTML to the client.

### Benefits
- Zero JavaScript sent to client
- Direct database/filesystem access
- Secrets stay on server
- Better SEO and initial load

### Use When
- Fetching data
- Accessing backend resources
- Keeping sensitive info on server
- Large dependencies that don't need interactivity

```tsx
// app/posts/page.tsx - Server Component (default)
import { db } from "@/db";

export default async function PostsPage() {
  const posts = await db.query.posts.findMany();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

## Client Components

Client Components render on the client with JavaScript interactivity.

### Benefits
- Event handlers (onClick, onChange)
- useState, useEffect, useReducer
- Browser APIs
- Custom hooks with state

### Use When
- Interactive UI (buttons, forms, modals)
- Using browser APIs (localStorage, geolocation)
- Using React hooks with state
- Third-party libraries that need client context

```tsx
// components/counter.tsx - Client Component
"use client";

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Decision Tree

```
Does it need interactivity (onClick, useState)?
├── Yes → Client Component ("use client")
└── No
    ├── Does it fetch data?
    │   └── Yes → Server Component
    ├── Does it access backend directly?
    │   └── Yes → Server Component
    └── Is it purely presentational?
        └── Server Component (default)
```

## Composition Patterns

### Server Component with Client Children

```tsx
// app/page.tsx (Server)
import { Counter } from "@/components/counter";

export default async function Page() {
  const data = await fetchData();

  return (
    <div>
      <h1>Server rendered: {data.title}</h1>
      <Counter /> {/* Client component */}
    </div>
  );
}
```

### Passing Server Data to Client

```tsx
// app/page.tsx (Server)
import { ClientComponent } from "@/components/client";

export default async function Page() {
  const data = await fetchData();

  return <ClientComponent initialData={data} />;
}

// components/client.tsx
"use client";

export function ClientComponent({ initialData }) {
  const [data, setData] = useState(initialData);
  // ...
}
```

### Children Pattern (Donut Pattern)

```tsx
// components/modal.tsx
"use client";

import { useState } from "react";

export function Modal({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open</button>
      {isOpen && (
        <div className="modal">
          {children} {/* Server Components can be children */}
          <button onClick={() => setIsOpen(false)}>Close</button>
        </div>
      )}
    </>
  );
}

// app/page.tsx (Server)
import { Modal } from "@/components/modal";
import { ServerContent } from "@/components/server-content";

export default function Page() {
  return (
    <Modal>
      <ServerContent /> {/* Stays as Server Component */}
    </Modal>
  );
}
```

## Common Mistakes

### Don't: Use hooks in Server Components

```tsx
// WRONG
export default function Page() {
  const [count, setCount] = useState(0); // Error!
  return <div>{count}</div>;
}
```

### Don't: Import Server into Client

```tsx
// WRONG - components/client.tsx
"use client";

import { ServerComponent } from "./server"; // Error!

export function ClientComponent() {
  return <ServerComponent />;
}
```

### Do: Pass as children or props

```tsx
// CORRECT - app/page.tsx (Server)
import { ClientWrapper } from "@/components/client-wrapper";
import { ServerContent } from "@/components/server-content";

export default function Page() {
  return (
    <ClientWrapper>
      <ServerContent />
    </ClientWrapper>
  );
}
```

## Third-Party Libraries

Many libraries need "use client" wrapper:

```tsx
// components/chart-wrapper.tsx
"use client";

import { Chart } from "some-chart-library";

export function ChartWrapper(props) {
  return <Chart {...props} />;
}
```

## Context Providers

Providers must be Client Components:

```tsx
// components/providers.tsx
"use client";

import { ThemeProvider } from "next-themes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class">
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  );
}

// app/layout.tsx (Server)
import { Providers } from "@/components/providers";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```
