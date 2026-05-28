---
name: mcp-testing
description: MCP testing guidance and patterns. Loaded by /ops/test/mcp command or subagents for comprehensive Navigator MCP server testing.
compatibility: Requires bun, jq, and navigator-server running on :9334
allowed-tools: Read Glob Grep Skill TodoWrite Bash(./.claude/scripts/run-mcp-tests.sh *) Bash(nav *) Bash(nav-dev *)
metadata:
  author: outfitter-dev
  version: "1.0"
---

# Navigator MCP Testing

Automated tests for Navigator MCP server via JSON-RPC protocol.

## Quick Start

```bash
# Start server
bun run dev

# Run tests
./.claude/scripts/run-mcp-tests.sh schema-validation
./.claude/scripts/run-mcp-tests.sh --all
```

## Structure

```
.claude/
├── commands/ops/test/mcp.md         # Command definition
├── scripts/run-mcp-tests.sh         # Test runner (all logic here)
├── scripts/lib/test-runner-lib.sh   # Shared test library
└── skills/mcp-testing/SKILL.md      # This file
```

## Test Categories

| Category | Tests | What It Validates |
|----------|-------|-------------------|
| `schema-validation` | 7 | Zod schema validation, missing/invalid params |
| `action-routing` | 7 | Action dispatch for all action types |
| `error-responses` | 4 | Error codes and structured error handling |
| `response-formatting` | 4 | MCP content structure (text/image types) |

## Output

```
.scratch/testing/
├── 20260116-abc12-mcp-schema-validation.md        # Results table
├── 20260116-abc12-mcp-schema-validation-debug.log # Debug output
└── ...
```

## Adding Tests

Edit `.claude/scripts/run-mcp-tests.sh`:

```bash
# Add a test to existing category
run_mcp_test 8 "New test name" '{"action":"snap"}' "expected_pattern" "false"  # false = expect success

# Add new category
run_new_category() {
  setup_category "new-category"
  log "Running new-category tests..."

  # Setup: navigate to test page
  mcp_call '{"action":"navigate","url":"https://example.com"}' >/dev/null 2>&1

  run_mcp_test 1 "Test name" '{"action":"..."}' "pattern" "false"
  # ... more tests

  finalize_category
}
```

Then add to `main()`:
```bash
new-category) test_new_category || exit_code=1 ;;
```

## Key Differences from CLI Tests

| Aspect | CLI | MCP |
|--------|-----|-----|
| Protocol | HTTP to server | JSON-RPC over stdio |
| Input | Shell arguments | JSON objects |
| Output | JSON stdout | MCP content array |
| Error detection | Exit code + stderr | `isError` flag |

## Exit Codes

- `0` - All passed
- `1` - Failures
- `2` - Setup error (server not running, jq missing)
