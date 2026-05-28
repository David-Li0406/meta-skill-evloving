---
name: trivy
description: >-
  Security vulnerability scanning using Trivy for ecommerce project. Scans
  dependencies, container images, and IaC. Blocks CRITICAL and HIGH severity.
  Triggers on "trivy", "vulnerability scan", "security scan", "container scan",
  "cve", "dependency scan", "npm audit", "docker scan", "security check".
  PROACTIVE: MUST invoke before committing code with new dependencies.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Security vulnerability scanning skill using Trivy
# ABOUTME: Enforces CRITICAL/HIGH blocking before commits

# Trivy Security Scanning Skill

## Quick Reference

| Scan Type | Command | When |
|-----------|---------|------|
| Dependencies | `trivy fs .` | package.json changes |
| Container | `trivy image <name>` | Dockerfile changes |
| IaC | `trivy config .` | Terraform changes |

---

## When to Scan

| Trigger | Action |
|---------|--------|
| `package.json` changed | Scan filesystem |
| `package-lock.json` changed | Scan filesystem |
| `Dockerfile` modified | Scan config + image |
| `*.tf` files changed | Scan IaC config |
| Before commit with deps | **MANDATORY** scan |

---

## Scan Commands

### Filesystem Scan (Dependencies)

```bash
# Most common - scan Node.js dependencies
trivy fs \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --ignore-unfixed \
    --format table \
    .
```

### Container Image Scan

```bash
# Build image first
docker build -t local-scan:latest .

# Scan the image
trivy image \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --ignore-unfixed \
    local-scan:latest
```

### IaC Configuration Scan

```bash
# Scan Terraform files
trivy config \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    infra/terraform/
```

---

## Severity Policy

| Severity | Action | Commit Allowed |
|----------|--------|----------------|
| CRITICAL | **BLOCK** - Fix immediately | NO |
| HIGH | **BLOCK** - Fix or upgrade | NO |
| MEDIUM | WARN - Plan remediation | YES |
| LOW | INFO - Document | YES |

---

## Remediation Strategies

### Strategy 1: Upgrade Package

```bash
# Check which version fixes the CVE
npm audit

# Upgrade specific package
npm install package@latest

# Or use npm audit fix
npm audit fix
```

### Strategy 2: Find Fixed Version

```bash
# Show fixed versions in JSON
trivy fs --severity CRITICAL,HIGH --format json . | \
  jq '.Results[].Vulnerabilities[] | {pkg: .PkgName, installed: .InstalledVersion, fixed: .FixedVersion}'
```

### Strategy 3: Override Transitive Dependency

```json
// package.json
{
  "overrides": {
    "vulnerable-package": "^X.Y.Z"
  }
}
```

### Strategy 4: Exclude False Positive

Create `.trivyignore`:

```
# CVE-2023-XXXXX: Not exploitable - we don't use affected feature
CVE-2023-XXXXX
```

**WARNING**: Every exclusion MUST have documented justification.

---

## Ecommerce-Specific Patterns

### Backend Scan

```bash
cd apps/backend
trivy fs --severity CRITICAL,HIGH --exit-code 1 .
```

### Frontend Scan

```bash
cd apps/frontend
trivy fs --severity CRITICAL,HIGH --exit-code 1 .
```

### Docker Compose Scan

```bash
# Build all images
docker-compose -f docker-compose.full.yml build

# Scan each
trivy image ecommerce-demo-backend:latest
trivy image ecommerce-demo-frontend:latest
```

### Terraform Scan

```bash
trivy config --severity CRITICAL,HIGH infra/terraform/
```

---

## CI Integration

The project has Trivy in CI (`.github/workflows/backend-ci.yml`):

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: 'apps/backend'
    format: 'json'
    output: 'security/reports/trivy-backend-${{ github.sha }}.json'
```

Reports saved to `security/reports/` for Claude CVE analysis.

---

## CVE Analysis Workflow

When Trivy finds vulnerabilities:

1. **Get the report**
   ```bash
   trivy fs --format json --output report.json .
   ```

2. **Ask Claude to analyze**
   ```
   Analyze report.json for contextual CVE prioritization.
   For each CVE:
   - Search codebase for usage of affected library
   - Evaluate if attack vector is exposed
   - Provide remediation priority
   ```

3. **Follow remediation plan**

---

## Checklist

Before committing with dependency changes:

- [ ] Trivy installed (`brew install trivy`)
- [ ] Ran `trivy fs --severity CRITICAL,HIGH --exit-code 1 .`
- [ ] No CRITICAL vulnerabilities
- [ ] No HIGH vulnerabilities (or documented exception)
- [ ] Any `.trivyignore` entries justified
- [ ] Container images scanned (if Dockerfile changed)
- [ ] IaC scanned (if Terraform changed)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `trivy: command not found` | `brew install trivy` |
| Slow scan | Use `--skip-update` after first run |
| False positive | Add to `.trivyignore` with justification |
| Transitive dependency | Use `overrides` in package.json |
| Old DB | Run `trivy --download-db-only` |
