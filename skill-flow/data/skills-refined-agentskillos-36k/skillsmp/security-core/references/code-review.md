# Security Code Review Checklist

Comprehensive checklist for reviewing code security.

## Authentication & Authorization

### Authentication
- [ ] Passwords hashed with bcrypt/argon2 (never plain text or weak hashing)
- [ ] Password minimum length enforced (12+ characters)
- [ ] JWT secrets are strong (256+ bits) and stored securely
- [ ] Tokens have appropriate expiration times
- [ ] Session cookies are HttpOnly, Secure, and SameSite
- [ ] MFA implemented for sensitive operations
- [ ] Account lockout after failed login attempts
- [ ] Rate limiting on authentication endpoints
- [ ] No authentication credentials in code/logs

### Authorization
- [ ] Authorization checks on all protected endpoints
- [ ] Deny by default (explicit allow required)
- [ ] Resource ownership validated before operations
- [ ] Role/permission checks before sensitive operations
- [ ] RLS enabled on multi-tenant database tables
- [ ] Direct object references use UUIDs (not sequential IDs)
- [ ] Authorization failures logged
- [ ] No privilege escalation vulnerabilities

## Input Validation & Sanitization

- [ ] All user inputs validated with schema (Zod, Pydantic, etc.)
- [ ] SQL queries use parameterized statements (never string concatenation)
- [ ] NoSQL queries validated (prevent injection)
- [ ] File uploads validated (type, size, content)
- [ ] File upload filenames sanitized
- [ ] URL inputs validated and restricted
- [ ] HTML output sanitized (DOMPurify, html.escape)
- [ ] Command injection prevented (avoid shell execution)
- [ ] Path traversal prevented (validate file paths)
- [ ] Maximum input sizes enforced

## Data Protection

### Encryption
- [ ] TLS/HTTPS enforced in production
- [ ] Sensitive data encrypted at rest
- [ ] Strong encryption algorithms used (AES-256-GCM)
- [ ] Encryption keys stored securely (not in code)
- [ ] Authenticated encryption used (GCM mode)

### Sensitive Data
- [ ] PII handled according to requirements (GDPR, etc.)
- [ ] Passwords never logged
- [ ] Secrets not in code or version control
- [ ] API keys/tokens not exposed in client code
- [ ] Sensitive data masked in logs
- [ ] Proper data retention policies

## Security Headers & Configuration

- [ ] Content-Security-Policy configured
- [ ] Strict-Transport-Security enabled (HSTS)
- [ ] X-Frame-Options set (clickjacking protection)
- [ ] X-Content-Type-Options set to nosniff
- [ ] Referrer-Policy configured
- [ ] CORS properly configured (not wildcard in production)
- [ ] X-Powered-By header removed
- [ ] Error messages don't leak sensitive info
- [ ] Debug mode disabled in production

## Session Management

- [ ] Session IDs are cryptographically random
- [ ] Sessions expire after inactivity
- [ ] Sessions invalidated on logout
- [ ] Old sessions cleaned up
- [ ] Session fixation prevented
- [ ] CSRF tokens on state-changing operations
- [ ] Session cookies are HttpOnly and Secure

## API Security

- [ ] Rate limiting implemented
- [ ] API versioning in place
- [ ] Proper error responses (don't leak implementation)
- [ ] Request size limits enforced
- [ ] Authentication required on protected endpoints
- [ ] Input validation on all endpoints
- [ ] CORS configured correctly
- [ ] API keys rotated regularly

## Database Security

- [ ] Least privilege database access
- [ ] Prepared statements/parameterized queries
- [ ] RLS enabled on appropriate tables
- [ ] Database credentials in environment variables
- [ ] No database credentials in logs
- [ ] Connection pooling configured securely
- [ ] Database backups encrypted

## Logging & Monitoring

- [ ] Authentication events logged
- [ ] Authorization failures logged
- [ ] Security events logged
- [ ] Sensitive data not logged
- [ ] Log aggregation configured
- [ ] Alerting on suspicious activity
- [ ] Logs retained appropriately

## Dependency Management

- [ ] Dependencies up to date
- [ ] No known vulnerable dependencies (npm audit, pip-audit, cargo audit)
- [ ] Dependency sources trusted
- [ ] Lock files committed
- [ ] Automated dependency scanning in CI/CD
- [ ] License compliance checked

## Error Handling

- [ ] Errors caught and handled gracefully
- [ ] Stack traces not exposed in production
- [ ] Generic error messages to users
- [ ] Detailed errors logged securely
- [ ] Application doesn't crash on errors
- [ ] Failed operations logged

## File Operations

- [ ] File upload size limits
- [ ] File type validation (not just extension)
- [ ] Uploaded files scanned for malware
- [ ] File storage location secured
- [ ] Generated filenames (not user-provided)
- [ ] Directory traversal prevented
- [ ] Temporary files cleaned up

## Third-Party Integrations

- [ ] API keys stored securely
- [ ] HTTPS for external API calls
- [ ] External API responses validated
- [ ] Timeouts on external calls
- [ ] Circuit breakers for failing services
- [ ] Webhook signatures verified
- [ ] OAuth redirects validated

## Code Quality

- [ ] No commented-out security code
- [ ] No TODO comments about security
- [ ] No hardcoded credentials
- [ ] No debug/test code in production
- [ ] Secrets not in environment variable names
- [ ] Type safety enforced
- [ ] Linter warnings addressed

## Testing

- [ ] Security test cases written
- [ ] Authentication tests
- [ ] Authorization tests
- [ ] Input validation tests
- [ ] XSS prevention tests
- [ ] CSRF prevention tests
- [ ] Rate limiting tests
- [ ] Penetration testing performed

## Common Vulnerabilities

### XSS (Cross-Site Scripting)
- [ ] User content sanitized before rendering
- [ ] CSP configured
- [ ] No innerHTML with user content
- [ ] Template engines auto-escape by default

### CSRF (Cross-Site Request Forgery)
- [ ] CSRF tokens on state-changing operations
- [ ] SameSite cookie attribute set
- [ ] Origin/Referer headers checked
- [ ] Double-submit cookie pattern used

### SQL Injection
- [ ] Parameterized queries everywhere
- [ ] ORM used correctly
- [ ] No string concatenation in queries
- [ ] Input validation in place

### Command Injection
- [ ] No shell command execution with user input
- [ ] Libraries used instead of shell commands
- [ ] Input sanitized if shell commands necessary

### Path Traversal
- [ ] File paths validated
- [ ] Path normalization used
- [ ] Access restricted to allowed directories
- [ ] No user-controlled file paths

### SSRF (Server-Side Request Forgery)
- [ ] URL validation and allowlisting
- [ ] Internal IPs blocked
- [ ] Network segmentation
- [ ] Redirects not followed blindly

## Language-Specific

### TypeScript/JavaScript
- [ ] `eval()` and `Function()` avoided
- [ ] `innerHTML` avoided (use `textContent`)
- [ ] Prototype pollution prevented
- [ ] Regular expressions safe (no ReDoS)
- [ ] `Object.create(null)` for maps

### Python
- [ ] `pickle` not used with untrusted data
- [ ] `exec()` and `eval()` avoided
- [ ] SQL parameterization used
- [ ] Template injection prevented
- [ ] XML parsers configured securely

### Rust
- [ ] Minimal use of `unsafe` blocks
- [ ] Unsafe code reviewed carefully
- [ ] Input validation at boundaries
- [ ] Error handling proper
- [ ] Dependencies audited

## Pre-Deployment

- [ ] Security review completed
- [ ] Penetration testing performed
- [ ] Vulnerability scanning completed
- [ ] Security documentation updated
- [ ] Incident response plan reviewed
- [ ] Backup and recovery tested
- [ ] Monitoring and alerting configured
- [ ] Rate limiting tested under load

## Quick Check Script

```typescript
// Run these checks locally before committing
const securityChecks = [
  'npm audit --audit-level=high',
  'grep -r "password.*=.*["\']" src/', // Hardcoded passwords
  'grep -r "api[_-]?key.*=.*["\']" src/', // Hardcoded API keys
  'grep -r "eval\\(" src/', // Dangerous eval
  'grep -r "innerHTML" src/', // XSS risk
  'grep -r "SELECT.*\\${" src/', // SQL injection risk
];

for (const check of securityChecks) {
  console.log(`Running: ${check}`);
  // Execute and review results
}
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
