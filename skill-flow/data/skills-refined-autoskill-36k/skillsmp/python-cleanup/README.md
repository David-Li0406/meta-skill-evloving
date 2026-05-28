# Python Dead Code & Clean-Up Analysis Skill

A comprehensive skill for analyzing and cleaning up Python codebases using static analysis, coverage, dependency checks, and security scanning.

## What It Does

This skill helps you:

- **Find dead code** - Identify unused functions, classes, variables, and imports
- **Analyze dependencies** - Detect unused, undeclared, or vulnerable dependencies
- **Check test coverage** - Find code never executed by tests
- **Modernize syntax** - Upgrade to modern Python features (f-strings, type hints, etc.)
- **Scan for security issues** - Find vulnerabilities, secrets, and unsafe patterns
- **Measure complexity** - Identify overly complex code that needs refactoring
- **Clean project artifacts** - Remove cache files and build artifacts

## Quick Start

### Installation

Install the required tools:

```bash
# Core tools (likely already in your project)
uv add --dev ruff mypy pytest pytest-cov

# Additional analysis tools
uv add --dev vulture deptry pip-audit pyupgrade radon bandit
```

### 5-Minute Quick Sweep

```bash
# Lint and format
uv run ruff check . --fix && uv run ruff format .

# Find dead code
uv run vulture src tests --min-confidence 80

# Check dependencies
uv run deptry .

# Security scan
uv run pip-audit
uv run bandit -r src --severity-level medium
```

### 30-Minute Deep Analysis

```bash
# Test coverage (find untested code)
uv run pytest --cov=src --cov-report=html

# Complexity analysis
uv run radon cc src -s -n B

# Type checking
uv run mypy src

# Full security audit
uv run pip-audit
uv run bandit -r src
```

## Common Use Cases

### 1. Weekly Maintenance

Keep your codebase healthy with regular clean-ups:

```bash
# Run this weekly
uv run ruff check . --fix
uv run ruff format .
uv run deptry .
uv run pip-audit
uv run pytest --cov=src --cov-report=term-missing
```

### 2. Pre-Merge Code Review

Before merging a large feature:

```bash
# Check what changed
git diff main...HEAD --name-only '*.py' | xargs uv run vulture --min-confidence 80

# Verify dependencies
uv run deptry .

# Check coverage
uv run pytest --cov=src --cov-fail-under=80

# Security scan
uv run bandit -r src
```

### 3. After Removing Features

Deep clean after removing major features:

```bash
# Find all dead code
uv run vulture src tests --min-confidence 60

# Verify with coverage
uv run pytest --cov=src --cov-report=html

# Remove unused dependencies
uv run deptry .

# Clean unused imports
uv run autoflake -r --remove-all-unused-imports src
```

### 4. Modernization Sprint

Upgrade entire codebase to modern Python:

```bash
# Upgrade syntax to Python 3.12+
uv run pyupgrade --py312-plus $(git ls-files '*.py')

# Clean up
uv run ruff check . --fix
uv run ruff format .

# Verify
uv run pytest
uv run mypy src
```

## Tools Included

| Tool | Purpose | Speed | Reliability |
|------|---------|-------|-------------|
| **coverage.py** | Find untested code | Medium | ⭐⭐⭐⭐⭐ |
| **vulture** | Find unused code | Fast | ⭐⭐⭐⭐ |
| **deptry** | Check dependencies | Fast | ⭐⭐⭐⭐⭐ |
| **ruff** | Lint & format | Very Fast | ⭐⭐⭐⭐⭐ |
| **mypy** | Type checking | Medium | ⭐⭐⭐⭐⭐ |
| **bandit** | Security scanning | Fast | ⭐⭐⭐⭐ |
| **pip-audit** | Vulnerability check | Fast | ⭐⭐⭐⭐⭐ |
| **radon** | Complexity analysis | Fast | ⭐⭐⭐⭐⭐ |
| **pyupgrade** | Modernize syntax | Fast | ⭐⭐⭐⭐⭐ |

## How to Use This Skill

### From Claude Code CLI

Simply ask Claude to analyze your code:

```
"Can you run a dead code analysis on this project?"
"Find unused dependencies"
"Check test coverage and find untested code"
"Run a security scan"
"Modernize Python syntax to 3.12+"
```

Claude will automatically:
1. Install required tools (if missing)
2. Run appropriate analysis commands
3. Interpret results
4. Suggest fixes
5. Apply safe automated fixes (with your approval)

### Manual Invocation

You can also run the tools directly:

```bash
# See all available commands
uv run vulture --help
uv run deptry --help
uv run radon --help

# Run specific analyses
uv run vulture src --min-confidence 80
uv run deptry .
uv run radon cc src -s
```

## Integration Options

### Pre-Commit Hooks

Add checks to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/jendrikseipp/vulture
    rev: 'v2.11'
    hooks:
      - id: vulture
        args: [src, tests, --min-confidence=80]

  - repo: https://github.com/fpgmaas/deptry
    rev: '0.20.0'
    hooks:
      - id: deptry
```

### CI/CD Pipeline

Add to GitHub Actions (`.github/workflows/quality.yml`):

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv python install 3.12
      - run: uv sync --all-extras
      - run: uv run ruff check .
      - run: uv run mypy src
      - run: uv run vulture src tests --min-confidence 80
      - run: uv run deptry .
      - run: uv run bandit -r src
      - run: uv run pip-audit
      - run: uv run pytest --cov=src --cov-fail-under=80
```

## Best Practices

### ✅ Do This

- Start with high confidence thresholds (Vulture: 80+)
- Always review automated changes before committing
- Run tests after applying fixes
- Use coverage.py for ground truth (dynamic analysis)
- Combine multiple tools for comprehensive analysis
- Create whitelists for intentional "unused" code

### ❌ Avoid This

- Blindly applying automated fixes without review
- Trusting only static analysis (use coverage too)
- Removing code flagged by Vulture without verification
- Skipping tests after automated changes
- Ignoring security warnings
- Running all tools at once when starting (start simple)

## Interpreting Results

### Vulture (Dead Code)

```
src/example.py:42: unused function 'old_helper' (80% confidence)
```

**Action:**
- 80-100% confidence: Usually safe to remove
- 60-79%: Review carefully (may be used dynamically)
- <60%: Often false positive, skip

### Coverage (Test Coverage)

```
src/example.py    85%    15 missed lines
```

**Action:**
- Green (100%): Fully tested
- Yellow (70-99%): Add tests for red lines
- Red (<70%): Needs significant test coverage

### deptry (Dependencies)

```
unused: package-name (declared but never imported)
undeclared: another-package (imported but not declared)
```

**Action:**
- **Unused**: Remove with `uv remove package-name`
- **Undeclared**: Add with `uv add package-name`

### Radon (Complexity)

```
src/example.py:complex_function - B (complexity: 8)
src/example.py:very_complex - D (complexity: 25)
```

**Action:**
- A-B: No action needed
- C: Consider simplifying
- D+: Refactor (break into smaller functions)

## Troubleshooting

### False Positives in Vulture

**Problem:** Vulture flags code that's actually used (e.g., Pydantic fields, FastAPI routes).

**Solution:** Create a whitelist file:
```python
# vulture_whitelist.py
_.pydantic_field
MyClass.abstract_method
test_fixture_name
```

Run: `vulture src tests vulture_whitelist.py --min-confidence 80`

### Autoflake Removed Needed Imports

**Problem:** Imports needed for side effects were removed.

**Solution:** Add `# noqa: F401` comment:
```python
import needed_for_side_effects  # noqa: F401
```

### Low Coverage in Integration Tests

**Problem:** Integration tests use mocked/recorded responses, lowering coverage.

**Solution:** Check coverage separately:
```bash
# Unit tests (should be high)
pytest tests/unit/ --cov=src

# Integration tests (may be lower, OK)
pytest tests/integration/ --cov=src --cov-append
```

## Resources

### Documentation

- **Vulture**: https://github.com/jendrikseipp/vulture
- **deptry**: https://github.com/fpgmaas/deptry
- **Ruff**: https://docs.astral.sh/ruff/
- **Coverage.py**: https://coverage.readthedocs.io/
- **Radon**: https://radon.readthedocs.io/
- **Bandit**: https://bandit.readthedocs.io/
- **pip-audit**: https://github.com/pypa/pip-audit

### Skill Files

- `SKILL.md` - Comprehensive tool reference and workflows
- `examples.md` - Practical examples for common scenarios
- `README.md` - This file (user-facing documentation)

## Support

For issues or questions:
1. Check the troubleshooting section in `SKILL.md`
2. Review examples in `examples.md`
3. Consult tool-specific documentation (links above)
4. Ask Claude for help interpreting results

## Contributing

To improve this skill:
1. Add new tools to the tool list
2. Share workflow examples
3. Document false positive patterns
4. Add project-specific configurations
5. Share lessons learned

## License

This skill is part of the Egregora project and follows the same license.

---

**Quick command reference:**

```bash
# Dead code
vulture src tests --min-confidence 80

# Dependencies
deptry .

# Coverage
pytest --cov=src --cov-report=html

# Lint/format
ruff check . --fix && ruff format .

# Modernize
pyupgrade --py312-plus $(git ls-files '*.py')

# Security
pip-audit && bandit -r src

# Complexity
radon cc src -s -n B

# Everything
pre-commit run --all-files
```

Happy cleaning! 🧹
