---
name: quality-assurance
description: Use this skill for ensuring strict quality and testing standards during the development phase of the ikigai project.
---

# Quality Assurance

## Description
This skill outlines the testing and quality requirements for the ikigai project, focusing on both development and coverage phases to ensure high standards.

## Pre-Commit Requirements

Before creating any commits, the following checks must be completed:

1. `make fmt` - Format code
2. `make check` - All tests must pass (100% for strict quality)
3. `make lint` - Complexity and file size checks must pass
4. `make check-coverage` - Coverage metrics (lines, functions, branches) must meet the required threshold (90% for strict quality)
5. `make check-dynamic` - All sanitizer checks must pass (ASan, UBSan, TSan)

If any check fails, fix all issues and re-run all checks until everything passes. Never commit with any known issues.

## Test Execution

**By Default**: Tests run in parallel, with up to 24 concurrent tests on this machine.
- `MAKE_JOBS=24` - Set the number of concurrent tests
- `PARALLEL=1` - Run all check-dynamic subtargets in parallel

**For clear debug output** (serialize execution):
```bash
PARALLEL=0 MAKE_JOBS=1 make check
```

**Best practice**: Test individual files during development and run the full suite before commits.

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
- Use `make lint && make check-coverage` before commits - **90% coverage is mandatory for strict quality**.
- **CRITICAL**: Never run multiple `make` commands simultaneously, as different targets use incompatible compiler flags and may corrupt the build.

## Development and Coverage Phase Mindset

- Aim for high test coverage of new code, focusing on both happy paths and obvious error cases.
- Every uncovered line is a potential bug, and every untested branch is a failure mode that hasn't been verified.
- Coverage gaps should be addressed in a dedicated coverage phase, and LCOV exclusions are a last resort.
- Maintain zero tolerance for coverage gaps to ensure robust code quality.