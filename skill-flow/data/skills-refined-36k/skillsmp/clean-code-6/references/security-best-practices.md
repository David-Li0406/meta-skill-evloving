# Security Best Practices

## Core Principles

- **Defense in Depth**: Multiple layers of security
- **Least Privilege**: Grant minimum necessary permissions
- **Fail Secure**: Default to deny on errors
- **Never Trust Input**: Validate and sanitize everything

---

## Client-Side Security

### XSS Prevention

```tsx
// ❌ Dangerous - allows XSS
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ Safe - React escapes by default
<div>{userContent}</div>

// ✅ If HTML needed - sanitize first
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

### Link Security

Always add `rel="noopener"` for external links:

```tsx
<a href={externalUrl} target="_blank" rel="noopener noreferrer">
  External Link
</a>
```

### Never Use eval()

```typescript
// ❌ Never
eval(userInput);
new Function(userInput);
setTimeout(userInput, 0);

// ❌ Never manipulate cookies directly
document.cookie = userInput;
```

---

## Input Validation

### Client-Side (UX Only)

```typescript
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150),
  website: z.string().url().optional(),
});
```

### Server-Side (Security)

**Always validate on the server, even with client-side validation:**

```typescript
"use server";

import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function createUser(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get("email"),
    name: formData.get("name"),
  });

  if (!result.success) {
    throw new Error("Invalid input");
  }

  // Process valid data
  return await db.user.create({ data: result.data });
}
```

### Validation Rules

- **Allowlists**: Define what IS allowed, not what's blocked
- **Type Checking**: Verify data types match expectations
- **Length Limits**: Set min/max for strings, arrays
- **Format Validation**: Use regex for emails, URLs, etc.
- **Range Validation**: Check numeric bounds

---

## SQL Injection Prevention

### Use Parameterized Queries

```typescript
// ❌ Vulnerable to SQL injection
const users = await db.$queryRaw`
  SELECT * FROM users WHERE email = '${userEmail}'
`;

// ✅ Safe - parameterized
const users = await db.$queryRaw`
  SELECT * FROM users WHERE email = ${userEmail}
`;

// ✅ Even better - use Prisma Client
const users = await db.user.findMany({
  where: { email: userEmail },
});
```

---

## Secrets Management

### Environment Variables

```typescript
// ✅ Server-side only
const apiKey = process.env.API_KEY;

// ❌ Never expose in client
const apiKey = process.env.NEXT_PUBLIC_API_KEY; // Exposed!
```

### Next.js Patterns

```typescript
// app/api/route.ts - Server only
const secret = process.env.DATABASE_URL; // ✅ Safe

// components/Client.tsx - Client component
// process.env.DATABASE_URL is undefined here ✅
```

### What to Keep Server-Side

- Database credentials
- API keys
- JWT secrets
- Encryption keys
- Third-party service tokens

---

## HTTPS & Transport Security

### Enforce HTTPS

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Strict-Transport-Security",
            value: "max-age=31536000; includeSubDomains",
          },
        ],
      },
    ];
  },
};
```

---

## Content Security Policy

### Basic CSP

```typescript
// next.config.js
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data:;
  font-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
`;

module.exports = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Content-Security-Policy",
            value: cspHeader.replace(/\n/g, ""),
          },
        ],
      },
    ];
  },
};
```

---

## CSRF Protection

### Server Actions (Built-in)

Next.js Server Actions have built-in CSRF protection.

### API Routes

```typescript
// For custom API routes, verify origin
export async function POST(request: Request) {
  const origin = request.headers.get("origin");
  const allowedOrigins = [process.env.NEXT_PUBLIC_URL];

  if (!origin || !allowedOrigins.includes(origin)) {
    return new Response("Forbidden", { status: 403 });
  }

  // Process request
}
```

---

## Authentication

### Password Security

```typescript
import bcrypt from "bcrypt";

// Hash password before storing
const hashedPassword = await bcrypt.hash(password, 12);

// Verify password
const isValid = await bcrypt.compare(inputPassword, hashedPassword);
```

### Session Management

```typescript
// Use secure, HTTP-only cookies
cookies().set("session", sessionId, {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax",
  maxAge: 60 * 60 * 24 * 7, // 1 week
});
```

---

## File Upload Security

```typescript
export async function uploadFile(file: File) {
  // Validate file type
  const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
  if (!allowedTypes.includes(file.type)) {
    throw new Error("Invalid file type");
  }

  // Validate file size (5MB max)
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    throw new Error("File too large");
  }

  // Generate safe filename
  const safeFilename = `${crypto.randomUUID()}.${file.type.split("/")[1]}`;

  // Upload to storage
  await storage.upload(safeFilename, file);
}
```

---

## Rate Limiting

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
});

export async function POST(request: Request) {
  const ip = request.headers.get("x-forwarded-for") ?? "127.0.0.1";
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return new Response("Too Many Requests", { status: 429 });
  }

  // Process request
}
```

---

## Security Checklist

### Before Production

- [ ] HTTPS enforced
- [ ] CSP headers configured
- [ ] No secrets in client code
- [ ] All inputs validated server-side
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] CSRF protection enabled
- [ ] Rate limiting implemented
- [ ] Secure cookies configured
- [ ] Error messages don't leak info

---

## Anti-Patterns

| Pattern                   | Risk                | Solution                |
| ------------------------- | ------------------- | ----------------------- |
| `dangerouslySetInnerHTML` | XSS                 | Sanitize with DOMPurify |
| `eval()`                  | Code injection      | Never use               |
| String interpolation SQL  | SQL injection       | Parameterized queries   |
| Secrets in client         | Exposure            | Server-only env vars    |
| No HTTPS                  | MITM attacks        | Enforce HTTPS           |
| Missing CSP               | XSS, injection      | Configure headers       |
| Plain text passwords      | Data breach         | bcrypt hashing          |
| No rate limiting          | DoS, brute force    | Implement limits        |
| Verbose error messages    | Information leakage | Generic client errors   |
