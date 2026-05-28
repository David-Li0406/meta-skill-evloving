# OWASP Top 10 Quick Reference

Patterns for detecting and preventing the most critical web application security risks.

## A01: Broken Access Control

### Detection Patterns

```javascript
// ❌ INSECURE: Direct object reference without authorization
app.get('/api/users/:id', (req, res) => {
  const user = db.findUser(req.params.id);  // No auth check!
  res.json(user);
});

// ✅ SECURE: Verify ownership
app.get('/api/users/:id', authenticate, (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = db.findUser(req.params.id);
  res.json(user);
});
```

### Checklist
- [ ] Deny by default (except public resources)
- [ ] Implement access control once, reuse everywhere
- [ ] Enforce record ownership
- [ ] Disable directory listing
- [ ] Log access control failures
- [ ] Rate limit API access

## A02: Cryptographic Failures

### Detection Patterns

```python
# ❌ INSECURE: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ SECURE: Use bcrypt/argon2
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
```

### Checklist
- [ ] Classify data (PII, secrets, etc.)
- [ ] Don't store sensitive data unnecessarily
- [ ] Encrypt data at rest and in transit
- [ ] Use strong algorithms (AES-256, RSA-2048+, SHA-256+)
- [ ] Use bcrypt/argon2/scrypt for passwords
- [ ] Disable caching for sensitive responses

## A03: Injection

### Detection Patterns

```python
# ❌ INSECURE: SQL injection
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# ✅ SECURE: Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

```javascript
// ❌ INSECURE: Command injection
exec(`ls ${userInput}`);

// ✅ SECURE: Use execFile with arguments array
execFile('ls', [userInput]);
```

### Types to Check
| Type | Sink | Prevention |
|------|------|------------|
| SQL | Database queries | Parameterized queries, ORMs |
| NoSQL | MongoDB queries | Schema validation, sanitize |
| Command | exec, system | execFile, avoid shell |
| LDAP | LDAP queries | Escape special characters |
| XPath | XML queries | Parameterized XPath |

## A04: Insecure Design

### Detection Patterns
- Missing rate limiting on sensitive endpoints
- No account lockout after failed attempts
- Credential recovery via security questions
- Missing business logic validation

### Checklist
- [ ] Threat model for critical flows
- [ ] Limit resource consumption
- [ ] Segregate tenants properly
- [ ] Unit/integration tests for access control

## A05: Security Misconfiguration

### Detection Patterns

```yaml
# ❌ INSECURE: Debug mode in production
DEBUG: true
STACK_TRACES: true

# ✅ SECURE: Production settings
DEBUG: false
STACK_TRACES: false
```

### Checklist
- [ ] Remove default credentials
- [ ] Disable unnecessary features
- [ ] Review cloud permissions (S3, GCS policies)
- [ ] Set security headers
- [ ] Keep dependencies updated
- [ ] Harden frameworks defaults

## A06: Vulnerable Components

### Detection Commands

```bash
# Node.js
npm audit
npx snyk test

# Python
pip-audit
safety check

# Go
govulncheck ./...

# General
trivy fs .
```

### Checklist
- [ ] Remove unused dependencies
- [ ] Inventory all components and versions
- [ ] Monitor CVE databases
- [ ] Obtain from official sources only
- [ ] Prefer maintained components

## A07: Authentication Failures

### Detection Patterns

```javascript
// ❌ INSECURE: Weak session
const sessionId = Math.random().toString();

// ✅ SECURE: Cryptographically secure
const sessionId = crypto.randomBytes(32).toString('hex');
```

### Checklist
- [ ] Implement MFA
- [ ] No default credentials
- [ ] Weak password checks (breached password lists)
- [ ] Limit failed login attempts
- [ ] Secure session management
- [ ] Use secure, httpOnly, sameSite cookies

## A08: Data Integrity Failures

### Detection Patterns

```javascript
// ❌ INSECURE: Trusting serialized data
const user = JSON.parse(req.cookies.user);

// ✅ SECURE: Signed/encrypted data
const user = jwt.verify(req.cookies.token, SECRET);
```

### Checklist
- [ ] Verify digital signatures
- [ ] Use integrity checks for serialized data
- [ ] Validate CI/CD pipeline integrity
- [ ] Review software update mechanisms

## A09: Logging & Monitoring Failures

### What to Log
```javascript
// Log security-relevant events
logger.info('Login attempt', {
  userId,
  ip: req.ip,
  success: false,
  reason: 'invalid_password'
});
```

### Checklist
- [ ] Log authentication events
- [ ] Log access control failures
- [ ] Log input validation failures
- [ ] Include context (user, IP, timestamp)
- [ ] Don't log sensitive data (passwords, tokens)
- [ ] Set up alerting for suspicious patterns

## A10: Server-Side Request Forgery (SSRF)

### Detection Patterns

```python
# ❌ INSECURE: User-controlled URL
response = requests.get(user_provided_url)

# ✅ SECURE: Validate and allowlist
from urllib.parse import urlparse

def fetch_url(url):
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Host not allowed")
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Scheme not allowed")
    # Block internal IPs
    ip = socket.gethostbyname(parsed.hostname)
    if ipaddress.ip_address(ip).is_private:
        raise ValueError("Private IP not allowed")
    return requests.get(url, timeout=5)
```

### Checklist
- [ ] Sanitize and validate all URLs
- [ ] Use allowlists for allowed destinations
- [ ] Block requests to private IP ranges
- [ ] Disable HTTP redirects or validate destinations
- [ ] Don't return raw responses to users

## Security Headers Quick Reference

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```
