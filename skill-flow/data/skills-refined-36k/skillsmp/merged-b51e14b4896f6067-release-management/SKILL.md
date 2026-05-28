---
name: release-management
description: Use this skill to manage versioning, create releases, and push changes to the repository.
---

# Release Management Workflow

This skill automates the process of version management, including bumping the version, updating changelogs, committing changes, tagging releases, and pushing to the remote repository.

## Triggering the Workflow

The workflow can be triggered by phrases such as "release", "bump version", "prepare release", or "new version".

## Steps to Execute

1. **Determine Version Bump Type**  
   Ask the user for the type of version bump if not specified:
   - `patch`: Increment the PATCH version (e.g., 0.1.0 → 0.1.1)
   - `minor`: Increment the MINOR version (e.g., 0.1.0 → 0.2.0)
   - `major`: Increment the MAJOR version (e.g., 0.1.0 → 1.0.0)

2. **Update Version in Relevant Files**  
   Update the version string in the following files:
   - `recent_state_summarizer/__init__.py` (field `__version__`)
   - `pyproject.toml` (if applicable)
   - `package.json` (field `"version": "X.Y.Z"`)
   - `src-tauri/Cargo.toml` (field `version = "X.Y.Z"`)
   - `src-tauri/tauri.conf.json` (field `"version": "X.Y.Z"`)

3. **Update CHANGELOG.md**  
   Move all content under `## [Unreleased]` to a new version section and add today's date:
   ```markdown
   ## [Unreleased]

   ## [X.Y.Z] - YYYY-MM-DD

   ### New Features
   - Description of new features...
   ```

4. **Run Tests**  
   Execute tests to ensure everything is functioning correctly:
   ```bash
   npm run test:backend
   npm run test:integration:tier1
   ```

5. **Build Release**  
   Build the project to verify that everything works:
   ```bash
   npm run tauri build
   ```

6. **Commit, Tag, and Push**  
   After a successful build, stage all changes, commit, create a tag, and push:
   ```bash
   git add -A
   git commit -m "chore: release vX.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z - Release notes"
   git push && git push --tags
   ```

7. **Report Results**  
   Show the path to the built installer or any relevant output.

## Notes
- Ensure that all feature branches are merged into `main` before executing this workflow.
- The CHANGELOG should be updated in the specified format, and the release notes should summarize the changes made since the last release.

## Example Usage
User: "release patch"  
→ Execute the workflow with the patch version increment.