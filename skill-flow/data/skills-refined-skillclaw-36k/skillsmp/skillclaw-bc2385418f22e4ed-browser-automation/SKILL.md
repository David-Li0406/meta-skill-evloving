---
name: browser-automation
description: Use this skill when you need to automate browser interactions for web testing, form filling, screenshots, and data extraction.
---

# Browser Automation Skill

This skill allows you to automate various browser interactions, including navigating websites, filling out forms, taking screenshots, and extracting data. 

## Quick Start

1. **Navigate to a URL**: 
   ```bash
   agent-browser open <url>
   ```

2. **Take a Snapshot of the Page**: 
   ```bash
   agent-browser snapshot -i  # Get interactive elements with refs
   ```

3. **Interact with Elements**: Use the refs obtained from the snapshot to perform actions:
   ```bash
   agent-browser click @e1           # Click an element
   agent-browser fill @e2 "text"     # Fill an input field
   ```

4. **Close the Browser**: 
   ```bash
   agent-browser close
   ```

## Core Commands

### Navigation
```bash
agent-browser open <url>      # Navigate to a specific URL
agent-browser back            # Go back in browser history
agent-browser forward         # Go forward in browser history
agent-browser reload          # Reload the current page
agent-browser close           # Close the browser
```

### Snapshot Commands
```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interaction Commands
```bash
agent-browser click @e1           # Click an element by ref
agent-browser fill @e2 "text"     # Fill an input field by ref
agent-browser check @e1           # Check a checkbox
agent-browser uncheck @e1         # Uncheck a checkbox
```

## Trigger Phrases
Use this skill when you hear phrases like "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", or "log into".