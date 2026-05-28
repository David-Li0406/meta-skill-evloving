# Security Best Practices for GitHub Actions

Security hardening, secret management, and secure workflow patterns for CI/CD pipelines.

---

## Permission Hardening

### Principle of Least Privilege

Start with minimal permissions and grant only what's needed:

```yaml
# Top-level: deny by default
permissions: {}

jobs:
  build:
    # Job-level: grant only what's needed
    permissions:
      contents: read  # For checkout
```

### Common Permission Levels

| Permission | Read | Write | Purpose |
|------------|------|-------|---------|
| `contents` | ✓ | | Read repository code |
| `contents` | | ✓ | Push commits/tags, create releases |
| `pull-requests` | ✓ | | Read PR data |
| `pull-requests` | | ✓ | Comment on PRs, update labels |
| `issues` | | ✓ | Create/update issues |
| `packages` | | ✓ | Publish to GitHub Packages |
| `id-token` | | ✓ | OIDC token for cloud auth |
| `actions` | ✓ | | Download artifacts from other runs |
| `checks` | | ✓ | Create check runs |

### Permission Examples

```yaml
# Read-only build job
jobs:
  build:
    permissions:
      contents: read

# Release job that creates GitHub releases
jobs:
  release:
    permissions:
      contents: write  # Create releases
      packages: write  # Publish packages

# Job that comments on PRs
jobs:
  comment:
    permissions:
      contents: read
      pull-requests: write
```

---

## Action Version Pinning

### Pinning Strategies

```yaml
# Good: Semantic version (easier to maintain)
- uses: actions/checkout@v4

# Better: Semantic version with minor (more stable)
- uses: actions/checkout@v4.1

# Best: SHA with comment (most secure)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

### When to Use Each

- **Semantic versions** (v4): First-party GitHub Actions (actions/*, github/*)
- **SHA pins**: Third-party actions from untrusted sources
- **Major versions only**: For actions you trust and want auto-updates

### Renovate/Dependabot Config

Keep pinned versions updated:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Secret Management

### Using Secrets

```yaml
- name: Deploy
  run: |
    deploy.sh
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
```

### Never Log Secrets

```yaml
# ❌ BAD: Secrets might leak in logs
- name: Deploy
  run: |
    echo "Token: ${{ secrets.API_TOKEN }}"
    curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" ...

# ✅ GOOD: Don't echo secrets, use env vars
- name: Deploy
  run: |
    echo "Deploying..."
    curl -H "Authorization: Bearer ${API_TOKEN}" ...
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
```

### Automatic Secret Redaction

GitHub automatically redacts registered secrets from logs, but:
- Only registered secrets are redacted
- Derived values (base64, reversed) are NOT redacted
- Always assume secrets might leak

### Secret Scope

- **Repository secrets**: Available to all workflows in repo
- **Environment secrets**: Only available to jobs targeting that environment
- **Organization secrets**: Shared across repos in org

Use environment secrets for production:

```yaml
jobs:
  deploy:
    environment: production  # Requires approval
    steps:
      - name: Deploy
        env:
          PROD_TOKEN: ${{ secrets.PROD_TOKEN }}
```

---

## Input Validation

### Validate External Input

Never trust user input in workflows:

```yaml
# ❌ BAD: Injection vulnerability
- name: Greet User
  run: echo "Hello ${{ github.event.issue.title }}"

# ✅ GOOD: Use environment variables
- name: Greet User
  run: echo "Hello ${ISSUE_TITLE}"
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
```

### Sanitize Filenames

```yaml
- name: Process File
  run: |
    # Validate filename
    filename="${{ github.event.inputs.filename }}"
    if [[ ! "$filename" =~ ^[a-zA-Z0-9._-]+$ ]]; then
      echo "Invalid filename"
      exit 1
    fi
    
    # Use sanitized filename
    process-file "$filename"
```

### Command Injection Prevention

```yaml
# ❌ BAD: Command injection possible
- run: |
    curl https://api.example.com/${{ github.event.issue.number }}

# ✅ GOOD: Use environment variables
- run: |
    curl "https://api.example.com/${ISSUE_NUMBER}"
  env:
    ISSUE_NUMBER: ${{ github.event.issue.number }}
```

---

## Pull Request Security

### Dangerous Events

Be careful with these triggers on public repos:

```yaml
# ⚠️ DANGEROUS: Runs untrusted code from PR
on:
  pull_request_target:  # Has write access to repo
  workflow_run:         # Runs after PR workflow

# ✅ SAFE: Runs in PR context (fork)
on:
  pull_request:  # Read-only for forks
```

### Pull Request Permissions

```yaml
# Safe for pull_request
on:
  pull_request:

permissions:
  contents: read  # Can only read code

# Dangerous for pull_request_target
on:
  pull_request_target:

permissions:
  contents: read  # Still has write if malicious
```

### Safe PR Workflow Pattern

```yaml
# workflow-1.yml - Runs untrusted code
on:
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-results
          path: results.json

# workflow-2.yml - Has permissions, uses trusted artifact
on:
  workflow_run:
    workflows: ["workflow-1"]
    types: [completed]

permissions:
  pull-requests: write

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-results
      - run: gh pr comment ...
```

---

## Token Security

### GitHub Token

The automatic `GITHUB_TOKEN` has limited permissions:

```yaml
# Automatic token with job permissions
- name: Create Release
  env:
    GITHUB_TOKEN: ${{ github.token }}

# Or secrets.GITHUB_TOKEN (same thing)
- name: Create Release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**GITHUB_TOKEN limitations:**
- Cannot trigger other workflows
- Limited to current repository
- Expires after job completes

### Personal Access Tokens (PATs)

Use PATs when you need to:
- Trigger other workflows
- Access other repositories
- Perform actions not available to GITHUB_TOKEN

```yaml
- name: Trigger Other Workflow
  run: |
    gh workflow run other-workflow.yml
  env:
    GH_TOKEN: ${{ secrets.PAT_TOKEN }}
```

**PAT Security:**
- Store as repository secret
- Use fine-grained PATs (not classic)
- Set minimum scope (e.g., `contents: read`)
- Set expiration date
- Rotate regularly

---

## Script Injection Prevention

### Direct Expression Evaluation

```yaml
# ❌ VULNERABLE: Script injection
- name: Print Issue Title
  run: echo "${{ github.event.issue.title }}"

# If title is: `"; malicious-command; echo "`
# Expands to: echo ""; malicious-command; echo ""
```

### Safe Patterns

**Pattern 1: Environment Variables**

```yaml
# ✅ SAFE: Use environment variables
- name: Print Issue Title
  run: echo "${ISSUE_TITLE}"
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
```

**Pattern 2: Actions (preferred)**

```yaml
# ✅ SAFE: Use actions instead of shell
- name: Comment on PR
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        body: context.payload.comment.body
      })
```

---

## Third-Party Actions

### Vetting Third-Party Actions

Before using:
1. Check repository popularity (stars, forks)
2. Review recent commits and maintainer activity
3. Look for security policy and vulnerability disclosure
4. Check if used by reputable organizations
5. Review the action's code (especially marketplace actions)
6. Pin to specific SHA, not tag

### Allowed Third-Party Actions

Configure in repository settings:

```yaml
# .github/workflows/allowed-actions.yml
allowed_actions:
  github_owned_allowed: true
  verified_allowed: true
  patterns_allowed:
    - "actions/*"
    - "goreleaser/goreleaser-action@*"
```

---

## Network Security

### Restrict Network Access

```yaml
# Only allow specific domains
- name: Download Dependencies
  run: |
    npm config set registry https://registry.npmjs.org/
    npm ci
```

### Verify Checksums

```yaml
- name: Download and Verify
  run: |
    curl -L https://example.com/tool.tar.gz -o tool.tar.gz
    echo "expected-sha256  tool.tar.gz" | sha256sum -c -
    tar xzf tool.tar.gz
```

---

## Artifact Security

### Secure Artifact Upload

```yaml
- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: dist/
    retention-days: 1  # Don't keep sensitive data long
    if-no-files-found: error
```

### Artifact Permissions

Artifacts inherit workflow permissions:
- Public repos: Artifacts visible to public
- Private repos: Artifacts visible to repo members
- Fork PRs: Artifacts not accessible to fork

### Don't Upload Secrets

```yaml
# ❌ BAD: Don't upload secret files
- uses: actions/upload-artifact@v4
  with:
    name: config
    path: .env  # Contains secrets!

# ✅ GOOD: Use secrets, not files
- run: deploy.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

---

## Security Checklist

- [ ] Use `permissions: {}` at top level
- [ ] Grant minimal permissions per job
- [ ] Pin third-party actions to SHA
- [ ] Never log secrets
- [ ] Use environment variables for external input
- [ ] Validate all external input
- [ ] Use `pull_request`, not `pull_request_target` for untrusted code
- [ ] Set short retention for sensitive artifacts
- [ ] Rotate secrets regularly
- [ ] Use fine-grained PATs, not classic
- [ ] Review third-party actions before use
- [ ] Verify checksums for downloads
- [ ] Keep actions updated with Dependabot/Renovate

---

## Security Resources

- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OpenSSF Scorecards](https://securityscorecards.dev/)
- [StepSecurity Action Security](https://www.stepsecurity.io/)
