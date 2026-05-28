---
name: depscan
description: Run OWASP Depscan for advanced Software Composition Analysis with VDR, CSAF, and license compliance. Use when scanning dependencies with deep SCA, generating VEX documents, SBOM+VDR analysis, or comprehensive license auditing.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# OWASP Depscan - Next-Generation SCA

## When to Use Depscan

**Ideal scenarios:**

- Advanced Software Composition Analysis (SCA)
- Vulnerability Disclosure Report (VDR) generation
- SBOM (Software Bill of Materials) creation and analysis
- CSAF 2.0 VEX (Vulnerability Exploitability eXchange) documents
- License compliance auditing
- Risk assessment and scoring
- Supply chain security analysis
- Multi-format vulnerability reporting

**Complements other tools:**

- More comprehensive than OSV-Scanner for SCA needs
- Use with CDXGen for enhanced SBOM generation
- Combine with code scanners (Semgrep, CodeQL) for complete coverage
- Use with SARIF Issue Reporter for findings analysis

## When NOT to Use

Do NOT use this skill for:

- Application code vulnerability scanning (use Semgrep or CodeQL)
- Secrets detection (use Gitleaks)
- IaC security analysis (use KICS)
- API endpoint discovery (use Noir)
- Quick lightweight SCA (use OSV-Scanner instead)

## Installation

```bash
# pip/pipx (recommended)
pipx install owasp-depscan

# pip
pip install owasp-depscan

# With SARIF tools
pipx install owasp-depscan sarif-tools

# Docker
docker pull ghcr.io/owasp-dep-scan/dep-scan:latest

# From source
git clone https://github.com/owasp-dep-scan/dep-scan.git
cd dep-scan
pip install .

# Verify
depscan --version
```

## Core Workflow

### 1. Quick Scan

```bash
# Scan current directory
depscan --src .

# Scan specific directory
depscan --src /path/to/project

# Scan with reports directory
depscan --src /path/to/project --reports-dir ./reports
```

### 2. SARIF Output

```bash
# Generate SARIF report
depscan --src /path/to/project \
  --reports-dir ./reports \
  --report-template sarif

# Multiple report formats
depscan --src /path/to/project \
  --reports-dir ./reports \
  --report-template sarif,json,html

# Critical vulnerabilities only (SARIF)
depscan --src /path/to/project \
  --reports-dir ./reports \
  --report-template sarif-critical
```

### 3. SBOM Generation

```bash
# Create CycloneDX SBOM
depscan --src /path/to/project \
  --reports-dir ./reports \
  --type bom

# SBOM with VDR (Vulnerability Disclosure Report)
depscan --src /path/to/project \
  --reports-dir ./reports \
  --type sbom-vdr

# Use existing SBOM
depscan --bom /path/to/sbom.json --reports-dir ./reports
```

### 4. VEX Document Generation

```bash
# Generate CSAF 2.0 VEX
depscan --src /path/to/project \
  --reports-dir ./reports \
  --vex

# VEX with existing SBOM
depscan --bom sbom.json \
  --reports-dir ./reports \
  --vex
```

## Supported Package Managers

| Ecosystem | Manifest Files | Lock Files |
|-----------|----------------|------------|
| **npm** | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| **Python** | requirements.txt, setup.py, pyproject.toml | Pipfile.lock, poetry.lock, pdm.lock |
| **Go** | go.mod | go.sum |
| **Rust** | Cargo.toml | Cargo.lock |
| **Java/Maven** | pom.xml | - |
| **Gradle** | build.gradle, build.gradle.kts | - |
| **Ruby** | Gemfile | Gemfile.lock |
| **PHP** | composer.json | composer.lock |
| **.NET** | packages.config, *.csproj | packages.lock.json, paket.lock |
| **Dart** | pubspec.yaml | pubspec.lock |
| **Swift** | Package.swift | Package.resolved |

## Advanced Features

### Risk Scoring

```bash
# Enable risk audit
depscan --src /path/to/project \
  --reports-dir ./reports \
  --risk-audit

# Risk score is calculated based on:
# - Vulnerability severity
# - CVSS scores
# - Exploitability
# - Attack complexity
# - Package popularity
# - Maintenance status
```

### License Compliance

```bash
# License audit
depscan --src /path/to/project \
  --reports-dir ./reports \
  --license-scan

# Fail on license violations
depscan --src /path/to/project \
  --reports-dir ./reports \
  --license-scan \
  --no-banner \
  --fail-on-license-violation
```

### CDXGen Integration

Depscan includes CDXGen for SBOM generation:

```bash
# Use cdxgen directly
cdxgen -r /path/to/project -o sbom.json

# Generate SBOM with evidence
cdxgen -r /path/to/project -o sbom.json --evidence

# Multiple languages
cdxgen -r /monorepo -o sbom.json --multi-language

# Then scan SBOM
depscan --bom sbom.json --reports-dir ./reports
```

### Specific Language Scans

```bash
# Python specific
depscan --src /python/project --type python --reports-dir ./reports

# Node.js specific
depscan --src /nodejs/project --type nodejs --reports-dir ./reports

# Java specific
depscan --src /java/project --type java --reports-dir ./reports

# Go specific
depscan --src /go/project --type go --reports-dir ./reports
```

## CI/CD Integration (GitHub Actions)

```yaml
name: OWASP Depscan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  depscan:
    runs-on: ubuntu-latest
    container: ghcr.io/owasp-dep-scan/dep-scan:latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Depscan
        run: |
          depscan --src ${{ github.workspace }} \
            --reports-dir ${{ github.workspace }}/reports \
            --report-template sarif,json,html \
            --risk-audit \
            --license-scan

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/depscan.sarif
          category: depscan

      - name: Upload Reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: depscan-reports
          path: reports/

      - name: Generate SBOM
        run: |
          cdxgen -r ${{ github.workspace }} \
            -o reports/sbom.json \
            --evidence

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: reports/sbom.json
```

## Report Templates

### Available Templates

```bash
# SARIF (all vulnerabilities)
--report-template sarif

# SARIF (critical only)
--report-template sarif-critical

# JSON format
--report-template json

# HTML report
--report-template html

# Custom template
--report-template custom.j2
```

### Custom Jinja Templates

Create `custom-report.j2`:

```jinja
# Vulnerability Report

Project: {{ project_name }}
Scan Date: {{ scan_date }}

## Summary

Total Vulnerabilities: {{ total_vulnerabilities }}
- Critical: {{ critical_count }}
- High: {{ high_count }}
- Medium: {{ medium_count }}
- Low: {{ low_count }}

## Vulnerabilities

{% for vuln in vulnerabilities %}
### {{ vuln.id }} - {{ vuln.severity }}

**Package:** {{ vuln.package }}@{{ vuln.version }}
**Fixed in:** {{ vuln.fixed_version }}
**CVSS:** {{ vuln.cvss_score }}

{{ vuln.description }}

---
{% endfor %}
```

Use custom template:

```bash
depscan --src /path/to/project \
  --reports-dir ./reports \
  --report-template custom-report.j2
```

## Configuration

### Config File

Create `depscan.toml`:

```toml
# Source paths
src = "/path/to/project"
reports_dir = "./reports"

# Scan options
risk_audit = true
license_scan = true
no_banner = true

# Report formats
report_template = ["sarif", "json", "html"]

# VEX generation
vex = true

# Fail conditions
fail_on_license_violation = false

# Exclude paths
exclude = [
    "**/test/**",
    "**/tests/**",
    "**/node_modules/**",
    "**/.venv/**"
]

# License allowlist
allowed_licenses = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "ISC"
]
```

Use config:

```bash
depscan --config depscan.toml
```

## Common Use Cases

### 1. Comprehensive SCA Audit

```bash
# Full audit with all features
depscan --src /path/to/project \
  --reports-dir ./audit-reports \
  --report-template sarif,json,html \
  --risk-audit \
  --license-scan \
  --vex

# Review reports
ls -la ./audit-reports/
# - depscan.sarif
# - depscan.json
# - depscan.html
# - bom.json (SBOM)
# - vex.json (VEX document)
```

### 2. SBOM + VDR Workflow

```bash
# Step 1: Generate SBOM with evidence
cdxgen -r /path/to/project -o sbom.json --evidence

# Step 2: Scan SBOM for vulnerabilities
depscan --bom sbom.json \
  --reports-dir ./reports \
  --type sbom-vdr

# Step 3: Generate VEX
depscan --bom sbom.json \
  --reports-dir ./reports \
  --vex

# Outputs:
# - sbom.json (Software Bill of Materials)
# - vdr.json (Vulnerability Disclosure Report)
# - vex.json (Vulnerability Exploitability eXchange)
```

### 3. License Compliance Check

```bash
# Audit licenses
depscan --src /path/to/project \
  --license-scan \
  --reports-dir ./compliance

# Review license report
cat ./compliance/license-report.json | jq '.licenses[] | select(.approved == false)'

# Fail build on violations
depscan --src /path/to/project \
  --license-scan \
  --fail-on-license-violation
```

### 4. Container Image Analysis

```bash
# Extract container filesystem
docker export $(docker create myimage:latest) | tar -C /tmp/container-fs -xf -

# Scan extracted filesystem
depscan --src /tmp/container-fs \
  --reports-dir ./container-reports \
  --report-template sarif

# Or use with Docker
docker run --rm -v $(pwd):/app ghcr.io/owasp-dep-scan/dep-scan \
  depscan --src /app --reports-dir /app/reports
```

### 5. Baldwin.sh Integration

```bash
# Match baldwin.sh justfile pattern
depscan \
  --src /workspace/src \
  --reports-dir /workspace/output \
  --report-template sarif \
  --no-banner

# SARIF output will be in /workspace/output/depscan.sarif
```

## Understanding Output

### SARIF Structure

Depscan SARIF includes:

- **Rules**: Each vulnerability type
- **Results**: Vulnerable dependencies
- **Properties**:
  - Package name and version
  - Vulnerability ID (CVE, GHSA, etc.)
  - Severity and CVSS
  - Fix versions
  - Risk score
  - Exploitability metrics
  - License information

### VDR Structure

Vulnerability Disclosure Report (VDR) in CycloneDX format:

```json
{
  "vulnerabilities": [
    {
      "id": "CVE-2024-12345",
      "source": {
        "name": "NVD",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12345"
      },
      "ratings": [
        {
          "score": 9.8,
          "severity": "critical",
          "method": "CVSSv3",
          "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
        }
      ],
      "affects": [
        {
          "ref": "pkg:npm/lodash@4.17.19"
        }
      ],
      "recommendation": "Upgrade to version 4.17.21 or later"
    }
  ]
}
```

### VEX Structure

CSAF 2.0 VEX document:

```json
{
  "document": {
    "category": "csaf_vex",
    "title": "Vulnerability Exploitability eXchange"
  },
  "vulnerabilities": [
    {
      "cve": "CVE-2024-12345",
      "product_status": {
        "known_affected": ["pkg:npm/lodash@4.17.19"]
      },
      "remediation": [
        {
          "category": "vendor_fix",
          "details": "Update to version 4.17.21"
        }
      ]
    }
  ]
}
```

## Remediation Workflow

### Step 1: Scan

```bash
depscan --src /project \
  --reports-dir ./reports \
  --report-template json,sarif \
  --risk-audit
```

### Step 2: Prioritize

```bash
# Extract high-risk vulnerabilities
jq '.results[] | select(.risk_score > 7)' reports/depscan.json

# Group by package
jq -r '.results[] | "\(.package): \(.vulnerabilities | length) vulns"' reports/depscan.json | sort
```

### Step 3: Fix

```bash
# Review fix recommendations
jq -r '.results[] | "\(.package)@\(.version) -> \(.fixed_version // "No fix available")"' reports/depscan.json

# Apply updates
npm update
pip install --upgrade -r requirements.txt
```

### Step 4: Verify

```bash
# Rescan
depscan --src /project --reports-dir ./post-fix

# Compare
diff <(jq '.results[].id' reports/depscan.json | sort) \
     <(jq '.results[].id' post-fix/depscan.json | sort)
```

## Performance Optimization

```bash
# Skip network calls for faster offline scanning
depscan --src /project --offline

# Limit report generation
depscan --src /project --report-template sarif

# Exclude test directories
depscan --src /project --exclude "**/test/**,**/tests/**"

# Use existing SBOM instead of regenerating
depscan --bom sbom.json --reports-dir ./reports
```

## Integration with Other Tools

### SARIF Tools

```bash
# Generate SARIF
depscan --src /project --reports-dir ./reports --report-template sarif

# Analyze with sarif-tools
pip install sarif-tools
sarif summary reports/depscan.sarif
sarif ls reports/depscan.sarif
sarif trends reports/*.sarif
```

### Dependency Track

```bash
# Generate SBOM+VDR for Dependency Track
depscan --src /project \
  --reports-dir ./reports \
  --type sbom-vdr

# Upload to Dependency Track
curl -X POST "https://dependency-track/api/v1/bom" \
  -H "X-API-Key: ${API_KEY}" \
  -F "bom=@reports/bom.json"
```

## Limitations

- **Performance**: Slower than OSV-Scanner due to deeper analysis
- **Network required**: Needs internet for vulnerability database (unless offline mode)
- **Memory usage**: Large projects may require significant RAM
- **False positives**: Risk scoring heuristics may over/under estimate
- **Private packages**: Only scans public vulnerability databases

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "OSV-Scanner is enough" | Depscan provides VDR, VEX, risk scoring, and license compliance OSV lacks |
| "Skip VEX generation" | VEX documents are critical for communicating vulnerability status to stakeholders |
| "Disable risk audit for speed" | Risk scores help prioritize fixes; speed shouldn't compromise decision quality |
| "Ignore license violations" | License compliance is legal requirement; violations can block product release |
| "Only scan production dependencies" | Dev dependencies can introduce supply chain attacks |

## References

- Repository: <https://github.com/owasp-dep-scan/dep-scan>
- Documentation: <https://depscan.readthedocs.io/>
- OWASP Project: <https://owasp.org/www-project-dep-scan/>
- CDXGen: <https://github.com/CycloneDX/cdxgen>
- CycloneDX Spec: <https://cyclonedx.org/>
- CSAF Spec: <https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html>
- SARIF Spec: <https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html>
-
