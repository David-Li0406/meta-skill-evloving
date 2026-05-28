## Logging Operations

### `append_entry`
**Purpose**: **PRIMARY TOOL** - Add structured log entries with metadata.

#### Single Entry Mode

**Required Parameters:**
- `agent` (string): Agent identifier (e.g., "Orchestrator", "CoderAgent", "ResearchAgent-A")
- `message` (string): Log message content

**Optional Parameters:**
- `status` (string): Status type - "info", "success", "warn", "error", "bug", "plan"
- `emoji` (string): Custom emoji override
- `meta` (dict): Metadata dictionary for context
- `timestamp_utc` (string): Custom UTC timestamp
- `log_type` (string): Target log identifier (defaults to "progress")

**Example Usage:**
```python
# Basic entry
await append_entry(agent="CoderAgent", message="Fixed authentication bug")

# With full context
await append_entry(
    agent="DebugBot",
    message="Fixed authentication bug",
    status="success",
    meta={"component": "auth", "tests_fixed": 5}
)

# Planning entry
await append_entry(
    agent="Orchestrator",
    message="Beginning database migration phase",
    status="plan",
    emoji="🗄️",
    meta={"phase": "migration", "priority": "high"}
)
```

#### Bulk Entry Mode

**Required Parameters:**
- `items` (string or list): JSON string array or direct list of entry dictionaries

**Each Entry Requires:**
- `message` (string): Log message content

**Each Entry Optional:**
- `status`, `emoji`, `agent`, `meta`, `timestamp_utc`, `log_type`

**Example Usage:**
```python
# As JSON string
await append_entry(agent="CoderAgent", items=json.dumps([
  {"message": "First task completed", "status": "success"},
  {"message": "Bug found in auth module", "status": "bug"},
  {"message": "Database migration finished", "status": "info",
   "meta": {"component": "database", "phase": "deployment"}}
]))

# As direct list
await append_entry(agent="ReviewAgent", items=[
  {"message": "Code review completed", "status": "success"},
  {"message": "Tests passing", "status": "success", "meta": {"tests_run": 25}}
])
```

**Returns:**
```json
{
  "ok": true,
  "written_line": "[ℹ️] [2025-11-02 07:39:07 UTC] [Agent: AgentName] [Project: project] [ID: hash] Your message",
  "path": "/path/to/progress/log.md",
  "meta": {"log_type": "progress"}
}
```

---
