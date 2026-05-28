---
name: test
description: Run tests on the codebase.
---

# Test

Run test suite to verify functionality.

## Steps

1. Detect the project type and find the test command:
   - TypeScript/JavaScript: `npm test`, `vitest`, `jest`
   - Go: `go test ./...`
   - Rust: `cargo test`
   - Python: `pytest`, `python -m unittest`
   - General: `make test`

2. If no test framework is configured, propose adding one appropriate for the project.

3. Run the command and report results. Fix any failing tests.
