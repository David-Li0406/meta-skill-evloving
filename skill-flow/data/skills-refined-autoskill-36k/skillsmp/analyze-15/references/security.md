# Security Analysis Reference

## Analysis Criteria

Check for common security issues. Verify exploitability before reporting critical/high severity. This complements but does not replace SAST tools and security audits.

### Injection

- **SQL Injection**: Unsanitized input in SQL queries
- **Command Injection**: User input passed to shell commands
- **XSS**: Unescaped output in HTML/JavaScript contexts
- **Template Injection**: User input in template engines
- **Path Traversal**: Unsanitized file paths

### Authentication/Authorization

- Hardcoded credentials in source code
- Weak authentication mechanisms
- Missing authorization checks on endpoints
- Session management issues (fixation, hijacking)
- Insecure token storage (localStorage for sensitive data)
- Missing CSRF protection

### Data Exposure

- Sensitive data in logs (passwords, tokens, PII)
- Secrets in code or config files
- Insecure data transmission (HTTP for sensitive data)
- Verbose error messages revealing internals
- Debug endpoints exposed in production

### Dependencies

- Known vulnerable packages (check CVE databases)
- Outdated dependencies with security fixes
- Unused but risky dependencies

### Configuration

- Debug mode enabled in production
- Insecure defaults (weak passwords, open permissions)
- Missing security headers (CSP, HSTS, X-Frame-Options)
- CORS misconfigurations (overly permissive origins)
- Exposed admin interfaces

## OWASP Top 10 Reference

| Category                           | What to Check                                    |
| ---------------------------------- | ------------------------------------------------ |
| A01:2021 Broken Access Control     | Missing auth checks, IDOR, path traversal        |
| A02:2021 Cryptographic Failures    | Weak crypto, hardcoded secrets, insecure storage |
| A03:2021 Injection                 | SQL, command, XSS, template injection            |
| A04:2021 Insecure Design           | Logic flaws, missing security requirements       |
| A05:2021 Security Misconfiguration | Debug mode, default creds, exposed configs       |
| A06:2021 Vulnerable Components     | Outdated deps, known CVEs                        |
| A07:2021 Auth Failures             | Weak auth, session issues, credential stuffing   |
| A08:2021 Data Integrity Failures   | Insecure deserialization, unsigned data          |
| A09:2021 Logging Failures          | Missing logs, sensitive data in logs             |
| A10:2021 SSRF                      | Server-side request forgery                      |

## Severity Guidelines

- **Critical**: Actively exploitable, high impact (RCE, data breach, auth bypass)
- **High**: Exploitable with some conditions, significant impact
- **Medium**: Potential risk, limited impact, requires specific conditions
- **Low**: Best practice violation, minimal direct risk

## Notes

Include in the `notes` field when relevant:

- Vulnerability type with CWE ID (e.g., "SQL Injection (CWE-89)")
- Risk assessment: what could happen if exploited
- OWASP category reference
- Attack vector or exploitation scenario
- Related vulnerabilities in the same flow
