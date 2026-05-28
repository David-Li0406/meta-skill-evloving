# Security Checklist

## Overview

Use this checklist before releases, during code reviews, and for security audits. Not every item applies to every project—use judgment.

---

## Pre-Release Security Checklist

### Authentication

- [ ] Passwords hashed with bcrypt/Argon2 (cost factor 12+)
- [ ] Password requirements enforced (12+ characters)
- [ ] Common passwords blocked
- [ ] Brute force protection (rate limiting, lockouts)
- [ ] Session IDs regenerated on login (prevent fixation)
- [ ] Session timeout implemented (absolute and idle)
- [ ] Logout invalidates session completely
- [ ] Password reset tokens are single-use and expire
- [ ] MFA available for sensitive accounts/actions

### Authorization

- [ ] Authorization checked on EVERY request
- [ ] Default deny—explicit grants required
- [ ] No IDOR vulnerabilities (verify resource ownership)
- [ ] Admin functions protected
- [ ] API endpoints have proper access control
- [ ] File access restricted to authorized users

### Session Management

- [ ] Session cookies: `Secure` flag (HTTPS only)
- [ ] Session cookies: `HttpOnly` flag (no JS access)
- [ ] Session cookies: `SameSite=Lax` or `Strict`
- [ ] Session data stored server-side (not in cookie)
- [ ] Session IDs are random and unpredictable

### Input Validation

- [ ] All user input validated on server side
- [ ] Input length limits enforced
- [ ] SQL queries use parameterized statements
- [ ] No command injection vulnerabilities
- [ ] File uploads validated (type, size, content)
- [ ] URLs validated against allowlist (if user-provided)
- [ ] JSON/XML input validated against schema

### Output Encoding

- [ ] HTML output encoded (XSS prevention)
- [ ] JavaScript data properly escaped
- [ ] URL parameters encoded
- [ ] CSV output escaped for formula injection
- [ ] Content-Type headers set correctly

### Cryptography

- [ ] HTTPS enforced (no HTTP)
- [ ] TLS 1.2+ only (no SSL, TLS 1.0/1.1)
- [ ] Strong cipher suites configured
- [ ] Certificates valid and not expiring soon
- [ ] Sensitive data encrypted at rest
- [ ] Encryption keys stored securely (not in code)
- [ ] No weak algorithms (MD5, SHA1 for security)

### API Security

- [ ] Rate limiting implemented
- [ ] CORS configured restrictively
- [ ] API authentication required
- [ ] API versioning in place
- [ ] Error responses don't leak sensitive info
- [ ] Request size limits enforced

### Security Headers

- [ ] `Strict-Transport-Security` (HSTS)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY` or `SAMEORIGIN`
- [ ] `Content-Security-Policy` configured
- [ ] `Referrer-Policy` set
- [ ] `Permissions-Policy` configured (if needed)

### Secrets Management

- [ ] No secrets in source code
- [ ] No secrets in version control history
- [ ] Secrets loaded from environment/vault
- [ ] API keys rotated regularly
- [ ] Database credentials not hardcoded
- [ ] `.gitignore` includes secret files

### Error Handling

- [ ] Stack traces not shown to users
- [ ] Database errors not exposed
- [ ] File paths not revealed
- [ ] Generic error messages for users
- [ ] Detailed errors logged server-side
- [ ] Error pages don't leak version info

### Logging & Monitoring

- [ ] Authentication events logged
- [ ] Authorization failures logged
- [ ] Sensitive operations logged
- [ ] Logs don't contain sensitive data (passwords, tokens)
- [ ] Log integrity protected
- [ ] Alerting configured for security events

### Dependencies

- [ ] Dependencies up to date
- [ ] No known vulnerabilities (npm audit, pip-audit)
- [ ] Lockfile committed
- [ ] Only necessary dependencies included
- [ ] Dependencies from trusted sources

### File Handling

- [ ] Uploads stored outside web root
- [ ] Upload filenames sanitized
- [ ] File type validated by content (not just extension)
- [ ] File size limits enforced
- [ ] Directory traversal prevented

---

## Code Review Security Focus

### Quick Checks

- [ ] No hardcoded secrets or credentials
- [ ] Input validation at entry points
- [ ] Output encoding for display
- [ ] Parameterized queries (no SQL concatenation)
- [ ] Authorization checks present
- [ ] Error handling doesn't leak info

### Red Flags

Look for these patterns:

| Red Flag | Risk |
|----------|------|
| `f"SELECT * FROM users WHERE id = {id}"` | SQL Injection |
| `eval(user_input)` | Code Injection |
| `os.system(f"cmd {param}")` | Command Injection |
| `element.innerHTML = data` | XSS |
| `pickle.loads(untrusted)` | Deserialization |
| `password = "secret123"` | Hardcoded Secret |
| `verify=False` (requests) | TLS Bypass |
| `shell=True` (subprocess) | Command Injection |
| `dangerouslySetInnerHTML` | XSS (React) |
| `| safe` filter | XSS (Jinja2) |

### Questions to Ask

1. Where does this data come from? Is it trusted?
2. What happens if this input is malicious?
3. Who should be able to access this? Is it checked?
4. What gets logged? Is it sensitive?
5. What happens if this fails? Is it secure?

---

## Environment-Specific Checks

### Development

- [ ] Debug mode disabled by default
- [ ] Test data doesn't contain real PII
- [ ] Development secrets separate from production
- [ ] Security linting enabled (bandit, eslint-security)

### Staging

- [ ] Mirrors production security config
- [ ] No production data without anonymization
- [ ] Access restricted to team
- [ ] HTTPS configured

### Production

- [ ] All development/debug features disabled
- [ ] Logging level appropriate (not DEBUG)
- [ ] Error pages are generic
- [ ] Admin interfaces protected/restricted
- [ ] Database access restricted
- [ ] Backups encrypted
- [ ] Monitoring and alerting active

---

## Periodic Security Tasks

### Weekly

- [ ] Review security alerts/logs
- [ ] Check dependency vulnerabilities
- [ ] Review failed login attempts

### Monthly

- [ ] Rotate API keys and tokens
- [ ] Review access permissions
- [ ] Update dependencies
- [ ] Review security patches

### Quarterly

- [ ] Security awareness refresher
- [ ] Review and update security policies
- [ ] Test backup restoration
- [ ] Review third-party integrations

### Annually

- [ ] Full security audit
- [ ] Penetration testing
- [ ] Review and update threat model
- [ ] Security training for team
- [ ] Review incident response plan

---

## Incident Response Checklist

If a security incident occurs:

### Immediate (0-1 hour)

- [ ] Contain the threat (revoke access, isolate systems)
- [ ] Preserve evidence (logs, artifacts)
- [ ] Notify security team
- [ ] Begin incident log

### Short-term (1-24 hours)

- [ ] Assess scope and impact
- [ ] Identify root cause
- [ ] Notify affected parties (if required)
- [ ] Implement temporary fixes

### Recovery (24-72 hours)

- [ ] Implement permanent fixes
- [ ] Verify fixes are effective
- [ ] Restore normal operations
- [ ] Update monitoring/detection

### Post-Incident

- [ ] Conduct post-mortem
- [ ] Document lessons learned
- [ ] Update security measures
- [ ] Share findings with team
