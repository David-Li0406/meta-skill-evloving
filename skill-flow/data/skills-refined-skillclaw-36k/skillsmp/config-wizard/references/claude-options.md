# Claude Code Configuration Reference

Complete reference for Claude Code CLI configuration options.

## Config File Locations

- **Global settings**: `~/.claude/settings.json`
- **Project settings**: `.claude/settings.json` (in project root)
- Project settings override global settings

## Settings Structure

```json
{
  "permissions": { },
  "env": { },
  "theme": "dark"
}
```

## Theme

```json
{
  "theme": "dark"
}
```

**Options:**
- `"dark"` - Dark color scheme
- `"light"` - Light color scheme
- `"system"` - Follow OS preference

## Permissions

### Tool-Based Permissions

Control which tools Claude can use without asking:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test)",
      "Bash(git status)",
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf)",
      "Bash(sudo *)"
    ]
  }
}
```

### Permission Patterns

**Exact match:**
```json
"Bash(npm test)"
```

**Wildcard patterns:**
```json
"Bash(npm run *)"
"Bash(git *)"
"Read(src/**)"
```

**Tool categories:**
```json
"Read"           // All file reads
"Write"          // All file writes
"Edit"           // All file edits
"Bash"           // All bash commands
"Glob"           // All glob searches
"Grep"           // All grep searches
"WebFetch"       // All web fetches
"WebSearch"      // All web searches
```

### Default Allow List (Commonly Used)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(yarn *)",
      "Bash(pnpm *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git branch *)",
      "Bash(ls *)",
      "Bash(pwd)",
      "Bash(which *)",
      "Bash(echo *)"
    ]
  }
}
```

### Restrictive Security Setup

```json
{
  "permissions": {
    "allow": [
      "Read(src/**)",
      "Read(tests/**)",
      "Read(*.json)",
      "Read(*.md)",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash",
      "Write",
      "Edit",
      "WebFetch",
      "WebSearch"
    ]
  }
}
```

## Environment Variables

Pass environment variables to Claude's tools:

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "true",
    "CUSTOM_VAR": "value"
  }
}
```

**Common use cases:**
- API keys for MCP servers
- Build configuration
- Feature flags

## MCP Servers

Configure Model Context Protocol servers in `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "gh",
      "args": ["mcp"],
      "env": {}
    },
    "database": {
      "command": "node",
      "args": ["/path/to/db-server.js"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### MCP Server Types

**Command-based (stdio):**
```json
{
  "server-name": {
    "command": "executable",
    "args": ["arg1", "arg2"],
    "env": { "KEY": "value" }
  }
}
```

**URL-based (SSE):**
```json
{
  "server-name": {
    "url": "https://mcp-server.example.com/sse",
    "headers": {
      "Authorization": "Bearer ${API_KEY}"
    }
  }
}
```

### Popular MCP Servers

**GitHub:**
```json
{
  "github": {
    "command": "gh",
    "args": ["mcp"]
  }
}
```

**Filesystem (sandboxed):**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-filesystem", "/allowed/path"]
  }
}
```

**PostgreSQL:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-postgres"],
    "env": {
      "POSTGRES_URL": "${POSTGRES_URL}"
    }
  }
}
```

## Model Configuration

Set in CLI flags or environment:

```bash
# Environment variable
export CLAUDE_MODEL=claude-sonnet-4-20250514

# CLI flag
claude --model claude-sonnet-4-20250514
```

**Available models:**
- `claude-sonnet-4-20250514` (default)
- `claude-opus-4-20250514`
- `claude-haiku-3-5-20241022`

## Hooks Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to modify file'",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Command executed'"
          }
        ]
      }
    ]
  }
}
```

### Hook Events

- `PreToolUse` - Before a tool is executed
- `PostToolUse` - After a tool completes
- `Stop` - When Claude stops generating
- `SubagentStop` - When a subagent completes
- `SessionStart` - When a session begins
- `SessionEnd` - When a session ends
- `UserPromptSubmit` - When user submits a prompt
- `PreCompact` - Before context compaction
- `Notification` - On notifications

### Hook Types

**Command hook:**
```json
{
  "type": "command",
  "command": "bash /path/to/script.sh",
  "timeout": 30
}
```

**Prompt hook (Claude processes result):**
```json
{
  "type": "prompt",
  "prompt": "Validate this file change follows our coding standards"
}
```

### Matcher Patterns

```json
"matcher": "Write"              // Exact tool match
"matcher": "Write|Edit"         // Multiple tools (OR)
"matcher": "Bash(npm *)"        // Tool with argument pattern
"matcher": "*"                  // All tools
```

## Example Complete Configuration

### Global (~/.claude/settings.json)

```json
{
  "theme": "dark",
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git *)",
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(ls *)",
      "Bash(pwd)",
      "Bash(which *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  },
  "mcpServers": {
    "github": {
      "command": "gh",
      "args": ["mcp"]
    }
  }
}
```

### Project (.claude/settings.json)

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run build)",
      "Bash(npm run lint)",
      "Write(src/**)",
      "Edit(src/**)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --fix",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## CLI Flags Reference

```bash
# Start with specific model
claude --model claude-opus-4-20250514

# Start in specific directory
claude --cwd /path/to/project

# Debug mode (verbose output)
claude --debug

# Load additional plugins
claude --plugin-dir /path/to/plugins

# Non-interactive mode
claude --print "your prompt here"

# Resume previous session
claude --resume

# Continue last conversation
claude --continue
```

## Directory Trust

Claude Code tracks trusted directories. When you first run Claude in a new directory, you'll be prompted to trust it. Trust settings are stored internally.

To reset trust:
```bash
# Remove trust for current directory
claude trust revoke .

# List trusted directories
claude trust list
```
