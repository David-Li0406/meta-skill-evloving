# Configuration Deep Dive

Comprehensive guide to all Claude Code configuration files and options.

## Configuration File Hierarchy

Configuration files are loaded in order of precedence (higher overrides lower):

| Level | File | Scope |
|-------|------|-------|
| 1 (highest) | Enterprise managed policy | Organization-wide |
| 2 | `.claude/settings.local.json` | Local project overrides |
| 3 | `.claude/settings.json` | Project settings |
| 4 | `~/.claude/settings.json` | User settings |
| 5 (lowest) | Claude Code defaults | Built-in defaults |

## .claude/settings.json

The main project configuration file. Committed to version control.

### Complete Schema

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "env": {},
  "hooks": {},
  "mcpServers": {},
  "extraKnownMarketplaces": {},
  "apiKeyHelper": "",
  "webSecurity": {}
}
```

### Permission Configuration

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Bash(bun:*)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)",
      "Bash(chmod 777:*)",
      "Write(.env*)",
      "Edit(.env*)"
    ]
  }
}
```

### Environment Variables

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "app:*",
    "LOG_LEVEL": "debug"
  }
}
```

**Note:** These environment variables are set when Claude Code runs commands. Use `.claude/settings.local.json` for personal environment overrides.

### Hooks Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat \"$CLAUDE_PROJECT_DIR\"/.claude/context.md"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

### MCP Servers (Inline)

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "custom": {
      "command": "node",
      "args": ["./mcp/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### Extra Marketplaces

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    },
    "team-skills": {
      "source": {
        "source": "url",
        "url": "https://internal.company.com/plugins"
      }
    }
  }
}
```

### API Key Helper

```json
{
  "apiKeyHelper": "/path/to/key-rotation-script.sh"
}
```

Script receives JSON on stdin with `action: "get"` and should output the API key.

### Web Security

```json
{
  "webSecurity": {
    "allowedDomains": ["github.com", "*.internal.company.com"],
    "blockedDomains": ["*.phishing.com"]
  }
}
```

## .claude/settings.local.json

Personal project overrides. Add to `.gitignore`.

### Use Cases

1. **Personal permissions** - Allow tools you trust but team doesn't
2. **Local environment** - Set personal API keys, debug flags
3. **Development preferences** - Custom hooks for your workflow

### Example

```json
{
  "permissions": {
    "allow": [
      "Bash(docker:*)",
      "Bash(kubectl:*)"
    ]
  },
  "env": {
    "DEBUG": "true",
    "MY_API_KEY": "personal-key-here"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "say 'File saved'"
          }
        ]
      }
    ]
  }
}
```

## ~/.claude/settings.json

User-level settings. Applies to all projects.

### Recommended User Settings

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)"
    ],
    "deny": []
  },
  "env": {
    "EDITOR": "code"
  },
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

## .mcp.json

Shared MCP server configuration. Place in project root.

### Complete Schema

```json
{
  "mcpServers": {
    "server-name": {
      "command": "string",
      "args": ["array", "of", "args"],
      "env": {
        "ENV_VAR": "value",
        "SECRET": "${SECRET_FROM_ENV}"
      },
      "cwd": "/optional/working/directory"
    }
  }
}
```

### Common MCP Servers

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

### Environment Variable Interpolation

Use `${VAR_NAME}` syntax to reference environment variables:

```json
{
  "mcpServers": {
    "custom": {
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "API_URL": "${API_URL:-https://default.api.com}"
      }
    }
  }
}
```

**Note:** Variables must be set in your shell environment or in `.env` file.

## CLAUDE.md Files

### Root CLAUDE.md

Primary project knowledge file.

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

[Your project description]

## Development Commands

```bash
bun install          # Install dependencies
bun dev              # Start development server
bun test             # Run tests
bun build            # Build for production
bun lint             # Run linter
```

## Architecture

```
src/
├── api/             # API routes
├── components/      # React components
├── lib/             # Shared utilities
└── types/           # TypeScript types
```

## Code Style

- Use TypeScript for all new files
- Prefer for-loops over forEach
- Use Bun for package management
- Follow existing naming conventions

## Important Notes

- Never mock data in implementations
- Run tests before committing
- Use environment variables for secrets
```

### Subdirectory CLAUDE.md

Module-specific instructions.

```markdown
# src/api/CLAUDE.md

## API Guidelines

- All routes use tRPC
- Authentication via JWT middleware
- Validate all inputs with Zod
- Return consistent error shapes

## Route Structure

```typescript
// src/api/routes/example.ts
export const exampleRouter = router({
  list: publicProcedure.query(async () => { ... }),
  create: protectedProcedure.input(schema).mutation(async ({ input }) => { ... }),
});
```
```

### Personal Global CLAUDE.md

`~/.claude/CLAUDE.md` - Your preferences across all projects.

```markdown
# Personal CLAUDE.md

## Preferences

- Use Bun over npm
- Prefer for-loops over forEach
- Always run tests after changes
- Don't mock data - code should work first time

## Common Commands

- `/cost` - Display API usage costs
- `/compact` - Compress conversation context
```

## IDE-Specific Settings

### VS Code

Create `.vscode/settings.json`:

```json
{
  "claude.enabled": true,
  "claude.autoComplete": true,
  "files.exclude": {
    ".claude/settings.local.json": true
  }
}
```

### JetBrains IDEs

Create `.idea/claude.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ClaudeSettings">
    <option name="enabled" value="true" />
    <option name="projectRoot" value="$PROJECT_DIR$" />
  </component>
</project>
```

## Configuration Validation

### Validate JSON Syntax

```bash
# Validate settings files
jq . .claude/settings.json
jq . .claude/settings.local.json
jq . .mcp.json

# Check for common issues
claude config validate  # If available
```

### Check Loaded Configuration

```bash
# List all configuration
claude config list

# Check specific setting
claude config get permissions

# View MCP servers
claude mcp list
```

## Configuration Examples by Project Type

### Node.js/TypeScript Project

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(bun:*)", "Bash(npm:*)", "Bash(npx:*)",
      "Bash(node:*)", "Bash(tsx:*)",
      "Bash(git:*)",
      "Bash(prettier:*)", "Bash(eslint:*)"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)",
      "Write(.env*)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

### Python Project

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(python:*)", "Bash(python3:*)",
      "Bash(pip:*)", "Bash(uv:*)", "Bash(poetry:*)",
      "Bash(pytest:*)", "Bash(mypy:*)", "Bash(ruff:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)"
    ]
  },
  "env": {
    "PYTHONPATH": "src"
  }
}
```

### Full-Stack Project

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(bun:*)", "Bash(npm:*)",
      "Bash(docker:*)", "Bash(docker-compose:*)",
      "Bash(git:*)",
      "Bash(psql:*)", "Bash(redis-cli:*)"
    ],
    "deny": [
      "Bash(rm -rf /*))",
      "Bash(sudo:*)",
      "Bash(docker rm -f:*)"
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "DATABASE_URL": "postgres://localhost:5432/dev"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint-fix.sh"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting Configuration

| Issue | Cause | Solution |
|-------|-------|----------|
| Settings not loading | Invalid JSON | Run `jq . file.json` to validate |
| Permission denied | Missing allow rule | Add to `permissions.allow` |
| MCP server not starting | Missing env var | Check `${VAR}` references |
| Hooks not running | Script not executable | Run `chmod +x script.sh` |
| Local settings ignored | Wrong filename | Must be `settings.local.json` |
| CLAUDE.md not read | Wrong location | Must be in cwd or project root |
