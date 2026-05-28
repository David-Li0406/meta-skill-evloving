---
name: fmt
description: Format code in the current project
user-invocable: true
argument-hint: [file-or-directory]
allowed-tools: Bash, Read, Glob
---

# Format Code

Detect the project type and format code appropriately.

## Detection and Commands

1. **Python** (`pyproject.toml` or `*.py` files):
   - `uv run ruff format $ARGUMENTS`
   - Fallback: `uv run black $ARGUMENTS`

2. **Rust** (`Cargo.toml`):
   - `cargo fmt $ARGUMENTS`

3. **Go** (`go.mod` or `*.go` files):
   - `go fmt ./...` or `gofmt -w $ARGUMENTS`

4. **Node.js/TypeScript** (`package.json`):
   - Check for prettier: `npx prettier --write $ARGUMENTS`
   - Check for format script: `npm run format`

5. **Mixed projects**:
   - Run all applicable formatters

## Target

- If $ARGUMENTS is empty: Format all files in project
- If $ARGUMENTS is provided: Format only specified file/directory
