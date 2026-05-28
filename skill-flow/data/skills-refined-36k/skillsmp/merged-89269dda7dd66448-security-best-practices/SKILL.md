---
name: security-best-practices
description: Use this skill for comprehensive application security, including OWASP Top 10, secrets management, and security testing patterns.
---

# Security Best Practices

This skill provides a comprehensive overview of application security patterns, including OWASP Top 10 vulnerabilities, secrets management, authentication, and security testing.

## When to Use

- Implementing authentication and authorization
- Securing APIs and web applications
- Managing secrets and credentials
- Conducting security reviews
- Setting up security testing
- Implementing encryption and data protection

## OWASP Top 10 Vulnerabilities and Mitigations

### 1. Injection Prevention

```typescript
// SQL Injection Prevention - Use parameterized queries
const safe = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### 2. Broken Authentication

```typescript
// Secure password hashing with Argon2
import argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,
    timeCost: 3,
    parallelism: 4,
  });
}
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
```

### 6. Cross-Site Scripting (XSS)

```typescript
// Sanitize HTML output using DOMPurify
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target'],
  });
}
```

### 7. Cross-Site Request Forgery (CSRF)

```typescript
// Use CSRF tokens
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.post('/api/transfer', csrfProtection, authenticate, async (req, res) => {
  await transferMoney(req.user.id, req.body.to, req.body.amount);
  res.json({ success: true });
});
```

### 8. Security Logging and Monitoring Failures

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### 9. Server-Side Request Forgery (SSRF)

```javascript
// Validate and sanitize user input to prevent SSRF
const url = req.body.url;
if (!isValidUrl(url)) {
  return res.status(400).json({ error: 'Invalid URL' });
}
```

### 10. Vulnerable and Outdated Components

```bash
npm audit --audit-level=high
npx snyk test
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
```

## Best Practices

- **Defense in Depth**: Implement multiple layers of security.
- **Secure Development Lifecycle**: Follow a structured approach to security throughout the development process.
- **Regular Security Testing**: Conduct regular security assessments, including penetration testing and vulnerability scanning.

## Resources

- OWASP: [https://owasp.org/](https://owasp.org/)
- OWASP Top 10: [https://owasp.org/Top10/](https://owasp.org/Top10/)
- CWE Top 25: [https://cwe.mitre.org/top25/](https://cwe.mitre.org/top25/)
- NIST Guidelines: [https://www.nist.gov/cybersecurity](https://www.nist.gov/cybersecurity)
- Security Headers: [https://securityheaders.com/](https://securityheaders.com/)
- SSL Labs: [https://www.ssllabs.com/](https://www.ssllabs.com/)