---
name: agent-browser
description:
  Browser automation using Vercel's agent-browser CLI. Use when you need to interact with web pages,
  fill forms, take screenshots, or scrape data. Uses Bash commands with ref-based element selection.
---

# agent-browser: CLI Browser Automation

Vercel's headless browser automation CLI designed for AI agents. Uses ref-based selection (@e1, @e2)
from accessibility snapshots.

## Setup

```bash
# Check installation
command -v agent-browser >/dev/null 2>&1 && echo "Installed" || echo "NOT INSTALLED"

# Install if needed
npm install -g agent-browser
agent-browser install  # Downloads Chromium
```

## Core Workflow

**Always follow the snapshot-interact-snapshot pattern:**

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

## Commands

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

### Get Information

```bash
agent-browser get text @e1          # Get element text
agent-browser get html @e1          # Get element HTML
agent-browser get value @e1         # Get input value
agent-browser get attr href @e1     # Get attribute
agent-browser get title             # Get page title
agent-browser get url               # Get current URL
agent-browser get count "button"    # Count matching elements
```

### Screenshots & PDFs

```bash
agent-browser screenshot                      # Viewport screenshot
agent-browser screenshot --full               # Full page
agent-browser screenshot output.png           # Save to file
agent-browser pdf output.pdf                  # Save as PDF
```

### Wait

```bash
agent-browser wait @e1              # Wait for element
agent-browser wait 2000             # Wait milliseconds
agent-browser wait "text"           # Wait for text to appear
```

### Semantic Locators (Alternative to Refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign up" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find placeholder "Search..." fill "query"
```

## Sessions (Parallel Browsers)

```bash
agent-browser --session browser1 open https://site1.com
agent-browser --session browser2 open https://site2.com
agent-browser session list
```

## Debug Mode

```bash
# Visible browser window for debugging
agent-browser --headed open https://example.com
```

## Examples

### Login Flow

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
# textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Sign in" [ref=e3]
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait 2000
agent-browser snapshot -i  # Verify logged in
```

### Search and Extract

```bash
agent-browser open https://news.ycombinator.com
agent-browser snapshot -i --json
agent-browser get text @e12  # Get headline text
agent-browser click @e12     # Click to open story
```

### Form Submission

```bash
agent-browser open https://forms.example.com
agent-browser snapshot -i
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser select @e3 "United States"
agent-browser check @e4  # Terms checkbox
agent-browser click @e5  # Submit
agent-browser screenshot confirmation.png
```

## Tips

### SPAs and Dynamic Content

- Always re-snapshot after clicks that trigger navigation or AJAX
- Use `wait` before snapshot if content loads asynchronously
- For React/Vue apps, wait for spinners to disappear

### Stale Refs

- Refs are invalidated after DOM changes
- If a click fails with "ref not found", re-snapshot first
- Don't cache refs across multiple interactions

### Timeouts

- Default timeout is usually 30s
- Add explicit waits for slow pages: `agent-browser wait 5000`
- Wait for specific elements: `agent-browser wait @e1`

### Handling Errors

- If element not found: re-snapshot and check available refs
- If click doesn't work: try `scrollintoview` first, then click
- For popups/modals: snapshot again after they appear

### Anti-Bot Detection

- Some sites block headless browsers
- Try `--headed` mode for debugging
- May need to add delays between actions
