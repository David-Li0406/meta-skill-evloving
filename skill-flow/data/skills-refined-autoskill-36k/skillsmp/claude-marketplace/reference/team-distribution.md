# Team Distribution Reference

Complete guide to configuring team plugin distribution, settings.json setup, and organizational workflows.

## Settings.json Configuration

### Basic Structure

Configure team marketplaces in `.claude/settings.json` at repository root:

```json
{
  "extraKnownMarketplaces": {
    "marketplace-name": {
      "source": {
        "source": "github",
        "repo": "org/marketplace-repo"
      }
    }
  }
}
```

**Location:** `.claude/settings.json` in repository root

**Effect:** When team members trust the repository, Claude Code automatically installs configured marketplaces.

### Single Marketplace

**GitHub marketplace:**

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  }
}
```

**Git URL marketplace:**

```json
{
  "extraKnownMarketplaces": {
    "internal-tools": {
      "source": {
        "source": "url",
        "url": "https://gitlab.company.com/devtools/plugins.git"
      }
    }
  }
}
```

**Local marketplace (development):**

```json
{
  "extraKnownMarketplaces": {
    "local-dev": {
      "source": {
        "source": "local",
        "path": "./marketplace"
      }
    }
  }
}
```

### Multiple Marketplaces

**Mixed sources:**

```json
{
  "extraKnownMarketplaces": {
    "company-core": {
      "source": {
        "source": "github",
        "repo": "company/core-plugins"
      }
    },
    "project-specific": {
      "source": {
        "source": "url",
        "url": "https://git.project.com/plugins.git"
      }
    },
    "experimental": {
      "source": {
        "source": "local",
        "path": "./experimental-plugins"
      }
    }
  }
}
```

**Benefits:**
- Separate stable vs experimental plugins
- Different sources for different plugin categories
- Gradual rollout of new plugins

### Complete Configuration Example

**Full settings.json with plugins:**

```json
{
  "extraKnownMarketplaces": {
    "company-standard": {
      "source": {
        "source": "github",
        "repo": "company/standard-plugins"
      }
    },
    "project-tools": {
      "source": {
        "source": "github",
        "repo": "company/project-plugins"
      }
    }
  },
  "enabledPlugins": [
    "code-formatter@company-standard",
    "linter@company-standard",
    "deployment-tools@project-tools"
  ]
}
```

## Enabled Plugins Configuration

### Basic Format

**Array of plugin specifications:**

```json
{
  "enabledPlugins": [
    "plugin-name@marketplace-name",
    "another-plugin@marketplace-name"
  ]
}
```

**Format:** `"plugin-name@marketplace-name"`

### Single Plugin

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  },
  "enabledPlugins": [
    "code-formatter@company-tools"
  ]
}
```

**Behavior:**
- Claude Code automatically installs `code-formatter` from `company-tools` marketplace
- Plugin enabled by default when repository trusted
- Updates pulled automatically based on marketplace configuration

### Multiple Plugins

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  },
  "enabledPlugins": [
    "code-formatter@company-tools",
    "linter@company-tools",
    "security-scanner@company-tools",
    "deployment-tools@company-tools"
  ]
}
```

**Installation order:** Plugins installed in array order

### Version Pinning

**Specify version in marketplace:**

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  },
  "enabledPlugins": [
    "production-plugin@company-tools"
  ]
}
```

**marketplace.json in company/plugins:**

```json
{
  "name": "company-tools",
  "owner": {...},
  "plugins": [
    {
      "name": "production-plugin",
      "source": "./production",
      "version": "1.2.3"
    }
  ]
}
```

**Result:** Team uses exact version 1.2.3

**Version ranges in marketplace:**

```json
{
  "plugins": [
    {
      "name": "evolving-plugin",
      "source": "./evolving",
      "version": "^1.2.0"
    }
  ]
}
```

**Result:** Team gets automatic minor/patch updates (>=1.2.0, <2.0.0)

### Automatic Installation Behavior

**When repository is trusted:**

1. Claude Code reads `.claude/settings.json`
2. Installs all configured marketplaces from `extraKnownMarketplaces`
3. Installs all plugins from `enabledPlugins` array
4. Enables plugins automatically
5. Plugins available immediately in new sessions

**When repository trust removed:**
- Plugins remain installed
- Must be manually disabled if desired

## Team Workflow Patterns

### Initial Setup Checklist

**1. Create marketplace repository:**

```bash
mkdir company-plugins
cd company-plugins
mkdir -p .claude-plugin
```

**2. Create marketplace.json:**

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
      "description": "Company code formatting standards",
      "version": "1.0.0"
    }
  ]
}
```

**3. Develop plugins:**

```bash
mkdir -p plugins/formatter/.claude-plugin
# Create plugin files
```

**4. Validate marketplace:**

```bash
claude plugin validate .
```

**5. Push to GitHub:**

```bash
git init
git add .
git commit -m "Initial marketplace setup"
git remote add origin git@github.com:company/plugins.git
git push -u origin main
```

**6. Configure project repositories:**

Create `.claude/settings.json` in each project:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  },
  "enabledPlugins": [
    "code-formatter@company-tools"
  ]
}
```

**7. Communicate to team:**

```markdown
# New Plugin Marketplace Available

We've set up a company plugin marketplace for Claude Code.

## For Team Members

1. Trust this repository in Claude Code
2. Plugins will install automatically
3. Use `/plugin list` to see available plugins

## Available Plugins

- **code-formatter**: Enforces company coding standards

## Documentation

See https://github.com/company/plugins for details
```

### Adding Team Members Workflow

**New team member onboarding:**

1. **Clone project repository:**
   ```bash
   git clone git@github.com:company/project.git
   cd project
   ```

2. **Open in Claude Code:**
   - Claude Code detects `.claude/settings.json`
   - Prompts to trust repository

3. **Trust repository:**
   - User accepts trust prompt
   - Marketplaces install automatically
   - Plugins enable automatically

4. **Verify installation:**
   ```shell
   /plugin marketplace list
   /plugin list
   ```

**No manual configuration required** - plugins work immediately after trusting repository.

### Repository Trust Process

**Security model:**

- Claude Code requires explicit trust for repositories
- Trust enables `.claude/settings.json` configuration
- Prevents arbitrary code execution from untrusted sources

**Trust workflow:**

1. **User opens repository:**
   - Claude Code detects settings.json
   - Shows trust dialog

2. **User reviews configuration:**
   - Inspects marketplace sources
   - Reviews enabled plugins
   - Checks plugin sources

3. **User grants trust:**
   - Marketplaces install
   - Plugins enable
   - Settings.json becomes active

4. **User can revoke trust:**
   - Removes marketplace/plugin auto-installation
   - Existing plugins remain but not auto-updated

**Best practices:**
- Document marketplace contents clearly
- Use private repositories for sensitive plugins
- Review plugin sources before trusting
- Establish organizational trust policies

### Plugin Update Workflow

**Update process:**

1. **Update plugin in marketplace repository:**

```bash
cd company-plugins
# Make changes to plugin
# Update version in plugin.json and marketplace.json
git commit -m "feat(formatter): add new formatting rules

Version 1.1.0"
git push
```

2. **Update marketplace.json:**

```json
{
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "version": "1.1.0"
    }
  ]
}
```

3. **Team members update:**

```shell
/plugin marketplace update company-tools
/plugin update code-formatter
```

**Or automatic update (if version range used):**

```json
{
  "plugins": [
    {
      "name": "code-formatter",
      "version": "^1.0.0"
    }
  ]
}
```

Team gets updates automatically on next marketplace refresh.

4. **Communicate changes:**

```markdown
# Plugin Update: code-formatter v1.1.0

## Changes
- Added support for new file types
- Improved error messages
- Fixed formatting edge cases

## Action Required
Run `/plugin update code-formatter` to get latest version

## Breaking Changes
None
```

### Rollback Strategies

**Scenario: Plugin update causes issues**

**Option 1: Revert marketplace version:**

```json
{
  "plugins": [
    {
      "name": "problematic-plugin",
      "version": "1.0.0"
    }
  ]
}
```

Team members run:
```shell
/plugin marketplace update company-tools
/plugin update problematic-plugin
```

**Option 2: Disable plugin temporarily:**

```json
{
  "enabledPlugins": []
}
```

Team members pull settings.json update and restart Claude Code.

**Option 3: Git revert marketplace repository:**

```bash
cd company-plugins
git revert HEAD
git push
```

Team members refresh marketplace to get reverted version.

**Option 4: Emergency communication:**

```markdown
# URGENT: Disable problematic-plugin

A critical issue was found in problematic-plugin v1.1.0.

## Immediate Action
Run: `/plugin disable problematic-plugin`

## Fix Timeline
We're releasing v1.1.1 with a fix within 2 hours.

## Details
[Describe issue and impact]
```

## Organization Best Practices

### Private vs Public Marketplaces

**Public marketplaces:**

```json
{
  "extraKnownMarketplaces": {
    "community-tools": {
      "source": {
        "source": "github",
        "repo": "community/claude-plugins"
      }
    }
  }
}
```

**Use cases:**
- Open source plugins
- Community contributions
- Public documentation
- Cross-organization sharing

**Benefits:**
- Wide accessibility
- Community contributions
- No authentication required

**Private marketplaces:**

```json
{
  "extraKnownMarketplaces": {
    "internal-tools": {
      "source": {
        "source": "github",
        "repo": "company-private/plugins"
      }
    }
  }
}
```

**Use cases:**
- Proprietary tools
- Internal workflows
- Sensitive integrations
- Compliance-required plugins

**Benefits:**
- Access control
- Intellectual property protection
- Compliance adherence

**Requirements:**
- Team members need repository access
- GitHub authentication configured
- SSH keys or tokens for automation

### Marketplace Organization Strategies

**Single marketplace (small teams):**

```
company-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── formatter/
    ├── linter/
    └── deployer/
```

**Benefits:**
- Simple management
- Single source of truth
- Easy discovery

**Multiple marketplaces (large organizations):**

```
company-core-plugins/        # Stable, company-wide
company-experimental/        # Beta, opt-in
project-alpha-plugins/       # Project-specific
```

**settings.json:**

```json
{
  "extraKnownMarketplaces": {
    "company-core": {
      "source": {
        "source": "github",
        "repo": "company/core-plugins"
      }
    },
    "project-alpha": {
      "source": {
        "source": "github",
        "repo": "company/alpha-plugins"
      }
    }
  },
  "enabledPlugins": [
    "formatter@company-core",
    "linter@company-core",
    "alpha-tool@project-alpha"
  ]
}
```

**Benefits:**
- Separation of concerns
- Different update cadences
- Granular access control
- Reduced blast radius

### Documentation Requirements

**Marketplace README.md:**

```markdown
# Company Claude Plugins

Internal plugin marketplace for Claude Code.

## Available Plugins

### code-formatter (v1.0.0)
- **Description**: Company coding standards enforcement
- **Commands**: `/format`, `/format-check`
- **Category**: Development

### deployment-tools (v2.1.0)
- **Description**: Automated deployment workflows
- **Commands**: `/deploy`, `/rollback`, `/deployment-status`
- **Category**: DevOps

## Installation

This marketplace is automatically configured in company projects.

For manual installation:
```shell
/plugin marketplace add github.com/company/plugins
/plugin install code-formatter@company-plugins
```

## Support

- Issues: https://github.com/company/plugins/issues
- Docs: https://docs.company.com/claude-plugins
- Contact: devtools@company.com
```

**Plugin README.md template:**

```markdown
# Plugin Name

Brief description.

## Features

- Feature 1
- Feature 2

## Usage

```shell
/command-name [args]
```

## Configuration

[If applicable]

## Troubleshooting

Common issues and solutions.

## Changelog

See [CHANGELOG.md](CHANGELOG.md)
```

### Security Considerations

**Code review:**
- Review plugin code before adding to marketplace
- Audit hooks and scripts for security issues
- Validate external API integrations

**Access control:**
- Use private repositories for sensitive plugins
- Implement branch protection
- Require PR approvals for marketplace changes

**Secrets management:**
- Never commit secrets to plugin repositories
- Use environment variables for sensitive data
- Document secret configuration requirements

**Trust model:**
- Educate team on repository trust implications
- Establish organizational trust policies
- Regular security audits of marketplace plugins

**Example security policy:**

```markdown
# Plugin Security Policy

## Approval Process

1. Plugin PR submitted to marketplace
2. Security review by DevSecOps team
3. Code review by 2+ senior engineers
4. Testing in isolated environment
5. Approval by team lead

## Security Requirements

- No hardcoded secrets
- All external API calls documented
- Hooks limited to read-only operations (exceptions require approval)
- MCP servers sandboxed appropriately

## Incident Response

If security issue found:
1. Immediately revert problematic version
2. Notify all users via Slack #claude-code
3. Issue fixed version within 24 hours
4. Post-mortem within 48 hours
```

### Governance Policies

**Plugin approval workflow:**

1. **Proposal**: Developer submits plugin proposal
2. **Review**: Team lead reviews use case and scope
3. **Development**: Plugin developed following standards
4. **Security audit**: Security team reviews code
5. **Testing**: QA testing in isolated environment
6. **Approval**: Team lead approves marketplace addition
7. **Documentation**: README and usage docs completed
8. **Rollout**: Added to marketplace with communication

**Maintenance responsibilities:**

- **Plugin owners**: Maintain plugin code, fix bugs, add features
- **Marketplace maintainers**: Manage marketplace.json, coordinate updates
- **Security team**: Regular audits, vulnerability response
- **DevTools team**: Infrastructure, CI/CD, documentation

**Version management policy:**

```markdown
# Version Management Policy

## Versioning

All plugins use semantic versioning (MAJOR.MINOR.PATCH).

## Update Cadence

- **Patch updates**: As needed for bug fixes
- **Minor updates**: Monthly release cycle
- **Major updates**: Quarterly with migration guides

## Communication

- Patch: Changelog entry
- Minor: Changelog + Slack announcement
- Major: Changelog + Slack + Email + Migration guide

## Deprecation

- Deprecated features: 2 minor version warning period
- Removed features: Major version bump only
- Migration guide required for all removals
```

## See Also

- [SKILL.md](../SKILL.md) - Main marketplace management guide
- [marketplace-schema.md](marketplace-schema.md) - Complete schema reference
- [plugin-management.md](plugin-management.md) - Plugin configuration details
- [troubleshooting.md](troubleshooting.md) - Debugging and error resolution
