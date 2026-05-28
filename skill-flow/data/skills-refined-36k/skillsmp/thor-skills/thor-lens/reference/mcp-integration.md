# MCP Integration

THOR Lens includes a Model Context Protocol (MCP) server that enables Claude Code and other MCP-compatible tools to query and analyze forensic timeline data.

## Transport Options

### Stdio Mode (Recommended for Claude Code)

```bash
./thorlens serve --case ./cases/mycase --mcp-stdio
```

Runs MCP over stdio with no HTTP server. Best for Claude Code integration.

### HTTP Transport Mode

```bash
./thorlens serve --case ./cases/mycase --port 8080
```

MCP is enabled by default on the same port as the web server.

**Endpoints:**
- `POST /mcp` - Send JSON-RPC messages (standard MCP HTTP transport)
- `GET /mcp` - Listen for notifications (polling)
- `DELETE /mcp` - End session

**SSE Endpoints (for clients that need SSE):**
- `GET /mcp/sse` - Establish SSE connection and get sessionId
- `POST /mcp/message?sessionId=xxx` - Send messages via SSE

## Claude Code Configuration

### Option 1: Stdio Mode (Recommended)

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "thor-lens": {
      "command": "/path/to/thorlens",
      "args": ["serve", "--case", "/path/to/cases/mycase", "--mcp-stdio"]
    }
  }
}
```

Or add to `~/.claude.json` for user-wide configuration.

**Important:**
- Use absolute paths for both the binary and case directory
- Ensure the thorlens binary is executable
- Restart Claude Code after adding configuration

### Option 2: HTTP Transport Mode

Start the server first:

```bash
./thorlens serve --case ./cases/demo --port 8080
```

Then configure `.mcp.json`:

```json
{
  "mcpServers": {
    "thor-lens": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**Note:** Use `/mcp` endpoint (not `/mcp/sse`).

## MCP Tools Available

### Query Tools

| Tool | Description |
|------|-------------|
| `search_events` | Search timeline events with filtering |
| `get_event` | Get full event details by ID |
| `get_events_by_ids` | Get multiple events by IDs (max 50) |
| `get_events_around_time` | Get events within a time window |
| `get_high_score_events` | Get events with high detection scores |

### Case Information

| Tool | Description |
|------|-------------|
| `get_case_info` | Case metadata, time range, event counts |
| `get_object_type_counts` | Event counts by object type |
| `get_time_kind_counts` | Event counts by time kind |

### Aggregation Tools

| Tool | Description |
|------|-------------|
| `get_time_buckets` | Event counts bucketed by time |
| `get_buckets_by_type` | Buckets with per-type breakdown |
| `get_buckets_by_score` | Buckets with score aggregations |
| `get_filtered_counts` | Counts for a time range |

### Analysis Tools

| Tool | Description |
|------|-------------|
| `find_related_events` | Find events related by entity or time |
| `summarize_time_range` | Summary of events in time range |

### Annotation Tools

| Tool | Description |
|------|-------------|
| `list_tags` | All tags with usage counts |
| `get_event_tags` | Tags for a specific event |
| `add_tag` | Add tag to event |
| `remove_tag` | Remove tag from event |
| `get_events_by_tags` | Find events matching tags |
| `bulk_add_tag` | Add tag to multiple events (max 100) |

### Comment Tools

| Tool | Description |
|------|-------------|
| `get_event_comments` | Get comments for an event |
| `add_comment` | Add comment to an event |

### Bookmark Tools

| Tool | Description |
|------|-------------|
| `list_bookmarks` | List bookmarked event IDs |
| `get_bookmarked_events` | Get full details of bookmarked events |
| `set_bookmark` | Bookmark an event |
| `remove_bookmark` | Remove a bookmark |

### Selection Tools

| Tool | Description |
|------|-------------|
| `list_selections` | List named selections |
| `create_selection` | Create a new selection |
| `get_selection_events` | Get event IDs in a selection |
| `add_to_selection` | Add event to selection |
| `remove_from_selection` | Remove event from selection |
| `bulk_add_to_selection` | Add multiple events (max 100) |

### Exclusion Filter Tools

| Tool | Description |
|------|-------------|
| `list_exclusion_filters` | List all exclusion patterns |
| `add_exclusion_filter` | Add exclusion pattern |
| `remove_exclusion_filter` | Remove exclusion filter |

## Tool Limits

| Limit | Value |
|-------|-------|
| Default result limit | 100 |
| Maximum result limit | 500 |
| Max bulk items | 100 |
| Max event IDs per batch | 50 |

## Example Queries in Claude Code

After connecting, Claude can:

```
"Show me all high-score events from yesterday"
"Find events related to this suspicious process"
"Tag all these events as 'lateral-movement'"
"Get events around the time of the initial access"
"Summarize activity between 2024-01-15 and 2024-01-16"
```

## Security Considerations

**Never expose MCP HTTP endpoint publicly:**
- MCP has no authentication
- Anyone with network access can query and modify annotations
- Use firewall rules to restrict access
- Prefer stdio mode for local use

## Troubleshooting

### Claude Code Can't Connect (Stdio)

1. Verify binary path is absolute and correct
2. Check binary is executable: `chmod +x /path/to/thorlens`
3. Verify case path exists and contains `meta.json`
4. Check Claude Code debug logs for errors
5. Restart Claude Code after config changes

### Claude Code Can't Connect (HTTP)

1. Verify server is running: `curl http://localhost:8080/api/meta`
2. Check port matches configuration
3. Verify firewall allows connection
4. Try `/mcp` endpoint (not `/mcp/sse`)

### No Tools Showing

1. Case must be imported first (valid `meta.json` and `events/` folder)
2. Check for errors in Claude Code's MCP logs
3. Verify JSON syntax in `.mcp.json`
