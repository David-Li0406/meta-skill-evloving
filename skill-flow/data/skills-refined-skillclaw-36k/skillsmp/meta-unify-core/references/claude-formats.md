---
source: ClaudeDocs
last_updated: 2025-01-09
plugin_version: 1.0.0
---

# Claude Code Configuration Formats Reference

Complete specification for all Claude Code configuration formats.

---

## 1. MCP Server Configuration

### File Locations

| Scope | Location | Description |
|:------|:---------|:------------|
| User | `~/.claude.json` under `mcpServers` | Personal servers across all projects |
| Local | `~/.claude.json` under project paths | Personal servers for specific project |
| Project | `.mcp.json` in project root | Team-shared servers (committed to git) |
| Managed | System `managed-mcp.json` | IT-deployed servers |

**Managed paths:**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

### STDIO Server Schema

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "/path/to/executable",
      "args": ["--flag", "value"],
      "env": {
        "API_KEY": "${API_KEY}",
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      },
      "cwd": "/optional/working/directory"
    }
  }
}
```

### HTTP Server Schema

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

### SSE Server Schema (Deprecated)

```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse",
      "url": "https://api.example.com/sse",
      "headers": {
        "X-API-Key": "${API_KEY}"
      }
    }
  }
}
```

### Environment Variable Syntax

- `${VAR}` - Expands to value of VAR
- `${VAR:-default}` - Uses default if VAR not set
- Supported in: `command`, `args`, `env`, `url`, `headers`

### Plugin MCP Servers

In `.mcp.json` at plugin root or inline in `plugin.json`:

```json
{
  "mcpServers": {
    "plugin-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DATA_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### Managed MCP Allowlist/Denylist

In `managed-settings.json`:

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": ["npx", "-y", "@approved/package"] },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "blocked-server" },
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

---

## 2. Skills Configuration

### File Location

| Scope | Path |
|:------|:-----|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `.claude/skills/<skill-name>/SKILL.md` |
| Plugin | `<plugin-root>/skills/<skill-name>/SKILL.md` |
| Managed | See IAM managed settings |

### SKILL.md YAML Frontmatter Schema

```yaml
---
# REQUIRED FIELDS
name: skill-name                    # Max 64 chars, lowercase letters/numbers/hyphens only
description: What this skill does   # Max 1024 chars, used for discovery

# OPTIONAL FIELDS
allowed-tools: Read, Grep, Glob     # Tools Claude can use without permission
# OR as YAML list:
allowed-tools:
  - Read
  - Grep
  - Glob

model: claude-sonnet-4-20250514     # Override model for this skill

context: fork                       # Run in isolated sub-agent context

agent: Explore                      # Agent type when context: fork
                                    # Options: Explore, Plan, general-purpose, or custom agent name

user-invocable: true                # Show in slash command menu (default: true)

disable-model-invocation: false     # Block programmatic invocation via Skill tool

hooks:                              # Skill-scoped hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true                # Run only once per session
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  Stop:
    - hooks:
        - type: prompt
          prompt: "Check if task is complete"
---
```

### Validation Rules

**name:**
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- Cannot contain: "anthropic", "claude"

**description:**
- Non-empty
- Max 1024 characters
- No XML tags
- Write in third person

### Directory Structure

```
skill-name/
├── SKILL.md              # Required - main instructions
├── reference.md          # Optional - detailed docs (loaded on demand)
├── examples.md           # Optional - usage examples
└── scripts/
    ├── helper.py         # Utility scripts (executed, not loaded)
    └── validate.sh
```

### Best Practices

- Keep SKILL.md body under 500 lines
- Use progressive disclosure - link to reference files
- Keep references one level deep from SKILL.md
- Use forward slashes in all paths
- Scripts should handle errors explicitly

---

## 3. Hooks Configuration

### File Locations

| Scope | Location |
|:------|:---------|
| User | `~/.claude/settings.json` under `hooks` |
| Project | `.claude/settings.json` under `hooks` |
| Local | `.claude/settings.local.json` under `hooks` |
| Plugin | `hooks/hooks.json` or inline in `plugin.json` |
| Managed | `managed-settings.json` |

### Complete Hooks Schema

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-handler.sh"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "permission_prompt|idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Notification'"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if subagent completed task: $ARGUMENTS"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "manual|auto",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/pre-compact.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/session-start.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/session-end.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Events

| Event | Matchers | Description |
|:------|:---------|:------------|
| PreToolUse | Tool names: `Bash`, `Write`, `Edit`, `Read`, `Glob`, `Grep`, `Task`, `WebFetch`, `WebSearch` | Before tool execution |
| PostToolUse | Same as PreToolUse | After successful tool execution |
| PermissionRequest | Same as PreToolUse | When permission dialog shown |
| Notification | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` | When notification sent |
| UserPromptSubmit | None (omit matcher) | When user submits prompt |
| Stop | None (omit matcher) | When main agent finishes |
| SubagentStop | None (omit matcher) | When subagent finishes |
| PreCompact | `manual`, `auto` | Before compact operation |
| SessionStart | `startup`, `resume`, `clear`, `compact` | At session start |
| SessionEnd | None (omit matcher) | At session end |

### Hook Types

**Command Hook:**
```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 60
}
```

**Prompt Hook:**
```json
{
  "type": "prompt",
  "prompt": "Evaluate context: $ARGUMENTS",
  "timeout": 30
}
```

**Agent Hook:**
```json
{
  "type": "agent",
  "prompt": "Verify the task completion"
}
```

### Matcher Syntax

- Simple string: `Write` - exact match
- Regex: `Write|Edit` - matches Write or Edit
- Regex: `Notebook.*` - matches NotebookEdit, etc.
- Wildcard: `*` - matches all tools
- Empty/omitted: matches all (for events without tool context)

### Environment Variables for Hooks

- `$CLAUDE_PROJECT_DIR` - Project root directory
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory (for plugin hooks)
- `$CLAUDE_ENV_FILE` - SessionStart only: file for persisting env vars
- `$CLAUDE_CODE_REMOTE` - "true" if remote/web, empty if local CLI

### Hook Input (via stdin)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_use_id": "toolu_01ABC123"
}
```

### Hook Output

**Exit Codes:**
- 0: Success (stdout shown in verbose mode)
- 2: Blocking error (stderr fed to Claude)
- Other: Non-blocking error (stderr shown in verbose mode)

**JSON Output (exit code 0):**

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": false,
  "systemMessage": "string",
  "decision": "block",
  "reason": "explanation",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "reason",
    "updatedInput": { "field": "new value" }
  }
}
```

### Plugin Hooks

In `hooks/hooks.json`:

```json
{
  "description": "Plugin hook description",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## 4. Permissions Configuration

### Location

In `settings.json` (user, project, or local scope):

```json
{
  "permissions": {
    "allow": [],
    "ask": [],
    "deny": [],
    "additionalDirectories": [],
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable"
  }
}
```

### Permission Rules Schema

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Bash(git diff:*)",
      "Read(~/.zshrc)",
      "Read(./docs/**)",
      "Write(./output/**)",
      "Edit(./src/**)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(rm:*)"
    ],
    "deny": [
      "WebFetch",
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Edit(./.git/**)"
    ],
    "additionalDirectories": [
      "../docs/",
      "/shared/resources/"
    ],
    "defaultMode": "default"
  }
}
```

### Tool Permission Syntax

| Pattern | Description |
|:--------|:------------|
| `ToolName` | Allow/deny entire tool |
| `Bash(command)` | Exact command match |
| `Bash(prefix:*)` | Command prefix match |
| `Read(path)` | Exact file path |
| `Read(path/*)` | Single directory level |
| `Read(path/**)` | Recursive directory match |
| `Edit(path/**/*.ts)` | Glob pattern in path |

### Permission Modes

| Mode | Description |
|:-----|:------------|
| `default` | Normal permission prompts |
| `plan` | Planning mode - no code execution |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Minimal permission prompts |
| `bypassPermissions` | Skip all permissions (dangerous) |

---

## 5. Settings.json Complete Schema

### File Locations

| Scope | Path |
|:------|:-----|
| User | `~/.claude/settings.json` |
| Project | `.claude/settings.json` |
| Local | `.claude/settings.local.json` |
| Managed | System `managed-settings.json` |

### Complete Settings Schema

```json
{
  "apiKeyHelper": "/bin/generate_api_key.sh",
  "cleanupPeriodDays": 30,
  "companyAnnouncements": ["Welcome message"],
  "env": {
    "MY_VAR": "value"
  },
  "attribution": {
    "commit": "Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
    "pr": ""
  },
  "includeCoAuthoredBy": true,
  "permissions": {
    "allow": [],
    "ask": [],
    "deny": [],
    "additionalDirectories": [],
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable"
  },
  "hooks": {},
  "disableAllHooks": false,
  "allowManagedHooksOnly": true,
  "model": "claude-sonnet-4-5-20250929",
  "otelHeadersHelper": "/bin/generate_otel_headers.sh",
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  },
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  },
  "respectGitignore": true,
  "outputStyle": "Explanatory",
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["memory", "github"],
  "disabledMcpjsonServers": ["filesystem"],
  "allowedMcpServers": [{ "serverName": "github" }],
  "deniedMcpServers": [{ "serverName": "dangerous" }],
  "strictKnownMarketplaces": [],
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "awsCredentialExport": "/bin/generate_aws_grant.sh",
  "alwaysThinkingEnabled": true,
  "language": "english",
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "allowUnsandboxedCommands": true,
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true,
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    },
    "enableWeakerNestedSandbox": false
  },
  "enabledPlugins": {
    "formatter@marketplace": true,
    "analyzer@marketplace": false
  },
  "extraKnownMarketplaces": {
    "my-marketplace": {
      "source": {
        "source": "github",
        "repo": "org/plugins"
      }
    }
  }
}
```

### Precedence (highest to lowest)

1. Managed settings (`managed-settings.json`)
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

---

## 6. Plugin Configuration

### Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                # Slash commands
│   └── my-command.md
├── agents/                  # Subagents
│   └── my-agent.md
├── skills/                  # Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/
│   └── hooks.json          # Plugin hooks
├── .mcp.json               # Plugin MCP servers
├── .lsp.json               # Plugin LSP servers
└── scripts/
    └── helper.sh
```

### plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Required Fields

| Field | Type | Description |
|:------|:-----|:------------|
| `name` | string | Unique identifier (kebab-case) |

### Optional Fields

| Field | Type | Description |
|:------|:-----|:------------|
| `version` | string | Semantic version |
| `description` | string | Plugin purpose |
| `author` | object | `{name, email, url}` |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |
| `commands` | string/array | Additional command paths |
| `agents` | string/array | Additional agent paths |
| `skills` | string/array | Additional skill paths |
| `hooks` | string/object | Hook config path or inline |
| `mcpServers` | string/object | MCP config path or inline |
| `lspServers` | string/object | LSP config path or inline |
| `outputStyles` | string/array | Output style paths |

### LSP Server Schema

In `.lsp.json`:

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "transport": "stdio",
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    },
    "env": {},
    "initializationOptions": {},
    "settings": {},
    "workspaceFolder": "${CLAUDE_PROJECT_DIR}",
    "startupTimeout": 10000,
    "shutdownTimeout": 5000,
    "restartOnCrash": true,
    "maxRestarts": 3,
    "loggingConfig": {
      "args": ["--log-level", "4"],
      "env": {
        "TSS_LOG": "-level verbose -file ${CLAUDE_PLUGIN_LSP_LOG_FILE}"
      }
    }
  }
}
```

### Plugin Environment Variables

- `${CLAUDE_PLUGIN_ROOT}` - Absolute path to plugin directory
- `${CLAUDE_PROJECT_DIR}` - Project root directory
- `${CLAUDE_PLUGIN_LSP_LOG_FILE}` - LSP log file path (with `--enable-lsp-logging`)

---

## 7. Subagent Configuration

### File Locations

| Scope | Path |
|:------|:-----|
| User | `~/.claude/agents/<agent-name>.md` |
| Project | `.claude/agents/<agent-name>.md` |
| Plugin | `<plugin-root>/agents/<agent-name>.md` |

### Agent Frontmatter Schema

```yaml
---
name: agent-name
description: What this agent specializes in
capabilities:
  - task1
  - task2
  - task3
skills: skill-name-1, skill-name-2    # Skills to preload
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---

# Agent Name

Detailed description and instructions for the agent.

## Capabilities
- Specific capability 1
- Specific capability 2

## Context and examples
When to use this agent and example scenarios.
```

---

## 8. Slash Commands

### File Locations

| Scope | Path |
|:------|:-----|
| User | `~/.claude/commands/<command-name>.md` |
| Project | `.claude/commands/<command-name>.md` |
| Plugin | `<plugin-root>/commands/<command-name>.md` |

### Command Frontmatter Schema

```yaml
---
description: What this command does
allowed-tools: Read, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: Explore
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true
---

# Command Instructions

Instructions for Claude when command is invoked.

Use $ARGUMENTS for all arguments.
Use $1, $2, etc. for positional arguments.
```

### Argument Placeholders

| Placeholder | Description |
|:------------|:------------|
| `$ARGUMENTS` | All arguments as single string |
| `$1`, `$2`, etc. | Positional arguments |

---

## Quick Reference Tables

### Configuration File Summary

| File | Location | Purpose |
|:-----|:---------|:--------|
| `settings.json` | `~/.claude/` or `.claude/` | General settings, permissions, hooks |
| `settings.local.json` | `.claude/` | Local overrides (gitignored) |
| `~/.claude.json` | Home directory | MCP servers, preferences, OAuth |
| `.mcp.json` | Project root | Project MCP servers |
| `SKILL.md` | In skill directories | Skill definitions |
| `plugin.json` | `.claude-plugin/` | Plugin manifest |
| `hooks.json` | `hooks/` | Plugin hooks |
| `.lsp.json` | Plugin root | LSP server config |

### Scope Hierarchy

1. **Managed** - Cannot be overridden
2. **CLI Arguments** - Session overrides
3. **Local** - Personal project overrides
4. **Project** - Team shared settings
5. **User** - Personal global defaults
