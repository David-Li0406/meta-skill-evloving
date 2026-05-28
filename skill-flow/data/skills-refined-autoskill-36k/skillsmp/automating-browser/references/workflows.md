# Claude Code MCP Patterns

Quick reference for using tabz MCP tools in Claude Code via mcp-cli.

## Check Schema First

Always check the tool schema before calling:

```bash
# Get tool schema (REQUIRED before calling)
mcp-cli info tabz/tabz_screenshot

# Search for tools by keyword
mcp-cli grep "screenshot"

# List all tabz tools
mcp-cli tools tabz
```

## Common Debugging Workflows

### Console Errors

```bash
mcp-cli info tabz/tabz_get_console_logs
mcp-cli call tabz/tabz_get_console_logs '{"level": "error"}'
```

### Network/API Debugging

```bash
# Enable BEFORE the action
mcp-cli info tabz/tabz_enable_network_capture
mcp-cli call tabz/tabz_enable_network_capture '{}'

# Trigger action (click, navigate, etc.)

# Check failures
mcp-cli info tabz/tabz_get_network_requests
mcp-cli call tabz/tabz_get_network_requests '{"statusMin": 400}'
```

### Screenshot + View

```bash
mcp-cli info tabz/tabz_screenshot
mcp-cli call tabz/tabz_screenshot '{}'
# Returns path like /tmp/tabz-screenshots/...
# Use Read tool to view the returned file path
```

### Get Page Info

```bash
mcp-cli info tabz/tabz_get_page_info
mcp-cli call tabz/tabz_get_page_info '{}'
# Returns: url, title, loading state
```

## Interaction

### Click

```bash
mcp-cli info tabz/tabz_click
mcp-cli call tabz/tabz_click '{"selector": "button.submit"}'
```

### Fill Form

```bash
mcp-cli info tabz/tabz_fill
mcp-cli call tabz/tabz_fill '{"selector": "#email", "value": "test@example.com"}'
```

## Tab Management

### List Tabs

```bash
mcp-cli info tabz/tabz_list_tabs
mcp-cli call tabz/tabz_list_tabs '{}'
# Note: Tab IDs are large integers (e.g., 1762556601)
```

### Switch Tab

```bash
mcp-cli info tabz/tabz_switch_tab
mcp-cli call tabz/tabz_switch_tab '{"tabId": 1762556601}'
```

### Create Tab Group

```bash
mcp-cli info tabz/tabz_create_group
mcp-cli call tabz/tabz_create_group '{"tabIds": [123, 456], "title": "My Research", "color": "blue"}'
```

## TTS Notifications

```bash
mcp-cli info tabz/tabz_speak
mcp-cli call tabz/tabz_speak '{"text": "Task complete", "priority": "high"}'
```

## Device Emulation

```bash
mcp-cli info tabz/tabz_emulate_device
mcp-cli call tabz/tabz_emulate_device '{"device": "iPhone 14"}'

# Clear emulation
mcp-cli info tabz/tabz_emulate_clear
mcp-cli call tabz/tabz_emulate_clear '{}'
```
