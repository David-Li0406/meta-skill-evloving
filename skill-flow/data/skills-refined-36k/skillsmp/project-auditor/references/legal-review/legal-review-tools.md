<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Code Legal Review Tools & Automation

Comprehensive guide to tools and automation for legal review of source code, including license scanning, secret detection, and content policy enforcement.

## Open Source License Scanners

### ScanCode Toolkit
- **URL**: https://github.com/nexB/scancode-toolkit
- **License**: Apache-2.0
- **Features**:
  - 30,000+ license texts
  - Copyright detection
  - Package metadata extraction
  - SPDX document generation
  - Comprehensive reporting

**Usage**:
```bash
# Basic scan
scancode --license --copyright --package --json-pp output.json path/to/code

# With all options
scancode \
  --license \
  --copyright \
  --package \
  --info \
  --email \
  --url \
  --json-pp output.json \
  --processes 4 \
  path/to/code
```

### Licensee (GitHub)
- **URL**: https://github.com/licensee/licensee
- **License**: MIT
- **Features**:
  - License detection with confidence scoring
  - Multiple license detection
  - Command-line and Ruby API
  - Used by GitHub.com

**Usage**:
```bash
licensee detect path/to/repo
licensee detect --json path/to/repo
```

### FOSSology
- **URL**: https://www.fossology.org/
- **License**: GPL-2.0
- **Features**:
  - Web-based platform
  - License clearance workflow
  - Compliance documentation
  - Report generation

### OSS Review Toolkit (ORT)
- **URL**: https://github.com/oss-review-toolkit/ort
- **License**: Apache-2.0
- **Features**:
  - Complete compliance workflow
  - Analyzer, Scanner, Evaluator, Reporter
  - Policy evaluation
  - Multiple package manager support

**Usage**:
```bash
# Analyze dependencies
ort analyze -i path/to/project -o analyzer-result.yml

# Scan for licenses
ort scan -i analyzer-result.yml -o scan-result.yml

# Evaluate against policy
ort evaluate -i scan-result.yml --rules-file rules.kts

# Generate report
ort report -i scan-result.yml -o report.html
```

## Secret Detection Tools

### TruffleHog
- **URL**: https://github.com/trufflesecurity/trufflehog
- **License**: AGPL-3.0
- **Features**:
  - High entropy string detection
  - 800+ credential detectors
  - Git history scanning
  - Real-time verification

**Usage**:
```bash
# Scan repository
trufflehog git https://github.com/user/repo

# Scan filesystem
trufflehog filesystem path/to/code

# With verification
trufflehog git https://github.com/user/repo --only-verified
```

### detect-secrets
- **URL**: https://github.com/Yelp/detect-secrets
- **License**: Apache-2.0
- **Features**:
  - Baseline management
  - Plugin architecture
  - Low false positive rate
  - Pre-commit integration

**Usage**:
```bash
# Create baseline
detect-secrets scan > .secrets.baseline

# Audit findings
detect-secrets audit .secrets.baseline

# Pre-commit hook
detect-secrets-hook --baseline .secrets.baseline
```

## Content Policy Tools

### alex
- **URL**: https://github.com/get-alex/alex
- **License**: MIT
- **Features**:
  - Insensitive/inconsiderate language detection
  - Gender favoritism detection
  - Polarizing language detection

**Usage**:
```bash
# Check markdown files
alex README.md

# Check all files
alex .

# Ignore specific files
alex --ignore "test/**"
```

### woke
- **URL**: https://github.com/get-woke/woke
- **License**: MIT
- **Features**:
  - Detect non-inclusive language
  - Custom rule support
  - Multiple output formats
  - CI/CD integration

**Usage**:
```bash
# Check files
woke path/to/code

# With custom rules
woke --config .woke.yaml

# Output JSON
woke --output json
```

## Commercial Tools

### FOSSA
- **URL**: https://fossa.com/
- **Features**:
  - Automated dependency scanning
  - License compliance
  - Vulnerability detection
  - Policy enforcement
  - Legal risk assessment

### Black Duck (Synopsys)
- **URL**: https://www.blackducksoftware.com/
- **Features**:
  - Comprehensive license detection
  - Security vulnerability scanning
  - Code match detection
  - Operational risk analysis
  - M&A due diligence

### Snyk
- **URL**: https://snyk.io/
- **Features**:
  - Open source license compliance
  - Security vulnerability detection
  - Automated fix PRs
  - Developer-friendly workflow

### WhiteSource/Mend
- **URL**: https://www.mend.io/
- **Features**:
  - License compliance
  - Security vulnerabilities
  - Code quality
  - Supply chain security

## Integrated Platforms

### GitHub Advanced Security
- Secret scanning
- Code scanning (CodeQL)
- Dependency review
- Security advisories

**Configuration**:
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  codeql:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: github/codeql-action/init@v2
      - uses: github/codeql-action/analyze@v2

  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: trufflesecurity/trufflehog@main
        with:
          path: ./
```

### GitLab Security Scanning
- License scanning
- Secret detection
- SAST (Static Application Security Testing)
- Dependency scanning

**Configuration**:
```yaml
# .gitlab-ci.yml
include:
  - template: Security/License-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/SAST.gitlab-ci.yml
```

## CI/CD Integration Examples

### Pre-commit Hooks

**.pre-commit-config.yaml**:
```yaml
repos:
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
        name: TruffleHog
        entry: bash -c 'trufflehog git file://. --only-verified'

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets

  - repo: https://github.com/get-woke/woke
    rev: v0.19.0
    hooks:
      - id: woke

  - repo: local
    hooks:
      - id: license-check
        name: License Check
        entry: python scripts/check_licenses.py
        language: python
```

### GitHub Actions

```yaml
name: Legal Review
on: [push, pull_request]

jobs:
  license-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install ScanCode
        run: pip install scancode-toolkit

      - name: Scan licenses
        run: |
          scancode --license --copyright --json-pp licenses.json .

      - name: Check compliance
        run: python scripts/check_license_compliance.py licenses.json

  secret-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  content-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check inclusive language
        uses: get-woke/woke-action@v0
        with:
          fail-on-error: true
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('License Scan') {
            steps {
                sh 'scancode --license --copyright --json licenses.json .'
                sh 'python check_licenses.py licenses.json'
            }
        }

        stage('Secret Detection') {
            steps {
                sh 'trufflehog git file://. --json > secrets-report.json'
            }
        }

        stage('Content Policy') {
            steps {
                sh 'woke . --output json > woke-report.json'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*-report.json'
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'legal-report.html',
                reportName: 'Legal Review Report'
            ])
        }
    }
}
```

## Custom Automation Scripts

### Combined Legal Scanner

```python
#!/usr/bin/env python3
"""Comprehensive legal scanner combining multiple tools."""

import json
import subprocess
import sys
from pathlib import Path

def scan_licenses(path):
    """Scan for licenses using ScanCode."""
    result = subprocess.run(
        ['scancode', '--license', '--copyright', '--json-pp', '-', path],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def detect_secrets(path):
    """Detect secrets using TruffleHog."""
    result = subprocess.run(
        ['trufflehog', 'filesystem', path, '--json'],
        capture_output=True,
        text=True
    )
    findings = []
    for line in result.stdout.splitlines():
        if line.strip():
            findings.append(json.loads(line))
    return findings

def check_content_policy(path):
    """Check content policy using woke."""
    result = subprocess.run(
        ['woke', path, '--output', 'json'],
        capture_output=True,
        text=True
    )
    if result.stdout:
        return json.loads(result.stdout)
    return []

def generate_report(license_data, secret_data, policy_data):
    """Generate comprehensive report."""
    report = {
        "licenses": {
            "total_files": len(license_data.get('files', [])),
            "violations": [],
        },
        "secrets": {
            "total_findings": len(secret_data),
            "high_confidence": [s for s in secret_data if s.get('Verified', False)],
        },
        "content_policy": {
            "total_violations": len(policy_data),
            "by_severity": {},
        },
    }

    # Analyze licenses
    denied_licenses = ['GPL-3.0', 'AGPL-3.0']
    for file in license_data.get('files', []):
        for license in file.get('licenses', []):
            if license['spdx_license_key'] in denied_licenses:
                report['licenses']['violations'].append({
                    "file": file['path'],
                    "license": license['spdx_license_key'],
                    "severity": "high",
                })

    return report

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    print("🔍 Running comprehensive legal scan...")

    print("  📜 Scanning licenses...")
    licenses = scan_licenses(path)

    print("  🔐 Detecting secrets...")
    secrets = detect_secrets(path)

    print("  📋 Checking content policy...")
    policy = check_content_policy(path)

    print("\n📊 Generating report...")
    report = generate_report(licenses, secrets, policy)

    output_file = 'legal-scan-report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Report saved to {output_file}")

    # Check for critical issues
    critical_issues = (
        len(report['licenses']['violations']) +
        len(report['secrets']['high_confidence'])
    )

    if critical_issues > 0:
        print(f"\n❌ Found {critical_issues} critical issues!")
        sys.exit(1)
    else:
        print("\n✅ No critical issues found")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

## Policy Configuration Examples

### License Policy

```yaml
# license-policy.yaml
policies:
  allow:
    - MIT
    - Apache-2.0
    - BSD-2-Clause
    - BSD-3-Clause
    - ISC
    - CC0-1.0
    - Unlicense

  review_required:
    - MPL-2.0
    - LGPL-3.0
    - EPL-2.0

  deny:
    - GPL-2.0
    - GPL-3.0
    - AGPL-3.0
    - SSPL-1.0

exceptions:
  - package: readline
    license: GPL-3.0
    reason: System library exception
    approved_by: legal@company.com
    approved_date: 2024-01-01
```

### Secret Detection Configuration

```yaml
# trufflehog.yaml
detectors:
  - name: CustomCompanyKey
    keywords:
      - "COMP-"
    regex:
      pattern: "COMP-[A-Za-z0-9]{32}"

# Use .secrets.baseline for detect-secrets
# detect-secrets scan > .secrets.baseline
```

regexes = [
    '''EXAMPLE_KEY''',
    '''sample_token''',
]
```

### Content Policy Configuration

```yaml
# .woke.yaml
rules:
  - name: whitelist-blacklist
    terms:
      - whitelist
      - blacklist
    alternatives:
      - allowlist
      - denylist
    severity: error

  - name: master-slave
    terms:
      - master
      - slave
    alternatives:
      - primary
      - replica
      - leader
      - follower
    severity: error

  - name: sanity-check
    terms:
      - sanity check
      - sanity test
    alternatives:
      - validation
      - verification
      - health check
    severity: warning

ignore_files:
  - vendor/**
  - node_modules/**
  - "*.min.js"
```

## Best Practices for Tool Integration

### 1. Layered Approach
- **Fast checks**: Pre-commit hooks
- **Comprehensive scans**: CI/CD pipeline
- **Deep analysis**: Scheduled scans

### 2. Progressive Enforcement
- **Warning phase**: Log but don't block
- **Soft enforcement**: Block on critical only
- **Full enforcement**: Block all violations

### 3. Developer Experience
- **Fast feedback**: Pre-commit hooks < 10s
- **Clear messages**: Explain violations
- **Auto-fix**: Provide fixes when possible
- **Documentation**: Link to policies

### 4. False Positive Management
- **Whitelist mechanisms**: Allow exemptions
- **Context awareness**: Reduce noise
- **Feedback loop**: Improve rules over time

### 5. Reporting & Metrics
- **Dashboard**: Centralized view
- **Trends**: Track improvements
- **Compliance score**: Overall health
- **Alerts**: Critical issues

## Tool Selection Matrix

| Use Case | Tool | Pros | Cons |
|----------|------|------|------|
| License Detection | ScanCode | Comprehensive, accurate | Slow on large codebases |
| License Detection | Licensee | Fast, GitHub integration | Less comprehensive |
| Secret Detection | TruffleHog | High accuracy, verification | Can be slow |
| Secret Detection | detect-secrets | Low false positives, baseline | Requires tuning |
| Content Policy | woke | Focused on inclusivity | Limited scope |
| Content Policy | alex | Natural language focus | Markdown/docs only |
| All-in-one | FOSSA | Complete solution | Commercial |
| All-in-one | Black Duck | Enterprise features | Expensive |

## Summary

Effective legal review automation requires:

1. **Multiple tools** - No single tool covers everything
2. **Layered scanning** - Pre-commit + CI/CD + scheduled
3. **Clear policies** - Define what's allowed/denied
4. **Developer education** - Explain why rules exist
5. **Continuous improvement** - Refine rules and reduce false positives
6. **Integration** - Seamless workflow integration
7. **Reporting** - Track compliance over time

Choose tools based on your specific needs, team size, and compliance requirements.
