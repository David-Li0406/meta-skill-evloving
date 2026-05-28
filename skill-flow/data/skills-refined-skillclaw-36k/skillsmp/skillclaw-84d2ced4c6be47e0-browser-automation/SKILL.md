---
name: browser-automation
description: Use this skill when you need to automate browser tasks such as navigating websites, verifying UI, testing web applications, or scraping data.
---

# Browser Automation

Browser automation via Vercel's agent-browser CLI. Runs headless by default; use `--headed` for a visible window. Uses ref-based selection (@e1, @e2) from accessibility snapshots.

## Setup

```bash
command -v agent-browser >/dev/null 2>&1 && echo "OK" || echo "MISSING: npm i -g agent-browser && agent-browser install"
```

## Core Workflow

1. **Open** URL
2. **Snapshot** to get refs
3. **Interact** via refs
4. **Re-snapshot** after DOM changes

```bash
agent-browser open https://example.com
agent-browser snapshot -i              # Interactive elements with refs
agent-browser click @e1
agent-browser wait --load networkidle  # Wait for SPA to settle
agent-browser snapshot -i              # Re-snapshot after change
```

## Essential Commands

### Navigation

```bash
agent-browser open <url>       # Navigate
agent-browser back             # Go back
agent-browser forward          # Go forward
agent-browser reload           # Reload
agent-browser close            # Close browser
```

### Snapshots

```bash
agent-browser snapshot           # Full accessibility tree
agent-browser snapshot -i        # Interactive only (recommended)
agent-browser snapshot -i --json # JSON for parsing
agent-browser snapshot -c        # Compact (remove empty)
agent-browser snapshot -d 3      # Limit depth
agent-browser snapshot -s "#main" # Scope to selector
```

### Interactions

```bash
agent-browser click @e1              # Click
agent-browser dblclick @e1           # Double-click
agent-browser fill @e1 "text"        # Clear + fill input
agent-browser type @e1 "text"        # Type without clearing
agent-browser press Enter            # Key press
agent-browser press Control+a        # Key combination
agent-browser hover @e1              # Hover
agent-browser check @e1              # Check checkbox
agent-browser uncheck @e1            # Uncheck
agent-browser select @e1 "option"    # Dropdown
agent-browser scroll down 500        # Scroll direction
```