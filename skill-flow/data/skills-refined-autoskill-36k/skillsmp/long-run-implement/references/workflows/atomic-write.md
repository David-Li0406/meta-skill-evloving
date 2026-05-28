# Atomic Write Workflow

## Purpose

Ensure all state file updates are atomic to prevent corruption from interruptions or crashes. Uses the POSIX-atomic `mv` pattern.

## Why Atomic Writes Matter

Direct file writes can be interrupted mid-operation, leaving files in a corrupted state:
- Power failure during write
- Process killed mid-operation
- Disk full during write

The `mv` (rename) operation is atomic on POSIX systems - it either completes fully or not at all.

## Atomic Write Pattern

### Bash Implementation

```bash
write_atomic() {
  local target="$1"
  local content="$2"
  local temp="${target}.tmp.$$"

  # Write to temp file first
  echo "$content" > "$temp"

  # Atomic move (rename) to target
  mv "$temp" "$target"
}
```

### Usage Example

```bash
# Instead of dangerous direct write:
# echo "$new_state" > STATE.md  # DANGEROUS - can corrupt

# Use atomic pattern:
write_atomic "STATE.md" "$new_state"
```

## JSON Update Protocol

For JSON files like `agent-history.json`:

```bash
update_json_atomic() {
  local target="$1"
  local jq_filter="$2"
  local temp="${target}.tmp.$$"

  # Read current state
  local current=$(cat "$target")

  # Modify in memory using jq
  local updated=$(echo "$current" | jq "$jq_filter")

  # Write atomically
  echo "$updated" > "$temp"
  mv "$temp" "$target"
}

# Example: Add entry to agent-history.json
update_json_atomic "agent-history.json" \
  '.agents += [{"agent_id": "abc123", "status": "spawned"}]'
```

## Markdown Update Protocol

For markdown files like `STATE.md`:

```bash
update_markdown_section() {
  local target="$1"
  local section="$2"
  local new_content="$3"
  local temp="${target}.tmp.$$"

  # Read, modify with sed/awk, write to temp
  cat "$target" | sed "s/^$section:.*/$section: $new_content/" > "$temp"

  # Atomic move
  mv "$temp" "$target"
}
```

## Corruption Recovery

If atomic write was interrupted (temp file exists):

### Detection

```bash
check_for_corruption() {
  local target="$1"

  # Check for orphaned temp files
  local temps=$(ls -1 "${target}.tmp."* 2>/dev/null)

  if [ -n "$temps" ]; then
    echo "Found incomplete write: $temps"
    return 1
  fi
  return 0
}
```

### Recovery Procedure

```bash
recover_from_corruption() {
  local target="$1"

  # Find most recent temp file
  local latest_temp=$(ls -t "${target}.tmp."* 2>/dev/null | head -1)

  if [ -n "$latest_temp" ]; then
    # Validate temp file
    if validate_file "$latest_temp"; then
      echo "Recovering from: $latest_temp"
      mv "$latest_temp" "$target"
      return 0
    else
      echo "Temp file invalid, removing"
      rm -f "${target}.tmp."*
      return 1
    fi
  fi

  return 1
}

validate_file() {
  local file="$1"

  # For JSON files
  if [[ "$file" == *.json* ]]; then
    jq empty "$file" 2>/dev/null
    return $?
  fi

  # For markdown, check it's not empty
  if [ -s "$file" ]; then
    return 0
  fi

  return 1
}
```

## Reinitialize from SUMMARYs

If state files are unrecoverable, reconstruct from SUMMARY.md files:

```bash
reinitialize_from_summaries() {
  local state_path="$1"

  echo "Reconstructing state from SUMMARY files..."

  # Count completed plans
  local completed=$(ls -1 "$state_path/summaries/"*-SUMMARY.md 2>/dev/null | wc -l)

  # Extract last plan info from most recent SUMMARY
  local latest=$(ls -t "$state_path/summaries/"*-SUMMARY.md 2>/dev/null | head -1)

  # Rebuild agent-history.json
  local agents="[]"
  for summary in "$state_path/summaries/"*-SUMMARY.md; do
    local plan=$(basename "$summary" | cut -d'-' -f1)
    agents=$(echo "$agents" | jq ". += [{\"plan\": \"$plan\", \"status\": \"completed\"}]")
  done

  write_atomic "$state_path/agent-history.json" \
    "{\"version\": \"1.0\", \"agents\": $agents}"

  echo "Reconstructed $completed completed plans"
}
```

## Concurrency Model

- **Single executor:** Only one subagent runs per spec at a time
- **Sequential execution:** Plans run one after another, never parallel
- **No shared access:** `.long-run/` is not accessed by external processes
- **current-agent-id.txt:** Transient, only exists during active execution

## Files Using Atomic Writes

| File | Update Frequency | Critical |
|------|------------------|----------|
| `STATE.md` | After each plan | Yes |
| `agent-history.json` | On spawn/complete | Yes |
| `current-agent-id.txt` | On spawn/clear | No (transient) |
| `checkpoint.json` | After each task | Yes |
| `ISSUES.md` | On Rule 5 trigger | No |
| `clarifications.md` | On user response | No |

## Error Handling

```bash
safe_atomic_write() {
  local target="$1"
  local content="$2"
  local temp="${target}.tmp.$$"

  # Ensure directory exists
  mkdir -p "$(dirname "$target")"

  # Write to temp
  if ! echo "$content" > "$temp"; then
    echo "ERROR: Failed to write temp file"
    rm -f "$temp"
    return 1
  fi

  # Verify temp was written
  if [ ! -s "$temp" ]; then
    echo "ERROR: Temp file is empty"
    rm -f "$temp"
    return 1
  fi

  # Atomic move
  if ! mv "$temp" "$target"; then
    echo "ERROR: Failed to move temp to target"
    rm -f "$temp"
    return 1
  fi

  return 0
}
```
