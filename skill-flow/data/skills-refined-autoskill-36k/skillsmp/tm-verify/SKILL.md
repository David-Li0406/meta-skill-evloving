---
name: tm-verify
description: Verify that security controls documented in the threat model actually exist in the codebase. Searches for control implementations, validates configurations, identifies gaps. Use when validating threat model against code, checking security control implementation, or finding security gaps.
allowed-tools: Read, Write, Glob, Grep
---

# Control Verification

## Purpose

Verify that security controls exist in your codebase by:

- Searching for control implementations
- Validating security configurations
- Checking for security middleware/decorators
- Identifying implementation gaps
- Collecting evidence for each control

## Usage

```
/tm-verify [--control <id>] [--category <name>] [--thorough] [--evidence]
```

**Arguments**:
- `--control`: Verify specific control by ID
- `--category`: Verify controls in category (auth, crypto, access-control, etc.)
- `--thorough`: Deep code analysis
- `--evidence`: Collect code evidence for documentation

## Prerequisites

Requires threat analysis. Run `/tm-threats` first if threats.json doesn't exist.

## Control Categories

### Authentication Controls
```
Search patterns:
- passport, authenticate, login, signin
- bcrypt, argon2, scrypt, pbkdf2
- jwt, jsonwebtoken, jose
- session, cookie
- oauth, oidc, saml
- mfa, totp, 2fa, two-factor
```

### Authorization Controls
```
Search patterns:
- authorize, isAuthorized, checkPermission
- hasRole, requireRole, role
- rbac, abac, acl
- permission, policy
- canAccess, isAllowed
```

### Input Validation Controls
```
Search patterns:
- validate, validator, sanitize
- joi, yup, zod, ajv
- escape, encode
- xss, html-entities
```

### Cryptography Controls
```
Search patterns:
- crypto, cipher, encrypt, decrypt
- hash, hmac, sign, verify
- tls, ssl, https
- certificate, key, secret
```

### Rate Limiting Controls
```
Search patterns:
- rate-limit, rateLimit, throttle
- express-rate-limit
- slowDown
- quota, limit
```

### Logging/Audit Controls
```
Search patterns:
- audit, log, logger
- winston, bunyan, pino
- monitor, track
- event, activity
```

### Error Handling Controls
```
Search patterns:
- error, exception, catch
- errorHandler, onError
- try, catch, finally
```

## Verification Process

### For Each Required Control

1. **Search for implementation patterns**
   - Use Grep with control-specific patterns
   - Search in configured code paths
   - Exclude test files and node_modules

2. **Analyze findings**
   - Verify pattern matches are actual implementations
   - Check configuration completeness
   - Validate security of implementation

3. **Assess implementation status**
   - `implemented`: Control fully present and configured
   - `partial`: Control exists but incomplete
   - `planned`: Control referenced but not implemented
   - `missing`: No evidence of control

4. **Collect evidence**
   - File paths and line numbers
   - Configuration values
   - Related test files

## Output Files

### verification-report.md (Visual Report)
```markdown
# Control Verification Report

**Generated**: [Date]
**Code Paths Analyzed**: [Paths]

## Summary

```
VERIFICATION RESULTS
═══════════════════════════════════════════════════════════

Controls Analyzed: 29

STATUS BREAKDOWN
─────────────────────────────────────────────────────────
✓ Implemented │████████████████████████████████████░░░░│ 18 (62%)
⚠ Partial     │██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░│  7 (24%)
✗ Missing     │████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  4 (14%)

GAPS BY SEVERITY
─────────────────────────────────────────────────────────
CRITICAL │████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  2
    HIGH │████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  4
  MEDIUM │██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  3
     LOW │████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  2
```

## Verified Controls

| Control | Status | Evidence |
|---------|--------|----------|
| Rate Limiting | ✓ Implemented | `src/middleware/rateLimiter.ts:15` |
| JWT Auth | ✓ Implemented | `src/middleware/auth.ts:23` |
| Input Validation | ⚠ Partial | `src/validators/` (missing on 3 routes) |
| MFA | ✗ Missing | No implementation found |

## Gap Details

### GAP-001: MFA Not Enforced (HIGH)

```
┌─────────────────────────────────────────────────────────┐
│ EXPECTED: MFA required for all admin accounts           │
│ ACTUAL:   MFA optional, no enforcement check found      │
│                                                         │
│ EVIDENCE:                                               │
│   Searched: mfa, totp, 2fa, two-factor                  │
│   Found:    No matches in auth middleware               │
│                                                         │
│ REMEDIATION:                                            │
│   Add MFA verification in admin route middleware        │
│   Effort: Medium | Priority: High                       │
└─────────────────────────────────────────────────────────┘
```

[Additional gaps...]
```

### controls.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "controls": [
    {
      "id": "control-001",
      "name": "Rate Limiting on Auth Endpoints",
      "type": "preventive",
      "category": "authentication",
      "description": "Limit login attempts to prevent brute force",
      "threats_mitigated": ["threat-001", "threat-002"],
      "implementation": {
        "status": "implemented",
        "method": "express-rate-limit middleware",
        "configuration": {
          "windowMs": 60000,
          "max": 5
        }
      },
      "verification": {
        "status": "verified",
        "evidence": [
          {
            "type": "code",
            "location": "src/middleware/rateLimiter.ts:15-45",
            "verified_at": "2025-01-20T10:00:00Z"
          }
        ]
      },
      "effectiveness": 0.7
    }
  ]
}
```

### gaps.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "gaps": [
    {
      "id": "gap-001",
      "control_id": "control-002",
      "title": "MFA Not Enforced for Admin Users",
      "description": "Multi-factor authentication available but not mandatory",
      "expected": "MFA required for all privileged accounts",
      "actual": "MFA optional, enforcement check missing",
      "severity": "high",
      "evidence": {
        "code_search": "No MFA enforcement in auth middleware",
        "config_check": "MFA_REQUIRED env var not set"
      },
      "remediation": {
        "recommendation": "Add MFA enforcement check in admin routes",
        "effort": "medium",
        "priority": "high"
      },
      "related_threats": ["threat-001", "threat-003"]
    }
  ]
}
```

## Common Gap Patterns

### Authentication Gaps
- Password policy not enforced
- Session timeout not configured
- MFA not enforced
- Account lockout missing

### Authorization Gaps
- Object-level authorization missing
- Function-level access control gaps
- IDOR vulnerabilities

### Input Validation Gaps
- Unvalidated user input
- Missing output encoding
- File upload without validation

### Cryptography Gaps
- Weak algorithms in use
- Hardcoded secrets
- Missing encryption at rest

### Logging Gaps
- Security events not logged
- Sensitive data in logs
- Missing log integrity

## Instructions for Claude

When executing this skill:

1. **Load threat model state**:
   - Read `.threatmodel/state/threats.json`
   - Read `.threatmodel/config.yaml` for code paths

2. **Determine required controls**:
   - For each threat, identify needed countermeasures
   - Group by control category

3. **Search codebase for each control**:
   - Use Grep with appropriate patterns
   - Search in configured code paths
   - Exclude test/vendor directories

4. **Analyze search results**:
   - Verify matches are actual implementations
   - Check for proper configuration
   - Look for related tests

5. **Assess implementation status**:
   - Mark as implemented, partial, or missing
   - Document evidence with file:line references

6. **Identify gaps**:
   - For missing/partial controls
   - Document expected vs actual
   - Assess severity
   - Recommend remediation

7. **Write visual report file** (`.threatmodel/reports/verification-report.md`):
   - Include ASCII progress bars for status breakdown
   - Include visual gap boxes with evidence
   - Use `✓`, `⚠`, `✗` symbols
   - This file should contain ALL the visual elements, not just JSON

8. **Console summary** (also display to user):
   ```
   Control Verification Complete
   =============================

   Controls Analyzed: X

   Verification Results:
     ✓ Implemented: N
     ⚠ Partial: N
     ✗ Missing: N

   Gaps Identified:
     Critical: N
     High: N
     Medium: N
     Low: N

   Top Gaps:
     [GAP-001] HIGH: MFA not enforced
       Expected: Mandatory for admins
       Found: Optional in src/auth/mfa.ts

     [GAP-002] HIGH: SQL queries not parameterized
       Expected: Parameterized queries
       Found: Concatenation in src/legacy/reports.ts:120

   Files Updated:
     .threatmodel/state/controls.json
     .threatmodel/state/gaps.json

   Next Steps:
     Run /tm-compliance to map to frameworks
     Run /tm-report to generate risk report
   ```

## Reference Files

- [STRIDE Framework](../../shared/frameworks/stride.md)
- [OWASP Top 10](../../shared/frameworks/owasp-top10-2021.md)
