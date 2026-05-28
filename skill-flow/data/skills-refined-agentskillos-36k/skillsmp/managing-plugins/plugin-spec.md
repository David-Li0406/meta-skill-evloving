# Plugin Structure Specification

## Directory Structure

```
plugin-root/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                 # Default location
├── agents/                   # Default location
├── skills/                   # Default location
├── hooks/                    # Default location
└── .mcp.json                # Optional MCP config
```

**Critical**: All component dirs (commands/, agents/, skills/, hooks/) at plugin root, NOT inside .claude-plugin/

## plugin.json Schema

### Required Fields
```json
{"name":"plugin-identifier"}
```

### Full Schema
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin purpose",
  "author": {"name": "Author", "email": "author@example.com", "url": "https://..."},
  "homepage": "https://...",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "commands": "./commands" | ["./cmd1", "./cmd2"],
  "agents": "./agents" | ["./agent1.md"],
  "hooks": "./hooks/hooks.json" | {...inline...},
  "mcpServers": "./.mcp.json" | {...inline...}
}
```

### Field Types
- **name** (string, required): kebab-case identifier
- **version** (string): semver format (MAJOR.MINOR.PATCH)
- **description** (string): Brief purpose
- **author** (object): name, email (optional), url (optional)
- **homepage** (string): Documentation URL
- **repository** (string): Source code URL
- **license** (string): License identifier (MIT, Apache-2.0, etc.)
- **keywords** (array): Discovery tags
- **commands** (string|array): Path(s) to command files/dirs
- **agents** (string|array): Path(s) to subagent definitions (subagents are subordinate agents started from Claude Code)
- **hooks** (string|object): Path to hooks.json OR inline config
- **mcpServers** (string|object): Path to .mcp.json OR inline config

### Path Rules
- All paths relative, start with ./
- Paths supplement defaults (don't replace)
- Arrays allowed for multiple paths
- Use ${CLAUDE_PLUGIN_ROOT} for absolute resolution

## Component Formats

### Commands
Markdown files with YAML frontmatter:
```markdown
---
description: Command description
argument-hint: <args>
---
Command prompt content
```

### Skills
Directory with SKILL.md:
```
skills/skill-name/
├── SKILL.md
├── supporting.md
└── scripts/
```

### Hooks
JSON config with events and actions:
```json
{
  "hooks": [{
    "event": "PreToolUse",
    "match": {"tool": "Bash"},
    "action": {"type": "command", "command": "./script.sh"}
  }]
}
```

Events: PreToolUse, PermissionRequest, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, SessionStart, SessionEnd, PreCompact

### MCP Servers
JSON config:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {"KEY": "value"},
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Server Configuration Fields**:
- **command** (string): Executable path or command name (use ${CLAUDE_PLUGIN_ROOT} for portability)
- **args** (array): Command-line arguments passed to server (optional)
- **env** (object): Environment variables available to server (optional)
- **cwd** (string): Working directory for server process (use ${CLAUDE_PLUGIN_ROOT} for plugin-relative paths)

## Naming Conventions

- Plugin names: kebab-case
- Command files: verb-noun.md (e.g., check-code.md)
- Skill dirs: gerund-form (e.g., analyzing-data/)
- No spaces, underscores, capitals in names

## Environment Variables

**${CLAUDE_PLUGIN_ROOT}**: Absolute path to plugin directory
- Required for portability
- Use in all script/server paths
- Resolves at runtime regardless of installation location
