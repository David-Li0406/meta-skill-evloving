# OWASP Top 10 Reference

Reference for: Codebase Audit

Quick reference for detecting OWASP Top 10 vulnerabilities in code audits.

## 1. Broken Access Control

**Risk:** Users acting outside intended permissions.

### Detection Patterns

```bash
# Missing authorization checks
grep -rn "req\.user\|req\.session" --include="*.js" --include="*.ts" . | grep -v "if.*role\|if.*permission"

# Direct object references without validation
grep -rn "params\.id\|query\.id" --include="*.js" --include="*.ts" . | head -20
```

### Vulnerable Code

```javascript
// ❌ Bad: No authorization check
app.delete('/api/users/:id', (req, res) => {
  User.delete(req.params.id);
});

// ✓ Good: Check ownership/role
app.delete('/api/users/:id', auth, (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).send('Forbidden');
  }
  User.delete(req.params.id);
});
```

## 2. Cryptographic Failures

**Risk:** Sensitive data exposed due to weak/missing encryption.

### Detection Patterns

```bash
# Passwords/secrets in plaintext
grep -rn "password.*=\|api_key.*=" --include="*.js" --include="*.ts" --include="*.py" . | grep -v "hash\|encrypt"

# Weak crypto algorithms
grep -rn "md5\|sha1\|DES\|RC4" --include="*.js" --include="*.ts" --include="*.py" .
```

### Vulnerable Code

```javascript
// ❌ Bad: Plaintext password
const user = { password: req.body.password };

// ❌ Bad: Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex');

// ✓ Good: Strong hashing with salt
const hash = await bcrypt.hash(password, 12);
```

## 3. Injection (SQL, Command, etc.)

**Risk:** Attacker executes malicious code through untrusted input.

### Detection Patterns

```bash
# SQL Injection - string concatenation in queries
grep -rn "query.*+\|execute.*+" --include="*.js" --include="*.ts" --include="*.py" .
grep -rn "execute.*%" --include="*.py" .

# Command Injection
grep -rn "exec\(.*req\.\|spawn\(.*req\.\|shell=True" --include="*.js" --include="*.ts" --include="*.py" .

# NoSQL Injection
grep -rn "\$where\|\$regex" --include="*.js" --include="*.ts" .
```

### Vulnerable Code

```javascript
// ❌ Bad: SQL Injection
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;

// ✓ Good: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [req.params.id]);

// ❌ Bad: Command Injection
exec(`convert ${req.body.file} output.pdf`);

// ✓ Good: Sanitize and validate
const file = path.basename(req.body.file);
if (!/^[a-zA-Z0-9_-]+\.jpg$/.test(file)) throw new Error('Invalid file');
exec(`convert ${file} output.pdf`);
```

## 4. Insecure Design

**Risk:** Missing or ineffective security controls.

### Check For

- **No rate limiting** on authentication endpoints
- **Missing CSRF protection** on state-changing operations
- **No input validation** on user data
- **Weak password requirements**
- **No multi-factor authentication** option

### Detection Patterns

```bash
# Missing rate limiting
grep -rn "express-rate-limit\|rate-limiter" --include="*.js" --include="*.ts" .

# Missing CSRF protection
grep -rn "csrf\|csurf" --include="*.js" --include="*.ts" .
```

## 5. Security Misconfiguration

**Risk:** Insecure default configurations, incomplete setups.

### Detection Patterns

```bash
# Debug mode enabled
grep -rn "DEBUG.*=.*true\|NODE_ENV.*development" --include="*.js" --include="*.ts" --include=".env*" .

# Default credentials
grep -rn "admin.*:.*admin\|root.*:.*root\|password.*:.*password" .

# Permissive CORS
grep -rn "Access-Control-Allow-Origin.*\*" --include="*.js" --include="*.ts" .

# Exposed error stacks
grep -rn "err\.stack\|error\.stack" --include="*.js" --include="*.ts" .
```

### Vulnerable Code

```javascript
// ❌ Bad: Permissive CORS
app.use(cors({ origin: '*' }));

// ✓ Good: Specific origins
app.use(cors({ origin: 'https://example.com' }));

// ❌ Bad: Exposing error details
res.status(500).json({ error: err.stack });

// ✓ Good: Generic error in production
res.status(500).json({ error: 'Internal server error' });
```

## 6. Vulnerable and Outdated Components

**Risk:** Using components with known vulnerabilities.

### Detection Commands

```bash
# Node.js
npm audit
npm outdated

# Python
pip-audit
pip list --outdated

# Check for known CVEs
npm audit --json | jq '.vulnerabilities'
```

### What to Check

- Dependencies with critical/high vulnerabilities
- Packages not updated in > 2 years
- Deprecated packages
- Transitive dependencies with issues

## 7. Identification and Authentication Failures

**Risk:** Compromised passwords, weak authentication.

### Detection Patterns

```bash
# Weak password requirements
grep -rn "password.*length" --include="*.js" --include="*.ts" . | grep -v "12\|16\|20"

# Insecure session management
grep -rn "localStorage.*token\|localStorage.*jwt" --include="*.js" --include="*.ts" .

# No brute force protection
grep -rn "login\|signin\|authenticate" --include="*.js" --include="*.ts" . | grep -v "rate-limit\|attempt"
```

### Vulnerable Code

```javascript
// ❌ Bad: Token in localStorage (XSS vulnerable)
localStorage.setItem('token', jwt);

// ✓ Good: HttpOnly cookie
res.cookie('token', jwt, { httpOnly: true, secure: true, sameSite: 'strict' });

// ❌ Bad: Weak password requirements
if (password.length < 6) return error;

// ✓ Good: Strong requirements
if (password.length < 12 || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
  return error;
}
```

## 8. Software and Data Integrity Failures

**Risk:** Code/data modified without verification.

### Detection Patterns

```bash
# Insecure deserialization
grep -rn "pickle\.loads\|yaml\.load\|eval\(" --include="*.py" --include="*.js" .

# Missing integrity checks
grep -rn "integrity=\|subresource" --include="*.html" .

# Unsigned updates
grep -rn "auto-update\|check.*update" --include="*.js" --include="*.ts" . | grep -v "signature\|verify"
```

### Vulnerable Code

```python
# ❌ Bad: Unsafe deserialization
import pickle
data = pickle.loads(untrusted_data)

# ✓ Good: Use JSON
import json
data = json.loads(untrusted_data)

# ❌ Bad: eval() on user input
result = eval(user_code)

# ✓ Good: Don't do it, or sandbox heavily
# Use ast.literal_eval() for safe evaluation
```

## 9. Security Logging and Monitoring Failures

**Risk:** Breaches not detected in time.

### Detection Patterns

```bash
# Missing logging
grep -rn "login\|authenticate\|delete\|admin" --include="*.js" --include="*.ts" . | grep -v "log\|audit"

# Console.log in production
grep -rn "console\.log\|console\.error" --include="*.js" --include="*.ts" . | grep -v "test\|spec"

# No monitoring setup
grep -rn "Sentry\|DataDog\|NewRelic\|AppInsights" --include="*.js" --include="*.ts" .
```

### What to Log

- Authentication attempts (success/failure)
- Authorization failures
- Input validation failures
- Critical operations (delete, admin actions)
- System errors and exceptions

### Don't Log

- Passwords
- Session tokens
- Credit card numbers
- Personal identification numbers

## 10. Server-Side Request Forgery (SSRF)

**Risk:** Attacker makes server request arbitrary URLs.

### Detection Patterns

```bash
# User-controlled URLs
grep -rn "fetch.*req\.\|axios.*req\.\|http\.get.*req\." --include="*.js" --include="*.ts" .

# URL parameters
grep -rn "params\.url\|query\.url\|body\.url" --include="*.js" --include="*.ts" .
```

### Vulnerable Code

```javascript
// ❌ Bad: User-controlled URL
app.get('/proxy', (req, res) => {
  fetch(req.query.url).then(r => r.text()).then(data => res.send(data));
});

// ✓ Good: Whitelist allowed domains
const ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com'];
app.get('/proxy', (req, res) => {
  const url = new URL(req.query.url);
  if (!ALLOWED_DOMAINS.includes(url.hostname)) {
    return res.status(400).send('Invalid domain');
  }
  fetch(url).then(r => r.text()).then(data => res.send(data));
});
```

## Quick Audit Commands

```bash
# Run all security checks
grep -rn "query.*+\|execute.*%" --include="*.js" --include="*.py" . # SQL Injection
grep -rn "innerHTML\|dangerouslySetInnerHTML" --include="*.jsx" . # XSS
grep -rn "localStorage.*token" --include="*.js" . # Insecure storage
grep -rn "md5\|sha1" --include="*.js" --include="*.py" . # Weak crypto
grep -rn "eval\(\|pickle\.loads" --include="*.js" --include="*.py" . # Deserialization
grep -rn "exec\(.*req\.\|spawn\(" --include="*.js" . # Command injection
```

## Severity Levels

| Severity | Criteria | Action |
|----------|---------|---------|
| **Critical** | Remote code execution, SQL injection, auth bypass | Fix immediately |
| **High** | XSS, CSRF, insecure deserialization | Fix before next release |
| **Medium** | Weak crypto, missing rate limiting | Fix soon |
| **Low** | Information disclosure, weak passwords allowed | Address in backlog |

## Resources

- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
