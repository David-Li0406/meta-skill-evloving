---
name: security-review
description: Perform OWASP Top 10 security audit, check auth/authz guards, find injection vulnerabilities, and identify data exposure. Use when reviewing security-sensitive code, before merging auth changes, or when asked to check for vulnerabilities.
---

# Security Review

Perform a comprehensive security audit focusing on OWASP Top 10 vulnerabilities and application-specific risks.

## Scope

Review the specified files or recent changes for:

### 1. Injection Vulnerabilities
- SQL injection (check Drizzle query construction)
- Command injection in Bash/shell commands
- XSS in React components (raw HTML rendering, unsanitized user input)
- Server-side template injection

### 2. Authentication & Authorization
- Verify `requireUser()` and `requireRole()` guards on all protected routes
- Check `ensureClientAccess()` usage before data queries
- Review session handling in `lib/auth/session.ts`
- Verify RLS bypass is properly handled (per CLAUDE.md: RLS is disabled, app-level guards required)

### 3. Data Exposure
- Sensitive data in API responses (passwords, tokens, PII)
- Overly permissive data fetching
- Missing field-level access control
- Secrets in client-side code or logs

### 4. Security Misconfigurations
- Missing rate limiting on sensitive endpoints
- CORS misconfigurations
- Missing security headers (CSP, X-Frame-Options)
- Environment variable exposure

### 5. Cryptographic Issues
- Weak or missing encryption
- Hardcoded secrets
- Insecure token generation

### 6. Business Logic Vulnerabilities
- Privilege escalation paths
- IDOR (Insecure Direct Object References)
- Race conditions in state changes

## Output Format

For each finding:
```
[SEVERITY: CRITICAL|HIGH|MEDIUM|LOW]
File: path/to/file.ts:lineNumber
Issue: Brief description
Risk: What could happen if exploited
Fix: Recommended remediation
```

## Actions

1. If reviewing staged changes: `git diff --cached`
2. If reviewing a PR: Use the Greptile MCP tools to fetch PR details
3. If reviewing specific files: Read and analyze each file
4. Cross-reference with `lib/auth/permissions.ts` patterns
5. Check for missing guards by comparing with similar protected routes

## Post-Review

Generate a summary with:
- Total findings by severity
- Priority remediation order
- Architectural recommendations if systemic issues found
