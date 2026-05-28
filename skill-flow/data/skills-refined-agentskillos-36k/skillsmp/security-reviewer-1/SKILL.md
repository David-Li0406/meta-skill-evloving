---
name: meta:plugin-creator
description: Create complete Claude Code plugins with proper structure including skills, commands, agents, and hooks. Generates plugin manifests and directory structures for distribution. Use when building plugins, creating plugin packages, distributing skills to marketplace.
---

# Plugin Creator

## Quick Start

### Step 1: Create the plugin

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── hello.md
```

```json
// .claude-plugin/plugin.json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My first Claude Code plugin"
}
```

```markdown
## <!-- commands/hello.md -->

## description: Say hello

Say "Hello from my-plugin!" to the user.
```

### Step 2: Validate (required)

**Always run validation after creating or modifying a plugin:**

```sh
uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py path/to/my-plugin
```

Fix any errors before publishing.

## Plugin Manifest

### Required Fields

```json
{
  "name": "plugin-name"
}
```

The `name` must be kebab-case with no spaces.

### Complete Schema

```json
{
  "name": "my-plugin",
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
  "commands": "./custom/commands/",
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

### Field Reference

| Field         | Type   | Required | Description                      |
| ------------- | ------ | -------- | -------------------------------- |
| `name`        | string | Yes      | Unique identifier (kebab-case)   |
| `version`     | string | No       | Semantic version (e.g., "1.2.0") |
| `description` | string | No       | Brief explanation                |
| `author`      | object | No       | `{name, email, url}`             |
| `homepage`    | string | No       | Documentation URL                |
| `repository`  | string | No       | Source code URL                  |
| `license`     | string | No       | License identifier               |
| `keywords`    | array  | No       | Discovery tags                   |

### Component Paths

| Field          | Type          | Default Location   |
| -------------- | ------------- | ------------------ |
| `commands`     | string/array  | `commands/`        |
| `agents`       | string/array  | `agents/`          |
| `skills`       | string/array  | `skills/`          |
| `hooks`        | string/object | `hooks/hooks.json` |
| `mcpServers`   | string/object | `.mcp.json`        |
| `lspServers`   | string/object | `.lsp.json`        |
| `outputStyles` | string/array  | -                  |

Custom paths **supplement** default directories—they don't replace them.

## Directory Structure

```text
my-plugin/
├── .claude-plugin/           # Metadata (ONLY plugin.json here)
│   └── plugin.json          # Required manifest
├── commands/                 # Slash commands (.md files)
│   ├── deploy.md
│   └── status.md
├── agents/                   # Subagents (.md files)
│   ├── reviewer.md
│   └── tester.md
├── skills/                   # Agent skills (directories)
│   └── code-review/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Event hooks
│   └── hooks.json
├── .mcp.json                # MCP server config
├── .lsp.json                # LSP server config
├── scripts/                 # Utility scripts
│   └── format.sh
├── LICENSE
└── CHANGELOG.md
```

> **Critical**: Components go at plugin root, NOT inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

## Plugin Components

### Commands

Location: `commands/*.md`

```markdown
---
description: Deploy to production
argument-hint: [environment]
---

Deploy the application to $ARGUMENTS environment.
```

Commands are namespaced: `/plugin-name:command-name`

### Agents

Location: `agents/*.md`

```markdown
---
name: security-reviewer
description: Review code for security vulnerabilities. Use proactively after auth changes.
tools: Read, Grep, Glob
model: haiku
---

# Security Reviewer

You review code for security issues...
```

### Skills

Location: `skills/*/SKILL.md`

```text
skills/
└── pdf-processor/
    ├── SKILL.md
    ├── reference.md
    └── scripts/
```

Skills are auto-discovered based on context.

### Hooks

Location: `hooks/hooks.json` or inline in `plugin.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

### MCP Servers

Location: `.mcp.json` or inline in `plugin.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### LSP Servers

Location: `.lsp.json` or inline in `plugin.json`

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Required: `command`, `extensionToLanguage`

## Environment Variables

| Variable                | Purpose                           |
| ----------------------- | --------------------------------- |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory |
| `${CLAUDE_PROJECT_DIR}` | Project root directory            |

Always use `${CLAUDE_PLUGIN_ROOT}` for plugin file paths.

## Installation Scopes

| Scope     | Settings File                 | Use Case                 |
| --------- | ----------------------------- | ------------------------ |
| `user`    | `~/.claude/settings.json`     | Personal, all projects   |
| `project` | `.claude/settings.json`       | Team, version controlled |
| `local`   | `.claude/settings.local.json` | Personal, gitignored     |
| `managed` | managed-settings.json         | Enterprise, read-only    |

## Common Mistakes

| Mistake                         | Impact            | Correct Pattern             |
| ------------------------------- | ----------------- | --------------------------- |
| Components in `.claude-plugin/` | Not discovered    | Put at plugin root          |
| Absolute paths                  | Break on install  | Use `${CLAUDE_PLUGIN_ROOT}` |
| Missing `plugin.json`           | Plugin won't load | Create in `.claude-plugin/` |
| Path traversal (`../`)          | Files not copied  | Keep files in plugin dir    |
| Non-executable scripts          | Hooks fail        | `chmod +x script.sh`        |

## Validation

Run the validator to check plugin structure:

```sh
uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py ./my-plugin
```

### Checklist

- [ ] `.claude-plugin/plugin.json` exists with `name` field
- [ ] Components at plugin root (not in `.claude-plugin/`)
- [ ] All paths relative, starting with `./`
- [ ] Scripts are executable
- [ ] Uses `${CLAUDE_PLUGIN_ROOT}` for paths
- [ ] Version follows semver (MAJOR.MINOR.PATCH)

## Delegation

- **After creating/modifying plugins**: Run `uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py <plugin-dir>`
- **Pattern discovery**: For existing plugin patterns, use `Explore` agent
- **Component creation**: Use `meta-skill-creator`, `meta-command-creator`, `meta-agent-creator`, `meta-hook-creator`

## Additional Resources

- For CLI commands, marketplace, debugging: [reference.md](reference.md)

## References

- Official Plugins Reference: [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference)
- Discover Plugins: [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)
- Plugin Marketplaces: [code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
