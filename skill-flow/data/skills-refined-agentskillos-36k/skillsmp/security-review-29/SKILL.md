---
name: security-review
description: |
  Security vulnerability detection skill for reviewer agents.
  OWASP Top 10 checklist, secrets detection, input validation, authentication patterns.
  CRITICAL for code handling user input, authentication, APIs, or sensitive data.
---

# Security Review

Security vulnerability detection and remediation guidance for ultrawork verification.

## What This Skill Provides

Comprehensive security checklists covering:
- OWASP Top 10 vulnerabilities
- Secrets and credential exposure
- Input validation and injection prevention
- Authentication and authorization patterns
- API security best practices

## When to Use This Skill

**ALWAYS review when code involves:**
- User input handling
- Authentication or authorization
- Database queries
- API endpoints
- File uploads
- Payment/financial operations
- External API integrations
- Sensitive data (PII, credentials, tokens)

**IMMEDIATELY review when:**
- Production incident occurred
- Dependency has known CVE
- User reports security concern
- Before major releases

## OWASP Top 10 Checklist

### 1. Injection (SQL, NoSQL, Command)

**Checklist:**

```
[ ] Queries use parameterization (no string concatenation)
[ ] ORMs used safely (no raw SQL strings)
[ ] User input is sanitized before queries
[ ] Command injection prevented (no shell execution with user input)
[ ] LDAP injection prevented
[ ] XPath injection prevented
```

**Examples:**

```javascript
// ❌ CRITICAL: SQL injection vulnerability
const query = `SELECT * FROM users WHERE id = ${userId}`;
await db.query(query);

// ✅ CORRECT: Parameterized query
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId);

// ❌ CRITICAL: Command injection
const { exec } = require('child_process');
exec(`ping ${userInput}`, callback);

// ✅ CORRECT: Use libraries instead
const dns = require('dns');
dns.lookup(userInput, callback);
```

### 2. Broken Authentication

**Checklist:**

```
[ ] Passwords are hashed (bcrypt, argon2, not MD5/SHA1)
[ ] JWT tokens properly validated
[ ] Sessions have timeouts
[ ] Multi-factor authentication available
[ ] Password reset tokens are single-use
[ ] Account lockout after failed attempts
[ ] Session fixation prevented
[ ] Credentials not in URLs or logs
```

**Examples:**

```javascript
// ❌ CRITICAL: Plaintext password comparison
if (password === storedPassword) { /* login */ }

// ✅ CORRECT: Hashed password comparison
import bcrypt from 'bcrypt';
const isValid = await bcrypt.compare(password, hashedPassword);

// ❌ CRITICAL: JWT not validated
const user = jwt.decode(token); // No verification!

// ✅ CORRECT: JWT validated
const user = jwt.verify(token, process.env.JWT_SECRET);
```

### 3. Sensitive Data Exposure

**Checklist:**

```
[ ] HTTPS enforced (no HTTP endpoints)
[ ] Secrets in environment variables (not hardcoded)
[ ] PII encrypted at rest
[ ] Logs don't contain sensitive data
[ ] API keys not exposed in client code
[ ] Database credentials not committed
[ ] Encryption uses strong algorithms (AES-256, not DES)
[ ] Sensitive data not in URLs or query params
```

**Examples:**

```javascript
// ❌ CRITICAL: Hardcoded secret
const apiKey = "sk-proj-abc123xyz";

// ✅ CORRECT: Environment variable
const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured');
}

// ❌ CRITICAL: Logging sensitive data
console.log('User login:', { email, password, apiKey });

// ✅ CORRECT: Sanitized logs
console.log('User login:', {
  email: email.replace(/(?<=.).(?=.*@)/g, '*'),
  passwordProvided: !!password
});
```

### 4. XML External Entities (XXE)

**Checklist:**

```
[ ] XML parsers have external entity processing disabled
[ ] XML input is validated
[ ] Alternative formats used when possible (JSON)
```

### 5. Broken Access Control

**Checklist:**

```
[ ] Authorization checked on every route
[ ] Users can only access their own resources
[ ] CORS configured properly (not '*' in production)
[ ] Object references are indirect (UUIDs, not sequential IDs)
[ ] Admin functions require admin role
[ ] Rate limiting prevents abuse
```

**Examples:**

```javascript
// ❌ CRITICAL: No authorization check
app.get('/api/user/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user); // Any user can see any profile!
});

// ✅ CORRECT: Verify access
app.get('/api/user/:id', authenticateUser, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = await getUser(req.params.id);
  res.json(user);
});
```

### 6. Security Misconfiguration

**Checklist:**

```
[ ] Default credentials changed
[ ] Debug mode disabled in production
[ ] Error messages don't expose internals
[ ] Security headers set (CSP, HSTS, X-Frame-Options)
[ ] Unnecessary features/ports disabled
[ ] Software is up to date
[ ] Directory listing disabled
[ ] Detailed errors not shown to users
```

**Security Headers:**

```javascript
// Required security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  next();
});
```

### 7. Cross-Site Scripting (XSS)

**Checklist:**

```
[ ] Output is escaped/sanitized
[ ] Content-Security-Policy header set
[ ] Frameworks escape by default (React, Vue)
[ ] innerHTML avoided (use textContent)
[ ] User input not directly rendered
[ ] URL parameters sanitized
```

**Examples:**

```javascript
// ❌ HIGH: XSS vulnerability
element.innerHTML = userInput;

// ✅ CORRECT: Use textContent
element.textContent = userInput;

// ✅ CORRECT: Sanitize if HTML needed
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 8. Insecure Deserialization

**Checklist:**

```
[ ] User input not deserialized without validation
[ ] JSON.parse has try/catch
[ ] Deserialization libraries up to date
[ ] Type checking after deserialization
```

### 9. Using Components with Known Vulnerabilities

**Checklist:**

```
[ ] Dependencies up to date
[ ] npm audit clean (no high/critical issues)
[ ] CVEs monitored
[ ] Automated dependency scanning enabled
[ ] Vulnerable packages replaced
```

**Commands:**

```bash
# Check for vulnerable dependencies
npm audit

# Fix automatically
npm audit fix

# High severity only
npm audit --audit-level=high
```

### 10. Insufficient Logging & Monitoring

**Checklist:**

```
[ ] Security events logged (login, failed auth, access control)
[ ] Logs monitored
[ ] Alerts configured for anomalies
[ ] Logs immutable (append-only)
[ ] Log retention policy defined
[ ] Sensitive data not logged
```

## Additional Security Patterns

### Server-Side Request Forgery (SSRF)

**Checklist:**

```
[ ] URLs validated and whitelisted
[ ] Internal IPs blocked
[ ] URL scheme restricted (http/https only)
```

**Example:**

```javascript
// ❌ HIGH: SSRF vulnerability
const response = await fetch(userProvidedUrl);

// ✅ CORRECT: Validate and whitelist
const allowedDomains = ['api.example.com', 'cdn.example.com'];
const url = new URL(userProvidedUrl);
if (!allowedDomains.includes(url.hostname)) {
  throw new Error('Invalid URL');
}
const response = await fetch(url.toString());
```

### Race Conditions (Financial/Critical Operations)

**Checklist:**

```
[ ] Atomic transactions for financial operations
[ ] Row-level locking for concurrent updates
[ ] Balance checks inside transactions
[ ] Idempotency keys for retries
```

**Example:**

```javascript
// ❌ CRITICAL: Race condition in balance check
const balance = await getBalance(userId);
if (balance >= amount) {
  await withdraw(userId, amount); // Another request could withdraw in parallel!
}

// ✅ CORRECT: Atomic transaction with lock
await db.transaction(async (trx) => {
  const balance = await trx('balances')
    .where({ user_id: userId })
    .forUpdate() // Lock row
    .first();

  if (balance.amount < amount) {
    throw new Error('Insufficient balance');
  }

  await trx('balances')
    .where({ user_id: userId })
    .decrement('amount', amount);
});
```

### Rate Limiting

**Checklist:**

```
[ ] Rate limiting on authentication endpoints
[ ] Rate limiting on API endpoints
[ ] Rate limiting on expensive operations
[ ] Different limits for authenticated/anonymous users
```

**Example:**

```javascript
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later'
});

app.post('/api/login', authLimiter, loginHandler);
```

## Secrets Detection

### Patterns to Detect

```bash
# Search for potential secrets
grep -r "api[_-]?key\|password\|secret\|token" \
  --include="*.js" \
  --include="*.ts" \
  --include="*.json" .

# Check git history for committed secrets
git log -p | grep -i "password\|api_key\|secret"
```

**Common secret patterns:**
- API keys: `sk-`, `pk-`, `api_key=`
- Passwords: `password =`, `pwd=`
- Tokens: `token=`, `access_token=`
- Private keys: `-----BEGIN PRIVATE KEY-----`

**Allowed patterns (not secrets):**
- `.env.example` files
- Test credentials clearly marked
- Public API keys (Stripe publishable key)
- Hash outputs (not keys)

## Security Review Process

### Step 1: Automated Scanning

```bash
# Dependency audit
npm audit

# Security linting
npx eslint . --plugin security

# Secrets scanning
npx trufflehog filesystem . --json
```

### Step 2: Manual Code Review

Focus on:
- Authentication/authorization code
- User input handling
- Database queries
- API endpoints
- File operations

### Step 3: Threat Modeling

Ask:
- What could an attacker do with this endpoint?
- What happens if user provides malicious input?
- Can users access others' data?
- Are financial operations atomic?

### Step 4: Evidence Collection

```bash
# Add security assessment to evidence
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --add-evidence "Security Review: PASS" \
  --add-evidence "- No hardcoded secrets" \
  --add-evidence "- Input validation present" \
  --add-evidence "- Authorization checked" \
  --add-evidence "- npm audit clean"
```

## Severity Classification

| Severity | Impact | Timeline |
|----------|--------|----------|
| CRITICAL | Data breach, financial loss, system compromise | Fix immediately, block deployment |
| HIGH | User data exposure, authentication bypass | Fix before production |
| MEDIUM | Information disclosure, weak crypto | Fix when possible |
| LOW | Best practice violation, minor info leak | Consider fixing |

## Common False Positives

**Not every finding is a vulnerability:**

- Environment variables in `.env.example` (examples, not secrets)
- Test credentials in test files (if clearly marked)
- Public API keys (Stripe publishable key)
- SHA256/MD5 for checksums (not passwords)
- Constants that look like secrets but aren't

**Always verify context before flagging.**

## Emergency Response

If CRITICAL vulnerability found:

1. **Document** - Create detailed report
2. **Notify** - Alert project owner immediately
3. **Recommend Fix** - Provide secure code example
4. **Test Fix** - Verify remediation works
5. **Verify Impact** - Check if vulnerability was exploited
6. **Rotate Secrets** - If credentials exposed
7. **Update Docs** - Add to security knowledge base

## Integration with Ultrawork

During VERIFICATION phase:

```bash
# Run security review
reviewer --task-id 1 --focus security

# Block if critical issues found
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --status resolved \
  --add-evidence "VERDICT: FAIL - CRITICAL security issue found" \
  --add-evidence "Hardcoded API key in src/api.ts:42"
```

## Quick Reference

**Must-check security items:**
- No hardcoded secrets
- Input validation on all user data
- Parameterized queries (no SQL injection)
- Authorization on protected routes
- HTTPS enforced
- Dependencies up to date

**Critical patterns:**
- SQL injection
- XSS vulnerabilities
- Authentication bypass
- Authorization bypass
- Hardcoded credentials
- Command injection
