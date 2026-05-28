---
name: update-plugin
description: Update plugin versions based on changes from main branch
---

# Update Plugin Version

## Overview

Analyze changes in the current branch compared to main and update plugin versions accordingly. Detects changed plugins, analyzes the nature of changes, updates CHANGELOGs, and updates version numbers appropriately following semantic versioning.

## Core Principles

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes, API changes, removed features
- MINOR: New commands, new functions, new capabilities
- PATCH: Bug fixes, documentation updates, minor improvements
- Update CHANGELOG before updating version numbers
- Marketplace version follows the highest change level across all plugins

## Instructions

1. **Detect Changed Plugins**

   Run `git diff main...HEAD --name-only` to get all changed files.

   Identify which plugins have changes by looking for files under `plugins/*/` directories.

2. **Analyze Changes for Each Plugin**

   For each changed plugin, examine the diff to determine the change type:
   - **MAJOR** (breaking changes): API changes, removed features, incompatible changes
   - **MINOR** (new features): New commands, new functions, new capabilities
   - **PATCH** (bug fixes): Bug fixes, documentation updates, minor improvements

   Use `git diff main...HEAD -- plugins/<plugin-name>/` to see the specific changes.

3. **Version Update Rules**

   Current version format: `MAJOR.MINOR.PATCH`
   - MAJOR: Increment first number, reset others to 0 (e.g., 1.2.3 -> 2.0.0)
   - MINOR: Increment second number, reset patch to 0 (e.g., 1.2.3 -> 1.3.0)
   - PATCH: Increment third number (e.g., 1.2.3 -> 1.2.4)

4. **Update Plugin CHANGELOG (For Each Changed Plugin)**

   Update `plugins/<plugin-name>/CHANGELOG.md` with the new version entry:

   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added

   - New feature or command (if applicable)

   ### Changed

   - Modified behavior or updated functionality (if applicable)

   ### Fixed

   - Bug fix description (if applicable)

   ### Removed

   - Removed feature or command (if applicable)
   ```

   Guidelines:
   - Use today's date in YYYY-MM-DD format
   - Only include relevant sections (Added, Changed, Fixed, Removed)
   - Keep entries concise using bullet points
   - Place new version entry at the top, below the header

5. **Update Plugin Version in Marketplace**

   After updating the CHANGELOG, update the plugin's version in `.claude-plugin/marketplace.json`:
   - Find the plugin entry in the `plugins` array
   - Update its `version` field to the new version
   - If `plugins/<plugin-name>/pyproject.toml` exists, also update the `version` field in `[project]` section

   **Version Synchronization Requirement**: When a plugin has both a marketplace.json entry and a pyproject.toml file, both versions MUST be updated to the same value. The pyproject.toml version analysis is independent from Claude prompt changes - the plugin as a whole should always have a single consistent version across all version declarations.

6. **Update Marketplace Root Version**

   After all plugin versions are updated, update the root `metadata.version` in `.claude-plugin/marketplace.json`:
   - Determine the highest change level across all modified plugins:
     - If ANY plugin has a MAJOR change: increment marketplace MAJOR version
     - If ANY plugin has a MINOR change (and no MAJOR): increment marketplace MINOR version
     - If ALL plugins have PATCH changes only: increment marketplace PATCH version

   Example: 3 plugins changed (2 patch, 1 minor) -> marketplace MINOR version +1

7. **Commit Version Updates**

   Use the /git-commit command to commit with message format:

   Single plugin:

   ```
   Bump <plugin-name> version to X.Y.Z (<change-type>)
   ```

   Multiple plugins:

   ```
   Bump plugin versions

   - <plugin1>: X.Y.Z (minor)
   - <plugin2>: A.B.C (patch)
   ```

## Output Guidance

Report the analysis and version changes:

```
## Plugin Version Updates

### Changed Plugins Detected
- plugin-name: [change type] (files changed: X)

### CHANGELOG Updates
- plugin-name: Added entry for vX.Y.Z

### Version Updates Applied
| Plugin | Old Version | New Version | Change Type |
|--------|-------------|-------------|-------------|
| plugin-name | 1.2.3 | 1.3.0 | minor |
| marketplace | 0.1.0 | 0.2.0 | minor |

### Commit
[Commit hash and message]
```
