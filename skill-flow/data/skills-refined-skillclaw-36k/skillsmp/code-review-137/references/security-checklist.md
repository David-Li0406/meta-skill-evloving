# Security Code Review Checklist

## Input Validation & Sanitization

### 1. User Input Validation
**Check:**
- [ ] All user inputs validated before use
- [ ] Whitelist validation preferred over blacklist
- [ ] Data type, format, length, range validated
- [ ] Validation on server-side (never trust client)

**Examples:**
```typescript
// Bad - No validation
app.post('/user', (req, res) => {
  const age = req.body.age;
  db.save({ age });
});

// Good - Validated
app.post('/user', (req, res) => {
  const age = parseInt(req.body.age);
  if (isNaN(age) || age < 0 || age > 150) {
    return res.status(400).json({ error: 'Invalid age' });
  }
  db.save({ age });
});
```

### 2. Input Sanitization
**Check:**
- [ ] HTML/XML special characters escaped
- [ ] URLs validated and sanitized
- [ ] File names sanitized (no path traversal)
- [ ] User-generated content sanitized before display

**Examples:**
```typescript
// Bad - Direct output
res.send(`<h1>Welcome ${req.query.name}</h1>`);

// Good - Escaped
import escapeHtml from 'escape-html';
res.send(`<h1>Welcome ${escapeHtml(req.query.name)}</h1>`);
```

---

## Injection Prevention

### 3. SQL Injection
**Check:**
- [ ] Parameterized queries/prepared statements used
- [ ] No string concatenation in SQL queries
- [ ] ORM used correctly (not bypassing protections)
- [ ] Stored procedures used safely

**Examples:**
```typescript
// CRITICAL - SQL Injection vulnerability
const query = `SELECT * FROM users WHERE id = '${userId}'`;
db.execute(query);

// Fixed - Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

### 4. Command Injection
**Check:**
- [ ] No shell commands constructed from user input
- [ ] If shell commands necessary, input strictly validated/escaped
- [ ] Prefer language APIs over shell commands
- [ ] Avoid `eval()`, `exec()`, `Function()` with user input

**Examples:**
```typescript
// CRITICAL - Command injection
const { exec } = require('child_process');
exec(`ping -c 4 ${userProvidedHost}`);

// Fixed - Use safe API
const dns = require('dns');
dns.resolve(userProvidedHost, (err, addresses) => {
  // Safe DNS lookup
});
```

### 5. Cross-Site Scripting (XSS)
**Check:**
- [ ] User content escaped before rendering
- [ ] Content Security Policy (CSP) headers configured
- [ ] `dangerouslySetInnerHTML` avoided or carefully used
- [ ] DOM manipulation sanitized

**Examples:**
```typescript
// CRITICAL - XSS vulnerability
document.getElementById('user-input').innerHTML = userContent;

// Fixed - Safe text content
document.getElementById('user-input').textContent = userContent;

// Or use sanitization library
import DOMPurify from 'dompurify';
document.getElementById('user-input').innerHTML = DOMPurify.sanitize(userContent);
```

### 6. LDAP Injection
**Check:**
- [ ] LDAP queries use proper escaping
- [ ] Special LDAP characters escaped
- [ ] Input validated before LDAP operations

### 7. XML/XPath Injection
**Check:**
- [ ] XML parsers configured to prevent XXE (XML External Entity)
- [ ] Disable DTD processing if not needed
- [ ] XPath queries parameterized or escaped

---

## Authentication & Session Management

### 8. Password Security
**Check:**
- [ ] Passwords never stored in plaintext
- [ ] Strong hashing algorithm used (bcrypt, Argon2, PBKDF2)
- [ ] Salt is unique per password
- [ ] Minimum password complexity enforced
- [ ] No password length limit (or very high limit)

**Examples:**
```typescript
// CRITICAL - Plaintext password
db.save({ username, password: userPassword });

// Fixed - Hashed with bcrypt
import bcrypt from 'bcrypt';
const saltRounds = 12;
const hashedPassword = await bcrypt.hash(userPassword, saltRounds);
db.save({ username, password: hashedPassword });
```

### 9. Authentication Mechanisms
**Check:**
- [ ] Multi-factor authentication (MFA) available for sensitive operations
- [ ] Account lockout after failed attempts
- [ ] Password reset tokens expire and single-use
- [ ] Session tokens cryptographically random
- [ ] Sessions timeout after inactivity

### 10. Session Management
**Check:**
- [ ] Session IDs not in URLs
- [ ] Secure and HttpOnly flags on cookies
- [ ] SameSite cookie attribute configured
- [ ] Session invalidated on logout
- [ ] New session ID after authentication

**Examples:**
```typescript
// Bad - Insecure cookie
res.cookie('sessionId', sessionId);

// Good - Secure cookie
res.cookie('sessionId', sessionId, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: 'strict',
  maxAge: 3600000 // 1 hour
});
```

---

## Authorization

### 11. Access Control
**Check:**
- [ ] Authorization checked on every request
- [ ] Role-based access control (RBAC) implemented
- [ ] Principle of least privilege applied
- [ ] No client-side only authorization
- [ ] Direct object references protected

**Examples:**
```typescript
// CRITICAL - No authorization check
app.delete('/user/:id', async (req, res) => {
  await db.deleteUser(req.params.id);
});

// Fixed - Check ownership
app.delete('/user/:id', async (req, res) => {
  const user = await db.getUser(req.params.id);
  if (user.id !== req.session.userId) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await db.deleteUser(req.params.id);
});
```

### 12. Insecure Direct Object References (IDOR)
**Check:**
- [ ] Users cannot access objects by guessing IDs
- [ ] Access control verified for each object
- [ ] Indirect references used when possible
- [ ] Authorization checked, not just authentication

---

## Data Protection

### 13. Encryption
**Check:**
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS for data in transit
- [ ] Strong encryption algorithms (AES-256, RSA-2048+)
- [ ] Encryption keys stored securely, not in code

**Examples:**
```typescript
// Bad - Plaintext sensitive data
db.save({ ssn: userSSN, creditCard: cardNumber });

// Good - Encrypted before storage
import { encrypt } from './encryption';
db.save({
  ssn: encrypt(userSSN),
  creditCard: encrypt(cardNumber)
});
```

### 14. Secrets Management
**Check:**
- [ ] No hardcoded passwords, API keys, tokens
- [ ] Secrets stored in environment variables or vault
- [ ] Secrets not committed to version control
- [ ] `.env` files in `.gitignore`

**Examples:**
```typescript
// CRITICAL - Hardcoded secret
const apiKey = 'sk_live_abc123xyz789';

// Fixed - Environment variable
const apiKey = process.env.API_KEY;
if (!apiKey) {
  throw new Error('API_KEY environment variable not set');
}
```

### 15. Sensitive Data Exposure
**Check:**
- [ ] Sensitive data not logged
- [ ] Passwords/tokens masked in logs
- [ ] Error messages don't reveal system details
- [ ] Debug mode disabled in production

---

## Cryptography

### 16. Cryptographic Practices
**Check:**
- [ ] Use proven cryptographic libraries (not custom crypto)
- [ ] Random number generator cryptographically secure
- [ ] Avoid deprecated algorithms (MD5, SHA1, DES, RC4)
- [ ] Proper key length for algorithms

**Examples:**
```typescript
// Bad - Weak random
const token = Math.random().toString(36).substr(2);

// Good - Cryptographically secure random
import crypto from 'crypto';
const token = crypto.randomBytes(32).toString('hex');
```

---

## Security Headers

### 17. HTTP Security Headers
**Check:**
- [ ] `Content-Security-Policy` configured
- [ ] `X-Frame-Options` prevents clickjacking
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Strict-Transport-Security` for HTTPS
- [ ] `X-XSS-Protection` enabled

**Examples:**
```typescript
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
```

---

## File Upload Security

### 18. File Upload Validation
**Check:**
- [ ] File type validated (not just extension)
- [ ] File size limited
- [ ] Uploaded files scanned for malware
- [ ] Files stored outside web root
- [ ] Unique, sanitized filenames generated

**Examples:**
```typescript
// Bad - No validation
app.post('/upload', (req, res) => {
  const file = req.files.upload;
  file.mv(`./uploads/${file.name}`);
});

// Good - Validated and sanitized
app.post('/upload', (req, res) => {
  const file = req.files.upload;

  // Validate type
  const allowedTypes = ['image/jpeg', 'image/png'];
  if (!allowedTypes.includes(file.mimetype)) {
    return res.status(400).json({ error: 'Invalid file type' });
  }

  // Validate size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    return res.status(400).json({ error: 'File too large' });
  }

  // Generate secure filename
  const ext = path.extname(file.name);
  const filename = `${crypto.randomUUID()}${ext}`;
  file.mv(`./uploads/${filename}`);
});
```

---

## Dependency Security

### 19. Third-Party Dependencies
**Check:**
- [ ] Dependencies regularly updated
- [ ] Vulnerability scanning enabled (npm audit, Snyk)
- [ ] Known vulnerable packages identified and fixed
- [ ] Minimal dependencies used
- [ ] Dependencies from trusted sources

**Commands:**
```bash
# Check for vulnerabilities
npm audit
npm audit fix

# Or use Snyk
snyk test
```

---

## Error Handling & Logging

### 20. Error Messages
**Check:**
- [ ] Generic error messages to users
- [ ] Detailed errors only in logs, not responses
- [ ] Stack traces not exposed to users
- [ ] No sensitive data in error messages

**Examples:**
```typescript
// Bad - Exposes details
try {
  db.query(sql);
} catch (error) {
  res.status(500).json({ error: error.message, stack: error.stack });
}

// Good - Generic to user, detailed in logs
try {
  db.query(sql);
} catch (error) {
  logger.error('Database error:', error);
  res.status(500).json({ error: 'An error occurred. Please try again.' });
}
```

### 21. Logging Security
**Check:**
- [ ] No passwords, tokens, or secrets logged
- [ ] PII (Personally Identifiable Information) masked
- [ ] Logs stored securely with access controls
- [ ] Log injection prevented

---

## API Security

### 22. Rate Limiting
**Check:**
- [ ] Rate limiting implemented for APIs
- [ ] Prevents brute force attacks
- [ ] Different limits for authenticated vs anonymous
- [ ] Graceful degradation under load

### 23. CORS Configuration
**Check:**
- [ ] CORS properly configured, not `*` in production
- [ ] Specific origins whitelisted
- [ ] Credentials handling secure

**Examples:**
```typescript
// Bad - Allows all origins
app.use(cors({ origin: '*', credentials: true }));

// Good - Specific origins
app.use(cors({
  origin: ['https://example.com', 'https://app.example.com'],
  credentials: true
}));
```

---

## Critical Security Vulnerabilities (OWASP Top 10)

1. **Injection** - SQL, NoSQL, OS, LDAP injection
2. **Broken Authentication** - Session management, password storage
3. **Sensitive Data Exposure** - Unencrypted data, weak crypto
4. **XML External Entities (XXE)** - XML processor vulnerabilities
5. **Broken Access Control** - Unauthorized function/data access
6. **Security Misconfiguration** - Default configs, verbose errors
7. **Cross-Site Scripting (XSS)** - Unescaped user content
8. **Insecure Deserialization** - Remote code execution
9. **Using Components with Known Vulnerabilities** - Outdated dependencies
10. **Insufficient Logging & Monitoring** - Attack detection failures

---

## Quick Security Audit Questions

1. Can users access data they shouldn't?
2. Are all inputs validated and sanitized?
3. Is sensitive data encrypted?
4. Are there hardcoded secrets?
5. Are error messages generic to users?
6. Is authentication/authorization checked everywhere?
7. Are dependencies up to date?
8. Is HTTPS enforced?
9. Are security headers configured?
10. Is rate limiting in place?
