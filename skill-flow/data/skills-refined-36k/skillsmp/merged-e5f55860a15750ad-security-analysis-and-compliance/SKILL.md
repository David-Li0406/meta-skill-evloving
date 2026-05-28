---
name: security-analysis-and-compliance
description: Use this skill when you need to analyze code for security vulnerabilities, perform security audits, manage secrets, or ensure compliance with security best practices.
---

# Security Analysis and Compliance

This skill provides a comprehensive framework for analyzing codebases for security vulnerabilities, implementing security controls, and ensuring compliance with best practices.

## When to Use

Use this skill to:
- Analyze code for security vulnerabilities and insecure coding patterns.
- Conduct security audits and vulnerability assessments.
- Manage secrets and secure configurations.
- Implement security best practices and compliance measures.

## Analysis Criteria

### 1. Input Validation and Sanitization

**What to check:**
- All user input is validated before use.
- Validation occurs at system boundaries (API endpoints, form handlers).
- Schema validation using libraries (e.g., Zod, Yup).
- Safe type coercion.

**Common vulnerabilities:**
- SQL Injection, XSS, Command Injection, Path Traversal.

**Look for:**
```javascript
// Dangerous patterns
query(`SELECT * FROM users WHERE id = ${userId}`)
element.innerHTML = userInput
exec(`ls ${userPath}`)

// Safe patterns
query('SELECT * FROM users WHERE id = ?', [userId])
element.textContent = userInput
execFile('ls', [validatedPath])
```

### 2. Authentication

**What to check:**
- Use of modern password hashing algorithms (bcrypt, argon2).
- Secure session management (httpOnly, secure cookies).
- Token expiration and refresh patterns.
- Multi-factor authentication support.

**Warning signs:**
- Plain text password storage, weak hashing algorithms, session tokens in URLs.

### 3. Authorization

**What to check:**
- Access control on every protected resource.
- Role-based or attribute-based access control.
- Server-side authorization checks.

**Warning signs:**
- Missing authorization checks, overly permissive default access.

### 4. Secrets Management

**What to check:**
- No hardcoded secrets or API keys.
- Use of environment variables or secret managers.
- Secrets not logged or exposed in errors.

**Search for patterns:**
```javascript
// Dangerous
const apiKey = "sk-1234567890abcdef"

// Safe
const apiKey = process.env.API_KEY
```

### 5. Data Exposure

**What to check:**
- Sensitive data not logged.
- Error messages do not leak internal details.
- API responses do not include unnecessary sensitive fields.

### 6. HTTPS and Transport Security

**What to check:**
- All external communications use HTTPS.
- Secure headers (HSTS, CSP).

### 7. Dependency Security

**What to check:**
- Dependencies are up to date.
- Known vulnerabilities in dependencies (npm audit, etc.).

## Security Scanning

### Static Application Security Testing (SAST)

```yaml
# GitHub Actions - CodeQL
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: javascript, python

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v3
```

### Dependency Scanning

```bash
# npm audit
npm audit --json > npm-audit.json
```

## OWASP Top 10 Checklist

1. **Broken Access Control**
2. **Cryptographic Failures**
3. **Injection**
4. **Insecure Design**
5. **Security Misconfiguration**
6. **Vulnerable Components**
7. **Authentication Failures**
8. **Data Integrity Failures**
9. **Logging Failures**
10. **SSRF**

## Report Structure

```markdown
# Security Analysis Report

## Risk Summary

[High/Medium/Low overall risk assessment]

## Critical Findings

[Issues requiring immediate attention]

### Finding 1: [Title]

- **Severity**: Critical/High/Medium/Low
- **Location**: [file:line]
- **Description**: [What the issue is]
- **Impact**: [What could happen if exploited]
- **Recommendation**: [How to fix]

## Security Strengths

[Positive security patterns found]

## Recommendations by Priority

### Immediate Actions

[Critical fixes needed now]

### Short-term Improvements

[Important but less urgent]

### Long-term Hardening

[Defense in depth improvements]

## OWASP Top 10 Assessment

[Status for each category]
```

## Security Monitoring

### Security Events to Monitor

| Event | Priority | Action |
|-------|----------|--------|
| Multiple failed logins | High | Alert, temp block |
| Privilege escalation | Critical | Alert, investigate |

## Additional Resources

### Reference Files

- **`references/owasp-cheatsheets.md`** - OWASP prevention guides
- **`references/security-headers.md`** - HTTP security headers reference

### Example Files

- **`examples/security-scan-pipeline.yml`** - CI security scanning workflow