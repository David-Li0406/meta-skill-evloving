---
name: ci
description: Run the full CI pipeline (format, lint, typecheck, test, validate-docs)
allowed-tools: Bash(poetry:*), Bash(make:*), Bash(direnv exec:*), Bash(git:*), Read, Grep, Glob, Edit, Write
user-invocable: true
---

# CI Pipeline Skill

This skill runs the full CI pipeline with detailed feedback, auto-fixing lint issues, and reviewing test coverage.

## Arguments

- `--eval` - Include `make test-eval` (runs Claude tool call evaluation tests, takes a long time)
- `--skip-docs` - Skip documentation validation
- `--coverage-only` - Only run test coverage analysis

## Pipeline Steps

Execute each step in order. Stop on failure unless the step is auto-fixable.

### Step 1: Install Dependencies

```bash
poetry install
```

Verify the virtual environment is set up correctly.

### Step 2: Format Code

```bash
poetry run ruff format src/ tests/
```

This auto-formats all code. Report what files were changed (if any).

### Step 3: Lint with Auto-Fix

```bash
poetry run ruff check --fix src/ tests/
```

If there are fixable issues, they will be auto-fixed. After auto-fix, run again without `--fix` to see remaining issues:

```bash
poetry run ruff check src/ tests/
```

If there are remaining unfixable issues, report them and stop.

### Step 4: Type Checking

```bash
poetry run mypy --warn-unreachable --warn-redundant-casts --warn-unused-ignores src/
```

Report any type errors. Stop if there are errors.

### Step 5: Run Unit Tests with Coverage

```bash
poetry run pytest tests/unit/ -v --cov=honeycomb --cov-report=term-missing --cov-branch
```

After tests complete:

1. **Check overall coverage percentage** - current baseline is ~38% (CLI and integration code is tested via live tests)
2. **Identify uncovered lines** - focus on models and validation code (should be 80%+)
3. **Check for new functionality without tests**:
   - Use `git diff --name-only HEAD~5` to find recently changed files
   - Cross-reference with coverage report
   - Flag any new code in `src/honeycomb/models/` or `src/honeycomb/validation/` without 80%+ coverage

**Coverage expectations by module:**
- `models/` and `validation/`: Should be 80%+ (unit testable)
- `resources/`: 30-50% typical (integration-heavy, tested via live tests)
- `cli/`: Low coverage expected (tested manually)
- `tools/executor.py`: 40-50% (tested via eval tests)

### Step 6: Validate Documentation (requires direnv)

```bash
direnv exec . poetry run python scripts/validate_docs_examples.py
direnv exec . poetry run pytest tests/integration/test_doc_examples.py -v
```

**Important:** This step requires environment variables from `.envrc`. If direnv is not configured, skip with a warning.

After validation:
1. **Check for docs-code mismatch**:
   - Use `git diff --name-only HEAD~5` to find changed source files
   - Check if corresponding docs in `docs/usage/` were updated
   - Flag functionality changes without docs updates

### Step 7: (Optional) Claude Tool Evaluation Tests

Only run if `--eval` argument is provided:

```bash
rm -rf tests/integration/.tool_call_cache/*.json
direnv exec . poetry run pytest tests/integration/test_claude_tools_eval.py -v -n 4
```

**Warning:** This step takes a long time (5-10 minutes) and requires `ANTHROPIC_API_KEY`.

## Post-Pipeline Analysis

After all steps complete, provide a summary:

### Coverage Analysis

1. **Overall coverage**: Report the percentage
2. **Coverage gaps**: List top 5 files with lowest coverage
3. **New code coverage**: For files changed in recent commits, report their coverage

### Documentation Sync Check

Compare changed files with docs:

```bash
# Get changed source files
git diff --name-only HEAD~5 -- 'src/honeycomb/*.py' 'src/honeycomb/**/*.py'

# Get changed doc files
git diff --name-only HEAD~5 -- 'docs/**/*.md'
```

Flag any source files in `resources/`, `models/`, or `builders/` that changed without corresponding doc updates.

### Test Coverage for New Features

For each new or significantly changed file:
1. Check if it has test coverage
2. If coverage < 70%, flag it
3. Suggest what tests might be needed

## Example Output Format

```
CI Pipeline Results
==================

Step 1: Install Dependencies ✓
Step 2: Format Code ✓ (2 files reformatted)
Step 3: Lint ✓ (3 issues auto-fixed)
Step 4: Type Check ✓
Step 5: Unit Tests ✓ (831 passed, 38% overall coverage)
Step 6: Documentation ✓
Step 7: Eval Tests ✓ (320 passed) [if --eval]

Coverage Analysis
-----------------
Overall: 38% (baseline for this project)

Models/Validation (target 80%+):
  ✓ src/honeycomb/models/tool_inputs.py: 99%
  ✓ src/honeycomb/models/tags_mixin.py: 100%
  ✓ src/honeycomb/validation/boards.py: 90%

Resources (30-50% expected):
  - src/honeycomb/resources/markers.py: 24%
  - src/honeycomb/resources/columns.py: 27%

Documentation Sync
------------------
Changed source files without doc updates:
  - src/honeycomb/resources/triggers.py (modified)
    Consider updating: docs/usage/triggers.md

New Code Without Tests
----------------------
  - src/honeycomb/models/new_feature.py: New file, 45% coverage
    Missing tests for: validate_feature(), get_feature()
```

## Failure Handling

- **Lint failures (unfixable)**: Stop and report. User must fix manually.
- **Type errors**: Stop and report. User must fix.
- **Test failures**: Stop and report failed tests with tracebacks.
- **Doc validation failures**: Report but continue if `--skip-docs` not set.

## Quick Commands

```bash
# Full CI (default)
/ci

# CI with eval tests (for tool call changes)
/ci --eval

# Skip docs validation
/ci --skip-docs

# Just coverage analysis
/ci --coverage-only
```
