---
name: claude-marketplace
description: Manage Claude Code plugin marketplaces and plugin listings. Create marketplace.json files, add/update/remove plugin entries, validate marketplace schemas, configure team distribution via settings.json, and troubleshoot marketplace issues. Use when working with marketplaces, plugin distribution, marketplace.json, or team plugin management.
---

# Claude Plugin Marketplace Management

Manage plugin marketplaces for distributing Claude Code extensions across teams and communities.

## What are Marketplaces?

**Marketplaces** are catalogs of available plugins defined in a `marketplace.json` file. They provide centralized discovery, version management, and team distribution of Claude Code plugins.

**Key benefits:**
- **Centralized discovery**: Browse plugins from multiple sources
- **Version management**: Track and update plugin versions
- **Team distribution**: Share required plugins across organizations
- **Flexible sources**: Support for GitHub, Git repositories, local paths, and direct URLs

## Quick Start

### Create Basic Marketplace

Create `.claude-plugin/marketplace.json` in your repository root:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "1.0.0"
    }
  ]
}
```

### Add First Plugin Entry

```json
{
  "name": "deployment-tools",
  "source": {
    "source": "github",
    "repo": "company/deploy-plugin"
  },
  "description": "Deployment automation tools",
  "version": "2.1.0",
  "author": {
    "name": "DevOps Team"
  }
}
```

### Validate Marketplace

```bash
claude plugin validate .
```

### Test Locally

```shell
/plugin marketplace add ./path/to/marketplace
/plugin install test-plugin@marketplace-name
```

## Common Marketplace Operations

### Add Plugin Entry

**GitHub repository:**
```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  },
  "description": "Plugin description",
  "version": "1.0.0"
}
```

**Git repository:**
```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  },
  "description": "Plugin description"
}
```

**Local path (relative to marketplace):**
```json
{
  "name": "local-plugin",
  "source": "./plugins/my-plugin",
  "description": "Plugin description"
}
```

**Direct marketplace URL:**
```json
{
  "name": "remote-plugin",
  "source": "https://url.of/marketplace.json",
  "description": "Plugin description"
}
```

### Update Plugin Metadata

Add optional fields to plugin entries:

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@company.com"
  },
  "homepage": "https://docs.company.com/plugins/enterprise",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity"
}
```

### Remove Plugin Entry

Delete the plugin object from the `plugins` array in marketplace.json and validate:

```bash
claude plugin validate .
```

### Configure Marketplace Metadata

Add optional marketplace-level metadata:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "metadata": {
    "description": "Internal development tools",
    "version": "3.0.0",
    "pluginRoot": "./packages"
  },
  "plugins": [...]
}
```

### Set Plugin Root

Use `pluginRoot` for relative plugin paths:

```json
{
  "name": "monorepo-marketplace",
  "owner": {...},
  "metadata": {
    "pluginRoot": "./packages/plugins"
  },
  "plugins": [
    {
      "name": "tool-a",
      "source": "./tool-a"
    },
    {
      "name": "tool-b",
      "source": "./tool-b"
    }
  ]
}
```

Plugin sources resolve to `./packages/plugins/tool-a` and `./packages/plugins/tool-b`.

## Plugin Entry Configuration

### Required Fields

| Field    | Type           | Description                               | Example                                 |
| :------- | :------------- | :---------------------------------------- | :-------------------------------------- |
| `name`   | string         | Plugin identifier (kebab-case, no spaces) | `"deployment-tools"`                    |
| `source` | string\|object | Where to fetch the plugin                 | `"./plugins/my-plugin"` or object below |

### Optional Metadata Fields

| Field         | Type   | Description                             | Example                                |
| :------------ | :----- | :-------------------------------------- | :------------------------------------- |
| `description` | string | Brief plugin description                | `"Deployment automation tools"`        |
| `version`     | string | Plugin version                          | `"2.1.0"`                              |
| `author`      | object | Author information                      | `{"name": "Team", "email": "..."}"`    |
| `homepage`    | string | Documentation URL                       | `"https://docs.example.com"`           |
| `repository`  | string | Source code URL                         | `"https://github.com/user/plugin"`     |
| `license`     | string | SPDX license identifier                 | `"MIT"`, `"Apache-2.0"`                |
| `keywords`    | array  | Discovery tags                          | `["deployment", "ci-cd"]`              |
| `category`    | string | Plugin category                         | `"productivity"`, `"development"`      |
| `tags`        | array  | Searchability tags                      | `["automation", "devops"]`             |
| `strict`      | boolean| Require plugin.json in plugin (default: true) | `false`                          |

### Component Configuration Fields

Override default component locations:

| Field        | Type           | Description                              | Example                            |
| :----------- | :------------- | :--------------------------------------- | :--------------------------------- |
| `commands`   | string\|array  | Custom command file/directory paths      | `["./cmd/core/", "./cmd/exp.md"]`  |
| `agents`     | string\|array  | Custom agent file paths                  | `["./agents/reviewer.md"]`         |
| `skills`     | string         | Custom skills directory path             | `"./custom-skills/"`               |
| `hooks`      | string\|object | Hook config path or inline configuration | `"./config/hooks.json"`            |
| `mcpServers` | string\|object | MCP config path or inline configuration  | `"./mcp-config.json"`              |

### Source Type Examples

**GitHub repo:**
```json
{
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

**Git URL:**
```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

**Relative path:**
```json
{
  "source": "./plugins/my-plugin"
}
```

### Strict Field Behavior

**`strict: true` (default)**:
- Plugin must include `plugin.json` manifest
- Marketplace fields supplement plugin.json values
- Plugin.json takes precedence for conflicting fields

**`strict: false`**:
- Plugin.json is optional
- If missing, marketplace entry serves as complete manifest
- Useful for simple plugins or rapid prototyping

### ${CLAUDE_PLUGIN_ROOT} Environment Variable

Use `${CLAUDE_PLUGIN_ROOT}` in hooks and MCP servers to reference plugin installation directory:

```json
{
  "name": "custom-plugin",
  "source": "./plugins/custom",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "plugin-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

## Basic Troubleshooting

### Common Issues

**Marketplace not loading:**
- Verify `.claude-plugin/marketplace.json` exists at specified path
- Check JSON syntax: `claude plugin validate .`
- For private repos, confirm access permissions

**Plugin installation fails:**
- Verify plugin source URL is accessible
- Check plugin directory contains required files
- For GitHub sources, ensure repo is public or accessible

**Validation errors:**
```bash
# Validate marketplace JSON
claude plugin validate .

# Check specific issues
# - name field must be kebab-case (no spaces)
# - owner object must include name
# - plugins must be an array
# - Each plugin must have name and source
```

**Path resolution issues:**
- All paths must be relative and start with `./`
- Use `metadata.pluginRoot` for monorepo structures
- Use `${CLAUDE_PLUGIN_ROOT}` for runtime paths in hooks/MCP servers

### Quick Fixes

| Issue                 | Solution                                  |
| :-------------------- | :---------------------------------------- |
| JSON syntax error     | Run `claude plugin validate .`            |
| Plugin not found      | Check source URL accessibility            |
| Permission denied     | Verify repository access rights           |
| Commands not appearing| Ensure plugin directory structure correct |

For detailed troubleshooting workflows, see [reference/troubleshooting.md](reference/troubleshooting.md).

## Reference Documentation

For complete details on marketplace management, see:

### [reference/marketplace-schema.md](reference/marketplace-schema.md)
Complete marketplace.json schema reference:
- Annotated schema examples
- Required and optional fields
- Plugin entry specifications
- Source type details
- Validation rules

### [reference/plugin-management.md](reference/plugin-management.md)
Plugin entry patterns and configuration:
- Simple to complex plugin entries
- Component configuration (commands, agents, skills, hooks, MCP)
- Version management strategies
- Plugin source management
- Monorepo organization

### [reference/team-distribution.md](reference/team-distribution.md)
Team distribution and workflows:
- Settings.json configuration
- extraKnownMarketplaces setup
- enabledPlugins configuration
- Team workflow patterns
- Organization best practices

### [reference/troubleshooting.md](reference/troubleshooting.md)
Detailed troubleshooting guide:
- Validation error catalog
- Installation issue resolution
- Runtime problem debugging
- Systematic debugging workflows
- Common error solutions

## When to Use This Skill

Use this skill when:
- Creating new plugin marketplaces
- Adding or updating plugin entries
- Configuring marketplace.json files
- Setting up team plugin distribution
- Validating marketplace schemas
- Troubleshooting marketplace or plugin installation issues
- Managing plugin versions and updates
- Organizing plugins in monorepos
- Configuring custom component paths
- Setting up private marketplaces for organizations

## Related Slash Commands

- `/plugin marketplace add` - Add a marketplace
- `/plugin marketplace list` - List configured marketplaces
- `/plugin marketplace update` - Refresh marketplace metadata
- `/plugin marketplace remove` - Remove a marketplace
- `/plugin install` - Install plugin from marketplace
- `/plugin` - Browse available plugins interactively

## Key Takeaways

1. **Marketplaces catalog plugins**: marketplace.json lists available plugins with sources
2. **Flexible sources**: Support GitHub, Git, local paths, direct URLs
3. **Team distribution**: Configure in settings.json for automatic installation
4. **Validation is critical**: Always run `claude plugin validate .` before distribution
5. **Progressive disclosure**: Use strict: false for simple plugins, strict: true for complex ones
6. **Environment variables**: Use `${CLAUDE_PLUGIN_ROOT}` for runtime paths

---

*For complete technical specifications, see the reference documentation above*
