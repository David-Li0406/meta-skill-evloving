---
name: test
description: Run tests for the current project
user-invocable: true
argument-hint: [test-pattern]
allowed-tools: Bash, Read, Glob
---

# Run Tests

Detect the project type and run tests appropriately.

## Detection and Commands

1. **Python** (`pyproject.toml` or `uv.lock`):
   - `uv run pytest $ARGUMENTS`
   - With coverage: `uv run pytest --cov $ARGUMENTS`

2. **Rust** (`Cargo.toml`):
   - `cargo test $ARGUMENTS`

3. **Go** (`go.mod`):
   - `go test ./... $ARGUMENTS`
   - With verbose: `go test -v ./... $ARGUMENTS`

4. **Node.js** (`package.json`):
   - Check for `test` script: `npm test $ARGUMENTS`
   - Or use detected test runner (jest, vitest, etc.)

## Options

If $ARGUMENTS contains:
- `-v` or `--verbose`: Run with verbose output
- `-c` or `--coverage`: Run with coverage (if supported)
- Other args: Pass directly to the test command
