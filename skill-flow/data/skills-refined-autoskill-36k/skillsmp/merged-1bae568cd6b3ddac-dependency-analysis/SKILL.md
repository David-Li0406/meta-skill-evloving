---
name: dependency-analysis
description: Use this skill to analyze third-party dependencies for security vulnerabilities, outdated versions, and license compliance. Ideal for auditing dependencies, reviewing new packages, or assessing supply chain security.
---

# Dependency Analysis

This skill provides automated assistance for analyzing your project's dependencies, focusing on security vulnerabilities, outdated packages, and license compliance issues.

## Core Risks

| Risk Category | Impact | Example |
|---------------|--------|---------|
| **Security** | Data breach, RCE | Known CVE in dependency |
| **Maintenance** | Future breakage | Unmaintained package |
| **License** | Legal liability | GPL in proprietary code |
| **Lock-in** | Migration cost | Deep integration with single vendor |
| **Supply Chain** | Compromise | Malicious package update |

## When to Use

- Adding new dependencies
- Regular security audits
- Preparing for production deployment
- Evaluating vendor/library choices
- License compliance review
- Investigating transitive dependencies

## Audit Workflow

### Step 1: Inventory Dependencies

```bash
# Node.js - List all dependencies
npm ls --all --depth=10 > deps.txt
npm ls --prod --depth=0  # Production only

# Python
pip list --format=freeze
pip-audit

# Go
go list -m all

# Rust
cargo tree
```

Categorize:
| Category | Count | Examples |
|----------|-------|----------|
| Direct (prod) | [N] | express, lodash |
| Direct (dev) | [N] | jest, typescript |
| Transitive | [N] | All nested deps |
| **Total** | [N] | |

### Step 2: Security Scan

```bash
# Node.js
npm audit
npm audit --json > audit.json

# Python
pip-audit
safety check

# Go
go list -json -m all | nancy sleuth

# Rust
cargo audit

# General
snyk test
trivy fs .
```

### Step 3: Analyze Health Signals

For each direct dependency, check:

| Signal | Good | Warning | Bad |
|--------|------|---------|-----|
| Last commit | <3 months | 3-12 months | >12 months |
| Open issues | Actively triaged | Backlog growing | Ignored |
| Maintainers | Multiple, active | One active | None active |
| Downloads | Growing/stable | Declining | Very low |
| GitHub stars | Appropriate to scope | N/A | Archived |
| Test coverage | Visible, high | Unknown | None |
| Security policy | SECURITY.md exists | N/A | None |

### Step 4: License Analysis

```bash
# Node.js
npx license-checker --summary
npx license-checker --production --csv > licenses.csv

# Python
pip-licenses

# Go
go-licenses csv .

# General
fossa analyze
```

### Step 5: Execute Checklist

Refer to a comprehensive audit checklist for the complete process.

## Output Format

### A) Dependency Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  DEPENDENCY OVERVIEW                         │
├─────────────────────────────────────────────────────────────┤
│ Package Manager: npm / pip / go / cargo                      │
│ Lock File: ✅ Present / ❌ Missing                           │
│                                                              │
│ Direct dependencies (prod):    [N]                           │
│ Direct dependencies (dev):     [N]                           │
│ Transitive dependencies:       [N]                           │
│ Total unique packages:         [N]                           │
│                                                              │
│ With known vulnerabilities:    [N]                           │
│ Unmaintained (>12 months):     [N]                           │
│ Deprecated:                    [N]                           │
└─────────────────────────────────────────────────────────────┘
```

### B) Security Vulnerabilities

```
┌─────────────────────────────────────────────────────────────┐
│                 SECURITY VULNERABILITIES                     │
├──────────────┬──────────┬───────────────────────────────────┤
│ Package      │ Severity │ Vulnerability                     │
├──────────────┼──────────┼───────────────────────────────────┤
│ lodash@4.17.15 │ CRITICAL │ CVE-2021-23337 - Command Injection│
│ axios@0.21.0 │ HIGH     │ CVE-2021-3749 - ReDoS             │
│ minimist@1.2.5 │ MEDIUM   │ CVE-2021-44906 - Prototype Pollution│
└──────────────┴──────────┴───────────────────────────────────┘

Remediation:
• lodash: Upgrade to 4.17.21
• axios: Upgrade to 0.21.2+
• minimist: Transitive via [parent] - update [parent]
```

### C) License Analysis

```
┌─────────────────────────────────────────────────────────────┐
│                   LICENSE SUMMARY                            │
├──────────────┬──────────────────────────────────────────────┤
│ License      │ Count    │ Risk Level                        │
├──────────────┼──────────┼───────────────────────────────────┤
│ MIT          │ 245      │ ✅ Permissive                     │
│ ISC          │ 89       │ ✅ Permissive                     │
│ Apache-2.0   │ 34       │ ✅ Permissive (patent grant)      │
│ BSD-3-Clause │ 12       │ ✅ Permissive                     │
│ GPL-3.0      │ 2        │ :red_circle: Copyleft - REVIEW!   │
│ UNKNOWN      │ 3        │ :orange_circle: Investigate       │
└──────────────┴──────────┴───────────────────────────────────┘
```

### D) Risk Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    RISK SUMMARY                              │
├─────────────────────────────────────────────────────────────┤
│ Security vulnerabilities:  [N] (Critical: X, High: Y)        │
│ Abandoned packages:        [N]                               │
│ License issues:            [N]                               │
│ High lock-in packages:     [N]                               │
├─────────────────────────────────────────────────────────────┤
│ OVERALL RISK: [LOW / MEDIUM / HIGH / CRITICAL]               │
├─────────────────────────────────────────────────────────────┤
│ Top 3 Actions:                                               │
│ 1. [Most critical action]                                    │
│ 2. [Second priority]                                         │
│ 3. [Third priority]                                          │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

- **Regular Scanning**: Schedule dependency checks regularly (e.g., weekly or monthly) to stay informed about new vulnerabilities and updates.
- **Pre-Deployment Checks**: Always run a dependency check before deploying any code to production to prevent introducing vulnerable dependencies.
- **Review and Remediation**: Carefully review the generated reports and take appropriate action to remediate identified vulnerabilities and update outdated packages.

## Integration

This skill integrates seamlessly with other tools, allowing you to use identified vulnerabilities to guide further actions, such as automatically creating pull requests to update dependencies or generating security reports for compliance purposes.

## Prerequisites

- Access to codebase and configuration files in {baseDir}/
- Security scanning tools installed as needed
- Understanding of security standards and best practices
- Permissions for security analysis operations

## Resources

- Security standard documentation (OWASP, CWE, CVE)
- Compliance framework guidelines (GDPR, HIPAA, PCI-DSS)
- Security scanning tool documentation
- Vulnerability remediation best practices