---
name: gitleaks
description: Run Gitleaks for hardcoded secrets detection in code and git history. Use when scanning for API keys, passwords, tokens, certificates, or sensitive credentials in source code and commit history.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Gitleaks Secret Detection

## When to Use Gitleaks

**Ideal scenarios:**

- Scanning for hardcoded secrets in source code
- Auditing git history for leaked credentials
- Pre-commit hooks to prevent secret commits
- CI/CD pipeline secret detection
- Finding API keys, passwords, tokens, private keys
- Compliance requirements for credential management

**Complements other tools:**

- Use before manual code review to catch obvious secrets
- Combine with SARIF Issue Reporter for detailed analysis
- Use alongside Application Inspector for comprehensive security audit

## When NOT to Use

Do NOT use this skill for:

- Code vulnerability detection (use Semgrep or CodeQL)
- Dependency scanning (use OSV-Scanner or Depscan)
- IaC security analysis (use KICS)
- Technology profiling (use Application Inspector)
- Finding secrets in binary files or compiled code

## Installation

```bash
# Homebrew (macOS/Linux)
brew install gitleaks

# Binary download
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-amd64
chmod +x gitleaks-linux-amd64
sudo mv gitleaks-linux-amd64 /usr/local/bin/gitleaks

# Docker
docker pull ghcr.io/gitleaks/gitleaks:latest

# Go install
go install github.com/gitleaks/gitleaks/v8@latest

# Verify
gitleaks version
```

## Core Workflow

### 1. Quick Scan

```bash
# Scan current directory (git repo)
gitleaks detect

# Scan specific directory
gitleaks detect --source /path/to/repo

# Scan uncommitted changes only
gitleaks protect

# Scan with no banner/color (for CI)
gitleaks detect --no-banner --no-color
```

### 2. SARIF Output

```bash
# Generate SARIF report
gitleaks detect \
  --report-format sarif \
  --report-path results.sarif

# With additional options
gitleaks detect \
  --source /path/to/repo \
  --report-format sarif \
  --report-path results.sarif \
  --no-banner \
  --no-color \
  --exit-code 0

# Redact secrets in output
gitleaks detect \
  --report-format sarif \
  --report-path results.sarif \
  --redact
```

### 3. Scan Git History

```bash
# Scan all commits
gitleaks detect --source /path/to/repo --verbose

# Scan specific commit range
gitleaks detect --log-opts="--since='2024-01-01'"

# Scan specific branch
gitleaks detect --source /path/to/repo --log-opts="origin/main"
```

### 4. Additional Formats

```bash
# JSON output
gitleaks detect --report-format json --report-path results.json

# CSV output
gitleaks detect --report-format csv --report-path results.csv

# JUnit XML
gitleaks detect --report-format junit --report-path results.xml
```

## Configuration

### Custom Config File

Create `.gitleaks.toml`:

```toml
title = "Gitleaks Configuration"

[extend]
# Extend default config
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''(?i)api[_-]?key['\"]?\s*[:=]\s*['\"]([a-z0-9]{32,})'''
keywords = ["apikey", "api_key"]

[[rules]]
id = "slack-webhook"
description = "Slack Webhook URL"
regex = '''https://hooks\.slack\.com/services/T[a-zA-Z0-9_]{8,}/B[a-zA-Z0-9_]{8,}/[a-zA-Z0-9_]{24,}'''

[[rules]]
id = "aws-access-key"
description = "AWS Access Key"
regex = '''AKIA[0-9A-Z]{16}'''
keywords = ["AKIA"]

[allowlist]
description = "Allowlist for false positives"
regexes = [
  '''EXAMPLE_API_KEY''',
  '''placeholder-secret''',
  '''test-token-123'''
]
paths = [
  '''.gitleaks.toml''',
  '''README.md''',
  '''docs/'''
]
```

### Use Custom Config

```bash
gitleaks detect --config .gitleaks.toml

# With SARIF output
gitleaks detect \
  --config .gitleaks.toml \
  --report-format sarif \
  --report-path results.sarif
```

## Ignoring False Positives

### Inline Comments

```python
# gitleaks:allow
api_key = "this-is-a-test-key-not-real"

password = "example-password"  # gitleaks:allow
```

### .gitleaksignore File

Create `.gitleaksignore`:

```
# Ignore specific findings by fingerprint
fingerprint:abc123def456

# Ignore files
tests/fixtures/secrets.txt
docs/examples/*.py

# Ignore commits
commit:a1b2c3d4e5f6
```

### Baseline Mode

```bash
# Create baseline of existing findings
gitleaks detect --report-path baseline.json --report-format json

# Scan only new findings
gitleaks detect --baseline-path baseline.json
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Gitleaks

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  gitleaks:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for complete scan

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # Optional: for Gitleaks Pro

      - name: Generate SARIF
        if: always()
        run: |
          gitleaks detect \
            --report-format sarif \
            --report-path gitleaks.sarif \
            --no-banner \
            --no-color \
            --exit-code 0

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: gitleaks.sarif
          category: gitleaks

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: gitleaks-results
          path: gitleaks.sarif
```

## Pre-commit Hook

### Install Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

# Install hook
pre-commit install

# Test
pre-commit run --all-files
```

### Manual Git Hook

```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
gitleaks protect --staged --verbose --redact
EOF

chmod +x .git/hooks/pre-commit
```

## Common Use Cases

### 1. Initial Repository Audit

```bash
# Full history scan with SARIF output
gitleaks detect \
  --source /path/to/repo \
  --report-format sarif \
  --report-path full-audit.sarif \
  --verbose

# Review results
sarif summary full-audit.sarif
```

### 2. Pre-deployment Scan

```bash
# Scan only uncommitted changes
gitleaks protect --staged --verbose

# If secrets found, prevent commit
gitleaks protect --staged --exit-code 1
```

### 3. CI/CD Pipeline Integration

```bash
# Baldwin.sh pattern
gitleaks dir \
  --source /workspace/src \
  --report-format sarif \
  --report-path /workspace/output/sarif/gitleaks.sarif \
  --no-banner \
  --no-color \
  --ignore-gitleaks-allow \
  --exit-code 0
```

### 4. Remediation Workflow

```bash
# 1. Initial scan
gitleaks detect --report-format json --report-path findings.json

# 2. Review and create baseline
gitleaks detect --report-path baseline.json --report-format json

# 3. Track only new leaks
gitleaks detect --baseline-path baseline.json --verbose

# 4. After cleanup, verify
gitleaks detect --exit-code 1  # Fail if any secrets found
```

## Understanding Output

### SARIF Structure

Gitleaks SARIF v2.1.0 includes:

- **Rules**: Each secret type (API key, password, token, etc.)
- **Results**: Specific locations where secrets were found
- **Properties**:
  - `commit`: Git commit hash (if applicable)
  - `file`: File path
  - `startLine`: Line number
  - `endLine`: Line number
  - `match`: Redacted or full secret (depending on `--redact`)
  - `secret`: The detected secret (if not redacted)

### JSON Output Example

```json
{
  "Description": "AWS Access Key",
  "StartLine": 42,
  "EndLine": 42,
  "StartColumn": 15,
  "EndColumn": 50,
  "Match": "AKIA****************",
  "Secret": "AKIA1234567890ABCDEF",
  "File": "config/aws.py",
  "SymlinkFile": "",
  "Commit": "a1b2c3d4e5f6g7h8",
  "Entropy": 4.5,
  "Author": "developer@example.com",
  "Email": "developer@example.com",
  "Date": "2024-01-15T10:30:00Z",
  "Message": "Add AWS configuration",
  "Tags": [],
  "RuleID": "aws-access-token",
  "Fingerprint": "a1b2c3d4e5f6g7h8:config/aws.py:aws-access-token:42"
}
```

## Advanced Features

### Entropy Detection

```bash
# Enable entropy scanning (experimental)
gitleaks detect --verbose --log-level debug
```

### Custom Rules Only

```bash
# Disable default rules, use custom only
gitleaks detect --config custom-rules.toml --no-default-config
```

### Scanning Specific Files

```bash
# Scan only Python files
gitleaks detect --source /code --log-opts="--all -- '*.py'"

# Exclude vendor directories
gitleaks detect --source /code --log-opts="--all -- . ':!vendor'"
```

## Performance Considerations

```bash
# Faster scans: limit git log depth
gitleaks detect --log-opts="--max-count=1000"

# Scan only recent commits
gitleaks detect --log-opts="--since='1 month ago'"

# Parallel processing (default)
gitleaks detect --source /large/repo
```

## Limitations

- **Binary files**: Limited detection in compiled/binary files
- **Obfuscation**: Misses heavily obfuscated or encoded secrets
- **Context-aware**: Can't determine if secret is actually valid/active
- **False positives**: Regex-based, may flag test data or examples
- **Git required**: Directory scans work, but git history scanning needs .git

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "Gitleaks found nothing = no secrets" | Obfuscated, encrypted, or dynamically constructed secrets are missed |
| "Only scan code, skip git history" | Secrets in history can still be exploited; attackers check git logs |
| "Disable in CI for speed" | Secret leaks are critical; speed should never compromise security |
| "Mark all as false positive" | Each finding needs review; some may be valid credentials |
| "Don't use --redact in reports" | Unredacted secrets in reports can leak to logs, artifacts, or dashboards |

## References

- Repository: <https://github.com/gitleaks/gitleaks>
- Documentation: <https://gitleaks.io/>
- Default Rules: <https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml>
- SARIF Spec: <https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html>
- Pre-commit Hook: <https://github.com/gitleaks/gitleaks#pre-commit>

