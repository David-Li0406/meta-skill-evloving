---
name: browser-automation
description: Use this skill for headless browser automation to navigate websites, interact with elements, take screenshots, and extract data.
---

# Browser Automation with agent-browser

## Overview
This skill provides access to the `agent-browser` CLI, a powerful tool for headless browser automation designed for AI agents. It supports web scraping, testing, form filling, and more through a series of commands and workflows.

## Quick Start
```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core Workflow
1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. **Interact**: Use commands like `click` or `fill` with the refs obtained from the snapshot.
4. **Re-snapshot**: After interactions or significant DOM changes, take a new snapshot to verify the state.

## Core Commands

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
agent-browser snapshot -d <n> # Limit depth to <n>
```

### Interactions (Use @refs from Snapshot)
```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press <key>         # Press key (e.g., Enter)
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser scroll <dir> <px>   # Scroll page
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
agent-browser screenshot <path>   # Save to file
agent-browser screenshot --full    # Full page screenshot
```

### Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait <ms>                     # Wait milliseconds
agent-browser wait --text "<text>"          # Wait for specific text
agent-browser wait --load networkidle        # Wait for network idle
```

### Semantic Locators (Alternative to Refs)
```bash
agent-browser find role <role> <action> [value]       # By ARIA role
agent-browser find text "<text>" <action>               # By text content
agent-browser find label "<label>" <action> [value]     # By label
```

## Example: Form Submission
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Example: Authentication with Saved State
```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Sessions (Parallel Browsers)
```bash
agent-browser --session <session_id> open <url>
agent-browser session list
```

## JSON Output (For Parsing)
Add `--json` for machine-readable output:
```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Debugging
```bash
agent-browser open <url> --headed  # Show browser window
agent-browser console                    # View console messages
agent-browser errors                     # View page errors
```