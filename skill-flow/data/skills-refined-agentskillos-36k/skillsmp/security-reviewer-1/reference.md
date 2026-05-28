# Plugin Creator Reference

Advanced patterns, CLI commands, marketplace integration, and debugging.

## CLI Commands

### Plugin Management

```sh
# Install plugin
claude plugin install <plugin>@<marketplace> [--scope user|project|local]

# Uninstall plugin
claude plugin uninstall <plugin>@<marketplace> [--scope]

# Enable disabled plugin
claude plugin enable <plugin>@<marketplace> [--scope]

# Disable without uninstalling
claude plugin disable <plugin>@<marketplace> [--scope]

# Update to latest version
claude plugin update <plugin>@<marketplace> [--scope]
```

### Marketplace Management

```sh
# Add marketplace from GitHub
/plugin marketplace add owner/repo

# Add from Git URL
/plugin marketplace add https://gitlab.com/company/plugins.git

# Add specific branch/tag
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0

# Add local directory
/plugin marketplace add ./my-marketplace

# List marketplaces
/plugin marketplace list

# Update marketplace listings
/plugin marketplace update marketplace-name

# Remove marketplace
/plugin marketplace remove marketplace-name
```

### Interactive UI

```sh
/plugin              # Open plugin manager
```

Tabs:

- **Discover**: Browse available plugins
- **Installed**: Manage installed plugins
- **Marketplaces**: Add/remove marketplaces
- **Errors**: View loading errors

## Marketplace Structure

### Directory Layout

```text
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace catalog
├── plugins/
│   ├── plugin-a/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── commands/
│   └── plugin-b/
│       └── ...
└── README.md
```

### marketplace.json

```json
{
  "name": "my-marketplace",
  "description": "My plugin collection",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "plugin-a",
      "source": "./plugins/plugin-a",
      "description": "Plugin A description",
      "keywords": ["utility", "automation"]
    },
    {
      "name": "plugin-b",
      "source": "./plugins/plugin-b"
    }
  ]
}
```

### Marketplace Entry Fields

| Field         | Required | Description                                |
| ------------- | -------- | ------------------------------------------ |
| `name`        | Yes      | Plugin identifier                          |
| `source`      | Yes      | Relative path to plugin                    |
| `description` | No       | Override plugin description                |
| `keywords`    | No       | Discovery tags                             |
| `strict`      | No       | If true, only use marketplace entry fields |

## LSP Server Configuration

### Required Fields

| Field                 | Description                          |
| --------------------- | ------------------------------------ |
| `command`             | LSP binary (must be in PATH)         |
| `extensionToLanguage` | Maps file extensions to language IDs |

### Optional Fields

| Field                   | Description                   |
| ----------------------- | ----------------------------- |
| `args`                  | Command-line arguments        |
| `transport`             | `stdio` (default) or `socket` |
| `env`                   | Environment variables         |
| `initializationOptions` | Server init options           |
| `settings`              | Workspace settings            |
| `workspaceFolder`       | Workspace folder path         |
| `startupTimeout`        | Max startup wait (ms)         |
| `shutdownTimeout`       | Max shutdown wait (ms)        |
| `restartOnCrash`        | Auto-restart on crash         |
| `maxRestarts`           | Max restart attempts          |
| `loggingConfig`         | Debug logging config          |

### Complete LSP Example

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    },
    "initializationOptions": {
      "preferences": {
        "includeInlayParameterNameHints": "all"
      }
    },
    "loggingConfig": {
      "args": ["--log-level", "verbose"],
      "env": {
        "TSS_LOG": "-level verbose -file ${CLAUDE_PLUGIN_LSP_LOG_FILE}"
      }
    }
  }
}
```

### Available LSP Plugins (Official)

| Language   | Plugin              | Binary Required              |
| ---------- | ------------------- | ---------------------------- |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Go         | `gopls-lsp`         | `gopls`                      |
| C/C++      | `clangd-lsp`        | `clangd`                     |

## Hook Types

### Command Hook

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check.sh",
  "timeout": 30
}
```

### Prompt Hook

LLM-based evaluation:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should proceed: $ARGUMENTS",
  "timeout": 30
}
```

### Agent Hook

Agentic verifier with tools:

```json
{
  "type": "agent",
  "prompt": "Verify the changes meet requirements"
}
```

## Plugin Caching

Plugins are copied to a cache directory on installation.

### Implications

- External files (outside plugin dir) are NOT copied
- Path traversal (`../shared`) won't work
- Use symlinks for shared dependencies

### Using Symlinks

```sh
# Inside plugin directory
ln -s /path/to/shared-utils ./shared-utils
```

Symlinks are followed during copy.

## Team Configuration

### Project Settings

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": ["your-org/claude-plugins"],
  "enabledPlugins": [
    {
      "name": "team-tools",
      "marketplace": "your-org-claude-plugins"
    }
  ]
}
```

Team members are prompted to install when they trust the folder.

### Auto-Updates

Toggle via `/plugin` > Marketplaces > Select marketplace > Enable/Disable auto-update.

Environment variables:

```sh
# Disable all auto-updates
export DISABLE_AUTOUPDATER=true

# Keep plugin updates, disable Claude Code updates
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

## Debugging

### Enable Debug Mode

```sh
claude --debug
```

Shows:

- Plugin loading details
- Manifest errors
- Component registration
- MCP server initialization

### Common Issues

| Issue                | Cause                           | Solution                                     |
| -------------------- | ------------------------------- | -------------------------------------------- |
| Plugin not loading   | Invalid `plugin.json`           | Validate JSON syntax                         |
| Commands missing     | Wrong directory                 | Components at root, not in `.claude-plugin/` |
| Hooks not firing     | Script not executable           | `chmod +x script.sh`                         |
| MCP server fails     | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for paths                       |
| LSP not found        | Binary not installed            | Install language server                      |
| Skills not appearing | Cache stale                     | Clear cache, reinstall                       |

### Clear Plugin Cache

```sh
rm -rf ~/.claude/plugins/cache
```

Then restart Claude Code and reinstall plugins.

### Debug Checklist

1. Run `claude --debug` and check "loading plugin" messages
2. Verify component directories in debug output
3. Check file permissions
4. Test scripts manually
5. Validate JSON syntax

## Complete Plugin Example

```text
deployment-tools/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md
│   ├── rollback.md
│   └── status.md
├── agents/
│   └── deployment-checker.md
├── skills/
│   └── infrastructure/
│       ├── SKILL.md
│       └── scripts/
│           └── validate-config.py
├── hooks/
│   └── hooks.json
├── .mcp.json
├── scripts/
│   ├── pre-deploy.sh
│   └── notify.py
├── LICENSE
└── CHANGELOG.md
```

### plugin.json

```json
{
  "name": "deployment-tools",
  "version": "2.1.0",
  "description": "Deployment automation for Claude Code",
  "author": {
    "name": "DevOps Team",
    "email": "devops@company.com"
  },
  "repository": "https://github.com/company/deployment-tools",
  "license": "MIT",
  "keywords": ["deployment", "ci-cd", "automation"]
}
```

### hooks.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/pre-deploy.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/notify.py"
          }
        ]
      }
    ]
  }
}
```

### .mcp.json

```json
{
  "mcpServers": {
    "deployment-api": {
      "command": "npx",
      "args": ["@company/deploy-mcp-server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}",
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## Version Management

Follow semantic versioning:

```text
MAJOR.MINOR.PATCH

MAJOR - Breaking changes
MINOR - New features (backward-compatible)
PATCH - Bug fixes (backward-compatible)
```

Best practices:

- Start at `1.0.0` for first stable release
- Update version before distributing changes
- Document changes in `CHANGELOG.md`
- Use pre-release: `2.0.0-beta.1`

## Official Marketplace Plugins

### Code Intelligence (LSP)

- `pyright-lsp` - Python
- `typescript-lsp` - TypeScript/JavaScript
- `rust-analyzer-lsp` - Rust
- `gopls-lsp` - Go

### External Integrations (MCP)

- `github`, `gitlab` - Source control
- `atlassian`, `linear`, `notion` - Project management
- `slack` - Communication
- `vercel`, `firebase`, `supabase` - Infrastructure

### Development Workflows

- `commit-commands` - Git workflows
- `pr-review-toolkit` - PR review agents
- `plugin-dev` - Plugin development toolkit
