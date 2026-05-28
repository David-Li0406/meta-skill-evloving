---
name: semgrep
description: Use this skill when you need to perform fast security scanning and pattern matching on code using Semgrep, write custom YAML rules, or set up Semgrep in CI/CD pipelines.
---

# Semgrep Static Analysis

## When to Use Semgrep

**Ideal scenarios:**
- Quick security scans (minutes, not hours)
- Pattern-based vulnerability detection
- Enforcing coding standards and best practices
- Finding known vulnerability patterns (e.g., OWASP Top 10, CWE Top 25)
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
semgrep --config p/security-audit --sarif -o results.sarif .   # SARIF
semgrep --config p/security-audit --json -o results.json .     # JSON
semgrep --config p/security-audit --dataflow-traces .          # Show data flow
```

### 4. Scan Specific Paths

```bash
semgrep --config p/python app.py           # Single file analysis
```