# Plugin Distribution

Complete guide for distributing Claude Code plugins via marketplaces and team configuration.

## Overview

Distribution involves:

1. **Create plugins** - Build your plugin(s) with components
2. **Create marketplace.json** - Catalog your plugins
3. **Host marketplace** - Push to GitHub/GitLab
4. **Share with users** - They add and install

## Marketplace Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json    # Required: marketplace catalog
├── plugins/
│   ├── formatter/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── commands/
│   └── deploy-tools/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       └── hooks/
└── README.md
```

## Creating marketplace.json

Location: `.claude-plugin/marketplace.json`

### Minimal Example

```json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "formatter",
      "source": "./plugins/formatter",
      "description": "Code formatting tools"
    }
  ]
}
```

### Complete Example

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "metadata": {
    "description": "Official company development tools",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      },
      "keywords": ["formatting", "linting"],
      "category": "development"
    },
    {
      "name": "deploy-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Marketplace Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Marketplace identifier (kebab-case) |
| `owner` | object | Maintainer information |
| `plugins` | array | List of available plugins |

### Owner Object

```json
{
  "owner": {
    "name": "Team Name",       // Required
    "email": "team@company.com" // Optional
  }
}
```

### Metadata Object

```json
{
  "metadata": {
    "description": "Brief marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"  // Base path for relative sources
  }
}
```

With `pluginRoot`, you can write:
```json
{ "name": "formatter", "source": "formatter" }
```
Instead of:
```json
{ "name": "formatter", "source": "./plugins/formatter" }
```

### Reserved Names

These marketplace names are reserved:
- `claude-code-marketplace`
- `claude-code-plugins`
- `claude-plugins-official`
- `anthropic-marketplace`
- `anthropic-plugins`
- `agent-skills`
- `life-sciences`

## Plugin Entries

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `source` | string\|object | Where to fetch plugin |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief plugin description |
| `version` | string | Plugin version |
| `author` | object | Author info (`name`, `email`) |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | SPDX license identifier |
| `keywords` | array | Discovery tags |
| `category` | string | Plugin category |
| `tags` | array | Search tags |
| `strict` | boolean | Require plugin.json in source |
| `commands` | string\|array | Custom command paths |
| `agents` | string\|array | Custom agent paths |
| `hooks` | string\|object | Hook configuration |
| `mcpServers` | string\|object | MCP configuration |
| `lspServers` | string\|object | LSP configuration |

### Strict Mode

| `strict` Value | Behavior |
|----------------|----------|
| `true` (default) | Plugin source must have `plugin.json` |
| `false` | Marketplace entry defines everything |

Use `strict: false` for simple plugins defined entirely in marketplace:

```json
{
  "name": "simple-command",
  "source": "./plugins/simple",
  "description": "A simple command",
  "strict": false,
  "commands": ["./plugins/simple/commands/"]
}
```

## Plugin Sources

### Relative Path

For plugins in same repository:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub Repository

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v1.0.0",     // Optional: branch/tag
    "path": "./plugin"   // Optional: subdirectory
  }
}
```

### Git URL

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Hosting

### GitHub (Recommended)

1. Create repository for marketplace
2. Add `.claude-plugin/marketplace.json`
3. Add plugins in `plugins/` directory
4. Push to GitHub

Users add via:
```
/plugin marketplace add owner/repo
```

### GitLab / Other Git Hosts

Same structure, full URL required:

```
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Private Repositories

For private repos, ensure users have access:
- GitHub: User must be collaborator or org member
- GitLab: User needs read access

## Team Distribution

### Repository-Level Configuration

Add to `.claude/settings.json` in your project:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  }
}
```

Team members are prompted to add marketplace when trusting project.

### Pre-Enable Plugins

Enable specific plugins by default:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "formatter@team-tools": true,
    "deploy-tools@team-tools": true
  }
}
```

## Enterprise Restrictions

### strictKnownMarketplaces

Managed setting that restricts which marketplaces users can add.

**Disable all marketplace additions:**
```json
{
  "strictKnownMarketplaces": []
}
```

**Allow only specific marketplaces:**
```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "company/approved-plugins"
    },
    {
      "source": "github",
      "repo": "company/security-tools",
      "ref": "v2.0"
    }
  ]
}
```

### How Restrictions Work

- Set in managed settings (not user-configurable)
- Validated before any network requests
- Exact matching required
- Prevents unauthorized marketplace access

## Validation

### Validate Marketplace

```bash
claude plugin validate ./my-marketplace
```

Or in Claude Code:
```
/plugin validate ./my-marketplace
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `File not found: marketplace.json` | Missing manifest | Create `.claude-plugin/marketplace.json` |
| `Invalid JSON syntax` | Syntax error | Check commas, quotes |
| `Duplicate plugin name` | Name collision | Use unique names |
| `Path traversal not allowed` | `..` in path | Use paths within marketplace |

### Warnings

| Warning | Meaning |
|---------|---------|
| `No plugins defined` | Empty plugins array |
| `No description provided` | Missing marketplace description |

## Testing

### Test Locally

```bash
# Add marketplace
/plugin marketplace add ./my-marketplace

# Install plugin
/plugin install my-plugin@my-marketplace

# Test plugin
/my-plugin:command

# Update marketplace
/plugin marketplace update my-marketplace
```

### Test Before Publishing

1. Validate JSON syntax
2. Add marketplace locally
3. Install each plugin
4. Test all commands, agents, hooks
5. Verify LSP and MCP servers start

## Workflow: Publish a Marketplace

### Prerequisites
- [ ] GitHub/GitLab repository created
- [ ] Plugin(s) created and tested
- [ ] README.md written

### Steps

1. **Create Marketplace File**
   - [ ] Create `.claude-plugin/marketplace.json`
   - [ ] Add `name`, `owner`, and `plugins` array
   - [ ] Define each plugin entry

2. **Organize Plugins**
   - [ ] Place plugins in `plugins/` directory
   - [ ] Ensure each has `.claude-plugin/plugin.json`
   - [ ] Verify all paths are relative

3. **Validate**
   - [ ] Run `claude plugin validate .`
   - [ ] Fix any errors or warnings

4. **Test Locally**
   - [ ] Add marketplace: `/plugin marketplace add ./`
   - [ ] Install each plugin
   - [ ] Test functionality

5. **Publish**
   - [ ] Commit all files
   - [ ] Push to remote repository
   - [ ] Tag release if using versions

6. **Document**
   - [ ] Update README with installation instructions
   - [ ] List available plugins
   - [ ] Provide usage examples

### Validation
- [ ] Marketplace validates without errors
- [ ] All plugins install correctly
- [ ] Commands work as expected
- [ ] Hooks fire correctly
- [ ] MCP/LSP servers start

## User Installation

Share these instructions with users:

### From GitHub

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Install plugins
/plugin install plugin-name@marketplace-name

# List available plugins
/plugin
```

### From Other Hosts

```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Update Marketplace

```bash
/plugin marketplace update marketplace-name
```

## Version Management

### Plugin Versions

Update in `plugin.json`:

```json
{
  "version": "1.2.0"
}
```

### Marketplace Versions

Update in `marketplace.json` metadata:

```json
{
  "metadata": {
    "version": "2.0.0"
  }
}
```

### Git Tags

Tag releases for pinned installations:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Users can pin to version:

```json
{
  "source": {
    "source": "github",
    "repo": "company/plugins",
    "ref": "v1.0.0"
  }
}
```

## Plugin Caching

**Important:** Plugins are copied to a cache directory when installed.

### Implications

- Files outside plugin directory are not copied
- Paths like `../shared-utils` won't work
- Use symlinks for shared dependencies

### Workarounds

**Symlinks:**
```bash
# Inside plugin directory
ln -s /path/to/shared-utils ./shared-utils
```

**Restructure marketplace:**
```json
{
  "name": "my-plugin",
  "source": "./",
  "commands": ["./plugins/my-plugin/commands/"],
  "strict": false
}
```

## See Also

- [SKILL.md](./SKILL.md) - Main plugin creation guide
- [MANIFEST.md](./MANIFEST.md) - Plugin manifest reference
- [COMPONENTS.md](./COMPONENTS.md) - Component type documentation
