---
name: cli-testing
description: CLI testing guidance and patterns. Loaded by /ops/test/cli command or subagents for comprehensive Navigator CLI testing.
compatibility: Requires bun and navigator-server running on :9334
allowed-tools: Read Glob Grep Skill TodoWrite Bash(./.claude/scripts/run-tests.sh *) Bash(nav *) Bash(nav-dev *)
metadata:
  author: outfitter-dev
  version: "1.0"
---

# Navigator CLI Testing

Automated stress tests for Navigator CLI.

## Quick Start

```bash
# Start server
bun run dev

# Run tests
./.claude/scripts/run-tests.sh edge-cases
./.claude/scripts/run-tests.sh --all
```

## Structure

```
.claude/
├── commands/ops/test/cli.md     # Command definition
├── scripts/run-tests.sh         # Test runner (all logic here)
├── scripts/lib/test-runner-lib.sh  # Shared test library
└── skills/cli-testing/SKILL.md  # This file
```

## Test Categories

| Category | Tests | What It Validates |
|----------|-------|-------------------|
| `edge-cases` | 10 | Invalid refs, missing args, exit codes |
| `error-taxonomy` | 5 | Error codes from PR #30 |
| `markers` | 10 | Marker creation from refs, tags, filtering |

## Output

```
.scratch/testing/
├── 20260116-abc12-edge-cases.md        # Results table
├── 20260116-abc12-edge-cases-debug.log # Debug output
└── ...
```

## Adding Tests

Edit `.claude/scripts/run-tests.sh`:

```bash
# Add a test to existing category
run_test 11 "New test name" "nav command" "expected_pattern" "true"  # true = expect error

# Add new category
run_new_category() {
  setup_category "new-category"
  log "Running new-category tests..."

  nav open "$TEST_URL" >/dev/null 2>&1

  run_test 1 "Test name" "nav command" "pattern" "false"
  # ... more tests

  finalize_category
}
```

Then add to `main()`:
```bash
new-category) run_new_category || exit_code=1 ;;
```

## Exit Codes

- `0` - All passed
- `1` - Failures
- `2` - Setup error
