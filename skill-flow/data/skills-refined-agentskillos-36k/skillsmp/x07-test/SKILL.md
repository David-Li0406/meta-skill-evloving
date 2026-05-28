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
- `x07 test` resolves `stdlib.lock` by searching upward from the manifest directory, then upward from the `x07` executable location. Override with `--stdlib-lock <path>`.
- New projects created with `x07 init` include `tests/tests.json` plus a minimal `tests/smoke.x07.json`.
- Tests under `tests/` can import your project modules under `src/` (via project module-root discovery).
- World-gating is enforced at compile time: if a module calls fixture-world APIs (like `fs.*`) anywhere, it cannot be compiled in `solve-pure`. Keep pure tests and fixture tests in separate modules.

See also: https://x07lang.org/docs/toolchain/testing-by-example/
