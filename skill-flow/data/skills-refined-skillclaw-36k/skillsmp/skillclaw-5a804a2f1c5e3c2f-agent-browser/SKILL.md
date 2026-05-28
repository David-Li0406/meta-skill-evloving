---
name: agent-browser
description: Use this skill when you need to automate web interactions, extract structured data, fill forms programmatically, or test web UIs using a headless browser.
---

# Skill body

## Installation

### npm recommended

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

### From Source

```bash
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install
pnpm build
agent-browser install
```

## Quick Start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core Workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

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
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser press Control+a     # Key combination
agent-browser keydown Shift       # Hold key down
agent-browser keyup Shift         # Release key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
```

## Using Real Chrome Profile (for OAuth/Logged-in Sessions)

For sites requiring Google/Discord/etc login (like star-swap.com):

**Method 1: Launch Chrome with Custom Profile, Connect via CDP**

```bash
# Terminal 1: Launch Chrome with your real profile and remote debugging
google-chrome --remote-debugging-port=9222 --user-data-dir=/home/user/.config/google-chrome/Default &

# Terminal 2: Connect agent-browser to that Chrome instance
agent-browser --cdp 9222 open "https://star-swap.com"
agent-browser --cdp 9222 snapshot -i
agent-browser --cdp 9222 click @e2
```

**Method 2: Session Persistence (First-time Manual Login)**

```bash
# First time: headed mode, login manually
agent-browser --headed --session starswap open "https://star-swap.com"
# Complete Google OAuth manually in the browser window
# Close when done

# Future runs: cookies persist!
agent-browser --session starswap open "https://star-swap.com"
# Already logged in automatically
```