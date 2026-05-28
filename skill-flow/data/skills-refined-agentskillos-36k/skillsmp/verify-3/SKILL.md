---
name: verify
description: Run code quality checks (ruff, black, mypy, pytest)
user_invocable: true
---

# /verify - Code Quality Verification

Runs all configured quality checks and reports pass/fail status. Required before commits when enforcement is enabled.

## Usage

```
/verify              # Run all checks
/verify --fix        # Run with auto-fix where possible
/verify lint         # Run only linting (ruff)
/verify format       # Run only formatting check (black)
/verify types        # Run only type checking (mypy)
/verify tests        # Run only tests (pytest)
```

## Tools

| Tool | Purpose | Auto-fix |
|------|---------|----------|
| ruff | Linting + import sorting | Yes (`--fix`) |
| black | Code formatting | Yes |
| mypy | Type checking | No |
| pytest | Test execution | No |

## Implementation

When invoked, execute the verify script:

```bash
python3 ~/.claude/plugins/agent-swarm/scripts/verify.py [args]
```

The script will:
1. Detect project type (Python, Node, etc.)
2. Run appropriate checks
3. Set `verify_passed` flag in session state if all pass
4. Output compliance signal: `[VERIFY] tests: X | types: X | lint: X | format: X`

## Enforcement Integration

When verify enforcement is enabled:
- Git commits are blocked unless verify has passed
- The `verify_passed` flag resets on any file edit
- Run `/verify` after making changes, before committing

## Exit Codes

- `0` - All checks passed
- `1` - One or more checks failed
- `2` - Configuration error (missing tools)

## Configuration

The script auto-detects tools. To customize, create `.verify.json`:

```json
{
  "lint": {"enabled": true, "cmd": "ruff check ."},
  "format": {"enabled": true, "cmd": "black --check ."},
  "types": {"enabled": true, "cmd": "mypy ."},
  "tests": {"enabled": true, "cmd": "pytest"}
}
```
