---
name: test
version: 1.0.0
changelog: Initial test runner with run_silent pattern
description: Run tests with context-efficient output.
---

# Test

Run tests with context-efficient output.

## Task
$ARGUMENTS

## Instructions

Output: `## Test`

**State**: Utility command. Does not modify STATE.md phase.

### 1. Parse Arguments

Arguments format: `[framework] [path] [extra flags]`

| Framework | Command | Fail-fast |
|-----------|---------|-----------|
| pytest | `pytest -x` | `-x` |
| jest | `jest --bail` | `--bail` |
| vitest | `vitest --bail` | `--bail` |
| go | `go test -failfast` | `-failfast` |
| npm | `npm test` | (none) |
| custom | as provided | (none) |

Default: `pytest` if no framework specified.

### 2. Execute with run_silent

Source and use the run_silent wrapper:

```bash
source .claude/skills/implement/scripts/run_silent.sh
run_silent_with_count "tests" "pytest -x tests/" "pytest"
```

This produces:
- Success: `  ✓ tests (45 tests, in 2.3s)`
- Failure: Full diagnostic output

### 3. Report Result

On success:
```markdown
## Test
✓ [framework] passed ([count] tests)
```

On failure:
```markdown
## Test
✗ [framework] failed

[Error output]
```

## Examples

```
/test                     # pytest -x (default)
/test pytest tests/api    # pytest -x tests/api
/test jest                # jest --bail
/test go ./...            # go test -failfast ./...
/test npm                 # npm test
/test "make test"         # custom command
```

## Constraints

- Always use fail-fast flags to minimize output
- Show full output only on failure
- Don't add verbose flags unless explicitly requested

## Exit Criteria

Test result reported with minimal context consumption.
