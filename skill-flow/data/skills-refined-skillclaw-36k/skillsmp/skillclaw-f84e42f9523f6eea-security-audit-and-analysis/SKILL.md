---
name: security-audit-and-analysis
description: Use this skill when you need to conduct a security audit, analyze code for vulnerabilities, or implement security best practices across applications and infrastructure.
---

# Security Audit and Analysis

This skill provides a comprehensive framework for analyzing codebases and systems for security vulnerabilities, ensuring compliance with security standards, and implementing best practices for secure coding and configuration.

## When to Use

Use this skill to:
- Conduct security audits and vulnerability assessments.
- Analyze code for security issues, including injection vulnerabilities and hardcoded secrets.
- Implement secure coding practices and manage secrets effectively.
- Ensure compliance with security standards and guidelines.

## Analysis Framework

### 1. Input Validation and Sanitization

**What to check:**
- Validate all user input before use.
- Ensure validation occurs at system boundaries (API endpoints, form handlers).
- Use schema validation libraries (e.g., Zod, Yup).

**Common vulnerabilities:**
- SQL Injection
- XSS
- Command Injection
- Path Traversal

**Safe patterns:**
```javascript
// Safe SQL query
query('SELECT * FROM users WHERE id = ?', [userId]);

// Safe HTML output
element.textContent = userInput;
```

### 2. Authentication and Authorization

**What to check:**
- Use modern password hashing algorithms (bcrypt, argon2).
- Implement secure session management (httpOnly, secure cookies).
- Ensure proper access control on all protected resources.

**Warning signs:**
- Plain text password storage.
- Missing authorization checks.

### 3. Secrets Management

**What to check:**
- Avoid hardcoded secrets and use environment variables or secret management tools.
- Regularly audit secrets and access controls.

**Example using HashiCorp Vault:**
```bash
# Store secret
vault kv put secret/myapp/database username=admin password=supersecret

# Retrieve secret
vault kv get -field=password secret/myapp/database
```

### 4. Security Scanning and Compliance

**Tools and practices:**
- Use automated tools for dependency scanning (e.g., npm audit, Snyk).
- Conduct regular security scans on code and infrastructure.
- Ensure compliance with security standards (e.g., OWASP).

**Example commands:**
```bash
# Run npm audit
npm audit --json > npm-audit.json

# Run dependency-check
dependency-check --project MyApp --scan ./src --format JSON
```

## Reporting and Remediation

1. **Identify vulnerabilities** and categorize them by severity.
2. **Document findings** and provide recommendations for remediation.
3. **Implement fixes** and verify that vulnerabilities have been addressed.

By following this framework, you can effectively analyze and improve the security posture of your applications and infrastructure.