---
type: directory-documentation
directory: .claude/skills/quality-enforcer
title: Quality Enforcer
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Quality Enforcer

> **Automated quality gate enforcement before PRs - ensuring code quality and test coverage standards**

The Quality Enforcer provides automated quality gate validation for the workflow. It runs comprehensive checks (tests, coverage, linting, type checking, builds) and enforces minimum standards before allowing PR creation. Integrates with git-workflow-manager for automatic semantic versioning.

## Features

- ✅ **Comprehensive quality gates** - Tests, coverage, linting, type checking, builds
- ✅ **80% coverage requirement** - Industry standard minimum enforced automatically
- ✅ **Fail-fast execution** - Stops on first failure for quick feedback
- ✅ **Semantic version integration** - Calculates version from code changes
- ✅ **TODO file updates** - Tracks quality metrics in workflow manifest
- ✅ **Clear reporting** - Detailed pass/fail messages with actionable fixes
- ✅ **Tech-stack adaptive** - Uses commands from tech-stack-adapter detection

## Quick Start

### Prerequisites

```bash
# Ensure dependencies installed
uv sync

# Verify test framework available
uv run pytest --version

# Verify coverage tool available
uv run pytest --cov --version
```

### Run All Quality Gates

```bash
# From feature worktree (after implementation complete)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Output (if all passed):
# Running quality gates...
#
# Running tests...
# ✓ All tests passed
#
# Checking coverage (≥80%)...
# ✓ Coverage: 88% (≥80% required)
#
# Checking build...
# ✓ Build successful
#
# Checking linting...
# ✓ Linting clean
#
# Checking type checking...
# ✓ Type checking passed
#
# ========================================
# Quality Gates: PASSED
# ========================================
# All quality gates passed! Ready for PR.
```

### Check Coverage Only

```bash
# Check if coverage meets 80% threshold
python .claude/skills/quality-enforcer/scripts/check_coverage.py 80

# Output:
# ✓ Coverage: 88% (≥80% required)
```

## Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `run_quality_gates.py` | Run all quality gates (tests, coverage, build, lint, types) | Phase 3 (before creating PR) |
| `check_coverage.py` | Validate test coverage meets threshold | Standalone coverage check |

## Quality Gates

### 1. Tests (Required)

**Command:** `uv run pytest -v`

**Requirement:** All tests must pass (zero failures)

**Rationale:** Broken tests indicate broken code. Zero tolerance for known failures.

**Example failure:**
```
✗ Some tests failed
tests/test_models.py::test_noun_validation FAILED
Fix failing tests before creating PR.
```

### 2. Coverage (Required)

**Command:** `uv run pytest --cov=src --cov-fail-under=80`

**Requirement:** ≥80% test coverage

**Rationale:** Industry standard minimum. Balances thorough testing with development velocity. Projects may exceed but not go below.

**Example failure:**
```
✗ Coverage: 72% (≥80% required)
Add tests to increase coverage before PR.
```

### 3. Build (Required)

**Command:** `uv build`

**Requirement:** Package must build successfully

**Rationale:** Catches configuration issues early (missing dependencies, bad imports, packaging errors).

**Example failure:**
```
✗ Build failed
ModuleNotFoundError: No module named 'pydantic'
Add missing dependency to pyproject.toml
```

### 4. Linting (Required)

**Command:** `uv run ruff check src/ tests/`

**Requirement:** No linting errors

**Rationale:** Enforces consistent code style, catches common errors.

**Example failure:**
```
✗ Linting failed
src/models.py:42:1: F401 'typing.Optional' imported but unused
Fix linting issues with: uv run ruff check --fix
```

### 5. Type Checking (Required if mypy configured)

**Command:** `uv run mypy src/`

**Requirement:** No type errors

**Rationale:** Validates type annotations, improves IDE support, prevents type-related bugs.

**Example failure:**
```
✗ Type checking failed
src/models.py:42: error: Incompatible return value type
Fix type annotations before PR.
```

## Workflow Integration

### Phase 3: Quality Gates

```bash
# After implementation complete in feature worktree
cd ../german_feature_auth-system

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# If passed, calculate semantic version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.6.0

# Update TODO file with quality metrics
# (automatically done by run_quality_gates.py)

# Create PR with version in title
gh pr create --title "feat: auth system (v1.6.0)" \
  --body "PR description" \
  --base contrib/stharrold
```

### Integration with Semantic Versioning

Quality gates output is merged with semantic version in TODO file:

```yaml
quality_gates:
  test_coverage: 88
  tests_passing: true
  semantic_version: "1.6.0"
```

**Benefits:**
- No manual version calculation
- Version correlates with actual changes + test quality
- Quality gates enforced before PR creation

## Examples

### All Gates Pass

```bash
$ python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

Running quality gates...

Running tests...
collected 42 items

tests/test_models.py ............... [ 38%]
tests/test_vocabulary.py ........... [ 76%]
tests/test_loader.py .............. [100%]

42 passed in 1.25s
✓ All tests passed

Checking coverage (≥80%)...
Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py             2      0   100%
src/models.py              45      3    93%
src/vocabulary/loader.py   32      2    94%
src/vocabulary/query.py    28      4    86%
-------------------------------------------
TOTAL                     107     9    92%
✓ Coverage: 92% (≥80% required)

Checking build...
Successfully built german-1.5.0.tar.gz and german-1.5.0-py3-none-any.whl
✓ Build successful

Checking linting...
All checks passed!
✓ Linting clean

Checking type checking...
Success: no issues found in 4 source files
✓ Type checking passed

========================================
Quality Gates: PASSED
========================================
All quality gates passed! Ready for PR.

Exit code: 0
```

### Coverage Below Threshold

```bash
$ python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

Running quality gates...

Running tests...
✓ All tests passed

Checking coverage (≥80%)...
Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py             2      0   100%
src/models.py              45     12    73%
src/vocabulary/loader.py   32      8    75%
src/vocabulary/query.py    28      7    75%
-------------------------------------------
TOTAL                     107     27    75%
✗ Coverage: 75% (≥80% required)
Add tests to increase coverage before PR.

Exit code: 1  (FAILED)
```

### Test Failures

```bash
$ python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

Running quality gates...

Running tests...
tests/test_models.py::test_noun_requires_gender FAILED

============================= FAILURES ==============================
______________________ test_noun_requires_gender ____________________

    def test_noun_requires_gender():
        with pytest.raises(ValidationError):
>           VocabularyWord(german="Haus", english="house", part_of_speech="noun")
E       Failed: DID NOT RAISE <class 'pydantic_core._pydantic_core.ValidationError'>

tests/test_models.py:42: Failed
======================== short test summary info ====================
FAILED tests/test_models.py::test_noun_requires_gender - Failed: ...
1 failed, 41 passed in 1.35s

✗ Some tests failed
tests/test_models.py::test_noun_requires_gender FAILED
Fix failing tests before creating PR.

Exit code: 1  (FAILED)
```

## Gate Execution Order

Quality gates run in this order (fail-fast):

1. **Tests** → Most critical (broken tests = broken code)
2. **Coverage** → No point checking if tests don't pass
3. **Build** → Validate packaging before style checks
4. **Linting** → Code quality standards
5. **Type checking** → Type annotation validation

**Rationale:** Fail-fast on most critical issues first. Saves time by not running all checks if tests fail.

## Adapting to Project Stack

Quality enforcer uses commands from tech-stack-adapter:

```bash
# Phase 0: Detect stack
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py

# Output:
# {
#   "test_cmd": "uv run pytest",
#   "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
#   "lint_cmd": "uv run ruff check",
#   "type_check_cmd": "uv run mypy src/",
#   "build_cmd": "uv build"
# }

# Phase 3: Quality gates use detected commands
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
# (uses commands from tech-stack detection)
```

## Troubleshooting

### Missing Test Framework

```bash
✗ Error: pytest not found

Fix: Add pytest to dev dependencies
  uv add --dev pytest pytest-cov
  uv sync
```

### Missing Coverage Tool

```bash
✗ Error: Coverage tool not configured

Fix: Install pytest-cov
  uv add --dev pytest-cov
  uv sync
```

### Coverage Below Threshold (What to Do)

**Option 1: Add tests** (recommended)
```bash
# Identify untested code
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Add tests for highlighted code
# Re-run quality gates
```

**Option 2: Lower threshold** (not recommended)
```bash
# Edit check_coverage.py threshold (discouraged)
# 80% is industry standard - don't lower without good reason
```

### Linting Errors

**Auto-fix most issues:**
```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Re-run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

### Type Errors

**Common fixes:**
```bash
# Add type annotations
def process_word(word: str) -> VocabularyWord:
    ...

# Use Optional for nullable values
from typing import Optional
gender: Optional[Gender] = None

# Re-run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

## Constants and Rationale

| Constant | Value | Rationale |
|----------|-------|-----------|
| COVERAGE_THRESHOLD | 80% | Industry standard minimum, balances quality with velocity |
| Gate execution order | Tests → Coverage → Build → Lint → Types | Fail-fast on most critical issues |
| Exit codes | 0 (success), 1 (failure) | Shell convention, allows workflow scripts to check success |

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete technical documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**See also:**
- [WORKFLOW.md](../../WORKFLOW.md) - Complete workflow guide (Phase 3)
- [git-workflow-manager](../git-workflow-manager/) - Semantic versioning
- [tech-stack-adapter](../tech-stack-adapter/) - Project detection

## Contributing

This skill is part of the workflow system. To update:

1. Modify scripts in `scripts/`
2. Update version in `SKILL.md` frontmatter
3. Document changes in `CHANGELOG.md`
4. Run validation: `python .claude/skills/workflow-utilities/scripts/validate_versions.py`
5. Sync documentation: `python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py quality-enforcer <version>`

## License

Part of the german repository workflow system.
