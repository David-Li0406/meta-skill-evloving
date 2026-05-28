---
name: chrome-devtools-mcp
description: Use this skill when you need to automate browser tasks, debug web applications, take screenshots, evaluate JavaScript, inspect network requests, or interact with Chrome DevTools programmatically.
---

# Chrome DevTools MCP Skill

## Overview

This skill allows you to control and inspect a live Chrome browser using the Chrome DevTools MCP. It provides a comprehensive set of tools for browser automation, debugging, performance analysis, and network inspection.

## When to Use This Skill

- **Browser Automation**: Automate repetitive tasks like navigation, clicking elements, and filling forms.
- **Debugging**: Inspect console messages, evaluate JavaScript, and analyze network requests.
- **Performance Analysis**: Record and analyze performance traces to identify bottlenecks.
- **Visual Inspection**: Capture screenshots or text snapshots of web pages.
- **Network Analysis**: Inspect API calls and responses for debugging purposes.

## Quick Start Workflow

1. **Setup**: Ensure the Chrome DevTools MCP server is installed and running.
   ```bash
   # macOS
   brew tap f/mcptools
   brew install mcp

   # Windows/Linux
   go install github.com/f/mcptools/cmd/mcptools@latest
   ```

2. **Navigate to a Page**:
   ```bash
   mcp__chrome-devtools__navigate_page({ url: "https://example.com" })
   ```

3. **Inspect Console Messages**:
   ```bash
   mcp__chrome-devtools__list_console_messages({ pageIdx: 0 })
   ```

4. **Capture a Screenshot**:
   ```bash
   mcp__chrome-devtools__take_screenshot({
     format: "png",
     fullPage: true,
     filePath: "./screenshot.png"
   })
   ```

5. **Evaluate JavaScript**:
   ```bash
   mcp__chrome-devtools__evaluate_script({ function: "() => document.title" })
   ```

## Core Tools

### Page Management
- **list_pages**: Get all open pages.
- **select_page**: Select a page for operations.
- **new_page**: Create a new page.
- **close_page**: Close a page.
- **navigate_page**: Navigate to a specific URL or reload.

### Debugging & Inspection
- **take_snapshot**: Get a text-based accessibility tree.
- **get_console_logs**: Retrieve console output.
- **get_network_logs**: Analyze network requests with full details.

### Performance
- **start_profiling**: Begin CPU profiling.
- **stop_profiling**: End profiling and get data.

### Input & Interaction
- **click**: Click on an element.
- **fill**: Fill input fields.
- **hover**: Hover over an element.

## Best Practices
- Always wait for operations to complete before proceeding to the next step.
- Inspect elements manually before automating to ensure selectors are correct.
- Document findings with screenshots and logs for future reference.

## Notes
- This skill is designed for use with the latest version of Chrome and requires Node.js.
- Ensure that the MCP server is running to execute commands successfully.