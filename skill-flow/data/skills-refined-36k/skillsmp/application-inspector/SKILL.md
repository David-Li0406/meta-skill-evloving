---
name: application-inspector
description: Run Microsoft Application Inspector for technology profiling and security feature detection. Use when analyzing technology stack, finding crypto/auth patterns, detecting sensitive API usage, or creating security posture reports.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Microsoft Application Inspector

## When to Use Application Inspector

**Ideal scenarios:**

- Technology stack profiling and discovery
- Identifying security-relevant code patterns (authentication, cryptography, logging)
- Pre-audit reconnaissance to understand codebase capabilities
- Detecting use of sensitive APIs and security controls
- Creating software composition reports
- Finding data handling patterns (PII, credentials, encryption)

**Complements other tools:**

- Use before Semgrep/CodeQL for context on what security patterns exist
- Combine with SARIF Issue Reporter for detailed findings analysis
- Use alongside SCA tools to understand both dependencies and implementation

## When NOT to Use

Do NOT use this skill for:

- Finding specific vulnerabilities (use Semgrep, CodeQL, or SAST tools)
- Dependency vulnerability scanning (use OSV-Scanner or Depscan)
- Secrets detection (use Gitleaks)
- IaC security analysis (use KICS)
- Deep data flow analysis

## Installation

```bash
# .NET tool (recommended)
dotnet tool install --global Microsoft.CST.ApplicationInspector.CLI

# Update
dotnet tool update --global Microsoft.CST.ApplicationInspector.CLI

# Verify
appinspector --version

# Docker
docker pull mcr.microsoft.com/app-inspector
docker run -v ${PWD}:/app mcr.microsoft.com/app-inspector analyze -s /app -f sarif -o /app/results.sarif
```

## Core Workflow

### 1. Quick Analysis

```bash
# Analyze directory with default rules
appinspector analyze -s /path/to/code -f html -o report.html

# Text summary
appinspector analyze -s /path/to/code -f text

# JSON output
appinspector analyze -s /path/to/code -f json -o results.json
```

### 2. SARIF Output

```bash
# Generate SARIF report
appinspector analyze -s /path/to/code \
  --output-file-format sarif \
  --output-file-path results.sarif

# With custom rules
appinspector analyze -s /path/to/code \
  -r /path/to/custom-rules \
  --output-file-format sarif \
  --output-file-path results.sarif

# Single-threaded for stability
appinspector analyze -s /path/to/code \
  --single-threaded \
  --file-timeout 500000 \
  --output-file-format sarif \
  --output-file-path results.sarif
```

### 3. Security-Focused Analysis

```bash
# Focus on security features
appinspector analyze -s /path/to/code \
  -t "Authentication,Cryptography,Authorization" \
  -f json -o security-features.json

# Exclude test files
appinspector analyze -s /path/to/code \
  -e "test,tests,spec,__pycache__" \
  -f sarif -o results.sarif
```

## Understanding Output

### Tag Categories

Application Inspector detects patterns across categories:

| Category | Examples |
|----------|----------|
| **Authentication** | OAuth, JWT, Session management, Password handling |
| **Cryptography** | AES, RSA, Hashing, Key derivation, Random generation |
| **Authorization** | RBAC, ACL, Permission checks, Policy enforcement |
| **Data.PII** | Email, SSN, Credit card, Phone numbers |
| **Data.Credentials** | API keys, Passwords, Tokens, Certificates |
| **CloudServices** | AWS, Azure, GCP API usage |
| **Framework** | Express, Django, Spring, ASP.NET |
| **Database** | SQL, NoSQL, ORM usage |

### Severity Levels

- **Critical**: High-risk patterns (hardcoded secrets, weak crypto)
- **Important**: Security-relevant code requiring review
- **Moderate**: Potentially sensitive functionality
- **ManualReview**: Patterns requiring human analysis
- **BestPractice**: Recommended patterns found

## Custom Rules

### Rule Structure

```json
{
  "name": "Detect hardcoded API keys",
  "id": "DS123456",
  "description": "Identifies potential hardcoded API keys",
  "tags": [
    "Data.Credentials.APIKey"
  ],
  "severity": "Critical",
  "patterns": [
    {
      "pattern": "api[_-]?key\\s*=\\s*['\"][a-zA-Z0-9]{20,}['\"]",
      "type": "regex",
      "confidence": "High",
      "scopes": [
        "code"
      ]
    }
  ]
}
```

### Rule File Format

Create `custom-rules.json`:

```json
[
  {
    "name": "AWS Access Key",
    "id": "DS001",
    "tags": ["Data.Credentials.AWS"],
    "severity": "Critical",
    "patterns": [
      {
        "pattern": "AKIA[0-9A-Z]{16}",
        "type": "regex",
        "confidence": "High"
      }
    ]
  }
]
```

Use with:

```bash
appinspector analyze -s /code -r custom-rules.json -f sarif -o results.sarif
```

## Verification Commands

```bash
# Verify rules
appinspector verify-rules -r /path/to/rules

# Test specific rule
appinspector verify-rules -r custom-rules.json

# List default rules
appinspector exportrules -o default-rules.json
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Application Inspector

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 1 * *'

jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0'

      - name: Install Application Inspector
        run: dotnet tool install --global Microsoft.CST.ApplicationInspector.CLI

      - name: Run Analysis
        run: |
          appinspector analyze \
            -s ${{ github.workspace }} \
            --output-file-format sarif \
            --output-file-path results.sarif \
            --single-threaded \
            --disable-archive-crawling

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
          category: application-inspector

      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: application-inspector-results
          path: results.sarif
```

## Configuration

### Performance Options

```bash
# Single-threaded (more stable)
appinspector analyze -s /code --single-threaded

# Increase timeout for large files
appinspector analyze -s /code --file-timeout 500000

# Disable archive scanning (faster)
appinspector analyze -s /code --disable-archive-crawling

# Process only specific languages
appinspector analyze -s /code -l "javascript,typescript,python"
```

### Exclusions

```bash
# Exclude paths
appinspector analyze -s /code \
  -e "node_modules,vendor,dist,build,__pycache__"

# Exclude file patterns
appinspector analyze -s /code \
  -e "*.min.js,*.test.js,*.spec.ts"
```

## Common Use Cases

### 1. Pre-Audit Technology Discovery

```bash
# Generate comprehensive technology report
appinspector analyze -s /code -f html -o tech-report.html

# Review report to understand:
# - What frameworks are used
# - What crypto libraries are present
# - How authentication is implemented
# - What cloud services are integrated
```

### 2. Security Feature Inventory

```bash
# Find all security-relevant patterns
appinspector analyze -s /code \
  -t "Authentication,Authorization,Cryptography,Data.Credentials" \
  -f json -o security-inventory.json
```

### 3. Compliance Scanning

```bash
# Detect PII handling
appinspector analyze -s /code \
  -t "Data.PII" \
  -f sarif -o pii-report.sarif

# Find credential usage
appinspector analyze -s /code \
  -t "Data.Credentials" \
  -f sarif -o credentials-report.sarif
```

### 4. Baldwin.sh Integration

```bash
# Match baldwin.sh justfile pattern
appinspector analyze \
  -s /workspace/src \
  --output-file-format sarif \
  --output-file-path /workspace/output/sarif/appinspector.sarif \
  --single-threaded \
  --file-timeout 500000 \
  --disable-archive-crawling
```

## Interpreting Results

### SARIF Structure

Application Inspector SARIF includes:

- **Rules**: Each detected pattern/tag
- **Results**: Specific code locations matching patterns
- **Properties**: Confidence, severity, tags
- **Locations**: File path, line number, code snippet

### Filter by Severity

```bash
# Use SARIF tools to filter
pip install sarif-tools

# Extract critical findings only
sarif summary results.sarif --level error

# Filter by tag
sarif filter --level error --rule-id "DS.*Credentials.*" results.sarif
```

## Limitations

- **Not a vulnerability scanner**: Identifies patterns, not exploits
- **False positives**: Regex-based detection can flag legitimate code
- **Performance**: Large codebases may require single-threaded mode
- **Language coverage**: Better for common languages (JS, Python, C#, Java)
- **No data flow**: Can't track how data moves through application

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "AppInspector found crypto, so it's secure" | Finding crypto usage doesn't mean it's implemented correctly; manual review required |
| "No credentials found = code is clean" | Pattern-based detection misses obfuscated or dynamically constructed secrets |
| "High confidence = definite issue" | High confidence means pattern match strength, not security impact |
| "Skip single-threaded mode for speed" | Multi-threaded can crash on complex codebases; stability > speed |
| "HTML report is enough" | SARIF output enables integration with other tools and automated workflows |

## References

- Repository: <https://github.com/microsoft/ApplicationInspector>
- Documentation: <https://github.com/microsoft/ApplicationInspector/wiki>
- Default Rules: <https://github.com/microsoft/ApplicationInspector/tree/main/AppInspector/rules>
- SARIF Spec: <https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html>

