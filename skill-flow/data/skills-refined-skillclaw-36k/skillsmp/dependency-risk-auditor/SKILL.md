---
name: dependency-risk-auditor
description: Analyze third-party dependencies for security, maintenance, and lock-in risk. Use when auditing dependencies, reviewing new packages, or assessing supply chain security. Triggers on "dependency audit", "package risk", "supply chain", "vulnerable dependencies", "license check", "outdated packages", "dependency review", "npm audit", "security scan".
---

# Dependency Risk Auditor

Analyze third-party dependencies for security vulnerabilities, maintenance health, license compliance, and vendor lock-in risk.

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

# Count dependencies
npm ls --all | wc -l
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

See [LICENSE-REFERENCE.md](LICENSE-REFERENCE.md) for license compatibility.

### Step 5: Execute Checklist

See [CHECKLIST.md](CHECKLIST.md) for the complete audit checklist.

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

### C) Abandoned/Risky Dependencies

```
### :red_circle: CRITICAL RISK: [package-name]

**Version:** [version]
**Last updated:** [date]
**Weekly downloads:** [count]
**Risk factors:**
- No commits in 24+ months
- 150+ open issues, no response
- Single maintainer, no activity
- Known unfixed vulnerabilities

**Used by:** [where it's used in codebase]
**Recommendation:** Replace with [alternative]
```

```
### :orange_circle: MODERATE RISK: [package-name]

**Version:** [version]
**Last updated:** [date]
**Risk factors:**
- Declining download trend
- Bus factor of 1
- No security policy

**Recommendation:** Monitor, plan migration
```

### D) Transitive Dependency Hotspots

```
┌─────────────────────────────────────────────────────────────┐
│              TRANSITIVE HOTSPOTS                             │
│  (Packages that many direct deps depend on)                  │
├──────────────┬───────────────────────────────────────────────┤
│ Package      │ Depended on by                                │
├──────────────┼───────────────────────────────────────────────┤
│ debug@4.3.1  │ express, morgan, axios, socket.io (12 paths) │
│ ms@2.1.2     │ debug, jsonwebtoken, mongoose (8 paths)      │
│ semver@7.3.5 │ npm, pacote, libnpmexec (15 paths)           │
└──────────────┴───────────────────────────────────────────────┘

⚠️ Vulnerability in these packages has amplified impact!
```

### E) License Analysis

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

:red_circle: LICENSE ISSUES:
• gpl-package@1.0.0 - GPL-3.0 incompatible with proprietary distribution
• mystery-lib@2.0.0 - No license file, check with legal
```

### F) Lock-in Assessment

```
┌─────────────────────────────────────────────────────────────┐
│                  LOCK-IN ASSESSMENT                          │
├──────────────┬───────────────────────────────────────────────┤
│ Dependency   │ Lock-in Risk                                  │
├──────────────┼───────────────────────────────────────────────┤
│ AWS SDK      │ HIGH - Deep integration, no abstraction       │
│ Prisma       │ MEDIUM - ORM-specific schema, migrations      │
│ React        │ LOW - Standard patterns, replaceable          │
│ stripe       │ MEDIUM - Payment flows, webhook contracts     │
└──────────────┴───────────────────────────────────────────────┘

Recommendations:
• AWS SDK: Consider abstracting behind interface for multi-cloud
• Prisma: Document schema as SQL for portability
```

### G) Upgrade Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  UPGRADE PRIORITY                            │
├─────────────────────────────────────────────────────────────┤
│ IMMEDIATE (Security):                                        │
│   • lodash 4.17.15 → 4.17.21 (CVE fix)                      │
│   • axios 0.21.0 → 1.6.0 (CVE fix)                          │
│                                                              │
│ THIS SPRINT (Maintenance):                                   │
│   • typescript 4.9 → 5.3 (improved types)                   │
│   • jest 28 → 29 (performance)                              │
│                                                              │
│ NEXT QUARTER (Major):                                        │
│   • express 4 → 5 (breaking changes, plan needed)           │
│   • react 17 → 18 (concurrent features)                     │
│                                                              │
│ MONITOR (Low priority):                                      │
│   • Various patch updates                                    │
└─────────────────────────────────────────────────────────────┘
```

### H) Risk Summary

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

## Quick Commands

```bash
# Security scan
npm audit --json | jq '.vulnerabilities | keys[]'
snyk test --json

# Find outdated packages
npm outdated
pip list --outdated

# Check specific package health
npm view [package] time modified
npm view [package] maintainers

# License check
npx license-checker --production --onlyAllow "MIT;ISC;Apache-2.0;BSD-3-Clause"

# Find who depends on a package
npm ls [package]

# Dependency tree visualization
npx npm-remote-ls [package]

# Check for deprecation
npm view [package] deprecated
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete audit checklist
- [LICENSE-REFERENCE.md](LICENSE-REFERENCE.md) - License compatibility guide
