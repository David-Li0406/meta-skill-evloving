# Security Patterns

## Input Validation

```
Validate at boundaries:
├─ API endpoints (request body, params, headers)
├─ Form submissions
├─ File uploads
├─ Webhooks from external services
└─ Queue message handlers
```

### Validation Rules

```typescript
// Example schema (Zod-style)
const createUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().positive().max(150).optional(),
  role: z.enum(['user', 'admin']).default('user'),
});
```

**Always:**

- Whitelist allowed values (not blacklist)
- Set max lengths on all strings
- Validate file types by content (not extension)
- Sanitize HTML if displaying user content

## SQL Injection Prevention

```python
# NEVER
query = f"SELECT * FROM users WHERE id = {user_id}"

# ALWAYS (parameterized)
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

```javascript
// NEVER
db.query(`SELECT * FROM users WHERE id = ${userId}`)

// ALWAYS
db.query('SELECT * FROM users WHERE id = $1', [userId])
```

## XSS Prevention

```
1. Escape output by default (templates do this)
2. Use Content-Security-Policy header
3. Set HttpOnly on session cookies
4. Sanitize if accepting HTML: use allowlist (DOMPurify)
```

### CSP Header

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
```

## OWASP Top 10 Checklist

| Risk | Mitigation |
|------|------------|
| Injection | Parameterized queries, ORM |
| Broken Auth | Strong passwords, MFA, rate limiting |
| Sensitive Data Exposure | HTTPS, encrypt at rest, don't log PII |
| XXE | Disable external entities in XML parsers |
| Broken Access Control | Check permissions per request, deny by default |
| Misconfiguration | Secure defaults, remove debug modes in prod |
| XSS | Escape output, CSP headers |
| Insecure Deserialization | Validate before deserializing, avoid pickle/eval |
| Vulnerable Components | Keep dependencies updated, audit regularly |
| Insufficient Logging | Log auth events, access to sensitive data |

## Rate Limiting

```python
# Key strategies
by_ip = f"rate:{ip}:{endpoint}"           # Basic
by_user = f"rate:{user_id}:{endpoint}"    # Authenticated
by_action = f"rate:{user_id}:login"       # Specific actions

# Typical limits
login: 5 attempts per 15 min
api: 100 requests per minute
signup: 3 per hour per IP
password_reset: 3 per hour per email
```

## Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0  # Deprecated, use CSP
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Secrets Management

```
DO:
├─ Environment variables
├─ Secret managers (AWS Secrets, Vault, 1Password)
├─ .env files (gitignored, local only)
└─ CI/CD secrets

DON'T:
├─ Hardcode in source
├─ Commit to git
├─ Log or expose in errors
└─ Share in plain text (Slack, email)
```
