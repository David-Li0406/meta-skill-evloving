---
name: opengrep
description: Run Opengrep static analysis for fast security scanning with open-source rules. Use when scanning with truly open-source SAST, avoiding proprietary rule licenses, using community rules freely, or requiring commercial tool integration.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Opengrep - Open Source Code Security Engine

## What is Opengrep?

Opengrep is a fork of Semgrep CE (Community Edition), launched in early 2025 by a consortium including JIT, Aikido Security, Endor Labs, and other companies. It was created in response to Semgrep's licensing changes that restricted community-contributed rules from being used in commercial products.

**Key Differences from Semgrep:**

- Fully open-source rules (no license restrictions)
- Community-driven governance
- No proprietary feature lock-in
- Compatible with Semgrep CE syntax and rules
- Focused on keeping critical features open
- Commercial integration friendly

## When to Use Opengrep

**Ideal scenarios:**

- Quick security scans (minutes, not hours)
- Pattern-based vulnerability detection
- Using community rules without license concerns
- Commercial product integration requiring open-source SAST
- Dataflow and taint analysis within files
- Multi-language security scanning
- First-pass security analysis before deeper tools
- When Semgrep licensing is a concern

**Consider CodeQL instead when:**

- Need interprocedural taint tracking across files
- Complex data flow analysis across modules required
- Analyzing custom proprietary frameworks with deep integration

## When NOT to Use

Do NOT use this skill for:

- Complex cross-file data flow analysis (use CodeQL)
- Binary or compiled code analysis without source
- Deep semantic analysis requiring full program analysis
- Runtime vulnerability detection
- Secrets scanning (use Gitleaks)
- Dependency scanning (use OSV-Scanner or Depscan)

## Installation

```bash
# Homebrew
brew install opengrep

# pip
pip install opengrep

# pipx (recommended)
pipx install opengrep

# Docker
docker pull ghcr.io/opengrep/opengrep:latest

# From source
git clone https://github.com/opengrep/opengrep.git
cd opengrep
pip install -e .

# Verify
opengrep --version
```

## Core Workflow

### 1. Quick Scan

```bash
# Auto scan with default rules
opengrep scan .

# Scan with specific ruleset
opengrep scan -f p/security-audit .

# Multiple rulesets
opengrep scan -f p/owasp-top-ten -f p/cwe-top-25 .
```

### 2. SARIF Output

```bash
# Generate SARIF report
opengrep scan --sarif -o results.sarif .

# SARIF with specific rules
opengrep scan -f p/security-audit --sarif -o results.sarif .

# Filter by severity in SARIF
opengrep scan \
  --severity=WARNING \
  --severity=ERROR \
  --sarif \
  -o results.sarif \
  .
```

### 3. Advanced Scanning

```bash
# Enable dataflow traces
opengrep scan --dataflow-traces .

# Taint analysis (intra-file)
opengrep scan --taint-intrafile .

# Experimental features
opengrep scan --experimental .

# Combined: dataflow + taint + experimental
opengrep scan \
  --dataflow-traces \
  --taint-intrafile \
  --experimental \
  .
```

### 4. Custom Rules

```bash
# Local rule files
opengrep scan -f /path/to/rules .

# Multiple rule directories
opengrep scan -f ./rules -f ./custom-rules .

# Exclude specific rules
opengrep scan \
  -f p/security-audit \
  --exclude-rule="rule-id-to-skip" \
  .
```

## Rulesets

### Public Rulesets

| Ruleset | Description |
|---------|-------------|
| `p/default` | General security and code quality |
| `p/security-audit` | Comprehensive security rules |
| `p/owasp-top-ten` | OWASP Top 10 vulnerabilities |
| `p/cwe-top-25` | CWE Top 25 vulnerabilities |
| `p/trailofbits` | Trail of Bits security rules |
| `p/python` | Python-specific security |
| `p/javascript` | JavaScript/TypeScript security |
| `p/golang` | Go-specific security |
| `p/java` | Java security patterns |
| `p/ruby` | Ruby security patterns |

### Community Rules

```bash
# Clone community rules
git clone https://github.com/opengrep/opengrep-rules.git

# Use community rules
opengrep scan -f opengrep-rules/ .

# Trail of Bits rules (fully open)
git clone https://github.com/trailofbits/semgrep-rules.git
opengrep scan -f semgrep-rules/rules .
```

## Output Formats

```bash
# Text output (default)
opengrep scan .

# SARIF (for CI/CD)
opengrep scan --sarif .

# JSON
opengrep scan --json .

# JUnit XML
opengrep scan --junit-xml .

# GitLab SAST format
opengrep scan --gitlab-sast .

# Vim quickfix
opengrep scan --vim .

# Emacs format
opengrep scan --emacs .
```

## Configuration

### .opengrepignore

Create `.opengrepignore`:

```
tests/fixtures/
**/testdata/
generated/
vendor/
node_modules/
__pycache__/
*.test.js
*.spec.ts
```

### Project Configuration

Create `.opengrep.yml`:

```yaml
rules:
  - id: custom-hardcoded-secret
    languages: [python, javascript]
    message: "Hardcoded secret detected"
    severity: ERROR
    pattern: |
      $VAR = "$SECRET"
    metadata:
      cwe: "CWE-798"
      owasp: "A07:2021 - Identification and Authentication Failures"

  - id: sql-injection-risk
    languages: [python]
    message: "Potential SQL injection"
    severity: ERROR
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
    pattern-sanitizers:
      - pattern: int(...)

exclude:
  - tests/
  - vendor/
```

Use config:

```bash
opengrep scan --config .opengrep.yml .
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Opengrep Security Scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  opengrep:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Opengrep
        run: pip install opengrep

      - name: Run Opengrep
        run: |
          opengrep scan \
            -f p/security-audit \
            -f p/owasp-top-ten \
            --dataflow-traces \
            --taint-intrafile \
            --experimental \
            --sarif \
            -o opengrep-results.sarif \
            --severity=WARNING \
            --severity=ERROR \
            --exclude=test \
            --exclude=tests \
            .

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: opengrep-results.sarif
          category: opengrep

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: opengrep-results
          path: opengrep-results.sarif
```

## Writing Custom Rules

### Basic Rule Structure

```yaml
rules:
  - id: dangerous-eval
    languages: [javascript, python]
    message: "Use of eval() is dangerous"
    severity: ERROR
    patterns:
      - pattern: eval($CODE)
      - pattern-not: eval("...")  # Literal strings okay
```

### Pattern Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `...` | Match anything | `func(...)` |
| `$VAR` | Capture metavariable | `$FUNC($INPUT)` |
| `<... ...>` | Deep expression match | `<... user_input ...>` |

### Pattern Operators

| Operator | Description |
|----------|-------------|
| `pattern` | Match exact pattern |
| `patterns` | All must match (AND) |
| `pattern-either` | Any matches (OR) |
| `pattern-not` | Exclude matches |
| `pattern-inside` | Match only inside context |
| `pattern-not-inside` | Match only outside context |
| `pattern-regex` | Regex matching |
| `metavariable-regex` | Regex on captured value |

### Taint Mode

```yaml
rules:
  - id: xss-vulnerability
    languages: [javascript]
    message: "User input flows to innerHTML (XSS risk)"
    severity: ERROR
    mode: taint
    pattern-sources:
      - pattern: req.query.$PARAM
      - pattern: req.body.$PARAM
    pattern-sinks:
      - pattern: $ELEMENT.innerHTML = $DATA
    pattern-sanitizers:
      - pattern: escapeHtml(...)
      - pattern: DOMPurify.sanitize(...)
```

## Common Use Cases

### 1. Comprehensive Security Audit

```bash
# Multi-ruleset scan
opengrep scan \
  -f p/security-audit \
  -f p/owasp-top-ten \
  -f p/cwe-top-25 \
  --dataflow-traces \
  --experimental \
  --sarif \
  -o security-audit.sarif \
  .
```

### 2. Language-Specific Scan

```bash
# Python security
opengrep scan \
  -f p/python \
  --taint-intrafile \
  --sarif \
  -o python-security.sarif \
  ./src

# JavaScript/TypeScript security
opengrep scan \
  -f p/javascript \
  -f p/typescript \
  --dataflow-traces \
  --sarif \
  -o js-security.sarif \
  ./frontend
```

### 3. Pre-commit Hook

```bash
# Scan staged files only
git diff --cached --name-only --diff-filter=ACMR | \
  grep -E '\.(py|js|ts|go|java|rb)$' | \
  xargs opengrep scan -f p/security-audit
```

### 4. Baldwin.sh Integration

```bash
# Match baldwin.sh justfile pattern
opengrep scan \
  -f /workspace/data/opengrep-rules \
  -f /workspace/data/trailofbits-rules \
  --exclude-rule="data.opengrep-rules.typescript.react.best-practice.define-styled-components-on-module-level" \
  --exclude-rule="data.opengrep-rules.typescript.react.portability.i18next.jsx-not-internationalized" \
  --dataflow-traces \
  --taint-intrafile \
  --severity=WARNING \
  --severity=ERROR \
  --exclude=test \
  --exclude=tests \
  --sarif \
  --experimental \
  --project-root=/workspace/src \
  /workspace/src \
  > /workspace/output/sarif/opengrep.sarif
```

### 5. Diff Scan (Changed Files Only)

```bash
# Scan only modified files
git diff --name-only origin/main...HEAD | \
  xargs opengrep scan -f p/security-audit --sarif -o diff-scan.sarif
```

## Suppressing False Positives

### Inline Suppressions

```python
# nosemgrep: rule-id
password = get_from_vault()

# Multiple rules
eval(safe_code)  # nosemgrep: dangerous-eval, code-injection
```

```javascript
// nosemgrep: xss-vulnerability
element.innerHTML = sanitizedContent;
```

### Configuration-Based Suppressions

```yaml
# .opengrep.yml
exclude-rules:
  - rule-id-1
  - rule-id-2

exclude-paths:
  - tests/
  - generated/
```

## Performance Optimization

```bash
# Limit to specific file types
opengrep scan --include='*.py' --include='*.js' .

# Exclude large directories
opengrep scan --exclude=node_modules --exclude=vendor .

# Set timeout per file
opengrep scan --timeout 60 .

# Disable experimental features for speed
opengrep scan -f p/security-audit .  # No --experimental
```

## Comparing with Semgrep

### Compatibility

Opengrep maintains compatibility with Semgrep CE:

- Same rule syntax (YAML)
- Same pattern language
- Same command-line interface
- Can use Semgrep rules directly

### Key Differences

| Feature | Opengrep | Semgrep CE |
|---------|----------|------------|
| **License** | LGPL 2.1 (fully open) | LGPL 2.1 (engine), restrictive rules |
| **Rules** | Fully open, no restrictions | Community rules have usage restrictions |
| **Governance** | Community consortium | r2c/Semgrep Inc. |
| **Commercial Use** | Unrestricted | Restricted for community rules |
| **Pro Features** | Being migrated to open | Proprietary |
| **Development** | Community-driven | Company-driven |

### Migration from Semgrep

```bash
# Rules are compatible - just change binary
alias opengrep=semgrep  # For testing
opengrep scan -f p/security-audit .

# Update CI/CD configs
sed -i 's/semgrep/opengrep/g' .github/workflows/security.yml
```

## Supported Languages

- **Web**: JavaScript, TypeScript, JSX, TSX
- **Backend**: Python, Go, Java, Kotlin, Scala
- **Systems**: C, C++, Rust
- **Mobile**: Swift, Kotlin, Java
- **Scripting**: Ruby, PHP, Bash, Lua
- **Infrastructure**: Terraform, Dockerfile, YAML, JSON
- **Other**: C#, Elixir, Solidity, Apex

## Limitations

- **Intra-file taint only**: Cross-file dataflow requires CodeQL
- **Pattern-based**: Can't understand complex program semantics
- **No runtime analysis**: Static analysis only
- **Performance**: Large codebases may be slow with all features enabled
- **Experimental features**: May have bugs or incomplete coverage

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "Opengrep found nothing = code is secure" | Pattern-based analysis can miss context-specific vulnerabilities |
| "Just use default rules" | Default rules are generic; custom rules for your stack are essential |
| "Skip dataflow/taint analysis for speed" | These features catch vulnerabilities simple patterns miss |
| "Semgrep and Opengrep are identical" | Licensing differences matter for commercial use; feature sets diverging |
| "Don't need both Opengrep and CodeQL" | Complementary: Opengrep is fast/broad, CodeQL is deep/precise |

## References

- Repository: <https://github.com/opengrep/opengrep>
- Website: <https://www.opengrep.dev/>
- Rules Repository: <https://github.com/opengrep/opengrep-rules>
- Documentation: <https://www.opengrep.dev/docs/>
- Trail of Bits Rules: <https://github.com/trailofbits/semgrep-rules>
- Comparison with Semgrep: <https://semgrep.dev/docs/faq/comparisons/opengrep>
- Launch Announcement: <https://www.aikido.dev/blog/launching-opengrep-why-we-forked-semgrep>
- Baldwin.sh Integration: <https://github.com/igbuend/baldwin.sh>

**Articles:**

- [Opengrep vs. Semgrep: Some Thoughts](https://blog.codacy.com/opengrep-vs-semgrep)
- [Launching Opengrep | Why we forked Semgrep](https://www.aikido.dev/blog/launching-opengrep-why-we-forked-semgrep)
- [Opengrep Launches as Free Fork After Semgrep License Shift](https://thenewstack.io/opengrep-launches-as-free-fork-after-semgrep-license-shift/)
