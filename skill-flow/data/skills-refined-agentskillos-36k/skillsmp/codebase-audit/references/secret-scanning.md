# Secret Scanning Reference

Reference for: Codebase Audit

Use this when scanning for hardcoded secrets, API keys, credentials, and sensitive data in code and git history.

## TruffleHog

The primary tool for secret scanning in codebase audits.

### Installation

```bash
# macOS
brew install trufflehog

# Or via Go
go install github.com/trufflesecurity/trufflehog/v3@latest
```

### Basic Usage

```bash
# Scan current filesystem
trufflehog filesystem . --json --no-update

# Scan git repository and history
trufflehog git file://. --json --no-update

# Scan remote repository
trufflehog git https://github.com/user/repo --json --no-update

# Scan specific branch
trufflehog git file://. --branch=main --json --no-update
```

### Advanced Options

```bash
# Only verified secrets (reduces false positives)
trufflehog filesystem . --only-verified --json

# Scan since specific commit
trufflehog git file://. --since-commit=abc123 --json

# Exclude paths
trufflehog filesystem . --exclude-paths=exclude-patterns.txt --json

# Output to file
trufflehog filesystem . --json > secrets-report.json
```

### Output Format

TruffleHog JSON output includes:
- `DetectorName` - Type of secret (e.g., AWS, GitHub, Slack)
- `Raw` - The actual secret value
- `File` - File path where found
- `Line` - Line number
- `Commit` - Git commit hash (if scanning git history)
- `Verified` - Whether the secret was verified as active

## Common Secret Patterns

| Secret Type | Pattern Example | Risk Level |
|------------|----------------|-----------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | Critical |
| GitHub Token | `gh[ps]_[a-zA-Z0-9]{36}` | Critical |
| Slack Token | `xox[baprs]-[0-9a-zA-Z-]+` | High |
| Private Keys | `-----BEGIN.*PRIVATE KEY-----` | Critical |
| JWT Tokens | `eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+` | High |
| Database URLs | `postgres://user:pass@host` | Critical |
| API Keys | `api[_-]?key.*['\"]([a-zA-Z0-9]{20,})` | High |

## Integration with CI/CD

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running secret scan..."
trufflehog filesystem . --json --no-update --fail

if [ $? -ne 0 ]; then
    echo "❌ Secrets detected! Commit blocked."
    exit 1
fi
```

### GitHub Actions

```yaml
name: Secret Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
```

## Remediation Steps

When secrets are found:

1. **Rotate immediately** - Assume the secret is compromised
   ```bash
   # Example: Rotate AWS key
   aws iam delete-access-key --access-key-id AKIA...
   aws iam create-access-key --user-name username
   ```

2. **Remove from git history** - Use git-filter-repo or BFG
   ```bash
   # Install git-filter-repo
   pip install git-filter-repo

   # Remove file from history
   git filter-repo --path-glob '*secret-file*' --invert-paths

   # Force push (WARNING: rewrites history)
   git push origin --force --all
   ```

3. **Prevent recurrence** - Add to .gitignore
   ```bash
   echo ".env" >> .gitignore
   echo "*.pem" >> .gitignore
   echo "*_rsa" >> .gitignore
   echo "secrets.json" >> .gitignore
   ```

4. **Use environment variables** - Move secrets to env vars
   ```bash
   # Instead of hardcoding:
   # API_KEY = "abc123"

   # Use:
   API_KEY = os.environ.get("API_KEY")
   ```

5. **Implement secret management** - Use proper secret stores
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - GitHub Secrets (for CI/CD)

## Alternative Tools

| Tool | Best For | Installation |
|------|---------|-------------|
| **TruffleHog** | Comprehensive scanning, git history | `brew install trufflehog` |
| **Gitleaks** | Fast scanning, CI/CD integration | `brew install gitleaks` |
| **detect-secrets** | Python projects, baseline mgmt | `pip install detect-secrets` |
| **GitGuardian** | Enterprise, real-time monitoring | SaaS platform |

## Quick Comparison

**Use TruffleHog when:**
- Scanning git history comprehensively
- Need verified secret detection
- Want detailed JSON output

**Use Gitleaks when:**
- Speed is critical
- CI/CD integration
- Need SARIF output format

**Use detect-secrets when:**
- Python-focused project
- Want baseline file for known secrets
- Need custom regex patterns

## Common False Positives

Filter out test/dummy data:

```bash
# Exclude test files and fixtures
trufflehog filesystem . \
  --exclude-paths="test/**,fixtures/**,*_test.go,*.test.js" \
  --json
```

Common patterns to exclude:
- Test API keys (e.g., "test-api-key-123")
- Documentation examples
- Mock data in tests
- Placeholder values

## Quick Commands

```bash
# Full audit - filesystem + git history
trufflehog filesystem . --json --no-update > fs-secrets.json
trufflehog git file://. --json --no-update > git-secrets.json

# Check for verified secrets only
trufflehog filesystem . --only-verified --json

# Scan since last audit (assuming you tagged it)
trufflehog git file://. --since-commit=$(git rev-parse last-audit) --json
```
