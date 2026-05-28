---
type: claude-context
directory: .claude/skills/quality-enforcer
purpose: Quality Enforcer provides **automated quality gate enforcement** for the workflow. It runs tests, checks coverage, validates linting, type checking, and builds before allowing PR creation. Enforces minimum 80% test coverage and all tests passing. Integrates with git-workflow-manager for semantic versioning.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
related_skills:
  - **workflow-orchestrator** - Calls quality-enforcer at Phase 3
  - **git-workflow-manager** - Semantic versioning after quality gates
  - **tech-stack-adapter** - Provides test/build commands
  - **speckit-author** - Quality gates validate spec implementation
---

# Claude Code Context: quality-enforcer

## Purpose

Quality Enforcer provides **automated quality gate enforcement** for the workflow. It runs tests, checks coverage, validates linting, type checking, and builds before allowing PR creation. Enforces minimum 80% test coverage and all tests passing. Integrates with git-workflow-manager for semantic versioning.

## Directory Structure

```
.claude/skills/quality-enforcer/
├── scripts/                      # Quality gate automation
│   ├── run_quality_gates.py      # Main orchestrator (Phase 3)
│   ├── check_coverage.py         # Coverage validation
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### run_quality_gates.py

**Purpose:** Run all quality gates and report results (tests, coverage, build, linting, type checking)

**When to use:** Phase 3 (Quality Gates) - after implementation complete, before creating PR

**Invocation:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**What it does:**
1. **Run tests:** `uv run pytest -v`
   - Validates all tests pass
   - Reports test failures if any

2. **Check coverage:** Calls `check_coverage.py` with 80% threshold
   - Validates test coverage ≥80%
   - Reports coverage percentage

3. **Check build:** `uv build`
   - Validates package builds successfully
   - Detects build configuration issues

4. **Check linting:** `uv run ruff check`
   - Validates code quality (no linting errors)
   - Reports violations if any

5. **Check type checking:** `uv run mypy src/`
   - Validates type annotations
   - Reports type errors if any

6. **Report results:** Prints summary of all gates
   - ✓ Pass: All gates passed
   - ✗ Fail: Shows which gates failed

**Output:**
```
Running quality gates...

Running tests...
✓ All tests passed

Checking coverage (≥80%)...
✓ Coverage: 88% (≥80% required)

Checking build...
✓ Build successful

Checking linting...
✓ Linting clean

Checking type checking...
✓ Type checking passed

========================================
Quality Gates: PASSED
========================================
All quality gates passed! Ready for PR.
```

**Key features:**
- Runs all quality gates in sequence
- Stops on first failure (fail-fast)
- Comprehensive reporting
- Exit code 0 (success) or 1 (failure)

---

### check_coverage.py

**Purpose:** Check test coverage meets minimum threshold

**When to use:** Called by run_quality_gates.py, or standalone coverage check

**Invocation:**
```bash
python .claude/skills/quality-enforcer/scripts/check_coverage.py [threshold]
```

**Example:**
```bash
# Check 80% threshold (default)
python .claude/skills/quality-enforcer/scripts/check_coverage.py 80

# Output: ✓ Coverage: 88% (≥80% required)
```

**What it does:**
1. Runs pytest with coverage: `uv run pytest --cov=src --cov-report=term`
2. Parses coverage percentage from output
3. Compares to threshold (default: 80%)
4. Reports pass/fail

**Key features:**
- Configurable threshold (default: 80%)
- Extracts percentage from pytest-cov output
- Clear pass/fail reporting
- Exit code indicates success/failure

---

## Usage by Claude Code

### Phase 3: Quality Gates

**Context:** Implementation complete, need to validate quality before PR

**User says:**
- "Run quality gates"
- "Check if ready for PR"
- "Run tests and coverage"
- "Validate quality"

**Claude Code should:**
```python
import subprocess

# Call run_quality_gates.py
result = subprocess.run([
    'python',
    '.claude/skills/quality-enforcer/scripts/run_quality_gates.py'
], capture_output=True, text=True)

if result.returncode == 0:
    # All gates passed
    print("✓ Quality gates passed. Ready for PR.")
    # Proceed to semantic versioning and PR creation
else:
    # Some gates failed
    print("✗ Quality gates failed:")
    print(result.stdout)
    print(result.stderr)
    # DO NOT create PR - fix issues first
```

---

### Standalone Coverage Check

**Context:** User wants to check coverage without running all gates

**User says:**
- "Check coverage"
- "What's my test coverage?"
- "Do I meet 80%?"

**Claude Code should:**
```python
import subprocess

# Call check_coverage.py
result = subprocess.run([
    'python',
    '.claude/skills/quality-enforcer/scripts/check_coverage.py',
    '80'  # threshold
], capture_output=True, text=True, check=False)

print(result.stdout)

if result.returncode == 0:
    print("✓ Coverage requirement met")
else:
    print("✗ Coverage below threshold")
```

---

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls run_quality_gates.py at Phase 3
- Blocks PR creation if gates fail
- Proceeds to semantic versioning if gates pass

**git-workflow-manager:**
- Quality gates must pass before semantic_version.py runs
- Version calculation happens after quality validation

**speckit-author:**
- Quality gates validate implementation matches spec
- Coverage requirement ensures all spec'd functionality is tested

**tech-stack-adapter:**
- Quality enforcer uses commands from tech-stack detection
- Adapts to project's test/build/lint commands

---

## Quality Gate Requirements

**Minimum requirements (enforced before PR):**

1. **Tests:** All tests must pass
   - Command: `uv run pytest -v`
   - Zero failures allowed

2. **Coverage:** ≥80% test coverage
   - Command: `uv run pytest --cov=src --cov-fail-under=80`
   - Measures code coverage in src/ directory

3. **Build:** Package must build successfully
   - Command: `uv build`
   - Validates pyproject.toml and package structure

4. **Linting:** No linting errors
   - Command: `uv run ruff check src/ tests/`
   - Enforces code quality standards

5. **Type Checking:** No type errors (if mypy configured)
   - Command: `uv run mypy src/`
   - Validates type annotations

**Rationale:**
- **80% coverage threshold:** Balance between quality and pragmatism. Allows edge cases to be untested while ensuring core functionality is covered.
- **All tests pass:** Zero tolerance for known failures. Broken tests indicate broken code.
- **Build validates:** Catches configuration issues early (missing dependencies, bad imports)
- **Linting enforces:** Consistent code style, catches common errors
- **Type checking prevents:** Type-related bugs, improves IDE support

---

## Constants and Rationale

**COVERAGE_THRESHOLD:** 80%
- **Rationale:** Industry standard minimum. Balances thorough testing with development velocity. Projects may exceed but not go below.

**Quality gate order:** Tests → Coverage → Build → Lint → Types
- **Rationale:** Fail-fast on most critical issues first. No point checking coverage if tests don't pass.

**Exit codes:** 0 (success), 1 (failure)
- **Rationale:** Shell convention. Allows workflow scripts to check `if run_quality_gates.py fails then abort`

---

## Error Handling

**Test failures:**
```
✗ Some tests failed
tests/test_models.py::test_noun_validation FAILED
Fix failing tests before creating PR.
```

**Coverage below threshold:**
```
✗ Coverage: 72% (≥80% required)
Add tests to increase coverage before PR.
```

**Build failures:**
```
✗ Build failed
ModuleNotFoundError: No module named 'pydantic'
Add missing dependency to pyproject.toml
```

**Linting errors:**
```
✗ Linting failed
src/models.py:42:1: F401 'typing.Optional' imported but unused
Fix linting issues with: uv run ruff check --fix
```

**Type errors:**
```
✗ Type checking failed
src/models.py:42: error: Incompatible return value type
Fix type annotations before PR.
```

---

## Workflow Integration Pattern

**Phase 3 sequence:**
```python
# 1. Implementation complete in feature worktree
cd ../german_feature_auth-system

# 2. Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# 3. If passed, calculate semantic version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# 4. Update TODO file with quality_gates section:
#    quality_gates:
#      test_coverage: 88
#      tests_passing: true
#      semantic_version: "1.6.0"

# 5. Create PR with version in title
gh pr create --title "feat: auth system (v1.6.0)" ...
```

**If quality gates fail:**
```
✗ Quality gates failed
DO NOT create PR - fix issues first:
1. Fix failing tests
2. Add tests to increase coverage
3. Fix linting errors
4. Fix type errors
```

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[WORKFLOW.md](../../WORKFLOW.md)** - Complete workflow guide (Phase 3)

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Calls quality-enforcer at Phase 3
- **git-workflow-manager** - Semantic versioning after quality gates
- **tech-stack-adapter** - Provides test/build commands
- **speckit-author** - Quality gates validate spec implementation
