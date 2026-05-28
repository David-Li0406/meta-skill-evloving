---
name: browser-automation
description: Use this skill for browser automation tasks such as web interaction, form filling, taking screenshots, scraping data, and UI/backend verification using Vercel's agent-browser CLI.
---

# Browser Automation: CLI Browser Automation

Vercel's headless browser automation CLI designed for AI agents. Uses ref-based selection (@e1, @e2) from accessibility snapshots.

## Setup Check

```bash
# Check installation
command -v agent-browser >/dev/null 2>&1 && echo "Installed" || echo "NOT INSTALLED - run: npm install -g agent-browser && agent-browser install"
```

### Install if Needed

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
agent-browser open <url>

# Step 2: Get interactive elements with refs
agent-browser snapshot -i

# Step 3: Interact using refs
agent-browser click @e1
agent-browser fill @e2 "search query"

# Step 4: Re-snapshot after changes
agent-browser snapshot -i
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
- Element positioning
- Visual alignment
- Responsive behavior at breakpoints
- Color and styling
- Overall aesthetics

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
agent-browser wait --url "**/path"  # Wait for URL pattern
```

### Execute JavaScript

```bash
agent-browser execute "localStorage.setItem('key', 'value')"
agent-browser execute "document.querySelector('.btn').click()"
```

### Console Errors

```bash
agent-browser errors                # Get console errors
```

## Semantic Locators (Alternative to Refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign up" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find placeholder "Search..." fill "query"
```

## Sessions (Parallel Browsers)

```bash
# Run multiple independent browser sessions
agent-browser --session browser1 open https://site1.com
agent-browser --session browser2 open https://site2.com

# List active sessions
agent-browser session list
```

## Debug Mode

```bash
# Run with visible browser window
agent-browser --headed open <url>
```

Use headed mode when debugging automation issues or testing apps with popups.

## JSON Output

Add `--json` for structured output:

```bash
agent-browser snapshot -i --json
```

## Important Rules

1. **ALWAYS** capture screenshots
2. **NEVER** claim confidence above 80% for UI
3. **ALWAYS** list what needs human review
4. **DOCUMENT** element refs used
5. **REPORT** console errors prominently
6. **TIMEOUT** gracefully after 60 seconds

## Examples

### Login Flow

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait 2000
agent-browser screenshot .unitwork/verify/after-login.png
agent-browser snapshot -i  # Verify logged in
```

### Form Filling with Verification

```bash
agent-browser open https://forms.example.com
agent-browser snapshot -i
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser select @e3 "United States"
agent-browser check @e4  # Agree to terms
agent-browser screenshot .unitwork/verify/form-filled.png
agent-browser click @e5  # Submit button
agent-browser wait 2000
agent-browser snapshot -i  # Check for success message
agent-browser errors  # Check for console errors
```