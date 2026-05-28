# GitHub Actions Security Patterns

**Category**: devops/iac-policies
**Description**: GitHub Actions workflow security and organizational policy patterns
**CWE**: CWE-78 (OS Command Injection), CWE-732 (Incorrect Permission Assignment)

---

## Action Security Patterns

### Unpinned Action Reference
**Pattern**: `(?i)uses:\s*[^@]+@(?:main|master|latest|v[0-9]+)\s*$`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Actions should be pinned to full commit SHA
- Example: `uses: actions/checkout@v4`
- Remediation: Pin to commit SHA: `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`

### Third-Party Action Without SHA
**Pattern**: `(?i)uses:\s*(?!actions/|github/)[^@\s]+@(?!sha:)[^@\s]+\s*$`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Third-party actions should be pinned to SHA
- Example: `uses: some-org/action@v1`
- Remediation: Pin to specific commit SHA for security

### Action from Untrusted Source
**Pattern**: `(?i)uses:\s*docker://[^/]+/`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Docker actions from public registries may be untrusted
- Example: `uses: docker://someimage:latest`
- Remediation: Use verified actions or self-hosted images

---

## Permission Patterns

### Write-All Permissions
**Pattern**: `(?i)permissions:\s*write-all`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, github-actions]
- Workflows should not have write-all permissions
- Example: `permissions: write-all`
- Remediation: Specify minimum required permissions

### Contents Write Permission
**Pattern**: `(?i)contents:\s*write`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Contents write allows modifying repository files
- Example: `contents: write`
- Remediation: Only use when necessary (releases, commits)

### Packages Write Permission
**Pattern**: `(?i)packages:\s*write`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Packages write allows publishing to GHCR
- Example: `packages: write`
- Remediation: Only use in publishing workflows

### ID Token Write Permission
**Pattern**: `(?i)id-token:\s*write`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- ID token write enables OIDC authentication
- Example: `id-token: write`
- Remediation: Only use with trusted cloud providers

### Missing Permission Block
**Pattern**: `(?i)^on:(?:(?!permissions:).)*jobs:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Workflows should explicitly define permissions
- Example: Workflow without permissions block
- Remediation: Add permissions block with minimum required

---

## Injection Patterns

### Script Injection via Title
**Pattern**: `(?i)\$\{\{\s*github\.event\.(?:issue|pull_request)\.title\s*\}\}`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, github-actions]
- Issue/PR titles can contain malicious content
- Example: `${{ github.event.issue.title }}`
- Remediation: Use environment variable with proper quoting

### Script Injection via Body
**Pattern**: `(?i)\$\{\{\s*github\.event\.(?:issue|pull_request|comment)\.body\s*\}\}`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, github-actions]
- Issue/PR/comment bodies can contain malicious content
- Example: `${{ github.event.pull_request.body }}`
- Remediation: Use environment variable with proper quoting

### Script Injection via Commit Message
**Pattern**: `(?i)\$\{\{\s*github\.event\.(?:head_commit|commits\[\d+\])\.message\s*\}\}`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, github-actions]
- Commit messages can contain malicious content
- Example: `${{ github.event.head_commit.message }}`
- Remediation: Use environment variable with proper quoting

### Script Injection via Branch Name
**Pattern**: `(?i)\$\{\{\s*github\.(?:head_ref|ref_name)\s*\}\}`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Branch names can contain shell metacharacters
- Example: `${{ github.head_ref }}`
- Remediation: Sanitize or use environment variable

### Unsafe Interpolation in Run
**Pattern**: `(?i)run:\s*.*\$\{\{\s*github\.event\.`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Direct interpolation in run commands is unsafe
- Example: `run: echo "${{ github.event.issue.title }}"`
- Remediation: Pass via environment variable

---

## Secret Handling Patterns

### Secret in Run Command
**Pattern**: `(?i)run:.*\$\{\{\s*secrets\.[^}]+\s*\}\}`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Secrets should be passed via environment variables
- Example: `run: curl -H "Authorization: ${{ secrets.TOKEN }}"`
- Remediation: Use env block to pass secrets

### Debug Logging with Secrets
**Pattern**: `(?i)ACTIONS_STEP_DEBUG:\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, github-actions]
- Debug logging can expose secrets
- Example: `ACTIONS_STEP_DEBUG: true`
- Remediation: Disable debug logging in production

### Secret in Output
**Pattern**: `(?i)echo\s+["']?.*\$\{\{\s*secrets\.[^}]+\s*\}\}`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Echoing secrets can expose them in logs
- Example: `echo "Token: ${{ secrets.TOKEN }}"`
- Remediation: Never echo secrets, use masking

---

## Workflow Triggers

### Pull Request Target Trigger
**Pattern**: `(?i)on:\s*\[?\s*pull_request_target`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- pull_request_target runs in base repo context with secrets
- Example: `on: pull_request_target`
- Remediation: Use pull_request unless secrets needed for forks

### Workflow Dispatch Without Inputs Validation
**Pattern**: `(?i)workflow_dispatch:(?:(?!inputs:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Manual triggers should validate inputs
- Example: workflow_dispatch without inputs
- Remediation: Add input validation with required fields

### Schedule Without Protection
**Pattern**: `(?i)schedule:\s*-\s*cron:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, github-actions]
- Scheduled workflows run on default branch
- Example: `schedule: - cron: "0 0 * * *"`
- Remediation: Ensure scheduled jobs have appropriate permissions

---

## Runner Security

### Self-Hosted Runner Without Labels
**Pattern**: `(?i)runs-on:\s*self-hosted\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Self-hosted runners should use specific labels
- Example: `runs-on: self-hosted`
- Remediation: Use `runs-on: [self-hosted, linux, x64]`

### Public Repo Self-Hosted Runner
**Pattern**: `(?i)runs-on:\s*\[?\s*self-hosted`
**Type**: regex
**Severity**: high
**Languages**: [yaml, github-actions]
- Self-hosted runners in public repos are risky
- Example: Self-hosted runner in public repository
- Remediation: Use GitHub-hosted runners for public repos

---

## Organizational Policies

### Missing Timeout
**Pattern**: `(?i)jobs:[\s\S]*?runs-on:(?:(?!timeout-minutes:).)*steps:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, github-actions]
- Jobs should have timeout to prevent stuck workflows
- Example: Job without timeout-minutes
- Remediation: Add `timeout-minutes: 30` (or appropriate)

### Missing Concurrency
**Pattern**: `(?i)^on:(?:(?!concurrency:).)*jobs:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, github-actions]
- Workflows should use concurrency to prevent duplicates
- Example: Workflow without concurrency block
- Remediation: Add concurrency group with cancel-in-progress

### Using Deprecated Node Version
**Pattern**: `(?i)node-version:\s*['"]?(?:12|14|16)['"]?`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, github-actions]
- Node.js 12/14/16 are end-of-life
- Example: `node-version: "16"`
- Remediation: Update to Node.js 18 or 20

---

## Detection Confidence

**Regex Detection**: 90%
**Security Pattern Detection**: 85%

---

## References

- GitHub Actions Security Hardening
- OWASP CI/CD Security Guide
- StepSecurity hardening recommendations
