# CI/CD Security Patterns

## Pipeline Security

### Secure Pipeline Configuration

```yaml
# GitHub Actions - secure defaults
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read  # Minimal permissions by default

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write  # Only what's needed

    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false  # Don't persist git credentials

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production
```

### Branch Protection

```yaml
# Required branch protection rules:
# - Require pull request reviews (at least 1)
# - Require status checks to pass
# - Require signed commits
# - Do not allow force pushes
# - Do not allow deletions
# - Require linear history

# GitHub API to set protection
curl -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["build", "test", "security-scan"]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true
    },
    "restrictions": null
  }' \
  "https://api.github.com/repos/OWNER/REPO/branches/main/protection"
```

## Secrets Management

### Secure Secret Handling

```yaml
# ✅ Use encrypted secrets
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh

# ❌ Never hardcode secrets
# API_KEY: "sk_live_xxxxx"

# ❌ Never echo secrets
# run: echo ${{ secrets.API_KEY }}

# ✅ Mask additional values
- name: Mask dynamic secret
  run: |
    TOKEN=$(get-token.sh)
    echo "::add-mask::$TOKEN"
    echo "TOKEN=$TOKEN" >> $GITHUB_ENV
```

### Secret Rotation

```yaml
# Use short-lived tokens
- name: Get OIDC Token
  uses: actions/github-script@v7
  with:
    script: |
      const token = await core.getIDToken('sts.amazonaws.com');
      core.setSecret(token);
      return token;

# AWS with OIDC (no long-lived credentials)
- name: Configure AWS
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/GitHubActions
    aws-region: us-east-1
```

## Dependency Security

### Dependency Scanning

```yaml
# Dependabot configuration
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      production:
        patterns:
          - "*"
        exclude-patterns:
          - "@types/*"
          - "*-types"

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Lock File Verification

```yaml
- name: Verify lockfile
  run: |
    # Check for lockfile changes
    npm ci  # Fails if lockfile doesn't match package.json

    # Audit dependencies
    npm audit --audit-level=high

- name: Check for known vulnerabilities
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Container Security in CI

### Image Scanning

```yaml
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

### Signed Images

```yaml
- name: Sign image with cosign
  uses: sigstore/cosign-installer@v3

- name: Sign and push
  run: |
    cosign sign --key env://COSIGN_PRIVATE_KEY \
      myregistry.io/myapp:${{ github.sha }}
  env:
    COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_KEY }}

# Verify in deployment
- name: Verify signature
  run: |
    cosign verify --key cosign.pub \
      myregistry.io/myapp:${{ github.sha }}
```

## Code Security Scanning

### SAST (Static Analysis)

```yaml
- name: CodeQL Analysis
  uses: github/codeql-action/analyze@v2
  with:
    languages: javascript, python

- name: Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/secrets
      p/owasp-top-ten
```

### Secret Detection

```yaml
- name: Detect secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    extra_args: --only-verified

# Or use gitleaks
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Artifact Security

### Artifact Signing

```yaml
- name: Sign artifact
  run: |
    # Generate checksum
    sha256sum dist/* > checksums.txt

    # Sign checksums
    gpg --armor --detach-sign checksums.txt

- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: release
    path: |
      dist/
      checksums.txt
      checksums.txt.asc
```

### SBOM Generation

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: ./
    format: spdx-json
    output-file: sbom.spdx.json

- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom.spdx.json
```

## Environment Isolation

### Separate Environments

```yaml
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        env:
          API_URL: ${{ vars.STAGING_API_URL }}
          API_KEY: ${{ secrets.STAGING_API_KEY }}

  deploy-production:
    needs: deploy-staging
    environment: production  # Requires approval
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        env:
          API_URL: ${{ vars.PROD_API_URL }}
          API_KEY: ${{ secrets.PROD_API_KEY }}
```

### Self-Hosted Runner Security

```yaml
# Use labels to target secure runners
jobs:
  sensitive-job:
    runs-on: [self-hosted, secure, production]

    steps:
      # Clean workspace before/after
      - name: Clean workspace
        run: rm -rf $GITHUB_WORKSPACE/*

      - uses: actions/checkout@v4

      # ... work ...

      - name: Clean workspace after
        if: always()
        run: rm -rf $GITHUB_WORKSPACE/*
```

## Pull Request Security

### PR Validation

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      # Don't run on forks with secrets
      - name: Check fork
        if: github.event.pull_request.head.repo.fork
        run: echo "Running without secrets"

      # Validate PR source
      - name: Validate author
        uses: actions/github-script@v7
        with:
          script: |
            const author = context.payload.pull_request.user.login;
            const allowed = ['dependabot[bot]', 'renovate[bot]'];
            if (context.payload.pull_request.head.repo.fork && !allowed.includes(author)) {
              core.warning('Fork PR - running with reduced permissions');
            }
```

## Security Checklist

| Area | Check |
|------|-------|
| Secrets | Use encrypted secrets, never hardcode |
| Permissions | Minimal permissions per job |
| Dependencies | Scan, audit, lock versions |
| Images | Scan for vulnerabilities, sign |
| Artifacts | Generate checksums, SBOM |
| Branches | Require reviews, status checks |
| Runners | Isolate, clean workspaces |
| PRs | Validate source, limit fork access |

## Audit Commands

```bash
# Check GitHub Actions permissions
gh api repos/{owner}/{repo}/actions/permissions

# List secrets (names only)
gh secret list

# Check branch protection
gh api repos/{owner}/{repo}/branches/main/protection

# Review workflow runs
gh run list --workflow=ci.yml --limit=10

# Check for exposed secrets in logs
gh run view {run_id} --log | grep -i -E "(token|key|secret|password)"
```
