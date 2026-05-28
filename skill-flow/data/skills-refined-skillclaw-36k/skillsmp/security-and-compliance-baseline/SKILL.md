---
name: security-and-compliance-baseline
description: Ensures changes respect security, privacy, and compliance constraints. Use before release.
triggers: [pre-release, external-facing, regulated-env]
outputs: [security-report, compliance-checklist]
depends_on: [regression-and-parity-check]
---

# Security and Compliance Baseline

## Purpose

Validates that all changes meet **security, privacy, and compliance requirements** before release. This skill blocks releases that introduce vulnerabilities or compliance violations.

---

## When to Use

- Before any production release
- When shipping external-facing features
- In regulated environments (healthcare, finance, etc.)
- When handling sensitive data

---

## Instructions

### 1. Identify Sensitive Data Flows

Map all data that requires protection:

```markdown
## Sensitive Data Inventory

| Data Type | Classification | Storage | Transmission | Retention |
|-----------|---------------|---------|--------------|-----------|
| Passwords | SECRET | Hashed (bcrypt) | TLS only | Never logged |
| Email | PII | Encrypted at rest | TLS only | Per policy |
| Payment | PCI | Tokenized | TLS 1.3 | 7 years |
```

### 2. Check Authentication & Authorization

```markdown
## Auth Checklist

- [x] All endpoints require authentication (except public)
- [x] Role-based access control implemented
- [x] Session tokens are secure (httpOnly, secure, sameSite)
- [x] Password policy enforced (min 12 chars, complexity)
- [x] Rate limiting on auth endpoints
- [ ] MFA available for sensitive operations
```

### 3. Enforce Least Privilege

```markdown
## Privilege Analysis

| Component | Current Access | Required Access | Status |
|-----------|---------------|-----------------|--------|
| API Server | DB read/write | DB read/write | ✅ OK |
| Worker | Full DB access | Read-only | ⚠️ OVER-PRIVILEGED |
| Frontend | Admin API | User API only | ❌ VIOLATION |
```

### 4. Flag Compliance Risks

```markdown
## Compliance Risks

| Risk ID | Category | Description | Severity | Mitigation |
|---------|----------|-------------|----------|------------|
| SEC-001 | OWASP A1 | SQL injection possible | CRITICAL | Use parameterized queries |
| SEC-002 | GDPR | PII logged in plaintext | HIGH | Mask PII in logs |
| SEC-003 | PCI-DSS | Card numbers in memory | MEDIUM | Use tokenization |
```

---

## Security Checklist

### Authentication
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Session tokens are cryptographically random
- [ ] Token expiry implemented
- [ ] Logout invalidates session

### Authorization
- [ ] RBAC or ABAC implemented
- [ ] All endpoints enforce authorization
- [ ] No privilege escalation paths
- [ ] Admin functions protected

### Data Protection
- [ ] Encryption at rest for sensitive data
- [ ] TLS for all network traffic
- [ ] PII handling per privacy policy
- [ ] Secure key management

### Input Validation
- [ ] All inputs validated
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] CSRF tokens implemented

### Logging & Monitoring
- [ ] Security events logged
- [ ] No secrets in logs
- [ ] Log integrity protected
- [ ] Alerting configured

---

## OWASP Top 10 Quick Check

| # | Vulnerability | Check | Status |
|---|--------------|-------|--------|
| A01 | Broken Access Control | Auth on all endpoints | ✅/❌ |
| A02 | Cryptographic Failures | Strong encryption | ✅/❌ |
| A03 | Injection | Parameterized queries | ✅/❌ |
| A04 | Insecure Design | Threat modeling done | ✅/❌ |
| A05 | Security Misconfiguration | Hardened configs | ✅/❌ |
| A06 | Vulnerable Components | Dependencies updated | ✅/❌ |
| A07 | Auth Failures | Strong auth implemented | ✅/❌ |
| A08 | Data Integrity Failures | Signatures verified | ✅/❌ |
| A09 | Logging Failures | Security events logged | ✅/❌ |
| A10 | SSRF | External requests validated | ✅/❌ |

---

## Integration

- **Precedes:** `delivery-readiness-gate`
- **Follows:** `regression-and-parity-check`
- **Blocks release if:** Any CRITICAL or unmitigated HIGH risks

---

## Constraints

- Security is non-negotiable
- CRITICAL issues block release immediately
- HIGH issues require mitigation plan
- All findings must be documented

Secure by default, verified before release.
