# Claude in Chrome Reference

Complete reference for the Claude in Chrome browser automation extension.

## Overview

Claude in Chrome provides direct control of the user's Chrome browser via a browser extension. This enables testing with the user's authenticated session, real-time observation, and advanced features like GIF recording and network monitoring.

## Prerequisites

1. Claude in Chrome extension installed in Chrome
2. Extension enabled for the current session
3. "Use Claude Code with Chrome" enabled in Conductor (if using Conductor)

## Session Setup

**Always call `tabs_context_mcp` first** to get available tabs and establish context:

```
mcp__claude-in-chrome__tabs_context_mcp
  createIfEmpty: true  # Creates tab group if none exists
```

This returns tab IDs that you'll use for all subsequent operations.

## Core Tools

### Tab Management

| Tool | Purpose |
|------|---------|
| `tabs_context_mcp` | Get available tabs (call FIRST) |
| `tabs_create_mcp` | Create new empty tab |

### Navigation

```
mcp__claude-in-chrome__navigate
  tabId: <number>      # Tab ID from context
  url: <string>        # URL or "back"/"forward"
```

### Reading Page Content

```
mcp__claude-in-chrome__read_page
  tabId: <number>
  filter: "all" | "interactive"  # Optional: filter elements
  depth: <number>                # Optional: tree depth (default 15)
  ref_id: <string>               # Optional: focus on specific element
```

Returns accessibility tree with `ref_*` IDs for interaction.

### Finding Elements

```
mcp__claude-in-chrome__find
  tabId: <number>
  query: <string>      # Natural language: "search bar", "login button"
```

Returns up to 20 matching elements with refs.

### Computer Actions

The `computer` tool handles clicks, typing, screenshots, and more:

```
mcp__claude-in-chrome__computer
  tabId: <number>
  action: <string>     # See action types below
  ...                  # Action-specific parameters
```

**Action types:**

| Action | Parameters | Description |
|--------|------------|-------------|
| `left_click` | `coordinate: [x, y]` or `ref: "ref_1"` | Click at position or element |
| `right_click` | `coordinate: [x, y]` | Right-click |
| `double_click` | `coordinate: [x, y]` | Double-click |
| `triple_click` | `coordinate: [x, y]` | Triple-click (select line) |
| `type` | `text: <string>` | Type text |
| `key` | `text: <string>` | Press key(s): "Enter", "cmd+a" |
| `screenshot` | - | Capture current viewport |
| `scroll` | `coordinate, scroll_direction, scroll_amount` | Scroll page |
| `scroll_to` | `ref: <string>` | Scroll element into view |
| `hover` | `coordinate` or `ref` | Move mouse without clicking |
| `wait` | `duration: <number>` | Wait (max 30 seconds) |
| `zoom` | `region: [x0, y0, x1, y1]` | Capture specific region |
| `left_click_drag` | `start_coordinate, coordinate` | Drag operation |

### Form Input

```
mcp__claude-in-chrome__form_input
  tabId: <number>
  ref: <string>        # Element ref from read_page
  value: <any>         # String, number, or boolean
```

### JavaScript Execution

```
mcp__claude-in-chrome__javascript_tool
  tabId: <number>
  action: "javascript_exec"
  text: <string>       # JS code to execute
```

Note: Don't use `return` - the last expression's value is returned automatically.

### Console Messages

```
mcp__claude-in-chrome__read_console_messages
  tabId: <number>
  pattern: <string>    # Optional: regex filter
  onlyErrors: <bool>   # Optional: errors only
  limit: <number>      # Optional: max messages (default 100)
  clear: <bool>        # Optional: clear after reading
```

### Network Requests

```
mcp__claude-in-chrome__read_network_requests
  tabId: <number>
  urlPattern: <string> # Optional: filter by URL
  limit: <number>      # Optional: max requests (default 100)
  clear: <bool>        # Optional: clear after reading
```

### GIF Recording

```
# Start recording
mcp__claude-in-chrome__gif_creator
  tabId: <number>
  action: "start_recording"

# Take screenshot immediately after to capture first frame
mcp__claude-in-chrome__computer
  tabId: <number>
  action: "screenshot"

# Perform demo actions...

# Take screenshot before stopping to capture last frame
mcp__claude-in-chrome__computer
  tabId: <number>
  action: "screenshot"

# Stop recording
mcp__claude-in-chrome__gif_creator
  tabId: <number>
  action: "stop_recording"

# Export
mcp__claude-in-chrome__gif_creator
  tabId: <number>
  action: "export"
  download: true
  filename: "demo.gif"
  options: {
    showClickIndicators: true,
    showActionLabels: true,
    showProgressBar: true
  }
```

### Image Upload

```
mcp__claude-in-chrome__upload_image
  tabId: <number>
  imageId: <string>    # From screenshot
  ref: <string>        # File input element ref
  # OR
  coordinate: [x, y]   # Drag & drop location
```

### Window Resize

```
mcp__claude-in-chrome__resize_window
  tabId: <number>
  width: <number>
  height: <number>
```

### Plan Approval

```
mcp__claude-in-chrome__update_plan
  domains: ["example.com"]
  approach: ["Step 1", "Step 2"]
```

## Common Patterns

### Authenticated Testing
```
1. tabs_context_mcp (get tab with logged-in session)
2. navigate to protected page
3. read_page to verify content
4. Interact as needed
```

### Visual Verification
```
1. tabs_context_mcp
2. navigate to page
3. computer action=screenshot
4. read_console_messages pattern="error|warn"
```

### Form Testing
```
1. navigate to form
2. read_page to get refs
3. form_input for each field
4. find query="submit button"
5. computer action=left_click ref=<submit_ref>
6. computer action=wait duration=2
7. computer action=screenshot
```

### API Debugging
```
1. tabs_context_mcp
2. navigate to page
3. Perform action that triggers API
4. read_network_requests urlPattern="/api/"
5. Inspect request/response data
```

## Best Practices

1. **Always get tab context first** - Required for all operations
2. **Create new tabs for testing** - Don't disrupt user's browsing
3. **Use refs from read_page** - More reliable than coordinates
4. **Filter console/network output** - Use patterns to reduce noise
5. **Screenshot at key points** - Visual evidence of state
6. **Avoid alerts/dialogs** - They block the extension

## Troubleshooting

### Tab ID invalid
Call `tabs_context_mcp` to get fresh tab IDs.

### Element not found
- Use `read_page` to see current page structure
- Element may be in loading state - use `wait`
- Check if element is in iframe (not directly accessible)

### Dialog blocking
JavaScript alerts/confirms block the extension. Ask user to dismiss manually.

### Extension not responding
User may need to refresh or restart Chrome.
