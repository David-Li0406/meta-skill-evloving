# OWASP Top 10 Security Risks

Comprehensive guide to preventing the most critical web application security risks (OWASP Top 10 2021).

## Quick Reference

| Risk | Prevention | Priority |
|------|-----------|----------|
| A01 Broken Access Control | Implement proper authorization, deny by default | ⚠️ Critical |
| A02 Cryptographic Failures | Use TLS, strong algorithms, proper key management | ⚠️ Critical |
| A03 Injection | Parameterized queries, input validation, sanitization | ⚠️ Critical |
| A04 Insecure Design | Threat modeling, secure design patterns | 🟡 High |
| A05 Security Misconfiguration | Secure defaults, minimal surface, automation | 🟡 High |
| A06 Vulnerable Components | Dependency scanning, updates, SBOMs | 🟡 High |
| A07 Auth Failures | MFA, secure session management, rate limiting | ⚠️ Critical |
| A08 Data Integrity Failures | Digital signatures, integrity checks | 🟢 Medium |
| A09 Logging Failures | Comprehensive logging, monitoring, alerts | 🟢 Medium |
| A10 SSRF | Input validation, network segmentation, allowlists | 🟡 High |

## A01: Broken Access Control

**Risk:** Users can access resources or perform actions they shouldn't be authorized for.

### Prevention

```typescript
// ❌ Bad: No authorization check
app.delete('/users/:id', async (req, res) => {
  await deleteUser(req.params.id);
  res.json({ success: true });
});

// ✅ Good: Proper authorization
app.delete('/users/:id', requireAuth, async (req, res) => {
  const targetUserId = req.params.id;
  const currentUser = req.user;

  // Check if user can delete (only admins or self)
  if (currentUser.role !== 'admin' && currentUser.id !== targetUserId) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  await deleteUser(targetUserId);
  res.json({ success: true });
});
```

### Best Practices
- Deny by default, require explicit authorization
- Check authorization on every request
- Use RLS for database-level enforcement
- Don't expose object IDs directly (use UUIDs)
- Log access control failures

## A02: Cryptographic Failures

**Risk:** Sensitive data exposed due to weak or missing encryption.

### Prevention

```typescript
// ✅ Good: Proper encryption at rest
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const KEY = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex'); // 32 bytes

function encrypt(text: string): { encrypted: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const tag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString('hex'),
    tag: tag.toString('hex'),
  };
}

function decrypt(encrypted: string, ivHex: string, tagHex: string): string {
  const iv = Buffer.from(ivHex, 'hex');
  const tag = Buffer.from(tagHex, 'hex');
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, iv);

  decipher.setAuthTag(tag);

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}
```

### Best Practices
- Use TLS 1.3 for data in transit
- Use strong algorithms (AES-256-GCM, ChaCha20-Poly1305)
- Never roll your own crypto
- Store keys securely (KMS, vault)
- Use authenticated encryption
- Hash passwords with bcrypt/argon2

## A03: Injection

**Risk:** Attacker injects malicious code (SQL, NoSQL, OS commands, etc.).

### SQL Injection Prevention

```typescript
// ❌ Bad: String concatenation
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const query = `SELECT * FROM users WHERE name = '${name}'`;
  const users = await db.query(query);
  res.json(users);
});

// ✅ Good: Parameterized queries
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const users = await db.query('SELECT * FROM users WHERE name = $1', [name]);
  res.json(users);
});

// ✅ Good: ORM
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const users = await User.findAll({ where: { name } });
  res.json(users);
});
```

### NoSQL Injection Prevention

```typescript
// ❌ Bad: Direct query from user input
app.get('/users', async (req, res) => {
  const filter = req.query.filter; // Could be {"$gt": ""}
  const users = await db.collection('users').find(filter).toArray();
  res.json(users);
});

// ✅ Good: Validate and sanitize input
import { z } from 'zod';

const FilterSchema = z.object({
  name: z.string().optional(),
  email: z.string().email().optional(),
  age: z.number().int().positive().optional(),
});

app.get('/users', async (req, res) => {
  const result = FilterSchema.safeParse(req.query);

  if (!result.success) {
    return res.status(400).json({ error: 'Invalid filter' });
  }

  const users = await db.collection('users').find(result.data).toArray();
  res.json(users);
});
```

### Command Injection Prevention

```typescript
// ❌ Bad: Unsanitized user input in shell command
import { exec } from 'child_process';

app.get('/files', (req, res) => {
  const filename = req.query.file;
  exec(`ls -l ${filename}`, (error, stdout) => {
    res.send(stdout);
  });
});

// ✅ Good: Avoid shell commands, use libraries
import fs from 'fs/promises';
import path from 'path';

app.get('/files', async (req, res) => {
  const filename = req.query.file as string;

  // Validate filename
  if (!/^[a-zA-Z0-9_-]+$/.test(filename)) {
    return res.status(400).json({ error: 'Invalid filename' });
  }

  const filePath = path.join('/safe/directory', filename);
  const stats = await fs.stat(filePath);

  res.json({
    name: filename,
    size: stats.size,
    modified: stats.mtime,
  });
});
```

## A04: Insecure Design

**Risk:** Missing or ineffective security controls in design phase.

### Best Practices
- Threat modeling before implementation
- Secure by default
- Principle of least privilege
- Defense in depth
- Fail securely

## A05: Security Misconfiguration

**Risk:** Missing security hardening, unnecessary features enabled.

### Prevention Checklist
- [ ] Remove default accounts and credentials
- [ ] Disable directory listing
- [ ] Remove unnecessary features and services
- [ ] Keep software updated
- [ ] Implement security headers
- [ ] Configure error messages to not leak info
- [ ] Use infrastructure as code

```typescript
// ✅ Good: Secure Express configuration
import express from 'express';
import helmet from 'helmet';

const app = express();

// Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));

// Disable X-Powered-By header
app.disable('x-powered-by');

// Custom error handler (don't leak stack traces)
app.use((err, req, res, next) => {
  console.error(err.stack);

  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message,
  });
});
```

## A06: Vulnerable and Outdated Components

**Risk:** Using libraries with known vulnerabilities.

### Prevention

```bash
# Run security audits regularly
npm audit
pip-audit
cargo audit

# Keep dependencies updated
npm update
pip install --upgrade
cargo update

# Use dependency scanning in CI/CD
```

```yaml
# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run npm audit
        run: npm audit --audit-level=high
      - name: Run Snyk test
        run: npx snyk test
```

## A07: Identification and Authentication Failures

**Risk:** Broken authentication allowing attackers to compromise accounts.

### Prevention

```typescript
// ✅ Good: Rate limiting on auth endpoints
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body;

  // Verify credentials
  const user = await verifyCredentials(email, password);

  if (!user) {
    // Don't leak which field was wrong
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Check if MFA is enabled
  if (user.mfaEnabled) {
    const tempToken = generateTempToken(user.id);
    return res.json({ requiresMFA: true, tempToken });
  }

  const token = generateToken(user);
  res.json({ token });
});

// MFA verification
app.post('/verify-mfa', async (req, res) => {
  const { tempToken, code } = req.body;

  const userId = verifyTempToken(tempToken);
  if (!userId) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  const user = await getUserById(userId);
  const isValid = verifyMFACode(user.mfaSecret, code);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid code' });
  }

  const token = generateToken(user);
  res.json({ token });
});
```

## A08: Software and Data Integrity Failures

**Risk:** Untrusted code or data accepted without verification.

### Prevention

```typescript
// ✅ Good: Verify package integrity
{
  "name": "my-app",
  "dependencies": {
    "express": "4.18.2"
  },
  "integrity": {
    "express": "sha512-..."
  }
}

// ✅ Good: Verify signed JWTs
import jwt from 'jsonwebtoken';

function verifyToken(token: string): TokenPayload {
  try {
    const payload = jwt.verify(token, PUBLIC_KEY, {
      algorithms: ['RS256'],
      issuer: 'your-service',
    }) as TokenPayload;

    return payload;
  } catch (error) {
    throw new Error('Token verification failed');
  }
}

// ✅ Good: Verify file uploads
import crypto from 'crypto';

function verifyFileIntegrity(file: Buffer, expectedHash: string): boolean {
  const hash = crypto.createHash('sha256').update(file).digest('hex');
  return hash === expectedHash;
}
```

## A09: Security Logging and Monitoring Failures

**Risk:** Insufficient logging and monitoring preventing detection of breaches.

### Best Practices

```typescript
import { getLogger } from '@logtape/logtape';

const logger = getLogger(['security']);

// Log authentication events
app.post('/login', async (req, res) => {
  const { email } = req.body;

  logger.info('Login attempt', { email, ip: req.ip });

  const user = await verifyCredentials(email, req.body.password);

  if (!user) {
    logger.warn('Failed login attempt', {
      email,
      ip: req.ip,
      userAgent: req.headers['user-agent'],
    });

    return res.status(401).json({ error: 'Invalid credentials' });
  }

  logger.info('Successful login', {
    userId: user.id,
    email,
    ip: req.ip,
  });

  res.json({ token: generateToken(user) });
});

// Log authorization failures
function requireRole(role: string) {
  return (req, res, next) => {
    if (!req.user) {
      logger.warn('Unauthorized access attempt', {
        path: req.path,
        ip: req.ip,
      });

      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!req.user.roles.includes(role)) {
      logger.warn('Forbidden access attempt', {
        userId: req.user.id,
        requiredRole: role,
        userRoles: req.user.roles,
        path: req.path,
        ip: req.ip,
      });

      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Log security events
function logSecurityEvent(event: string, metadata: Record<string, any>) {
  logger.warn('Security event', { event, ...metadata });

  // Send to monitoring system
  monitoring.trackSecurityEvent(event, metadata);
}
```

## A10: Server-Side Request Forgery (SSRF)

**Risk:** Application fetches remote resources without validating user-supplied URL.

### Prevention

```typescript
// ❌ Bad: Unchecked URL fetching
app.post('/fetch-url', async (req, res) => {
  const url = req.body.url;
  const response = await fetch(url);
  const data = await response.text();
  res.send(data);
});

// ✅ Good: Validate and restrict URLs
import { z } from 'zod';
import { URL } from 'url';

const ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com'];
const BLOCKED_IPS = ['127.0.0.1', 'localhost', '0.0.0.0'];

function isUrlSafe(urlString: string): boolean {
  try {
    const url = new URL(urlString);

    // Only allow HTTPS
    if (url.protocol !== 'https:') {
      return false;
    }

    // Check domain allowlist
    if (!ALLOWED_DOMAINS.includes(url.hostname)) {
      return false;
    }

    // Block private/local IPs
    const hostname = url.hostname;
    if (
      BLOCKED_IPS.includes(hostname) ||
      hostname.startsWith('192.168.') ||
      hostname.startsWith('10.') ||
      hostname.startsWith('172.')
    ) {
      return false;
    }

    return true;
  } catch {
    return false;
  }
}

app.post('/fetch-url', async (req, res) => {
  const url = req.body.url;

  if (!isUrlSafe(url)) {
    return res.status(400).json({ error: 'Invalid or forbidden URL' });
  }

  const response = await fetch(url, {
    timeout: 5000,
    redirect: 'manual', // Don't follow redirects
  });

  const data = await response.text();
  res.send(data);
});
```

## Language-Specific Considerations

### TypeScript/Node.js
- Use `helmet` for security headers
- Validate all inputs with Zod
- Use prepared statements for databases
- Never use `eval()` or `Function()` with user input
- Sanitize HTML with DOMPurify

### Python
- Use parameterized queries (never f-strings for SQL)
- Validate with Pydantic
- Use `secrets` module for cryptography
- Enable type hints and mypy
- Use `html.escape()` for HTML output

### Rust
- Compiler prevents many vulnerabilities
- Still validate input at boundaries
- Use `sqlx` with compile-time checked queries
- Be careful with `unsafe` blocks
- Use `secrecy` crate for sensitive data

## Security Testing

```typescript
// Example security test
import { describe, it, expect } from 'vitest';

describe('Security Tests', () => {
  it('should prevent SQL injection', async () => {
    const maliciousInput = "' OR '1'='1";

    const response = await request(app)
      .get('/users')
      .query({ name: maliciousInput });

    expect(response.status).toBe(200);
    expect(response.body).toEqual([]); // Should return no users
  });

  it('should prevent unauthorized access', async () => {
    const response = await request(app)
      .delete('/users/other-user-id')
      .set('Authorization', `Bearer ${regularUserToken}`);

    expect(response.status).toBe(403);
  });

  it('should rate limit login attempts', async () => {
    for (let i = 0; i < 6; i++) {
      await request(app).post('/login').send({
        email: 'test@example.com',
        password: 'wrong',
      });
    }

    const response = await request(app).post('/login').send({
      email: 'test@example.com',
      password: 'wrong',
    });

    expect(response.status).toBe(429);
  });
});
```

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Security Headers](https://securityheaders.com/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
