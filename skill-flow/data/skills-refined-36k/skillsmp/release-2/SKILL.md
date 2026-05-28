---
name: release
description: Guide for releases and changelog. Triggers on: changelog, release, version.
---

# Release Guide

## Before Merging a Release PR

### 1. Bump Version in `package.json`

| PR Title Prefix | Version Bump |
|-----------------|--------------|
| `feat:` or `minor:` | Minor (0.X.0) |
| `fix:` or `patch:` | Patch (0.0.X) |
| `major:` or `type!:` | Major (X.0.0) |

### 2. Update `CHANGELOG.md`

Add entry under `## [Unreleased]`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added/Fixed/Breaking Changes

- Description from PR title
```

Section headers by bump type:
- `major:` or `!:` → `### Breaking Changes`
- `feat:` or `minor:` → `### Added`
- `fix:` or `patch:` → `### Fixed`

### 3. PR Title Must Have Release Prefix

Examples:
```
feat: add batch retry for failed rows     → creates tag from package.json version
fix: correct token refresh timing         → creates tag from package.json version
major: redesign API endpoints             → creates tag from package.json version
feat!: change auth flow (breaking)        → creates tag from package.json version
```

## After Merge

Workflow automatically:
1. Detects release prefix in commit message
2. Reads version from `package.json`
3. Fails if tag already exists (forgot to bump version)
4. Creates and pushes tag
5. Tag triggers `release.yml` → build + GitHub release

## Skipping Releases

PRs with non-release prefixes won't trigger tag creation:
- `docs:` - documentation
- `refactor:` - code restructure
- `test:` - test changes
- `chore:` - maintenance
- `ci:` - CI changes

## Errors

**"Tag vX.Y.Z already exists"** → You forgot to bump the version in `package.json`. Update the version in your PR and re-merge (or create a follow-up PR).

## Manual Release (Emergency)

```bash
# Bump version in package.json
# Update CHANGELOG.md
git add package.json CHANGELOG.md
git commit -m "chore: release vX.Y.Z"
git tag vX.Y.Z
git push origin HEAD vX.Y.Z
```
