# Semgrep - Static Analysis Engine

## Overview

Semgrep is a fast, open-source static analysis tool for finding bugs, detecting vulnerabilities, and enforcing code standards. It supports 30+ languages and uses a pattern syntax similar to the code being searched.

## Technology Details

| Attribute | Value |
|-----------|-------|
| Category | Code Security / SAST |
| Type | Static Analysis Engine |
| Maintained By | Semgrep Inc (formerly r2c) |
| License | LGPL-2.1 |
| Website | https://semgrep.dev |
| Registry | https://semgrep.dev/explore |

## Directory Structure

```
rag/semgrep/
├── semgrep.md              # This documentation
├── community-rules/        # Downloaded registry rules (cached)
│   ├── default/            # Default profile rules
│   ├── security/           # Security-focused rules
│   ├── quality/            # Code quality rules
│   └── languages/          # Language-specific rules
├── custom-rules/           # Gibson custom rules
└── documentation/          # Additional docs
```

## Rule Packs

### Security Packs

| Pack | Description | Rules |
|------|-------------|-------|
| `p/security-audit` | Comprehensive security audit | 500+ |
| `p/owasp-top-ten` | OWASP Top 10 vulnerabilities | 100+ |
| `p/cwe-top-25` | CWE Top 25 dangerous weaknesses | 80+ |
| `p/secrets` | Secret/credential detection | 200+ |
| `p/supply-chain` | Supply chain security | 50+ |
| `p/command-injection` | Command injection patterns | 30+ |
| `p/sql-injection` | SQL injection patterns | 40+ |
| `p/xss` | Cross-site scripting | 50+ |
| `p/insecure-transport` | TLS/SSL issues | 20+ |

### Quality Packs

| Pack | Description |
|------|-------------|
| `p/best-practices` | Language best practices |
| `p/maintainability` | Code maintainability |

### Language Packs

| Pack | Languages |
|------|-----------|
| `p/python` | Python security + quality |
| `p/javascript` | JavaScript/TypeScript |
| `p/java` | Java security |
| `p/go` | Go security |
| `p/ruby` | Ruby security |
| `p/php` | PHP security |
| `p/c` | C/C++ security |
| `p/rust` | Rust security |

## Profiles

Gibson provides three scanning profiles:

### Default Profile
- Tech discovery + basic security
- Rules: secrets, security-audit
- Git blame enrichment: enabled
- Use case: General purpose scanning

### Security Profile
- Comprehensive security scanning
- Rules: All security packs (OWASP, CWE, injection, etc.)
- Git blame enrichment: enabled
- Use case: Security audits, compliance

### Quick Profile
- Fast tech discovery only
- Rules: Custom rules only (no community)
- Git blame enrichment: disabled
- Use case: Quick inventory, CI/CD

## Usage

### Sync Community Rules

```bash
# Sync default rules
./utils/scanners/semgrep/community-rules.sh sync

# Sync security rules
./utils/scanners/semgrep/community-rules.sh sync security

# Sync all profiles
./utils/scanners/semgrep/community-rules.sh sync all --force

# Check status
./utils/scanners/semgrep/community-rules.sh status
```

### Run Scanner

```bash
# Default profile
./utils/scanners/semgrep/semgrep-scanner.sh /path/to/repo

# Security profile
./utils/scanners/semgrep/semgrep-scanner.sh --profile security /path/to/repo

# Quick profile (no community rules)
./utils/scanners/semgrep/semgrep-scanner.sh --profile quick /path/to/repo

# Custom options
./utils/scanners/semgrep/semgrep-scanner.sh --type secrets --no-git -o results.json /path/to/repo
```

## Rule Format

Semgrep rules are YAML files with this structure:

```yaml
rules:
  - id: rule-id
    message: Description of the issue
    severity: ERROR | WARNING | INFO
    languages:
      - python
      - javascript
    pattern: |
      dangerous_function($ARG)
    metadata:
      category: security
      technology: python
      cwe: CWE-78
      owasp: A1:2017
```

### Pattern Types

| Type | Description | Example |
|------|-------------|---------|
| `pattern` | Exact match | `eval($X)` |
| `pattern-either` | Match any | Multiple patterns |
| `pattern-regex` | Regex match | `api_key.*=.*["']` |
| `pattern-inside` | Context match | Inside a function |
| `pattern-not` | Exclusion | Except safe patterns |

## Integration

### With Phantom

Semgrep is integrated into phantom's scanning pipeline:

1. **Bootstrap**: Community rules synced on startup
2. **Tech Discovery**: Identifies technologies via import patterns
3. **Security Scanning**: Finds vulnerabilities using security profiles
4. **Results**: JSON output with git blame enrichment

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run Semgrep
  run: |
    ./utils/scanners/semgrep/semgrep-scanner.sh \
      --profile security \
      -o semgrep-results.json \
      ${{ github.workspace }}
```

## Custom Rules

Gibson generates custom rules from RAG patterns:

```bash
# Regenerate custom rules from RAG
python3 utils/scanners/semgrep/rag-to-semgrep.py \
  rag/technology-identification \
  utils/scanners/semgrep/rules
```

Custom rules are stored in `utils/scanners/semgrep/rules/`:
- `tech-discovery.yaml` - Technology detection
- `secrets.yaml` - Secret patterns
- `tech-debt.yaml` - TODO/FIXME markers

## Performance

### Optimization Tips

1. **Use profiles appropriately**: `quick` for CI, `security` for audits
2. **Exclude large directories**: node_modules, vendor, dist
3. **Set timeouts**: `--timeout 30` for large files
4. **Limit memory**: `--max-memory 4096` MB

### Caching

Community rules are cached for 24 hours to avoid redundant downloads:
- Cache location: `rag/semgrep/community-rules/<profile>/.last-update`
- Force refresh: `community-rules.sh sync --force`

## Resources

- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Rule Registry](https://semgrep.dev/explore)
- [Writing Rules](https://semgrep.dev/docs/writing-rules/overview)
- [Pattern Syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax)
