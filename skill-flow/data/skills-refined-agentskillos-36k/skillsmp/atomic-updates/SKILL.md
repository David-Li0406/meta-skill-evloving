---
name: atomic-updates
description: Atomic file update patterns to prevent corruption
category: orchestration
depends-on: []
---

# Atomic Updates

> "Read-modify-write with temp file - prevents corruption from concurrent writes."

## The Problem

If two agents write to the same file simultaneously, data can be lost or corrupted.

## The Solution: Atomic Updates

Always update files using the temp-file pattern:

```bash
# Read
STATE=$(cat file.json)

# Modify
NEW_STATE=$(echo "$STATE" | jq '.field = "value"')

# Write atomically
echo "$NEW_STATE" > file.json.tmp && mv file.json.tmp file.json
```

The `mv` command is atomic on Unix-like systems - either the whole rename succeeds or it fails, never leaving a partial file.

## PowerShell Atomic Update

```powershell
# Read
$state = Get-Content "file.json" | ConvertFrom-Json

# Modify
state.field = "value"

# Write atomically
$tempPath = "file.json.tmp"
$state | ConvertTo-Json -Depth 10 | Set-Content -Path $tempPath
Move-Item -Path $tempPath -Destination "file.json" -Force
```

## Update Specific Field (jq)

```bash
# Single field update
jq '.iteration += 1' coordinator-state.json > coordinator-state.json.tmp
mv coordinator-state.json.tmp coordinator-state.json

# Nested field update
jq '.agents.developer.lastSeen = "2026-01-19T12:00:00Z"' coordinator-state.json > coordinator-state.json.tmp
mv coordinator-state.json.tmp coordinator-state.json
```

## PowerShell Update-JsonFile (if available)

If the project provides `Update-JsonFile`:

```powershell
Update-JsonFile -FilePath "file.json" -UpdateScript {
    param($state)
    $state.field = "value"
    return $state
}
```

This wrapper handles the atomic pattern automatically.

## Error Handling

If atomic update fails:

1. **Log the error** - write to progress file
2. **Wait 5 seconds** - give other processes time to complete
3. **Re-read the file** - get latest state
4. **Re-apply changes** - merge your updates
5. **Try again** - attempt atomic update once more

If it fails twice, log the conflict and continue polling.

## When Atomic Updates Matter Most

- **High-contention files**: `coordinator-state.json`, `current-task.json`
- **Shared log files**: `session.log` (use append-only instead)
- **PRD file**: Multiple agents may update different fields

## When Atomic Updates Don't Apply

- **Agent-specific files**: `developer-progress.txt` (only one writer)
- **Append-only logs**: These don't need atomic pattern
- **New file creation**: No existing content to protect

## Reference

- [file-permissions.md](file-permissions.md) — Who can write to what
