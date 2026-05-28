# Python Clean-Up Skill - Practical Examples

This document provides real-world examples of using the Python clean-up tools in common scenarios.

## Table of Contents

1. [First-Time Setup](#first-time-setup)
2. [Weekly Maintenance Workflow](#weekly-maintenance-workflow)
3. [Pre-Release Checklist](#pre-release-checklist)
4. [Refactoring Large Features](#refactoring-large-features)
5. [Onboarding to Legacy Codebase](#onboarding-to-legacy-codebase)
6. [CI/CD Integration](#cicd-integration)
7. [Handling False Positives](#handling-false-positives)
8. [Project-Specific Examples](#project-specific-examples)

---

## First-Time Setup

### Scenario: You want to start using these tools in your project

```bash
# Step 1: Install all tools
uv add --dev ruff mypy pytest pytest-cov vulture deptry pip-audit \
              pyupgrade autoflake radon xenon bandit detect-secrets pre-commit

# Step 2: Run initial assessment (don't fix anything yet)
echo "=== Linting Issues ==="
uv run ruff check . --statistics

echo "=== Dead Code (High Confidence) ==="
uv run vulture src tests --min-confidence 80

echo "=== Dependency Issues ==="
uv run deptry .

echo "=== Security Issues ==="
uv run bandit -r src --severity-level high

echo "=== Test Coverage ==="
uv run pytest --cov=src --cov-report=term-missing

echo "=== Complexity Issues ==="
uv run radon cc src -s -n C

# Step 3: Create baseline (save to file for tracking progress)
uv run ruff check . --statistics > baseline-report.txt
uv run vulture src tests --min-confidence 80 >> baseline-report.txt
uv run radon cc src -s >> baseline-report.txt

# Step 4: Review the report and prioritize fixes
cat baseline-report.txt
```

**Expected output interpretation:**

```
=== Linting Issues ===
10 F401 [*] `module` imported but unused
5 E501 Line too long (120 > 110 characters)
2 BLE001 Do not catch blind exception: `Exception`

=== Dead Code (High Confidence) ===
src/old_utils.py:42: unused function 'deprecated_helper' (95% confidence)
src/models.py:105: unused variable 'temp' (80% confidence)

=== Dependency Issues ===
unused: requests (declared but never imported)
undeclared: httpx (imported in src/api.py but not in dependencies)
```

**Next steps:**
1. Fix high-priority issues first (security, dependencies)
2. Set up pre-commit hooks
3. Create whitelists for false positives
4. Track progress weekly

---

## Weekly Maintenance Workflow

### Scenario: Keep codebase healthy with regular 15-minute clean-ups

Create a script `scripts/weekly-cleanup.sh`:

```bash
#!/bin/bash
set -e

echo "🧹 Starting weekly code cleanup..."

# Step 1: Update dependencies
echo "📦 Updating dependencies..."
uv sync --upgrade

# Step 2: Security checks (CRITICAL - do first)
echo "🔒 Checking for vulnerabilities..."
uv run pip-audit --severity high || {
    echo "❌ CRITICAL: Security vulnerabilities found!"
    exit 1
}

# Step 3: Lint and format
echo "✨ Linting and formatting..."
uv run ruff check . --fix
uv run ruff format .

# Step 4: Check for unused dependencies
echo "📦 Checking dependencies..."
uv run deptry . || echo "⚠️  Dependency issues found (review manually)"

# Step 5: Run tests with coverage
echo "🧪 Running tests with coverage..."
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=75

# Step 6: Check for dead code (high confidence only)
echo "🔍 Checking for dead code..."
uv run vulture src tests --min-confidence 80 || echo "⚠️  Dead code found (review manually)"

# Step 7: Quick complexity check
echo "📊 Checking complexity..."
uv run radon cc src -s -n C || echo "⚠️  Complex functions found (review manually)"

# Step 8: Commit if there are changes
if [[ -n $(git status --porcelain) ]]; then
    echo "💾 Committing changes..."
    git add -A
    git commit -m "chore: weekly code cleanup

- Update dependencies
- Fix linting issues
- Format code with ruff
- Run security audit (passed)
- Coverage: $(uv run pytest --cov=src -q | grep TOTAL | awk '{print $NF}')"
    echo "✅ Changes committed!"
else
    echo "✅ No changes needed!"
fi

echo "🎉 Weekly cleanup complete!"
```

Make it executable and run:

```bash
chmod +x scripts/weekly-cleanup.sh
./scripts/weekly-cleanup.sh
```

**Typical output:**

```
🧹 Starting weekly code cleanup...
📦 Updating dependencies...
Resolved 42 packages in 1.2s
🔒 Checking for vulnerabilities...
No known vulnerabilities found
✨ Linting and formatting...
Fixed 3 errors, formatted 12 files
📦 Checking dependencies...
All dependencies are used correctly
🧪 Running tests with coverage...
====== 145 passed in 5.23s ======
Coverage: 87%
🔍 Checking for dead code...
No issues found
📊 Checking complexity...
All functions have acceptable complexity
✅ No changes needed!
🎉 Weekly cleanup complete!
```

---

## Pre-Release Checklist

### Scenario: Before releasing v1.2.0, ensure code quality

Create a script `scripts/pre-release-check.sh`:

```bash
#!/bin/bash
set -e

VERSION=${1:-"unknown"}
echo "🚀 Pre-release checks for version $VERSION"

# Step 1: Security audit (BLOCKER)
echo "1️⃣ Security audit..."
uv run pip-audit || {
    echo "❌ BLOCKER: Security vulnerabilities found"
    exit 1
}
uv run bandit -r src --severity-level medium || {
    echo "❌ BLOCKER: Security issues in code"
    exit 1
}

# Step 2: Type checking (BLOCKER)
echo "2️⃣ Type checking..."
uv run mypy src || {
    echo "❌ BLOCKER: Type errors found"
    exit 1
}

# Step 3: Linting (BLOCKER)
echo "3️⃣ Linting..."
uv run ruff check . || {
    echo "❌ BLOCKER: Linting errors found"
    exit 1
}

# Step 4: Test coverage (BLOCKER if <80%)
echo "4️⃣ Test coverage..."
uv run pytest --cov=src --cov-fail-under=80 --cov-report=html || {
    echo "❌ BLOCKER: Coverage below 80%"
    exit 1
}

# Step 5: Dependency check (WARNING only)
echo "5️⃣ Dependency check..."
uv run deptry . || echo "⚠️  WARNING: Dependency issues found"

# Step 6: Dead code check (WARNING only)
echo "6️⃣ Dead code check..."
DEAD_CODE=$(uv run vulture src tests --min-confidence 80 | wc -l)
if [ $DEAD_CODE -gt 0 ]; then
    echo "⚠️  WARNING: $DEAD_CODE potential dead code issues found"
    uv run vulture src tests --min-confidence 80
fi

# Step 7: Complexity check (WARNING only)
echo "7️⃣ Complexity check..."
uv run radon cc src -s -n D || echo "⚠️  WARNING: High complexity functions found"

# Step 8: Check for secrets (BLOCKER)
echo "8️⃣ Scanning for secrets..."
uv run detect-secrets scan --all-files || {
    echo "❌ BLOCKER: Potential secrets found in code"
    exit 1
}

# Step 9: Generate reports
echo "9️⃣ Generating reports..."
mkdir -p reports/
uv run pytest --cov=src --cov-report=html:reports/coverage
uv run mypy src --html-report reports/mypy
uv run radon cc src -s > reports/complexity.txt
uv run bandit -r src -f html -o reports/security.html

echo "✅ All checks passed! Ready for release $VERSION"
echo "📊 Reports available in reports/"
```

Run before release:

```bash
./scripts/pre-release-check.sh v1.2.0
```

**If checks fail:**

```
❌ BLOCKER: Coverage below 80%
TOTAL: 142 statements, 108 covered, 76% coverage

Next steps:
1. Review uncovered code: open reports/coverage/index.html
2. Add tests for critical paths
3. Re-run pre-release checks
```

---

## Refactoring Large Features

### Scenario: You removed a major feature and want to clean up leftovers

```bash
#!/bin/bash
# scripts/deep-clean-after-feature-removal.sh

FEATURE_NAME=${1:-"feature"}
echo "🧹 Deep cleaning after removing $FEATURE_NAME"

# Step 1: Create a branch for cleanup
git checkout -b cleanup-${FEATURE_NAME}

# Step 2: Find all potential dead code (lower confidence threshold)
echo "1️⃣ Finding dead code (this may take a minute)..."
uv run vulture src tests --min-confidence 60 > dead-code-report.txt
echo "Found $(wc -l < dead-code-report.txt) potential issues"

# Step 3: Run coverage to verify dead code
echo "2️⃣ Running coverage analysis..."
uv run pytest --cov=src --cov-branch --cov-report=html

# Step 4: Find unused dependencies
echo "3️⃣ Checking for unused dependencies..."
uv run deptry . > dependency-report.txt || true

# Step 5: Remove unused imports (CAREFUL - review after)
echo "4️⃣ Removing unused imports..."
uv run autoflake -r --in-place --remove-all-unused-imports \
                  --remove-unused-variables src

# Step 6: Remove commented-out code
echo "5️⃣ Removing commented-out code..."
uv run eradicate -r --in-place src

# Step 7: Clean up formatting
echo "6️⃣ Formatting code..."
uv run ruff check . --fix
uv run ruff format .

# Step 8: Run tests to ensure nothing broke
echo "7️⃣ Running tests..."
uv run pytest || {
    echo "❌ Tests failed! Review changes carefully."
    git diff
    exit 1
}

# Step 9: Review all changes
echo "8️⃣ Reviewing changes..."
git diff --stat
echo ""
echo "Review the changes:"
echo "  git diff"
echo ""
echo "If everything looks good:"
echo "  git add -A"
echo "  git commit -m 'refactor: remove dead code after $FEATURE_NAME removal'"
echo "  git push -u origin cleanup-${FEATURE_NAME}"
```

**Example session:**

```bash
$ ./scripts/deep-clean-after-feature-removal.sh old-auth-system

🧹 Deep cleaning after removing old-auth-system
1️⃣ Finding dead code...
Found 23 potential issues

2️⃣ Running coverage analysis...
Coverage: 89% (was 87% before cleanup)

3️⃣ Checking for unused dependencies...
Found unused dependencies:
- pyjwt (used by old auth system)
- bcrypt (used by old auth system)

4️⃣ Removing unused imports...
Removed 15 unused imports

5️⃣ Removing commented-out code...
Cleaned 8 files

6️⃣ Formatting code...
Formatted 12 files

7️⃣ Running tests...
====== 145 passed in 5.23s ======

8️⃣ Reviewing changes...
 12 files changed, 342 insertions(+), 567 deletions(-)

Next steps:
1. Review: git diff
2. Commit: git add -A && git commit -m "refactor: remove dead code"
3. Push: git push -u origin cleanup-old-auth-system
```

---

## Onboarding to Legacy Codebase

### Scenario: You inherited a legacy codebase and want to understand its health

```bash
#!/bin/bash
# scripts/codebase-health-report.sh

echo "📊 Generating codebase health report..."

REPORT_DIR="codebase-health-$(date +%Y%m%d)"
mkdir -p $REPORT_DIR

# 1. Code statistics
echo "📈 Analyzing codebase statistics..."
echo "=== Code Statistics ===" > $REPORT_DIR/summary.txt
cloc src >> $REPORT_DIR/summary.txt

# 2. Test coverage
echo "🧪 Analyzing test coverage..."
uv run pytest --cov=src --cov-report=html:$REPORT_DIR/coverage \
              --cov-report=json:$REPORT_DIR/coverage.json -q
COVERAGE=$(python -c "import json; print(json.load(open('$REPORT_DIR/coverage.json'))['totals']['percent_covered'])")
echo "Coverage: $COVERAGE%" >> $REPORT_DIR/summary.txt

# 3. Dead code analysis
echo "🔍 Analyzing dead code..."
uv run vulture src tests --min-confidence 60 > $REPORT_DIR/dead-code.txt || true
DEAD_CODE_COUNT=$(wc -l < $REPORT_DIR/dead-code.txt)
echo "Potential dead code: $DEAD_CODE_COUNT issues" >> $REPORT_DIR/summary.txt

# 4. Complexity analysis
echo "📊 Analyzing complexity..."
uv run radon cc src -s --json > $REPORT_DIR/complexity.json
uv run radon cc src -s -n C > $REPORT_DIR/complex-functions.txt || true
COMPLEX_COUNT=$(wc -l < $REPORT_DIR/complex-functions.txt)
echo "Complex functions (C+): $COMPLEX_COUNT" >> $REPORT_DIR/summary.txt

# 5. Maintainability index
echo "🔧 Analyzing maintainability..."
uv run radon mi src -s > $REPORT_DIR/maintainability.txt
MI_AVG=$(uv run radon mi src -s | grep "Average MI" | awk '{print $3}')
echo "Maintainability Index: $MI_AVG" >> $REPORT_DIR/summary.txt

# 6. Type coverage
echo "📝 Analyzing type coverage..."
uv run mypy src --html-report $REPORT_DIR/types || true
TYPE_COV=$(grep -o "[0-9]\+%" $REPORT_DIR/types/index.html | head -1 || echo "0%")
echo "Type coverage: $TYPE_COV" >> $REPORT_DIR/summary.txt

# 7. Security issues
echo "🔒 Analyzing security..."
uv run bandit -r src -f json -o $REPORT_DIR/security.json || true
HIGH_SEC=$(python -c "import json; issues=[i for i in json.load(open('$REPORT_DIR/security.json'))['results'] if i['issue_severity']=='HIGH']; print(len(issues))" || echo "0")
echo "High severity security issues: $HIGH_SEC" >> $REPORT_DIR/summary.txt

# 8. Dependency health
echo "📦 Analyzing dependencies..."
uv run pip-audit --format json > $REPORT_DIR/vulnerabilities.json || true
VULN_COUNT=$(python -c "import json; print(len(json.load(open('$REPORT_DIR/vulnerabilities.json'))))" || echo "0")
echo "Dependency vulnerabilities: $VULN_COUNT" >> $REPORT_DIR/summary.txt

# 9. Generate summary report
cat > $REPORT_DIR/README.md <<EOF
# Codebase Health Report
Generated: $(date)

## Summary

\`\`\`
$(cat $REPORT_DIR/summary.txt)
\`\`\`

## Health Score

- ✅ **Excellent**: Coverage >80%, MI >70, Few complex functions
- ⚠️  **Good**: Coverage >60%, MI >50, Some refactoring needed
- ❌ **Needs Work**: Coverage <60%, MI <50, Many complex functions

**Current Status**: $(
    if (( $(echo "$COVERAGE > 80" | bc -l) )) && [ $COMPLEX_COUNT -lt 10 ]; then
        echo "✅ Excellent"
    elif (( $(echo "$COVERAGE > 60" | bc -l) )); then
        echo "⚠️  Good"
    else
        echo "❌ Needs Work"
    fi
)

## Recommendations

### High Priority (Do First)
- [ ] Fix $HIGH_SEC high-severity security issues
- [ ] Address $VULN_COUNT dependency vulnerabilities
- [ ] Improve test coverage (current: $COVERAGE%, target: 80%+)

### Medium Priority (Next Sprint)
- [ ] Refactor $COMPLEX_COUNT complex functions
- [ ] Remove dead code ($DEAD_CODE_COUNT potential issues)
- [ ] Improve type coverage (current: $TYPE_COV, target: 70%+)

### Low Priority (Long Term)
- [ ] Improve maintainability index (current: $MI_AVG, target: 70+)
- [ ] Add missing docstrings
- [ ] Modernize Python syntax

## Detailed Reports

- [Test Coverage]($REPORT_DIR/coverage/index.html)
- [Type Coverage]($REPORT_DIR/types/index.html)
- [Complex Functions]($REPORT_DIR/complex-functions.txt)
- [Dead Code]($REPORT_DIR/dead-code.txt)
- [Security Issues]($REPORT_DIR/security.json)
- [Dependency Vulnerabilities]($REPORT_DIR/vulnerabilities.json)

## Next Steps

1. Review this report with the team
2. Create GitHub issues for high-priority items
3. Schedule refactoring sprints
4. Set up pre-commit hooks to prevent regressions
5. Re-run this report monthly to track progress
EOF

echo "✅ Health report generated in $REPORT_DIR/"
echo "📄 View summary: cat $REPORT_DIR/README.md"
open $REPORT_DIR/README.md || xdg-open $REPORT_DIR/README.md || cat $REPORT_DIR/README.md
```

**Example output:**

```
📊 Codebase Health Report
Generated: 2025-01-15

Summary:
- Lines of code: 12,450
- Coverage: 67%
- Potential dead code: 34 issues
- Complex functions (C+): 12
- Maintainability Index: 58
- Type coverage: 45%
- High severity security issues: 2
- Dependency vulnerabilities: 3

Current Status: ⚠️  Good

Recommendations:
High Priority: Fix security issues, improve coverage
Medium Priority: Refactor complex functions, remove dead code
Low Priority: Improve maintainability, add types
```

---

## CI/CD Integration

### Scenario: Add quality checks to GitHub Actions

Create `.github/workflows/code-quality.yml`:

```yaml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Check formatting
        run: |
          uv run ruff format --check .
        continue-on-error: false

      - name: Lint
        run: |
          uv run ruff check . --output-format=github
        continue-on-error: false

      - name: Type check
        run: |
          uv run mypy src --junit-xml mypy-report.xml
        continue-on-error: true  # Warning only

      - name: Dead code check
        run: |
          uv run vulture src tests --min-confidence 80
        continue-on-error: true  # Warning only

      - name: Dependency check
        run: |
          uv run deptry .
        continue-on-error: true  # Warning only

      - name: Security scan
        run: |
          uv run bandit -r src --severity-level high --format json --output bandit-report.json
        continue-on-error: true

      - name: Vulnerability check
        run: |
          uv run pip-audit --format json --output audit-report.json
        continue-on-error: false  # BLOCKER

      - name: Run tests with coverage
        run: |
          uv run pytest --cov=src --cov-report=xml --cov-report=term-missing --cov-fail-under=75

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: quality-reports
          path: |
            mypy-report.xml
            bandit-report.json
            audit-report.json
            coverage.xml

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            // Read coverage
            const coverage = fs.readFileSync('coverage.xml', 'utf8');
            const coverageMatch = coverage.match(/line-rate="([0-9.]+)"/);
            const coveragePct = coverageMatch ? (parseFloat(coverageMatch[1]) * 100).toFixed(1) : 'N/A';

            // Create comment
            const comment = `## 📊 Code Quality Report

            **Coverage**: ${coveragePct}%
            **Target**: 75%+

            - ✅ Linting: Passed
            - ✅ Type checking: See artifacts
            - ✅ Security: No high-severity issues
            - ⚠️  Dead code: See artifacts

            View detailed reports in workflow artifacts.
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

This CI workflow:
- ✅ **Blocks** merges on: formatting, linting, vulnerabilities, low coverage
- ⚠️ **Warns** on: type errors, dead code, dependency issues
- 📊 **Reports**: coverage, security, complexity in PR comments

---

## Handling False Positives

### Example 1: Vulture False Positives

**Problem:** Vulture flags Pydantic fields as unused

```python
# src/models.py
from pydantic import BaseModel

class UserModel(BaseModel):
    username: str  # ← Vulture flags this as unused
    email: str     # ← Vulture flags this as unused
```

**Solution:** Create `vulture_whitelist.py`:

```python
# vulture_whitelist.py
# Whitelist for intentionally "unused" code

# Pydantic model fields (used by framework)
_.username
_.email
_.created_at
_.updated_at

# FastAPI dependencies (called by framework)
get_db
get_current_user

# Test fixtures (used by pytest)
db_session
mock_api_client

# Abstract methods (implemented by subclasses)
BaseClass.abstract_method
AgentTool.run

# Registered tools (used via ToolRegistry)
write_post
read_profile
search_media
```

Run with whitelist:
```bash
uv run vulture src tests vulture_whitelist.py --min-confidence 80
```

### Example 2: Autoflake Removing Needed Imports

**Problem:** Autoflake removes imports needed for side effects

```python
# src/app.py
import patches  # Sets up monkey patches - NEEDED!
from sqlalchemy import event  # Side effect: registers event handlers
```

**After autoflake:**
```python
# src/app.py
# Both imports removed! ❌
```

**Solution 1:** Use `noqa` comments:
```python
import patches  # noqa: F401
from sqlalchemy import event  # noqa: F401
```

**Solution 2:** Explicit exports:
```python
import patches
from sqlalchemy import event

__all__ = ['patches', 'event']  # Tells autoflake these are used
```

### Example 3: Coverage False Negatives

**Problem:** Some code shows as uncovered but is actually tested

```python
# src/utils.py
def parse_config(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:  # ← Shows as uncovered in coverage report
        logger.error(f"Config not found: {path}")
        raise
```

**Reason:** Test doesn't trigger `FileNotFoundError` path

**Solution:** Add test for error case:

```python
# tests/test_utils.py
def test_parse_config_not_found():
    with pytest.raises(FileNotFoundError):
        parse_config("/nonexistent/path")
```

**Alternative:** Exclude from coverage if intentionally untested:

```python
def parse_config(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:  # pragma: no cover
        # This path is tested in integration tests, not unit tests
        logger.error(f"Config not found: {path}")
        raise
```

---

## Project-Specific Examples

### Example: Egregora (This Project)

```bash
#!/bin/bash
# egregora-specific-cleanup.sh

echo "🧹 Egregora code cleanup"

# 1. Lint (respects 110 char line length in pyproject.toml)
uv run ruff check . --fix
uv run ruff format .

# 2. Type check (respects mypy config)
uv run mypy src/egregora

# 3. Dead code (with whitelist for agent tools)
cat > vulture_whitelist.py <<EOF
# Pydantic-AI agent tools (registered in ToolRegistry)
_.write_post
_.read_profile
_.write_profile
_.search_media
_.annotate_conversation
_.generate_banner

# Pydantic model fields
_.timestamp
_.author
_.message
_.message_id
_.original_line
_.tagged_line

# Pipeline stage functions (called dynamically)
_.parse_source
_.anonymize_conversation
_.enrich_urls
_.write_posts_with_pydantic_agent
EOF

uv run vulture src tests vulture_whitelist.py --min-confidence 80

# 4. Check dependencies
uv run deptry .

# 5. Coverage (high bar for pipeline stages)
uv run pytest --cov=egregora --cov-report=html --cov-fail-under=80

# 6. Security scan
uv run bandit -r src/egregora --severity-level medium --skip B101,B110

# 7. Complexity (pipeline stages should be simple)
uv run radon cc src/egregora -s -n B

echo "✅ Cleanup complete!"
```

**Egregora-specific notes:**
- Use `--cov=egregora` not `--cov=src` (package name)
- Skip bandit B101 (assert in tests) and B110 (try/except pass in optional features)
- High coverage bar for privacy/pipeline stages (critical data flow)
- Lower bar for agents (LLM behavior is non-deterministic)

---

## Summary

These examples show:
- ✅ **Setup**: First-time tool installation and baseline
- ✅ **Maintenance**: Weekly/monthly workflows
- ✅ **Pre-release**: Quality gates before shipping
- ✅ **Refactoring**: Deep clean after major changes
- ✅ **Assessment**: Understanding inherited codebases
- ✅ **CI/CD**: Automated quality checks
- ✅ **False positives**: Handling tool quirks
- ✅ **Project-specific**: Adapting to project needs

**Key takeaway:** Start simple, iterate, automate what works.

**Next steps:**
1. Pick one example that matches your needs
2. Adapt the script to your project
3. Run it and review results
4. Adjust thresholds and whitelists
5. Automate in CI/CD
6. Track progress over time

Happy cleaning! 🧹
