# Project Setup Checklist

## Repository Basics

### Essential Files

| File | Purpose | Priority |
|------|---------|----------|
| `README.md` | Project overview, quick start | Critical |
| `LICENSE` | Legal terms for use | Critical |
| `.gitignore` | Exclude build artifacts, secrets | Critical |
| `CONTRIBUTING.md` | How to contribute | High |
| `CHANGELOG.md` | Version history | High |
| `CODE_OF_CONDUCT.md` | Community guidelines | Medium |
| `SECURITY.md` | Vulnerability reporting | High |

### README Structure

```markdown
# Project Name

One-line description of what this does.

## Quick Start

\`\`\`bash
# 3-5 commands to see it work
\`\`\`

## Installation

Full installation instructions.

## Usage

Common use cases with examples.

## Configuration

All options documented.

## Contributing

Link to CONTRIBUTING.md

## License

[LICENSE_TYPE](LICENSE)
```

### .gitignore Essentials

```gitignore
# Dependencies
node_modules/
vendor/
.venv/
__pycache__/

# Build outputs
dist/
build/
*.o
*.exe

# IDE
.idea/
.vscode/
*.swp

# Environment (CRITICAL - never commit)
.env
.env.local
*.pem
*.key

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test coverage
coverage/
.nyc_output/
```

## Development Environment

### Configuration Files

| Language | Files |
|----------|-------|
| Node.js | `package.json`, `tsconfig.json`, `.nvmrc` |
| Python | `pyproject.toml`, `requirements.txt`, `.python-version` |
| Go | `go.mod`, `go.sum` |
| Rust | `Cargo.toml`, `Cargo.lock` |
| Java | `pom.xml` or `build.gradle` |

### Linting & Formatting

| Language | Linter | Formatter |
|----------|--------|-----------|
| JavaScript/TypeScript | ESLint | Prettier |
| Python | Ruff, Flake8 | Black, Ruff |
| Go | golangci-lint | gofmt |
| Rust | Clippy | rustfmt |
| Java | Checkstyle | google-java-format |

### Editor Configuration

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{py,java,go,rs}]
indent_size = 4

[Makefile]
indent_style = tab
```

## CI/CD Pipeline

### Minimum Pipeline Stages

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: npm test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security scan
        run: npm audit
```

### Branch Protection

- [ ] Require PR reviews (1+ approvals)
- [ ] Require status checks to pass
- [ ] Require branches to be up to date
- [ ] Block force pushes to main
- [ ] Restrict who can push to main

## Security

### Secrets Management

| Location | Example | Risk |
|----------|---------|------|
| `.env` | `API_KEY=sk-...` | In gitignore |
| `config.json` | Hardcoded | **HIGH RISK** |
| CI Variables | GitHub Secrets | Secure |
| Vault | HashiCorp/AWS | Most secure |

### Required Checks

- [ ] No secrets in code (use gitleaks)
- [ ] Dependencies scanned (Dependabot)
- [ ] SAST enabled (Semgrep, CodeQL)
- [ ] Container scanning (if applicable)

### Security Policy Template

```markdown
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x | :white_check_mark: |
| 1.x | :x: |

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com.

Do NOT create public GitHub issues for security vulnerabilities.

We will respond within 48 hours.
```

## Testing

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with dependencies
├── e2e/            # End-to-end tests
└── fixtures/       # Test data
```

### Coverage Targets

| Type | Target | Critical Paths |
|------|--------|----------------|
| Unit | 80%+ | All business logic |
| Integration | Key paths | Database, APIs |
| E2E | Happy paths | User journeys |

## Documentation

### Code Documentation

- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] Examples provided
- [ ] Types documented (TypeScript/JSDoc)

### Architecture Documentation

- [ ] System overview diagram
- [ ] Key design decisions (ADRs)
- [ ] Data flow documented
- [ ] Deployment architecture

## Quick Audit Commands

```bash
# Check for missing files
for f in README.md LICENSE .gitignore; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ $f missing"
done

# Check for secrets
gitleaks detect --source .

# Count tests
find . -name "*_test.*" -o -name "*.test.*" | wc -l

# Check dependencies
npm outdated    # Node.js
pip list -o     # Python
go list -m -u all  # Go

# Check CI config exists
[ -d ".github/workflows" ] && echo "✓ CI" || echo "✗ No CI"
```

## Audit Report Template

```markdown
# Project Audit: [Name]

**Date:** YYYY-MM-DD
**Health:** Good / Fair / Poor

## Summary

| Category | Status |
|----------|--------|
| Essential files | ✓/✗ |
| CI/CD | ✓/✗ |
| Security | ✓/✗ |
| Testing | ✓/✗ |
| Documentation | ✓/✗ |

## Critical Issues

1. [Issue]: [Impact] → [Recommendation]

## Recommendations

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```
