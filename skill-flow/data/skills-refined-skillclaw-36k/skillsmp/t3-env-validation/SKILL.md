---
name: t3-env-validation
version: 1.0.0
lastUpdated: 2026-01-18
description: Type-safe environment variable validation with @t3-oss/env-nextjs and Zod. Build-time validation ensures all required env vars are present and correctly typed.
tags: [environment, validation, zod, type-safety, security, next.js]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to add a new environment variable
  - Validate optional env vars with defaults
  - Client-side vs server-side environment variables
  - Transform environment variable values
---

# T3 Env Validation Skill

Type-safe environment variable validation with @t3-oss/env-nextjs and Zod.

> **Reference Files:**
> - [setup.md](./setup.md) - Configuration patterns
> - [schema-patterns.md](./schema-patterns.md) - Common Zod validation patterns
> - [testing.md](./testing.md) - Mocking env vars in tests
> - [examples.md](./examples.md) - Practical examples

## Project Configuration

Environment variables are validated in two files:

| File | Purpose | Variables |
|------|---------|-----------|
| `data/env/server.ts` | Server-only vars | `CLERK_SECRET_KEY`, Firebase, etc. |
| `data/env/client.ts` | Public vars | `NEXT_PUBLIC_*` variables |

## Quick Start

### Adding Server Environment Variable

```typescript
// data/env/server.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  server: {
    // Add new variable
    DATABASE_URL: z.string().url(),
    API_SECRET: z.string().min(32),
  },
  experimental__runtimeEnv: process.env,
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
```

### Adding Client Environment Variable

```typescript
// data/env/client.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  client: {
    // Must be prefixed with NEXT_PUBLIC_
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  // Must manually map client vars
  experimental__runtimeEnv: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
```

### Usage in Code

```typescript
// Server-side (Server Components, Server Actions, API routes)
import { env } from "~/data/env/server";

const apiSecret = env.API_SECRET;  // Type-safe!

// Client-side (Client Components)
import { env } from "~/data/env/client";

const apiUrl = env.NEXT_PUBLIC_API_URL;  // Type-safe!
```

## Key Concepts

### Build-Time Validation

T3 Env validates environment variables at build time:

```
npm run build

❌ Invalid environment variables:
  CLERK_SECRET_KEY: Required
  FIREBASE_PROJECT_ID: Required
```

This prevents deploying with missing configuration.

### Server vs Client Variables

| Type | Prefix | Accessible In | Bundled |
|------|--------|---------------|---------|
| Server | None | Server Components, Actions, API | No |
| Client | `NEXT_PUBLIC_` | Everywhere | Yes (in JS bundle) |

**Security Rule:** Never put secrets in client variables!

### Empty String Handling

```typescript
emptyStringAsUndefined: true
```

With this setting:
- `VAR=""` is treated as undefined
- Required vars with empty string will fail validation
- Optional vars with empty string use default

## Common Patterns

### Required String

```typescript
API_KEY: z.string()
```

### Optional with Default

```typescript
LOG_LEVEL: z.enum(["debug", "info", "warn", "error"])
  .optional()
  .default("info")
```

### Boolean Transform

```typescript
FEATURE_FLAG: z
  .enum(["true", "false"])
  .optional()
  .transform((val) => val === "true")
```

### URL Validation

```typescript
API_URL: z.string().url()
DATABASE_URL: z.string().url().startsWith("postgresql://")
```

### Number Transform

```typescript
PORT: z.string().transform((val) => parseInt(val, 10))
TIMEOUT_MS: z.coerce.number().int().positive()
```

## File Locations

| Purpose | Location |
|---------|----------|
| Server env | `data/env/server.ts` |
| Client env | `data/env/client.ts` |
| Env template | `.env.example` |
| Local env | `.env.local` |

## Troubleshooting

### Build Fails with Missing Env

```bash
# Skip validation (for Docker builds)
SKIP_ENV_VALIDATION=true npm run build
```

### Variable Not Available

1. Server var → Can only be used in server code
2. Client var → Must be in `experimental__runtimeEnv`
3. Check spelling and `NEXT_PUBLIC_` prefix

### Type Errors

```typescript
// Import from correct file
import { env } from "~/data/env/server";  // For server vars
import { env } from "~/data/env/client";  // For client vars
```

## Related Skills

- `server-actions` - Using env vars in server actions
- `firebase-firestore` - Firebase env configuration
- `clerk-auth-proxy` - Clerk env configuration
