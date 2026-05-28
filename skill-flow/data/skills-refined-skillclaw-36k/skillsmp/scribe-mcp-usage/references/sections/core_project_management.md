## Core Project Management

### `set_project`
**Purpose**: Create/select a project and bootstrap documentation structure.

**Required Parameters:**
- `agent` (string): Agent identifier (e.g., "Orchestrator", "CoderAgent", "ResearchAgent-A")
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
await set_project(agent="Orchestrator", name="my-project")

# With custom defaults
await set_project(
    agent="CoderAgent",
    name="my-project",
    defaults={"emoji": "🧪"}
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

**Required Parameters:**
- `agent` (string): Agent identifier

**Example Usage:**
```python
await get_project(agent="Orchestrator")
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

**Required Parameters:**
- `agent` (string): Agent identifier

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
await list_projects(agent="Orchestrator")

# With pagination
await list_projects(agent="CoderAgent", limit=10, page=1)

# Filtered by name
await list_projects(agent="ResearchAgent", filter="my-project", limit=3)

# Filtered by repo root (for bridge workspace resolution)
await list_projects(agent="Orchestrator", root="/home/austin/projects/MCP_SPINE/council_mcp")
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
