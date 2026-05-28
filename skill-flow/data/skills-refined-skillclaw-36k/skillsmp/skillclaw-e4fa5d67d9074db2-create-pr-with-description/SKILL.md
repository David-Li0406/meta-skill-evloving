---
name: create-pr-with-description
description: Use this skill to create a well-formatted GitHub pull request with a comprehensive description of changes, including summaries and attention areas.
---

# Skill body

## Create Pull Request

Create a well-formatted GitHub pull request for the current branch.

### Arguments

`$ARGUMENTS` can be used for special instructions, such as:
- Specifying a base branch: "use base branch: develop"
- Guiding the summary: "emphasize the performance improvements in the summary"
- Adding context: "this is part of the auth refactor epic"
- Any other guidance for PR creation

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

- [1-2 sentence overview of what changed and why]
- [Additional context or instructions if necessary]

## Changes
- ✨ Added: [List of new features]
- 🔧 Changed: [List of modifications]
- 🐛 Fixed: [List of bug fixes]
- 📚 Docs: [Documentation updates]
- 🧪 Tests: [Test changes]

## Attention Areas
- [List any areas that require special attention]
```