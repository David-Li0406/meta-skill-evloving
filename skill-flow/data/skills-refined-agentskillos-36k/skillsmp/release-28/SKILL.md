---
name: release
description: Create a GitHub release with auto-generated release notes. Analyzes commits since the last release, categorizes changes, drafts release notes, and creates the release after user confirmation.
---

# Release

## Overview

Automate the creation of GitHub releases with well-structured release notes. This skill:
- Detects the latest release tag
- Determines the next version (user-specified or auto-suggested)
- Analyzes commits since the last release
- Categorizes changes (features, fixes, improvements, etc.)
- Generates a release notes draft
- Creates the release after user confirmation

## Workflow

1. **Check prerequisites**
   - Verify `gh` CLI is installed and authenticated.
   - Ensure the working directory is a git repository.
   - Check that `origin` remote exists.

2. **Get existing releases**
   - List existing tags:
     ```sh
     git tag -l --sort=-v:refname | head -10
     ```
   - Get latest release:
     ```sh
     gh release list --limit 1
     ```
   - If no releases exist, use the first commit as the base.

3. **Determine the next version**
   - If the user specifies a version (e.g., `v0.2.0`), use it.
   - Otherwise, suggest the next version based on semantic versioning:
     - Analyze commit messages for breaking changes, features, or fixes.
     - `BREAKING CHANGE` or `!:` → major bump
     - `feat:` → minor bump
     - `fix:`, `chore:`, `docs:`, etc. → patch bump
   - Ask the user to confirm or specify a different version.

4. **Fetch commits since last release**
   - Get commit log:
     ```sh
     git log <last_tag>..HEAD --oneline --no-merges
     ```
   - Get detailed commit information:
     ```sh
     git log <last_tag>..HEAD --pretty=format:"%h %s" --no-merges
     ```
   - Get file change statistics:
     ```sh
     git diff <last_tag>..HEAD --stat
     ```

5. **Categorize changes**
   - Parse commit messages and group by type:
     - **New Features**: `feat:` prefix or new functionality
     - **Bug Fixes**: `fix:` prefix
     - **Improvements**: `refactor:`, `perf:` prefixes
     - **Documentation**: `docs:` prefix
     - **Other Changes**: `chore:`, `test:`, `ci:`, `build:`, etc.
   - For non-conventional commits, infer category from content.

6. **Generate release notes draft**
   - Use this template:
     ```markdown
     ## <Project Name> <version>

     ### New Features

     **<Feature title>**

     - <Bullet point description>
     - <Additional details if needed>

     ### Bug Fixes

     - <Fix description>

     ### Improvements

     - <Improvement description>

     ### Other Changes

     - <Other change description>

     **Full Changelog**: https://github.com/<owner>/<repo>/compare/<last_tag>...<new_tag>
     ```
   - Omit empty sections.
   - For significant changes, expand with context from:
     - Reading modified files
     - Examining PR descriptions (if available)
     - Analyzing the diff

7. **Present draft to user**
   - Display the generated release notes.
   - Ask for confirmation or edits:
     - Confirm and create
     - Edit the notes (user provides corrections)
     - Cancel

8. **Create the release**
   - Use `gh release create`:
     ```sh
     gh release create <version> --title "<version>" --notes "$(cat <<'EOF'
     <release notes content>
     EOF
     )"
     ```
   - Report the release URL on success.

## Version Format

- Default format: `v<major>.<minor>.<patch>` (e.g., `v1.2.3`)
- Support alternative formats if the project uses them:
  - Without `v` prefix: `1.2.3`
  - With pre-release: `v1.2.3-beta.1`
- Match the existing tag format in the repository.

## Release Notes Guidelines

- **Be concise**: 1-2 sentences per item.
- **Focus on user impact**: What changed for users, not implementation details.
- **Group related changes**: Multiple commits for one feature become one entry.
- **Use active voice**: "Add dark mode" not "Dark mode was added".
- **Include context**: Brief explanation of why the change matters.

## Edge Cases

- **No commits since last release**: Report that there are no changes to release.
- **First release**: Use all commits from the beginning, or ask for a base commit.
- **Merge commits**: Skip merge commits (use `--no-merges`).
- **Squash-merged PRs**: Treat as single feature commits.
- **Pre-release versions**: Support `-alpha`, `-beta`, `-rc` suffixes.

## Options

### Specify version
```
/release v1.0.0
```

### Draft only (don't create)
```
/release --draft
```

### Include pre-release tag
```
/release v1.0.0-beta.1 --prerelease
```

## Examples

### Basic usage (auto-detect version)
```
/release
```

### Specify version explicitly
```
/release v2.0.0
```

### Create a pre-release
```
/release v1.0.0-rc.1 --prerelease
```

## Error Handling

- If `gh` CLI is not installed, show installation instructions.
- If not authenticated, prompt `gh auth login`.
- If no commits since last release, report and exit.
- If release creation fails, show the error and suggest manual creation.
