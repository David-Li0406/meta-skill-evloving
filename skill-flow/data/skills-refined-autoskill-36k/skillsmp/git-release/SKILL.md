---
name: git-release
description: Create consistent releases with changelogs and version bumping
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I Do

- Analyze commits since last tag to generate release notes
- Determine appropriate version bump (major/minor/patch) based on conventional commits
- Generate a changelog entry
- Provide copy-pasteable commands for creating the release

## When to Use Me

Use this skill when:
- Preparing a new release
- Creating a changelog
- Deciding on version numbers

## Release Process

### 1. Analyze Changes

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Check existing tags
git tag --sort=-v:refname | head -5
```

### 2. Version Bump Rules

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat!:` or `BREAKING CHANGE:` | Major (1.0.0 → 2.0.0) | Breaking API change |
| `feat:` | Minor (1.0.0 → 1.1.0) | New feature |
| `fix:` | Patch (1.0.0 → 1.0.1) | Bug fix |
| `docs:`, `chore:`, `refactor:` | Patch | Maintenance |

### 3. Changelog Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features
```

### 4. Create Release

```bash
# Tag the release
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# Or use GitHub CLI
gh release create vX.Y.Z --generate-notes --title "vX.Y.Z"
```

## Ask Clarifying Questions If

- Versioning scheme is unclear (semver vs calver vs other)
- Pre-release versions are needed (alpha, beta, rc)
- Multiple release branches exist
