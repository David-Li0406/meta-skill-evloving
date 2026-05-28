# Error Message Style Guide

Standardized conventions for error, warning, and success messages in skill scripts.

## Message Prefixes

### Shell Scripts

```bash
# Errors (stderr, exit non-zero)
echo "ERROR: Description of what failed" >&2

# Warnings (stderr, continue execution)
echo "WARNING: Description of potential issue" >&2

# Success (stdout)
echo "OK: Description of success"

# Progress (stdout, with checkmark)
echo "✓ Task completed successfully"
```

### Python Scripts

```python
import sys

# Errors (stderr, exit non-zero)
print("Error: Description of what failed", file=sys.stderr)
sys.exit(1)

# Warnings (stderr, continue execution)
print("Warning: Description of potential issue", file=sys.stderr)

# Success (stdout)
print("OK: Description of success")

# Structured status (for validators)
print("[OK] Check passed")
print("[FAIL] Check failed")
print("[PASS] All checks passed")
```

## Capitalization Rules

| Language   | Error                 | Warning                 | Success         |
| ---------- | --------------------- | ----------------------- | --------------- |
| **Shell**  | `ERROR:` (all caps)   | `WARNING:` (all caps)   | `OK:` or `✓`    |
| **Python** | `Error:` (title case) | `Warning:` (title case) | `OK:` or `[OK]` |

## Output Destination

| Message Type     | Destination | Rationale                                                       |
| ---------------- | ----------- | --------------------------------------------------------------- |
| Errors           | `stderr`    | Separates from normal output, visible even if stdout redirected |
| Warnings         | `stderr`    | Non-fatal issues should not pollute stdout                      |
| Success/Progress | `stdout`    | Normal output flow                                              |
| Debug            | `stderr`    | Optional, for troubleshooting                                   |

## Anti-Patterns

Avoid these inconsistent patterns found in legacy code:

```bash
# BAD: Emoji mixing
echo "❌ ERROR: ..."   # Inconsistent with plain ERROR:

# BAD: Leading space
echo " ERROR: ..."     # Inconsistent spacing

# BAD: Lowercase in shell
echo "error: ..."      # Should be ERROR: in shell

# BAD: Missing colon
echo "ERROR something" # Should be "ERROR: something"
```

## Color Codes (Optional)

If using color, define constants at script top:

```bash
/usr/bin/env bash << 'ERROR_MESSAGE_STYLE_SCRIPT_EOF'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

echo -e "${RED}ERROR:${NC} Description"
echo -e "${GREEN}✓${NC} Success"
echo -e "${YELLOW}WARNING:${NC} Caution"
ERROR_MESSAGE_STYLE_SCRIPT_EOF
```

## Validator Scripts

For scripts that check multiple conditions, use bracketed notation:

```python
# Individual checks
print("[OK] ADR file exists")
print("[FAIL] Missing YAML frontmatter")

# Final summary
print("\n[PASS] All checks passed")
# or
print("\n[FAIL] 2 checks failed")
```

## Migration Checklist

When updating existing scripts:

- [ ] Replace `❌ ERROR:` with plain `ERROR:`
- [ ] Remove leading spaces from error messages
- [ ] Ensure shell uses `ERROR:` (caps) and Python uses `Error:` (title)
- [ ] Add `>&2` or `file=sys.stderr` for error/warning output
- [ ] Use consistent exit codes (0=success, 1=error)
