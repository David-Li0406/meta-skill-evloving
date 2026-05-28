---
name: nextjs-client-server-boundary-module-errors
description: |
  Fix Next.js 16 build errors "Module not found: Can't resolve 'dns', 'fs', 'net', 'tls'"
  when client components import constants from files that transitively import Node.js modules.
  Use when: (1) Build fails with Node.js module resolution errors in client components,
  (2) Error trace shows [Client Component Browser] importing from a utility file,
  (3) Constants or shared code in a file with database/Prisma/server imports.
  Solves client/server boundary violations by extracting shared constants to isolated files.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# Next.js 16 Client-Server Boundary Module Resolution Errors

## Problem

Next.js 16 build fails with errors like:
```
Module not found: Can't resolve 'dns'
Module not found: Can't resolve 'fs'
Module not found: Can't resolve 'net'
Module not found: Can't resolve 'tls'
```

The error trace shows:
```
Import trace:
  ./node_modules/.pnpm/pg@8.16.3/...
  ./packages/database/index.ts [Client Component Browser]
  ./apps/web/lib/utils/some-util.ts [Client Component Browser]
  ./apps/web/components/SomeClientComponent.tsx [Client Component Browser]
```

This happens when a client component (`"use client"`) imports constants or utilities from a file that transitively imports Node.js-only modules (like Prisma, database clients, or server-side libraries).

## Context / Trigger Conditions

**When this occurs:**
- Building Next.js 16 app with `next build` or `turbo build`
- Client component imports constants/types from a utility file
- That utility file also contains server-side functions that import database/Node.js modules
- The error mentions Node.js built-in modules: `dns`, `fs`, `net`, `tls`, `child_process`, etc.

**Why it happens:**
Next.js 16 enforces strict client/server boundaries. When you import ANY export from a file, the entire file gets bundled. If that file imports server-only modules (even if you're only using constants), those server imports try to resolve in the browser bundle and fail.

**Common scenarios:**
1. Constants defined alongside database utility functions
2. Type definitions in files that also import ORM clients
3. Enums/config objects in server action files
4. Shared validators in files with server-side imports

## Solution

### Step 1: Identify the Import Chain

Look at the error's import trace to find where the client component is pulling in server code:

```
./apps/web/lib/utils/preferences.ts [Client Component Browser]
./apps/web/components/NotificationPreferencesClient.tsx [Client Component Browser]
```

This tells you `preferences.ts` is being bundled for the browser because a client component imports from it.

### Step 2: Examine the Problematic File

Read the file that's causing issues (e.g., `lib/utils/preferences.ts`):

```typescript
// ❌ PROBLEM: Server imports in same file as constants
import { db, PreferenceCategory } from "database";  // Server-only!

export const EMAIL_NOTIFICATION_KEYS = {
  BOOKING: "email.notification.booking",
  // ...
};

export async function getEmailPreference(db: any, userId: string) {
  // Server-only function using db
}
```

The client component only needs `EMAIL_NOTIFICATION_KEYS`, but importing it pulls in the entire file including the `database` import.

### Step 3: Extract Constants to Separate File

Create a new constants-only file with NO server-side imports:

**New file:** `lib/constants/email-preferences.ts`
```typescript
/**
 * Email Preference Constants
 *
 * Shared constants for email notification preferences.
 * This file has no server-side dependencies and can be safely imported in client components.
 */

export const EMAIL_NOTIFICATION_KEYS = {
  BOOKING: "email.notification.booking",
  PAYMENT: "email.notification.payment",
  MESSAGING: "email.notification.messaging",
  VERIFICATION: "email.notification.verification",
} as const;

export type EmailNotificationKey =
  (typeof EMAIL_NOTIFICATION_KEYS)[keyof typeof EMAIL_NOTIFICATION_KEYS];

export const MESSAGING_COOLDOWN_MS = 60 * 60 * 1000;
```

### Step 4: Update Original Utility File

Import and re-export from the new constants file for backward compatibility:

**Modified:** `lib/utils/preferences.ts`
```typescript
import { db, PreferenceCategory } from "database";  // Server imports OK here
import {
  EMAIL_NOTIFICATION_KEYS,
  MESSAGING_COOLDOWN_MS,
  type EmailNotificationKey,
} from "@/lib/constants/email-preferences";  // Import from constants file

// Re-export for backward compatibility
export { EMAIL_NOTIFICATION_KEYS, MESSAGING_COOLDOWN_MS };
export type { EmailNotificationKey };

// Server-only functions remain here
export async function getEmailPreference(db: any, userId: string) {
  // ...
}
```

### Step 5: Update Client Component Imports

Change client component to import directly from constants file:

```typescript
"use client";

// ❌ Before: Imports from file with server dependencies
import { EMAIL_NOTIFICATION_KEYS } from "@/lib/utils/preferences";

// ✅ After: Imports from constants-only file
import { EMAIL_NOTIFICATION_KEYS } from "@/lib/constants/email-preferences";
```

### Step 6: Verify Fix

```bash
turbo build  # or next build
```

Build should succeed. The client component now imports from a file with no server dependencies.

## Verification

1. **Build succeeds**: `turbo build` or `next build` completes without module resolution errors
2. **Client bundle clean**: No Node.js modules in browser bundle
3. **Route renders**: The page using the client component renders correctly
4. **No runtime errors**: No "Module not found" errors in browser console

Check the build output for your route:
```
Route (app)
├ ◐ /[locale]/settings/notifications  ✓ Should show without errors
```

## Alternative Solutions

### Option 1: Turbopack resolveAlias (Workaround, Not Recommended)

You can configure Turbopack to load empty modules for Node.js built-ins:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      fs: { browser: './empty.ts' },
      dns: { browser: './empty.ts' },
      net: { browser: './empty.ts' },
      tls: { browser: './empty.ts' },
    },
  },
}

export default nextConfig
```

**Warning**: This is a workaround that masks the problem. The recommended approach is to refactor your code to respect client/server boundaries.

### Option 2: Duplicate Constants (Not Recommended)

Copying constants to both files works but creates maintenance burden:

```typescript
// lib/utils/preferences.ts (server)
export const EMAIL_NOTIFICATION_KEYS = { /* ... */ };

// lib/constants/email-preferences.ts (client)
export const EMAIL_NOTIFICATION_KEYS = { /* ... */ };  // Duplicate!
```

**Better**: Extract once and import from the shared location.

## Best Practices

### 1. Organize by Server/Client Capability

```
lib/
├── constants/          # Client-safe constants, types, enums (no server imports)
│   ├── email-preferences.ts
│   ├── routes.ts
│   └── validation-messages.ts
├── utils/              # Server-only utilities
│   ├── preferences.ts  # Can import database
│   └── auth.ts         # Can import server modules
└── shared/             # Truly universal utilities (no server or client-specific APIs)
    └── formatters.ts   # Pure functions only
```

### 2. Mark Constants Files Clearly

Add a comment banner to constants-only files:

```typescript
/**
 * Client-Safe Constants
 *
 * This file has no server-side dependencies and can be safely imported
 * in both server components and client components.
 *
 * DO NOT add imports from: database, fs, path, crypto, or any Node.js modules.
 */
```

### 3. Use Separate Barrel Exports

If you have many constants, create a barrel export:

```typescript
// lib/constants/index.ts
export * from './email-preferences';
export * from './routes';
export * from './validation';

// Client components import from barrel
import { EMAIL_NOTIFICATION_KEYS } from '@/lib/constants';
```

### 4. Validate Imports with ESLint

Consider using `eslint-plugin-no-server-import-in-page` or similar rules to catch these issues during development.

## Notes

- **This is specific to Next.js 16**: Earlier versions had looser boundaries
- **Applies to all client components**: Any file with `"use client"` directive
- **Transitive imports matter**: Even if your file doesn't directly import Node.js modules, if it imports from a file that does, you'll hit this issue
- **Server Components are safe**: Server Components can import from files with Node.js modules without issues
- **Type imports are usually safe**: `import type { ... }` statements are typically fine because they're erased at runtime, but mixed imports (`import { type X, Y }`) will still pull in the runtime code

## Common Mistakes

❌ **Mistake 1**: Adding `"use client"` to the utility file
```typescript
"use client";  // ❌ Doesn't fix the problem, makes it worse
import { db } from "database";
```

❌ **Mistake 2**: Using dynamic imports for constants
```typescript
// ❌ Overly complex, constants should be static imports
const keys = await import('@/lib/utils/preferences').then(m => m.EMAIL_NOTIFICATION_KEYS);
```

❌ **Mistake 3**: Ignoring the error with webpack fallbacks
```typescript
// ❌ Masks the problem, doesn't fix architecture
webpack: { resolve: { fallback: { fs: false } } }
```

✅ **Correct**: Extract constants to separate file with no server imports

## Example: Complete Refactor

**Before (broken):**
```
lib/utils/preferences.ts              <-- Has db imports
  - EMAIL_NOTIFICATION_KEYS           <-- Constants mixed with server code
  - getEmailPreference()              <-- Server function

components/NotificationClient.tsx     <-- "use client"
  - imports EMAIL_NOTIFICATION_KEYS   <-- ❌ Pulls in db imports
```

**After (fixed):**
```
lib/constants/email-preferences.ts    <-- NO server imports
  - EMAIL_NOTIFICATION_KEYS           <-- ✅ Pure constants

lib/utils/preferences.ts              <-- Has db imports
  - imports from constants file       <-- ✅ Uses constants, doesn't define them
  - re-exports for backward compat    <-- ✅ Existing code still works
  - getEmailPreference()              <-- Server function

components/NotificationClient.tsx     <-- "use client"
  - imports from constants file       <-- ✅ No server dependencies
```

## References

- [Next.js Module Not Found Error](https://nextjs.org/docs/messages/module-not-found)
- [Next.js "use client" Directive](https://nextjs.org/docs/app/api-reference/directives/use-client)
- [Fixing Module not found: Can't resolve 'fs' in Next.js | Sentry](https://sentry.io/answers/module-not-found-nextjs/)
- [How To Solve Module Not Found Can't Resolve 'fs' in Next.js](https://maikelveen.com/blog/how-to-solve-module-not-found-cant-resolve-fs-in-nextjs)
- [Next.js Server Components vs. Client Components: Best Practices | Medium](https://medium.com/@jigsz6391/next-js-server-components-vs-client-components-best-practices-2e735f4ad27c)
