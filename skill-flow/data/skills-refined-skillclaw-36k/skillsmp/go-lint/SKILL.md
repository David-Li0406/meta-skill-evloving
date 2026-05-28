---
name: go-lint
description: Lint and format Go code via golangci-lint. Use when asked to lint code, fix lint errors, or check code quality.
allowed-tools: ["shell"]
metadata:
  short-description: Lint Go code with golangci-lint
---

# Go Linter

**Reference:** `~/.config/agent/domain/coding/go/tooling.md` for Go linting details

## Instructions

Lint Go code using golangci-lint per AGENT.md guidelines:

### Standard Lint (with auto-fix)

```bash
golangci-lint run --new-false --fix ${ARGUMENTS}
```

Default to `./...` if no package path is provided.

### Lint Only (no fixes)

If user wants to see issues without applying fixes:
```bash
golangci-lint run --new-false ${ARGUMENTS}
```

### Lint Flags

- `--new-false`: Deprecated syntax for `--new=false` (show all issues)
- `--fix`: Automatically fix issues where possible
- Path defaults to `./...` (all packages)

### Common Usage

```bash
# Lint and fix all packages
golangci-lint run --new-false --fix ./...

# Lint specific package
golangci-lint run --new-false --fix ./path/to/package

# Check without fixing
golangci-lint run --new-false ./...
```

## Arguments

Target package(s): ${ARGUMENTS:-./...}
