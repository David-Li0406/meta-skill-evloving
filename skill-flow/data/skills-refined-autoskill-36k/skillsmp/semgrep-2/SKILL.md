---
name: semgrep
description: Run Semgrep static analysis for fast security scanning and pattern matching. Use when asked to scan code with Semgrep, write custom YAML rules, find vulnerabilities quickly, use taint mode, or set up Semgrep in CI/CD pipelines.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Semgrep Static Analysis

## When to Use Semgrep

**Ideal scenarios:**

- Quick security scans (minutes, not hours)
- Pattern-based vulnerability detection
- Enforcing coding standards and best practices
- Finding known vulnerability patterns (OWASP Top 10, CWE Top 25)
- Intra-file taint analysis and data flow tracking
- Custom rule development for specific code patterns
- First-pass security analysis before deeper tools
- CI/CD security gates for fast feedback
- Multi-language security scanning

**Complements other tools:**

- Use before manual code review to catch common patterns
- Combine with SARIF Issue Reporter for detailed findings
- Use alongside CodeQL for comprehensive coverage
- Pair with dependency scanners (OSV-Scanner, Depscan)

**Consider CodeQL instead when:**

- Need interprocedural taint tracking across files
- Complex data flow analysis across modules required
- Analyzing custom proprietary frameworks with deep integration

## When NOT to Use

Do NOT use this skill for:

- Complex interprocedural data flow analysis (use CodeQL instead)
- Binary analysis or compiled code without source
- Custom deep semantic analysis requiring AST/CFG traversal
- Tracking taint across many function boundaries and files
- Secrets detection (use Gitleaks)
- Dependency vulnerability scanning (use OSV-Scanner or Depscan)
- IaC security analysis (use KICS)
- API endpoint discovery (use Noir)

## Installation

```bash
# pip
python3 -m pip install semgrep

# pipx (recommended)
pipx install semgrep

# Homebrew
brew install semgrep

# Docker
docker pull returntocorp/semgrep:latest
docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep --config auto /src

# Update
pip install --upgrade semgrep

# Verify
semgrep --version
```

## Core Workflow

### 1. Quick Scan

```bash
semgrep --config auto .                    # Auto-detect rules
semgrep --config auto --metrics=off .      # Disable telemetry for proprietary code
```

### 2. Use Rulesets

```bash
semgrep --config p/<RULESET> .             # Single ruleset
semgrep --config p/security-audit --config p/trailofbits .  # Multiple
```

| Ruleset | Description |
|---------|-------------|
| `p/default` | General security and code quality |
| `p/security-audit` | Comprehensive security rules |
| `p/owasp-top-ten` | OWASP Top 10 vulnerabilities |
| `p/cwe-top-25` | CWE Top 25 vulnerabilities |
| `p/r2c-security-audit` | r2c security audit rules |
| `p/trailofbits` | Trail of Bits security rules |
| `p/python` | Python-specific |
| `p/javascript` | JavaScript-specific |
| `p/golang` | Go-specific |

### 3. Output Formats

```bash
# SARIF output (for CI/CD)
semgrep --config p/security-audit --sarif -o results.sarif .

# JSON output
semgrep --config p/security-audit --json -o results.json .

# Text output with dataflow traces
semgrep --config p/security-audit --dataflow-traces .

# JUnit XML
semgrep --config p/security-audit --junit-xml -o results.xml .

# GitLab SAST format
semgrep --config p/security-audit --gitlab-sast -o gl-sast-report.json .

# Vim quickfix
semgrep --config p/security-audit --vim .
```

### 4. Scan Specific Paths

```bash
# Single file
semgrep --config p/python app.py

# Specific directory
semgrep --config p/javascript src/

# Include tests (excluded by default)
semgrep --config auto --include='**/test/**' .

# Exclude paths
semgrep --config auto --exclude='vendor' --exclude='node_modules' .

# Multiple languages
semgrep --config p/python --config p/javascript .
```

### 5. Advanced Features

```bash
# Enable Pro Engine features (requires license)
semgrep --config p/security-audit --pro .

# Pro Engine interfile analysis
semgrep --config p/security-audit --pro --pro-intrafile .

# Disable telemetry
semgrep --config auto --metrics=off .

# Verbose output
semgrep --config p/security-audit --verbose .

# Quiet mode (only show findings)
semgrep --config p/security-audit --quiet .
```

## Writing Custom Rules

### Basic Structure

```yaml
rules:
  - id: hardcoded-password
    languages: [python]
    message: "Hardcoded password detected: $PASSWORD"
    severity: ERROR
    pattern: password = "$PASSWORD"
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
| `metavariable-comparison` | Compare values |

### Combining Patterns

```yaml
rules:
  - id: sql-injection
    languages: [python]
    message: "Potential SQL injection"
    severity: ERROR
    patterns:
      - pattern-either:
          - pattern: cursor.execute($QUERY)
          - pattern: db.execute($QUERY)
      - pattern-not:
          - pattern: cursor.execute("...", (...))
      - metavariable-regex:
          metavariable: $QUERY
          regex: .*\+.*|.*\.format\(.*|.*%.*
```

### Taint Mode (Data Flow)

Simple pattern matching finds obvious cases:

```python
# Pattern `os.system($CMD)` catches this:
os.system(user_input)  # Found
```

But misses indirect flows:

```python
# Same pattern misses this:
cmd = user_input
processed = cmd.strip()
os.system(processed)  # Missed - no direct match
```

Taint mode tracks data through assignments and transformations:

- **Source**: Where untrusted data enters (`user_input`)
- **Propagators**: How it flows (`cmd = ...`, `processed = ...`)
- **Sanitizers**: What makes it safe (`shlex.quote()`)
- **Sink**: Where it becomes dangerous (`os.system()`)

```yaml
rules:
  - id: command-injection
    languages: [python]
    message: "User input flows to command execution"
    severity: ERROR
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
      - pattern: request.form[...]
      - pattern: request.json
    pattern-sinks:
      - pattern: os.system($SINK)
      - pattern: subprocess.call($SINK, shell=True)
      - pattern: subprocess.run($SINK, shell=True, ...)
    pattern-sanitizers:
      - pattern: shlex.quote(...)
      - pattern: int(...)
```

### Full Rule with Metadata

```yaml
rules:
  - id: flask-sql-injection
    languages: [python]
    message: "SQL injection: user input flows to query without parameterization"
    severity: ERROR
    metadata:
      cwe: "CWE-89: SQL Injection"
      owasp: "A03:2021 - Injection"
      confidence: HIGH
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
      - pattern: request.form[...]
      - pattern: request.json
    pattern-sinks:
      - pattern: cursor.execute($QUERY)
      - pattern: db.execute($QUERY)
    pattern-sanitizers:
      - pattern: int(...)
    fix: cursor.execute($QUERY, (params,))
```

## Testing Rules

### Test File Format

```python
# test_rule.py
def test_vulnerable():
    user_input = request.args.get("id")
    # ruleid: flask-sql-injection
    cursor.execute("SELECT * FROM users WHERE id = " + user_input)

def test_safe():
    user_input = request.args.get("id")
    # ok: flask-sql-injection
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
```

```bash
semgrep --test rules/
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Semgrep

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 1 * *'  # Monthly

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: returntocorp/semgrep

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for diff-aware scanning

      - name: Run Semgrep
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            semgrep ci --baseline-commit ${{ github.event.pull_request.base.sha }}
          else
            semgrep ci
          fi
        env:
          SEMGREP_RULES: >-
            p/security-audit
            p/owasp-top-ten
            p/trailofbits
```

## Configuration

### .semgrepignore

```
tests/fixtures/
**/testdata/
generated/
vendor/
node_modules/
```

### Suppress False Positives

```python
password = get_from_vault()  # nosemgrep: hardcoded-password
dangerous_but_safe()  # nosemgrep
```

## Performance

```bash
semgrep --config rules/ --time .    # Check rule performance
ulimit -n 4096                       # Increase file descriptors for large codebases
```

### Path Filtering in Rules

```yaml
rules:
  - id: my-rule
    paths:
      include: [src/]
      exclude: [src/generated/]
```

## Common Use Cases

### 1. Comprehensive Security Audit

```bash
# Multi-ruleset scan with SARIF output
semgrep scan \
  --config p/security-audit \
  --config p/owasp-top-ten \
  --config p/cwe-top-25 \
  --sarif -o security-audit.sarif \
  .
```

### 2. Language-Specific Deep Scan

```bash
# Python with taint mode
semgrep scan \
  --config p/python \
  --config p/flask \
  --config p/django \
  --dataflow-traces \
  --sarif -o python-security.sarif \
  ./backend

# JavaScript/TypeScript
semgrep scan \
  --config p/javascript \
  --config p/typescript \
  --config p/react \
  --sarif -o js-security.sarif \
  ./frontend
```

### 3. Custom Rules with Existing Rulesets

```bash
# Combine custom and community rules
semgrep scan \
  --config ./custom-rules \
  --config p/security-audit \
  --sarif -o combined-scan.sarif \
  .
```

### 4. CI/CD Diff Scanning

```bash
# Scan only changed files (PR context)
git diff --name-only origin/main...HEAD | \
  xargs semgrep scan --config p/security-audit --sarif -o diff-scan.sarif
```

### 5. Baldwin.sh Integration

While baldwin.sh uses Opengrep, Semgrep commands are identical:

```bash
# Equivalent to opengrep in baldwin.sh
semgrep scan \
  -f /workspace/data/semgrep-rules \
  -f /workspace/data/trailofbits-rules \
  --dataflow-traces \
  --severity=WARNING \
  --severity=ERROR \
  --exclude=test \
  --exclude=tests \
  --sarif \
  -o /workspace/output/sarif/semgrep.sarif \
  /workspace/src
```

## Understanding Output

### SARIF Structure

Semgrep SARIF v2.1.0 includes:

- **Rules**: Each Semgrep rule with metadata
- **Results**: Specific code locations matching patterns
- **Properties**:
  - Severity: ERROR, WARNING, INFO
  - CWE and OWASP mappings
  - Confidence levels
  - Fix suggestions (if available)
  - Dataflow traces (if enabled)

### Result Categories

| Severity | Meaning |
|----------|---------|
| **ERROR** | High-confidence security vulnerability |
| **WARNING** | Potential security issue requiring review |
| **INFO** | Code smell or best practice violation |

## Autofix

```bash
# Show available fixes
semgrep scan --config p/security-audit --autofix --dryrun .

# Apply fixes automatically
semgrep scan --config p/security-audit --autofix .

# Review fixes before applying
semgrep scan --config p/security-audit --autofix --dryrun . | less
```

## Third-Party Rules

```bash
# Trail of Bits rules
git clone https://github.com/trailofbits/semgrep-rules.git
semgrep scan -f semgrep-rules/rules --sarif -o results.sarif .

# Semgrep Registry
semgrep scan --config "r/trailofbits" .

# Custom remote rules
semgrep scan --config https://example.com/custom-rules.yaml .
```

## Advanced Rule Development

### Using Metavariable Propagation

```yaml
rules:
  - id: context-aware-xss
    languages: [javascript]
    message: "XSS: User input flows to innerHTML"
    severity: ERROR
    mode: taint
    pattern-sources:
      - pattern: req.query.$PARAM
    pattern-propagators:
      - pattern: $X.toString()
        from: $X
        to: $X.toString()
      - pattern: `${$X}`
        from: $X
        to: `${$X}`
    pattern-sinks:
      - pattern: $ELEMENT.innerHTML = $DATA
    pattern-sanitizers:
      - pattern: DOMPurify.sanitize($X)
```

### Focus Metavariables

```yaml
rules:
  - id: sql-injection-advanced
    languages: [python]
    message: "SQL injection via string formatting"
    severity: ERROR
    pattern: |
      $CURSOR.execute($QUERY)
    focus-metavariable: $QUERY
    metavariable-regex:
      metavariable: $QUERY
      regex: .*(\+|format|%).*
```

## Performance Optimization

```bash
# Limit to specific file types
semgrep scan --include='*.py' --include='*.js' .

# Increase timeout for large files
semgrep scan --timeout 60 .

# Use baseline for faster incremental scans
semgrep scan --baseline-commit HEAD~1 .

# Parallel processing (default uses all CPUs)
semgrep scan --jobs 4 .

# Disable expensive rules
semgrep scan --config p/security-audit --exclude-rule 'expensive-rule-id' .
```

## Supported Languages

Semgrep supports 30+ languages:

- **Web**: JavaScript, TypeScript, JSX, TSX, HTML
- **Backend**: Python, Go, Java, Kotlin, Scala, C#
- **Systems**: C, C++, Rust
- **Mobile**: Swift, Kotlin, Java, Objective-C
- **Scripting**: Ruby, PHP, Bash, Lua, Perl
- **Infrastructure**: Terraform, Dockerfile, YAML, JSON
- **Data**: SQL (generic)
- **Other**: Elixir, Clojure, Solidity, Apex, R

## Semgrep Pro vs Community Edition

| Feature | Community | Pro |
|---------|-----------|-----|
| **Pattern matching** | ✓ | ✓ |
| **Intra-file taint** | ✓ | ✓ |
| **Custom rules** | ✓ | ✓ |
| **SARIF output** | ✓ | ✓ |
| **Cross-file analysis** | ✗ | ✓ |
| **Interfile taint** | ✗ | ✓ |
| **Supply chain** | ✗ | ✓ |
| **Secrets detection** | ✗ | ✓ |
| **Assistant (AI)** | ✗ | ✓ |

## Troubleshooting

### Common Issues

```bash
# Rule parsing errors
semgrep scan --validate --config custom-rules.yaml

# Timeout on large files
semgrep scan --timeout 120 .

# Memory issues
semgrep scan --max-memory 4000 .  # MB

# Debug mode
semgrep scan --debug --config p/security-audit .
```

### Rule Testing

```bash
# Test rules against test files
semgrep scan --test rules/

# Validate rule syntax
semgrep scan --validate --config rules/my-rule.yaml

# Benchmark rules
semgrep scan --time --config rules/ test-codebase/
```

## Limitations

- **Cross-file limited**: Intra-file taint only in Community Edition
- **Pattern-based**: Can't understand complex business logic
- **Performance**: Large codebases with many rules can be slow
- **False positives**: Regex patterns may over-match
- **Language gaps**: Some languages have limited rule coverage

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "Semgrep found nothing, code is clean" | Semgrep is pattern-based; it can't track complex data flow across functions |
| "I wrote a rule, so we're covered" | Rules need testing with `semgrep --test`; false negatives are silent |
| "Taint mode catches injection" | Only if you defined all sources, sinks, AND sanitizers correctly |
| "Pro rules are comprehensive" | Pro rules are good but not exhaustive; supplement with custom rules for your codebase |
| "Too many findings = noisy tool" | High finding count often means real problems; tune rules, don't disable them |

## References

- Registry: <https://semgrep.dev/explore>
- Playground: <https://semgrep.dev/playground>
- Documentation: <https://semgrep.dev/docs/>
- Rule Examples: <https://semgrep.dev/docs/writing-rules/rule-ideas>
- Pattern Syntax: <https://semgrep.dev/docs/writing-rules/pattern-syntax>
- Trail of Bits Rules: <https://github.com/trailofbits/semgrep-rules>
- OWASP Rules: <https://semgrep.dev/p/owasp-top-ten>
- Blog: <https://semgrep.dev/blog/>
- GitHub Action: <https://github.com/returntocorp/semgrep-action>
- SARIF Spec: <https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html>
- Initial Source: [Trail of Bits skills](https://github.com/trailofbits/skills)
- Baldwin.sh Integration: <https://github.com/igbuend/baldwin.sh>
