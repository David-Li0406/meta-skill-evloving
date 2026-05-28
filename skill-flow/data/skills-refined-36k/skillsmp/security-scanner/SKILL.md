---
name: security-scanner
description: Comprehensive security scanner for vulnerabilities, hardcoded secrets, and OWASP Top 10 issues
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
version: 1.0.0
author: GLINCKER Team
license: Apache-2.0
keywords: [security, vulnerability, owasp, secrets, scanning]
---

# Security Scanner

Comprehensive security analysis detecting hardcoded secrets, SQL injection, XSS, insecure dependencies, and OWASP Top 10 vulnerabilities.

## What This Skill Does

- Scans for hardcoded secrets (API keys, passwords, tokens)
- Detects SQL injection vulnerabilities
- Finds XSS attack vectors
- Checks insecure dependencies
- Identifies authentication/authorization flaws
- Reviews CORS and CSP configurations
- Checks for insecure cryptography

## Instructions

### Phase 1: Secret Detection

Search for common secret patterns:

```bash
# API Keys
Grep for patterns:
- AWS: AKIA[0-9A-Z]{16}
- GitHub: ghp_[0-9a-zA-Z]{36}
- Slack: xox[baprs]-[0-9]{10,13}-[0-9a-zA-Z]{24,}
- Stripe: sk_live_[0-9a-zA-Z]{24}
- Private keys: -----BEGIN.*PRIVATE KEY-----

# Passwords
- password\s*=\s*["'][^"']+["']
- DB connection strings
- Hardcoded credentials
```

**Example findings**:
```
HIGH: Hardcoded AWS key found
File: src/config.js:12
Pattern: const AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
Risk: Exposed AWS credentials
Fix: Use environment variables or secrets manager
```

### Phase 2: Injection Vulnerabilities

**SQL Injection**:
```python
# BAD: String concatenation
query = "SELECT * FROM users WHERE id = " + user_id

# GOOD: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
```

**Command Injection**:
```javascript
// BAD: Direct execution
exec(`ls ${userInput}`)

// GOOD: Sanitized input
execFile('ls', [sanitize(userInput)])
```

**XSS Detection**:
```javascript
// BAD: innerHTML with user input
element.innerHTML = userInput

// GOOD: textContent or sanitize
element.textContent = userInput
// Or use DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput)
```

### Phase 3: Dependency Vulnerabilities

```bash
# Check for vulnerable dependencies
npm audit
pip-audit
cargo audit

# Generate report
npm audit --json > audit-report.json
```

### Phase 4: OWASP Top 10 Checks

1. **Broken Access Control**
   - Missing authorization checks
   - Insecure direct object references
   - Exposed admin endpoints

2. **Cryptographic Failures**
   - Hardcoded encryption keys
   - Weak algorithms (MD5, SHA1)
   - Unencrypted sensitive data

3. **Injection**
   - SQL, NoSQL, OS command, LDAP injection
   - Unsanitized user input

4. **Insecure Design**
   - Missing rate limiting
   - No CSRF protection
   - Weak session management

5. **Security Misconfiguration**
   - Debug mode in production
   - Default credentials
   - Unnecessary services enabled

## Scan Report Format

```markdown
# Security Scan Report

**Scan Date**: 2025-01-13
**Project**: myapp
**Total Issues**: 12

## Critical (2)
1. Hardcoded AWS credentials
   - File: config/aws.js:5
   - Risk: Full AWS account compromise
   - Fix: Use AWS IAM roles or environment variables

2. SQL Injection vulnerability
   - File: api/users.js:45
   - Code: `SELECT * FROM users WHERE id = ${userId}`
   - Fix: Use parameterized queries

## High (5)
3. XSS vulnerability in search
   - File: components/Search.jsx:23
   - Risk: Arbitrary JavaScript execution
   - Fix: Sanitize user input with DOMPurify

4. Missing authentication on /admin endpoint
   - File: routes/admin.js
   - Risk: Unauthorized access to admin functions
   - Fix: Add authentication middleware

## Medium (3)
5. Weak CORS configuration
   - File: server.js:10
   - Issue: CORS set to *
   - Fix: Whitelist specific domains

## Low (2)
6. Console.log in production
   - Multiple files
   - Risk: Information disclosure
   - Fix: Remove or use proper logging

## Recommendations
1. Implement secrets management (AWS Secrets Manager, Vault)
2. Add input validation library (joi, express-validator)
3. Enable Content Security Policy
4. Implement rate limiting
5. Add security headers (helmet.js)
```

## Auto-Fix Suggestions

```javascript
// Before (Vulnerable)
const query = `SELECT * FROM users WHERE email = '${email}'`;

// After (Fixed)
const query = 'SELECT * FROM users WHERE email = ?';
db.execute(query, [email]);
```

## Best Practices

1. **Never commit secrets**: Use .env files (in .gitignore)
2. **Sanitize all input**: Treat all user input as untrusted
3. **Use prepared statements**: Prevent SQL injection
4. **Implement CSP**: Mitigate XSS attacks
5. **Regular dependency updates**: Fix known vulnerabilities
6. **Principle of least privilege**: Minimal permissions

## Tool Requirements

- **Read**: Examine source code
- **Grep**: Pattern matching for vulnerabilities
- **Glob**: Find all relevant files
- **Bash**: Run security tools (npm audit, etc.)

## Examples

### Example 1: Quick Scan

**User**: "Scan my code for security issues"

**Output**:
- 3 Critical: Hardcoded secrets
- 5 High: SQL injection, XSS
- 2 Medium: CORS misconfiguration
- Auto-fix suggestions provided

### Example 2: Dependency Audit

**User**: "Check for vulnerable dependencies"

**Output**:
- 15 vulnerabilities found
- 10 fixable with `npm audit fix`
- 5 require manual updates

## Changelog

### Version 1.0.0
- Secret detection
- Injection vulnerability scanning
- OWASP Top 10 checks
- Dependency auditing
- Auto-fix suggestions

## Author

**GLINCKER Team**
- Repository: [claude-code-marketplace](https://github.com/GLINCKER/claude-code-marketplace)
