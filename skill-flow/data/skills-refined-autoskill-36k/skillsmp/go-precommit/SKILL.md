---
name: go-precommit
description: Run full pre-commit workflow for Go code. Use when preparing to commit Go changes, before creating pull requests, or ensuring code quality.
allowed-tools: ["shell"]
metadata:
  short-description: Run Go pre-commit checks
---

# Go Pre-Commit Workflow

**Read these references:**
- `~/.config/agent/domain/coding/go/tooling.md` - Go command details
- `~/.config/agent/domain/coding/quality.md` - Quality requirements (all steps blocking)

## Instructions

Execute the full pre-commit workflow in order. All steps are **blocking** - stop on first failure.

### Step 1: Format and Lint (with auto-fix)

```bash
golangci-lint run --new-false --fix ./...
```

Wait for completion. If errors occur, investigate and fix before proceeding.

### Step 2: Run Tests (with race detection and coverage)

```bash
go test -race -count 1 -coverprofile=cover.out ./...
```

All tests must pass. If failures occur:
- Read test output carefully
- Identify root cause
- Fix issues
- Re-run from Step 1

### Step 3: Final Lint Check (verify no unfixed issues)

```bash
golangci-lint run --new-false ./...
```

Ensures all lint issues are resolved. Any errors indicate problems introduced during fixes.

## Failure Handling

Per AGENT.md Problem-Solving Framework:
1. **Understand**: Read error output carefully
2. **Plan**: Identify root cause and fix strategy
3. **Execute**: Apply fix methodically
4. **Verify**: Re-run workflow from beginning
5. **Reflect**: Consider what caused the issue

## Success Criteria

All three steps must pass with zero errors before code is ready for commit.
