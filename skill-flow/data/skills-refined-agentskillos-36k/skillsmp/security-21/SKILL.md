---
name: security
description: Security standards for authentication, input validation, and OWASP compliance
user-invocable: false
---

# Security Skill

**Version:** 1.0
**Source:** Security Standards

> Security must be built in from the start, not bolted on later. These standards apply to all code that handles user data, authentication, or external input.

---

## Core Principles

1. **Security by Design** — Build security in from the start, not as an afterthought
2. **Defense in Depth** — Multiple layers of security; no single point of failure
3. **Least Privilege** — Grant minimum access required for the task
4. **Fail Securely** — Errors should not expose vulnerabilities or sensitive data
5. **Zero Trust** — Never trust input, always verify
6. **Assume Breach** — Design as if attackers will get in; minimize blast radius

---

## OWASP Top 10 (2021)

Critical vulnerabilities to prevent:

| # | Vulnerability | Prevention |
|---|---------------|------------|
| 1 | **Broken Access Control** | Check authorization on every request |
| 2 | **Cryptographic Failures** | Use strong encryption, never roll your own |
| 3 | **Injection** | Parameterized queries, input validation |
| 4 | **Insecure Design** | Threat modeling, secure architecture |
| 5 | **Security Misconfiguration** | Secure defaults, proper error handling |
| 6 | **Vulnerable Components** | Keep dependencies updated, audit regularly |
| 7 | **Auth Failures** | Strong auth, MFA, secure session management |
| 8 | **Integrity Failures** | Verify code/data integrity, sign releases |
| 9 | **Logging Failures** | Log security events, protect log data |
| 10 | **SSRF** | Validate and allowlist server-side URLs |

---

## Input Validation

### The Golden Rule

**Never trust user input.** All input is potentially malicious.

### Validation Strategy

```
1. Validate → 2. Sanitize → 3. Encode (for output context)
```

### SQL Injection Prevention

```python
# ❌ NEVER - String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ ALWAYS - Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ✅ ALWAYS - ORM with parameters
User.objects.filter(id=user_id)
```

### XSS Prevention

```javascript
// ❌ NEVER - Direct HTML insertion
element.innerHTML = userInput;
document.write(userInput);

// ✅ ALWAYS - Text content (auto-escapes)
element.textContent = userInput;

// ✅ ALWAYS - Template literals with escaping
const escaped = escapeHtml(userInput);
```

### Command Injection Prevention

```python
# ❌ NEVER - Shell execution with user input
os.system(f"ls {user_path}")
subprocess.call(f"convert {filename}", shell=True)

# ✅ ALWAYS - Argument arrays (no shell)
subprocess.run(["ls", user_path], shell=False)
subprocess.run(["convert", filename], shell=False)
```

### Input Validation Patterns

```python
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) and len(email) <= 254

def validate_username(username: str) -> bool:
    """Validate username: alphanumeric, 3-30 chars."""
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return bool(re.match(pattern, username))

def validate_url(url: str, allowed_domains: list[str]) -> bool:
    """Validate URL against allowlist."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return (
        parsed.scheme in ('http', 'https') and
        parsed.netloc in allowed_domains
    )
```

---

## Authentication & Authorization

### Password Requirements

| Requirement | Minimum |
|-------------|---------|
| Length | 12 characters |
| Complexity | Not required if length met |
| Common passwords | Block top 10,000 |
| Breached passwords | Check against HaveIBeenPwned |

### Password Storage

```python
# ✅ Use bcrypt, Argon2, or scrypt
import bcrypt

def hash_password(password: str) -> bytes:
    """Hash password with bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode(), hashed)
```

**NEVER:**
- Store passwords in plain text
- Use MD5 or SHA1 for passwords
- Roll your own hashing

### Session Management

```python
# Session security settings
SESSION_CONFIG = {
    "cookie_secure": True,      # HTTPS only
    "cookie_httponly": True,    # No JavaScript access
    "cookie_samesite": "Lax",   # CSRF protection
    "session_lifetime": 3600,   # 1 hour max
    "regenerate_on_login": True # Prevent session fixation
}
```

### Authorization Checks

```python
# ✅ Check authorization on EVERY request
def get_document(user, document_id):
    document = Document.get(document_id)

    # Always verify ownership/access
    if document.owner_id != user.id and not user.is_admin:
        raise PermissionError("Access denied")

    return document
```

---

## Data Protection

### Encryption Requirements

| Data Type | At Rest | In Transit |
|-----------|---------|------------|
| Passwords | Hashed (bcrypt/Argon2) | TLS 1.2+ |
| PII (name, email, address) | AES-256 | TLS 1.2+ |
| Payment data | AES-256 + PCI DSS | TLS 1.3 |
| Health data | AES-256 + HIPAA | TLS 1.3 |
| Session tokens | N/A | TLS 1.2+ |
| API keys | AES-256 | TLS 1.2+ |

### Sensitive Data Handling

```python
# ✅ Mask sensitive data in logs
def log_user_action(user, action, data):
    safe_data = {
        "user_id": user.id,
        "email": mask_email(user.email),  # j***@example.com
        "action": action,
        # Never log: passwords, tokens, full credit cards
    }
    logger.info("User action", extra=safe_data)

def mask_email(email: str) -> str:
    """Mask email for logging."""
    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"

def mask_card(card: str) -> str:
    """Show only last 4 digits."""
    return f"****-****-****-{card[-4:]}"
```

### Data Retention

- Delete data when no longer needed
- Implement data expiration policies
- Provide user data export/deletion (GDPR)
- Securely wipe deleted data (not just mark deleted)

---

## API Security

### Rate Limiting

```python
# Implement rate limiting per endpoint
RATE_LIMITS = {
    "/api/login": "5/minute",      # Prevent brute force
    "/api/register": "3/minute",   # Prevent spam
    "/api/password-reset": "3/hour",
    "/api/*": "100/minute",        # General limit
}
```

### CORS Configuration

```python
# ✅ Specific origins only
CORS_CONFIG = {
    "origins": [
        "https://app.example.com",
        "https://admin.example.com",
    ],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_credentials": True,
    "max_age": 3600,
}

# ❌ NEVER in production
CORS_CONFIG = {
    "origins": "*",  # Allows any origin!
}
```

### API Response Security

```python
# ❌ Never expose internal errors
def handle_error(error):
    # Don't send: stack traces, SQL errors, file paths
    return {"error": "An error occurred"}, 500

# ✅ Log details, return generic message
def handle_error(error):
    logger.error(f"Internal error: {error}", exc_info=True)
    return {"error": "Internal server error"}, 500
```

### Security Headers

```python
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}
```

---

## Secrets Management

### Environment Variables

```bash
# ✅ Store secrets in environment
export DATABASE_URL="postgres://..."
export API_KEY="..."
export JWT_SECRET="..."

# ❌ NEVER commit secrets to code
DATABASE_URL = "postgres://user:password@host/db"  # In code!
```

### Secret Requirements

| Secret Type | Rotation Period | Storage |
|-------------|-----------------|---------|
| API keys | 90 days | Vault/env vars |
| Database passwords | 90 days | Vault/env vars |
| JWT secrets | 30 days | Vault/env vars |
| Encryption keys | 1 year | HSM/KMS |
| User passwords | On compromise | Hashed in DB |

### .gitignore

```gitignore
# Secrets - NEVER commit
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.yaml
config/secrets/*
```

---

## File Upload Security

### Validation Checklist

```python
def validate_upload(file) -> bool:
    """Validate uploaded file."""

    # 1. Check file size
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    if file.size > MAX_SIZE:
        raise ValueError("File too large")

    # 2. Check extension against allowlist
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
    ext = Path(file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")

    # 3. Verify magic bytes (don't trust extension)
    magic_bytes = file.read(8)
    file.seek(0)
    if not is_valid_magic(magic_bytes, ext):
        raise ValueError("File content doesn't match extension")

    # 4. Generate safe filename
    safe_name = generate_safe_filename(file.name)

    # 5. Store outside web root
    storage_path = UPLOAD_DIR / safe_name  # Not in /public!

    return True
```

### Safe Filename Generation

```python
import uuid
import re
from pathlib import Path

def generate_safe_filename(original: str) -> str:
    """Generate safe filename, preserving extension."""
    ext = Path(original).suffix.lower()
    # Use UUID, not original filename
    return f"{uuid.uuid4()}{ext}"
```

---

## Logging & Monitoring

### What to Log

```python
# ✅ Log these security events
SECURITY_EVENTS = [
    "login_success",
    "login_failure",
    "logout",
    "password_change",
    "password_reset_request",
    "permission_denied",
    "invalid_token",
    "rate_limit_exceeded",
    "suspicious_input",
    "admin_action",
]
```

### What NOT to Log

```python
# ❌ NEVER log these
NEVER_LOG = [
    "password",
    "password_hash",
    "credit_card",
    "ssn",
    "api_key",
    "session_token",
    "jwt_token",
    "private_key",
]
```

### Structured Security Logging

```python
def log_security_event(event_type: str, user_id: str, details: dict):
    """Log security event with context."""
    logger.info("security_event", extra={
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": get_client_ip(),
        "user_agent": get_user_agent(),
        **sanitize_details(details),
    })
```

---

## Security Checklist

### Before Every Release

- [ ] No secrets in code or version control
- [ ] All user input validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] Authentication on all protected endpoints
- [ ] Authorization checks on all resources
- [ ] HTTPS enforced (no HTTP)
- [ ] Security headers configured
- [ ] Rate limiting in place
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies updated and audited
- [ ] File uploads validated and stored safely
- [ ] Logging captures security events
- [ ] CORS configured restrictively

### Code Review Security Focus

- [ ] Input validation at all entry points
- [ ] Output encoding for XSS prevention
- [ ] Access control checks present
- [ ] No hardcoded secrets
- [ ] Proper error handling (no stack traces)
- [ ] Secure defaults used
- [ ] Third-party libraries are necessary and trusted

---

## References

- `references/owasp-top-10.md` — Detailed OWASP vulnerability guide
- `references/input-validation.md` — Complete input validation patterns
- `references/auth-patterns.md` — Authentication and authorization patterns

## Assets

- `assets/security-checklist.md` — Pre-release security checklist
- `assets/threat-model-template.md` — Threat modeling template

## Scripts

- `scripts/scan_secrets.py` — Scan code for accidentally committed secrets
- `scripts/check_dependencies.py` — Check dependencies for known vulnerabilities
