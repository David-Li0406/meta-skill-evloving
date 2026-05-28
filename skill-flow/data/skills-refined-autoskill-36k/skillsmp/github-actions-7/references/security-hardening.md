# Security Hardening for GitHub Actions

## Overview

Security should be a primary consideration when designing GitHub Actions workflows. This guide covers security best practices and patterns.

## Core Principles

### 1. Principle of Least Privilege

Always request the minimum permissions required:

```yaml
permissions:
  contents: read      # Only read code
  pull-requests: write  # Only comment on PRs
```

### 2. Never Hardcode Secrets

```yaml
# BAD
env:
  API_KEY: ak_live_abc123

# GOOD
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### 3. Use Pinned Action Versions

```yaml
# BAD
- uses: actions/checkout@main

# GOOD
- uses: actions/checkout@v4
```

## Security Workflows

### CodeQL Analysis

Automated static code analysis:

```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: javascript
    queries: +security-and-quality
```

### Dependency Review

Block PRs with vulnerable dependencies:

```yaml
- uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: moderate
    deny-licenses: GPL-3.0, AGPL-3.0
```

### Secret Scanning

```yaml
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Container Security

### Dockerfile Best Practices

```dockerfile
# Use specific base image tags
FROM node:20-alpine3.19

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Scan for vulnerabilities
RUN apk add --no-cache trivy && \
    trivy filesystem --exit-code 0 --no-progress / && \
    apk del trivy
```

### Container Scanning

```yaml
- name: Scan with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    format: 'sarif'
    output: 'trivy-results.sarif'
```

## Environment Protection

### Required Reviewers

Configure in repository settings:

1. Settings → Environments → New Environment
2. Add protection rules:
   - Required reviewers: `@security-team`
   - Wait timer: 30 minutes
   - Restrict to branch: `main`

### Manual Approval

```yaml
deploy-prod:
  environment:
    name: production
    url: https://prod.example.com
  runs-on: ubuntu-latest
  # Deployment pauses here for approval
```

## Secrets Management

### Organization Secrets

Share secrets across repositories:

1. Settings → Secrets and variables → Actions
2. New organization secret
3. Select repositories

### Environment Secrets

Scope secrets to environments:

```yaml
jobs:
  deploy-staging:
    environment: staging
    # Has access to staging secrets

  deploy-prod:
    environment: production
    # Has access to production secrets
```

### Secret Rotation

Implement rotation strategy:

1. Use short-lived tokens
2. Implement expiration checks
3. Rotate regularly (quarterly)
4. Document rotation procedures

## Third-Party Actions

### Verification

Before using third-party actions:

1. Check action source
2. Review action code
3. Verify publisher reputation
4. Check for recent updates

### Pinning by SHA

```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ github.sha }}  # Pin to specific commit
```

### Custom Actions

Create custom actions for sensitive operations:

```yaml
# .github/actions/deploy/action.yml
name: 'Secure Deploy'
runs:
  using: 'composite'
  steps:
    - shell: bash
      run: |
        # Custom deployment logic
        # Auditable and version-controlled
```

## Branch Protection

### Require Status Checks

```
Settings → Branches → Add rule
- Require status checks to pass before merging
- Require branches to be up to date before merging
```

### Require Pull Request Reviews

```
- Require approval from: Code owners
- Dismiss stale reviews
- Require review from CODEOWNERS file
```

## Audit and Compliance

### Action Usage Audit

```bash
# List all actions used
grep -rh "uses:" .github/workflows/ | \
  sort | uniq -c | sort -rn
```

### Permission Audit

```bash
# Check for excessive permissions
grep -A5 "permissions:" .github/workflows/*.yml | \
  grep "write:" | wc -l
```

### Compliance Reporting

```yaml
- name: Generate compliance report
  run: |
    echo "### Workflow Compliance" > report.md
    echo "- All actions pinned to versions" >> report.md
    echo "- No hardcoded secrets" >> report.md
    echo "- Least privilege permissions" >> report.md
```

## Incident Response

### Compromised Secret

1. **Immediate Actions:**
   - Revoke compromised secret
   - Rotate to new secret
   - Update workflow with new secret

2. **Investigation:**
   - Check workflow runs for suspicious activity
   - Review access logs
   - Identify affected repositories

3. **Prevention:**
   - Implement secret scanning
   - Reduce secret scope
   - Add approval requirements

## Examples

See `assets/workflows/security/` for complete security workflows.
