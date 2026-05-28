## Project Cleanup

### `delete_project`
**Purpose**: Delete or archive a project and all associated data.

**Required Parameters:**
- `name` (string): Project name to delete
- `confirm` (bool): Must be True to proceed with deletion

**Optional Parameters:**
- `mode` (string, default: "archive"): "archive" or "permanent"
- `force` (bool): Override safety checks (not recommended)
- `archive_path` (string): Custom archive directory
- `agent_id` (string): Agent identification

**Example Usage:**
```python
# Archive project (safe default)
await delete_project(
    name="old-project",
    confirm=True
)

# Permanent deletion (dangerous)
await delete_project(
    name="temp-project",
    confirm=True,
    mode="permanent"
)
```

**Returns:**
```json
{
  "success": true,
  "project_name": "project-name",
  "mode": "archive",
  "message": "Project 'project-name' archived to path",
  "archive_location": "/path/to/archive",
  "database_cleanup": true
}
```

---
