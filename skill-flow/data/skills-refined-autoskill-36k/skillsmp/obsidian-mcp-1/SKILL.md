---
name: obsidian-mcp
description: Provides access to Obsidian vault notes through MCP (Model Context Protocol) tools. Use this skill when the user needs to interact with their Obsidian knowledge base, including reading notes, creating new notes, updating content, searching vault contents, or any knowledge management tasks involving Obsidian. If tools are not available, instructs the user to enable them manually.
---

# Obsidian MCP Integration

Provides access to Obsidian vault operations through MCP (Model Context Protocol) tools for knowledge management tasks.

## Purpose

This skill enables interaction with Obsidian vaults when the MCP server is properly configured. The Obsidian MCP tools must be manually enabled by the user in the GitHub Copilot Chat interface.

## When to Use

Use this skill when the user needs to:

- **Read or search notes** in their Obsidian vault
- **Create new notes** with structured content
- **Update or modify** existing notes
- **Query knowledge** stored in Obsidian
- **Manage tags, links**, or vault structure
- **Work with daily notes** or templates

Do NOT use for general coding tasks, file operations outside Obsidian, or when the user hasn't mentioned their knowledge base.

## Checking Tool Availability

### Method 1: Context Analysis (Preferred)

Check if Obsidian MCP tools are available by examining the tools listed in the system context. Look for tools like:
- `search_notes`
- `read_note`
- `create_note`
- `update_note`
- `list_notes`
- `get_tags`
- `get_backlinks`

If these tools are NOT present in your available tools, the MCP server is not active.

### Method 2: Status Script

Run the status check script to verify MCP configuration:

```powershell
powershell -ExecutionPolicy Bypass -File .github/skills/obsidian-mcp/scripts/check_mcp_status.ps1
```

This shows whether the MCP server is configured in `.vscode/mcp.json`, but does NOT indicate if tools are active.

## Workflow

### When Tools Are Available

1. User requests Obsidian-related task
2. Verify tools are available in context
3. Proceed with operations using MCP tools

### When Tools Are NOT Available

1. User requests Obsidian-related task
2. Check context - tools not found
3. Inform user: 
   ```
   The Obsidian MCP tools are not currently active. To enable them:
   
   1. In GitHub Copilot Chat, click the "+" button to add tools
   2. Look for and enable the "obsidian" MCP server tools
   3. The server is already configured in .vscode/mcp.json
   
   Once enabled, I can help you with your Obsidian vault operations.
   ```

## Available MCP Tools

When enabled, the Obsidian MCP provides:

- **search_notes** - Search vault by content or metadata
- **read_note** - Read specific note content
- **create_note** - Create new note with content
- **update_note** - Modify existing note
- **list_notes** - List all notes in vault
- **get_tags** - Retrieve all tags
- **get_backlinks** - Find notes linking to a note

## Best Practices

1. **Check context first** - Verify tools are available before attempting operations
2. **Clear instructions** - Give users specific steps to enable tools
3. **Batch operations** - Complete all vault tasks in one session
4. **Graceful degradation** - If tools unavailable, provide alternative suggestions

## Configuration

The MCP server is configured in `.vscode/mcp.json`:
- **Vault path**: `C:\Users\Renato Augusto\Documents\Obsidian Vault\Psicodelila`
- **MCP package**: `@mauricio.wolff/mcp-obsidian@latest`
- **Server name**: `obsidian`

Users must manually enable the tools in Copilot Chat to activate them.
