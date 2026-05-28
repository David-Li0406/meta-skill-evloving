---
name: create-playwright-mcp
description: Sets up Playwright MCP server integration for Claude Code. Use when setting up Playwright, browser automation, web testing, scraping, or adding browser control capabilities.
allowed-tools: Bash, Read, Write, AskUserQuestion, Glob
---

# Create Playwright MCP Integration

## Purpose

Guide users through setting up a Playwright MCP server to enable Claude Code to interact with browsers for web automation, testing, and scraping.

## Instructions

### 1. Check Prerequisites

Verify Node.js is installed (v18+ required):
```bash
node --version
```

### 2. Install Playwright Browsers

Playwright requires browser binaries to be installed:

```bash
npx playwright install
```

This installs Chromium, Firefox, and WebKit browsers. For a smaller installation, you can install only specific browsers:
```bash
npx playwright install chromium  # Chromium only
npx playwright install firefox   # Firefox only
npx playwright install webkit    # WebKit only
```

### 3. Register the MCP Server

Add the official Microsoft Playwright MCP server to Claude Code using npx (no local installation needed):

```bash
claude mcp add playwright -s project -- npx @playwright/mcp@latest
```

### 4. Display Restart Notice

**IMPORTANT**: After completing all setup steps, you MUST display this notice to the user:

```
================================================
  RESTART REQUIRED
================================================
  The Playwright MCP server has been configured.

  Please restart Claude Code for the MCP
  server to be registered and available.

  After restarting:
  1. Run /mcp to verify the server is connected
  2. Test with: "Navigate to google.com and take a screenshot"
================================================
```

This notice is critical because MCP servers are only loaded when Claude Code starts.

## Output Format

Provide step-by-step guidance with commands the user can copy and run. After each step, confirm success before proceeding.

**Always end with the restart notice** - this is mandatory to ensure users know to restart Claude Code.

## Troubleshooting

**Browser installation failed:**
- Ensure you have sufficient disk space (browsers require ~500MB each)
- On Linux, install dependencies: `npx playwright install-deps`
- Try installing a single browser: `npx playwright install chromium`

**Node.js issues:**
- Ensure Node.js v18+ is installed
- Run `node --version` to verify

**MCP not connecting:**
- Restart Claude Code after adding the server
- Check `/mcp` shows the playwright server as connected
- Verify npx can run: `npx @playwright/mcp@latest --help`

**Browser crashes or timeouts:**
- Increase timeout settings if pages are slow to load
- Use headless mode (default) for better stability
- Check system resources (memory, CPU)

## Best Practices

- Use headless mode for automated tasks (default behavior)
- Set appropriate timeouts for page loads and actions
- Clean up browser sessions after use
- Test with simple navigation first before complex interactions
- Consider using specific browsers for compatibility testing

## Capabilities

Once set up, the Playwright MCP enables Claude to:
- Navigate to URLs and interact with web pages
- Take screenshots and capture page content
- Fill forms and click buttons
- Extract text and data from pages
- Wait for elements and handle dynamic content
- Execute JavaScript in page context

## Example

**User**: "Set up Playwright MCP for my project"

**Response**:
1. Verify Node.js v18+ is installed
2. Install Playwright browsers via `npx playwright install`
3. Register the MCP server with `claude mcp add playwright -s project -- npx @playwright/mcp@latest`
4. Display the RESTART REQUIRED notice prominently
