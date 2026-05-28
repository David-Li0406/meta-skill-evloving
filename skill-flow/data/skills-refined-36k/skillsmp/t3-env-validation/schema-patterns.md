# Zod Schema Patterns for Environment Variables

## String Validations

### Required String

```typescript
// Simple required string
API_KEY: z.string()

// With minimum length
API_SECRET: z.string().min(32, "API secret must be at least 32 characters")

// With exact length
ENCRYPTION_KEY: z.string().length(64, "Encryption key must be exactly 64 characters")

// With pattern
API_KEY_FORMAT: z.string().regex(/^sk_[a-z]+_[A-Za-z0-9]{32}$/, "Invalid API key format")
```

### Optional String

```typescript
// Optional (undefined if not set)
OPTIONAL_VAR: z.string().optional()

// Optional with default
REGION: z.string().optional().default("us-east-1")

// Optional but validated if present
WEBHOOK_SECRET: z.string().min(16).optional()
```

### URL Validation

```typescript
// Any valid URL
API_ENDPOINT: z.string().url()

// URL with specific protocol
DATABASE_URL: z.string().url().startsWith("postgresql://")

// URL with custom message
WEBHOOK_URL: z.string().url("Must be a valid webhook URL")

// Optional URL
FALLBACK_URL: z.string().url().optional()
```

### Email Validation

```typescript
ADMIN_EMAIL: z.string().email()
SUPPORT_EMAIL: z.string().email("Invalid support email address")
```

## Enum Validations

### Simple Enum

```typescript
NODE_ENV: z.enum(["development", "test", "production"])

LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace"])

ENVIRONMENT: z.enum(["local", "staging", "production"])
```

### Optional Enum with Default

```typescript
LOG_LEVEL: z
  .enum(["fatal", "error", "warn", "info", "debug", "trace"])
  .optional()
  .default("info")

CACHE_STRATEGY: z
  .enum(["memory", "redis", "none"])
  .optional()
  .default("memory")
```

## Boolean Transforms

Environment variables are always strings, so booleans need transformation.

### String to Boolean

```typescript
// "true" / "false"
FEATURE_ENABLED: z
  .enum(["true", "false"])
  .transform((val) => val === "true")

// Multiple truthy values
DEBUG_MODE: z
  .enum(["true", "false", "1", "0", "yes", "no"])
  .transform((val) => ["true", "1", "yes"].includes(val))

// Optional boolean
ANALYTICS_ENABLED: z
  .enum(["true", "false"])
  .optional()
  .transform((val) => val === "true")
```

### CI Environment Detection

```typescript
CI: z
  .enum(["true", "false", "0", "1"])
  .optional()
  .transform((value) => value === "true" || value === "1")
```

## Number Transforms

### String to Number

```typescript
// Integer
PORT: z.string().transform((val) => parseInt(val, 10))

// With validation
PORT: z.string()
  .transform((val) => parseInt(val, 10))
  .pipe(z.number().int().min(1).max(65535))

// Using coerce (simpler)
PORT: z.coerce.number().int().positive()

// Float
RATE_LIMIT: z.coerce.number().positive()

// Optional with default
TIMEOUT_MS: z.coerce.number().int().positive().optional().default(5000)
```

### Number Range

```typescript
// Port range
PORT: z.coerce.number().int().min(1024).max(65535)

// Percentage
SAMPLE_RATE: z.coerce.number().min(0).max(1)

// Positive integer
MAX_RETRIES: z.coerce.number().int().positive()
```

## Array and Object Patterns

### Comma-Separated List

```typescript
// "a,b,c" -> ["a", "b", "c"]
ALLOWED_ORIGINS: z
  .string()
  .transform((val) => val.split(",").map(s => s.trim()))
  .pipe(z.array(z.string().url()))

// Optional with default
CORS_ORIGINS: z
  .string()
  .optional()
  .default("http://localhost:3000")
  .transform((val) => val.split(",").map(s => s.trim()))
```

### JSON String

```typescript
// Parse JSON config
CONFIG_JSON: z
  .string()
  .transform((val) => JSON.parse(val))
  .pipe(z.object({
    maxItems: z.number(),
    enableFeature: z.boolean(),
  }))
```

## Special Patterns

### Firebase Private Key

```typescript
// Firebase private key comes with escaped newlines
FIREBASE_PRIVATE_KEY: z.string().transform((key) => {
  // Replace escaped newlines with actual newlines
  return key.replace(/\\n/g, "\n");
})
```

### Base64 Encoded

```typescript
// Base64 secret
JWT_SECRET: z.string().transform((val) => Buffer.from(val, "base64"))

// Validate base64 format first
ENCODED_CONFIG: z
  .string()
  .regex(/^[A-Za-z0-9+/]+=*$/, "Invalid base64")
  .transform((val) => Buffer.from(val, "base64").toString())
```

### Duration String

```typescript
// "30s", "5m", "1h" -> milliseconds
CACHE_TTL: z.string().transform((val) => {
  const match = val.match(/^(\d+)(s|m|h)$/);
  if (!match) throw new Error("Invalid duration format");

  const [, num, unit] = match;
  const multipliers = { s: 1000, m: 60000, h: 3600000 };
  return parseInt(num) * multipliers[unit as keyof typeof multipliers];
})
```

## Conditional Validation

### Required in Production

```typescript
// Required only in production
SENTRY_DSN: z.string().url().optional().refine(
  (val) => process.env.NODE_ENV !== "production" || val !== undefined,
  "SENTRY_DSN is required in production"
)
```

### Dependent Variables

```typescript
// If one is set, both must be set
const env = createEnv({
  server: {
    REDIS_HOST: z.string().optional(),
    REDIS_PORT: z.coerce.number().optional(),
  },
  experimental__runtimeEnv: process.env,
}).refine(
  (env) => {
    if (env.REDIS_HOST && !env.REDIS_PORT) return false;
    if (env.REDIS_PORT && !env.REDIS_HOST) return false;
    return true;
  },
  "REDIS_HOST and REDIS_PORT must both be set or both be unset"
);
```

## Complete Example

```typescript
// data/env/server.ts
import { z } from "zod";
import { createEnv } from "@t3-oss/env-nextjs";

export const env = createEnv({
  server: {
    // Application
    NODE_ENV: z.enum(["development", "test", "production"]),
    LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace"])
      .optional()
      .default("info"),

    // Feature flags
    ANALYZE: z.enum(["true", "false"]).optional()
      .transform((val) => val === "true"),
    DEBUG_MODE: z.enum(["true", "false"]).optional()
      .transform((val) => val === "true"),

    // Authentication
    CLERK_SECRET_KEY: z.string().startsWith("sk_"),
    JWT_SECRET: z.string().min(32),

    // Database
    DATABASE_URL: z.string().url().startsWith("postgresql://"),
    DATABASE_POOL_SIZE: z.coerce.number().int().min(1).max(100)
      .optional()
      .default(10),

    // Firebase
    FIREBASE_PROJECT_ID: z.string(),
    FIREBASE_CLIENT_EMAIL: z.string().email(),
    FIREBASE_PRIVATE_KEY: z.string()
      .transform((key) => key.replace(/\\n/g, "\n")),

    // External services
    REDIS_URL: z.string().url().optional(),
    SENTRY_DSN: z.string().url().optional(),

    // CORS
    ALLOWED_ORIGINS: z.string().optional()
      .default("http://localhost:3000")
      .transform((val) => val.split(",").map(s => s.trim())),

    // Rate limiting
    RATE_LIMIT_MAX: z.coerce.number().int().positive()
      .optional()
      .default(100),
    RATE_LIMIT_WINDOW_MS: z.coerce.number().int().positive()
      .optional()
      .default(60000),
  },

  experimental__runtimeEnv: process.env,
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
```
