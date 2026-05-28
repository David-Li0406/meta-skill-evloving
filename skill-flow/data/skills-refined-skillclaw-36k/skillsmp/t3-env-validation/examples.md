# Practical Examples

## Adding a New Environment Variable

### Step 1: Add to Schema

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    // ... existing vars

    // Add new variable
    STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
    STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),
  },
  experimental__runtimeEnv: process.env,
  // ...
});
```

### Step 2: Add to .env.example

```bash
# .env.example

# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### Step 3: Add to .env.local

```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_actual_key
STRIPE_WEBHOOK_SECRET=whsec_actual_secret
```

### Step 4: Use in Code

```typescript
// features/payments/server/stripe.ts
import { env } from "~/data/env/server";
import Stripe from "stripe";

export const stripe = new Stripe(env.STRIPE_SECRET_KEY, {
  apiVersion: "2023-10-16",
});
```

## Feature Flags

### Environment-Based Features

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    // Feature flags
    FEATURE_NEW_DASHBOARD: z
      .enum(["true", "false"])
      .optional()
      .default("false")
      .transform((val) => val === "true"),

    FEATURE_AI_ASSISTANT: z
      .enum(["true", "false"])
      .optional()
      .default("false")
      .transform((val) => val === "true"),

    FEATURE_EXPORT_PDF: z
      .enum(["true", "false"])
      .optional()
      .default("false")
      .transform((val) => val === "true"),
  },
  // ...
});
```

### Usage

```typescript
// app/dashboard/page.tsx
import { env } from "~/data/env/server";

export default function DashboardPage() {
  if (env.FEATURE_NEW_DASHBOARD) {
    return <NewDashboard />;
  }

  return <LegacyDashboard />;
}
```

## Database Configuration

### Multiple Database Support

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    // Primary database
    DATABASE_URL: z.string().url(),
    DATABASE_POOL_MIN: z.coerce.number().int().min(0).optional().default(2),
    DATABASE_POOL_MAX: z.coerce.number().int().min(1).optional().default(10),

    // Read replica (optional)
    DATABASE_READ_REPLICA_URL: z.string().url().optional(),

    // Redis cache
    REDIS_URL: z.string().url().optional(),
    REDIS_PREFIX: z.string().optional().default("app:"),
  },
  // ...
});
```

### Usage

```typescript
// lib/database.ts
import { env } from "~/data/env/server";

export const dbConfig = {
  connectionString: env.DATABASE_URL,
  pool: {
    min: env.DATABASE_POOL_MIN,
    max: env.DATABASE_POOL_MAX,
  },
};

export const readReplicaConfig = env.DATABASE_READ_REPLICA_URL
  ? { connectionString: env.DATABASE_READ_REPLICA_URL }
  : null;
```

## External API Configuration

### Multiple API Integrations

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    // OpenAI
    OPENAI_API_KEY: z.string().startsWith("sk-"),
    OPENAI_MODEL: z.string().optional().default("gpt-4"),

    // SendGrid
    SENDGRID_API_KEY: z.string().startsWith("SG."),
    SENDGRID_FROM_EMAIL: z.string().email(),
    SENDGRID_FROM_NAME: z.string().optional().default("App"),

    // Sentry
    SENTRY_DSN: z.string().url().optional(),
    SENTRY_ENVIRONMENT: z
      .enum(["development", "staging", "production"])
      .optional()
      .default("development"),
  },
  // ...
});
```

### Usage

```typescript
// lib/email.ts
import { env } from "~/data/env/server";
import sgMail from "@sendgrid/mail";

sgMail.setApiKey(env.SENDGRID_API_KEY);

export async function sendEmail(to: string, subject: string, html: string) {
  await sgMail.send({
    to,
    from: {
      email: env.SENDGRID_FROM_EMAIL,
      name: env.SENDGRID_FROM_NAME,
    },
    subject,
    html,
  });
}
```

## Client-Side Configuration

### Analytics and Tracking

```typescript
// data/env/client.ts
export const env = createEnv({
  client: {
    NEXT_PUBLIC_GA_ID: z.string().startsWith("G-").optional(),
    NEXT_PUBLIC_POSTHOG_KEY: z.string().optional(),
    NEXT_PUBLIC_POSTHOG_HOST: z.string().url().optional(),
  },
  experimental__runtimeEnv: {
    NEXT_PUBLIC_GA_ID: process.env.NEXT_PUBLIC_GA_ID,
    NEXT_PUBLIC_POSTHOG_KEY: process.env.NEXT_PUBLIC_POSTHOG_KEY,
    NEXT_PUBLIC_POSTHOG_HOST: process.env.NEXT_PUBLIC_POSTHOG_HOST,
  },
  // ...
});
```

### Usage

```typescript
// components/analytics.tsx
"use client";

import { env } from "~/data/env/client";
import { GoogleAnalytics } from "@next/third-parties/google";

export function Analytics() {
  if (!env.NEXT_PUBLIC_GA_ID) {
    return null;
  }

  return <GoogleAnalytics gaId={env.NEXT_PUBLIC_GA_ID} />;
}
```

## Rate Limiting Configuration

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    // Rate limiting
    RATE_LIMIT_ENABLED: z
      .enum(["true", "false"])
      .optional()
      .default("true")
      .transform((val) => val === "true"),

    RATE_LIMIT_REQUESTS: z.coerce.number().int().positive()
      .optional()
      .default(100),

    RATE_LIMIT_WINDOW_SECONDS: z.coerce.number().int().positive()
      .optional()
      .default(60),

    RATE_LIMIT_SKIP_IPS: z.string().optional()
      .transform((val) => val?.split(",").map(s => s.trim()) ?? []),
  },
  // ...
});
```

### Usage

```typescript
// lib/rate-limit.ts
import { env } from "~/data/env/server";

export const rateLimitConfig = {
  enabled: env.RATE_LIMIT_ENABLED,
  requests: env.RATE_LIMIT_REQUESTS,
  windowSeconds: env.RATE_LIMIT_WINDOW_SECONDS,
  skipIps: env.RATE_LIMIT_SKIP_IPS,
};

export function shouldSkipRateLimit(ip: string): boolean {
  return rateLimitConfig.skipIps.includes(ip);
}
```

## Logging Configuration

```typescript
// data/env/server.ts
export const env = createEnv({
  server: {
    LOG_LEVEL: z
      .enum(["fatal", "error", "warn", "info", "debug", "trace"])
      .optional()
      .default("info"),

    LOG_FORMAT: z
      .enum(["json", "pretty"])
      .optional()
      .default("json"),

    LOG_INCLUDE_TIMESTAMP: z
      .enum(["true", "false"])
      .optional()
      .default("true")
      .transform((val) => val === "true"),
  },
  // ...
});
```

### Usage

```typescript
// lib/logger.ts
import { env } from "~/data/env/server";
import pino from "pino";

export const logger = pino({
  level: env.LOG_LEVEL,
  transport:
    env.LOG_FORMAT === "pretty"
      ? { target: "pino-pretty" }
      : undefined,
  timestamp: env.LOG_INCLUDE_TIMESTAMP
    ? pino.stdTimeFunctions.isoTime
    : false,
});
```

## Complete Server Configuration

```typescript
// data/env/server.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  server: {
    // Core
    NODE_ENV: z.enum(["development", "test", "production"]),

    // Build
    ANALYZE: z.enum(["true", "false"]).optional()
      .transform((val) => val === "true"),
    CI: z.enum(["true", "false", "0", "1"]).optional()
      .transform((val) => val === "true" || val === "1"),

    // Logging
    LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace"])
      .optional().default("info"),

    // Authentication
    CLERK_SECRET_KEY: z.string(),

    // Database
    FIREBASE_PROJECT_ID: z.string(),
    FIREBASE_CLIENT_EMAIL: z.string(),
    FIREBASE_PRIVATE_KEY: z.string(),

    // External Services
    VERCEL_URL: z.string().optional(),
  },

  experimental__runtimeEnv: process.env,
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});

// Type export for use elsewhere
export type ServerEnv = typeof env;
```

## Complete Client Configuration

```typescript
// data/env/client.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  client: {
    // Clerk (public keys only!)
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_IN_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL: z.string(),
    NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL: z.string(),
  },

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

// Type export for use elsewhere
export type ClientEnv = typeof env;
```
