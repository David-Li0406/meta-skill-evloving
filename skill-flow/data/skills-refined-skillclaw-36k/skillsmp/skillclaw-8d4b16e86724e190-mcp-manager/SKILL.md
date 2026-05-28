---
name: mcp-manager
description: Use this skill when you need a conversational interface to manage MCP (Model Context Protocol) server configurations.
---

# MCP Manager Skill

## Overview

Natural language interface to the MCP Manager CLI tool for managing Model Context Protocol server configurations. Users can interact conversationally, e.g., "enable the filesystem MCP", "add a database server", "show me all my MCPs".

## Activation

Activates on MCP keywords within a 3-message window or explicit invocation: `/mcp-manager`.

## Commands

### 1. List MCPs
Display all configured MCP servers with status.
- **User Input:** "List all my MCPs" / "Show me my MCP servers"
- **CLI Command:** `python3 -m mcp-manager.cli list`

### 2. Enable MCP
Activate a disabled MCP server.
- **User Input:** "Enable the filesystem MCP" / "Turn on puppeteer"
- **CLI Command:** `python3 -m mcp-manager.cli enable <server-name>`

### 3. Disable MCP
Deactivate an MCP server without removing it. Requires confirmation.
- **User Input:** "Disable the puppeteer MCP" / "Turn off github"
- **CLI Command:** `python3 -m mcp-manager.cli disable <server-name>`

### 4. Add MCP
Add a new MCP server interactively (collects name, command, args, env vars).
- **User Input:** "Add a new MCP server" / "Configure a database MCP"
- **CLI Command:** `python3 -m mcp-manager.cli add <name> <command> [args...] --env KEY=VALUE`

### 5. Remove MCP
Delete MCP server configuration completely. Requires confirmation with warning.
- **User Input:** "Remove the puppeteer MCP" / "Delete the old-server"
- **CLI Command:** `python3 -m mcp-manager.cli remove <server-name>`

### 6. Show MCP
Display detailed information for a specific MCP server.
- **User Input:** "Show me the filesystem MCP" / "Details for github server"
- **CLI Command:** `python3 -m mcp-manager.cli show <server-name>`

### 7. Validate MCPs
Check all MCP configurations for errors.
- **User Input:** "Validate my MCP configuration" / "Check for MCP errors"
- **CLI Command:** `python3 -m mcp-manager.cli validate`

### 8. Export MCPs
Export configurations to a JSON file for backup.
- **User Input:** "Export my MCP configuration" / "Back up my MCPs"
- **CLI Command:** `python3 -m mcp-manager.cli export [output-file]`

### 9. Import MCPs
Import configurations from a JSON file.
- **User Input:** "Import MCPs from backup.json" / "Restore my MCPs"
- **CLI Command:** `python3 -m mcp-manager.cli import [input-file]`