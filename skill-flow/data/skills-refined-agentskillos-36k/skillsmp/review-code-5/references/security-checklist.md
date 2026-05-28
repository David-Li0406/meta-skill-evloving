<overview>
Security code review checklist based on OWASP Code Review Guide and Top 10 2025. Comprehensive vulnerability patterns and search techniques.
</overview>

<critical_vulnerabilities>
<a01_broken_access_control priority="most_critical">
Authorization checks on **every request** (not just UI):

- [ ] Server-side enforcement (never trust client)
- [ ] IDOR protection: Users can't access others' data by changing IDs
- [ ] No privilege escalation paths
- [ ] Default deny policy (explicit allow required)
      </a01_broken_access_control>

<a02_security_misconfiguration>
Configuration hardening:

- [ ] No default credentials
- [ ] Debug mode disabled in production
- [ ] Secure headers present (CSP, X-Frame-Options, HSTS)
- [ ] Error messages don't expose internals
      </a02_security_misconfiguration>

<a04_cryptographic_failures>
Encryption requirements:

- [ ] TLS 1.2+ for data in transit
- [ ] AES-256 for data at rest
- [ ] Password hashing: bcrypt/Argon2/scrypt (NOT MD5/SHA1)
- [ ] No hardcoded encryption keys
      </a04_cryptographic_failures>

<a05_injection>
Injection prevention:

- [ ] SQL: Parameterized queries only (no string concatenation)
- [ ] Command: No `eval()`, `exec()`, `system()` with user input
- [ ] XSS: Output encoding context-appropriate
- [ ] Template: No user input in template names
      </a05_injection>
      </critical_vulnerabilities>

<input_validation>
Server-side validation checklist:

✓ Server-side validation on ALL inputs
✓ Allowlist approach (whitelist known-good)
✓ Validate: type, length, format, range
✓ File uploads: extension + MIME + content inspection
✓ Regex reviewed for ReDoS vulnerabilities
</input_validation>

<authentication>
| Check | Requirement |
|-------|-------------|
| Password Storage | bcrypt/Argon2 with salt |
| Session Tokens | ≥128 bits entropy, HttpOnly+Secure+SameSite |
| Error Messages | Generic ("Invalid credentials"), no enumeration |
| MFA | Required for sensitive accounts |
| Lockout | Exponential delay after failed attempts |
</authentication>

<authorization>
Access control requirements:

✓ Default deny (explicit allow required)
✓ Checks on EVERY request
✓ Server-side only (never trust client roles)
✓ Centralized access control logic
✓ No horizontal escalation (user → other user's data)
✓ No vertical escalation (user → admin functions)
</authorization>

<search_patterns>
Grep patterns for vulnerability detection:

<hardcoded_secrets>

```bash
grep -rE "(password|api[_-]?key|secret|token)\s*=\s*['\"]" --include="*.{js,ts,py,java}"
```

</hardcoded_secrets>

<dangerous_functions>

```bash
grep -rE "(eval|exec|system|shell_exec)\s*\(" --include="*.{js,ts,py,php}"
```

</dangerous_functions>

<sql_injection_risk>

```bash
grep -rE "query\s*\(\s*['\"].*\+|execute\s*\(\s*f['\"]" --include="*.{js,ts,py}"
```

</sql_injection_risk>
</search_patterns>

<csrf_protection>
CSRF prevention requirements:

✓ Tokens in state-changing requests (POST, PUT, DELETE)
✓ Token validated server-side
✓ SameSite=Lax minimum on cookies
✓ GET requests have no side effects
</csrf_protection>

<logging_security>
<must_log>
Events that must be logged:

- Authentication events (login, logout, failed attempts)
- Authorization failures
- Sensitive data access
  </must_log>

<never_log>
Sensitive data to never log:

- Passwords, API keys, session tokens
- Full credit card numbers
- PII without masking
  </never_log>
  </logging_security>

<sources>
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [OWASP Top 10:2025](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
</sources>
