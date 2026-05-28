# Security Checklist

Deep-dive security review. Reference this when security concerns are detected.

---

## OWASP Top 10 Quick Reference

| # | Vulnerability | What to Check |
|---|---------------|---------------|
| A01 | Broken Access Control | Auth checks, RBAC, direct object references |
| A02 | Cryptographic Failures | Hardcoded secrets, weak algorithms, plaintext |
| A03 | Injection | SQL, command, LDAP, XPath injection |
| A04 | Insecure Design | Business logic flaws, missing threat modeling |
| A05 | Security Misconfiguration | Default creds, verbose errors, open ports |
| A06 | Vulnerable Components | Outdated dependencies with CVEs |
| A07 | Auth Failures | Weak passwords, session issues, credential exposure |
| A08 | Data Integrity Failures | Unsigned updates, insecure deserialization |
| A09 | Logging Failures | Missing audit logs, exposed sensitive data in logs |
| A10 | SSRF | Unvalidated URLs, internal network access |

---

## 1. Secrets & Credentials

### Check For

- [ ] API keys, tokens, passwords in code
- [ ] Hardcoded connection strings
- [ ] Private keys or certificates in repo
- [ ] `.env` files committed (check `.gitignore`)
- [ ] Secrets in comments or documentation

### Red Flags

```
# Patterns that suggest secrets
password = "..."
api_key = "sk-..."
secret = "..."
token = "eyJ..."
AWS_ACCESS_KEY = "AKIA..."
private_key = "-----BEGIN"
```

### Recommendation

Use environment variables or secret managers (Vault, AWS Secrets Manager, etc.)

---

## 2. Injection Vulnerabilities

### SQL Injection

- [ ] User input concatenated into SQL
- [ ] Dynamic query building without parameterization
- [ ] ORM used without proper escaping

```python
# BAD
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# GOOD
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Command Injection

- [ ] User input in shell commands
- [ ] `exec()`, `eval()`, `system()` with user data
- [ ] Subprocess calls without proper escaping

```typescript
// BAD
exec(`ls ${userInput}`);

// GOOD
execFile('ls', [validatedPath]);
```

### XSS (Cross-Site Scripting)

- [ ] User content rendered without escaping
- [ ] `innerHTML`, `dangerouslySetInnerHTML` with user data
- [ ] URL parameters reflected in page

```tsx
// BAD
<div dangerouslySetInnerHTML={{ __html: userComment }} />

// GOOD
<div>{userComment}</div>  // React auto-escapes
```

### Path Traversal

- [ ] File paths constructed from user input
- [ ] No validation of `..` in paths
- [ ] Symlink following not considered

```python
# BAD
filename = request.args.get('file')
return send_file(f"/uploads/{filename}")

# GOOD
filename = secure_filename(request.args.get('file'))
if not filename:
    abort(400)
return send_file(os.path.join(UPLOAD_DIR, filename))
```

---

## 3. Authentication & Authorization

### Authentication

- [ ] Password hashing uses strong algorithm (bcrypt, argon2)
- [ ] Timing-safe comparison for secrets
- [ ] Rate limiting on login attempts
- [ ] Session tokens are random and sufficient length
- [ ] Tokens expire appropriately

### Authorization

- [ ] Every endpoint checks permissions
- [ ] RBAC/ABAC properly implemented
- [ ] Direct object references validated
- [ ] No privilege escalation paths

```python
# BAD: Direct object reference
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return db.get_user(user_id)  # Anyone can access any user!

# GOOD: Authorization check
@app.get("/users/{user_id}")
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403)
    return db.get_user(user_id)
```

---

## 4. Data Exposure

### Sensitive Data in Logs

- [ ] Passwords not logged
- [ ] Credit card numbers masked
- [ ] PII (emails, SSN) not in debug logs
- [ ] Auth tokens not logged

```python
# BAD
logger.info(f"User login: {username}, password: {password}")

# GOOD
logger.info(f"User login attempt: {username}")
```

### API Response Leakage

- [ ] Internal IDs not exposed unnecessarily
- [ ] Stack traces not sent to clients
- [ ] Debug info disabled in production
- [ ] Sensitive fields excluded from serialization

```typescript
// BAD: Exposing internal details
catch (error) {
  res.status(500).json({ error: error.stack });
}

// GOOD: Generic error to client
catch (error) {
  logger.error(error);
  res.status(500).json({ error: 'Internal server error' });
}
```

---

## 5. Cryptography

### Check For

- [ ] Strong algorithms (AES-256, RSA-2048+, SHA-256+)
- [ ] No MD5 or SHA1 for security purposes
- [ ] Proper IV/nonce handling
- [ ] Key rotation capability
- [ ] TLS for data in transit

### Weak Patterns

```python
# BAD: Weak hash
hashlib.md5(password.encode()).hexdigest()

# GOOD: Proper password hashing
bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# BAD: ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# GOOD: GCM mode with nonce
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
```

---

## 6. Dependencies

### Check For

- [ ] `npm audit` / `pip-audit` / `cargo audit` run
- [ ] No known CVEs in dependencies
- [ ] Lockfile committed (package-lock.json, poetry.lock)
- [ ] Dependencies from trusted sources
- [ ] Minimal dependency surface

### Actions

```bash
# Check for vulnerabilities
npm audit
pip-audit
cargo audit

# Update vulnerable packages
npm audit fix
pip install --upgrade <package>
```

---

## 7. SSRF (Server-Side Request Forgery)

### Check For

- [ ] URL validation before fetching
- [ ] Whitelist of allowed domains
- [ ] No access to internal IPs (127.0.0.1, 10.x, 192.168.x)
- [ ] Protocol restrictions (http/https only)

```python
# BAD: Unvalidated URL
url = request.args.get('url')
response = requests.get(url)  # Can access internal services!

# GOOD: Validate URL
from urllib.parse import urlparse
url = request.args.get('url')
parsed = urlparse(url)
if parsed.scheme not in ('http', 'https'):
    abort(400)
if is_internal_ip(parsed.hostname):
    abort(400)
response = requests.get(url)
```

---

## 8. Input Validation

### General Rules

- [ ] Validate type, length, format, range
- [ ] Whitelist over blacklist
- [ ] Validate on server (client validation is UX only)
- [ ] Sanitize for specific context (HTML, SQL, shell)

### Examples

```typescript
// Validate with schema
const userSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(['user', 'admin']),
});

// Validate file uploads
if (!['image/png', 'image/jpeg'].includes(file.mimetype)) {
  throw new Error('Invalid file type');
}
if (file.size > 5 * 1024 * 1024) {
  throw new Error('File too large');
}
```

---

## Severity Guide

| Finding | Severity |
|---------|----------|
| Hardcoded production secret | Critical |
| SQL injection possible | Critical |
| Command injection possible | Critical |
| Missing auth check on sensitive endpoint | Critical |
| XSS vulnerability | Critical |
| Weak password hashing | Critical |
| Known CVE in dependency | Critical/Warning |
| Missing input validation | Warning |
| Verbose error messages | Warning |
| Missing rate limiting | Warning |
| Debug mode enabled | Warning |
| Outdated dependency (no CVE) | Info |
| Missing security headers | Info |
