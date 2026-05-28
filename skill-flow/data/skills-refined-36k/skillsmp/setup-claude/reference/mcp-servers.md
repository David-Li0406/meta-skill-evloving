# MCP Servers Reference

This reference lists MCP servers with their configurations and context window impact.

## Core Principle

> **CLI-First**: Only use MCP when no CLI alternative exists.
> Each MCP adds tools to your context window.

---

## Quick Reference Table

| MCP | Tools | CLI Alternative | Recommendation |
|-----|-------|-----------------|----------------|
| context7 | ~5 | None | ✓ Use |
| shadcn | ~3 | None | ✓ Use if using shadcn/ui |
| filesystem | ~10 | Built-in Read/Write | Rarely needed |
| memory | ~5 | None | Optional |
| github | ~20 | `gh` | ✗ Use CLI |
| supabase | ~15 | `supabase` | ✗ Use CLI |
| stripe | ~15 | `stripe` | ✗ Use CLI |
| postgres | ~10 | `psql` | ✗ Use CLI |
| sqlite | ~8 | `sqlite3` | ✗ Use CLI |

---

## Recommended MCPs

### context7 - Framework Documentation

**Purpose**: Look up documentation for frameworks and packages.

**Configuration**:
```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/context7-mcp"]
  }
}
```

**Tools provided**: ~5
- resolve-library-id
- get-library-docs
- search-libraries

**When to use**: Any project using frameworks (Next.js, React, Vue, etc.)

**Alternative**: Web search (less efficient)

---

### shadcn - UI Component Documentation

**Purpose**: Look up shadcn/ui component documentation and examples.

**Configuration**:
```json
{
  "shadcn": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/shadcn-mcp"]
  }
}
```

**Tools provided**: ~3
- get-component
- list-components
- search-components

**When to use**: Projects using shadcn/ui

**Alternative**: Web search or reading source files

---

### memory - Persistent Memory

**Purpose**: Store information across sessions.

**Configuration**:
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  }
}
```

**Tools provided**: ~5
- store
- retrieve
- list
- delete

**When to use**: Long-running projects needing context persistence

**Alternative**: CLAUDE.md for project context

---

## Not Recommended MCPs

### github - GitHub Operations

**Why not**: The `gh` CLI is more powerful and adds zero context overhead.

```bash
# Instead of github MCP, use:
gh pr create
gh pr list
gh issue create
gh issue list
gh workflow run
gh api /repos/{owner}/{repo}/...
```

**If you must use it**:
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
    }
  }
}
```

---

### supabase - Database Operations

**Why not**: The `supabase` CLI handles all operations.

```bash
# Instead of supabase MCP, use:
supabase db push
supabase db pull
supabase gen types typescript
supabase functions deploy
```

---

### stripe - Payment Operations

**Why not**: The `stripe` CLI is comprehensive.

```bash
# Instead of stripe MCP, use:
stripe listen --forward-to localhost:3000/api/webhooks
stripe trigger payment_intent.succeeded
stripe customers list
stripe logs tail
```

---

### filesystem - File Operations

**Why not**: Claude Code has built-in Read/Write/Edit tools.

The filesystem MCP is only useful for accessing files outside the project directory, which is rarely needed.

---

## Configuration Patterns

### Minimal Setup (Recommended)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  },
  "disabledMcpServers": []
}
```

**Total tools**: ~5

---

### With UI Documentation

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    },
    "shadcn": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/shadcn-mcp"]
    }
  },
  "disabledMcpServers": []
}
```

**Total tools**: ~8

---

### With Memory (For Long Projects)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  },
  "disabledMcpServers": []
}
```

**Total tools**: ~10

---

### Migrating from Heavy MCP Usage

If you have many MCPs enabled:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  },
  "disabledMcpServers": [
    "github",
    "supabase",
    "stripe",
    "filesystem"
  ]
}
```

This preserves the config but disables them, making it easy to re-enable if needed.

---

## Environment Variables

Some MCPs require environment variables:

```json
{
  "mcpServers": {
    "example-mcp": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"],
      "env": {
        "API_KEY": "${EXAMPLE_API_KEY}",
        "SECRET": "${EXAMPLE_SECRET}"
      }
    }
  }
}
```

**Security note**: Store secrets in environment variables, not in the config file.

---

## Verifying MCP Setup

After configuring MCPs:

1. Restart Claude Code
2. Check that MCPs are loading (look for tool availability)
3. Test a tool from each enabled MCP

```bash
# Verify MCP config is valid JSON
cat .mcp.json | python -m json.tool

# Check if npx can find the packages
npx -y @anthropic-ai/context7-mcp --help
```

---

## Troubleshooting

### MCP Won't Load

1. Check JSON syntax: `cat .mcp.json | python -m json.tool`
2. Verify package exists: `npm view @package/name`
3. Check command is in PATH: `which npx`
4. Restart Claude Code

### Tools Not Appearing

1. MCP may be in `disabledMcpServers`
2. Package may have failed to install
3. Environment variables may be missing

### Performance Issues

1. Count total MCPs enabled
2. Calculate estimated tools
3. Disable unused MCPs
4. Prefer CLI for operations

---

## Context Window Budget

| Category | Recommended Max |
|----------|-----------------|
| Total MCPs | 10 |
| Total tools (MCPs + plugins) | 80 |
| Essential MCPs only | 2-3 |

**Formula**:
```
Safe = Base(25) + MCPs(~20) + Plugins(~15) = ~60 tools
Risky = Base(25) + MCPs(~50) + Plugins(~30) = ~105 tools
```
