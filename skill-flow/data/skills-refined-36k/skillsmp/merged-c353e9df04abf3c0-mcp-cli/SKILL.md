---
name: mcp-cli
description: Use this skill when you need to interact with external tools, APIs, or data sources through MCP (Model Context Protocol) servers via the command line.
---

# MCP-CLI

Access MCP servers through the command line. MCP enables interaction with external systems like GitHub, filesystems, databases, and APIs.

## Commands

| Command                            | Output                          |
| ---------------------------------- | ------------------------------- |
| `mcp-cli`                          | List all servers and tool names |
| `mcp-cli info <server>`           | Show tools with parameters      |
| `mcp-cli info <server> <tool>`    | Get tool JSON schema            |
| `mcp-cli call <server> <tool>`    | Call tool (reads JSON from stdin if no args) |
| `mcp-cli call <server> <tool> '<json>'` | Call tool with arguments        |
| `mcp-cli grep "<pattern>"`         | Search tools by name            |

**Add `-d` to include descriptions** (e.g., `mcp-cli info filesystem -d`)

## Workflow

1. **Discover**: `mcp-cli` → see available servers and tools
2. **Explore**: `mcp-cli info <server>` → see tools with parameters
3. **Inspect**: `mcp-cli info <server> <tool>` → get full JSON input schema
4. **Execute**: `mcp-cli call <server> <tool> '<json>'` → run with arguments

## Examples

```bash
# List all servers and tool names
mcp-cli

# See all tools with parameters
mcp-cli info filesystem

# Get JSON schema for specific tool
mcp-cli info filesystem/read_file

# Call the tool
mcp-cli call filesystem/read_file '{"path": "./README.md"}'

# Search for tools
mcp-cli grep "*file*"

# JSON output for parsing
mcp-cli call filesystem/read_file '{"path": "./README.md"}' --json

# Complex JSON with quotes (use heredoc or stdin)
mcp-cli call server/tool <<EOF
{"content": "Text with 'quotes' inside"}
EOF

# Or pipe from a file/command
cat args.json | mcp-cli call server/tool

# Find all TypeScript files and read the first one
mcp-cli call filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli call filesystem/read_file "{\"path\": \"{}\"}"'
```

## Options

| Flag         | Purpose                   |
| ------------ | ------------------------- |
| `-j, --json` | JSON output for scripting |
| `-r, --raw`  | Raw text content          |
| `-d`         | Include descriptions      |
| `-c <path>`  | Specify config file      |

## Exit Codes

- `0`: Success
- `1`: Client error (bad args, missing config)
- `2`: Server error (tool failed)
- `3`: Network error

## Common Errors

| Wrong Command | Error | Fix |
|---------------|-------|-----|
| `mcp-cli server tool` | AMBIGUOUS_COMMAND | Use `call server tool` or `info server tool` |
| `mcp-cli run server tool` | UNKNOWN_SUBCOMMAND | Use `call` instead of `run` |
| `mcp-cli list` | UNKNOWN_SUBCOMMAND | Use `info` instead of `list` |
| `mcp-cli call server` | MISSING_ARGUMENT | Add tool name |
| `mcp-cli call server tool {bad}` | INVALID_JSON | Use valid JSON with quotes |