---
name: test-stress-tester
description: Skill for hunting flaky tests and race conditions by running specific tests multiple times.
---

# Test Stress Tester

This skill provides a programmatic way to run tests repeatedly to catch flakiness, race conditions, or intermittent failures that only surface in CI.

## When to use
- When a test passes locally but fails in CI.
- When you suspect a race condition in asynchronous code.
- When you want to verify the stability of a new feature before merging.

## Scripts

### `run-repeatedly`
Runs a vitest test file a specified number of times and reports the failure rate.

**Command**:
```bash
./.agent/skills/test-stress-tester/scripts/run-repeatedly.sh <test-file> <iterations>
```

**Parameters**:
- `<test-file>`: Path to the vitest test file.
- `<iterations>`: Number of times to run the test (default: 5).

## Examples

### Stress testing a component
```bash
./.agent/skills/test-stress-tester/scripts/run-repeatedly.sh src/components/AdDetail.test.tsx 10
```

## Tips
- Keep iterations reasonable (5-10) for UI tests.
- For backend/logic tests, you can go higher (50+).
- Check the `stress-test.log` in the skill folder for detailed failure logs if any.
