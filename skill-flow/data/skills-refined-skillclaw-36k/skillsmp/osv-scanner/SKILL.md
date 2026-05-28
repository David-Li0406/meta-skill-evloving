---
name: osv-scanner
description: Run Google OSV-Scanner for Software Composition Analysis (SCA) and vulnerability detection in dependencies. Use when scanning package manifests, lock files, SBOMs, or container images for known vulnerabilities.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Google OSV-Scanner - Vulnerability Detection for Dependencies

## When to Use OSV-Scanner

**Ideal scenarios:**

- Software Composition Analysis (SCA)
- Dependency vulnerability scanning
- License compliance checking
- SBOM (Software Bill of Materials) analysis
- Container image vulnerability scanning
- Supply chain security assessment
- CI/CD security gates for dependencies
- Open source risk management

**Complements other tools:**

- Use alongside code scanners (Semgrep, CodeQL) for complete coverage
- Combine with Depscan for enhanced SCA capabilities
- Use with SARIF Issue Reporter for findings analysis
- Pair with Gitleaks for secrets + dependency security

## When NOT to Use

Do NOT use this skill for:

- Application code vulnerability scanning (use Semgrep or CodeQL)
- Secrets detection (use Gitleaks)
- IaC security analysis (use KICS)
- API endpoint discovery (use Noir)
- Custom/proprietary code analysis

## Installation

```bash
# Go install
go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Homebrew
brew install osv-scanner

# Download binary (Linux)
wget https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64
chmod +x osv-scanner_linux_amd64
sudo mv osv-scanner_linux_amd64 /usr/local/bin/osv-scanner

# Download binary (macOS)
wget https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_darwin_amd64
chmod +x osv-scanner_darwin_amd64
sudo mv osv-scanner_darwin_amd64 /usr/local/bin/osv-scanner

# Docker
docker pull ghcr.io/google/osv-scanner:latest

# Verify
osv-scanner --version
```

## Core Workflow

### 1. Quick Scan

```bash
# Scan current directory
osv-scanner scan .

# Scan specific directory
osv-scanner scan /path/to/project

# Recursive scan
osv-scanner scan -r /path/to/project

# Scan multiple paths
osv-scanner scan ./app ./services ./libs
```

### 2. SARIF Output

```bash
# Generate SARIF report
osv-scanner scan --format sarif /path/to/project > results.sarif

# Named output file
osv-scanner scan --format sarif -o results.sarif /path/to/project

# Quiet mode with SARIF
osv-scanner scan -q --format sarif /path/to/project > results.sarif
```

### 3. Scan Specific Files

```bash
# Package manifest files
osv-scanner scan --lockfile package-lock.json
osv-scanner scan --lockfile Gemfile.lock
osv-scanner scan --lockfile requirements.txt
osv-scanner scan --lockfile go.mod
osv-scanner scan --lockfile Cargo.lock
osv-scanner scan --lockfile composer.lock
osv-scanner scan --lockfile pom.xml

# Multiple lock files
osv-scanner scan \
  --lockfile package-lock.json \
  --lockfile go.mod \
  --lockfile requirements.txt
```

### 4. SBOM Scanning

```bash
# Scan CycloneDX SBOM
osv-scanner scan --sbom sbom.json

# Scan SPDX SBOM
osv-scanner scan --sbom sbom.spdx.json

# Multiple SBOMs
osv-scanner scan --sbom app-sbom.json --sbom lib-sbom.json
```

### 5. Container Image Scanning

```bash
# Scan Docker image
osv-scanner scan --docker nginx:latest

# Scan local image
osv-scanner scan --docker my-app:1.0.0

# Export to SARIF
osv-scanner scan --docker my-app:1.0.0 --format sarif -o results.sarif
```

## Supported Ecosystems

| Ecosystem | Manifest Files | Lock Files |
|-----------|----------------|------------|
| **npm** | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| **Python** | requirements.txt, setup.py | Pipfile.lock, poetry.lock, pdm.lock |
| **Go** | go.mod | go.sum |
| **Rust** | Cargo.toml | Cargo.lock |
| **Java/Maven** | pom.xml | - |
| **Ruby** | Gemfile | Gemfile.lock |
| **PHP** | composer.json | composer.lock |
| **.NET** | packages.config, *.csproj | packages.lock.json |
| **Pub (Dart)** | pubspec.yaml | pubspec.lock |
| **CocoaPods** | Podfile | Podfile.lock |

## Output Formats

```bash
# Table format (default, human-readable)
osv-scanner scan /path/to/project

# JSON output
osv-scanner scan --format json /path/to/project

# SARIF output (for CI/CD integration)
osv-scanner scan --format sarif /path/to/project

# Markdown output
osv-scanner scan --format markdown /path/to/project

# Vertical format (detailed)
osv-scanner scan --format vertical /path/to/project
```

## Advanced Options

### Severity Filtering

```bash
# Show all severities (default)
osv-scanner scan /path/to/project

# Exit with error on any vulnerability
osv-scanner scan --fail-on-vuln /path/to/project

# Custom exit code
osv-scanner scan --exit-code 2 /path/to/project
```

### Offline Mode

```bash
# Download vulnerability database
osv-scanner scan --download-databases /path/to/db

# Use offline database
osv-scanner scan --offline --db-path /path/to/db /path/to/project
```

### Call Analysis (Experimental)

```bash
# Enable call analysis to reduce false positives
osv-scanner scan --experimental-call-analysis /path/to/project

# Requires source code analysis to determine if vulnerable code is actually used
```

### License Scanning

```bash
# Include license information
osv-scanner scan --experimental-licenses /path/to/project

# Output licenses only
osv-scanner scan --experimental-licenses --format json /path/to/project | jq '.licenses'
```

## CI/CD Integration (GitHub Actions)

```yaml
name: OSV-Scanner

on:
  push:
    branches: [main]
    paths:
      - '**/package*.json'
      - '**/requirements*.txt'
      - '**/go.mod'
      - '**/Cargo.lock'
      - '**/Gemfile.lock'
      - '**/composer.lock'
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  osv-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run OSV-Scanner
        uses: google/osv-scanner-action@v2
        with:
          scan-args: |-
            --recursive
            --format sarif
            --output results.sarif
            ./

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
          category: osv-scanner

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: osv-scanner-results
          path: results.sarif
```

## Configuration

### Ignore Vulnerabilities

Create `osv-scanner.toml`:

```toml
# Ignore specific vulnerabilities
[[IgnoredVulns]]
id = "CVE-2024-12345"
reason = "False positive - not used in our code path"
expiry = "2025-12-31"

[[IgnoredVulns]]
id = "GHSA-xxxx-yyyy-zzzz"
reason = "Accepted risk - fix scheduled for Q2"

# Ignore specific packages
[[PackageOverrides]]
name = "lodash"
version = "4.17.19"
ignore = true
reason = "Locked to specific version for compatibility"
```

Use config:

```bash
osv-scanner scan --config osv-scanner.toml /path/to/project
```

### Inline Ignores

```bash
# Scan and create ignore file from results
osv-scanner scan --json /path/to/project > vulnerabilities.json

# Review and selectively ignore
# Edit osv-scanner.toml based on vulnerabilities.json

# Rescan with ignores
osv-scanner scan --config osv-scanner.toml /path/to/project
```

## Common Use Cases

### 1. Pre-commit Dependency Check

```bash
# Scan staged lock files
git diff --cached --name-only | grep -E '(package-lock\.json|go\.sum|Cargo\.lock)' | \
  xargs -I {} osv-scanner scan --lockfile {}
```

### 2. Container Image Security

```bash
# Before deployment
osv-scanner scan --docker myapp:latest --format sarif -o image-vulns.sarif

# Fail build on vulnerabilities
osv-scanner scan --docker myapp:latest --fail-on-vuln || exit 1
```

### 3. SBOM Analysis

```bash
# Generate SBOM
syft dir:/path/to/project -o cyclonedx-json > sbom.json

# Scan SBOM for vulnerabilities
osv-scanner scan --sbom sbom.json --format sarif -o vuln-report.sarif

# Combine for complete view
sarif summary vuln-report.sarif
```

### 4. Multi-language Project

```bash
# Scan entire monorepo
osv-scanner scan -r /monorepo --format sarif -o complete-scan.sarif

# Per-language breakdown
osv-scanner scan --lockfile frontend/package-lock.json --format json > npm-vulns.json
osv-scanner scan --lockfile backend/go.mod --format json > go-vulns.json
osv-scanner scan --lockfile api/requirements.txt --format json > python-vulns.json
```

### 5. Baldwin.sh Integration

```bash
# Match baldwin.sh justfile pattern
osv-scanner scan \
  -r /workspace/src \
  --format sarif \
  > /workspace/output/sarif/osv-scanner.sarif
```

## Understanding Output

### SARIF Structure

OSV-Scanner SARIF v2.1.0 includes:

- **Rules**: Each vulnerability (CVE, GHSA, etc.)
- **Results**: Each vulnerable dependency instance
- **Properties**:
  - Package name and version
  - Vulnerability ID (CVE, GHSA)
  - Severity (if available from advisory)
  - CVSS scores
  - Fix versions
  - Affected versions
  - References and links

### Vulnerability Information

Each finding includes:

- **ID**: CVE-YYYY-NNNNN or GHSA-xxxx-yyyy-zzzz
- **Summary**: Brief vulnerability description
- **Details**: Comprehensive explanation
- **Affected**: Package name and version range
- **Fixed**: Version that fixes the vulnerability
- **Severity**: CRITICAL, HIGH, MODERATE, LOW
- **CVSS**: Score and vector if available
- **References**: Links to advisories, patches, discussions

## Remediation Workflow

### Step 1: Identify

```bash
osv-scanner scan --format json /path/to/project > vulns.json
```

### Step 2: Prioritize

```bash
# Extract critical/high severity
jq '.results[] | select(.vulnerability.severity == "HIGH" or .vulnerability.severity == "CRITICAL")' vulns.json

# Group by package
jq -r '.results[] | "\(.package.name): \(.vulnerability.id)"' vulns.json | sort | uniq -c
```

### Step 3: Fix

```bash
# Review fix versions
jq -r '.results[] | "\(.package.name)@\(.package.version) -> Fix: \(.vulnerability.fixed)"' vulns.json

# Update dependencies
npm update
pip install --upgrade -r requirements.txt
go get -u
cargo update
```

### Step 4: Verify

```bash
# Rescan after fixes
osv-scanner scan /path/to/project --format sarif -o post-fix.sarif

# Compare before/after
diff <(jq -r '.runs[].results[].ruleId' pre-fix.sarif | sort) \
     <(jq -r '.runs[].results[].ruleId' post-fix.sarif | sort)
```

## Guided Remediation

```bash
# Show fix suggestions
osv-scanner scan --format vertical /path/to/project

# Example output:
# ╭─────────────────────────────────────────────────────────╮
# │ Vulnerability: CVE-2024-12345                           │
# │ Package: lodash@4.17.19                                 │
# │ Fixed in: 4.17.21                                       │
# │ Recommendation: npm install lodash@4.17.21              │
# ╰─────────────────────────────────────────────────────────╯
```

## Performance Optimization

```bash
# Skip git commits scanning
osv-scanner scan --skip-git /path/to/project

# Limit concurrent API calls
export OSV_SCANNER_MAX_CONCURRENT=5
osv-scanner scan /path/to/project

# Use offline mode for large scans
osv-scanner scan --download-databases ./osv-db
osv-scanner scan --offline --db-path ./osv-db /path/to/project
```

## Limitations

- **Transitive dependencies**: May not catch all indirect dependencies
- **Private packages**: Only scans public vulnerability databases
- **Custom code**: Doesn't analyze proprietary code vulnerabilities
- **Reachability**: Doesn't verify if vulnerable code is actually called (without experimental flag)
- **Zero-days**: Only detects publicly disclosed vulnerabilities

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "No vulnerabilities = dependencies are safe" | OSV only knows about disclosed vulnerabilities; zero-days and private exploits exist |
| "Low severity = can ignore" | Multiple low severity issues can combine into critical exploits |
| "Skip SCA in CI for speed" | Vulnerable dependencies are a primary attack vector; speed < security |
| "Only scan on major releases" | New vulnerabilities are disclosed daily; frequent scanning is essential |
| "Ignore transitive dependencies" | Indirect dependencies can introduce critical vulnerabilities |

## References

- Repository: <https://github.com/google/osv-scanner>
- Documentation: <https://google.github.io/osv-scanner/>
- OSV Database: <https://osv.dev/>
- GitHub Action: <https://github.com/google/osv-scanner-action>
- Output Formats: <https://google.github.io/osv-scanner/output/>
- SARIF Spec: <https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html>

