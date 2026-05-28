# Claude Code Plugin Formats Reference

This document describes the file formats and structures used by Claude Code plugins.

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           # REQUIRED - Plugin manifest
├── commands/                  # Slash commands
│   ├── command-one.md
│   └── command-two.md
├── skills/                    # Agent skills
│   └── skill-name/
│       └── SKILL.md
├── agents/                    # Subagent definitions
│   └── agent-name.md
├── hooks/                     # Event hooks
│   └── hooks.json
├── .mcp.json                  # MCP server configuration
├── .lsp.json                  # Language server configuration
└── scripts/                   # Supporting scripts
```

**Important:** Only `plugin.json` belongs in `.claude-plugin/`. All other content goes at plugin root.

---

## Plugin Manifest (plugin.json)

Location: `.claude-plugin/plugin.json`

### Minimal Example

```json
{
  "name": "my-plugin"
}
```

### Full Example

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A helpful plugin for doing things",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/author/my-plugin",
  "license": "MIT",
  "keywords": ["productivity", "automation"],
  "commands": "./commands/",
  "skills": "./skills/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json"
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique plugin identifier (kebab-case) |
| `version` | string | No | Semantic version (e.g., "1.0.0") |
| `description` | string | No | Brief description of plugin purpose |
| `author` | object | No | Author information |
| `author.name` | string | No | Author's name |
| `author.email` | string | No | Author's email |
| `author.url` | string | No | Author's website/profile |
| `homepage` | string | No | Plugin documentation URL |
| `repository` | string | No | Source code repository URL |
| `license` | string | No | License identifier (e.g., "MIT") |
| `keywords` | string[] | No | Tags for discoverability |
| `commands` | string | No | Path to commands directory |
| `skills` | string | No | Path to skills directory |
| `agents` | string | No | Path to agents directory |
| `hooks` | string | No | Path to hooks configuration |
| `mcpServers` | string | No | Path to MCP server config |
| `lspServers` | string | No | Path to LSP server config |

---

## Slash Commands

Location: `commands/*.md`

Commands are Markdown files with YAML frontmatter. The filename determines the command name:
- `commands/hello.md` → `/plugin-name:hello`
- `commands/list-items.md` → `/plugin-name:list-items`

### Command File Format

```markdown
---
description: One-line description shown in /help
---

# Command Name

Instructions for Claude on how to execute this command.

## Arguments

Parse `$ARGUMENTS` for user input:
- First positional argument: [description]
- `--flag-name`: [description]

## Behavior

Detailed instructions on what the command should do...
```

### Special Variable

- `$ARGUMENTS` - Contains everything the user typed after the command name

### Example Command

```markdown
---
description: Greet a user by name
---

# Greet Command

You are helping the user send a greeting.

## Arguments

Parse `$ARGUMENTS` for:
- **name**: The name to greet (required)
- `--formal`: Use formal greeting style

## Behavior

1. Extract the name from arguments
2. If `--formal` flag present, use "Good day, [name]"
3. Otherwise, use "Hey [name]!"
4. Display the greeting to the user
```

---

## Agent Skills

Location: `skills/[skill-name]/SKILL.md`

Skills are specialized capabilities that Claude can invoke automatically or on demand.

### SKILL.md Format

```markdown
---
name: skill-name
description: What this skill does
user-invocable: false
---

# Skill Name

Detailed instructions for when and how to use this skill.

## Trigger Conditions

This skill activates when:
- [condition 1]
- [condition 2]

## Capabilities

[What this skill can do]

## Implementation

[Step-by-step instructions]
```

### Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill identifier |
| `description` | string | Yes | Brief description |
| `user-invocable` | boolean | No | If true, users can invoke directly (default: true) |

---

## Event Hooks

Location: `hooks/hooks.json` or inline in `plugin.json`

Hooks trigger actions in response to Claude Code events.

### hooks.json Format

```json
{
  "EventName": [
    {
      "type": "command",
      "command": "shell-command-to-run"
    }
  ]
}
```

### Hook Types

| Type | Description |
|------|-------------|
| `command` | Run a shell command |
| `prompt` | Send instruction to Claude |
| `agent` | Invoke an agentic subprompt |

### Available Events

| Event | Description |
|-------|-------------|
| `PreToolUse` | Before a tool is executed |
| `PostToolUse` | After a tool completes successfully |
| `PostToolUseFailure` | After a tool fails |
| `PermissionRequest` | When permission is requested |
| `UserPromptSubmit` | When user submits a message |
| `Notification` | When a notification is shown |
| `Stop` | When execution is stopped |
| `SubagentStart` | When a subagent starts |
| `SubagentStop` | When a subagent stops |
| `SessionStart` | At session beginning |
| `SessionEnd` | At session end |
| `PreCompact` | Before context compaction |

### Hook Examples

**Command Hook:**
```json
{
  "SessionStart": [
    {
      "type": "command",
      "command": "echo 'Session started' >> ~/session.log"
    }
  ]
}
```

**Prompt Hook:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Before running this command, verify it is safe."
        }
      ]
    }
  ]
}
```

**Hook with Matcher:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'File being edited: $FILE_PATH'"
        }
      ]
    }
  ]
}
```

### Environment Variables in Hooks

| Variable | Available In | Description |
|----------|--------------|-------------|
| `$TOOL_NAME` | PreToolUse, PostToolUse | Name of the tool |
| `$TOOL_INPUT` | PreToolUse | Tool input as JSON |
| `$TOOL_OUTPUT` | PostToolUse | Tool output |
| `$FILE_PATH` | Edit, Read, Write | Path being operated on |
| `$SESSION_ID` | All | Current session identifier |

---

## MCP Server Configuration

Location: `.mcp.json` or inline in `plugin.json`

MCP (Model Context Protocol) servers provide external tool integrations.

### .mcp.json Format

```json
{
  "server-name": {
    "type": "stdio|http|sse",
    "command": "command-to-run",
    "args": ["arg1", "arg2"],
    "env": {
      "API_KEY": "${ENV_VAR_NAME}"
    }
  }
}
```

### Server Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `stdio` | Local process communication | `command`, optionally `args` |
| `http` | HTTP endpoint | `url` |
| `sse` | Server-sent events | `url` |

### STDIO Server Example

```json
{
  "github-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": ["@github/mcp-server"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

### HTTP Server Example

```json
{
  "api-server": {
    "type": "http",
    "url": "https://api.example.com/mcp"
  }
}
```

### Plugin Path Variable

Use `${CLAUDE_PLUGIN_ROOT}` for paths relative to the plugin:

```json
{
  "local-server": {
    "type": "stdio",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/server.sh"
  }
}
```

---

## Marketplace Configuration

Location: `.claude-plugin/marketplace.json`

### marketplace.json Format

```json
{
  "name": "marketplace-id",
  "owner": {
    "name": "Owner Name",
    "email": "owner@example.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-id",
      "source": "./relative/path",
      "description": "Plugin description"
    }
  ]
}
```

### Plugin Source Types

**Relative Path:**
```json
{
  "name": "my-plugin",
  "source": "./my-plugin",
  "description": "Local plugin"
}
```

**GitHub:**
```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repo"
  },
  "description": "Plugin from GitHub"
}
```

**NPM:**
```json
{
  "name": "npm-plugin",
  "source": {
    "source": "npm",
    "package": "@org/plugin"
  }
}
```

**URL:**
```json
{
  "name": "url-plugin",
  "source": {
    "source": "url",
    "url": "https://example.com/plugin.tar.gz"
  }
}
```

---

## Name Validation Rules

### Plugin Names
- Must be kebab-case: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`
- Length: 2-50 characters
- Must start with a letter
- Cannot end with hyphen
- No consecutive hyphens

**Valid:** `my-plugin`, `cool-tool-v2`, `a1`
**Invalid:** `My-Plugin`, `my--plugin`, `-plugin`, `plugin-`

### Marketplace Names
- Same rules as plugin names
- Should be unique across all known marketplaces

### Command Names
- Derived from filename (without .md extension)
- Same kebab-case rules apply
- Accessed as `/plugin-name:command-name`

---

## File Locations Summary

| Component | Location | Format |
|-----------|----------|--------|
| Plugin manifest | `.claude-plugin/plugin.json` | JSON |
| Commands | `commands/*.md` | Markdown + YAML frontmatter |
| Skills | `skills/*/SKILL.md` | Markdown + YAML frontmatter |
| Agents | `agents/*.md` | Markdown + YAML frontmatter |
| Hooks | `hooks/hooks.json` | JSON |
| MCP servers | `.mcp.json` | JSON |
| LSP servers | `.lsp.json` | JSON |
| Marketplace | `.claude-plugin/marketplace.json` | JSON |
