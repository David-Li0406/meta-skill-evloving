## Log Maintenance

### `rotate_log`
**Purpose**: Archive current progress log and start fresh file.

**Optional Parameters:**
- `confirm` (bool): When True, perform actual rotation
- `dry_run` (bool, default: true): Preview rotation without changes
- `log_type` (string): Specific log type to rotate
- `log_types` (list): Multiple log types to rotate
- `rotate_all` (bool): Rotate every configured log type
- `auto_threshold` (bool): Only rotate if entry count exceeds threshold
- `threshold_entries` (int): Override entry threshold
- `suffix` (string): Optional suffix for archive filenames
- `custom_metadata` (string): JSON metadata for rotation record

**Example Usage:**
```python
# Preview rotation
await rotate_log(dry_run=True)

# Actually rotate progress log
await rotate_log(confirm=True)

# Rotate multiple log types
await rotate_log(
    confirm=True,
    log_types=["progress", "doc_updates"]
)

# Auto-threshold rotation
await rotate_log(
    confirm=True,
    auto_threshold=True,
    threshold_entries=1000
)
```

**Returns:**
```json
{
  "ok": true,
  "rotations": [
    {
      "log_type": "progress",
      "dry_run": false,
      "rotation_id": "unique-id",
      "project": "project-name",
      "current_file_path": "/path/to/current.md",
      "archived_to": "/path/to/archive.md",
      "entry_count": 150,
      "requires_confirmation": false,
      "auto_threshold_triggered": false
    }
  ]
}
```

### `verify_rotation_integrity`
**Purpose**: Verify the integrity of a specific rotation archive.

**Required Parameters:**
- `archive_path` (string): Path to rotation archive to verify

**Example Usage:**
```python
await verify_rotation_integrity(
    archive_path="/path/to/archive.md"
)
```

### `get_rotation_history`
**Purpose**: Return recent rotation history entries for the active project.

**Parameters:** None (requires active project)

**Example Usage:**
```python
await get_rotation_history()
```

**Returns:**
```json
{
  "ok": true,
  "project": "project-name",
  "rotation_count": 3,
  "rotations": [
    {
      "rotation_id": "id",
      "timestamp": "2025-11-02 07:40:21 UTC",
      "log_type": "progress",
      "entry_count": 150
    }
  ]
}
```

---
