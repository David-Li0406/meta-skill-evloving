---
name: github-pr-management
description: Use this skill to create or update GitHub pull requests with well-formatted descriptions and summaries of changes.
---

# GitHub Pull Request Management

This skill allows you to create a new GitHub pull request or update an existing one with a detailed description of changes.

## Create Pull Request

### Arguments

`$ARGUMENTS` can be used for special instructions, such as:
- Specifying a base branch: "use base branch: develop"
- Guiding the summary: "emphasize the performance improvements in the summary"
- Adding context: "this is part of the auth refactor epic"

Default base branch: `main` (unless specified in arguments)

### Step 1: Gather Information

Run these commands in parallel to understand the changes:

1. **Current branch**: `git branch --show-current`
2. **Uncommitted changes**: `git status --porcelain`
3. **Commits on branch**: `git log origin/main..HEAD --oneline`
4. **File changes summary**: `git diff --stat origin/main..HEAD`
5. **Full diff**: `git diff origin/main..HEAD`
6. **Recent commit style**: `git log -5 --oneline` (to match PR title convention)

**Important checks:**
- If uncommitted changes exist, warn the user and ask if they want to commit first.
- If no commits ahead of main, inform the user there's nothing to PR.
- If branch isn't pushed, you'll push it in Step 4.

### Step 2: Analyze and Categorize Changes

#### By Change Type (from commits and diff)
- ✨ **Added**: New files, features, capabilities
- 🔧 **Changed**: Modified existing functionality
- 🗑️ **Removed**: Deleted files or features
- 🐛 **Fixed**: Bug fixes
- 📚 **Docs**: Documentation updates
- 🧪 **Tests**: Test additions/modifications

#### Identify Attention Areas 🔍
Flag for special reviewer attention:
- Files with significant changes (>100 lines)
- Changes to base classes, interfaces, or public API
- New dependencies (`pyproject.toml`, `requirements.txt`)
- Configuration schema changes
- Security-related changes

### Step 3: Generate PR Title

Use conventional commit format matching the repo style:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for refactoring
- `chore:` for maintenance
- `test:` for test changes

If commits have mixed types, use the primary/most significant type.

### Step 4: Create the PR

1. **Push branch** (if needed):
   ```bash
   git push -u origin <branch-name>
   ```

2. **Create PR** using this template:

```markdown
## 📋 Summary

[1-2 sentence overview of what this PR accomplishes]

## 🔄 Changes

### ✨ Added
- [New features/files - link to key files when helpful]

### 🔧 Changed
- [Modified functionality - reference commits for specific changes]

### 🗑️ Removed
- [Deleted items]

### 🐛 Fixed
- [Bug fixes - if applicable]

## 🔍 Attention Areas

> ⚠️ **Reviewers:** Please pay special attention to the following:

- `path/to/critical/file.py` - [Why this needs attention]

---
🤖 *Generated with AI*
```

3. **Execute**:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```

4. **Return the PR URL** to the user.

## Update Pull Request Description

### Arguments

```
/pr-description <PR_NUMBER> [--fixes <ISSUE_NUMBERS>]
```

- `PR_NUMBER` (required): The pull request number to update
- `--fixes` (optional): Comma-separated issue numbers that this PR fixes (e.g., `--fixes 123,456`)

### Instructions

1. Gather information about the PR:
   - Use GitHub plugin to get PR details (title, current description, base branch)
   - Use local git to get commits: `git log main..HEAD --oneline`
   - Use local git to get the diff: `git diff main..HEAD`
   - Parse any `--fixes` argument for issue numbers

2. Check the existing PR description:
   - If it already has a complete, accurate description that reflects the changes, do nothing.
   - If it's missing sections, incomplete, or outdated compared to the actual changes, proceed to update.
   - If it only has the template placeholder text, generate a full description.

3. Analyze the changes:
   - Understand the purpose of each commit.
   - Identify any breaking changes (API changes, removed features, behavior changes).
   - Look for new features, bug fixes, refactoring, or documentation changes.
   - Collect issue numbers from:
     - The `--fixes` argument (if provided)
     - Commit messages (patterns like "Fixes #123", "Closes #456", "Resolves #789")

4. Generate or update the PR description with these sections:

### PR Description Format

#### Summary (always include)

Brief bullet points describing what changed and why. Focus on the *purpose* and *impact*, not implementation details.

```markdown
## Summary

- Added X to enable Y
- Fixed bug where Z would happen
- Refactored W for better maintainability
```

#### Breaking Changes (include only if applicable)

Document any changes that affect existing users or APIs.

```markdown
## Breaking Changes

- `ClassName.method()` now requires a `param` argument
- Removed deprecated `old_function()` - use `new_function()` instead
```

#### Testing (include when non-obvious)

How to verify the changes work. Skip for trivial changes.

```markdown
## Testing

- Run `uv run pytest tests/test_feature.py` to verify the fix
- Example usage: `uv run examples/new_feature.py`
```

#### Fixes (include if issues are provided or found in commits)

List issues this PR fixes. GitHub will automatically close these issues when the PR is merged.

```markdown
## Fixes

- Fixes #123
- Fixes #456
```

### Guidelines

- **Be concise** - Reviewers should understand the PR in 30 seconds.
- **Focus on why** - The diff shows *what* changed, explain *why*.
- **Skip empty sections** - Only include sections that have content.
- **Use bullet points** - Easier to scan than paragraphs.
- **Don't duplicate the diff** - Avoid listing every file or line changed.

## Example Output

```markdown
## Summary

- Added `/docstring` skill for documenting Python modules with Google-style docstrings
- Skill finds classes by name and handles conflicts when multiple matches exist
- Skips already-documented code to avoid unnecessary changes

## Testing

/docstring ClassName

## Fixes

- Fixes #123
```

## Checklist

Before updating the PR:

- [ ] Verified existing description needs updating (not already complete)
- [ ] Summary accurately reflects the changes
- [ ] Breaking changes are clearly documented (if any)
- [ ] No unnecessary sections included
- [ ] Description is concise and scannable