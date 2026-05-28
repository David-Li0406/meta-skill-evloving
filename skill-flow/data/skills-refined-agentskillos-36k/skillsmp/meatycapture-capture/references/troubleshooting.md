# Troubleshooting Guide

Common issues when using MeatyCapture CLI and their solutions.

## JSON Parse Errors

**Problem**: `Error: Invalid JSON input at line 5`

**Solutions**:
- Validate JSON with `jq`: `echo "$JSON" | jq .`
- Use heredoc to avoid shell escaping issues
- Check for trailing commas (invalid in JSON)
- Verify proper quote escaping

**Example**:

```bash
# Test JSON validity before sending
echo "$JSON_INPUT" | jq . >/dev/null
if [ $? -eq 0 ]; then
  echo "$JSON_INPUT" | meatycapture log create --json
else
  echo "Invalid JSON" >&2
  exit 1
fi
```

---

## Project Not Found

**Problem**: `Error: Project 'xyz' not configured`

**Solutions**:
- List available projects: `meatycapture projects list --json`
- Create project first: `meatycapture projects add xyz`
- Verify project slug matches exactly (case-sensitive)
- Check configuration file: `~/.meatycapture/projects.json`

**Example**:

```bash
# Check if project exists before capture
PROJECT="meatycapture"
EXISTS=$(meatycapture projects list --json | jq -r --arg p "$PROJECT" '.projects[] | select(.id==$p) | .id')

if [ -z "$EXISTS" ]; then
  echo "Project $PROJECT not found. Creating..." >&2
  meatycapture projects add "$PROJECT" --default-path ~/.meatycapture/meatycapture
fi
```

---

## Path Not Writable

**Problem**: `Error: Cannot write to path ~/.meatycapture/xyz/`

**Solutions**:
- Check directory exists: `ls -la ~/.meatycapture/`
- Verify permissions: `stat ~/.meatycapture/xyz/`
- Create directory if missing: `mkdir -p ~/.meatycapture/xyz/`
- Check disk space: `df -h ~/.meatycapture/`
- Verify no permission issues: `test -w ~/.meatycapture/xyz/ && echo "writable"`

**Example**:

```bash
# Ensure path is writable before capture
PROJECT_PATH="$HOME/.meatycapture/meatycapture"

if [ ! -d "$PROJECT_PATH" ]; then
  echo "Creating project directory: $PROJECT_PATH" >&2
  mkdir -p "$PROJECT_PATH"
fi

if [ ! -w "$PROJECT_PATH" ]; then
  echo "Error: Path not writable: $PROJECT_PATH" >&2
  exit 2
fi

# Proceed with capture
echo "$JSON_INPUT" | meatycapture log create --json
```

---

## Append to Non-Existent Doc

**Problem**: `Error: Document not found: REQ-20251229-xyz.md`

**Solutions**:
- List existing docs: `meatycapture log list xyz --json`
- Use `create` instead of `append` for new docs
- Verify doc_id format: `REQ-YYYYMMDD-{project-slug}`
- Check file exists: `ls -la ~/.meatycapture/xyz/REQ-*.md`

**Example**:

```bash
# Check if document exists before append
DOC_PATH="$HOME/.meatycapture/meatycapture/REQ-20251229-meatycapture.md"

if [ -f "$DOC_PATH" ]; then
  # Append to existing
  echo "$ITEMS_JSON" | meatycapture log append "$DOC_PATH" --json
else
  # Create new
  echo "$CREATE_JSON" | meatycapture log create --json
fi
```

---

## Empty Response

**Problem**: Command succeeds but returns empty JSON `{}`

**Solutions**:
- Check exit code: `echo $?` (0 = success)
- Verify `--json` flag is set
- Check stderr for warnings: `2>&1 | tee output.log`
- Increase verbosity: `--verbose` (if supported)

**Example**:

```bash
# Capture both stdout and stderr
RESULT=$(echo "$JSON_INPUT" | meatycapture log create --json 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  if [ -z "$RESULT" ] || [ "$RESULT" = "{}" ]; then
    echo "Warning: Empty response, but command succeeded" >&2
  else
    echo "$RESULT" | jq .
  fi
else
  echo "Command failed (exit code: $EXIT_CODE)" >&2
  echo "$RESULT" >&2
  exit $EXIT_CODE
fi
```

---

## Validation Failures

**Problem**: `Error: Validation failed - Invalid value 'feature' for field 'type'`

**Solutions**:
- Check field values against allowed enums (see `./field-options.md`)
- Validate JSON schema before sending (see `./json-schemas.md`)
- Use templates to avoid typos (see `../templates/`)
- Review validation error details in response

**Example**:

```bash
# Pre-validate enum values
VALID_TYPES=("enhancement" "bug" "idea" "task" "question")

TYPE=$(echo "$JSON_INPUT" | jq -r '.items[0].type')

if [[ ! " ${VALID_TYPES[@]} " =~ " ${TYPE} " ]]; then
  echo "Error: Invalid type '$TYPE'. Must be one of: ${VALID_TYPES[*]}" >&2
  exit 1
fi

# Proceed with capture
echo "$JSON_INPUT" | meatycapture log create --json
```

---

## File Corruption

**Problem**: `Error: Failed to parse document - invalid YAML frontmatter`

**Solutions**:
- Check backup file: `~/.meatycapture/xyz/REQ-*.md.bak`
- Restore from backup if needed
- Validate frontmatter format
- Report issue with corrupted file content

**Example**:

```bash
# Restore from backup
DOC_PATH="$HOME/.meatycapture/meatycapture/REQ-20251229-meatycapture.md"
BACKUP_PATH="${DOC_PATH}.bak"

if [ -f "$BACKUP_PATH" ]; then
  echo "Restoring from backup: $BACKUP_PATH" >&2
  cp "$BACKUP_PATH" "$DOC_PATH"
  echo "Restored successfully" >&2
else
  echo "Error: No backup found at $BACKUP_PATH" >&2
  exit 2
fi
```

---

## Concurrent Write Conflicts

**Problem**: Two agents/processes writing to same document simultaneously

**Current Behavior**: Last-write wins (MVP limitation)

**Workarounds**:
- Serialize writes through queue or lock
- Use separate documents per agent/session
- Batch items and write once
- Check file modification time before write

**Example**:

```bash
# Simple file lock mechanism
LOCK_FILE="/tmp/meatycapture-${PROJECT}.lock"

# Acquire lock
exec 200>"$LOCK_FILE"
flock -x 200 || {
  echo "Error: Could not acquire lock" >&2
  exit 1
}

# Perform write
echo "$JSON_INPUT" | meatycapture log create --json

# Release lock (automatic on script exit)
```

---

## Permission Denied

**Problem**: `Error: Permission denied when writing to ~/.meatycapture/`

**Solutions**:
- Check file ownership: `ls -la ~/.meatycapture/`
- Fix permissions: `chmod -R u+w ~/.meatycapture/`
- Verify not running as different user
- Check parent directory permissions

**Example**:

```bash
# Fix common permission issues
CONFIG_DIR="$HOME/.meatycapture"

# Ensure directory exists with correct permissions
mkdir -p "$CONFIG_DIR"
chmod u+w "$CONFIG_DIR"

# Fix existing files
find "$CONFIG_DIR" -type f -exec chmod u+w {} \;
find "$CONFIG_DIR" -type d -exec chmod u+w {} \;
```

---

## Large Document Performance

**Problem**: Append operations slow on documents with 100+ items

**Solutions**:
- Create new document for new work period
- Use titled documents to group related items
- Consider archiving old documents
- Optimize tag aggregation (future enhancement)

**Best Practice**:

```bash
# Create new document for each work session/day
# Rather than appending to massive document

# Good: One doc per day/session
echo '{
  "project": "meatycapture",
  "title": "Work Session - 2025-12-29 PM",
  "items": [...]
}' | meatycapture log create --json

# Avoid: Appending to 6-month-old document with 500 items
```

---

## Exit Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Parse response JSON |
| 1 | Validation Error | Fix input JSON, check field values |
| 2 | File I/O Error | Check paths, permissions, disk space |
| 3 | Command Error | Verify command syntax, arguments |
| 124 | Timeout | Increase timeout, check system load |
| 127 | Command Not Found | Install/configure MeatyCapture CLI |

**Example - Handle All Exit Codes**:

```bash
RESULT=$(echo "$JSON_INPUT" | meatycapture log create --json 2>&1)
EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "Success"
    echo "$RESULT" | jq .
    ;;
  1)
    echo "Validation error:" >&2
    echo "$RESULT" | jq -r '.error' >&2
    ;;
  2)
    echo "File I/O error - check paths and permissions" >&2
    ;;
  3)
    echo "Command error - check syntax" >&2
    ;;
  127)
    echo "MeatyCapture CLI not found - install first" >&2
    ;;
  *)
    echo "Unknown error (exit code: $EXIT_CODE)" >&2
    ;;
esac

exit $EXIT_CODE
```

---

## Debugging Tips

### Enable Verbose Output

```bash
# If CLI supports verbose mode
MEATYCAPTURE_DEBUG=1 meatycapture log create input.json --json --verbose
```

### Inspect Generated Document

```bash
# View created document to verify output
DOC_PATH=$(echo "$JSON_INPUT" | meatycapture log create --json | jq -r '.doc_path')
cat "$DOC_PATH"
```

### Validate Input Before Sending

```bash
# Use validation script from json-schemas.md
./validate-meatycapture-input.sh "$JSON_INPUT"
if [ $? -eq 0 ]; then
  echo "$JSON_INPUT" | meatycapture log create --json
fi
```

### Check Configuration

```bash
# Verify projects and fields configuration
cat ~/.meatycapture/projects.json | jq .
cat ~/.meatycapture/fields.json | jq .
```

### Test with Minimal Input

```bash
# Simplify to isolate issue
echo '{
  "project": "meatycapture",
  "items": [{
    "title": "Test",
    "type": "task",
    "domain": "core"
  }]
}' | meatycapture log create --json
```

---

## Getting Help

1. **Check documentation**: `./field-options.md`, `./json-schemas.md`
2. **Review examples**: `../templates/`, `../SKILL.md`
3. **Validate input**: Use `jq` to check JSON structure
4. **Test CLI**: `meatycapture --help`, `meatycapture log --help`
5. **Check logs**: stderr output, system logs
6. **File issue**: If bug discovered, capture it using this skill!

**Example - Self-Documenting Bug**:

```bash
# Bug found while using skill - capture it!
echo '{
  "project": "meatycapture",
  "items": [{
    "title": "CLI returns empty response on create",
    "type": "bug",
    "domain": "cli",
    "priority": "high",
    "tags": ["cli", "json-output", "bug"],
    "notes": "Problem: `meatycapture log create` succeeds (exit 0) but returns empty JSON instead of doc_id.\n\nRepro: [exact command]\nExpected: {\"success\":true,\"doc_id\":\"...\"}\nActual: {}\n\nGoal: Return proper response JSON."
  }]
}' | meatycapture log create --json
```
