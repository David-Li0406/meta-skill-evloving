---
name: agent-browser
description: Use this skill for browser automation tasks such as web interaction, form filling, taking screenshots, and scraping data using Vercel's agent-browser CLI.
---

# Skill body

## Setup

```bash
# Check installation
command -v agent-browser >/dev/null 2>&1 && echo "Installed" || echo "NOT INSTALLED - run: npm install -g agent-browser && agent-browser install"

# Install if needed
npm install -g agent-browser
agent-browser install  # Downloads Chromium
```

## Core Workflow

**Follow the snapshot-interact-snapshot pattern:**

1. **Navigate** to URL
2. **Snapshot** to get interactive elements with refs
3. **Interact** using refs (@e1, @e2, etc.)
4. **Re-snapshot** after any navigation or DOM changes

```bash
agent-browser open https://example.com
agent-browser snapshot -i              # Get refs for interactive elements
agent-browser click @e1
agent-browser fill @e2 "search query"
agent-browser snapshot -i              # Re-snapshot after changes
```

## Verification Capabilities

### What You CAN Verify (High Confidence)

- Element existence (by test ID, role, or text)
- Text content of elements
- Page titles and headings
- Form field presence and labels
- Button clicks triggering navigation
- Form submission behavior
- Error message display
- Console errors

### What You CANNOT Verify (Flag for Human)

- Layout and spacing
- Element positioning ("is button centered?")
- Visual alignment ("do these items line up?")
- Responsive behavior at breakpoints
- Color and styling
- Overall aesthetics
- "Does this look right?"

**ALWAYS** flag these for human review when UI is involved.

## Command Reference

### Navigation

```bash
agent-browser open <url>       # Navigate to URL
agent-browser back             # Go back
agent-browser forward          # Go forward
agent-browser reload           # Reload page
agent-browser close            # Close browser
```

### Snapshots

```bash
agent-browser snapshot              # Full accessibility tree
agent-browser snapshot -i           # Interactive elements only (preferred)
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
agent-browser uncheck @e1                  # Uncheck checkbox
agent-browser select @e1 "option"          # Select dropdown option
agent-browser scroll down 500              # Scroll (up/down/left/right)
agent-browser scrollintoview @e1           # Scroll element into view
```