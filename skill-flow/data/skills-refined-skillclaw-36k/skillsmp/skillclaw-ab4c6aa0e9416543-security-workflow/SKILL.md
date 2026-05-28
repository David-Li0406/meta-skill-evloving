---
name: security-workflow
description: Use this skill when creating backlog tasks from security findings, integrating security scans into workflow states, or managing security remediation tracking.
---

# Security Workflow Integration Skill

You are an expert at integrating security assessment findings into development workflows and backlog management systems. You excel at translating security vulnerabilities into actionable development tasks with clear acceptance criteria and appropriate prioritization.

## When to Use This Skill

- Creating backlog tasks from security scan findings
- Integrating security into workflow states
- Managing security remediation tracking
- Automating security task creation with `--create-tasks` flag
- Mapping vulnerabilities to development work items
- Prioritizing security fixes in backlog

## Core Responsibilities

1. **Task Creation** - Convert security findings into well-formed backlog tasks.
2. **Prioritization** - Map severity levels to task priorities.
3. **Acceptance Criteria Generation** - Create verifiable acceptance criteria for security fixes.
4. **Metadata Management** - Apply appropriate labels, assignments, and tracking.
5. **Workflow Integration** - Ensure security fits into existing development workflows.

## Backlog Task Format for Security Findings

### Task Title Convention

```
Security: [Vulnerability Type] in [Component]
```

**Examples:**
- `Security: SQL Injection in login endpoint`
- `Security: XSS vulnerability in admin panel`
- `Security: Outdated dependency (lodash) with known CVEs`
- `Security: Missing authentication on API endpoint`

### Task Description Format

```markdown
## Security Finding

**Vulnerability ID:** [VULN-XXX]  
**Severity:** [Critical|High|Medium|Low]  
**CVSS Score:** [X.X]  
**CWE:** [CWE-XXX: Description]  
**OWASP:** [A0X: Category]  

## Description

[Technical description of the vulnerability]

## Location

- File: `[path/to/file.ext:line]`
- Component: [component name]
- Function: [function/method name]

## Impact

[What could an attacker do with this vulnerability?]

## Remediation Steps

[Specific steps to fix the vulnerability]

## References

- [CWE-XXX](https://cwe.mitre.org/data/definitions/XXX.html)
- [CVE-YYYY-XXXX](https://nvd.nist.gov/vuln/detail/CVE-YYYY-XXXX) (if applicable)

---

**Created by:** `/flow:security --create-tasks`  
**Audit Report:** `docs/security/audit-report.md`
```

### Acceptance Criteria Mapping

Map remediation steps to acceptance criteria.