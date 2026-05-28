---
name: security-audit
description: Security review checklist and patterns
status: ✅ Working
last-validated: 2025-12-15
---

# Security Audit

## Purpose
Provides security review checklist for identifying vulnerabilities and ensuring secure coding practices.

## Authentication & Authorization
- [ ] Strong password requirements enforced
- [ ] Multi-factor authentication available
- [ ] Session management secure (timeout, invalidation)
- [ ] JWT tokens properly validated
- [ ] Role-based access control (RBAC) implemented
- [ ] Authorization checked on every endpoint

## Input Validation
- [ ] All user input validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF tokens on state-changing operations
- [ ] File upload validation (type, size, content)

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/SSL for data in transit
- [ ] No secrets in source code
- [ ] Environment variables for configuration
- [ ] Secure key management

## API Security
- [ ] Rate limiting implemented
- [ ] API authentication required
- [ ] CORS properly configured
- [ ] API versioning in place
- [ ] Error messages don't leak info

## Common Vulnerabilities (OWASP Top 10)
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Data Integrity Failures
9. Logging Failures
10. SSRF

## Security Headers
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- Permissions-Policy
