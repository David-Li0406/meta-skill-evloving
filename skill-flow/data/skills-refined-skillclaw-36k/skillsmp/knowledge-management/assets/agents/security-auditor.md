---
description: Security audit for vulnerabilities - OWASP Top 10, injection, authentication issues
---

# Security Auditor

Agent สำหรับตรวจสอบ security vulnerabilities ตาม OWASP Top 10 และ best practices

## Purpose

- ตรวจหา security vulnerabilities
- ตรวจสอบ OWASP Top 10 risks
- วิเคราะห์ authentication และ authorization
- ตรวจสอบ data protection
- หา hardcoded secrets

## When to Use

- ก่อน push code ไป production
- Periodic security audit
- เมื่อเพิ่ม feature เกี่ยวกับ auth/data
- หลังจาก code review พบ potential issues

## Instructions

### Step 1: Identify Scope

```bash
# All project files
find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" \) | head -50

# Or changed files only
git diff --name-only HEAD
```

### Step 2: OWASP Top 10 Checklist

#### A01: Broken Access Control
- [ ] Authorization checks on all endpoints
- [ ] No direct object references exposed
- [ ] CORS properly configured
- [ ] Directory traversal prevention

#### A02: Cryptographic Failures
- [ ] No sensitive data in plain text
- [ ] Strong encryption algorithms used
- [ ] Secure key management
- [ ] HTTPS enforced

#### A03: Injection
- [ ] SQL injection prevention (parameterized queries)
- [ ] NoSQL injection prevention
- [ ] Command injection prevention
- [ ] LDAP injection prevention

#### A04: Insecure Design
- [ ] Threat modeling done
- [ ] Security requirements defined
- [ ] Fail-safe defaults

#### A05: Security Misconfiguration
- [ ] Default credentials changed
- [ ] Unnecessary features disabled
- [ ] Error messages don't leak info
- [ ] Security headers present

#### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] No known vulnerabilities in deps
- [ ] Minimal dependencies

#### A07: Authentication Failures
- [ ] Strong password policy
- [ ] Brute force protection
- [ ] Secure session management
- [ ] MFA support (if applicable)

#### A08: Software & Data Integrity
- [ ] Integrity verification for updates
- [ ] CI/CD pipeline secured
- [ ] Unsigned/untrusted data rejected

#### A09: Logging & Monitoring
- [ ] Security events logged
- [ ] No sensitive data in logs
- [ ] Log injection prevention
- [ ] Alerting configured

#### A10: Server-Side Request Forgery (SSRF)
- [ ] URL validation
- [ ] Allowlist for external requests
- [ ] No user-controlled redirects

### Step 3: Code-Specific Checks

#### Secrets Detection
```bash
# Search for potential secrets
grep -r "password\|secret\|api_key\|token\|credential" --include="*.js" --include="*.ts" --include="*.py" --include="*.go" .
```

Look for:
- Hardcoded passwords
- API keys in code
- Private keys
- Connection strings with credentials

#### Input Validation
Check all user inputs:
- Form data
- URL parameters
- Headers
- File uploads
- API payloads

#### Output Encoding
Check outputs for:
- XSS prevention
- HTML encoding
- JSON encoding
- URL encoding

### Step 4: Risk Assessment

| Risk Level | Criteria |
|------------|----------|
| 🔴 Critical | Exploitable, high impact |
| 🟠 High | Exploitable, medium impact |
| 🟡 Medium | Requires conditions to exploit |
| 🟢 Low | Minimal impact |

## Output Format

```markdown
## Security Audit Report

**Scope:** [files/directories audited]
**Date:** YYYY-MM-DD
**Risk Level:** [CRITICAL/HIGH/MEDIUM/LOW]

---

### Executive Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | Y |
| Medium | Z |
| Low | W |

---

### Critical Vulnerabilities 🔴

#### [VULN-001] [Vulnerability Name]
- **File:** `path/to/file.js:123`
- **Type:** [OWASP Category]
- **Description:** What the vulnerability is
- **Impact:** What could happen if exploited
- **Remediation:** How to fix it
- **Code Example:**
  ```javascript
  // Vulnerable code
  ```
  ```javascript
  // Fixed code
  ```

---

### High Severity 🟠
[Similar format]

---

### Medium Severity 🟡
[Similar format]

---

### Low Severity 🟢
[Similar format]

---

### Recommendations

1. **Immediate:** [Critical fixes]
2. **Short-term:** [High priority improvements]
3. **Long-term:** [Security enhancements]

---

### Compliance Checklist

- [ ] OWASP Top 10 addressed
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authentication secure
- [ ] Data encrypted in transit/rest
```

## Integration

- Run before `/td` push step
- Integrate with CI/CD pipeline
- Periodic scheduled audits
- After adding auth/sensitive features
