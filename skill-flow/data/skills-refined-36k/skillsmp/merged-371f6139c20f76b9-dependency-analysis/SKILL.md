---
name: dependency-analysis
description: Use this skill to analyze project dependencies for security vulnerabilities, outdated packages, and compliance issues when auditing third-party libraries or planning upgrades.
---

# Dependency Analysis Skill

## Purpose
Systematic analysis of project dependencies for security and maintenance.

## When to Use
- Security audits
- Before adding new dependencies
- Planning version upgrades
- Regular maintenance checks

## Analysis Process

### Step 1: Identify Package Manager
Detect from files:
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` → Node.js
- `requirements.txt` / `Pipfile.lock` / `poetry.lock` → Python
- `go.sum` → Go
- Other manifest files for additional languages (e.g., `composer.json`, `Gemfile`)

### Step 2: Run Security Audit
Execute appropriate command:
```bash
# Node.js
npm audit --json || yarn audit --json

# Python (if pip-audit installed)
pip-audit --format json

# Go
govulncheck ./...

# Other languages (e.g., Composer, Bundler)
# composer audit
# bundle audit
```

### Step 3: Check Outdated Packages
```bash
# Node.js
npm outdated --json

# Python
pip list --outdated --format json

# Go
go list -u -m all

# Other languages
# composer outdated --format=json
# bundle outdated
```

### Step 4: Analyze Results
Categorize findings:
- **Critical**: Security vulnerabilities with known exploits
- **High**: Security issues or major version behind
- **Medium**: Minor version behind or deprecated
- **Low**: Patch version behind

## Output Format
Generate a comprehensive report summarizing:
- Vulnerability summaries
- Detailed vulnerability information
- Outdated packages with recommended updates
- License compliance issues

## Storage Location
Save to: `docs/research/dependency-audit-{date}.md`

## Best Practices
- Schedule regular scans (e.g., weekly or monthly) to stay informed about new vulnerabilities and updates.
- Always run a dependency check before deploying any code to production.
- Review generated reports and take appropriate action to remediate identified vulnerabilities and update outdated packages.

## Error Handling
If security scanning fails:
- Verify tool installation and configuration
- Check file and directory permissions
- Validate scan target paths
- Review tool-specific error messages
- Ensure network access for dependency checks

## Resources
- Security standard documentation (OWASP, CWE, CVE)
- Compliance framework guidelines (GDPR, HIPAA, PCI-DSS)
- Security scanning tool documentation
- Vulnerability remediation best practices