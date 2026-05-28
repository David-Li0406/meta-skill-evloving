---
name: security-engineering
description: Use this skill when implementing application security measures, including OWASP Top 10 mitigations, secrets management, and security testing patterns.
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
const safe = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// Using ORM (Prisma)
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
  return iv.toString('hex') + ':' + encrypted;
}
```