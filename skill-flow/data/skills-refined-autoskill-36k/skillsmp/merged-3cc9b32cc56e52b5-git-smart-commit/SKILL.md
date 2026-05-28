---
name: git-smart-commit
description: Use this skill for a smart git commit workflow that stages changes, crafts commit messages, and ensures safety checks.
---

# Git Smart Commit Skill

This skill provides a comprehensive workflow for committing changes in Git, including staging, message crafting, and safety checks.

## Available Commands

| Command            | Description                                             |
| ------------------ | ------------------------------------------------------- |
| `git.status`       | Show working tree status                                |
| `git.stage_all`    | Stage all changes with security scan                   |
| `git.commit`       | Commit staged changes                                   |
| `git.smart_commit` | Smart Commit workflow (stage → scan → approve → commit) |
| `git.push`         | Push to remote                                          |
| `git.log`          | Show commit logs                                        |

## Triggers

- "commit"
- "commit changes"
- "git commit"
- "save my changes"
- "commit this"
- "commit and push" (includes automatic push to origin)

## Workflow Overview

1. **Assess Current State**: Check the working directory and see staged and unstaged changes.
2. **Smart Staging**: Automatically stage relevant files while excluding sensitive information.
3. **Message Crafting**: Create conventional commit messages.
4. **Safety Checks**: Prevent dangerous operations and ensure compliance with security rules.
5. **Co-authoring**: Add co-author attribution if applicable.
6. **Auto-Push**: Automatically push to the origin if "commit and push" is triggered.

### Step-by-Step Process

#### Step 1: Assess Current State

```bash
git status
git diff --cached --stat
git diff --stat
git log --oneline -5
```

#### Step 2: Stage Changes

```bash
git add -A
```

**Exclude from staging:**
- `.env`, `.env.*` - environment secrets
- `credentials.json`, `*_secret.json` - API keys
- `*.pem`, `*.key` - certificates
- `node_modules/`, `__pycache__/` - dependencies

If secrets are detected, warn the user to remove them before committing.

#### Step 3: Craft Commit Message

Use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvement |

#### Step 4: Commit

```bash
git commit -m "$(cat <<'EOF'
feat(scope): short description

Optional longer explanation of what changed and why.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

#### Step 5: Verify

```bash
git log -1 --stat
git status
```

#### Step 6: Push (if "commit and push" trigger)

If the user said "commit and push", automatically push after successful commit:

```bash
git push origin main
```

#### Step 7: Visualize Push (if "commit and push" trigger)

Send a visualization after a successful push to show what was committed and pushed.

### Safety Rules

**NEVER Do These:**
- `git commit --amend` on pushed commits
- `git push --force` without explicit user request
- Commit files matching secret patterns
- Skip pre-commit hooks (`--no-verify`)
- Commit to main/master without confirmation

**ALWAYS Do These:**
- Read files before committing
- Show diff summary before committing
- Use HEREDOC for multi-line messages
- Verify commit succeeded after

## Integration with GitHub Skill

- **"commit and push"** → This skill handles both commit AND push automatically.
- **"commit"** alone → Local commit only; use "push" separately if needed.

## Quick Reference

| Command | Action |
|---------|--------|
| "commit" | Full workflow (local only) |
| "commit and push" | Full workflow + push to origin |
| "commit these files" | Commit specific files |
| "amend" | Amend last commit (if safe) |
| "what changed" | Show diff without committing |
| "undo last commit" | `git reset --soft HEAD~1` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "nothing to commit" | Check if files are saved, or already committed |
| Pre-commit hook fails | Fix issues, stage, commit again (no amend) |
| Merge conflict | Resolve conflicts first, then commit |
| Detached HEAD | `git checkout main` first |
| Wrong branch | `git checkout <correct-branch>` |