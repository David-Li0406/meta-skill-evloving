---
name: security-review-and-audit
description: Use this skill for comprehensive security review and audit processes to identify vulnerabilities, review security configurations, and implement best practices.
---

# Security Review and Audit

## When to Use

Use this skill proactively when:
- Implementing authentication or authorization features
- Handling user input or file uploads
- Creating new API endpoints
- Managing sensitive data or credentials
- Integrating third-party APIs
- Conducting security audits and reviews

## Security Checklist (OWASP Top 10)

### 1. Injection Attacks

#### SQL Injection
```typescript
// ❌ Dangerous
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ Safe - Parameterized Query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

#### NoSQL Injection
```typescript
// ❌ Dangerous
db.users.find({ username: req.body.username });

// ✅ Safe
const username = validator.escape(req.body.username);
db.users.find({ username });
```

#### Command Injection
```typescript
// ❌ Dangerous
exec(`ping ${userInput}`);

// ✅ Safe
const { spawn } = require('child_process');
spawn('ping', [userInput]);
```

### 2. Broken Authentication

#### Password Storage
```typescript
import bcrypt from 'bcrypt';

// ✅ Hash Password
const saltRounds = 10;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// ✅ Verify Password
const isValid = await bcrypt.compare(password, hashedPassword);
```

#### JWT Security
```typescript
import jwt from 'jsonwebtoken';

// ✅ Generate Token
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// ✅ Verify Token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
} catch (error) {
  // Token invalid or expired
}
```

### 3. Sensitive Data Exposure

#### Data Encryption
```typescript
import crypto from 'crypto';

// ✅ Encrypt Sensitive Data
const algorithm = 'aes-256-gcm';
const key = crypto.scryptSync(password, 'salt', 32);
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update(text, 'utf8', 'hex');
encrypted += cipher.final('hex');
```

#### HTTPS Enforcement
```typescript
// ✅ Force HTTPS
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});
```

### 4. XML External Entity (XXE)

```typescript
// ✅ Disable External Entities
const parser = new DOMParser();
parser.setFeature('http://xml.org/sax/features/external-general-entities', false);
parser.setFeature('http://xml.org/sax/features/external-parameter-entities', false);
```

### 5. Broken Access Control

#### Permission Checks
```typescript
// ✅ Middleware for Permission Check
function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
}
```

### 6. Security Misconfiguration

#### Security Headers
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
}));
```

### 7. Cross-Site Scripting (XSS)

#### Input Validation and Output Encoding
```typescript
import DOMPurify from 'dompurify';
import validator from 'validator';

// ✅ Clean HTML
const clean = DOMPurify.sanitize(userInput);
```

### 8. Insecure Deserialization

```typescript
// ❌ Dangerous
const obj = eval(userInput);

// ✅ Safe
const obj = JSON.parse(userInput);
```

### 9. Using Components with Known Vulnerabilities

```bash
# ✅ Regularly Check for Vulnerabilities
npm audit
npm audit fix
```

### 10. Insufficient Logging and Monitoring

```typescript
import winston from 'winston';

// ✅ Structured Logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

## Security Review Report Format

```markdown
# Security Review Report

**File:** [path/to/file.ts]
**Review Date:** YYYY-MM-DD
**Reviewer:** security-reviewer

## Summary

- **Critical Issues:** X
- **High-Risk Issues:** Y
- **Medium-Risk Issues:** Z
- **Risk Level:** High / Medium / Low

## Critical Issues (Immediate Fix)

### 1. [Issue Title]
**Severity:** CRITICAL
**Category:** SQL Injection / XSS / Authentication / etc.
**Location:** `file.ts:123`

**Description:**
[Description of the vulnerability]

**Impact:**
[Consequences if exploited]

**Remediation:**
[Example of secure implementation]
```

## Deployment Security Checklist

- [ ] **Sensitive Data**: No hardcoding, all using environment variables
- [ ] **Input Validation**: All user inputs validated
- [ ] **SQL Injection**: All queries parameterized
- [ ] **XSS**: User content sanitized
- [ ] **CSRF**: Protection enabled
- [ ] **Authentication**: Proper token handling
- [ ] **Authorization**: Role checks in place
- [ ] **Rate Limiting**: All endpoints enabled
- [ ] **HTTPS**: Enforced in production
- [ ] **Security Headers**: CSP, X-Frame-Options set
- [ ] **Dependencies**: Up-to-date and free of vulnerabilities

## Emergency Response

Upon discovering a CRITICAL vulnerability:

1. **Log** - Create a detailed report
2. **Notify** - Immediately alert the project owner
3. **Suggest Remediation** - Provide secure code examples
4. **Test Remediation** - Verify the fix is effective
5. **Rotate Secrets** - Change if there is a leak

## Related Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security Guide](https://nextjs.org/docs/security)
- [Supabase Security Guide](https://supabase.com/docs/guides/auth)