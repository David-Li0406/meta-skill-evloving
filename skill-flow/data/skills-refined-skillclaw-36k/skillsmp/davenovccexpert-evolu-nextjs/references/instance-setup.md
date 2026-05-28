# Evolu Instance Setup

Create the Evolu instance and set up the React provider.

## lib/evolu.ts

```typescript
"use client";

import { createEvolu, createUseEvolu, EvoluProvider } from "@evolu/react";
import { evoluReactWebDeps } from "@evolu/react-web";
import {
  id,
  InferType,
  maxLength,
  NonEmptyString,
  nullOr,
  SqliteBoolean,
} from "@evolu/common";

// Schema definition
const TodoId = id("Todo");
type TodoId = InferType<typeof TodoId>;

const NonEmptyString100 = maxLength(100, NonEmptyString);
type NonEmptyString100 = InferType<typeof NonEmptyString100>;

const Schema = {
  todo: {
    id: TodoId,
    title: NonEmptyString100,
    isCompleted: nullOr(SqliteBoolean),
  },
};

// Create the Evolu instance with platform-specific dependencies
export const evolu = createEvolu(evoluReactWebDeps)(Schema, {
  name: "my-app-db", // Database name
  // Optional: sync server (defaults to free.evoluhq.com)
  // syncUrl: "wss://your-sync-server.com",
});

// Create typed hook for accessing evolu
export const useEvolu = createUseEvolu(evolu);

// Re-export for convenience
export { EvoluProvider };
export type { TodoId, NonEmptyString100 };
```

## Next.js App Router Setup

### app/providers.tsx

```tsx
"use client";

import { EvoluProvider, evolu } from "@/lib/evolu";
import { Suspense } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <EvoluProvider value={evolu}>
      <Suspense fallback={<div>Loading...</div>}>
        {children}
      </Suspense>
    </EvoluProvider>
  );
}
```

### app/layout.tsx

```tsx
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

## Important Notes

- The EvoluProvider and components using Evolu **must** be Client Components (`"use client"`)
- Suspense boundary is required because `useQuery` uses React Suspense
- The evolu instance should be created once and shared via context
