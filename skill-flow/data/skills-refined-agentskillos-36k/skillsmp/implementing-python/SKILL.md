---
name: implementing-python
description: Implements concise, streamlined Python code matching exact architect specifications. Use when writing Python code, creating modules, or when the user asks to implement features in Python.
---

# Python Implementation

Creates **focused, streamlined** Python implementations following architect
specifications exactly. No over-engineering.

## Python Standards

See `docs/python-best-practices.md` for comprehensive Python guidelines.

## Workflow

1. **Read architect specifications** from provided documents
2. **Validate scope** - Simple (100-200 lines) vs Complex (500+ lines)
3. **Study existing patterns** in `src/` structure
4. **Implement minimal solution** matching stated functionality
5. **Run `make validate_quick`** after writing code - fix formatting/type errors immediately
6. **Create focused tests** matching task complexity
7. **Run `make validate`** for full validation - fix all remaining issues

## Implementation Strategy

**Simple Tasks**: Minimal functions, basic error handling, lightweight
dependencies, focused tests

**Complex Tasks**: Class-based architecture, comprehensive validation,
necessary dependencies, full test coverage

**Always**: Use existing project patterns, pass `make validate`

## Output Standards

**Simple Tasks**: Minimal Python functions with basic type hints
**Complex Tasks**: Complete modules with comprehensive testing
**All outputs**: Concise, streamlined, no unnecessary complexity

## Quality Checks

**During development** (after writing code):

```bash
make validate_quick  # Fast check: formatting + types + tests
```

**Before completing** any task:

```bash
make validate  # Full check: formatting + types + tests
```

**CRITICAL**: Run validation commands proactively during development. Fix issues immediately, don't wait until the end. All type checks, linting, and tests must pass before task completion.
