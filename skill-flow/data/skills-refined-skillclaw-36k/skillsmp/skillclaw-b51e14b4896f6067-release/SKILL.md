---
name: release
description: Use this skill to bump the version, update changelogs, commit, tag, and push a release in your project.
---

# Release Workflow

Trigger on: "release", "bump version", "prepare release", "new version".

## Instructions

When triggered, **execute all steps** (don't just show commands):

1. **Determine Version Bump Type**: Ask the user for the bump type if not specified:
   - `patch` (0.1.0 → 0.1.1) - bug fixes
   - `minor` (0.1.0 → 0.2.0) - new features
   - `major` (0.1.0 → 1.0.0) - breaking changes

2. **Update Version in All Relevant Files**: Update the version string in the necessary files (e.g., `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`).

3. **Update CHANGELOG.md**:
   - Move all content under `## [Unreleased]` to a new version section.
   - Add today's date in the format `## [X.Y.Z] - YYYY-MM-DD`.
   - Leave an empty `## [Unreleased]` section at the top.

4. **Run Tests**: Execute tests to ensure nothing is broken:
   ```bash
   npm run test:backend
   npm run test:integration:tier1
   ```

5. **Build Release**: Build the project to verify everything works:
   ```bash
   npm run tauri build
   ```

6. **Stage All Changes**:
   ```bash
   git add -A
   ```

7. **Commit with Version in Message**:
   ```bash
   git commit -m "chore: release vX.Y.Z"
   ```

8. **Create Annotated Git Tag**:
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z - Release Notes"
   ```

9. **Push Commits and Tags**:
   ```bash
   git push && git push --tags
   ```

## Example

User: "release patch"
→ Run script with patch
→ Update files, run tests, build, commit, tag, and push.

## Viewing Release Notes

```bash
# View tag message
git tag -l -n99 vX.Y.Z

# Create GitHub release from tag
gh release create vX.Y.Z --notes-from-tag
```