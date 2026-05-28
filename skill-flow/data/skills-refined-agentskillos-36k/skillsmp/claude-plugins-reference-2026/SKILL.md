---
name: claude-plugins-reference-2026
description: Reference guide for Claude Code plugins system (January 2026). Use when creating, distributing, or understanding plugins, plugin.json schema, marketplace configuration, bundling skills/commands/agents/hooks/MCP/LSP, or plugin validation.
---

# Claude Code Plugins System - Complete Reference (January 2026)

Plugins bundle multiple Claude Code capabilities (skills, commands, agents, hooks, MCP servers, LSP servers) into distributable packages.

---

## plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description with trigger keywords",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": ["./skills/skill-one", "./skills/skill-two"],
  "hooks": "./hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

### Required Fields

| Field  | Type   | Constraints                                 |
| ------ | ------ | ------------------------------------------- |
| `name` | string | Kebab-case, unique identifier, max 64 chars |

### Recommended Fields

| Field         | Type   | Purpose                                  |
| ------------- | ------ | ---------------------------------------- |
| `version`     | string | Semantic versioning (X.Y.Z)              |
| `description` | string | Max 1024 chars, include trigger keywords |
| `author`      | object | `{name, email?, url?}`                   |
| `homepage`    | string | Documentation URL                        |
| `repository`  | string | Source code URL                          |
| `license`     | string | SPDX identifier                          |
| `keywords`    | array  | Marketplace discoverability              |

### Component Paths

| Field          | Type          | Default Location         |
| -------------- | ------------- | ------------------------ |
| `commands`     | string/array  | `./commands/`            |
| `agents`       | string/array  | `./agents/`              |
| `skills`       | string/array  | `./skills/`              |
| `hooks`        | string/object | `./hooks.json` or inline |
| `mcpServers`   | string/object | `./.mcp.json` or inline  |
| `lspServers`   | string/object | `./.lsp.json` or inline  |
| `outputStyles` | string        | `./styles/`              |

---

## Directory Structure

```
plugin-name/
├── .claude-plugin/           # REQUIRED metadata directory
│   └── plugin.json          # REQUIRED manifest (only file here)
├── commands/                 # Slash command files (.md)
├── agents/                   # Agent definitions (.md)
├── skills/                   # SKILL.md directories
│   ├── skill-one/
│   │   ├── SKILL.md
│   │   └── references/
│   └── skill-two/
│       └── SKILL.md
├── hooks.json               # Hook configurations
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Helper scripts for hooks
├── LICENSE
├── CHANGELOG.md
└── README.md
```

**Critical**: `.claude-plugin/` contains ONLY `plugin.json` - never put components here.

---

## Distribution Methods

### Marketplace (Recommended)

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Team Name",
    "email": "team@example.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "source": "./plugins/plugin-one"
    },
    {
      "name": "plugin-two",
      "source": { "source": "github", "repo": "owner/repo" }
    }
  ]
}
```

### Plugin Sources

| Type          | Format                                         |
| ------------- | ---------------------------------------------- |
| Relative path | `"./plugins/my-plugin"`                        |
| GitHub        | `{ "source": "github", "repo": "owner/repo" }` |
| Git URL       | `{ "source": "url", "url": "https://..." }`    |

### Installation Commands

```bash
# Add marketplace
/plugin marketplace add owner/repo
/plugin marketplace add https://gitlab.com/company/plugins.git
/plugin marketplace add ./local-marketplace

# Install plugin
/plugin install plugin-name@marketplace-name
/plugin install plugin-name@marketplace-name --scope project
/plugin install plugin-name@marketplace-name --scope local

# Manage
/plugin enable plugin-name
/plugin disable plugin-name
/plugin update plugin-name
/plugin uninstall plugin-name
```

---

## Installation Scopes

| Scope     | Settings File                 | Use Case                     |
| --------- | ----------------------------- | ---------------------------- |
| `user`    | `~/.claude/settings.json`     | Personal, global (default)   |
| `project` | `.claude/settings.json`       | Team, shared via git         |
| `local`   | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | `managed-settings.json`       | Enterprise, admin-controlled |

---

## Bundled Capabilities

### Commands

- Location: `commands/` directory
- Format: Markdown with frontmatter
- Namespace: `/plugin-name:command-name`

### Agents

- Location: `agents/` directory
- Format: Markdown with frontmatter
- Auto-delegation by Claude

### Skills

- Location: `skills/` with `SKILL.md`
- Auto-activation by Claude
- Progressive disclosure support

### Hooks

- Location: `hooks.json` or `plugin.json` inline
- Events: PreToolUse, PostToolUse, Stop, etc.
- Use `${CLAUDE_PLUGIN_ROOT}` for paths

### MCP Servers

- Location: `.mcp.json`
- Types: http, stdio
- Auto-start when plugin enabled

### LSP Servers

- Location: `.lsp.json`
- Requires binary installation
- Code intelligence features

---

## Environment Variables

| Variable                | Description                       |
| ----------------------- | --------------------------------- |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory |
| `${CLAUDE_PROJECT_DIR}` | Project root directory            |

---

## Validation

```bash
# CLI
claude plugin validate .
claude plugin validate ./my-plugin

# In Claude Code
/plugin validate .
```

### Testing

```bash
# Load during development
claude --plugin-dir ./my-plugin
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

---

## Enterprise Features

```json
{
  "enabledPlugins": {
    "code-formatter@company-tools": true
  },
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": { "source": "github", "repo": "org/plugins" }
    }
  },
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" }
  ]
}
```

| Setting                              | Effect            |
| ------------------------------------ | ----------------- |
| `strictKnownMarketplaces: []`        | Complete lockdown |
| `strictKnownMarketplaces: [sources]` | Allowlist only    |
| `strictKnownMarketplaces: undefined` | No restrictions   |

---

## Constraints

- Plugins copied to cache, not used in-place
- Cannot reference files outside plugin directory (`../` fails)
- LSP servers require separate binary installation
- All paths must be relative, start with `./`
- Path traversal (`..`) not allowed
- Scripts must be executable (`chmod +x`)
- Reserved marketplace names: `claude-code-marketplace`, `anthropic-plugins`

---

## Private Repository Authentication

| Service   | Environment Variable         | Scope             |
| --------- | ---------------------------- | ----------------- |
| GitHub    | `GITHUB_TOKEN` or `GH_TOKEN` | `repo`            |
| GitLab    | `GITLAB_TOKEN` or `GL_TOKEN` | `read_repository` |
| Bitbucket | `BITBUCKET_TOKEN`            | read access       |

---

## Sources

- [Create Plugins](https://code.claude.com/docs/en/plugins)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Discover and Install Plugins](https://code.claude.com/docs/en/discover-plugins)
