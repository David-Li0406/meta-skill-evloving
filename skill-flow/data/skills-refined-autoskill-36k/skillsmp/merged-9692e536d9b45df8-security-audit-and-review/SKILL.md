---
name: security-audit-and-review
description: Use this skill when auditing code for security issues, reviewing authentication and authorization, evaluating input validation, analyzing cryptographic usage, or checking for vulnerabilities in a codebase.
---

# Security Audit and Review Framework

This framework is designed for conducting thorough security audits and reviews of codebases, focusing on identifying vulnerabilities, insecure coding patterns, and security misconfigurations.

## When to Use

Use this skill to:
- Conduct security audits and code reviews
- Review authentication and authorization mechanisms
- Evaluate input validation and sanitization
- Analyze cryptographic implementations
- Assess dependency and supply chain security
- Perform threat modeling for new features

## Analysis Criteria

### 1. Input Validation and Sanitization

**What to check:**
- All user input is validated before use
- Validation occurs at system boundaries (API endpoints, form handlers)
- Use of schema validation libraries (e.g., Zod, Yup)
- Safe type coercion practices

**Common vulnerabilities:**
- SQL Injection, XSS, Command Injection, Path Traversal

**Look for:**
```javascript
// Dangerous patterns
query(`SELECT * FROM users WHERE id = ${userId}`)
element.innerHTML = userInput
exec(`ls ${userPath}`)
readFile(basePath + userInput)

// Safe patterns
query('SELECT * FROM users WHERE id = ?', [userId])
element.textContent = userInput
execFile('ls', [validatedPath])
readFile(path.join(basePath, path.basename(userInput)))
```

### 2. Authentication

**What to check:**
- Use of modern password hashing algorithms (bcrypt, argon2)
- Secure session management (httpOnly, secure, sameSite cookies)
- Token expiration and refresh patterns
- Multi-factor authentication support

**Warning signs:**
- Plain text password storage
- Weak hashing algorithms (MD5, SHA1)
- Session tokens in URLs

### 3. Authorization

**What to check:**
- Access control on every protected resource
- Role-based or attribute-based access control
- Server-side authorization checks

**Warning signs:**
- Missing authorization checks
- Client-side only access control

### 4. Secrets Management

**What to check:**
- No hardcoded secrets or API keys
- Use of environment variables or secret managers
- Secrets not logged or exposed in errors

**Search for patterns:**
```javascript
// Dangerous
const apiKey = "sk-1234567890abcdef"
password: "hardcoded123"

// Safe
const apiKey = process.env.API_KEY
password: config.get('db.password')
```

### 5. Data Exposure

**What to check:**
- Sensitive data not logged
- Error messages do not leak internal details
- API responses do not include unnecessary sensitive fields

### 6. HTTPS and Transport Security

**What to check:**
- All external communications use HTTPS
- Secure headers (HSTS, CSP)

### 7. Dependency Security

**What to check:**
- Dependencies are up to date
- Known vulnerabilities in dependencies (use tools like npm audit)

### 8. OWASP Top 10 Checklist

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

## Analysis Process

1. **Map attack surface**: Identify entry points (APIs, forms, file uploads)
2. **Review authentication flow**: Trace login, session, and token handling
3. **Check authorization**: Verify access control on sensitive operations
4. **Search for secrets**: Look for hardcoded credentials and keys
5. **Audit input handling**: Trace user input through the system
6. **Review dependencies**: Check for known vulnerabilities
7. **Examine error handling**: Look for information leakage
8. **Document findings**: Create a prioritized report with remediation steps

## Reporting Structure

```markdown
# Security Audit Report

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

## Rules

**ALWAYS:**
- Start with threat modeling before code review
- Map complete attack surface
- Check against all OWASP Top 10 categories
- Provide specific remediation with code

**NEVER:**
- Skip threat modeling for "simple" features
- Assume input is trustworthy
- Log sensitive data

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Database](https://cwe.mitre.org/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)