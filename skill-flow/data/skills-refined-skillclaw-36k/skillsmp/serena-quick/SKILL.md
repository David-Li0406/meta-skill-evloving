---
name: serena-quick
description: Quick code exploration using Serena MCP. Use for small-scale tasks like checking single file structure, finding a specific symbol, or quick reference lookup. No subagent - runs in main context for efficiency.
---

# Serena Quick Skill

Lightweight code exploration using Serena MCP tools directly in main context.

## When to Use

- Check structure of a single file
- Find a specific function/class/symbol
- Quick reference lookup (who calls this?)
- Read or update project memory

## MCP Tools (load via ToolSearch first)

**IMPORTANT: Load Serena tools before use:**
```
ToolSearch query: "serena"
```

### Core Tools
| Tool | Use Case |
|------|----------|
| `mcp__serena__get_symbols_overview` | File structure overview |
| `mcp__serena__find_symbol` | Find specific symbol by name |
| `mcp__serena__find_referencing_symbols` | Who uses this symbol? |
| `mcp__serena__read_file` | Read file content |
| `mcp__serena__list_dir` | Directory listing |

### Memory Tools
| Tool | Use Case |
|------|----------|
| `mcp__serena__read_memory` | Retrieve stored knowledge |
| `mcp__serena__write_memory` | Store new knowledge |
| `mcp__serena__list_memories` | List all memories |

## Workflow

1. Load Serena MCP: `ToolSearch query: "serena"`
2. Execute the appropriate tool for the task
3. Return results directly (no summarization needed)

## Task: $ARGUMENTS

Quick exploration request:

$ARGUMENTS

Load Serena MCP and execute the minimal set of tools needed.
