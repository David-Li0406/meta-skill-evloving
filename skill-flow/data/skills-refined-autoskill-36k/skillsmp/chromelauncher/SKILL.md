---
name: ChromeLauncher
description: Launch Chrome for browser automation. USE WHEN mcp__claude-in-chrome tools fail with "extension not connected", or before any browser automation task.
allowed-tools:
  - Bash
---

# ChromeLauncher - Chrome Extension Launcher

Ensures Chrome is running and the Claude in Chrome extension is connected before browser automation tasks.

## When to Use

**Invoke this skill when:**
- `mcp__claude-in-chrome__tabs_context_mcp` returns "Browser extension is not connected"
- Starting a browser automation session
- Chrome was closed and needs to be relaunched

## Quick Command

```bash
~/.claude/skills/ChromeLauncher/launch-chrome.sh
```

**Actions:**
- `ensure` (default) - Launch Chrome if needed, wait for extension
- `status` - Check Chrome and extension status
- `launch` - Just launch Chrome, don't wait
- `wait` - Wait for extension to connect

## Workflow

1. Run the launch script with `ensure` action
2. Script checks if Chrome is running
3. If not, launches Chrome in background
4. Waits up to 30 seconds for extension socket at `/tmp/claude-mcp-browser-bridge-$USER`
5. Returns "ready" on success, "timeout" on failure

## Environment Variables

- `CHROME_CMD` - Chrome binary to use (default: `google-chrome-stable`)

## Integration Pattern

Before using Chrome MCP tools:

```
1. Try mcp__claude-in-chrome__tabs_context_mcp
2. If "not connected" → Run launch-chrome.sh ensure
3. Retry mcp__claude-in-chrome__tabs_context_mcp
```
