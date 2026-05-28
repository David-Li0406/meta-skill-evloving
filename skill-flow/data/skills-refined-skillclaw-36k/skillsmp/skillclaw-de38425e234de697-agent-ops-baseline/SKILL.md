---
name: agent-ops-baseline
description: Use this skill when capturing baseline build, lint, and test results, or investigating newly introduced findings.
---

# Baseline Workflow

## Preconditions
- Ensure that `.agent/constitution.md` exists and commands are CONFIRMED.

## CLI Commands

**This skill works with or without the `aoc` CLI installed.** Baseline operations use direct file editing by default.

### Build/Lint/Test Commands

Retrieve commands from `.agent/constitution.md`, which may vary by project:

```bash
# Example constitution commands (project-specific)
build: npm run build
lint: npm run lint
test: npm run test
format: npm run format
```

### Issue Discovery After Baseline (File-Based — Default)

To track baseline findings as issues:

1. Increment `.agent/issues/.counter`.
2. Append issues to the appropriate `.agent/issues/{priority}.md` file.
3. Use type `BUG` for failures and `CHORE` for warnings.

### CLI Integration (when `aoc` is available)

If the `aoc` CLI is detected in `.agent/tools.json`, the following commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| Create issue from finding | `aoc issues create --type BUG --priority high --title "..."` |
| List existing issues | `aoc issues list --status open` |
| Show issue | `aoc issues show <ID>` |

## Baseline Capture (mandatory before code changes)

1. Run build/lint commands from the constitution.
2. Write to `.agent/baseline.md`:
   - Commands executed
   - Exit codes
   - Warnings/errors grouped by file
3. Run unit tests command from the constitution.
4. Write to `.agent/baseline.md`:
   - Command
   - Summary (pass/fail/skip counts)
   - Failure details (stack traces/logs)

## Issue Discovery After Baseline

**After capturing the baseline, invoke the `agent-ops-tasks` discovery procedure:**

1. Collect all findings from the baseline:
   - Build errors → `BUG` (critical/high)
   - Test failures → `BUG` (high)
   - Lint errors → `BUG` (medium)
   - Lint warnings → `CHORE` (low/medium)
   - Missing test coverage → `TEST` (medium)
   - Security warnings → `SEC` (high)

2. Present to the user:
   ```
   📋 Baseline captured. Found {N} existing issues:
   
   High:
   - [BUG] 2 failing tests in UserService
   - [SEC] 1 security warning (npm audit)
   
   Medium:
   - [BUG] 15 lint errors
   - [TEST] Coverage below threshold
   ```