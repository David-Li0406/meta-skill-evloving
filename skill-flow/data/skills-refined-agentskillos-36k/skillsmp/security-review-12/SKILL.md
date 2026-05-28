---
name: security-review
description: Conduct comprehensive security code reviews covering OWASP Top 10, vulnerability assessment, secure coding practices, input validation, authentication, authorization, and data protection.
---

# Security Review

Complete framework for conducting security code reviews and identifying vulnerabilities before they reach production.

## When to Use

- Reviewing code before merging to production
- Auditing existing codebase for vulnerabilities
- Assessing third-party dependencies
- Preparing for security audits
- Training developers on secure coding
- Investigating security incidents

## OWASP Top 10 Security Risks

**Critical vulnerabilities to check for:**

1. **Injection** (SQL, Command, LDAP)
2. **Broken Authentication**
3. **Sensitive Data Exposure**
4. **XML External Entities (XXE)**
5. **Broken Access Control**
6. **Security Misconfiguration**
7. **Cross-Site Scripting (XSS)**
8. **Insecure Deserialization**
9. **Vulnerable Components**
10. **Insufficient Logging & Monitoring**

---

## Workflow

### Step 1: Risk Assessment

**Determine the security criticality:**

```markdown
## Security Risk Assessment: [Feature/PR]

**Data Sensitivity**:
- [ ] None (public data only)
- [ ] Low (non-sensitive user data)
- [ ] Medium (PII, email, phone)
- [ ] High (passwords, payment info)
- [ ] Critical (health records, financial data)

**Attack Surface**:
- [ ] Internal only (admin tools)
- [ ] Authenticated users
- [ ] Public (unauthenticated)

**Impact if Compromised**:
- [ ] Low (minor inconvenience)
- [ ] Medium (data leak, service disruption)
- [ ] High (financial loss, reputation damage)
- [ ] Critical (legal liability, major breach)

**Overall Risk Level**: [Low / Medium / High / Critical]
```

### Step 2: Input Validation Review

**Check all user input is validated:**

```markdown
## Input Validation Checklist

**Server-Side Validation**:
- [ ] All user input validated on server (never trust client)
- [ ] Validation uses allowlists, not blocklists
- [ ] Input length limits enforced
- [ ] Special characters properly handled
- [ ] File uploads validated (type, size, name)
- [ ] URL parameters sanitized
- [ ] JSON/XML parsed safely

**Specific Checks**:
- [ ] Email format validation
- [ ] Phone number format
- [ ] Date/time format
- [ ] Numeric ranges
- [ ] Enum values
```

**Example: Safe Input Validation**
```javascript
// ❌ VULNERABLE: Trusts client-side validation
app.post('/api/users', (req, res) => {
  const { email } = req.body;
  db.query(`INSERT INTO users (email) VALUES ('${email}')`);
});

// ✅ SECURE: Server-side validation + parameterized queries
const { z } = require('zod');

const userSchema = z.object({
  email: z.string().email().max(255),
  age: z.number().int().min(13).max(120)
});

app.post('/api/users', (req, res) => {
  // Validate input
  const result = userSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: result.error });
  }

  // Use parameterized query
  const { email, age } = result.data;
  db.query('INSERT INTO users (email, age) VALUES ($1, $2)', [email, age]);
});
```

### Step 3: Injection Prevention

**SQL Injection:**
```javascript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);

// ✅ SECURE: Parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);

// ✅ SECURE: ORM with prepared statements
const user = await User.findOne({ where: { email } });
```

**Command Injection:**
```javascript
// ❌ VULNERABLE
const { exec } = require('child_process');
exec(`convert ${filename} output.png`);

// ✅ SECURE: Use execFile (doesn't spawn shell)
const { execFile } = require('child_process');
execFile('convert', [filename, 'output.png']);

// ✅ BETTER: Use library that doesn't execute commands
const sharp = require('sharp');
await sharp(filename).toFile('output.png');
```

**Path Traversal:**
```javascript
// ❌ VULNERABLE
const filePath = `/uploads/${userInput}`;
fs.readFile(filePath);

// ✅ SECURE
const path = require('path');
const safeName = path.basename(userInput);
const filePath = path.join('/uploads', safeName);

// Verify it's within expected directory
const realPath = path.resolve(filePath);
if (!realPath.startsWith(path.resolve('/uploads'))) {
  throw new Error('Invalid path');
}
```

### Step 4: Authentication Review

```markdown
## Authentication Checklist

**Password Security**:
- [ ] Passwords hashed with bcrypt/argon2 (NOT md5/sha1)
- [ ] Minimum password requirements enforced
- [ ] No plain text passwords anywhere (code, logs, DB)
- [ ] Password reset is secure (token-based, time-limited)

**Session Management**:
- [ ] Session tokens are random and long (128+ bits)
- [ ] Sessions stored server-side
- [ ] Session invalidated on logout
- [ ] Session timeout implemented (30 min inactivity)
- [ ] Tokens use httpOnly and secure flags

**Brute Force Protection**:
- [ ] Rate limiting on login attempts
- [ ] Account lockout after X failed attempts
- [ ] CAPTCHA after multiple failures

**Multi-Factor Authentication**:
- [ ] MFA option available (TOTP, SMS, hardware key)
- [ ] Backup codes provided
```

**Example: Secure Password Hashing**
```javascript
const bcrypt = require('bcrypt');

// ❌ VULNERABLE
function hashPassword(password) {
  return crypto.createHash('md5').update(password).digest('hex');
}

// ✅ SECURE
async function hashPassword(password) {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}
```

### Step 5: Authorization Review

```markdown
## Authorization Checklist

**Access Control**:
- [ ] Authorization checked on EVERY request
- [ ] Authorization checked server-side (never client)
- [ ] Principle of least privilege applied
- [ ] No direct object references without auth check
- [ ] Admin functions properly protected
- [ ] Row-level security where needed (multi-tenant)

**Common Patterns**:
- [ ] Check user owns resource before modification
- [ ] Verify user role/permissions
- [ ] Prevent privilege escalation
```

**Example: Insecure Direct Object Reference (IDOR)**
```javascript
// ❌ VULNERABLE: Anyone can access any order
app.get('/api/orders/:id', (req, res) => {
  const order = db.getOrder(req.params.id);
  res.json(order);
});

// ✅ SECURE: Verify user owns the order
app.get('/api/orders/:id', requireAuth, (req, res) => {
  const order = db.getOrder(req.params.id);

  // Authorization check
  if (order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json(order);
});
```

### Step 6: XSS Prevention

**Cross-Site Scripting (XSS) Types:**

**Reflected XSS:**
```javascript
// ❌ VULNERABLE
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`);
});

// ✅ SECURE: Escape output
const escapeHtml = require('escape-html');
app.get('/search', (req, res) => {
  const query = escapeHtml(req.query.q);
  res.send(`<h1>Results for: ${query}</h1>`);
});
```

**Stored XSS:**
```javascript
// ❌ VULNERABLE: Storing unsan itized HTML
element.innerHTML = userInput;

// ✅ SECURE: Use textContent for text
element.textContent = userInput;

// ✅ SECURE: If HTML needed, sanitize first
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

**DOM-based XSS:**
```javascript
// ❌ VULNERABLE
const name = location.hash.substring(1);
document.write('Hello ' + name);

// ✅ SECURE
const name = location.hash.substring(1);
const safe = document.createTextNode('Hello ' + name);
document.body.appendChild(safe);
```

### Step 7: Data Protection

```markdown
## Data Protection Checklist

**Encryption**:
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS used for data in transit
- [ ] Encryption keys not in code
- [ ] Strong algorithms (AES-256, not DES)

**Secrets Management**:
- [ ] Secrets not in code or version control
- [ ] Secrets not in logs or error messages
- [ ] Environment variables or secrets manager used
- [ ] API keys rotated regularly

**PII Handling**:
- [ ] PII handled according to privacy policy
- [ ] Data retention policies followed
- [ ] Secure deletion when required
- [ ] Data minimization (collect only what's needed)
```

**Example: Secrets Management**
```javascript
// ❌ VULNERABLE
const API_KEY = 'sk_live_abc123...';  // Hardcoded!

// ✅ SECURE
const API_KEY = process.env.STRIPE_API_KEY;

// Validate secret is loaded
if (!API_KEY) {
  throw new Error('STRIPE_API_KEY environment variable not set');
}
```

### Step 8: Security Headers

**Essential Security Headers:**
```javascript
app.use((req, res, next) => {
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Enable XSS filter
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Control referrer information
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Content Security Policy (adjust for your app)
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );

  // HSTS (force HTTPS)
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains'
  );

  next();
});
```

### Step 9: Dependency Security

```markdown
## Dependency Security Checklist

**Vulnerability Scanning**:
- [ ] Run `npm audit` or `yarn audit` regularly
- [ ] Automated scanning in CI/CD
- [ ] Update dependencies monthly
- [ ] Pin dependency versions (avoid `^` or `~`)

**Supply Chain**:
- [ ] Review new dependencies before adding
- [ ] Check dependency maintainership
- [ ] Avoid packages with no recent updates
- [ ] Use lock files (package-lock.json, yarn.lock)
```

**Check for Vulnerabilities:**
```bash
# NPM
npm audit
npm audit fix

# Yarn
yarn audit
yarn upgrade-interactive --latest

# Python
pip-audit

# Ruby
bundler-audit
```

### Step 10: Logging & Monitoring

```markdown
## Logging & Monitoring Checklist

**What to Log**:
- [ ] Authentication events (login, logout, failed)
- [ ] Authorization failures
- [ ] Input validation failures
- [ ] Security-relevant actions (password change, role change)
- [ ] Errors and exceptions

**What NOT to Log**:
- [ ] Passwords (NEVER)
- [ ] Session tokens
- [ ] Full credit card numbers
- [ ] PII (unless required and encrypted)
- [ ] API keys/secrets
```

**Example: Safe Logging**
```javascript
// ❌ BAD: Logs password
logger.info({ user: email, password }, 'Login attempt');

// ✅ GOOD: No sensitive data
logger.info({ user: email, success: true }, 'Login successful');

// ❌ BAD: Logs full error with stack trace to user
catch (error) {
  res.status(500).json({ error: error.message, stack: error.stack });
}

// ✅ GOOD: Generic error to user, detailed logs server-side
catch (error) {
  logger.error({ error, userId, action }, 'Operation failed');
  res.status(500).json({ error: 'An error occurred' });
}
```

---

## Security Review Template

```markdown
## Security Review: [Feature/PR]

**Reviewer**: [Name]
**Date**: [Date]
**Code Reviewed**: [Files/PR Link]

### Risk Assessment
- **Data Sensitivity**: [None/Low/Medium/High/Critical]
- **Attack Surface**: [Internal/Authenticated/Public]
- **Overall Risk**: [Low/Medium/High/Critical]

### Findings

#### Critical (Fix Before Merge)
| ID | Issue | Location | Remediation |
|----|-------|----------|-------------|
| C1 | SQL Injection | users.js:45 | Use parameterized queries |

#### High (Fix Soon)
| ID | Issue | Location | Remediation |
|----|-------|----------|-------------|
| H1 | Missing authorization | orders.js:22 | Add ownership check |

#### Medium (Track for Future)
| ID | Issue | Location | Remediation |
|----|-------|----------|-------------|
| M1 | Weak session timeout | auth.js:10 | Reduce from 24h to 30min |

#### Low/Informational
| ID | Issue | Location | Remediation |
|----|-------|----------|-------------|
| L1 | Consider rate limiting | api.js:5 | Add per-user rate limits |

### Checklist Results
| Category | Status | Notes |
|----------|--------|-------|
| Input Validation | ✅ | All inputs validated |
| Authentication | ❌ | No MFA option |
| Authorization | ✅ | Ownership checks in place |
| Data Protection | ⚠️ | Secrets in env vars but not rotated |
| XSS Prevention | ✅ | Outputs properly escaped |
| Injection Prevention | ❌ | SQL injection found |
| Security Headers | ✅ | All headers configured |
| Dependencies | ⚠️ | 2 medium vulnerabilities |
| Logging | ✅ | No sensitive data logged |

### Recommendations
1. **Critical**: Fix SQL injection in users.js before merge
2. **High**: Add MFA option in next sprint
3. **Medium**: Set up automated dependency scanning

### Sign-off
- [ ] All critical findings addressed
- [ ] All high findings addressed or have tracking tickets
- [ ] Medium findings tracked for follow-up
```

---

## Common Vulnerabilities & Fixes

| Vulnerability | Example | Fix |
|---------------|---------|-----|
| SQL Injection | `query = "SELECT * FROM users WHERE id = " + userId` | Use parameterized queries |
| XSS | `element.innerHTML = userInput` | Use `textContent` or sanitize |
| IDOR | No ownership check on `/api/orders/:id` | Verify `order.userId === req.user.id` |
| Weak Passwords | No requirements | Enforce min length, complexity |
| Session Fixation | Reuse session after login | Regenerate session on auth change |
| CSRF | No token validation | Implement CSRF tokens |
| Exposed Secrets | API keys in code | Use environment variables |

---

## Tools & Resources

**Automated Scanning:**
- Snyk (dependency scanning)
- OWASP ZAP (web app scanner)
- Bandit (Python security linter)
- Brakeman (Ruby on Rails scanner)

**Manual Review:**
- OWASP Top 10 Checklist
- Security Code Review Guide
- CWE/SANS Top 25

**Training:**
- OWASP WebGoat (hands-on practice)
- PentesterLab (security challenges)
- HackerOne CTF

---

## Related Skills

- `/code-review` - General code quality review
- `/performance-optimization` - Performance considerations
- `/devops-cicd` - Security in CI/CD pipelines

---

**Last Updated**: 2026-01-22
