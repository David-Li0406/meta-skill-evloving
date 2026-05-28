---
name: git-push
description: Use this skill when you want to stage, commit, and push changes to a remote Git repository with conventional commit messages.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:
- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

```bash
bash scripts/smart_commit.sh
```

With custom message:

```bash
bash scripts/smart_commit.sh "feat: add feature"
```

### Script Functionality

The script handles:
- Staging all changes
- Auto-generating conventional commit messages
- Adding a Claude Code footer
- Pushing to remote (with -u for new branches)
- Showing PR link for GitHub repos

### Manual Path (Fallback)

Use when the script is unavailable or a custom workflow is needed:

1. **Check Git Status**
   - Run `git status` to understand which files have changed and what will be committed.

2. **Stage Changes**
   - Run `git add .` to stage all changes or stage specific files if a partial commit is needed.

3. **Create Commit Message**
   - If the user provided a message, use it directly.
   - If no message is provided, analyze changes using `git diff` and generate a conventional commit message:
     - Format: `type(scope): description`
     - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
     - Keep the description concise (50-90 characters) and use imperative mood.

4. **Push to Remote**
   - Run `git push` to push the committed changes to the remote repository.