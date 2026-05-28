---
name: broken-authentication-testing
description: Use this skill when you need to test for broken authentication vulnerabilities, assess session management security, or evaluate password policies in web applications.
---

# Skill body

## Purpose

Identify and exploit authentication and session management vulnerabilities in web applications. Broken authentication consistently ranks in the OWASP Top 10 and can lead to account takeover, identity theft, and unauthorized access to sensitive systems. This skill covers testing methodologies for password policies, session handling, multi-factor authentication, and credential management.

## Prerequisites

### Required Knowledge
- HTTP protocol and session mechanisms
- Authentication types (SFA, 2FA, MFA)
- Cookie and token handling
- Common authentication frameworks

### Required Tools
- Burp Suite Professional or Community
- Hydra or similar brute-force tools
- Custom wordlists for credential testing
- Browser developer tools

### Required Access
- Target application URL
- Test account credentials
- Written authorization for testing

## Outputs and Deliverables

1. **Authentication Assessment Report** - Document all identified vulnerabilities.
2. **Credential Testing Results** - Brute-force and dictionary attack outcomes.
3. **Session Security Analysis** - Token randomness and timeout evaluation.
4. **Remediation Recommendations** - Security hardening guidance.

## Core Workflow

### Phase 1: Authentication Mechanism Analysis

Understand the application's authentication architecture:

```
# Identify authentication type
- Password-based (forms, basic auth, digest)
- Token-based (JWT, OAuth, API keys)
- Certificate-based (mutual TLS)
- Multi-factor (SMS, TOTP, hardware tokens)

# Map authentication endpoints
/login, /signin, /authenticate
/register, /signup
/forgot-password, /reset-password
/logout, /signout
/api/auth/*, /oauth/*
```

Capture and analyze authentication requests:

```http
POST /login HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

username=test&password=test123
```

### Phase 2: Password Policy Testing

Evaluate password requirements and enforcement:

```bash
# Test minimum length (a, ab, abcdefgh)
# Test complexity (password, ...)
```