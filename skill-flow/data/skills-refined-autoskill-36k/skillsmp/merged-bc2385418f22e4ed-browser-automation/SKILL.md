---
name: browser-automation
description: Use this skill when you need to automate browser interactions for web testing, form filling, screenshots, and data extraction.
---

# Browser Automation

You are a browser automation specialist. Your role is to automate web interactions for testing, data extraction, and web application validation.

## Your Task

Execute the following browser automation request: `<ARGUMENTS>`

## Quick Start

```bash
# Navigate to a page
agent-browser open <url>

# Take a snapshot of interactive elements
agent-browser snapshot -i

# Click an element by reference
agent-browser click @e1

# Fill an input by reference
agent-browser fill @e2 "text"

# Close the browser
agent-browser close
```

## Core Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. **Interact** using refs from the snapshot
4. **Re-snapshot** after navigation or significant DOM changes

## Commands

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
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interactions (Use @refs from Snapshot)
```bash
agent-browser click @e1           # Click
agent-browser fill @e2 "text"     # Clear and type
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown
```

### Get Information
```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get title           # Get page title
```

### Screenshots & PDF
```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser pdf output.pdf      # Save as PDF
```

### Video Recording
```bash
agent-browser record start ./demo.webm    # Start recording
agent-browser record stop                 # Stop and save video
```

### Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
```

### Semantic Locators (Alternative to Refs)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
```

### Cookies & Storage
```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser storage local               # Get all localStorage
```

### Network
```bash
agent-browser network route <url>              # Intercept requests
agent-browser network unroute [url]            # Remove routes
```

### Tabs & Windows
```bash
agent-browser tab new [url]       # New tab
agent-browser tab close           # Close tab
```

### Frames
```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

### Dialogs
```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

### JavaScript
```bash
agent-browser eval "document.title"   # Run JavaScript
```

## Example: Form Submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
```

## Example: Authentication with Saved State

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Debugging

```bash
agent-browser open example.com --headed              # Show browser window
agent-browser console                                # View console messages
```

## Error Recovery

Page state persists after failures. Debug with:

```bash
agent-browser open example.com
agent-browser snapshot -i
```

## Environment Variables

```bash
DB_SERVER_URL=http://localhost:9222  # Server URL (default)
```

## Scraping Guide

For large datasets, intercept and replay network requests rather than scrolling the DOM. See the complete guide for scraping techniques.