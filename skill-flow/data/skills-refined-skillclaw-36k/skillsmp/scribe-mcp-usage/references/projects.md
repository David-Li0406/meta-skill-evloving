# Projects

## Contents
- `set_project`
- `get_project`
- `list_projects`
- `delete_project`

### `set_project`
**Purpose**: Create/select a project and bootstrap documentation structure.

**Required Parameters:**
- `name` (string): Project name (automatically normalized - hyphens, underscores, spaces all work)

**Optional Parameters:**
- `root` (string): Project root directory (defaults to current directory)
- `progress_log` (string): Path to progress log file
- `defaults` (dict): Default settings for the project

**Project Name Normalization:**
Project names are automatically normalized to use underscores. You can use any of these formats:
- `"my-project"` → normalized to `"my_project"`
- `"my_project"` → kept as `"my_project"`
- `"My Project"` → normalized to `"my_project"`

This means all tools (`manage_docs`, `query_entries`, etc.) accept any format and resolve to the same project.

**Example Usage:**
```python
# Basic usage
await set_project(name="my-project")

# With custom defaults
await set_project(
    name="my-project",
    defaults={"emoji": "🧪", "agent": "MyAgent"}
)
```

**Returns:**
```json
{
  "ok": true,
  "project": {
    "name": "my-project",
    "root": "/path/to/project",
    "progress_log": "/path/to/progress/log.md",
    "docs_dir": "/path/to/docs",
    "docs": {
      "architecture": "/path/to/ARCHITECTURE_GUIDE.md",
      "phase_plan": "/path/to/PHASE_PLAN.md",
      "checklist": "/path/to/CHECKLIST.md",
      "progress_log": "/path/to/PROGRESS_LOG.md"
    },
    "defaults": {"agent": "Scribe"},
    "author": "Scribe"
  }
}
```

### `get_project`
**Purpose**: Retrieve current active project context and configuration.

**Parameters:** None

**Example Usage:**
```python
await get_project()
```

**Returns:**
```json
{
  "ok": true,
  "project": {
    "name": "current-project",
    "root": "/path/to/project",
    "progress_log": "/path/to/log.md",
    "docs_dir": "/path/to/docs",
    "defaults": {"agent": "Scribe"},
    "author": "Scribe"
  }
}
```

### `list_projects`
**Purpose**: Discover available projects and their configurations.

**Optional Parameters:**
- `limit` (int, default: 5): Maximum number of projects to return
- `filter` (string): Filter projects by name (case-insensitive substring match)
- `root` (string): Filter projects by repo root path (exact match, path-normalized). Useful for bridge integrations that need to resolve workspace → project mappings.
- `compact` (bool): Use compact response format
- `fields` (list): Specific fields to include in response
- `include_test` (bool, default: false): Include test/temp projects
- `page` (int, default: 1): Page number for pagination
- `page_size` (int): Number of items per page

**Example Usage:**
```python
# Basic usage
await list_projects()

# With pagination
await list_projects(limit=10, page=1)

# Filtered by name
await list_projects(filter="my-project", limit=3)

# Filtered by repo root (for bridge workspace resolution)
await list_projects(root="/home/austin/projects/MCP_SPINE/council_mcp")
```

**Returns:**
```json
{
  "ok": true,
  "projects": [
    {
      "name": "project-name",
      "root": "/path/to/project",
      "progress_log": "/path/to/log.md"
    }
  ],
  "count": 1,
  "pagination": {
    "page": 1,
    "page_size": 5,
    "total_count": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Logging Operations

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

## Best Practices

### 1. **Always Set Project First**
```python
await set_project(name="your-project")
# Now use other tools
```

### 2. **Use Structured Metadata**
```python
await append_entry(
    message="Fixed critical bug",
    status="success",
    meta={
        "component": "auth",
        "bug_id": "BUG-123",
        "tests_fixed": 5,
        "phase": "bugfix"
    }
)
```

### 3. **Log Meaningful Events**
- Code changes and why they were made
- Test results and failures
- Decisions and reasoning
- Bug discoveries and fixes
- Milestone completions

### 4. **Use Bulk Mode for Backfilling**
```python
# If you forget to log, use bulk mode immediately
await append_entry(items=[
    {"message": "Step 1 completed", "status": "success"},
    {"message": "Step 2 completed", "status": "success"},
    {"message": "Bug discovered", "status": "bug", "agent": "DebugBot"}
])
```

### 5. **Leverage Enhanced Search**
```python
# Cross-project learning
await query_entries(
    message="authentication pattern",
    search_scope="all_projects",
    document_types=["architecture", "progress"],
    relevance_threshold=0.9
)
```

---

## Developer Guide: Database Abstraction Layer

**For contributors adding/modifying tools that touch the database.**

All database operations MUST go through the `StorageBackend` API (`storage/base.py`). Direct SQL via `_execute()` is prohibited in tool code.

### Canonical StorageBackend Methods

| Method | Purpose |
|--------|---------|
| `upsert_project(name, repo_root, progress_log_path, docs_json)` | Create/update project |
| `fetch_project(name)` | Get project by name |
| `list_projects()` | List all projects |
| `delete_project(name)` | Delete project |
| `update_project_docs(name, docs_json)` | Partial update - docs_json only |
| `insert_entry(...)` | Add log entry |
| `fetch_recent_entries(...)` | Get recent log entries |
| `query_entries(...)` | Search log entries |

### Why Use the API

Direct `_execute()` calls bypass:
- Write locking (`_write_lock`) - causes race conditions
- Initialization (`_initialise()`) - tables may not exist
- Backend abstraction - breaks Postgres support

### Correct Pattern

```python
# ❌ WRONG - Direct SQL
await backend._execute("UPDATE scribe_projects SET docs_json = ?", (json, name))

# ✅ CORRECT - Use API
await backend.update_project_docs(name, docs_json)
```

### Adding New Operations

If no API method exists for your operation:
1. Add abstract method to `storage/base.py`
2. Implement in `storage/sqlite.py`
3. Implement in `storage/postgres.py` (if applicable)
4. Call from tool code

---

## Error Handling

Common errors and solutions:

1. **"No project configured"** → Call `set_project()` first
2. **"Invalid arguments for tool"** → Check parameter names and types
3. **"dictionary update sequence element #0 has length 1; 2 is required"** → `meta` parameter format issue

---

## Tool Summary Quick Reference

| Tool | Purpose | Required Params | Project Context |
|------|---------|----------------|-----------------|
| `set_project` | Initialize project | `name` | No |
| `get_project` | Get current context | None | Yes |
| `list_projects` | Browse projects | None | No |
| `append_entry` | **PRIMARY** logging | `message` or `items` | Yes |
| `read_recent` | Recent entries | None | Yes |
| `query_entries` | Search logs | None | Yes |
| `manage_docs` | Documentation | `action`, `doc_name` | Yes |
| `generate_doc_templates` | Create templates | `project_name` | No |
| `rotate_log` | Archive logs | None | Yes |
| `verify_rotation_integrity` | Verify archive | `archive_path` | No |
| `get_rotation_history` | Rotation history | None | Yes |
| `delete_project` | Remove project | `name`, `confirm` | No |
