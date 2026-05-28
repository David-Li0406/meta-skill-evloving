---
name: agent-browser
description: Browser automation CLI for AI agents. Use this skill to navigate websites, interact with elements, take screenshots, and extract data using a headless browser.
triggers:
  - "browse the web"
  - "open website"
  - "check url"
  - "take screenshot"
  - "agent-browser"
  - "use browser"
---

# Agent Browser Skill

This skill provides access to the `agent-browser` CLI, a powerful tool for headless browser automation designed for AI agents.

## 🚀 Usage

The core workflow relies on **snapshots** and **refs**. Instead of guessing CSS selectors, you get a snapshot of the page with unique references (like `@e1`, `@e2`) for every interactive element.

### Basic Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Analyze**: `agent-browser snapshot -i` (Get interactive elements with refs)
3. **Interact**: `agent-browser click @e1` or `agent-browser fill @e2 "text"`
4. **Repeat**: Take a new snapshot after interactions to see the updated state.

### Common Commands

- **Open URL**: `agent-browser open google.com`
- **Get Snapshot**: `agent-browser snapshot -i` (Interactive only, recommended)
- **Click**: `agent-browser click @e1`
- **Type/Fill**: `agent-browser fill @e2 "search term"`
- **Press Key**: `agent-browser press Enter`
- **Go Back**: `agent-browser back`
- **Screenshot**: `agent-browser screenshot page.png`
- **Read Text**: `agent-browser get text @e1`

### Advanced

- **Sessions**: `agent-browser --session my-session open ...` (Keep cookies/state separate)
- **Wait**: `agent-browser wait --text "Success"`
- **Help**: `agent-browser --help`
-

### Core Commands

agent-browser open <url>              # Navigate to URL (aliases: goto, navigate)
agent-browser click <sel>             # Click element
agent-browser dblclick <sel>          # Double-click element
agent-browser focus <sel>             # Focus element
agent-browser type <sel> <text>       # Type into element
agent-browser fill <sel> <text>       # Clear and fill
agent-browser press <key>             # Press key (Enter, Tab, Control+a) (alias: key)
agent-browser keydown <key>           # Hold key down
agent-browser keyup <key>             # Release key
agent-browser hover <sel>             # Hover element
agent-browser select <sel> <val>      # Select dropdown option
agent-browser check <sel>             # Check checkbox
agent-browser uncheck <sel>           # Uncheck checkbox
agent-browser scroll <dir> [px]       # Scroll (up/down/left/right)
agent-browser scrollintoview <sel>    # Scroll element into view (alias: scrollinto)
agent-browser drag <src> <tgt>        # Drag and drop
agent-browser upload <sel> <files>    # Upload files
agent-browser screenshot [path]       # Take screenshot (--full for full page, base64 png to stdout if no path)
agent-browser pdf <path>              # Save as PDF
agent-browser snapshot                # Accessibility tree with refs (best for AI)
agent-browser eval <js>               # Run JavaScript
agent-browser connect <port>          # Connect to browser via CDP
agent-browser close                   # Close browser (aliases: quit, exit)

### Get Info

agent-browser get text <sel>          # Get text content
agent-browser get html <sel>          # Get innerHTML
agent-browser get value <sel>         # Get input value
agent-browser get attr <sel> <attr>   # Get attribute
agent-browser get title               # Get page title
agent-browser get url                 # Get current URL
agent-browser get count <sel>         # Count matching elements
agent-browser get box <sel>           # Get bounding box
Check State
agent-browser is visible <sel>        # Check if visible
agent-browser is enabled <sel>        # Check if enabled
agent-browser is checked <sel>        # Check if checked
Find Elements (Semantic Locators)
agent-browser find role <role> <action> [value]       # By ARIA role
agent-browser find text <text> <action>               # By text content
agent-browser find label <label> <action> [value]     # By label
agent-browser find placeholder <ph> <action> [value]  # By placeholder
agent-browser find alt <text> <action>                # By alt text
agent-browser find title <text> <action>              # By title attr
agent-browser find testid <id> <action> [value]       # By data-testid
agent-browser find first <sel> <action> [value]       # First match
agent-browser find last <sel> <action> [value]        # Last match
agent-browser find nth <n> <sel> <action> [value]     # Nth match
Actions: click, fill, check, hover, text

### Examples

agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "<test@test.com>"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text

### Wait

agent-browser wait <selector>         # Wait for element to be visible
agent-browser wait <ms>               # Wait for time (milliseconds)
agent-browser wait --text "Welcome"   # Wait for text to appear
agent-browser wait --url "**/dash"    # Wait for URL pattern
agent-browser wait --load networkidle # Wait for load state
agent-browser wait --fn "window.ready === true"  # Wait for JS condition
