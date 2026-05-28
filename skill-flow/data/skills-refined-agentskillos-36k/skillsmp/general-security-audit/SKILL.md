---
name: general-security-audit
description: Workflow for auditing security vulnerabilities using trivy, osv-scanner, and trunk.
---

# General Security Audit

This skill provides a comprehensive workflow for identifying security vulnerabilities in the codebase using industry-standard tools.

## Prerequisites

Before starting the audit, ensure the following tools are installed:

- [ ] `trivy` (Container and filesystem vulnerability scanner)
- [ ] `osv-scanner` (Google's vulnerability scanner for open-source dependencies)
- [ ] `trunk` (Integrated security and linting platform)

### Tool Installation

If any tools are missing, install them using the following commands. If Homebrew (`brew`) is available, it is the recommended method.

**Using Homebrew (macOS/Linux):**

```bash
brew install trivy osv-scanner trunk
```

**Manual Installation:**

- **trivy**: [Installation Guide](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)
- **osv-scanner**: [Installation Guide](https://github.com/google/osv-scanner#installation)
- **trunk**: [Installation Guide](https://docs.trunk.io/check/installation)

## Workflow Steps

### 1. Broad Filesystem Scan (`trivy`)

Run a filesystem scan to catch vulnerabilities and hard-coded secrets in configuration files, source code, and project structure. By default, `trivy fs` scans for both vulnerabilities and secrets.

```bash
# Scan for vulnerabilities and secrets
trivy fs .

# (Optional) Scan for misconfigurations in IaC and config files
trivy config .
```

### 2. Dependency Vulnerability Scan (`osv-scanner`)

Perform a deep scan of your project's dependencies against the OSV database using the `scan source` command.

```bash
osv-scanner scan source -r .
```

### 3. Integrated Security Check (`trunk`)

Run integrated security checks. `trunk check` executes all enabled linters. You may need to enable specific security scanners like `trivy` first.

```bash
# Enable trivy if not already enabled
trunk check enable trivy

# Run security checks on modified files
trunk check

# Run on all files
trunk check --all --scope security
```

## Report Format

After running the tools, compile a report in the following structure:

### Executive Summary

[Brief overview of the security posture]

### Findings Table

| Tool        | Severity                | Component         | Description         | Recommendation   |
| ----------- | ----------------------- | ----------------- | ------------------- | ---------------- |
| [Tool Name] | [Critical/High/Med/Low] | [File/Dependency] | [Issue Description] | [Fix/Mitigation] |

### Remediation Plan

1. **Immediate Actions**: Fixes for Critical and High vulnerabilities.
2. **Follow-up**: Mitigation strategies for lower-severity issues.
3. **Prevention**: Configuration changes to prevent reintroduction.
