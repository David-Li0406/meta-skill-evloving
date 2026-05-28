---
name: git-pushing
description: Use this skill to stage, commit, and push git changes with conventional commit messages when the user wants to save and push their work or mentions pushing to remote.
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

### Fast Path (Recommended)

Use the automated script for maximum speed:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

This script handles:

- ✅ Staging all changes
- ✅ Auto-generating conventional commit messages
- ✅ Adding Claude Code footer
- ✅ Pushing to remote (with -u for new branches)
- ✅ Showing PR link for GitHub repos

**With custom message:**

```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add new feature"
```

### Manual Path (Fallback)

Use when the script is unavailable or a custom workflow is needed:

1. **Check Git Status**
   - Run `git status` to understand which files have changed and the current branch name.

2. **Stage Changes**
   - Run `git add .` to stage all changes or stage specific files if a partial commit is needed.

3. **Create Commit Message**
   - If a user-provided message is available, use it directly.
   - If no message is provided, analyze changes using `git diff` and generate a conventional commit message:
     - Format: `type(scope): description`
     - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
     - Keep the description concise (50-90 characters) and in imperative mood.
   - Always append Claude Code footer:

   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

   Use heredoc format:

   ```bash
   git commit -m "$(cat <<'EOF'
   commit message here

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

4. **Push to Remote**
   - Run `git push` to push commits. If it's a new branch, use `git push -u origin <branch>`.
   - If the push fails due to diverged branches, inform the user and ask how to proceed.

5. **Confirm Success**
   - Report the commit hash, summarize what was committed, and confirm the push succeeded.

## Examples

- User: "Push these changes"
  → Check status, stage all, generate commit message, push.

- User: "Commit with message 'fix: resolve table extraction issue'"
  → Use provided message, push.

- User: "Let's save this to github"
  → Activate workflow, generate appropriate commit message.