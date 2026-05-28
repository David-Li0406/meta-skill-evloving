---
name: obsidian-plugin-release
description: Automate Obsidian plugin release workflows including version management, CHANGELOG updates, building, PR creation, and GitHub Release publishing. Use when preparing initial releases or version updates for Obsidian community plugins. Handles version consistency across manifest.json, package.json, and versions.json with support for interactive workflows and individual utility scripts.
---

# Obsidian Plugin Release

Automate the release process for Obsidian community plugins from version bumping through GitHub Release creation.

## Overview

This skill provides Python scripts for managing Obsidian plugin releases:

- **Version Management**: Check consistency and bump versions across all config files
- **CHANGELOG Automation**: Generate and update CHANGELOG.md with proper formatting
- **Build Verification**: Build plugin and verify required artifacts exist
- **GitHub Integration**: Create PRs and Releases using GitHub CLI (gh)
- **Interactive Workflow**: Guided step-by-step release process

## Quick Start

### Interactive Workflow (Recommended for First-Time Users)

Run the interactive workflow for guided release:

```bash
python3 .claude/skills/obsidian-plugin-release/scripts/release_workflow.py
```

This will guide you through:
1. Pre-flight checks (git status, current version)
2. Version selection (initial or bump type)
3. CHANGELOG generation/update
4. Plugin build
5. Git commit and push
6. Next steps guidance

### Individual Commands (For Advanced Users)

Use individual scripts for specific tasks:

```bash
# Check version consistency
python3 scripts/check_versions.py [project_root]

# Bump version
python3 scripts/bump_version.py <major|minor|patch|X.Y.Z> [project_root]

# Build plugin
python3 scripts/build_plugin.py [project_root]

# Update CHANGELOG
python3 scripts/update_changelog.py <create|update> <version> <owner/repo> [project_root]

# Create PR (requires gh CLI)
python3 scripts/create_pr.py <from_branch> <to_branch> <version> [project_root]

# Create GitHub Release (requires gh CLI)
python3 scripts/create_release.py <version> [--publish] [project_root]
```

## Workflow Patterns

### Pattern 1: Initial Release (First-Time)

For the first public release of an Obsidian plugin:

```bash
# 1. Run interactive workflow
python3 .claude/skills/obsidian-plugin-release/scripts/release_workflow.py

# Select "1. Initial release"
# Follow prompts to set version (default 1.0.0)
# Edit CHANGELOG.md when prompted
# Workflow will build, commit, and push

# 2. Create PR manually or use script
python3 scripts/create_pr.py feature/core main 1.0.0

# 3. Merge PR on GitHub

# 4. Checkout main and build
git checkout main
git pull
python3 scripts/build_plugin.py

# 5. Create release
python3 scripts/create_release.py 1.0.0 --publish
```

### Pattern 2: Version Update (Subsequent Releases)

For updating existing plugins:

```bash
# 1. Run interactive workflow
python3 .claude/skills/obsidian-plugin-release/scripts/release_workflow.py

# Select "2. Version update"
# Choose bump type: patch (bugs), minor (features), or major (breaking)
# Edit CHANGELOG.md when prompted
# Workflow will build, commit, and push

# 2. Create PR
python3 scripts/create_pr.py feature/new-feature main 1.1.0

# 3. Merge PR on GitHub

# 4. Checkout main and build
git checkout main
git pull
python3 scripts/build_plugin.py

# 5. Create release
python3 scripts/create_release.py 1.1.0 --publish
```

**Note:** For manual step-by-step control, use individual scripts documented in "Script Reference" section below.

## Script Reference

### check_versions.py

Validates version consistency across config files.

**Checks:**
- `manifest.json` version exists
- `package.json` version matches manifest (if exists)
- `versions.json` has entry for current version
- `versions.json` entry matches `manifest.json` minAppVersion

**Usage:**
```bash
python3 scripts/check_versions.py [project_root]
```

**Exit codes:**
- 0: All versions consistent
- 1: Inconsistency found

### bump_version.py

Updates version in all config files atomically.

**Updates:**
- `manifest.json`: version field
- `package.json`: version field (if exists)
- `versions.json`: adds new entry, removes old

**Usage:**
```bash
# Semantic version bump
python3 scripts/bump_version.py patch    # 1.0.0 → 1.0.1
python3 scripts/bump_version.py minor    # 1.0.0 → 1.1.0
python3 scripts/bump_version.py major    # 1.0.0 → 2.0.0

# Explicit version
python3 scripts/bump_version.py 1.5.3
```

### build_plugin.py

Builds the plugin and verifies artifacts.

**Actions:**
1. Runs `npm run build`
2. Verifies `main.js` exists
3. Verifies `manifest.json` exists
4. Reports file sizes

**Usage:**
```bash
python3 scripts/build_plugin.py [project_root]
```

**Exit codes:**
- 0: Build successful, artifacts present
- 1: Build failed or artifacts missing

### update_changelog.py

Creates or updates CHANGELOG.md using Keep a Changelog format.

**Modes:**
- `create`: Generate initial CHANGELOG.md with TODO sections
- `update`: Add new version section to existing CHANGELOG.md

**Usage:**
```bash
# Create initial CHANGELOG
python3 scripts/update_changelog.py create 1.0.0 owner/repo

# Update for new version
python3 scripts/update_changelog.py update 1.1.0 owner/repo
```

**Generated Structure:**
The script follows Keep a Changelog format with these requirements:

```markdown
## [Unreleased]

## [1.1.0] - 2026-01-17
### Added
- New feature

## [1.0.0] - 2026-01-16
### Added
- Initial release

[Unreleased]: https://github.com/owner/repo/compare/1.1.0...HEAD
[1.1.0]: https://github.com/owner/repo/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/owner/repo/releases/tag/1.0.0
```

**⚠️ CRITICAL: Link Definition Placement**
- ALL link definitions MUST be placed at the end of the file
- Do NOT place links between version sections
- Keep all `[version]:` definitions together at the bottom

**Notes:**
- Always leaves TODO markers for manual editing
- Automatically extracts previous version for comparison links
- Follows Keep a Changelog format
- Verify link definitions remain at file end after manual edits

### create_pr.py

Creates GitHub Pull Request using `gh` CLI.

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated

**Generated PR includes:**
- Title: "Release vX.Y.Z"
- Body: Release checklist and post-merge steps
- Base/head branch configuration

**Usage:**
```bash
python3 scripts/create_pr.py feature/core main 1.0.0
```

**Setup gh CLI:**
```bash
# Install: https://cli.github.com/
# Authenticate:
gh auth login
```

### create_release.py

Creates GitHub Release with build artifacts.

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated
- Build artifacts present: `main.js`, `manifest.json`, `styles.css` (optional)

**Features:**
- Extracts release notes from CHANGELOG.md
- Attaches build artifacts automatically
- Creates draft by default (use `--publish` to publish immediately)
- Uses tag without 'v' prefix (Obsidian requirement)

**CHANGELOG Integration:**
- Extracts content from version section: `## [X.Y.Z] - YYYY-MM-DD`
- Includes subsections: `### Added`, `### Changed`, `### Fixed`, etc.
- Automatically appends installation instructions
- Link definitions at file end are excluded from extraction

**Generated Release Example:**
```
Tag: 1.1.4
Title: Release 1.1.4
Assets: main.js, manifest.json, styles.css

Notes:
## Changed
- Move command/agent editor Save and Cancel buttons into a sticky header

## Installation
### Manual Installation
1. Download main.js, manifest.json, and styles.css
2. Place in: <VaultFolder>/.obsidian/plugins/<plugin-id>/
3. Restart Obsidian and enable the plugin
```

**Usage:**
```bash
# Create draft release (recommended)
python3 scripts/create_release.py 1.0.0

# Create and publish immediately
python3 scripts/create_release.py 1.0.0 --publish

# Publish draft later via gh CLI
gh release edit 1.0.0 --draft=false
```

## Important: Obsidian-Specific Requirements

### Tag Naming Convention

❌ **WRONG**: `v1.0.0` (with 'v' prefix)  
✅ **CORRECT**: `1.0.0` (no prefix)

Obsidian plugin system requires tags without 'v' prefix. All scripts enforce this.

### Required Release Artifacts

Every GitHub Release MUST include:
- `main.js` (bundled plugin code)
- `manifest.json` (plugin metadata)
- `styles.css` (optional, but include if present)

These files must be built from the **main branch** after PR merge, not from feature branch.

### Version Consistency

Three files must stay synchronized:
1. `manifest.json` → `version` field
2. `package.json` → `version` field
3. `versions.json` → entry mapping plugin version to minimum Obsidian version

Scripts handle this automatically, but manual edits must maintain consistency.

## GitHub CLI Setup

Scripts that interact with GitHub require the `gh` CLI:

**Installation:**
- macOS: `brew install gh`
- Windows: `winget install GitHub.cli`
- Linux: See https://cli.github.com/

**Authentication:**
```bash
gh auth login
```

**Verification:**
```bash
gh auth status
```

## Troubleshooting

### "Version mismatch" error

Run `check_versions.py` to diagnose:
```bash
python3 scripts/check_versions.py
```

If inconsistent, either:
- Use `bump_version.py` to fix
- Manually edit files to match

### "Build artifacts missing"

Ensure build completed successfully:
```bash
python3 scripts/build_plugin.py
```

Check that `main.js` and `manifest.json` exist at project root.

### "gh CLI not authenticated"

Authenticate GitHub CLI:
```bash
gh auth login
```

Follow prompts to complete authentication.

### "npm command not found"

Install Node.js and npm:
- https://nodejs.org/

Verify installation:
```bash
npm --version
```

### "CHANGELOG format issues"

**Problem: Link definitions scattered between version sections**

Symptoms:
- Links appear between `## [version]` headers
- Multiple groups of link definitions throughout file

Solution:
1. Locate ALL `[version]:` link definitions in the file
2. Cut them from their current locations
3. Paste ALL of them at the very end of the file
4. Ensure they're in reverse chronological order (newest first)

Correct structure:
```markdown
## [1.1.0] - 2026-01-17
...

## [1.0.0] - 2026-01-16
...

[Unreleased]: https://github.com/.../compare/1.1.0...HEAD
[1.1.0]: https://github.com/.../compare/1.0.0...1.1.0
[1.0.0]: https://github.com/.../releases/tag/1.0.0
```

**Problem: Release notes not extracted by create_release.py**

Cause: CHANGELOG structure doesn't match expected format

Solution:
- Verify version section exists: `## [X.Y.Z] - YYYY-MM-DD`
- Check that content is properly categorized under `### Added`, `### Changed`, etc.
- Ensure no malformed markdown between version header and content

## Best Practices

1. **Always use interactive workflow for first release** - Reduces chance of errors
2. **Edit CHANGELOG before committing** - Don't leave TODO markers in commits
3. **Validate CHANGELOG structure before committing**:
   - ALL link definitions `[version]:` are at the file end (not scattered between sections)
   - Comparison URLs follow correct pattern: `compare/old...new`
   - `[Unreleased]` compares latest version to HEAD
   - No orphaned or duplicate link definitions
4. **Build on main branch before release** - Ensures artifacts match published code
5. **Create draft releases first** - Review before making public
6. **Test manually before publishing** - Install plugin locally and verify functionality
7. **Use semantic versioning correctly**:
   - Patch: Bug fixes only
   - Minor: New features, backward compatible
   - Major: Breaking changes
8. **Customize commit messages and branch names** as needed - all scripts accept parameters

## Example: Complete First Release

```bash
# 1. From feature branch, run workflow
python3 .claude/skills/obsidian-plugin-release/scripts/release_workflow.py
# Select: 1 (initial release)
# Version: 1.0.0
# Edit CHANGELOG.md when prompted

# 2. Create PR
python3 .claude/skills/obsidian-plugin-release/scripts/create_pr.py feature/core main 1.0.0

# 3. Review and merge PR on GitHub

# 4. Switch to main and build
git checkout main
git pull origin main
python3 .claude/skills/obsidian-plugin-release/scripts/build_plugin.py

# 5. Create release
python3 .claude/skills/obsidian-plugin-release/scripts/create_release.py 1.0.0

# 6. Review draft release on GitHub, then publish

# Done! Plugin is now released and BRAT-compatible
```
