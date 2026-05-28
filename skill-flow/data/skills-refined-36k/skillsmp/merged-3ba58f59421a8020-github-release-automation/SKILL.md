---
name: github-release-automation
description: Use this skill to automate the creation of GitHub releases with auto-generated release notes based on commits since the last tag.
---

# GitHub Release Automation

Automate the creation of GitHub releases with well-structured release notes. This skill detects the latest release tag, analyzes commits, categorizes changes, drafts release notes, and creates the release after user confirmation.

## Prerequisites
- Ensure `gh` CLI is installed and authenticated.
- The working directory must be a git repository with existing tags.

## Workflow

1. **Check existing releases**:
   - List existing tags:
     ```bash
     git tag -l --sort=-v:refname | head -10
     ```
   - Get the latest release:
     ```bash
     gh release list --limit 1
     ```
   - If no releases exist, use the first commit as the base.

2. **Determine the next version**:
   - If the user specifies a version (e.g., `v0.2.0`), use it.
   - Otherwise, suggest the next version based on semantic versioning:
     - Analyze commit messages for breaking changes, features, or fixes.
     - `BREAKING CHANGE` or `!:` → major bump
     - `feat:` → minor bump
     - `fix:`, `chore:`, `docs:`, etc. → patch bump
   - Ask the user to confirm or specify a different version.

3. **Fetch commits since the last release**:
   - Get commit log:
     ```bash
     git log <last_tag>..HEAD --oneline --no-merges
     ```
   - Get detailed commit information:
     ```bash
     git log <last_tag>..HEAD --pretty=format:"%h %s" --no-merges
     ```

4. **Categorize changes**:
   - Parse commit messages and group by type:
     - **New Features**: `feat:` prefix
     - **Bug Fixes**: `fix:` prefix
     - **Improvements**: `refactor:`, `perf:` prefixes
     - **Documentation**: `docs:` prefix
     - **Other Changes**: `chore:`, `test:`, etc.

5. **Generate release notes draft**:
   - Use this template:
     ```markdown
     ## What's New in v<version>

     ### New Features
     - **<Feature title>**: <Bullet point description>

     ### Bug Fixes
     - <Fix description>

     ### Improvements
     - <Improvement description>

     ### Other Changes
     - <Other change description>

     **Full Changelog**: https://github.com/<owner>/<repo>/compare/<last_tag>...<new_tag>
     ```
   - Omit empty sections.

6. **Present draft to user**:
   - Display the generated release notes.
   - Ask for confirmation or edits:
     - Confirm and create
     - Edit the notes (user provides corrections)
     - Cancel

7. **Create the release**:
   - Use `gh release create`:
     ```bash
     gh release create <version> --title "<version>" --notes "$(cat <<'EOF'
     <release notes content>
     EOF
     )"
     ```
   - Report the release URL on success.

## Version Format
- Default format: `v<major>.<minor>.<patch>` (e.g., `v1.2.3`)
- Support alternative formats if the project uses them.

## Release Notes Guidelines
- **Be concise**: 1-2 sentences per item.
- **Focus on user impact**: What changed for users, not implementation details.
- **Group related changes**: Multiple commits for one feature become one entry.
- **Use active voice**: "Add dark mode" not "Dark mode was added".

## Edge Cases
- **No commits since last release**: Report that there are no changes to release.
- **First release**: Use all commits from the beginning, or ask for a base commit.

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

## Error Handling
- If `gh` CLI is not installed, show installation instructions.
- If not authenticated, prompt `gh auth login`.
- If no commits since last release, report and exit.
- If release creation fails, show the error and suggest manual creation.