---
name: agent-browser
description: Use this skill for headless browser automation, enabling web scraping, form filling, testing, and taking screenshots through the agent-browser CLI.
---

# Agent Browser Skill

This skill provides access to the `agent-browser` CLI, a powerful tool for headless browser automation designed for AI agents.

## Core Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i --json` (Get interactive elements with refs)
3. **Interact**: Use refs from the snapshot to perform actions like `agent-browser click @e1` or `agent-browser fill @e2 "text"`.
4. **Re-snapshot**: After interactions or significant DOM changes, take a new snapshot to verify the updated state.

## Quick Start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Key Commands

### Navigation
```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward  
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (Page Analysis)
```bash
agent-browser snapshot        # Full accessibility tree
agent-browser snapshot -i     # Interactive elements only (recommended)
agent-browser snapshot -c     # Compact output
agent-browser snapshot -d 3   # Limit depth to 3
agent-browser snapshot -i --json  # JSON output for parsing
```

### Interactions (Use @refs from Snapshot)
```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser fill @e2 "text"     # Clear and fill input
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter          # Press key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser scroll down 500     # Scroll page
agent-browser scrollintoview @e1  # Scroll element into view
```

### Get Information
```bash
agent-browser get text @e1        # Get element text
agent-browser get value @e1       # Get input value
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
```

### Screenshots
```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser screenshot --full   # Full page
```

### Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --load networkidle      # Wait for network idle
```

### Sessions (Parallel Browsers)
```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

### State Persistence
```bash
agent-browser state save auth.json        # Save cookies/storage
agent-browser state load auth.json        # Load (skip login)
```

## Best Practices
1. **Always use `-i` flag** - Focus on interactive elements.
2. **Always use `--json`** - Easier to parse.
3. **Wait for stability** - Use `agent-browser wait --load networkidle`.
4. **Save auth state** - Skip login flows with `state save/load`.
5. **Use sessions** - Isolate different browser contexts.

## Example: Form Automation
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i --json
# AI identifies: @e2=name, @e3=email, @e4=submit
agent-browser fill @e2 "John Doe"
agent-browser fill @e3 "john@example.com"
agent-browser click @e4
agent-browser wait --text "Success"
```

## Installation
```bash
npm install -g agent-browser
agent-browser install                     # Download Chromium
agent-browser install --with-deps         # Linux: + system deps
```