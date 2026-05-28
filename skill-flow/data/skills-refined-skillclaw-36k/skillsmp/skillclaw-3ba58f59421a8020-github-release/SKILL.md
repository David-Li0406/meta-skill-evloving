---
name: github-release
description: Use this skill to automate the creation of a GitHub release with well-structured release notes generated from commits since the last tag.
---

# Skill body

## Overview

This skill automates the creation of GitHub releases, generating release notes based on commits since the last tag. It categorizes changes into features, bug fixes, and other improvements, and requires user confirmation before creating the release.

## Prerequisites

- Ensure the `gh` CLI is installed and authenticated.
- The working directory must be a Git repository with existing tags.

## Workflow

1. **Get the latest tag**:
   ```bash
   git tag --sort=-v:refname | head -1
   ```

2. **Fetch commits since the latest tag**:
   ```bash
   git log <TAG>..HEAD --pretty=format:"%h %s%n%b---" --no-merges
   ```

3. **Determine the next version**:
   - If the user specifies a version (e.g., `v0.2.0`), use it.
   - Otherwise, suggest the next version based on semantic versioning:
     - Analyze commit messages for breaking changes, features, or fixes.
     - `BREAKING CHANGE` or `!:` → major bump
     - `feat:` → minor bump
     - `fix:`, `chore:`, `docs:`, etc. → patch bump
   - Confirm with the user.

4. **Categorize changes**:
   - Group commits by type:
     - **New Features**: `feat:` prefix
     - **Bug Fixes**: `fix:` prefix
     - **Improvements**: `refactor:`, `perf:`
     - **Documentation**: `docs:`
     - **Other Changes**: `chore:`, `test:`, etc.

5. **Generate release notes draft**:
   ```markdown
   ## What's New in vX.X.X

   [1-2 sentence summary]

   ### New Features
   - **Feature** - Description

   ### Bug Fixes
   - **Fix** - Description

   ### Improvements
   - **Change** - Description

   ### Downloads

   | Platform | Download |
   |----------|----------|
   | Windows | `Project_X.X.X_x64-setup.exe` |
   | macOS (Intel) | `Project_X.X.X_x64.dmg` |
   | macOS (Apple Silicon) | `Project_X.X.X_aarch64.dmg` |
   | Linux (Debian/Ubuntu) | `Project_X.X.X_amd64.deb` |
   | Linux (AppImage) | `Project_X.X.X_amd64.AppImage` |
   | Android | `Project_X.X.X.apk` |

   ---
   **Full Changelog**: https://github.com/<username>/<repository>/compare/<prev-tag>...v<version>
   ```

6. **Confirm with user**: Show version, tag, commit count, and notes preview.

7. **Commit and push version bump**:
   ```bash
   git add -A && git commit -m "chore: bump version to X.X.X"
   git push
   ```

8. **Create the release**:
   ```bash
   gh release create vX.X.X --title "Project vX.X.X" --notes "$(cat <<'EOF'
   <notes>
   EOF
   )"
   ```

9. **Done**: Show release URL.