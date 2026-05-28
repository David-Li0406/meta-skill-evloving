---
name: security-best-practices
description: Use this skill when applying secure coding practices and identifying vulnerabilities in web applications, particularly when handling user input, authentication, and authorization.
---

# Security Best Practices

This skill provides guidance for writing secure code and avoiding common vulnerabilities.

## When This Skill Applies

- Handling user input or form data
- Implementing authentication or authorization
- Working with secrets, tokens, or credentials
- Building APIs or web endpoints
- Processing file uploads
- Interacting with databases

## Core Principles

1. **Never trust user input** - Validate and sanitize everything.
2. **Defense in depth** - Multiple layers of security.
3. **Least privilege** - Minimum permissions needed.
4. **Fail securely** - Errors shouldn't leak info or open holes.
5. **Secure by default** - Safe defaults, opt-in to danger.

## OWASP Top 10 Vulnerabilities

| # | Vulnerability | Prevention |
|---|---------------|------------|
| A01 | Injection | Use parameterized queries and prepared statements. |
| A02 | Broken Authentication | Hash passwords with bcrypt, enforce strong policies, and implement MFA. |
| A03 | Sensitive Data Exposure | Encrypt data at rest and in transit, and use secure headers. |
| A04 | XML External Entities (XXE) | Disable external entities when parsing XML. |
| A05 | Broken Access Control | Verify authorization on every request and log access control failures. |
| A06 | Security Misconfiguration | Disable debug mode in production and keep dependencies updated. |
| A07 | Cross-Site Scripting (XSS) | Escape output based on context and use Content-Security-Policy headers. |
| A08 | Insecure Deserialization | Don't deserialize untrusted data and validate allowed types. |
| A09 | Using Components with Known Vulnerabilities | Regularly audit dependencies and keep them updated. |
| A10 | Insufficient Logging & Monitoring | Log authentication successes and failures, and monitor for suspicious activity. |

## Input Validation

### Validate Everything

```python
def create_user(email: str, age: int):
    if not isinstance(email, str):
        raise ValueError("Email must be a string")
    if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
        raise ValueError("Invalid email format")
    if not 0 < age < 150:
        raise ValueError("Invalid age")
    if len(email) > 254:
        raise ValueError("Email too long")
```

### Validation Layers

1. **Client-side** - UX only, never trust.
2. **API layer** - Schema validation (Zod, Pydantic).
3. **Business logic** - Domain-specific rules.
4. **Database** - Constraints and types.

## Authentication Patterns

### Password Hashing

```python
import bcrypt

# Hash
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verify
bcrypt.checkpw(password.encode(), stored_hash)
```

### JWT Best Practices

- Use short expiration times (15 min access, longer refresh).
- Validate all claims (iss, aud, exp).
- Use asymmetric keys (RS256) for distributed systems.
- Store refresh tokens securely (httpOnly cookies).
- Implement token revocation.

## Secrets Management

### Never Do

```python
API_KEY = "sk-1234567890abcdef"  # Never hardcode
```

### Always Do

```python
API_KEY = os.environ.get("API_KEY")  # Use environment variable
```

## Security Review Checklist

Before deploying, verify:

- [ ] No hardcoded secrets.
- [ ] All user input validated.
- [ ] SQL queries parameterized.
- [ ] Output properly escaped.
- [ ] Authentication on protected routes.
- [ ] Authorization checks per-resource.
- [ ] Sensitive data encrypted.
- [ ] Security headers configured.
- [ ] Dependencies updated.
- [ ] Error messages don't leak info.

## Resources

- **OWASP Top 10**: https://owasp.org/Top10/
- **OWASP Cheat Sheets**: https://cheatsheetseries.owasp.org/
- **Node.js Security**: https://nodejs.org/en/docs/guides/security/
- **Snyk**: https://snyk.io/