---
name: security-review
description: Comprehensive security review workflow for identifying vulnerabilities
license: MIT
---

# Security Review Skill

Use this skill when conducting security audits or reviewing code for vulnerabilities.

## When to Use

- Before deploying to production
- After adding authentication/authorization
- When handling sensitive data
- Processing user input
- Integrating third-party services
- Regular security audits

## Security Review Checklist

### 1. Authentication

```typescript
// ❌ Bad: Plain text password comparison
if (password === user.password) { ... }

// ✅ Good: Secure hash comparison
import bcrypt from 'bcrypt';
if (await bcrypt.compare(password, user.passwordHash)) { ... }

// ❌ Bad: Weak JWT secret
const token = jwt.sign(payload, 'secret123');

// ✅ Good: Strong secret from environment
const token = jwt.sign(payload, process.env.JWT_SECRET, {
  expiresIn: '1h',
  algorithm: 'HS256',
});
```

### 2. Authorization

```typescript
// ❌ Bad: No authorization check
app.delete('/api/posts/:id', async (req, res) => {
  await db.posts.delete(req.params.id);
});

// ✅ Good: Verify ownership
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await db.posts.findById(req.params.id);
  
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  await db.posts.delete(req.params.id);
});
```

### 3. Input Validation

```typescript
// ❌ Bad: No validation
app.post('/api/users', (req, res) => {
  db.users.create(req.body);
});

// ✅ Good: Schema validation
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150).optional(),
});

app.post('/api/users', (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({ errors: result.error.issues });
  }
  db.users.create(result.data);
});
```

### 4. SQL Injection Prevention

```typescript
// ❌ Bad: String interpolation
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);

// ✅ Good: Parameterized query
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ✅ Good: ORM with escaping
const user = await db.users.findOne({
  where: { email },
});
```

### 5. XSS Prevention

```typescript
// ❌ Bad: Direct HTML injection
element.innerHTML = userInput;

// ✅ Good: Text content only
element.textContent = userInput;

// ✅ Good: Sanitize if HTML needed
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// React: Already safe by default
return <div>{userInput}</div>;

// ❌ Bad: dangerouslySetInnerHTML without sanitization
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Good: Sanitize first
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### 6. CSRF Protection

```typescript
// ✅ Good: CSRF token validation
import csrf from 'csurf';

app.use(csrf({ cookie: true }));

// Include token in forms
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// Token automatically validated on POST
app.post('/submit', (req, res) => {
  // CSRF token validated
});
```

### 7. Secrets Management

```typescript
// ❌ Bad: Hardcoded secrets
const API_KEY = 'sk_live_abc123xyz';
const DB_PASSWORD = 'password123';

// ✅ Good: Environment variables
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// ✅ Good: Validation at startup
if (!process.env.API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
```

### 8. Secure Headers

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
  },
}));
```

### 9. Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Global rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: 'Too many requests' },
});

app.use('/api/', limiter);

// Stricter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 attempts per hour
});

app.use('/api/auth/login', authLimiter);
```

### 10. File Upload Security

```typescript
import multer from 'multer';
import path from 'path';

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    
    // Check extension too (mimetype can be spoofed)
    const ext = path.extname(file.originalname).toLowerCase();
    if (!['.jpg', '.jpeg', '.png', '.gif'].includes(ext)) {
      return cb(new Error('Invalid file extension'));
    }
    
    cb(null, true);
  },
});
```

## Security Scan Commands

```bash
# Dependency vulnerabilities
npm audit
npm audit fix

# Secret scanning
npx gitleaks detect

# Static analysis
npx eslint --plugin security src/

# SAST scanning
npx semgrep --config auto
```

## Common Vulnerabilities (OWASP Top 10)

| Rank | Vulnerability | Prevention |
|------|---------------|------------|
| 1 | Broken Access Control | Verify permissions on every request |
| 2 | Cryptographic Failures | Use strong algorithms, secure storage |
| 3 | Injection | Parameterized queries, input validation |
| 4 | Insecure Design | Threat modeling, security requirements |
| 5 | Security Misconfiguration | Secure defaults, remove debug features |
| 6 | Vulnerable Components | Regular updates, dependency scanning |
| 7 | Auth Failures | MFA, secure session management |
| 8 | Data Integrity Failures | Verify signatures, validate inputs |
| 9 | Logging Failures | Log security events, monitor |
| 10 | SSRF | Validate URLs, allowlist destinations |

## Security Review Report Template

```markdown
## Security Review: [Component/Feature]

### Scope
- Files reviewed: X
- Lines of code: Y

### Findings

#### Critical 🔴
1. [Finding description]
   - Location: file:line
   - Impact: [What could happen]
   - Fix: [How to fix]

#### High ⚠️
...

#### Medium 💡
...

### Passed Checks ✅
- [ ] Authentication implemented correctly
- [ ] Authorization on all endpoints
- [ ] Input validation present
- [ ] No SQL injection vectors
- [ ] XSS prevention in place
- [ ] Secrets not in code
- [ ] Dependencies up to date

### Recommendations
1. [Action item]
2. [Action item]
```

## Resources

- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
