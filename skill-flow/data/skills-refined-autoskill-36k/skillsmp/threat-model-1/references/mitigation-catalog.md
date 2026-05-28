# Mitigation Catalog

## Authentication

### Password Security

| Threat | Mitigation | Implementation |
|--------|------------|----------------|
| Weak passwords | Password policy | Min 12 chars, complexity |
| Credential stuffing | Breach detection | Check HaveIBeenPwned API |
| Brute force | Rate limiting | Max 5 attempts, exponential backoff |
| Password storage | Strong hashing | bcrypt/Argon2, cost factor 12+ |

```python
# Password hashing example
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash = ph.hash(password)
ph.verify(hash, password)  # Raises on mismatch
```

### Multi-Factor Authentication

| Factor | Examples | Strength |
|--------|----------|----------|
| Knowledge | Password, PIN | Weak alone |
| Possession | Phone, hardware key | Strong |
| Inherence | Biometrics | Strong |

**Implementation:**
- TOTP (Authenticator apps)
- WebAuthn/FIDO2 (Hardware keys)
- SMS (Weakest, avoid if possible)

### Session Management

| Threat | Mitigation |
|--------|------------|
| Session hijacking | HttpOnly, Secure, SameSite cookies |
| Session fixation | Regenerate session ID on login |
| Session timeout | Absolute and idle timeouts |
| Concurrent sessions | Limit sessions per user |

```
Set-Cookie: session=abc123;
  HttpOnly;           # No JavaScript access
  Secure;             # HTTPS only
  SameSite=Strict;    # No cross-site sending
  Path=/;
  Max-Age=3600
```

## Authorization

### Access Control

| Pattern | Use Case | Example |
|---------|----------|---------|
| RBAC | Role-based access | Admin, Editor, Viewer |
| ABAC | Attribute-based | Owner can edit own posts |
| ACL | Resource-specific | Share file with user |

```python
# Authorization check pattern
def get_document(user, doc_id):
    doc = Document.get(doc_id)
    if not doc:
        raise NotFoundError()
    if not user.can_access(doc):  # Check BEFORE returning
        raise ForbiddenError()
    return doc
```

### Principle of Least Privilege

| Layer | Implementation |
|-------|----------------|
| Application | Role-based access, feature flags |
| Database | Read-only connections where possible |
| Infrastructure | Service accounts with minimal permissions |
| Network | Deny by default, allow specific |

## Input Validation

### Validation Strategy

```python
# Defense in depth: validate at every layer
def create_user(request):
    # 1. Input validation
    email = validate_email(request.email)
    name = validate_string(request.name, max_length=100)

    # 2. Business logic validation
    if User.exists(email):
        raise DuplicateError()

    # 3. Database constraints
    # Unique constraint on email column

    # 4. Output encoding
    # When rendering: escape HTML
```

### Injection Prevention

| Attack | Mitigation | Example |
|--------|------------|---------|
| SQL Injection | Parameterized queries | `SELECT * FROM users WHERE id = ?` |
| XSS | Output encoding | `htmlspecialchars($data)` |
| Command Injection | Avoid shell, use APIs | `subprocess.run(['ls', path])` |
| Path Traversal | Validate path | `os.path.realpath()` |

```python
# SQL - Always use parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)  # Parameter, not string formatting
)

# Command - Avoid shell=True
subprocess.run(['convert', input_file, output_file])  # Good
subprocess.run(f'convert {input_file} {output_file}', shell=True)  # Bad
```

## Cryptography

### Data at Rest

| Data Type | Encryption | Key Storage |
|-----------|------------|-------------|
| Database fields | AES-256-GCM | KMS/HSM |
| Files | AES-256-GCM | KMS/HSM |
| Backups | Full encryption | Separate key |
| Logs | Sensitive fields only | Application key |

### Data in Transit

| Protocol | Configuration |
|----------|---------------|
| TLS 1.3 | Preferred |
| TLS 1.2 | Minimum, strong ciphers |
| mTLS | Service-to-service |

```nginx
# nginx TLS configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
add_header Strict-Transport-Security "max-age=63072000" always;
```

### Secrets Management

| Don't | Do |
|-------|-----|
| Hardcode in code | Environment variables |
| Commit to git | Secrets manager |
| Log secrets | Mask in logs |
| Share via email | Secure vault |

## API Security

### Rate Limiting

| Limit Type | Example | Purpose |
|------------|---------|---------|
| Per IP | 100 req/min | Prevent abuse |
| Per User | 1000 req/hour | Fair usage |
| Per Endpoint | 10 req/min (login) | Prevent brute force |

```nginx
# nginx rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api {
    limit_req zone=api burst=20 nodelay;
}
```

### API Authentication

| Method | Use Case | Security Level |
|--------|----------|----------------|
| API Key | Service-to-service | Medium |
| OAuth 2.0 | User authorization | High |
| JWT | Stateless auth | High |
| mTLS | Infrastructure | Highest |

## Logging & Monitoring

### What to Log

| Event | Data | Don't Log |
|-------|------|-----------|
| Authentication | User ID, IP, timestamp | Passwords |
| Authorization failures | Resource, user, action | Session tokens |
| Input validation failures | Field, pattern | Full input (may contain PII) |
| Errors | Stack trace (internal only) | Sensitive data in context |

### Detection Rules

| Attack | Detection |
|--------|-----------|
| Brute force | > 10 failed logins in 5 min |
| Account takeover | Login from new device + suspicious action |
| Data exfiltration | Large data export by single user |
| Privilege escalation | User accessing admin endpoints |

## Security Headers

```
# Essential headers
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

## Defense Matrix

| STRIDE | Primary Mitigations |
|--------|---------------------|
| **Spoofing** | Strong authentication, MFA |
| **Tampering** | Input validation, integrity checks, TLS |
| **Repudiation** | Audit logging, digital signatures |
| **Information Disclosure** | Encryption, access controls |
| **Denial of Service** | Rate limiting, input validation |
| **Elevation of Privilege** | Authorization checks, least privilege |
