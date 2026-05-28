---
name: security
description: "Security review process and vulnerability prevention. Use when reviewing code for security issues, implementing authentication or authorization, handling user input or secrets, adding API endpoints, or approving code that touches security boundaries. Also use for OWASP Top 10 analysis, secret scanning, dependency auditing, or when code handles forms, file uploads, sessions, tokens, database queries, or shell commands. Essential when someone says 'it's just a small change.'"
---

# Security Review Skill

## Overview

Security issues are cheap to prevent, expensive to fix after deployment. This skill guides systematic security review before code ships.

**Core principle:** Every code change is a potential security change. Review security implications BEFORE approving.

## The Security Review Process

### Phase 1: Threat Surface Identification

Before reviewing code details, identify what's at risk:

1. **Data Classification**
   - What sensitive data does this code touch?
   - PII, credentials, financial data, health records?
   - What's the impact if this data leaks?

2. **Trust Boundaries**
   - Where does untrusted input enter?
   - User input, API responses, file contents, environment variables?
   - What assumes data is "safe"?

3. **Attack Surface**
   - What new endpoints or interfaces are added?
   - What existing security controls might be bypassed?

### Phase 2: Vulnerability Scanning

Check for common vulnerability patterns:

1. **Injection Points** (CRITICAL - check first)
   - SQL queries with string concatenation
   - Shell command execution with user input
   - HTML rendering with unescaped content
   - See `references/owasp-top-10.md` for patterns

2. **Authentication/Authorization**
   - Missing auth checks on endpoints
   - Broken access control (can user A access user B's data?)
   - Weak session management
   - See `references/auth-patterns.md` for secure patterns

3. **Secrets Management**
   - Hardcoded credentials, API keys, tokens
   - Secrets in logs or error messages
   - Secrets committed to git history
   - See `references/secrets-guide.md` for detection patterns

4. **Data Exposure**
   - Sensitive data in responses (passwords, tokens, PII)
   - Verbose error messages revealing internals
   - Debug endpoints left enabled

### Phase 3: Verification

Before approving:

1. **Test Security Controls**
   - Do auth checks actually prevent unauthorized access?
   - Does input validation reject malicious input?
   - Are rate limits effective?

2. **Review Dependencies**
   - Any new dependencies with known vulnerabilities?
   - Run `npm audit` / `pip-audit` / `govulncheck`

3. **Check Configuration**
   - Security headers configured?
   - HTTPS enforced?
   - Secure cookie flags set?

## Red Flags - STOP and Investigate

If you see ANY of these, STOP and investigate before proceeding:

### Critical - Block Immediately
```
- String concatenation in SQL: f"SELECT * FROM users WHERE id = '{id}'"
- eval() or exec() with any external input
- innerHTML with user-controlled content
- Hardcoded secrets: API_KEY = "sk-live-..."
- Missing authentication on sensitive endpoints
- Shell commands with user input: os.system(f"ls {path}")
```

### High Risk - Require Justification
```
- Disabling security features: verify=False, --no-verify
- Broad CORS: Access-Control-Allow-Origin: *
- Elevated privileges: running as root, admin endpoints
- Cryptographic operations (easy to get wrong)
- Custom auth implementations (use standard libraries)
```

### Suspicious Patterns - Question Intent
```
- Base64 "encoding" treated as encryption
- MD5/SHA1 for passwords (use bcrypt/argon2)
- JWT with 'none' algorithm or long expiry
- Catching and silencing all exceptions
- Comments like "TODO: add auth later"
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "It's internal only" | Internal apps get compromised. Apply same standards. |
| "We'll add security later" | Later never comes. Security debt compounds. |
| "It's behind a firewall" | Defense in depth. Assume firewall fails. |
| "Only admins use this" | Admin credentials get stolen. Validate anyway. |
| "The framework handles it" | Frameworks have defaults. Verify they're secure. |
| "It's just for testing" | Test code ships to production. It happens. |
| "We trust this input" | Trust is a vulnerability. Validate everything. |

## Security Checklist

Before approving ANY code change:

- [ ] **Injection**: No string concatenation in queries/commands
- [ ] **Auth**: All sensitive endpoints require authentication
- [ ] **AuthZ**: Users can only access their own data
- [ ] **Secrets**: No hardcoded credentials, keys in env vars
- [ ] **Input**: All user input validated and sanitized
- [ ] **Output**: Sensitive data not leaked in responses/logs
- [ ] **Dependencies**: No known vulnerabilities (`npm audit` clean)
- [ ] **Headers**: Security headers configured (CSP, HSTS, etc.)

## Quick Reference Commands

```bash
# Secret scanning
gitleaks detect --source .
trufflehog filesystem .

# Dependency audit
npm audit                    # Node.js
pip-audit                    # Python
govulncheck ./...           # Go
cargo audit                  # Rust

# SAST scanning
semgrep --config auto .
bandit -r src/              # Python
gosec ./...                 # Go
```

## References

Detailed patterns and examples in `references/`:
- `owasp-top-10.md` - Top 10 vulnerabilities with code examples
- `auth-patterns.md` - Secure authentication implementation
- `secrets-guide.md` - Secret detection and management
- `security-headers.md` - HTTP security header configuration
