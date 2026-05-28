---
name: x07-test
description: Use this skill when you need to run tests for an X07 project using the built-in test harness and generate a machine-readable JSON report.
---

# Skill body

This skill provides the single canonical way to run tests for an X07 project using the built-in test harness.

## Canonical command

- `x07 test --manifest tests/tests.json`

## Notes

- By default, `x07 test` prints JSON to stdout; use `--report-out <path>` to write a report file.
- If your project pins stdlib via `stdlib.lock`, keep it in the project root or pass `--stdlib-lock <path>`.
- New projects created with `x07 init` include `tests/tests.json` plus a minimal `tests/smoke.x07.json`.
- Tests under `tests/` can import your project modules under `src/` (via project module-root discovery).
- World-gating is enforced at compile time: if a module calls fixture-world APIs (like `fs.*`) anywhere, it cannot be compiled in `solve-pure`. Keep pure tests and fixture tests in separate modules.

See also: https://x07lang.org/docs/toolchain/testing-by-example/