---
name: homebrew-release
description: Create and deploy new versions to Homebrew tap with automatic cask updates
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: release
---

# Homebrew Release Deployment

Use this skill when creating a new release that will be distributed via Homebrew.

## Overview

This project uses an **automated release pipeline** that:

1. Builds a macOS ARM64 DMG with ad-hoc signing
2. Creates a GitHub Release
3. Automatically updates the Homebrew tap (`bradhannah/homebrew-doggy-bag`)

**No manual Homebrew tap updates are required** - everything is triggered by pushing a version tag.

## Prerequisites

Before releasing, ensure:

- `HOMEBREW_TAP_TOKEN` secret is configured in the GitHub repo (PAT with `repo` + `workflow` scopes)
- The Homebrew tap repository exists: `bradhannah/homebrew-doggy-bag`

## Key Files

| File                               | Purpose                                            |
| ---------------------------------- | -------------------------------------------------- |
| `src-tauri/tauri.conf.json`        | **Source of truth** - version number (line 4)      |
| `src-tauri/Cargo.toml`             | Rust package version (should match)                |
| `package.json`                     | Root npm package version (should match)            |
| `api/package.json`                 | API npm package version (should match)             |
| `.github/workflows/release.yml`    | Release automation workflow                        |
| Homebrew tap: `Casks/doggy-bag.rb` | Cask definition (auto-updated by release workflow) |

### Version Sync

When bumping versions, update all four version files to keep them in sync:

```bash
# Check current versions
grep '"version"' src-tauri/tauri.conf.json package.json api/package.json
grep '^version' src-tauri/Cargo.toml

# After updating, verify they match
```

The `api/src/services/version-service.ts` reads version dynamically from `tauri.conf.json` at runtime (no hardcoded fallback).

## Release Process

### Step 1: Check Current State

```bash
# View recent tags
git tag --sort=-v:refname | head -5

# View recent commits since last tag
git log --oneline $(git describe --tags --abbrev=0)..HEAD

# Check current version in tauri.conf.json
grep '"version"' src-tauri/tauri.conf.json
```

### Step 2: Determine Version Bump

Choose the appropriate version increment:

| Change Type                   | Version Bump | Example        |
| ----------------------------- | ------------ | -------------- |
| Bug fixes, minor improvements | Patch        | 0.2.2 -> 0.2.3 |
| New features, enhancements    | Minor        | 0.2.2 -> 0.3.0 |
| Breaking changes              | Major        | 0.2.2 -> 1.0.0 |

### Step 3: Bump Version

Edit `src-tauri/tauri.conf.json` and update the `"version"` field:

```json
{
  "version": "X.Y.Z"
}
```

### Step 4: Commit, Tag, and Push

```bash
# Commit the version bump
git add src-tauri/tauri.conf.json
git commit -m "chore: bump version to X.Y.Z"

# Create tag and push everything
git tag vX.Y.Z && git push && git push origin vX.Y.Z
```

**Important:** The tag format must be `vX.Y.Z` (with the `v` prefix) to trigger the release workflow.

## What Happens Automatically

After pushing the tag, the GitHub Actions workflow (`.github/workflows/release.yml`) executes:

1. **create-release** - Creates a draft GitHub Release with auto-generated notes
2. **build-macos** - Builds the macOS ARM64 DMG:
   - Installs dependencies (Bun, Node.js, Rust)
   - Builds the Tauri app with `npm run tauri build -- --target aarch64-apple-darwin`
   - Ad-hoc code signs the app bundle
   - Creates and uploads the DMG
   - Calculates SHA256 hash
3. **publish-release** - Publishes the draft release
4. **update-homebrew** - Dispatches `update-cask` event to `bradhannah/homebrew-doggy-bag` with:
   - Version number (without `v` prefix)
   - SHA256 hash of the DMG

The Homebrew tap repository receives the dispatch and automatically:

- Updates `Casks/doggy-bag.rb` with new version and SHA256
- Commits and pushes the change

## Monitoring the Release

Track progress at:

1. **Main release workflow:** `https://github.com/bradhannah/doggy-bag/actions`
2. **Homebrew tap update:** `https://github.com/bradhannah/homebrew-doggy-bag/actions`

## Verification

After the release completes:

```bash
# Update Homebrew and check the new version
brew update
brew info bradhannah/doggy-bag/doggy-bag

# Upgrade to the new version
brew upgrade doggy-bag
```

## Quick Reference

```bash
# Full release command sequence (replace X.Y.Z with actual version)
git tag --sort=-v:refname | head -3  # Check latest tags
# Edit src-tauri/tauri.conf.json to update version
git add src-tauri/tauri.conf.json && git commit -m "chore: bump version to X.Y.Z"
git tag vX.Y.Z && git push && git push origin vX.Y.Z
```

## Workflow Diagram

```
Push vX.Y.Z tag
       |
       v
+------------------+
| release.yml      |
| (BudgetForFun)   |
+------------------+
       |
       +---> create-release (draft)
       |
       +---> build-macos
       |         |
       |         +---> Build DMG
       |         +---> Calculate SHA256
       |         +---> Upload to Release
       |
       +---> publish-release
       |
       +---> update-homebrew
                 |
                 v
        repository_dispatch
                 |
                 v
+------------------+
| update-cask.yml  |
| (homebrew-tap)   |
+------------------+
       |
       +---> Update Casks/doggy-bag.rb
       +---> Commit & Push
       |
       v
  Homebrew Updated!
```
