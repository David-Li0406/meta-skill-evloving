---
name: run
description: Run the current project based on detected language
user-invocable: true
argument-hint: [file-or-args]
allowed-tools: Bash, Read, Glob
---

# Run Project

Detect the project type and run it appropriately.

## Detection Order

1. Check for `pyproject.toml` or `uv.lock` -> Use `uv run`
2. Check for `Cargo.toml` -> Use `cargo run`
3. Check for `go.mod` -> Use `go run .`
4. Check for `package.json` -> Use `npm run` (check scripts)
5. If a specific file is provided as $ARGUMENTS, run that file directly

## Execution

- Python: `uv run python $ARGUMENTS` or `uv run .`
- Rust: `cargo run $ARGUMENTS`
- Go: `go run . $ARGUMENTS` or `go run $ARGUMENTS`
- Node.js: Check `package.json` scripts, default to `npm start` or `node $ARGUMENTS`

If $ARGUMENTS is empty, run the main entry point.
If $ARGUMENTS is provided, pass it as arguments or run that specific file.
