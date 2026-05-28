# Plugin Manifest Reference

Complete documentation for the `plugin.json` manifest file.

## Location

The manifest must be at `.claude-plugin/plugin.json` inside your plugin directory:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json    # <-- Here
├── commands/
└── ...
```

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

The `name` field:
- Becomes the namespace prefix for commands (`/deployment-tools:status`)
- Must be unique within a marketplace
- Should be descriptive and lowercase
- Use hyphens to separate words

## Minimal Manifest

```json
{
  "name": "my-plugin"
}
```

That's all that's required. Everything else is optional but recommended.

## Recommended Fields

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief explanation of what the plugin does"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version (MAJOR.MINOR.PATCH) |
| `description` | string | Brief explanation shown in plugin manager |

## Complete Schema

```json
{
  "name": "enterprise-plugin",
  "version": "2.1.0",
  "description": "Enterprise workflow automation tools",

  "author": {
    "name": "DevTools Team",
    "email": "devtools@company.com",
    "url": "https://github.com/devtools-team"
  },

  "homepage": "https://docs.company.com/enterprise-plugin",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],

  "commands": ["./custom/commands/"],
  "agents": ["./custom/agents/"],
  "skills": ["./custom/skills/"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

## Metadata Fields

### Author Object

```json
{
  "author": {
    "name": "Your Name",          // Required if author specified
    "email": "you@example.com",   // Optional
    "url": "https://yoursite.com" // Optional
  }
}
```

### Homepage and Repository

```json
{
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/user/plugin"
}
```

- `homepage`: Documentation or landing page URL
- `repository`: Source code repository URL

### License

```json
{
  "license": "MIT"
}
```

Use SPDX license identifiers:
- `MIT`
- `Apache-2.0`
- `GPL-3.0`
- `BSD-3-Clause`
- `ISC`

### Keywords

```json
{
  "keywords": ["deployment", "ci-cd", "automation"]
}
```

Used for:
- Plugin discovery in marketplaces
- Categorization and filtering
- Search matching

## Component Path Fields

Override or extend default component locations:

| Field | Type | Default Location | Description |
|-------|------|------------------|-------------|
| `commands` | string\|array | `commands/` | Additional command files/dirs |
| `agents` | string\|array | `agents/` | Additional agent files |
| `skills` | string\|array | `skills/` | Additional skill directories |
| `hooks` | string\|object | `hooks/hooks.json` | Hook config path or inline |
| `mcpServers` | string\|object | `.mcp.json` | MCP config path or inline |
| `lspServers` | string\|object | `.lsp.json` | LSP config path or inline |
| `outputStyles` | string\|array | - | Output style files/dirs |

### Path Behavior Rules

**Important:** Custom paths supplement default directories - they don't replace them.

```json
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

- If `commands/` exists, it loads in addition to custom paths
- All paths must be relative to plugin root
- Paths must start with `./`
- Multiple paths can be specified as arrays

### Inline Configuration

Instead of referencing files, provide configuration inline:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
      }]
    }]
  },
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server/run.sh"
    }
  }
}
```

## Version Management

Follow semantic versioning:

```
MAJOR.MINOR.PATCH
```

| Part | When to Increment | Example |
|------|-------------------|---------|
| MAJOR | Breaking changes | `2.0.0` |
| MINOR | New features (backward-compatible) | `1.2.0` |
| PATCH | Bug fixes | `1.0.1` |

### Pre-release Versions

```json
{
  "version": "2.0.0-beta.1"
}
```

Use for testing before stable release:
- `2.0.0-alpha.1`
- `2.0.0-beta.1`
- `2.0.0-rc.1`

### Best Practices

- Start at `1.0.0` for first stable release
- Update version before distributing changes
- Document changes in `CHANGELOG.md`
- Tag releases in git

## Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths:

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
      }]
    }]
  },
  "mcpServers": {
    "db-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DATA_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

**Why it matters:** Plugins are copied to a cache directory when installed. Absolute paths break; `${CLAUDE_PLUGIN_ROOT}` resolves to the actual installation location.

## Validation

Validate your manifest:

```bash
claude plugin validate ./my-plugin
```

Or from within Claude Code:

```
/plugin validate ./my-plugin
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `name: Required` | Missing name field | Add `"name": "plugin-name"` |
| `Invalid JSON syntax` | Syntax error | Check commas, quotes, brackets |
| `Path traversal not allowed` | `..` in path | Use relative paths without `..` |

## Examples

### Minimal Production Plugin

```json
{
  "name": "code-formatter",
  "version": "1.0.0",
  "description": "Automatic code formatting on file save",
  "author": {
    "name": "DevTools Team"
  },
  "license": "MIT"
}
```

### Full-Featured Plugin

```json
{
  "name": "enterprise-suite",
  "version": "2.3.0",
  "description": "Complete enterprise development toolkit with deployment, monitoring, and compliance tools",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@company.com",
    "url": "https://company.com/team"
  },
  "homepage": "https://docs.company.com/enterprise-suite",
  "repository": "https://github.com/company/enterprise-suite",
  "license": "Apache-2.0",
  "keywords": [
    "enterprise",
    "deployment",
    "monitoring",
    "compliance",
    "automation"
  ],
  "commands": [
    "./commands/deployment/",
    "./commands/monitoring/",
    "./commands/compliance/"
  ],
  "agents": [
    "./agents/security-reviewer.md",
    "./agents/compliance-checker.md"
  ],
  "skills": "./skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./config/mcp.json",
  "lspServers": "./config/lsp.json"
}
```

### Plugin with Inline Hooks

```json
{
  "name": "auto-lint",
  "version": "1.0.0",
  "description": "Auto-lint files after editing",
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npm run lint:fix -- $TOOL_INPUT_file_path"
      }]
    }]
  }
}
```

## See Also

- [SKILL.md](./SKILL.md) - Main plugin creation guide
- [COMPONENTS.md](./COMPONENTS.md) - Component type documentation
- [DISTRIBUTION.md](./DISTRIBUTION.md) - Marketplace distribution
