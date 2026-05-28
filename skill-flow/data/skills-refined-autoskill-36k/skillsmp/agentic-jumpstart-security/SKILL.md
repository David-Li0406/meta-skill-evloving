---
name: agentic-jumpstart-security
description: Security best practices for TanStack Start applications with React 19, Drizzle ORM, PostgreSQL, Stripe, OAuth, and AWS S3/R2. Use when writing secure code, implementing authentication, handling payments, protecting API endpoints, validating input, preventing XSS/CSRF/SQL injection, or when the user mentions security, vulnerabilities, or authentication.
---

# Security Best Practices

## Authentication & Authorization

### Session Management with Arctic OAuth

```typescript
// Always use the validateRequest utility for authentication
import { validateRequest } from "~/utils/auth";

const { user, session } = await validateRequest();
if (!user) {
  throw redirect({ to: "/unauthenticated" });
}
```

### Middleware Protection Patterns

Always protect server functions with appropriate middleware:

```typescript
import { createServerFn } from "@tanstack/react-start";
import { authenticatedMiddleware, adminMiddleware, unauthenticatedMiddleware } from "~/lib/auth";

// For authenticated-only endpoints
export const protectedFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .handler(async ({ context }) => {
    // context.userId is guaranteed to exist
  });

// For admin-only endpoints
export const adminOnlyFn = createServerFn()
  .middleware([adminMiddleware])
  .handler(async ({ context }) => {
    // Only admins can access
  });

// For public endpoints that may have user context
export const publicFn = createServerFn()
  .middleware([unauthenticatedMiddleware])
  .handler(async ({ context }) => {
    // context.userId may be undefined
  });
```

### Route Protection

```typescript
import { assertIsAdminFn } from "~/fn/auth";

export const Route = createFileRoute("/admin/settings")({
  beforeLoad: () => assertIsAdminFn(),
  component: AdminSettingsPage,
});
```

## Input Validation with Zod

Always validate all input with Zod schemas:

```typescript
import { z } from "zod";

export const updateUserFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .inputValidator(
    z.object({
      name: z.string().min(1).max(100),
      email: z.string().email(),
      bio: z.string().max(500).optional(),
    })
  )
  .handler(async ({ data, context }) => {
    // data is fully validated and typed
    return updateUserUseCase(context.userId, data);
  });
```

### Common Validation Patterns

```typescript
// ID validation
const idSchema = z.number().int().positive();

// Slug validation
const slugSchema = z.string().regex(/^[a-z0-9-]+$/).min(1).max(100);

// Pagination
const paginationSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20),
});

// File upload validation
const fileSchema = z.object({
  name: z.string().max(255),
  size: z.number().max(500 * 1024 * 1024), // 500MB max
  type: z.string().refine((t) => ALLOWED_MIME_TYPES.includes(t)),
});
```

## SQL Injection Prevention

### Use Drizzle ORM Parameterized Queries

Drizzle ORM automatically parameterizes queries. Never use raw string concatenation:

```typescript
// GOOD: Parameterized query
const user = await database
  .select()
  .from(users)
  .where(eq(users.email, email))
  .limit(1);

// GOOD: Using SQL template literals for raw queries
import { sql } from "drizzle-orm";
const result = await database.execute(
  sql`SELECT * FROM users WHERE email = ${email}`
);

// BAD: Never do this
// const result = await database.execute(`SELECT * FROM users WHERE email = '${email}'`);
```

## XSS Prevention

### HTML Sanitization

Always sanitize user-generated HTML content:

```typescript
import sanitizeHtml from "sanitize-html";

const sanitizedContent = sanitizeHtml(userContent, {
  allowedTags: ["b", "i", "em", "strong", "a", "p", "br", "ul", "ol", "li"],
  allowedAttributes: {
    a: ["href", "target"],
  },
  allowedSchemes: ["http", "https"],
});
```

### React Escaping

React automatically escapes content, but be careful with:

```typescript
// DANGEROUS: Only use when content is trusted/sanitized
<div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />

// SAFE: React auto-escapes
<div>{userContent}</div>
```

## Stripe Payment Security

### Webhook Verification

Always verify Stripe webhooks:

```typescript
import Stripe from "stripe";

const stripe = new Stripe(env.STRIPE_SECRET_KEY);

export async function handleStripeWebhook(request: Request) {
  const body = await request.text();
  const signature = request.headers.get("stripe-signature");

  if (!signature) {
    throw new Error("Missing stripe signature");
  }

  // Verify the webhook signature
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    env.STRIPE_WEBHOOK_ENDPOINT_SECRET
  );

  // Process the verified event
  switch (event.type) {
    case "checkout.session.completed":
      await handleCheckoutComplete(event.data.object);
      break;
    // Handle other events...
  }
}
```

### Sensitive Data Handling

```typescript
// Never log full card numbers or sensitive payment data
console.log("Payment processed for customer:", customerId);
// NOT: console.log("Card:", cardNumber);

// Use Stripe's client-side library for card collection
// Never handle raw card data on your server
```

## File Upload Security

### Presigned URL Pattern

```typescript
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { PutObjectCommand } from "@aws-sdk/client-s3";

export async function getUploadUrl(
  userId: number,
  fileName: string,
  contentType: string
) {
  // Validate content type
  const allowedTypes = ["image/jpeg", "image/png", "video/mp4"];
  if (!allowedTypes.includes(contentType)) {
    throw new Error("Invalid file type");
  }

  // Generate unique key with user ID for ownership
  const key = `uploads/${userId}/${Date.now()}-${fileName}`;

  const command = new PutObjectCommand({
    Bucket: env.R2_BUCKET_NAME,
    Key: key,
    ContentType: contentType,
  });

  const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 });
  return { url, key };
}
```

### File Validation

```typescript
const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB
const ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm"];
const ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

function validateFileUpload(file: { size: number; type: string }) {
  if (file.size > MAX_FILE_SIZE) {
    throw new Error("File too large");
  }

  const allAllowedTypes = [...ALLOWED_VIDEO_TYPES, ...ALLOWED_IMAGE_TYPES];
  if (!allAllowedTypes.includes(file.type)) {
    throw new Error("Invalid file type");
  }
}
```

## Environment Variables

### Secure Configuration

```typescript
// src/utils/env.ts - Centralized environment validation
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_ENDPOINT_SECRET: z.string().startsWith("whsec_"),
  GOOGLE_CLIENT_ID: z.string(),
  GOOGLE_CLIENT_SECRET: z.string(),
  R2_ACCESS_KEY_ID: z.string(),
  R2_SECRET_ACCESS_KEY: z.string(),
  BASE_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

### Gitignore Pattern

Ensure sensitive files are never committed:

```gitignore
.env
.env.local
.env.production
*.pem
*.key
```

## Cookie Security

```typescript
import { setCookie } from "vinxi/http";

setCookie("session", sessionId, {
  httpOnly: true,        // Prevent XSS access
  secure: true,          // HTTPS only in production
  sameSite: "lax",       // CSRF protection
  maxAge: 60 * 60 * 24 * 30, // 30 days
  path: "/",
});
```

## Error Handling

### Never Expose Internal Errors

```typescript
// Use PublicError for user-facing errors
export class PublicError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PublicError";
  }
}

// In handlers, catch and sanitize errors
try {
  await riskyOperation();
} catch (error) {
  if (error instanceof PublicError) {
    throw error; // Safe to expose
  }
  console.error("Internal error:", error);
  throw new PublicError("An unexpected error occurred");
}
```

## Rate Limiting

Consider implementing rate limiting for sensitive endpoints:

```typescript
// Track attempts by IP or user
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

function checkRateLimit(key: string, maxAttempts: number, windowMs: number) {
  const now = Date.now();
  const record = rateLimitMap.get(key);

  if (!record || record.resetAt < now) {
    rateLimitMap.set(key, { count: 1, resetAt: now + windowMs });
    return true;
  }

  if (record.count >= maxAttempts) {
    throw new PublicError("Too many requests. Please try again later.");
  }

  record.count++;
  return true;
}
```

## Security Checklist

- [ ] All server functions use appropriate middleware
- [ ] All input is validated with Zod schemas
- [ ] User-generated HTML is sanitized before rendering
- [ ] Stripe webhooks are signature-verified
- [ ] File uploads validate type and size
- [ ] Environment variables are validated at startup
- [ ] Cookies use httpOnly, secure, and sameSite flags
- [ ] Internal errors are not exposed to users
- [ ] Sensitive routes are protected with beforeLoad
- [ ] Database queries use parameterized queries (Drizzle ORM)
