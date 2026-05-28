---
name: release
description: Create a new specops release with version bump, tag, and GitHub release
---

# Release Process

Create a new release for specops.

## Steps

### 1. Determine Version

Ask the user for the new version, or suggest one based on semver:
- **patch** (x.y.Z): bug fixes, minor changes
- **minor** (x.Y.0): new features, backwards compatible
- **major** (X.0.0): breaking changes

To find the current version:
```bash
git describe --tags --abbrev=0
```

### 2. Bump Version

Update version in these files:
- `install.ps1`: `$VERSION = "vX.Y.Z"`
- `install.sh`: `VERSION="vX.Y.Z"`
- `README.md`: Update install URLs to use `vX.Y.Z` instead of previous version

### 3. Commit Version Bump

```bash
git add install.ps1 install.sh README.md
git commit -m "Bump version to vX.Y.Z"
```

### 4. Create and Push Tag

```bash
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z
```

### 5. Generate Release Notes

Get commits since last tag for release notes:
```bash
git log $(git describe --tags --abbrev=0 HEAD^)..HEAD --oneline
```

### 6. Create GitHub Release

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "RELEASE_NOTES_HERE"
```

Format release notes as:
```markdown
## Changes

- Change 1
- Change 2

## Installation

**Windows:**
```powershell
irm https://raw.githubusercontent.com/wilddeer/specops/main/install.ps1 | iex
```

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/wilddeer/specops/main/install.sh | bash
```
```

## Checklist

- [ ] Version follows semver
- [ ] Both install scripts updated
- [ ] README install URLs updated
- [ ] Tag matches version in scripts and README
- [ ] Release notes summarize changes clearly
