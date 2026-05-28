---
name: quality
description: Quality skill for the ikigai project
---

# Quality

## Description
Testing and quality requirements for development phase. Focus on high coverage.

## Pre-Commit Requirements

Before creating commits:

1. `make fmt` - Format code
2. `make check` - All tests pass
3. `make lint` - Complexity/file size checks pass

## Test Execution

**By Default**: Tests run in parallel, with 24 parallel tests on this machine.
- `MAKE_JOBS=24` - up to 24 concurrent tests

**When you need clear debug output** (serialize execution):
```bash
PARALLEL=0 MAKE_JOBS=1 make check
```

**Best practice**: Test individual files during development, run full suite before commits.

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

## Development Phase Focus

- Aim for high test coverage of new code
- Test the happy path and obvious error cases
- Coverage gaps will be closed in a dedicated coverage phase
- Don't let coverage metrics slow down feature development

**CRITICAL**: Never run multiple `make` commands simultaneously. Different targets use incompatible compiler flags and will corrupt the build.
