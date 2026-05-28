# Express.js Security Patterns

**Category**: code-security/framework-security/express
**Description**: Security vulnerabilities and secure coding patterns for Express.js applications
**CWE**: CWE-89, CWE-79, CWE-78, CWE-22, CWE-352, CWE-693, CWE-384

---

## Overview

Express.js is minimal by design, requiring explicit security configurations. Many vulnerabilities arise from missing middleware or improper input handling.

---

## SQL/NoSQL Injection Patterns

### SQL Template Literal
**Pattern**: `\$\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Template literal string in SQL query
- CWE-89: SQL Injection

### MongoDB Query Injection
**Pattern**: `\.find(?:One)?\s*\(\s*\{\s*\w+\s*:\s*req\.(?:body|query|params)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Direct request input in MongoDB query
- CWE-943: NoSQL Injection

### Mongoose Query
**Pattern**: `\.findOne\s*\(\s*req\.body\s*\)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Entire request body as MongoDB query
- CWE-943: NoSQL Injection

---

## XSS Patterns

### Template Literal Response
**Pattern**: `res\.send\s*\(\s*`.*\$\{.*req\.`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Request input directly in HTML response
- CWE-79: Cross-site Scripting

### Unescaped HTML
**Pattern**: `innerHTML\s*=\s*.*req\.`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- User input assigned to innerHTML
- CWE-79: Cross-site Scripting

---

## Command Injection Patterns

### Exec with Template
**Pattern**: `exec\s*\(\s*`.*\$\{`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Template literal in child_process.exec
- CWE-78: OS Command Injection

### Exec with Concatenation
**Pattern**: `exec\s*\([^)]*\+\s*req\.`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Request input concatenated in exec
- CWE-78: OS Command Injection

---

## Path Traversal Patterns

### SendFile with Params
**Pattern**: `sendFile\s*\([^)]*req\.params`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- sendFile with unvalidated path parameter
- CWE-22: Path Traversal

### ReadFile with Request
**Pattern**: `readFile(?:Sync)?\s*\([^)]*req\.`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- File read with user-controlled path
- CWE-22: Path Traversal

---

## Security Header Patterns

### Missing Helmet
**Pattern**: `const\s+app\s*=\s*express\s*\(\s*\)(?![\s\S]*helmet)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Express app without helmet middleware
- CWE-693: Protection Mechanism Failure

### X-Powered-By Enabled
**Pattern**: `app\.disable\s*\(\s*['"]x-powered-by['"]\s*\)`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript]
- X-Powered-By header should be disabled (positive pattern)

---

## CORS Patterns

### Wildcard CORS Origin
**Pattern**: `cors\s*\(\s*\{\s*origin\s*:\s*['"]\*['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- CORS allows any origin
- CWE-942: Permissive CORS Policy

### Reflected CORS Origin
**Pattern**: `['"]Access-Control-Allow-Origin['"]\s*,\s*req\.headers\.origin`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- CORS origin reflected from request
- CWE-942: Permissive CORS Policy

### CORS Credentials with Wildcard
**Pattern**: `cors\s*\(\s*\{[^}]*origin\s*:\s*['"]\*['"][^}]*credentials\s*:\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- CORS credentials with wildcard origin
- CWE-942: Permissive CORS Policy

---

## Session Security Patterns

### Weak Session Secret
**Pattern**: `session\s*\(\s*\{[^}]*secret\s*:\s*['"][^'"]{1,15}['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Short/weak session secret
- CWE-798: Hardcoded Credentials

### Insecure Session Cookie
**Pattern**: `session\s*\(\s*\{[^}]*cookie\s*:\s*\{[^}]*secure\s*:\s*false`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Session cookie not secure
- CWE-614: Sensitive Cookie Without Secure

### Missing HttpOnly
**Pattern**: `cookie\s*:\s*\{[^}]*httpOnly\s*:\s*false`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Cookie accessible via JavaScript
- CWE-1004: Sensitive Cookie Without HttpOnly

---

## Error Handling Patterns

### Stack Trace Exposure
**Pattern**: `res\.(?:json|send)\s*\(\s*\{[^}]*(?:stack|error)\s*:\s*(?:err|error)\.stack`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Stack trace sent to client
- CWE-209: Error Message Information Leak

---

## Rate Limiting Patterns

### Auth Without Rate Limit
**Pattern**: `app\.post\s*\(\s*['"]\/(?:api\/)?(?:login|auth|signin)['"]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Login endpoint (check for rate limiting middleware)
- CWE-307: Improper Restriction of Auth Attempts

---

## Code Examples

### SQL Injection - Vulnerable vs Secure

```javascript
// VULNERABLE - String concatenation
app.get('/user', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.query.id}`;
  db.query(query);
});

// SECURE - Parameterized queries
app.get('/user', (req, res) => {
  const query = 'SELECT * FROM users WHERE id = ?';
  db.query(query, [req.query.id]);
});
```

### NoSQL Injection - Vulnerable vs Secure

```javascript
// VULNERABLE - Direct object from request
app.post('/login', (req, res) => {
  User.findOne({
    username: req.body.username,
    password: req.body.password  // Can inject { $gt: "" }
  });
});

// SECURE - Validate and sanitize
const mongoSanitize = require('express-mongo-sanitize');
app.use(mongoSanitize());

app.post('/login', (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);
  User.findOne({ username, password });
});
```

### Command Injection - Vulnerable vs Secure

```javascript
// VULNERABLE - User input in shell command
const { exec } = require('child_process');

app.get('/ping', (req, res) => {
  exec(`ping -c 4 ${req.query.host}`, (err, stdout) => {
    res.send(stdout);
  });
});

// SECURE - Use execFile with array arguments
const { execFile } = require('child_process');

app.get('/ping', (req, res) => {
  const hostRegex = /^[a-zA-Z0-9.-]+$/;
  if (!hostRegex.test(req.query.host)) {
    return res.status(400).send('Invalid host');
  }

  execFile('ping', ['-c', '4', req.query.host], (err, stdout) => {
    res.send(stdout);
  });
});
```

---

## Security Middleware Stack

```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');
const hpp = require('hpp');
const cors = require('cors');

const app = express();

// Security headers
app.use(helmet());

// CORS
app.use(cors({
  origin: 'https://yourdomain.com',
  credentials: true
}));

// Rate limiting
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));

// Body parsing with size limit
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// Data sanitization
app.use(mongoSanitize());  // NoSQL injection
app.use(xss());            // XSS

// Prevent parameter pollution
app.use(hpp());
```

---

## Express Security Checklist

- [ ] helmet() middleware enabled
- [ ] Rate limiting configured
- [ ] CORS properly restricted
- [ ] CSRF protection for forms
- [ ] Input validation on all routes
- [ ] Parameterized database queries
- [ ] Secure session configuration
- [ ] HTTPS enforced
- [ ] Error messages sanitized
- [ ] File upload validation
- [ ] Dependencies audited (`npm audit`)

---

## References

- [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [OWASP NodeJS Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)
