# Distribution & Versioning Guide

## Versioning

### Semantic Versioning (SemVer)
Format: MAJOR.MINOR.PATCH (e.g., "1.2.3")

- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward-compatible additions
- **PATCH**: Bug fixes, backward-compatible fixes

Examples:
- 1.0.0 → 1.0.1: Bug fix
- 1.0.1 → 1.1.0: New feature added
- 1.1.0 → 2.0.0: Breaking change

### Version Management
Update version in plugin.json:
```json
{"version": "1.2.3"}
```

Create git tags for releases:
```bash
git tag v1.2.3
git push origin v1.2.3
```

## Distribution Methods

### 1. Local Distribution (Development)
Structure:
```
project/
├── .claude/
│   └── marketplace.json
└── plugins/
    └── my-plugin/
        ├── .claude-plugin/plugin.json
        ├── commands/
        └── skills/
```

marketplace.json:
```json
{
  "name": "local-dev",
  "owner": {"name": "Dev"},
  "plugins": [{"name": "my-plugin", "source": "./plugins/my-plugin", "description": "Dev plugin"}]
}
```

Install: `/plugin install my-plugin@local-dev`

### 2. Git Repository Distribution
Host plugin as git repo:
```
github.com/user/my-plugin/
├── .claude-plugin/plugin.json
├── commands/
├── skills/
└── README.md
```

marketplace.json references repo:
```json
{
  "plugins": [
    {"name": "my-plugin", "source": "https://github.com/user/my-plugin", "description": "Plugin"}
  ]
}
```

Install: Clones repo, installs plugin

### 3. Team Distribution (Recommended)
Commit plugin to team repo:
```
team-repo/
├── .claude/
│   ├── marketplace.json
│   └── settings.json
└── plugins/
    └── team-standards/
        ├── .claude-plugin/plugin.json
        ├── commands/
        └── skills/
```

#### Team Settings Configuration

Configure `.claude/settings.json` with automatic marketplace and plugin installation:

**Basic auto-install**:
```json
{
  "plugins": {
    "autoInstall": ["plugin-name@team-tools"]
  }
}
```

**Advanced with explicit marketplace configuration**:
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    },
    "project-specific": {
      "source": {
        "source": "url",
        "url": "https://gitlab.com/team/project-plugins.git"
      }
    }
  },
  "plugins": {
    "autoInstall": [
      "code-standards@team-tools",
      "deployment-tools@team-tools",
      "project-validators@project-specific"
    ]
  }
}
```

**Workflow**:
1. Create `.claude/marketplace.json` with team plugins (local paths or remote repos)
2. Create `.claude/settings.json` with `extraKnownMarketplaces` and `autoInstall` configuration
3. Commit both files to team repository
4. When team members trust the repository, plugins install automatically on project open
5. Users can manage plugins manually afterward with `/plugin enable`, `/plugin disable`, `/plugin update`

### 4. Archive Distribution
Create tarball:
```bash
cd plugins/my-plugin
tar -czf my-plugin-1.0.0.tar.gz .
```

Host on web server:
```json
{"source": "https://example.com/plugins/my-plugin-1.0.0.tar.gz"}
```

## Testing Workflow

### Development Cycle
1. Create plugin locally
2. Test with local marketplace
3. Iterate: uninstall → modify → reinstall
4. Validate with `/plugin list` and `claude --debug`

### Team Auto-Install Testing
Before distributing team plugins with auto-install:

1. **Test individual plugins first**
   - Verify each plugin works standalone
   - Test commands, skills, hooks separately
   - Check for file reference issues

2. **Test marketplace configuration**
   - Verify `marketplace.json` has valid JSON syntax
   - Test marketplace discovery: `/plugin list @team-tools`
   - Confirm all plugin sources are accessible (local paths exist, remote repos are cloneable)

3. **Test settings.json configuration**
   - Verify `.claude/settings.json` has valid JSON syntax
   - Check `extraKnownMarketplaces` references existing marketplaces
   - Confirm `autoInstall` plugin names match marketplace entries

4. **Test auto-install workflow**
   - Create test branch with `.claude/settings.json` and marketplace
   - Add teammate as trusted user on test branch
   - Verify plugins auto-install when teammate opens project
   - Check that plugins work correctly post-installation

5. **Verify team experience**
   - Test `/plugin list` shows installed plugins
   - Test `/plugin enable` and `/plugin disable` work
   - Test `/plugin update` for plugin updates
   - Check plugin commands and skills are available

### Testing Commands
```bash
# List installed plugins
/plugin list

# Uninstall for testing
/plugin uninstall plugin-name

# Reinstall after changes
/plugin install plugin-name@marketplace-name

# Debug plugin loading
claude --debug
```

### Pre-Distribution Checklist
- [ ] plugin.json valid (all required fields)
- [ ] Version follows semver
- [ ] All component files present
- [ ] No absolute paths
- [ ] ${CLAUDE_PLUGIN_ROOT} used for scripts
- [ ] README.md with usage instructions
- [ ] Tested installation from marketplace
- [ ] Tested all commands/skills/hooks
- [ ] No sensitive data (API keys, credentials)

## Maintenance

### Updates
1. Increment version in plugin.json
2. Document changes in CHANGELOG.md
3. Commit and tag release
4. Users run `/plugin update plugin-name`

### Deprecation
1. Mark as deprecated in description
2. Provide migration path in README
3. Maintain for 2+ major versions
4. Remove from marketplace when discontinued

## Documentation Requirements

### README.md Template
```markdown
# Plugin Name

Description

## Installation
/plugin install plugin-name@marketplace-name

## Components
- Commands: /cmd1, /cmd2
- Skills: skill-name
- Hooks: PreToolUse validation

## Usage
Examples...

## Configuration
Optional config...

## Version History
See CHANGELOG.md
```

### CHANGELOG.md Template
```markdown
# Changelog

## [1.1.0] - 2024-XX-XX
### Added
- New command /feature

### Fixed
- Bug in validation

## [1.0.0] - 2024-XX-XX
Initial release
```
