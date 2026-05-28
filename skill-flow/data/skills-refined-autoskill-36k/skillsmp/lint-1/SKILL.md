---
name: lint
description: Run linting for Lua and TCL code
user-invocable: true
allowed-tools: Bash, Read
---

Run linting tools on the codebase.

## Usage

`/lint` - Run all linters
`/lint lua` - Run only Lua linter
`/lint tcl` - Run only TCL linter

## Commands

Run all linting:
```bash
make lint
```

Run Lua linting only:
```bash
make lint-lua
```

Run TCL linting only:
```bash
make lint-tcl
```

## Tools Used

- **Lua**: luacheck
- **TCL**: nagelfar

After running linters, summarize:
1. Total warnings/errors by category
2. Files with issues
3. Suggestions for fixing critical issues
