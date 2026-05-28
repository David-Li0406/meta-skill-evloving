---
name: tdd-enforce
description: Use when strict test-first discipline is explicitly requested or required for a change.
allowed-tools: ["shell", "read_file", "apply_patch", "update_plan"]
metadata:
  short-description: Strict TDD (opt-in)
---

# Test-Driven Development (Strict)

**Read these references:**
- `~/.config/agent/domain/testing/unit.md` - Unit testing strategy
- `~/.config/agent/domain/testing/coverage.md` - Coverage expectations

## Overview

This is strict TDD. It is **opt-in**: use only when explicitly requested. Default guidance elsewhere is to **encourage** TDD, not require it.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If code was written before the failing test, delete it and start over.

## Red-Green-Refactor

1. **RED**: Write a failing test
2. **Verify RED**: Run test, confirm it fails for the right reason
3. **GREEN**: Minimal code to pass
4. **Verify GREEN**: Run tests, confirm pass
5. **REFACTOR**: Clean up while keeping tests green

## Key Rules

- One behavior per test
- Tests must fail before implementation
- Minimal implementation first
- Refactor only after green

## When Not to Use

- Throwaway prototypes
- Generated code
- Configuration-only changes

If tests fail unexpectedly or behavior is unclear, switch to `systematic-debugging`.

## Testing Anti-Patterns

Read `testing-anti-patterns.md` before adding mocks or test utilities.

## Arguments

Target: ${ARGUMENTS}
