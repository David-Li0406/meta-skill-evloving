---
name: update-plugin
description: Update the celestia-engineering Claude Code plugin with latest changes from GitHub main branch
---

# Update Plugin Skill

Update the installed celestia-engineering plugin with latest changes from GitHub.

## When to Use

- User says "update the plugin", "install latest changes", or similar
- After new version is merged to celestia-engineering main branch on GitHub

## Update Process

### Step 1: Pull latest from GitHub
```bash
cd ~/.claude/plugins/marketplaces/celestia-marketplace/plugins/celestia-engineering
git fetch origin main
git reset --hard origin/main
```

### Step 2: Get version from updated source
```bash
cat ~/.claude/plugins/marketplaces/celestia-marketplace/plugins/celestia-engineering/.claude-plugin/plugin.json
```
Extract the version number (e.g., "2.2.0").

### Step 3: Create cache directory for new version
```bash
VERSION="X.Y.Z"  # from step 2

# Create cache directory
mkdir -p ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/$VERSION

# Copy all plugin files to cache
cp -r ~/.claude/plugins/marketplaces/celestia-marketplace/plugins/celestia-engineering/* \
   ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/$VERSION/
cp -r ~/.claude/plugins/marketplaces/celestia-marketplace/plugins/celestia-engineering/.claude-plugin \
   ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/$VERSION/
```

### Step 4: Update installed_plugins.json
Edit `~/.claude/plugins/installed_plugins.json` and update the celestia-engineering entry:
- Change `installPath` to include new version path
- Change `version` to new version
- Update `lastUpdated` to current ISO timestamp

Example:
```json
"celestia-engineering@celestia-marketplace": [
  {
    "scope": "user",
    "installPath": "/Users/USERNAME/.claude/plugins/cache/celestia-marketplace/celestia-engineering/X.Y.Z",
    "version": "X.Y.Z",
    "installedAt": "2026-01-13T22:50:00.000Z",
    "lastUpdated": "2026-01-15T00:00:00.000Z"
  }
]
```

### Step 5: Cleanup old cache (optional)
```bash
# List existing cache versions
ls ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/

# Remove old versions if desired
rm -rf ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/OLD_VERSION
```

### Step 6: Verify
```bash
cat ~/.claude/plugins/cache/celestia-marketplace/celestia-engineering/$VERSION/.claude-plugin/plugin.json
```

## Important Notes

1. **Restart required**: User must restart Claude Code (`/exit`) for changes to take effect
2. **Source of truth**: GitHub main branch (https://github.com/celestiaorg/celestia-engineering)
3. **Version format**: Semantic versioning (MAJOR.MINOR.PATCH)
