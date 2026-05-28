# CLI Reference

## Global Flags

```bash
-p <profile>, --profile=<profile>   # Use specific profile
--json                               # JSON output
-q, --quiet                          # Minimal output
```

## Commands

### add

```bash
agent-deck add [path] [options]
```

| Flag | Description |
|------|-------------|
| `-t, --title` | Session title |
| `-g, --group` | Group path |
| `-c, --cmd` | Command (claude, gemini, etc.) |
| `--parent` | Parent session (creates child) |
| `--mcp` | Attach MCP (repeatable) |

```bash
agent-deck add -t "My Project" -c claude .
agent-deck add -t "Child" --parent "Parent" -c claude /tmp/x
agent-deck add -t "Research" -c claude --mcp exa --mcp firecrawl /tmp/r
```

### session

```bash
agent-deck session <command> [options] <name>
```

| Command | Description |
|---------|-------------|
| `start` | Start session (creates tmux) |
| `stop` | Stop session |
| `restart` | Restart (reloads MCPs) |
| `attach` | Attach to tmux (Ctrl+Q to detach) |
| `send "msg"` | Send message |
| `output` | Get last response |
| `show` | Show details |
| `current` | Detect current session |
| `fork` | Fork Claude session |

```bash
agent-deck session start "My Project"
agent-deck session send "My Project" "Hello"
agent-deck session output "My Project"
agent-deck session current -q              # Just name
agent-deck session current --json          # Full JSON
```

### mcp

```bash
agent-deck mcp <command> [options]
```

| Command | Description |
|---------|-------------|
| `list` | Show available MCPs |
| `attached <name>` | Show attached MCPs |
| `attach <name> <mcp>` | Attach MCP |
| `detach <name> <mcp>` | Detach MCP |

**Note:** Run `session restart` after attach/detach.

### group

```bash
agent-deck group <command> [options]
```

| Command | Description |
|---------|-------------|
| `list` | List groups |
| `create <name>` | Create group |
| `delete <name>` | Delete group |
| `move <session> <group>` | Move session |

### Other

```bash
agent-deck list [--json]     # List sessions
agent-deck status [-v|-q]    # Status summary
agent-deck remove <name>     # Remove session
```

## Session Resolution

Commands accept:
- **Title:** `"My Project"`
- **ID prefix:** `abc123` (≥6 chars)
- **Path:** `/path/to/project`

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |
| 2 | Not found |
