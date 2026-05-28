# Refactor Testing (Minimal, Necessary)

Use these guidelines to add just enough tests to refactor safely without overbuilding a full test suite.

## Goals

- Lock in current behavior before moving code.
- Keep tests small, fast, and focused on public behavior.
- Prefer stable seams (ports, handlers, use-case APIs) over internal details.

## What to Test

1) **Characterization tests at entrypoints**
- HTTP: handler or router-level tests with `httptest` for critical routes.
- gRPC: service method tests with a real server or handler-level calls.
- Worker/CLI: call the entry function with fake ports and assert outputs.

2) **Use-case behavior**
- Add 1-2 tests per critical use case to capture core rules.
- Focus on inputs/outputs and side effects through ports.

3) **Boundary contracts**
- For each outbound port, add a simple fake to assert calls and data.
- Avoid mocking internal structs or private helpers.

## How to Keep It Minimal

- Start with the smallest test that proves behavior; add more only if a refactor step breaks.
- Prefer table-driven tests with a short list of cases.
- Avoid deep fixtures; build only the data needed for the assertion.

## Execution During Refactor

- Before moving code, write the characterization test around the current behavior.
- After each refactor step, run only impacted tests.
- At the end, run full tests.

Commands:

```bash
# targeted packages
go test ./internal/... ./cmd/...

# full suite (if feasible)
go test ./...
```

## When to Remove or Keep Tests

- Keep tests that express stable behavior or business rules.
- Remove temporary tests only if they are redundant and do not add coverage.
