# Plugin Management Reference

Comprehensive guide to plugin entry patterns, component configuration, version management, and source organization.

## Plugin Entry Patterns

### Simple Plugin (Minimal Fields)

**Use case:** Basic plugin with default directory structure

```json
{
  "name": "quick-formatter",
  "source": "./plugins/formatter",
  "description": "Code formatting utility",
  "version": "1.0.0"
}
```

**Directory structure:**

```
formatter/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── format.md
└── README.md
```

**Behavior:**
- Uses default component locations (commands/, agents/, skills/)
- Requires plugin.json (strict: true by default)
- Minimal marketplace entry, full manifest in plugin

### Full-Featured Plugin (All Metadata)

**Use case:** Production plugin with complete documentation

```json
{
  "name": "enterprise-security",
  "source": {
    "source": "github",
    "repo": "enterprise/security-plugin"
  },
  "description": "Comprehensive security scanning and compliance tools",
  "version": "2.3.1",
  "author": {
    "name": "Security Team",
    "email": "security@enterprise.com",
    "url": "https://github.com/enterprise/security-team"
  },
  "homepage": "https://docs.enterprise.com/plugins/security",
  "repository": "https://github.com/enterprise/security-plugin",
  "license": "MIT",
  "keywords": ["security", "compliance", "audit", "scanning"],
  "category": "security",
  "tags": ["vulnerability", "sast", "dast"]
}
```

**Benefits:**
- Rich discovery metadata for users
- Clear licensing and ownership
- Searchable by keywords and category
- Complete documentation links

### Multi-Component Plugin (Custom Paths)

**Use case:** Complex plugin with non-standard organization

```json
{
  "name": "devops-suite",
  "source": "./packages/devops",
  "description": "Complete DevOps automation suite",
  "version": "3.0.0",
  "commands": [
    "./cmd/deploy/",
    "./cmd/monitor/",
    "./cmd/rollback/"
  ],
  "agents": [
    "./agents/deployment-planner.md",
    "./agents/incident-responder.md"
  ],
  "skills": "./custom-skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./config/mcp.json"
}
```

**Directory structure:**

```
devops/
├── .claude-plugin/
│   └── plugin.json
├── cmd/
│   ├── deploy/
│   ├── monitor/
│   └── rollback/
├── agents/
│   ├── deployment-planner.md
│   └── incident-responder.md
├── custom-skills/
│   ├── deployment/
│   └── monitoring/
└── config/
    ├── hooks.json
    └── mcp.json
```

**Note:** Custom paths supplement default directories (commands/, agents/, skills/)

### Monorepo Organization

**Use case:** Multiple plugins in single repository

**marketplace.json:**

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools"
  },
  "metadata": {
    "pluginRoot": "./packages"
  },
  "plugins": [
    {
      "name": "formatter",
      "source": "./formatter",
      "description": "Code formatting",
      "version": "1.0.0"
    },
    {
      "name": "linter",
      "source": "./linter",
      "description": "Code linting",
      "version": "1.2.0"
    },
    {
      "name": "deployer",
      "source": "./deployer",
      "description": "Deployment automation",
      "version": "2.0.0"
    }
  ]
}
```

**Repository structure:**

```
company-tools/
├── .claude-plugin/
│   └── marketplace.json
└── packages/
    ├── formatter/
    │   └── .claude-plugin/
    ├── linter/
    │   └── .claude-plugin/
    └── deployer/
        └── .claude-plugin/
```

**Benefits:**
- Centralized marketplace management
- Shared CI/CD and tooling
- Consistent versioning across plugins
- Simplified dependency management

## Component Configuration

### Commands: Single File

**Minimal configuration:**

```json
{
  "name": "simple-deploy",
  "source": "./plugins/deploy",
  "commands": "./deploy-now.md"
}
```

**Directory structure:**

```
deploy/
├── .claude-plugin/
│   └── plugin.json
└── deploy-now.md
```

**Behavior:** Single command file loaded in addition to default commands/ directory

### Commands: Multiple Files

**Array configuration:**

```json
{
  "name": "deployment-suite",
  "source": "./plugins/deploy",
  "commands": [
    "./commands/core/deploy.md",
    "./commands/core/rollback.md",
    "./commands/experimental/preview.md"
  ]
}
```

**Use cases:**
- Organize commands by maturity (core, experimental)
- Split commands across feature areas
- Include commands from non-standard locations

### Commands: Directory

**Directory configuration:**

```json
{
  "name": "admin-tools",
  "source": "./plugins/admin",
  "commands": "./admin-commands/"
}
```

**Directory structure:**

```
admin/
├── .claude-plugin/
│   └── plugin.json
├── commands/              # Default location (still loaded)
│   └── status.md
└── admin-commands/        # Additional location
    ├── user-mgmt.md
    └── system-config.md
```

**Result:** Both commands/ and admin-commands/ are loaded

### Agents: Single vs Multiple Files

**Single agent:**

```json
{
  "name": "code-reviewer",
  "source": "./plugins/reviewer",
  "agents": "./agents/comprehensive-reviewer.md"
}
```

**Multiple agents:**

```json
{
  "name": "ci-suite",
  "source": "./plugins/ci",
  "agents": [
    "./agents/test-runner.md",
    "./agents/coverage-analyzer.md",
    "./agents/security-scanner.md"
  ]
}
```

**Agent file format:**

```markdown
---
description: What this agent specializes in
capabilities: ["capability1", "capability2"]
---

# Agent Name

Detailed description of agent's role and when to invoke it.

## Capabilities
- Specific task the agent excels at
- Another specialized capability
```

### Skills: Directory Organization

**Skills configuration:**

```json
{
  "name": "data-tools",
  "source": "./plugins/data",
  "skills": "./data-skills/"
}
```

**Directory structure:**

```
data/
├── .claude-plugin/
│   └── plugin.json
├── skills/                # Default location
│   └── csv-processor/
│       └── SKILL.md
└── data-skills/           # Additional location
    ├── sql-analyzer/
    │   ├── SKILL.md
    │   └── reference/
    └── data-visualizer/
        └── SKILL.md
```

**Result:** Both skills/ and data-skills/ are loaded

### Hooks: Inline vs File Reference

**Inline configuration:**

```json
{
  "name": "auto-formatter",
  "source": "./plugins/formatter",
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

**File reference:**

```json
{
  "name": "security-suite",
  "source": "./plugins/security",
  "hooks": "./config/hooks.json"
}
```

**hooks.json:**

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-check.sh"
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
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
        }
      ]
    }
  ]
}
```

**Available hook events:**
- `PreToolUse`: Before Claude uses any tool
- `PostToolUse`: After Claude uses any tool
- `UserPromptSubmit`: When user submits prompt
- `SessionStart`: At session beginning
- `SessionEnd`: At session end
- `PermissionRequest`: When permission dialog shown
- `Notification`: When Claude Code sends notifications
- `Stop`: When Claude attempts to stop
- `SubagentStop`: When subagent attempts to stop
- `PreCompact`: Before conversation compaction

### MCP Servers: Configuration Patterns

**Inline configuration:**

```json
{
  "name": "database-tools",
  "source": "./plugins/db",
  "mcpServers": {
    "db-connector": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data",
        "LOG_LEVEL": "info"
      }
    },
    "query-optimizer": {
      "command": "npx",
      "args": ["@company/query-optimizer", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**File reference:**

```json
{
  "name": "enterprise-integrations",
  "source": "./plugins/enterprise",
  "mcpServers": "./mcp-config.json"
}
```

**mcp-config.json:**

```json
{
  "crm-connector": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/crm",
    "args": ["--api-key", "${CRM_API_KEY}"]
  },
  "analytics-engine": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/analytics",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/analytics-config.yaml"]
  }
}
```

**MCP server fields:**
- `command`: Executable path or command
- `args`: Array of command-line arguments
- `env`: Environment variables object
- `cwd`: Working directory for server process

## Version Management

### Version Field Usage

**Semantic versioning (recommended):**

```json
{
  "name": "plugin",
  "source": "./plugin",
  "version": "2.3.1"
}
```

**Format:** MAJOR.MINOR.PATCH
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

**Version progression examples:**

```
1.0.0 → 1.0.1   # Bug fix
1.0.1 → 1.1.0   # New feature
1.1.0 → 2.0.0   # Breaking change
```

### Update Strategies

**Conservative (explicit versions):**

```json
{
  "plugins": [
    {
      "name": "stable-plugin",
      "source": "./plugin",
      "version": "1.2.3"
    }
  ]
}
```

**Benefit:** Predictable, controlled updates
**Trade-off:** Manual version bumps required

**Progressive (range versions):**

```json
{
  "plugins": [
    {
      "name": "evolving-plugin",
      "source": {
        "source": "github",
        "repo": "owner/plugin"
      },
      "version": "^1.2.0"
    }
  ]
}
```

**Benefit:** Automatic minor/patch updates
**Trade-off:** Potential for unexpected changes

**Version range formats:**
- `1.2.3`: Exact version
- `^1.2.3`: Compatible with 1.x.x (>=1.2.3, <2.0.0)
- `~1.2.3`: Approximately 1.2.x (>=1.2.3, <1.3.0)
- `>=1.2.3`: Greater than or equal

### Breaking Change Communication

**Major version bump:**

```json
{
  "name": "api-tools",
  "source": "./plugin",
  "version": "2.0.0",
  "description": "API tools - v2.0.0: Breaking changes, see CHANGELOG.md"
}
```

**CHANGELOG.md example:**

```markdown
# Changelog

## [2.0.0] - 2024-03-15

### Breaking Changes
- Removed deprecated `legacy-deploy` command
- Changed `config.yaml` format (see migration guide)
- Renamed `analyze` command to `audit`

### Migration Guide
1. Update config.yaml: rename `options` to `settings`
2. Replace `/legacy-deploy` with `/deploy --mode=legacy`
3. Update scripts using `analyze` to use `audit`

## [1.5.0] - 2024-02-01

### Added
- New `audit` command for security analysis
- Enhanced error reporting

### Fixed
- Memory leak in deployment monitor
```

### Changelog Best Practices

**Structure:**
- Group changes by type (Breaking, Added, Changed, Fixed, Deprecated, Removed)
- Include migration instructions for breaking changes
- Link to relevant issues/PRs
- Date each release

**Example entry:**

```markdown
## [1.2.0] - 2024-01-15

### Added
- `/deploy preview` command for staging deployments (#42)
- Support for multiple environment configurations

### Changed
- Improved error messages with actionable suggestions

### Fixed
- Deployment timeout on large applications (#38)
- Config validation edge cases (#40)

### Deprecated
- `legacy-deploy` command (use `/deploy --mode=legacy` instead)
  Will be removed in v2.0.0
```

## Plugin Source Management

### Local Development Workflow

**Development marketplace:**

```json
{
  "name": "local-dev",
  "owner": {
    "name": "Developer"
  },
  "plugins": [
    {
      "name": "plugin-in-progress",
      "source": "./local-plugin",
      "version": "0.1.0-dev",
      "strict": false
    }
  ]
}
```

**Workflow:**

1. **Develop locally:**
   ```bash
   cd my-marketplace
   mkdir local-plugin
   # Create plugin files
   ```

2. **Test marketplace:**
   ```shell
   /plugin marketplace add ./my-marketplace
   /plugin install plugin-in-progress@local-dev
   ```

3. **Iterate rapidly:**
   - Make changes to plugin
   - Reload plugin: `/plugin disable plugin-in-progress && /plugin enable plugin-in-progress`
   - Test changes

4. **Promote to production:**
   - Create plugin repository
   - Update source to GitHub/Git URL
   - Set `strict: true`
   - Bump version to 1.0.0

### GitHub Release Workflow

**Production marketplace entry:**

```json
{
  "name": "production-plugin",
  "source": {
    "source": "github",
    "repo": "company/production-plugin"
  },
  "version": "1.0.0",
  "strict": true
}
```

**Release process:**

1. **Prepare release:**
   ```bash
   # Update version in plugin.json
   # Update CHANGELOG.md
   # Commit changes
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Update marketplace:**
   ```json
   {
     "name": "production-plugin",
     "source": {
       "source": "github",
       "repo": "company/production-plugin"
     },
     "version": "1.0.0"
   }
   ```

3. **Communicate update:**
   - Announce in team channels
   - Document breaking changes
   - Provide migration guide if needed

4. **Monitor adoption:**
   - Track installation issues
   - Gather feedback
   - Prepare patch releases for bugs

### Private Repository Setup

**GitHub private repo:**

```json
{
  "name": "internal-tools",
  "source": {
    "source": "github",
    "repo": "company-private/internal-tools"
  },
  "description": "Internal company tools (requires access)",
  "version": "1.0.0"
}
```

**Requirements:**
- Users must have GitHub authentication configured
- Users must have repository access permissions
- Consider using SSH URLs for automation

**GitLab private repo:**

```json
{
  "name": "gitlab-internal",
  "source": {
    "source": "url",
    "url": "git@gitlab.company.com:team/plugin.git"
  },
  "description": "Internal GitLab-hosted plugin"
}
```

**Access setup:**
- SSH key authentication for GitLab
- Personal access tokens for HTTPS
- Configure git credentials in user environment

### Monorepo vs Separate Repos

**Monorepo approach:**

```
company-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── packages/
    ├── formatter/
    ├── linter/
    ├── deployer/
    └── shared-utils/
```

**Pros:**
- Centralized management
- Shared dependencies
- Consistent tooling
- Atomic cross-plugin changes

**Cons:**
- Larger repository size
- All plugins updated together
- Slower clone times

**Separate repos approach:**

```
company-plugins-marketplace/
└── .claude-plugin/
    └── marketplace.json

company-plugin-formatter/
├── .claude-plugin/
│   └── plugin.json
└── ...

company-plugin-linter/
├── .claude-plugin/
│   └── plugin.json
└── ...
```

**marketplace.json:**

```json
{
  "name": "company-tools",
  "owner": {...},
  "plugins": [
    {
      "name": "formatter",
      "source": {
        "source": "github",
        "repo": "company/plugin-formatter"
      },
      "version": "1.0.0"
    },
    {
      "name": "linter",
      "source": {
        "source": "github",
        "repo": "company/plugin-linter"
      },
      "version": "2.1.0"
    }
  ]
}
```

**Pros:**
- Independent versioning
- Smaller repository sizes
- Focused development teams
- Granular access control

**Cons:**
- More repositories to manage
- Duplicate tooling setup
- Cross-plugin changes require multiple PRs

**Recommendation:** Monorepo for small teams/tightly coupled plugins, separate repos for large organizations/independent plugins

## See Also

- [SKILL.md](../SKILL.md) - Main marketplace management guide
- [marketplace-schema.md](marketplace-schema.md) - Complete schema reference
- [team-distribution.md](team-distribution.md) - Team workflow setup
- [troubleshooting.md](troubleshooting.md) - Debugging and error resolution
