# Marketplace Configuration

## marketplace.json Schema

```json
{
  "name": "marketplace-identifier",
  "owner": {"name": "Owner Name"},
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./local-path",
      "description": "Plugin description"
    },
    {
      "name": "other-plugin",
      "source": "https://github.com/user/repo",
      "description": "Remote plugin"
    }
  ]
}
```

## Field Specifications

### Top-Level Fields
- **name** (string, required): Marketplace identifier
- **owner** (object, required): {name: "Owner Name"}
- **plugins** (array, required): Plugin entries

### Plugin Entry Fields
- **name** (string, required): Plugin identifier
- **source** (string|object, required): Location (see sources below)
- **description** (string, required): Brief description

### Optional Plugin Entry Fields
- **strict** (boolean, default: true): When true, plugin must include plugin.json. When false, marketplace entry serves as complete manifest if plugin.json is missing
- **category** (string): Plugin category for organization (e.g., "productivity", "development", "testing")
- **tags** (array): Additional tags for searchability and discovery (e.g., ["formatter", "linter", "automation"])

## Source Types

### Local Path (String Format)
```json
{"source": "./plugins/my-plugin"}
```
Relative to marketplace.json location

### GitHub Repository (Object Format)
```json
{"source": {"source": "github", "repo": "owner/plugin-repo"}}
```
Clones repo from GitHub at installation

### Git Repository (Object Format)
```json
{"source": {"source": "url", "url": "https://gitlab.com/team/plugin.git"}}
```
Clones any git repository URL at installation

### URL/HTTP Link (String Format)
```json
{"source": "https://github.com/user/plugin-repo"}
```
Direct URL clones repo or downloads archive at installation

### Tarball/Archive (String Format)
```json
{"source": "https://example.com/plugin.tar.gz"}
```
Downloads and extracts archive at installation

## Distribution Patterns

### Team Marketplace (Project)
Location: `.claude/marketplace.json`
```json
{
  "name": "team-tools",
  "owner": {"name": "Engineering Team"},
  "plugins": [
    {"name": "code-standards", "source": "./plugins/code-standards", "description": "Team coding standards"}
  ]
}
```
Committed to git, team-shared

### Personal Marketplace
Location: `~/.claude/marketplace.json`
```json
{
  "name": "personal-tools",
  "owner": {"name": "User Name"},
  "plugins": [
    {"name": "my-workflow", "source": "./plugins/my-workflow", "description": "Personal workflow"}
  ]
}
```
User-specific, not committed

### Public Marketplace
Hosted remotely, accessed by URL:
```bash
/plugin install plugin-name@https://example.com/marketplace.json
```

## Installation Commands

```bash
# Install from marketplace
/plugin install plugin-name@marketplace-name

# Install from specific marketplace URL
/plugin install plugin-name@https://example.com/marketplace.json

# List available plugins in marketplace
/plugin list @marketplace-name

# Update plugin
/plugin update plugin-name
```

## Auto-Installation (Team)

Configure in `.claude/settings.json`:
```json
{
  "plugins": {
    "autoInstall": ["plugin-name@team-tools"]
  }
}
```
Plugins install automatically when team members open project
