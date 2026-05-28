---
name: security-engineering
description: Application security, OWASP Top 10, secrets management, and security testing patterns.
author: claude-code-ultimate
category: security
tags: [security, owasp, secrets, authentication, encryption]
license: MIT
version: 1.0.0
---

# Security Engineering

Comprehensive security patterns covering OWASP Top 10, secrets management, authentication, and security testing.

## When to Use

- Implementing authentication and authorization
- Securing APIs and web applications
- Managing secrets and credentials
- Conducting security reviews
- Setting up security testing
- Implementing encryption and data protection

## OWASP Top 10 Mitigations

### 1. Injection Prevention

```typescript
// SQL Injection Prevention - Use parameterized queries
// SAFE: Use parameterized queries
const safe = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// SAFE: Using ORM (Prisma)
const user = await prisma.user.findUnique({
  where: { id: userId }
});
```

### 2. Broken Authentication

```typescript
// Secure password hashing with Argon2
import argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4,
  });
}

async function verifyPassword(hash: string, password: string): Promise<boolean> {
  return argon2.verify(hash, password);
}

// Secure session configuration
import session from 'express-session';

app.use(session({
  name: '__Host-session', // Secure cookie prefix
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true, // HTTPS only
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
  },
}));

// Rate limiting for login
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
});

app.post('/login', loginLimiter, loginHandler);
```

### 3. Sensitive Data Exposure

```typescript
// Encrypt sensitive data at rest
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const KEY = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');

function encrypt(plaintext: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

// Mask sensitive data in logs
function maskSensitiveData(data: Record<string, any>): Record<string, any> {
  const sensitiveFields = ['password', 'ssn', 'creditCard', 'apiKey'];
  return Object.fromEntries(
    Object.entries(data).map(([key, value]) => {
      if (sensitiveFields.some(f => key.toLowerCase().includes(f))) {
        return [key, '***REDACTED***'];
      }
      return [key, value];
    })
  );
}
```

### 4. Broken Access Control

```typescript
// Role-based access control
type Role = 'admin' | 'user' | 'guest';

const requireRole = (...roles: Role[]) => {
  return async (c, next) => {
    const user = c.get('user');
    if (!user || !roles.includes(user.role)) {
      return c.json({ error: 'Forbidden' }, 403);
    }
    await next();
  };
};

// Resource ownership check
const requireOwnership = (resourceType: string) => {
  return async (c, next) => {
    const user = c.get('user');
    const resourceId = c.req.param('id');
    const resource = await db.findResource(resourceType, resourceId);
    if (!resource || resource.ownerId !== user.id) {
      return c.json({ error: 'Forbidden' }, 403);
    }
    c.set('resource', resource);
    await next();
  };
};
```

### 5. Security Misconfiguration

```typescript
// Secure HTTP headers with Helmet
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
}));

app.disable('x-powered-by');
```

### 6. XSS Prevention

```typescript
// Sanitize HTML output using DOMPurify
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target'],
  });
}

// React escapes content by default - prefer this:
<div>{userContent}</div>

// Always sanitize before rendering any HTML from user input
const cleanHtml = sanitizeHtml(userContent);
```

## Secrets Management

### Environment Variables

```typescript
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

export const env = envSchema.parse(process.env);
```

### AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretName: string): Promise<Record<string, string>> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  if (response.SecretString) {
    return JSON.parse(response.SecretString);
  }
  throw new Error('Secret not found');
}
```

## JWT Security

```typescript
import jwt from 'jsonwebtoken';

function generateAccessToken(payload: { userId: string; role: string }): string {
  return jwt.sign(payload, process.env.JWT_ACCESS_SECRET!, {
    expiresIn: '15m',
    algorithm: 'RS256',
    issuer: 'myapp',
    audience: 'myapp-users',
  });
}

function verifyAccessToken(token: string) {
  return jwt.verify(token, process.env.JWT_ACCESS_PUBLIC_KEY!, {
    algorithms: ['RS256'],
    issuer: 'myapp',
    audience: 'myapp-users',
  });
}
```

## Input Validation

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string()
    .min(12, 'Password must be at least 12 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  name: z.string().min(1).max(100),
});

function validateInput<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new ValidationError(result.error.flatten());
  }
  return result.data;
}
```

## Security Testing

### ESLint Security Plugins

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['security', 'no-secrets'],
  extends: ['plugin:security/recommended'],
  rules: {
    'security/detect-object-injection': 'error',
    'security/detect-unsafe-regex': 'error',
    'no-secrets/no-secrets': 'error',
  },
};
```

### Dependency Scanning

```bash
npm audit --audit-level=high
npx snyk test
```

## Source

This skill covers security best practices from OWASP and industry security standards.
