---
name: security-scan
description: Automated security vulnerability scanning for the multi-tenant OutreachGlobal platform
---

# Security Vulnerability Scanning Instructions

## Purpose
Identify and prevent security vulnerabilities in the OutreachGlobal multi-tenant platform, with special focus on data breaches, authentication issues, and compliance violations.

## When to Use This Skill
- Code reviews and pull requests
- Before production deployments
- Security audits and compliance checks
- Investigating security incidents
- Adding new dependencies or integrations

## Critical Security Areas

### 1. Authentication & Authorization
**Check for:**
- Secure password storage (bcrypt, not plain text)
- JWT token validation and expiration
- Proper session management
- Multi-factor authentication where appropriate

**Red flags:**
```typescript
// ❌ NEVER DO THIS
const user = await db.query("SELECT * FROM users WHERE password = ?", [password]);

// ✅ DO THIS
const user = await db.query("SELECT * FROM users WHERE email = ?", [email]);
const validPassword = await bcrypt.compare(password, user.hashedPassword);
```

### 2. Data Exposure Prevention
**Multi-tenant security:**
- All queries filter by `teamId`
- No cross-tenant data access
- Secure file storage with proper permissions
- Encrypted sensitive data at rest

**Audit queries:**
```typescript
// Check for missing tenant filters
const vulnerableQueries = searchFiles({
  regex: "SELECT.*FROM.*WHERE.*[^teamId]",
  filePattern: "*.ts"
});
```

### 3. Input Validation & Sanitization
**Required for all inputs:**
- Zod schema validation on all API inputs
- SQL injection prevention (use parameterized queries)
- XSS prevention in React components
- File upload validation and scanning

### 4. API Security
**RESTful API checks:**
- Proper HTTP status codes
- Rate limiting implementation
- CORS configuration
- API key rotation and security

### 5. Infrastructure Security
**Digital Ocean specific:**
- Firewall rules restrict access
- SSL/TLS properly configured
- Environment variables not logged
- Database connections encrypted

## Common Vulnerabilities to Detect

### High Risk
1. **SQL Injection**: Raw SQL queries without parameterization
2. **Cross-Tenant Data Leak**: Missing `teamId` filters
3. **Authentication Bypass**: Weak password policies or missing validation
4. **Sensitive Data Exposure**: API keys or passwords in logs/code

### Medium Risk
1. **XSS Vulnerabilities**: Unsanitized user input in HTML
2. **CSRF Attacks**: Missing CSRF tokens on state-changing operations
3. **Insecure Dependencies**: Outdated packages with known vulnerabilities
4. **Weak Encryption**: Using deprecated encryption algorithms

### Low Risk
1. **Information Disclosure**: Error messages revealing system details
2. **Missing Security Headers**: No HSTS, CSP, etc.
3. **Insecure Defaults**: Default credentials or open ports

## Scanning Methodology

### Automated Checks
- Search for hardcoded secrets
- Validate TLS configuration
- Check dependency vulnerabilities
- Review authentication flows

### Manual Review Points
- Database query patterns
- File upload handling
- Error handling and logging
- Third-party integrations

## Compliance Considerations

### GDPR/CCPA Requirements
- Data minimization principles
- Right to erasure implementation
- Consent management
- Data processing records

### Industry Standards
- OWASP Top 10 compliance
- SOC 2 Type II readiness
- ISO 27001 alignment

## Response Format
When performing security scans, provide:
1. **Risk level** (Critical/High/Medium/Low)
2. **CVSS score** where applicable
3. **Specific code locations** with line numbers
4. **Remediation steps** with code examples
5. **Compliance impact** assessment

## Security Testing Commands
```bash
# Dependency vulnerability check
npm audit

# Secret scanning
grep -r "password\|secret\|key" --exclude-dir=node_modules .

# TLS configuration check
openssl s_client -connect your-domain.com:443
```

## Related Skills
- Use with `multi-tenant-audit` for data isolation
- Combine with `api-integration-test` for external service security
- Reference `cost-guardian` for API abuse prevention