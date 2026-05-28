# Serve & UI

## Serve Command

```bash
./thorlens serve --case <path> [--port N] [--mcp-stdio] [--mcp-port N]
```

| Option | Description |
|--------|-------------|
| `--case, -c` | Path to case directory (required) |
| `--port, -p` | HTTP port (default: 8080) |
| `--mcp-stdio` | Enable MCP server over stdio (no HTTP server, MCP only) |
| `--mcp-port` | MCP HTTP/SSE port (default=same as HTTP port, 0=disabled, N=specific port) |

## Serve Examples

### Standard Web Server

```bash
# Default: web UI + MCP on same port
./thorlens serve --case ./cases/demo --port 8080
# Web UI: http://localhost:8080
# MCP: http://localhost:8080/mcp
```

### Web Server with MCP Disabled

```bash
./thorlens serve --case ./cases/demo --mcp-port 0
```

### Web Server with MCP on Separate Port

```bash
./thorlens serve --case ./cases/demo --port 8080 --mcp-port 9091
# Web UI: http://localhost:8080
# MCP: http://localhost:9091/mcp
```

### MCP Stdio Mode (No HTTP Server)

```bash
./thorlens serve --case ./cases/demo --mcp-stdio
```

This mode runs MCP only over stdio - no web server. Used for Claude Code integration.

## Web UI Features

### Layout

- **Header** - Case name, time range, settings
- **Histogram** - Brush-select time ranges, click buckets to zoom
- **Filters** - Object types, time kinds, search, score filter, exclusions
- **Event Table** - Resizable columns, infinite scroll
- **Detail Pane** - Tabs for Overview, JSON, Reasons, References

### Histogram Features

| Mode | Description |
|------|-------------|
| Count mode | Bars colored by event type |
| Score mode | Bars colored by max score (hot = high score) |

| Action | Effect |
|--------|--------|
| Click and drag | Brush-select time range |
| Click bucket | Zoom to that time range |
| Presets | 2 days, 7 days, 30 days, 3 months, All |

### Predefined Tags

- suspicious, benign, IOC
- lateral-movement, persistence, exfiltration
- needs-review, false-positive

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate events |
| `←` / `→` | Hide/show detail pane |
| `b` | Toggle bookmark |
| `t` | Focus tag input |
| `/` | Focus search |
| `f` | Add entity to exclusion filters |
| `p` | Add parent path to exclusion filters |
| `d` | Clear brush selection on histogram |
| `c` | Clear search |
| `Esc` | Close detail pane |

## API Endpoints

### Event Queries (DuckDB over Parquet)

| Endpoint | Description |
|----------|-------------|
| `GET /api/meta` | Case metadata |
| `GET /api/buckets` | Time-bucket aggregations |
| `GET /api/buckets-by-type` | Buckets with type breakdown |
| `GET /api/buckets-by-score` | Buckets with score aggregations |
| `GET /api/events` | Paged event list |
| `GET /api/event/:id` | Full event detail |

### Annotations (SQLite)

| Endpoint | Description |
|----------|-------------|
| `GET/POST /api/event/:id/tags` | Manage tags |
| `GET/POST /api/event/:id/comments` | Manage comments |
| `PUT/DELETE /api/event/:id/bookmark` | Toggle bookmark |
| `GET/POST /api/selections` | Named event sets |
| `GET/POST/DELETE /api/exclusion-filters` | Manage exclusion filters |

## Event ID Stability

Every timeline event has a deterministic `event_id` derived from:

```
sha256(case_name|object_id|object_type|time_kind|timestamp)[:16]
```

This ensures:
- Same input produces same ID
- Annotations survive re-import
- 16 hex chars = 64 bits (sufficient for millions of events)

## Troubleshooting

### Port Already in Use

```bash
./thorlens serve --case ./cases/mycase --port 9000
```

### Testing API

```bash
# Check server is running
curl http://127.0.0.1:8080/api/meta | jq .

# Get event count
curl http://127.0.0.1:8080/api/meta | jq '.event_count'

# Get time range
curl http://127.0.0.1:8080/api/meta | jq '{min: .min_time, max: .max_time}'
```

### Logs and Debugging

THOR Lens logs to stdout. To see verbose output:

```bash
./thorlens serve --case ./cases/demo --port 8080 2>&1 | tee thorlens.log
```

## Reverse Proxy Notes

If placing behind nginx or another reverse proxy:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

**Security Note**: THOR Lens has no built-in authentication. Use reverse proxy authentication or restrict access via firewall.
