# Querying Logs

## Contents
- `read_recent`
- `query_entries`

### `read_recent`
**Purpose**: Retrieve recent log entries with pagination.

**Optional Parameters:**
- `n` (int, default: 50): Number of recent entries to return
- `filter` (dict): Optional filters for agent, status, emoji
- `page` (int, default: 1): Page number for pagination
- `page_size` (int): Number of entries per page
- `compact` (bool): Use compact response format
- `fields` (list): Specific fields to include
- `include_metadata` (bool): Include metadata field in entries

**Example Usage:**
```python
# Basic usage
await read_recent()

# Limited entries
await read_recent(n=10)

# With filters
await read_recent(n=5, filter={"agent": "DebugBot", "status": "success"})
```

**Returns:**
```json
{
  "ok": true,
  "entries": [
    {
      "id": "entry_id",
      "ts": "2025-11-02 07:39:07 UTC",
      "emoji": "ℹ️",
      "agent": "AgentName",
      "message": "Log message",
      "meta": {"log_type": "progress"},
      "raw_line": "Full log line"
    }
  ],
  "count": 1,
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_count": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### `query_entries`
**Purpose**: Advanced log searching and filtering.

**Optional Parameters:**
- `project` (string): Project name (uses active project if None)
- `start` (string): Start timestamp filter
- `end` (string): End timestamp filter
- `message` (string): Message text filter
- `message_mode` (string): How to match message - "substring", "regex", "exact"
- `case_sensitive` (bool): Case sensitive message matching
- `emoji` (string or list): Filter by emoji(s)
- `status` (string or list): Filter by status(es)
- `agents` (string or list): Filter by agent name(s)
- `meta_filters` (dict): Filter by metadata key/value pairs
- `limit` (int): Maximum results to return
- `page` (int): Page number for pagination
- `page_size` (int): Number of results per page

**Enhanced Search Parameters:**
- `search_scope`: "project", "global", "all_projects", "research", "bugs", "all"
- `document_types`: ["progress", "research", "architecture", "bugs", "global"]
- `relevance_threshold`: Minimum relevance score (0.0-1.0)
- `verify_code_references`: Check if mentioned code exists
- `time_range`: Temporal filtering ("last_30d", "last_7d", "today")

**Example Usage:**
```python
# Basic message search
await query_entries(message="bug", message_mode="substring")

# Date range search
await query_entries(start="2025-10-23", end="2025-10-24")

# Enhanced cross-project search
await query_entries(
    message="authentication",
    search_scope="all_projects",
    document_types=["progress", "bugs"],
    relevance_threshold=0.8
)

# Metadata filtering
await query_entries(
    meta_filters={"component": "auth", "severity": "high"}
)
```

**Returns:**
```json
{
  "ok": true,
  "entries": [/* matching entries */],
  "count": 5,
  "pagination": {/* pagination info */}
}
```

---
