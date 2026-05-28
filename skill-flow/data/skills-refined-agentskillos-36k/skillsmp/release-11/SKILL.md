---
name: release
description: Create a new release by bumping version, committing, and pushing a git tag. Use when the user wants to release a new version (e.g., "release 1.0.1", "release patch", "make a release", "bump version and release", "create version 2.0.0").
allowed_tools:
  - Bash
  - Read
  - Edit
---

# Release Workflow

Create a new release for Eyes on Claude Code.

## Arguments

The user may specify a version in one of these formats:
- **Explicit version**: `1.0.1`, `2.0.0`
- **Semver bump**: `patch`, `minor`, `major`

If not specified, ask the user which version type they want.

## Workflow

### 1. Determine New Version

If explicit version provided, use it directly.

If semver bump keyword provided:
```bash
# Get current version from package.json
node -p "require('./package.json').version"
```

Then calculate:
- `patch`: 1.0.0 → 1.0.1
- `minor`: 1.0.0 → 1.1.0
- `major`: 1.0.0 → 2.0.0

### 2. Update Version in Files

Update version in both files:

**package.json:**
```json
{
  "version": "NEW_VERSION"
}
```

**src-tauri/tauri.conf.json:**
```json
{
  "version": "NEW_VERSION"
}
```

### 3. Commit Version Bump

```bash
git add package.json src-tauri/tauri.conf.json
git commit -m "Bump version to NEW_VERSION"
```

### 4. Create and Push Tag

```bash
git tag vNEW_VERSION
git push origin main vNEW_VERSION
```

### 5. Report Success

Output the following:
- New version number
- Git tag created
- GitHub Actions URL: `https://github.com/joe-re/claude-code-session-manager/actions`
- Remind user to check the draft release on GitHub after the build completes

## Example User Requests

- "release 1.0.1"
- "release patch"
- "make a minor release"
- "bump version to 2.0.0 and release"
- "create a new release"

## Notes

- Always ensure working directory is clean before running
- GitHub Actions will automatically build for all platforms (macOS, Linux, Windows)
- The release is created as a draft - user must publish it manually on GitHub
