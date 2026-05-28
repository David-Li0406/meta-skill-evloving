---
name: quality-assurance
description: Use this skill to ensure strict quality and testing standards are met before committing code changes.
---

# Quality Assurance

## Description
This skill outlines the strict testing, coverage, and quality requirements necessary for maintaining high standards in the development process.

## Pre-Commit Requirements

Before creating any commit (mandatory, no exceptions):

1. `make fmt` - Format code
2. `make check` - All tests must pass (100%)
3. `make lint` - All complexity/file size checks must pass
4. `make check-coverage` - All metrics (lines, functions, branches) must meet a minimum of 90% coverage
5. `make check-dynamic` - All sanitizer checks must pass (ASan, UBSan, TSan)

If any check fails, fix all issues, re-run all checks, and repeat until everything passes. Never commit with any known issues, even if they are "pre-existing" or "in another file".

## Test Execution

**By Default**: Tests run in parallel, with up to 24 concurrent tests on this machine.
- `MAKE_JOBS=24` - up to 24 concurrent tests
- `PARALLEL=1` - all check-dynamic subtargets run in parallel

**When you need clear debug output** (serialize execution):
```bash
PARALLEL=0 MAKE_JOBS=1 make check
```

**Best practice**: Test individual files during development, and run the full suite before commits.

Example:
```bash
make build/tests/unit/array/basic_test && ./build/tests/unit/array/basic_test
```

## Build Modes

```bash
make BUILD={debug|release|sanitize|tsan|coverage}
```

- `debug` - Development builds with symbols
- `release` - Optimized production builds
- `sanitize` - Address and undefined behavior sanitizers
- `tsan` - Thread sanitizer
- `coverage` - Code coverage analysis

## Quality Gates

- Use `make check` to verify tests while working on code changes.
- Use `make lint && make check-coverage` before commits - **90% coverage is mandatory**.
- **CRITICAL**: Never run multiple `make` commands simultaneously. Different targets use incompatible compiler flags and will corrupt the build.

## Coverage Phase Mindset

- Every uncovered line is a bug waiting to happen.
- Every untested branch is a failure mode you haven't verified.
- LCOV exclusions are a last resort, not a shortcut.
- Zero tolerance for coverage gaps.