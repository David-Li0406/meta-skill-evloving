# Silent Failure Patterns

Reference for detecting and fixing silent failures in Claude Code hooks.

## Why This Matters

Hook entry points are executed by Claude Code. If they fail silently:

- Claude doesn't know something went wrong
- Users don't see error messages
- Debugging becomes difficult

**Rule**: All hook entry points MUST emit to stderr on failure.

## Hook Entry Points vs Utility Scripts

| Location                 | Type        | Requirement                  |
| ------------------------ | ----------- | ---------------------------- |
| `plugins/*/hooks/*.sh`   | Entry point | MUST emit to stderr          |
| `plugins/*/hooks/*.py`   | Entry point | MUST emit to stderr          |
| `plugins/*/scripts/*.sh` | Utility     | Fallback behavior acceptable |
| `plugins/*/scripts/*.py` | Utility     | Fallback behavior acceptable |

## Bash Patterns

### Silent Commands to Check

```bash
# These commands can fail silently:
mkdir -p "$DIR"      # Directory creation
cp "$SRC" "$DST"     # File copy
mv "$SRC" "$DST"     # File move
rm -f "$FILE"        # File removal
jq '.key' "$FILE"    # JSON parsing
```

### Fix Pattern: if ! ... then

```bash
# BAD - silent failure
mkdir -p "$STATE_DIR"

# GOOD - emits to stderr
if ! mkdir -p "$STATE_DIR" 2>&1; then
    echo "[plugin] Failed to create directory: $STATE_DIR" >&2
fi
```

### Fix Pattern: || operator

```bash
# BAD - silent failure
cp "$SRC" "$DST"

# GOOD - emits to stderr on failure
cp "$SRC" "$DST" 2>&1 || echo "[plugin] Failed to copy: $SRC" >&2
```

### Fix Pattern: Trap for cleanup

```bash
# For temporary files with cleanup
temp=$(mktemp)
trap 'rm -f "$temp"' EXIT

if ! some_command > "$temp" 2>&1; then
    echo "[plugin] Command failed" >&2
fi
```

## Python Patterns

### Silent Exception: pass

```python
# BAD - silent failure
try:
    config = json.loads(path.read_text())
except (json.JSONDecodeError, OSError):
    pass  # Silent!

# GOOD - emits to stderr
try:
    config = json.loads(path.read_text())
except (json.JSONDecodeError, OSError) as e:
    print(f"[plugin] Warning: Failed to load config: {e}", file=sys.stderr)
    config = {}  # Fallback
```

### Silent Exception: No capture

```python
# BAD - no exception capture
try:
    result = subprocess.run(cmd, check=True)
except subprocess.CalledProcessError:
    return None  # What went wrong?

# GOOD - captures and logs
try:
    result = subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"[plugin] Command failed: {e}", file=sys.stderr)
    return None
```

### Acceptable Silent Patterns

Some silent patterns are acceptable in utility code:

```python
# OK in utility functions (not hook entry points)
# When fallback behavior is intentional and well-documented

def find_git_root(workspace: Path) -> Path | None:
    """Find git root, returns None if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # OK - fallback to None is documented behavior
    return None
```

## Detection Commands

### Find silent bash commands

```bash
grep -rn "mkdir\|cp\|mv\|rm" plugins/*/hooks/*.sh | grep -v "if !" | grep -v "||" | grep -v "#"
```

### Find silent Python exceptions

```bash
grep -rn "except.*:" plugins/*/hooks/*.py | grep -v "as e" | grep -v "as err"
grep -rn "pass$" plugins/*/hooks/*.py -B2 | grep "except"
```

### Run shellcheck

```bash
shellcheck plugins/*/hooks/*.sh
```

## Integration

This audit runs automatically in `/plugin-dev:create` Phase 3.

Manual invocation:

```bash
uv run plugins/plugin-dev/skills/plugin-validator/scripts/audit_silent_failures.py plugins/my-plugin/ --fix
```
