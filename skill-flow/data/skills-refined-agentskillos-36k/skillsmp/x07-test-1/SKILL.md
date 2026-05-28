---
name: x07-test
description: Run project tests using the X07 test harness (x07 test), producing a machine-readable JSON report.
metadata:
  short-description: Run x07 tests
  version: 0.1.0
  kind: docs
---

# x07-test

This skill provides the single canonical way to run tests for an X07 project using the built-in test harness.

## Canonical command

- `x07 test --manifest tests/tests.json`

## Notes

- By default, `x07 test` prints JSON to stdout; use `--report-out <path>` to write a report file.
- If your project pins stdlib via `stdlib.lock`, keep it in the project root or pass `--stdlib-lock <path>`.
