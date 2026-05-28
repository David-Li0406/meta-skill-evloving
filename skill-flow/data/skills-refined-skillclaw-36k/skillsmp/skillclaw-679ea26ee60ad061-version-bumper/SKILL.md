---
name: version-bumper
description: Use this skill to automatically manage semantic version updates across plugin.json and marketplace catalog when relevant phrases are detected, ensuring version consistency in the repository.
---

# Version Bumper

## Purpose
This skill automates the management of semantic version updates for Claude Code plugins, ensuring consistency across `plugin.json`, `marketplace.extended.json`, and git tags.

## Trigger Keywords
- "bump version"
- "update version"
- "release"
- "new release"
- "major version"
- "minor version"
- "patch version"
- "increment version"
- "version update"

## Semantic Versioning

**Format:** MAJOR.MINOR.PATCH (e.g., 2.1.3)

**Rules:**
- **MAJOR (2.x.x)** - Breaking changes, incompatible API changes
- **MINOR (x.1.x)** - New features, backward compatible
- **PATCH (x.x.3)** - Bug fixes, backward compatible

**Examples:**
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.0` → `1.1.0` (new feature)
- `1.0.0` → `2.0.0` (breaking change)

## Version Bump Process

When activated, I will:

1. **Identify Current Version**
   ```bash
   # Read plugin version
   current=$(jq -r '.version' .claude-plugin/plugin.json)
   echo "Current version: $current"
   ```

2. **Determine Bump Type**
   - From user request (major/minor/patch)
   - Suggest based on changes
   - Ask user which type if unclear

3. **Calculate New Version**
   ```bash
   # Example for patch bump: 1.2.3 → 1.2.4
   IFS='.' read -r major minor patch <<< "$current"
   new_version="$major.$minor.$((patch + 1))"
   ```

4. **Update Files**
   - Update `.claude-plugin/plugin.json`
   - Update `.claude-plugin/marketplace.extended.json`
   - Sync to `marketplace.json`

5. **Validate Consistency**
   - Ensure all files have the same version
   - Check no other plugins use this version
   - Validate semver format

6. **Create Git Tag (Optional)**
   ```bash
   git tag -a "v$new_version" -m "Release v$new_version"
   ```

## Update Locations

### 1. Plugin JSON
```json
// .claude-plugin/plugin.json
{
  "name": "plugin-name",
  "version": "1.2.4",  // ← Update here
  ...
}
```

### 2. Marketplace Extended
```json
// .claude-plugin/marketplace.extended.json
{
  "plugins": [
    {
      "name": "plugin-name",
      "version": "1.2.4",  // ← Update here
      ...
    }
  ]
}
```

### 3. Sync CLI Catalog
```bash
npm run sync-marketplace
# Regenerates marketplace.json with new version
```