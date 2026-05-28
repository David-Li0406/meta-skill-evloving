---
name: security
description: Review implementation for security vulnerabilities and best practices. Checks input validation, injection prevention, auth/authz, secrets handling. Use after code review before merge.
allowed-tools: Read, Glob, Grep
user-invocable: true
---

# Security Review Skill

## Purpose

Review implementation for security vulnerabilities before approval. Produce pass/fail report with findings and recommendations.

**Key Input**: Spec group at `.claude/specs/groups/<spec-group-id>/`

## Usage

```
/security <spec-group-id>                   # Security review all changes for spec group
/security <spec-group-id> <atomic-spec-id>  # Review specific atomic spec implementation
```

## When to Use

**Mandatory for**:
- Any feature handling user input
- Authentication or authorization changes
- API endpoints or data access
- File system operations
- Database queries
- External API calls
- Cryptographic operations

**Optional for**:
- Pure UI changes with no data handling
- Documentation updates
- Test-only changes

## Review Pipeline Position

```
Implementation → Unify → Code Review → Security Review → Merge
                                            ↑
                                        You are here
```

Security review runs AFTER code review because:
- Quality issues should be fixed first
- Clean code is easier to security-review
- Separation of concerns (quality vs security)

## Prerequisites

Before security review, verify:

1. **Spec group exists** at `.claude/specs/groups/<spec-group-id>/`
2. **Code review passed** - `convergence.code_review_passed: true` in manifest
3. **All atomic specs implemented** - status is `implemented`

If prerequisites not met → STOP and run `/code-review` first.

## Security Review Process

### Step 1: Load Spec Group and Implementation Evidence

```bash
# Load manifest
cat .claude/specs/groups/<spec-group-id>/manifest.json

# Verify code review passed
# convergence.code_review_passed: true

# Load spec for context
cat .claude/specs/groups/<spec-group-id>/spec.md

# List atomic specs
ls .claude/specs/groups/<spec-group-id>/atomic/

# Build file list from Implementation Evidence in each atomic spec
```

Identify:
- Entry points (API routes, event handlers)
- Data flows (input → processing → output)
- External boundaries (user input, APIs, database)

### Step 2: Input Validation Review

Check all user inputs are validated:

```bash
# Find input sources
grep -r "req.body\|req.query\|req.params" src/ --include="*.ts"

# Check for validation
grep -r "z\.\|Zod\|validate" src/ --include="*.ts"
```

#### Validation Checklist
- [ ] All user inputs validated with schemas (Zod, Joi, etc.)
- [ ] Type validation (string, number, email, URL)
- [ ] Length limits enforced
- [ ] Whitelist validation for enums
- [ ] No raw user input passed to dangerous functions

**Good**:
```typescript
// Input validated with Zod
const LoginSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128)
});

const input = LoginSchema.parse(req.body);
```

**Bad**:
```typescript
// No validation - vulnerable
const { email, password } = req.body;
login(email, password);
```

#### Findings Format
```markdown
### Finding 1: Missing Input Validation (High)
- **File**: src/api/auth.ts:42
- **Atomic Spec**: as-002
- **Issue**: Email not validated before use
- **Risk**: Injection attacks, malformed data
- **Recommendation**: Add Zod schema validation
```

### Step 3: Injection Prevention Review

Check for SQL injection, command injection, XSS.

#### SQL Injection
```bash
# Find database queries
grep -r "db.query\|db.raw\|sql\`" src/ --include="*.ts"
```

Verify:
- [ ] Parameterized queries used (never string concatenation)
- [ ] ORM used correctly (Prisma, TypeORM)
- [ ] No raw SQL with user input

**Good**:
```typescript
// Parameterized query
const user = await db.query(
  "SELECT * FROM users WHERE email = $1",
  [email]
);
```

**Bad**:
```typescript
// SQL injection vulnerable
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);
```

#### Command Injection
```bash
# Find shell commands
grep -r "exec\|spawn\|execFile" src/ --include="*.ts"
```

Verify:
- [ ] No user input in shell commands
- [ ] If necessary, use `execFile` with array args (not `exec`)
- [ ] Whitelist validation for any user-controlled values

#### XSS (Cross-Site Scripting)
```bash
# Find HTML rendering
grep -r "innerHTML\|dangerouslySetInnerHTML" src/ --include="*.tsx"
```

Verify:
- [ ] User input properly escaped
- [ ] No `dangerouslySetInnerHTML` with user content
- [ ] Framework escaping used (React, Vue auto-escape)
- [ ] Content Security Policy headers set

### Step 4: Authentication & Authorization Review

Check auth is properly enforced.

```bash
# Find auth middleware
grep -r "authenticate\|authorize\|requireAuth" src/ --include="*.ts"

# Find protected routes
grep -r "router\.\|app\.\|@Get\|@Post" src/ --include="*.ts"
```

#### Auth Checklist
- [ ] Endpoints require authentication (except public routes)
- [ ] Authorization checks before data access
- [ ] No auth bypasses (e.g., `if (user || true)`)
- [ ] Tokens validated on every request
- [ ] Session management secure (httpOnly cookies, SameSite)

### Step 5: Secrets & Sensitive Data Review

Check secrets are not exposed.

```bash
# Find potential secrets
grep -r "password\|secret\|key\|token" src/ --include="*.ts"

# Check for hardcoded secrets
grep -r "\".*secret.*\"\|'.*secret.*'" src/ --include="*.ts"
```

#### Secrets Checklist
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] Environment variables used for secrets
- [ ] Secrets not logged
- [ ] Secrets not sent to client
- [ ] PII (Personally Identifiable Information) encrypted at rest

### Step 6: Data Protection Review

Check sensitive data is protected.

#### Encryption
- [ ] Passwords hashed (bcrypt, argon2, scrypt)
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced for transport

#### Logging
```bash
# Find logging statements
grep -r "console.log\|logger\." src/ --include="*.ts"
```

Verify:
- [ ] No PII in logs (emails, SSNs, credit cards)
- [ ] No passwords or tokens in logs
- [ ] Error messages don't leak sensitive info

### Step 7: Dependency Security Review

Check for vulnerable dependencies.

```bash
# Run security audit
npm audit

# Check for high/critical vulnerabilities
npm audit --audit-level=high
```

#### Dependency Checklist
- [ ] No known critical vulnerabilities
- [ ] Dependencies up to date
- [ ] Minimal dependency surface (only necessary packages)
- [ ] Lock file committed (package-lock.json)

### Step 8: Generate Security Report

Aggregate findings into security report.

```markdown
# Security Review Report: <spec-group-id>

**Date**: 2026-01-14
**Reviewer**: security-reviewer
**Spec Group**: .claude/specs/groups/<spec-group-id>/

## Summary: ✅ PASS

No critical or high-severity issues found. 1 medium-severity recommendation.

---

## Per Atomic Spec Review

### as-001: Logout Button UI
- **Files**: src/components/UserMenu.tsx
- **Security**: ✅ No security concerns (pure UI)

### as-002: Token Clearing
- **Files**: src/services/auth-service.ts
- **Security**: ✅ Pass
- **Notes**: Token properly cleared from localStorage

### as-003: Post-Logout Redirect
- **Files**: src/router/auth-router.ts
- **Security**: ✅ Pass
- **Notes**: Redirect uses hardcoded path (no open redirect)

### as-004: Error Handling
- **Files**: src/services/auth-service.ts
- **Security**: ⚠️ 1 Medium finding
- **Notes**: Error message could be more specific

---

## Findings

### Medium Severity

#### Finding 1: Weak Error Message
- **File**: src/services/auth-service.ts:47
- **Atomic Spec**: as-004
- **Issue**: Error message "Logout failed. Please try again." doesn't indicate cause
- **Risk**: Medium - User confusion, but no security impact
- **Recommendation**: Add specific error codes without leaking sensitive info

---

## Security Checklist

### Input Validation: ✅ Pass
- No user input in logout flow
- N/A

### Injection Prevention: ✅ Pass
- No SQL queries
- No shell commands
- No HTML rendering

### Authentication & Authorization: ✅ Pass
- Logout endpoint properly authenticated
- Token cleared after server confirms logout
- No auth bypasses

### Secrets & Sensitive Data: ✅ Pass
- No secrets in code
- Token cleared from localStorage
- No sensitive data logged

### Data Protection: ✅ Pass
- No PII handled in this feature
- Error messages generic

### Dependencies: ✅ Pass
- No new dependencies added
- Existing deps: 0 vulnerabilities

---

## Approval: ✅ CAN PROCEED

**Status**: Pass with recommendations

**Next Steps**:
1. Address medium-severity finding (optional)
2. Proceed to browser testing (if applicable)
3. Ready for commit
```

### Step 9: Handle Security Failures

If critical or high-severity issues found:

```markdown
## Summary: ❌ FAIL

**Critical issues found. DO NOT MERGE.**

---

## Critical Findings

### Finding 1: SQL Injection Vulnerability (Critical)
- **File**: src/api/users.ts:34
- **Atomic Spec**: as-002
- **Issue**: User input directly concatenated into SQL query
- **Risk**: CRITICAL - Attacker can access/modify entire database
- **POC**: `userId = "1 OR 1=1--"` returns all users
- **Recommendation**: Use parameterized query immediately
```typescript
// Fix required
const user = await db.query(
  "SELECT * FROM users WHERE id = $1",
  [userId]  // Parameterized
);
```

**Action**: STOP - Fix critical issues before proceeding.
```

**Severity levels**:
- **Critical**: Immediate data breach or system compromise risk
- **High**: Significant security risk, should be fixed before merge
- **Medium**: Security concern, should be addressed soon
- **Low**: Best practice improvement, nice to have

### Step 10: Update Manifest

Update manifest.json with security review status:

```json
{
  "convergence": {
    "security_review_passed": true
  },
  "decision_log": [
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "security_review_complete",
      "details": "0 critical, 0 high, 1 medium - PASS"
    }
  ]
}
```

## Common Vulnerabilities to Check

### OWASP Top 10

1. **Injection** (SQL, NoSQL, Command, LDAP)
2. **Broken Authentication**
3. **Sensitive Data Exposure**
4. **XML External Entities (XXE)**
5. **Broken Access Control**
6. **Security Misconfiguration**
7. **Cross-Site Scripting (XSS)**
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

## Integration with Other Skills

**Before security review**:
- Run `/unify` to ensure spec-impl-test convergence
- Run `/code-review` for code quality review

**After security review**:
- If PASS with UI changes → Proceed to `/browser-test`
- If PASS with public API → Trigger `/docs` for documentation
- If PASS (simple change, no UI, no public API) → Ready for commit
- If FAIL → Use `/implement` to fix issues, then re-run `/security`

**Documentation trigger**: If the implementation adds or modifies public APIs, user-facing features, or configuration options, dispatch the documenter subagent after security passes.

## Examples

### Example 1: Pass with No Findings

**Input**: Logout button implementation (spec group sg-logout-button)

**Security Review**:
- as-001: N/A (pure UI)
- as-002: ✅ Token cleared properly
- as-003: ✅ Hardcoded redirect (safe)
- as-004: ✅ Error handling safe

**Output**: ✅ PASS - No findings, ready for merge

### Example 2: Fail - SQL Injection

**Input**: User search endpoint (spec group sg-user-search)

**Security Review**:
- as-001: ❌ CRITICAL - SQL injection in search query

**Output**:
```markdown
❌ FAIL - Critical SQL injection vulnerability

**Finding**: User input directly in SQL query
**File**: src/api/search.ts:12
**Atomic Spec**: as-001
**Fix**: Use parameterized query

DO NOT MERGE until fixed.
```

**Action**: Fix SQL injection → Re-run security review → Pass

### Example 3: Pass with Recommendations

**Input**: Login endpoint (spec group sg-user-login)

**Security Review**:
- as-001: ⚠️ Medium - Min password length is 6 (recommend 8)
- as-002: ✅ Pass
- as-003: ✅ Pass

**Output**:
```markdown
✅ PASS with recommendations

**Finding (Medium)**: Weak password requirements
**Atomic Spec**: as-001
**Recommendation**: Increase minimum password length to 8 characters

Can proceed to merge, but recommend addressing finding in future iteration.
```
