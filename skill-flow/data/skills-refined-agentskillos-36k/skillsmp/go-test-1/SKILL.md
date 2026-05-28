---
name: go-test
description: Run Go tests with race detection and coverage. Use when asked to run tests, check test coverage, or verify Go code functionality.
allowed-tools: ["shell"]
metadata:
  short-description: Run Go tests with race detection
---

# Go Test Runner

**Reference:** `~/.config/agent/domain/coding/go/tooling.md` for Go command details

## Instructions

Run Go tests with proper flags per AGENT.md guidelines:

### Standard Test Run

```bash
go test -race -count 1 -coverprofile=cover.out ${ARGUMENTS}
```

Default to `./...` if no package path is provided.

### Verbose Mode

If user requests verbose output:
```bash
go test -v -race -count 1 -coverprofile=cover.out ${ARGUMENTS}
```

### Coverage Report

After tests pass, offer to show coverage:
```bash
# Text summary
go tool cover -func=cover.out

# HTML report (opens in browser)
go tool cover -html=cover.out
```

### Package-Specific Tests

For single package:
```bash
go test -race -count 1 ./path/to/package
```

### Test Flags

- `-race`: Enable race detector
- `-count 1`: Disable test caching
- `-coverprofile`: Generate coverage profile
- `-v`: Verbose output (when requested)

## Arguments

Target package(s): ${ARGUMENTS:-./...}
