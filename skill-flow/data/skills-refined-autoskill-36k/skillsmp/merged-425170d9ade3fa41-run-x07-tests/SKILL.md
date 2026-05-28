---
name: run-x07-tests
description: Use this skill to run project tests using the X07 test harness, producing a machine-readable JSON report.
---

# Run X07 Tests

This skill provides the canonical way to run tests for an X07 project using the built-in test harness.

## Canonical Command

- `x07 test --manifest <path_to_tests_json>`

## Notes

- By default, `x07 test` prints JSON to stdout; use `--report-out <path>` to write a report file.
- If your project pins stdlib via `stdlib.lock`, keep it in the project root or pass `--stdlib-lock <path>`.
- New projects created with `x07 init` include a default `tests/tests.json` and a minimal `tests/smoke.x07.json`.
- Tests under `tests/` can import your project modules under `src/` via project module-root discovery.
- World-gating is enforced at compile time: if a module calls fixture-world APIs (like `fs.*`) anywhere, it cannot be compiled in `solve-pure`. Keep pure tests and fixture tests in separate modules.

See also: [X07 Testing Documentation](https://x07lang.org/docs/toolchain/testing-by-example/)