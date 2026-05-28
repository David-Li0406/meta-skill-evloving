---
name: security
description:
  Apply secure coding practices and identify vulnerabilities. Use this skill when handling user
  input, authentication, authorization, secrets, or any security-sensitive code. Covers OWASP top
  10, common vulnerability patterns, and secure defaults.
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

1. **Never trust user input** - Validate and sanitize everything
2. **Defense in depth** - Multiple layers of security
3. **Least privilege** - Minimum permissions needed
4. **Fail securely** - Errors shouldn't leak info or open holes
5. **Secure by default** - Safe defaults, opt-in to danger

## OWASP Top 10 Patterns

### 1. Injection (SQL, Command, etc.)

**Bad:**

```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

**Good:**

```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**Rules:**

- Use parameterized queries / prepared statements
- Use ORMs with proper escaping
- Never interpolate user input into commands

### 2. Broken Authentication

**Checklist:**

- [ ] Hash passwords with bcrypt/argon2 (never MD5/SHA1)
- [ ] Enforce strong password policies
- [ ] Implement rate limiting on login
- [ ] Use secure session management
- [ ] Invalidate sessions on logout
- [ ] Implement MFA where possible

### 3. Sensitive Data Exposure

**Rules:**

- Encrypt data at rest and in transit (TLS everywhere)
- Never log sensitive data (passwords, tokens, PII)
- Use secure headers (HSTS, CSP, X-Content-Type-Options)
- Minimize data collection and retention

### 4. XML External Entities (XXE)

**If parsing XML:**

```python
# Disable external entities
parser = etree.XMLParser(resolve_entities=False)
```

### 5. Broken Access Control

**Rules:**

- Verify authorization on every request
- Use role-based access control (RBAC)
- Deny by default
- Log access control failures
- Rate limit API access

### 6. Security Misconfiguration

**Checklist:**

- [ ] Disable debug mode in production
- [ ] Remove default credentials
- [ ] Keep dependencies updated
- [ ] Disable unnecessary features/endpoints
- [ ] Set secure HTTP headers

### 7. Cross-Site Scripting (XSS)

**Rules:**

- Escape output based on context (HTML, JS, URL, CSS)
- Use Content-Security-Policy headers
- Use frameworks with auto-escaping (React, Vue)
- Sanitize HTML if allowing rich text

### 8. Insecure Deserialization

**Rules:**

- Don't deserialize untrusted data
- Use JSON instead of pickle/serialize
- Validate and whitelist allowed types
- Sign serialized data if it must be trusted

### 9. Using Components with Known Vulnerabilities

**Practices:**

- Run `npm audit` / `pip-audit` / `cargo audit` regularly
- Keep dependencies updated
- Subscribe to security advisories
- Use Dependabot or similar tools

### 10. Insufficient Logging & Monitoring

**Log these events:**

- Authentication successes and failures
- Authorization failures
- Input validation failures
- Application errors
- High-value transactions

## Secrets Management

### Never Do

```python
API_KEY = "sk-1234567890abcdef"  # Never hardcode
```

### Always Do

```python
API_KEY = os.environ.get("API_KEY")  # Environment variable
# Or use a secrets manager (Vault, AWS Secrets Manager, etc.)
```

**Rules:**

- Never commit secrets to git
- Use `.env` files for local dev (gitignored)
- Rotate secrets regularly
- Use different secrets per environment
- Audit secret access

## Input Validation

### Validate Everything

```python
def create_user(email: str, age: int):
    # Type check
    if not isinstance(email, str):
        raise ValueError("Email must be a string")

    # Format check
    if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
        raise ValueError("Invalid email format")

    # Range check
    if not 0 < age < 150:
        raise ValueError("Invalid age")

    # Length check
    if len(email) > 254:
        raise ValueError("Email too long")
```

### Validation Layers

1. **Client-side** - UX only, never trust
2. **API layer** - Schema validation (Zod, Pydantic)
3. **Business logic** - Domain-specific rules
4. **Database** - Constraints and types

## Authentication Patterns

### Password Hashing

```python
# Python with bcrypt
import bcrypt

# Hash
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verify
bcrypt.checkpw(password.encode(), stored_hash)
```

### JWT Best Practices

- Use short expiration times (15 min access, longer refresh)
- Validate all claims (iss, aud, exp)
- Use asymmetric keys (RS256) for distributed systems
- Store refresh tokens securely (httpOnly cookies)
- Implement token revocation

## API Security

### Headers to Set

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

### Rate Limiting

Implement rate limiting on:

- Login endpoints (prevent brute force)
- API endpoints (prevent abuse)
- Resource-intensive operations

## Security Review Checklist

Before deploying, verify:

- [ ] No hardcoded secrets
- [ ] All user input validated
- [ ] SQL queries parameterized
- [ ] Output properly escaped
- [ ] Authentication on protected routes
- [ ] Authorization checks per-resource
- [ ] Sensitive data encrypted
- [ ] Security headers configured
- [ ] Dependencies updated
- [ ] Error messages don't leak info
