---
name: agent-browser
description: Use this skill when you need to automate browser interactions, such as filling forms, taking screenshots, or scraping data using Vercel's agent-browser CLI.
---

# Skill body

## Setup Check

```bash
# Check installation
command -v agent-browser >/dev/null 2>&1 && echo "Installed" || echo "NOT INSTALLED - run: npm install -g agent-browser && agent-browser install"
```

### Install if needed

```bash
npm install -g agent-browser
agent-browser install  # Downloads Chromium
```

## Core Workflow

**The snapshot + ref pattern is optimal for LLMs:**

1. **Navigate** to URL
2. **Snapshot** to get interactive elements with refs
3. **Interact** using refs (@e1, @e2, etc.)
4. **Re-snapshot** after navigation or DOM changes

```bash
# Step 1: Open URL
agent-browser open https://example.com

# Step 2: Get interactive elements with refs
agent-browser snapshot -i --json

# Step 3: Interact using refs
agent-browser click @e1
agent-browser fill @e2 "search query"

# Step 4: Re-snapshot after changes
agent-browser snapshot -i
```

## Key Commands

### Navigation

```bash
agent-browser open <url>       # Navigate to URL
agent-browser back             # Go back
agent-browser forward          # Go forward
agent-browser reload           # Reload page
agent-browser close            # Close browser
```

### Snapshots (Essential for AI)

```bash
agent-browser snapshot              # Full accessibility tree
agent-browser snapshot -i           # Interactive elements only (recommended)
agent-browser snapshot -i --json    # JSON output for parsing
agent-browser snapshot -c           # Compact (remove empty elements)
agent-browser snapshot -d 3         # Limit depth
```

### Interactions

```bash
agent-browser click @e1                    # Click element
agent-browser dblclick @e1                 # Double-click
agent-browser fill @e1 "text"              # Clear and fill input
agent-browser type @e1 "text"              # Type without clearing
agent-browser press Enter                  # Press key
agent-browser hover @e1                    # Hover element
agent-browser check @e1                    # Check checkbox
```