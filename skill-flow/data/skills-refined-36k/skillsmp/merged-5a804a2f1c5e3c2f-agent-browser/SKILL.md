---
name: agent-browser
description: Use this skill for headless browser automation to navigate, interact with web pages, and extract data via structured commands.
---

# Agent Browser

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

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
agent-browser open <url>            # Navigate to page
agent-browser snapshot -i           # Get interactive elements with refs
agent-browser click @e2             # Click element by ref
agent-browser fill @e3 "text"       # Fill input by ref
agent-browser get text @e1          # Get element text
agent-browser screenshot path.png    # Save screenshot to file
agent-browser close                 # Close browser
```

## Core Commands

### Navigation

```bash
agent-browser open <url>            # Navigate to URL
agent-browser back                   # Go back
agent-browser forward                # Go forward
agent-browser reload                 # Reload page
```

### Interaction

```bash
agent-browser click <selector>       # Click element
agent-browser fill <selector> <text> # Fill input field
agent-browser check <selector>       # Check checkbox
agent-browser uncheck <selector>     # Uncheck checkbox
agent-browser select <selector> <value> # Select dropdown
```

### Extraction and Info

```bash
agent-browser snapshot                # Take a snapshot of the page
agent-browser get text <selector>     # Get text of an element
agent-browser get html <selector>     # Get innerHTML of an element
agent-browser get value <selector>    # Get value of an input
agent-browser screenshot [path]       # Take a screenshot
agent-browser pdf <path>              # Save as PDF
```

### Check State

```bash
agent-browser is visible <selector>   # Check if element is visible
agent-browser is enabled <selector>   # Check if element is enabled
agent-browser is checked <selector>   # Check if checkbox is checked
```

### Wait and Timing

```bash
agent-browser wait <selector>         # Wait for an element
agent-browser wait <ms>                # Wait for milliseconds
agent-browser wait --text "Success"   # Wait for specific text
agent-browser wait --load networkidle   # Wait for network to be idle
```

### Advanced Control

```bash
agent-browser scroll <direction> [px] # Scroll page
agent-browser eval <js>                # Execute JavaScript
agent-browser cookies                  # Manage cookies
agent-browser storage local            # Access local storage
```

## Sessions

Run multiple isolated browser instances.

```bash
agent-browser --session <name> open <url>  # Open a new session
```

## Snapshot Options

The snapshot command supports filtering to reduce output size.

```bash
agent-browser snapshot -i                # Interactive elements only
agent-browser snapshot -c                 # Compact output
agent-browser snapshot -d <depth>         # Limit depth
agent-browser snapshot -s <selector>      # Scope to CSS selector
```

## Selectors and Refs

Refs provide deterministic element selection from snapshots. Use the `@ref` syntax.

```bash
agent-browser snapshot                    # Take a snapshot
agent-browser click @e2                   # Click using ref
```

## Troubleshooting

- If the command is not found on Linux ARM64, use the full path in the bin folder.
- If an element is not found, use snapshot to find the correct ref.
- If the page is not loaded, add a wait command after navigation.
- Use `--headed` to see the browser window for debugging.

## Options

- `--session <name>` uses an isolated session.
- `--json` provides JSON output.
- `--full` takes a full page screenshot.
- `--headed` shows the browser window.
- `--timeout <ms>` sets the command timeout in milliseconds.

## Notes

- Refs are stable per page load but change on navigation.
- Always snapshot after navigation to get new refs.
- Use fill instead of type for input fields to ensure existing text is cleared.