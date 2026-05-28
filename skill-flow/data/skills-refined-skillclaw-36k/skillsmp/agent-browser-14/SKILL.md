---
name: agent-browser
description: Agent Browser Skill
---

# Agent Browser Skill

## Overview

Agent Browser is a headless browser automation CLI designed specifically for AI agents. It provides fast, deterministic browser control with an AI-friendly interface using element references (refs) for reliable interaction.

## Key Features

- **AI-First Design**: Uses accessibility tree with refs for deterministic element selection
- **Fast Performance**: Native Rust CLI with Node.js daemon architecture
- **Comprehensive**: 50+ commands for complete browser automation
- **Cross-Platform**: Works on macOS, Linux, Windows
- **Session Management**: Multiple isolated browser instances
- **JSON Output**: Machine-readable responses for AI integration

## Installation

```bash
npm install -g agent-browser
```

## Core Workflow

### 1. Basic AI Agent Pattern
```bash
# Navigate to page
agent-browser open example.com

# Get accessibility tree with refs (AI-friendly)
agent-browser snapshot -i --json

# Parse output to identify target refs
# Example output:
# - heading "Welcome" [ref=e1]
# - link "Click me" [ref=e2]
# - input "Email" [ref=e3]

# Execute actions using refs
agent-browser click @e2
agent-browser fill @e3 "user@example.com"

# Get updated snapshot after page changes
agent-browser snapshot -i --json

# Close browser
agent-browser close
```

### 2. Traditional Selectors (Alternative)
```bash
# CSS selectors
agent-browser click "#submit-button"
agent-browser fill "#email-input" "user@example.com"

# Semantic locators
agent-browser find role button click --name "Submit"
agent-browser find label "Email" fill "user@example.com"
```

## Essential Commands

### Navigation
```bash
agent-browser open <url>              # Navigate to URL
agent-browser back                    # Go back
agent-browser forward                 # Go forward  
agent-browser reload                  # Reload page
agent-browser close                   # Close browser
```

### Page Interaction
```bash
agent-browser click <selector>        # Click element
agent-browser fill <sel> <text>       # Clear and fill input
agent-browser type <sel> <text>       # Type without clearing
agent-browser press <key>            # Press key (Enter, Tab, etc)
agent-browser scroll <dir> [px]      # Scroll direction
agent-browser screenshot [path]      # Take screenshot
```

### Information Gathering
```bash
agent-browser snapshot                # Get accessibility tree with refs
agent-browser get text <sel>         # Get element text
agent-browser get html <sel>         # Get innerHTML
agent-browser get title               # Get page title
agent-browser get url                 # Get current URL
```

### State Checking
```bash
agent-browser is visible <sel>        # Check if visible
agent-browser is enabled <sel>        # Check if enabled
agent-browser wait <selector>         # Wait for element
agent-browser wait --text "Welcome"   # Wait for text to appear
```

## Integration Patterns

### With AG4ONE Workflow

1. **Discovery Phase**: Use browser automation to research web applications
2. **Requirements Gathering**: Extract data from web forms and interfaces
3. **Testing**: Automate browser-based testing workflows
4. **Documentation**: Capture screenshots and gather information

### Error Handling

```bash
# Check if element exists before interaction
if agent-browser is visible @e5 --json | grep -q "true"; then
    agent-browser click @e5
else
    echo "Element not found"
fi
# Wait for page load before proceeding
agent-browser wait --load networkidle
agent-browser wait --text "Page loaded"
```

### Session Management

```bash
# Save authentication state
agent-browser state save auth-state.json

# Load state in new session
agent-browser open example.com
agent-browser state load auth-state.json
```

## Best Practices

1. **Always use refs** from snapshot for reliable interaction
2. **Wait for page stability** before taking actions
3. **Use JSON output** for machine-readable responses
4. **Save state** when dealing with authentication
5. **Handle errors** gracefully with state checking
6. **Close browsers** to free resources

## Advanced Features

### Network Control
```bash
# Block requests
agent-browser network route "ads/*" --abort

# Mock responses
agent-browser network route "/api/data" --body '{"mock": true}'
```

### Device Emulation
```bash
# Mobile device
agent-browser set device "iPhone 14"

# Custom viewport
agent-browser set viewport 375 812
```

### Multi-tab Management
```bash
agent-browser tab new https://example.com
agent-browser tab 1  # Switch to second tab
agent-browser tab close 1
```

## Example Use Cases

### Web Form Automation
```bash
agent-browser open "https://example.com/login"
agent-browser snapshot -i --json
# Parse refs for username, password, submit
agent-browser fill @e3 "username"
agent-browser fill @e4 "password"
agent-browser click @e5
agent-browser wait --text "Dashboard"
```

### Data Extraction
```bash
agent-browser open "https://example.com/data"
agent-browser snapshot -i --json
# Extract all links with specific text
agent-browser get text "[data-row]" --json
```

### Visual Testing
```bash
agent-browser open "https://example.com"
agent-browser set viewport 1920 1080
agent-browser screenshot desktop-view.png
agent-browser set device "iPhone 14"
agent-browser screenshot mobile-view.png
```

## Troubleshooting

### Common Issues
1. **Element not found**: Use updated snapshot after page changes
2. **Timing issues**: Add explicit waits before interactions
3. **Selector conflicts**: Use unique refs from snapshot
4. **Authentication**: Save and load state for logged-in sessions

### Debug Commands
```bash
agent-browser highlight @e5         # Highlight element
agent-browser console               # View console messages
agent-browser errors                # View page errors
```

This skill enables AI agents to reliably interact with web browsers for testing, automation, and data gathering tasks within the AG4ONE workflow.