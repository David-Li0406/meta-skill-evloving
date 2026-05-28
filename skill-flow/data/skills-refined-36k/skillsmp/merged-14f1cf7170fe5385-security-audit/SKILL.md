---
name: security-audit
description: Use this skill when implementing authentication, handling user input, working with sensitive data, or conducting security reviews.
---

# Security Audit Skill

## When to Use

- Implementing authentication/authorization
- Handling user input
- Working with sensitive data (passwords, tokens, keys)
- Security review requests
- Designing API endpoints

## Security Checklist

### Input Validation

- [ ] Validate all user input
- [ ] Prevent SQL Injection
- [ ] Prevent XSS
- [ ] Prevent Command Injection

### Authentication

- [ ] Secure password hashing
- [ ] Session management
- [ ] JWT security settings

### Authorization

- [ ] Permission verification
- [ ] Resource access control

## Reference Documents (Import Syntax)
@./reference/security.md
@./reference/error-handling.md
@./reference/api-design.md

## OWASP Top 10 Reference

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring