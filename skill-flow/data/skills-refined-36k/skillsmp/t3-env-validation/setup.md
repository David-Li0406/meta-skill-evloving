# Environment Validation Setup

## Project Structure

```
data/
└── env/
    ├── server.ts    # Server-only environment variables
    └── client.ts    # Public (NEXT_PUBLIC_) environment variables
```

## Server Environment File

```typescript
// data/env/server.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  server: {
    // Required
    NODE_ENV: z.enum(["development", "test", "production"]),

    // Optional with transform
    ANALYZE: z
      .enum(["true", "false"])
      .optional()
      .transform((value) => value === "true"),

    CI: z
      .enum(["true", "false", "0", "1"])
      .optional()
      .transform((value) => value === "true" || value === "1"),

    // Optional with default
    LOG_LEVEL: z
      .enum(["fatal", "error", "warn", "info", "debug", "trace"])
      .optional()
      .default("info"),

    // Third-party services
    CLERK_SECRET_KEY: z.string(),

    // Database
    FIREBASE_PROJECT_ID: z.string(),
    FIREBASE_CLIENT_EMAIL: z.string(),
    FIREBASE_PRIVATE_KEY: z.string(),

    // Optional
    VERCEL_URL: z.string().optional(),
  },

  // For App Router, use process.env directly
  experimental__runtimeEnv: process.env,

  // Skip validation in Docker builds
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,

  // Treat empty strings as undefined
  emptyStringAsUndefined: true,
});
```

## Client Environment File

```typescript
// data/env/client.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  client: {
    // All client vars must start with NEXT_PUBLIC_
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_IN_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL: z.string(),
  },

  // Must manually map each client variable
  experimental__runtimeEnv: {
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY:
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
    NEXT_PUBLIC_CLERK_SIGN_IN_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL,
    NEXT_PUBLIC_CLERK_SIGN_UP_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL,
    NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL,
    NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL,
    NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL:
      process.env.NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL,
  },

  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
```

## Configuration Options

### createEnv Options

| Option | Description | Required |
|--------|-------------|----------|
| `server` | Server-side variables schema | No |
| `client` | Client-side variables schema | No |
| `shared` | Variables used in both | No |
| `experimental__runtimeEnv` | Runtime env mapping | Yes |
| `skipValidation` | Bypass validation | No |
| `emptyStringAsUndefined` | Treat "" as undefined | No |
| `onValidationError` | Custom error handler | No |
| `onInvalidAccess` | Access control handler | No |

### experimental__runtimeEnv

For the App Router, you have two options:

**Option 1: Pass entire process.env (server only)**

```typescript
// Only for server.ts
experimental__runtimeEnv: process.env,
```

**Option 2: Manual mapping (required for client)**

```typescript
// Required for client.ts
experimental__runtimeEnv: {
  NEXT_PUBLIC_VAR: process.env.NEXT_PUBLIC_VAR,
},
```

### skipValidation

Useful for CI/CD pipelines and Docker builds:

```typescript
skipValidation: !!process.env.SKIP_ENV_VALIDATION,
```

Usage:

```bash
# Build without validation
SKIP_ENV_VALIDATION=true npm run build
```

### emptyStringAsUndefined

```typescript
emptyStringAsUndefined: true,
```

Effects:

| .env Value | Without Option | With Option |
|------------|----------------|-------------|
| `VAR=""` | `""` (empty string) | `undefined` |
| `VAR=value` | `"value"` | `"value"` |
| (not set) | `undefined` | `undefined` |

## Environment Files

### .env.example (Template)

```bash
# .env.example
# Copy to .env.local and fill in values

# Application
NODE_ENV=development
LOG_LEVEL=info

# Clerk Authentication
CLERK_SECRET_KEY=sk_test_xxx
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/onboarding

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

### .env.local (Local Development)

```bash
# .env.local (git-ignored)
# Actual values for local development

CLERK_SECRET_KEY=sk_test_actual_key
# ... rest of values
```

### .env.test (Testing)

```bash
# .env.test
# Values for test environment

NODE_ENV=test
LOG_LEVEL=error
SKIP_ENV_VALIDATION=true
```

## Importing Environment Variables

### Server-Side Usage

```typescript
// In Server Components, Server Actions, API Routes
import { env } from "~/data/env/server";

export async function GET() {
  // Type-safe access
  const projectId = env.FIREBASE_PROJECT_ID;
  const logLevel = env.LOG_LEVEL;

  return Response.json({ status: "ok" });
}
```

### Client-Side Usage

```typescript
// In Client Components
"use client";

import { env } from "~/data/env/client";

export function ClerkProvider({ children }) {
  // Only NEXT_PUBLIC_ vars available
  const publishableKey = env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  return (
    <ClerkProviderBase publishableKey={publishableKey}>
      {children}
    </ClerkProviderBase>
  );
}
```

### Shared Variables

If you need variables in both server and client:

```typescript
// data/env/shared.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  shared: {
    NODE_ENV: z.enum(["development", "test", "production"]),
  },
  experimental__runtimeEnv: {
    NODE_ENV: process.env.NODE_ENV,
  },
});
```

## Type Safety

T3 Env provides full TypeScript support:

```typescript
import { env } from "~/data/env/server";

// Autocomplete works
env.FIREBASE_PROJECT_ID  // string
env.LOG_LEVEL            // "fatal" | "error" | "warn" | "info" | "debug" | "trace"
env.ANALYZE              // boolean | undefined
env.CI                   // boolean | undefined

// Type error if variable doesn't exist
env.NONEXISTENT_VAR  // ❌ Property 'NONEXISTENT_VAR' does not exist
```

## Validation Errors

When validation fails:

```
❌ Invalid environment variables:
  CLERK_SECRET_KEY: Required
  FIREBASE_PRIVATE_KEY: Expected string, received undefined
```

### Custom Error Handler

```typescript
export const env = createEnv({
  server: { /* ... */ },
  experimental__runtimeEnv: process.env,

  onValidationError: (error) => {
    console.error("❌ Invalid environment variables:");
    console.error(error.flatten().fieldErrors);
    throw new Error("Invalid environment variables");
  },
});
```
