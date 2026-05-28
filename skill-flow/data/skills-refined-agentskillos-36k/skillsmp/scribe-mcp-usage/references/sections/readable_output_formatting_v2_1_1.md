## Readable Output Formatting (v2.1.1+)

Scribe MCP tools support a `format` parameter that controls output rendering for agent readability.

### Format Options

| Format | Returns | Use Case |
|--------|---------|----------|
| `readable` (default) | `CallToolResult` with `TextContent` | Clean display in Claude Code with actual newlines |
| `structured` | Raw dict/JSON | Programmatic parsing, backward compatibility |
| `compact` | Minimal dict | Token conservation |
| `both` | `CallToolResult` + `structuredContent` | Future use when Issue #9962 is resolved |

### ANSI Color Policy

**Critical design decision for token conservation and agent experience:**

| Tool Type | ANSI Colors | Rationale |
|-----------|-------------|-----------|
| **High-frequency tools** (`append_entry`, `set_project`, confirmations) | **OFF (hardcoded)** | Called 10-30x/session; ANSI codes are visual clutter for agents |
| **Display-heavy tools** (`read_file`, `read_recent`, `query_entries`) | **Config-driven** | Called 1-5x/session; colors aid human scanning of large outputs |

**Config setting** (`.scribe/config/scribe.yaml`):
```yaml
use_ansi_colors: true  # Enable ANSI colors for display-heavy tools
```

### Implementation Pattern for Tool Authors

When adding readable format support to a new tool:

```python
# 1. Add format parameter to tool signature
async def my_tool(
    ...,
    format: str = "readable",  # readable (default), structured, compact
) -> Union[Dict[str, Any], str]:

# 2. Build response data as usual
response = {"ok": True, "data": ...}

# 3. Route through formatter at the end
return await default_formatter.finalize_tool_response(
    data=response,
    format=format,
    tool_name="my_tool"
)
```

**For high-frequency tools** (confirmations, logging):
```python
# In format_readable_my_tool():
USE_COLORS = False  # Hardcode OFF - no config check needed
```

**For display-heavy tools** (file content, log queries):
```python
# Uses self.USE_COLORS property which reads from config
if self.USE_COLORS:
    # Apply ANSI formatting
```

### Reasoning Block Display

The `append_entry` readable format parses `meta.reasoning` JSON and displays it as a tree:

```
Reasoning:
├─ Why: <decision context>
├─ What: <constraints and alternatives>
└─ How: <methodology and steps>
```

This makes the audit trail immediately scannable without parsing JSON.

### Conditional Sections

Readable formats only display sections when they contain data:
- **Reminders**: Only shown if `len(reminders) > 0`
- **Metadata**: Only shown if explicitly set and non-empty
- **Errors**: Formatted prominently with suggestions

---
