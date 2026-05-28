# SDLC Requirements by Project Type

Detailed validation requirements for each supported project type.

## Claude Code Plugins

### Structure Validation
- `plugin.json` or `.claude-plugin/plugin.json` exists
- Required fields present: `name`, `version`, `description`
- Valid JSON syntax

### Component Validation
- **Agents**: Check `agents/` directory for `.md` files with YAML frontmatter
- **Skills**: Check `skills/*/SKILL.md` exists with valid frontmatter
- **Commands**: Check `commands/*.md` exists
- **Hooks**: Validate `hooks.json` if present

### Frontmatter Requirements
```yaml
---
name: required-field
description: required-field
allowed-tools: optional
---
```

## Python Projects

### Test Validation
```bash
python3 -m pytest --cov=. --cov-report=term-missing -q
```
- All tests must pass
- Coverage must meet threshold (default 95%)

### Lint Validation
```bash
# Primary: ruff (fast)
ruff check .

# Fallback: flake8
flake8 .
```

### Type Checking
```bash
mypy . --ignore-missing-imports
```
- Type errors are warnings (non-blocking)

### Security Scanning
```bash
# Code security
bandit -r . -q

# Dependency vulnerabilities
pip-audit
```

### Required Files
- `pyproject.toml` or `setup.py`
- `pytest.ini` or pytest config in pyproject.toml (recommended)

## Node.js Projects

### Test Validation
```bash
npm test
```
- Must have `test` script in package.json
- All tests must pass

### Lint Validation
```bash
# If lint script exists
npm run lint

# Fallback: direct eslint
npx eslint .
```

### Security Scanning
```bash
npm audit --production
```

### Required Files
- `package.json` with `name`, `version`
- `package-lock.json` (recommended)

## Go Projects

### Test Validation
```bash
go test -cover -race ./...
```
- All tests must pass
- Coverage must meet threshold
- Race detector enabled

### Lint Validation
```bash
golangci-lint run
```

### Vet Validation
```bash
go vet ./...
```

### Required Files
- `go.mod` with module declaration
- `go.sum` (recommended)

## Rust Projects

### Test Validation
```bash
cargo test
```
- All tests must pass

### Lint Validation
```bash
cargo clippy -- -D warnings
```
- Warnings treated as errors

### Security Scanning
```bash
cargo audit
```

### Format Validation
```bash
cargo fmt --check
```
- Code must be formatted

### Required Files
- `Cargo.toml` with `name`, `version`
- `Cargo.lock` (recommended for binaries)

## Common Validations (All Projects)

### CHANGELOG.md
- File must exist
- Must contain `## [Unreleased]` section
- Entries should follow Keep a Changelog format

### CI Configuration
Check for presence of:
- `.github/workflows/*.yml` (GitHub Actions)
- `.gitlab-ci.yml` (GitLab CI)
- `Jenkinsfile` (Jenkins)
- `.circleci/` (CircleCI)

### Breaking Change Detection
Analyze git diff since last tag:
```bash
git diff --name-status $(git describe --tags --abbrev=0)..HEAD
```

Breaking indicators:
- `D` (deleted) - Public files removed
- `R` (renamed) - Public files renamed
- Excludes: dotfiles, test files

### Git Status
- Working directory should be clean (or changes explicitly included)
- Branch should be up to date with remote

## Coverage Thresholds

| Project Type | Default | Config Location |
|--------------|---------|-----------------|
| Python | 95% | pyproject.toml `[tool.pytest.ini_options]` |
| Node.js | 95% | package.json `jest.coverageThreshold` |
| Go | 95% | Command line |
| Rust | N/A | cargo-tarpaulin if available |

### Python Coverage Config
```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-fail-under=95"
```

### Node.js Coverage Config
```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "lines": 95
      }
    }
  }
}
```

## Validation Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | One or more validations failed |

## Remediation Guide

### Tests Failing
1. Run tests locally: `pytest -v` / `npm test` / `go test -v ./...`
2. Fix failing tests
3. Verify all pass before release

### Coverage Below Threshold
1. Identify uncovered code: `pytest --cov-report=html`
2. Add tests for uncovered paths
3. Or lower threshold with `--coverage=N` flag

### Lint Errors
1. Run linter with auto-fix: `ruff check --fix .` / `npm run lint -- --fix`
2. Manually fix remaining issues
3. Verify clean lint pass

### Security Vulnerabilities
1. Review vulnerability details
2. Update affected dependencies
3. Or document accepted risks

### Missing CHANGELOG
1. Create CHANGELOG.md
2. Add `## [Unreleased]` section
3. Document changes for this release
