---
name: git-expert
description: "Use when working with git operations including commits, branches, worktrees, and PRs. Covers the full git workflow from feature isolation to PR submission."
---

# Git Expert

## Overview

Expert git workflow skill covering isolation (worktrees), commits, branching, and PR submission using GitHub CLI (gh).

**Core principles:**
- Isolation: Work in worktrees to avoid context pollution
- Atomic commits: Each commit represents one logical change
- Verification: Always verify before committing or pushing
- Clean history: Meaningful commits, clean rebases

## Sub-Skills

This skill contains three sub-skills for different phases:

1. **Worktrees** - Feature isolation and workspace setup
2. **Commits** - Intelligent commit protocol
3. **Finishing** - Branch completion and PR submission

---

## 1. Git Worktrees

### When to Use

- Starting feature work that needs isolation
- Before executing implementation plans
- Working on multiple branches simultaneously
- Need clean baseline without affecting main workspace

### Directory Selection Process

Follow this priority:

```bash
# 1. Check existing directories
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative

# 2. Check CLAUDE.md for preference
grep -i "worktree.*director" CLAUDE.md 2>/dev/null

# 3. If neither exists, ask user
```

### Safety Verification

**MUST verify directory is ignored before creating worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null
```

**If NOT ignored:**
1. Add to .gitignore: `echo '.worktrees/' >> .gitignore`
2. Commit the change
3. Proceed with worktree creation

### Creation Steps

```bash
# 1. Get project name
project=$(basename "$(git rev-parse --show-toplevel)")

# 2. Create worktree with new branch
git worktree add .worktrees/$BRANCH_NAME -b feature/$BRANCH_NAME

# 3. Move to worktree
cd .worktrees/$BRANCH_NAME

# 4. Auto-detect and run setup
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f go.mod ]; then go mod download; fi

# 5. Verify clean baseline
npm test  # or project-appropriate test command
```

### Worktree Commands

| Command | Purpose |
|---------|---------|
| `git worktree add <path> -b <branch>` | Create new worktree with branch |
| `git worktree list` | List all worktrees |
| `git worktree remove <path>` | Remove worktree |
| `git worktree prune` | Clean up stale references |

---

## 2. Git Commits

### Core Rules

**Never do without explicit permission:**
- Push to remote
- Force push
- Run `git clean -fdx`
- Modify git config
- Amend pushed commits

**Always do:**
- Include meaningful commit messages
- Check status before operations
- Verify tests pass before committing
- Use HEREDOC for multi-line messages

### Pre-Commit Protocol

```bash
# 1. Status check
git status

# 2. Pre-commit validation (if available)
npm run lint && npm run typecheck

# 3. Run tests
npm test

# 4. Review changes
git diff --cached
```

### Commit Message Format

**Format:** `{type}: {summary}`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation
- `style`: Formatting
- `test`: Tests
- `build`: Build system
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat: add user profile endpoint"
git commit -m "fix: resolve race condition in auth flow"
git commit -m "refactor: extract validation helpers"
```

### Multi-Line Commit Messages

Use HEREDOC for complex messages:

```bash
git commit -m "$(cat <<'EOF'
feat: implement retry mechanism for API calls

- Add exponential backoff with jitter
- Configure max retries via environment variable
- Add comprehensive test coverage

Closes #123
EOF
)"
```

### Staged vs Unstaged

```bash
# See what's staged
git diff --cached --name-only

# See what's unstaged
git diff --name-only

# Stage related files together
git add src/auth/* tests/auth/*

# Stage hunks interactively (if needed)
git add -p
```

### Verification Before Commit

**MANDATORY before every commit:**

```bash
# 1. Run tests
npm test  # Must pass

# 2. Run linter
npm run lint  # Must be clean

# 3. Type check (if applicable)
npm run typecheck  # Must pass

# 4. Review staged changes
git diff --cached
```

---

## 3. Finishing a Development Branch

### When to Use

- Implementation complete
- All tests pass
- Ready to integrate work

### The Process

#### Step 1: Verify Tests

```bash
npm test  # Must pass before proceeding
```

If tests fail, stop. Fix before continuing.

#### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
```

#### Step 3: Present Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

#### Option 1: Merge Locally

```bash
git checkout main
git pull
git merge feature/my-feature
npm test  # Verify after merge
git branch -d feature/my-feature
```

Then cleanup worktree.

#### Option 2: Create PR (Standard Git)

```bash
git push -u origin feature/my-feature

gh pr create --title "Add feature X" --body "$(cat <<'EOF'
## Summary
- Implemented X
- Added tests for Y

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
EOF
)"
```

#### Option 3: Keep As-Is

Report status. Don't cleanup.

#### Option 4: Discard

**Require confirmation:**
```
This will permanently delete:
- Branch feature/my-feature
- All commits: abc123, def456
- Worktree at .worktrees/my-feature

Type 'discard' to confirm.
```

```bash
git checkout main
git branch -D feature/my-feature
git worktree remove .worktrees/my-feature
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/description` | `feature/user-auth` |
| Bug fix | `fix/description` | `fix/login-redirect` |
| Refactor | `refactor/description` | `refactor/auth-module` |
| Personal | `dev/name/description` | `dev/erik/auth-poc` |

## Protected Branches

- `main` / `master`: Production (never direct push)
- `develop` / `dev`: Development/staging

**Always create feature branches from the appropriate base.**

---

## Common Mistakes

### Skipping verification
- **Problem:** Commit broken code
- **Fix:** Always run tests before commit

### Force push without warning
- **Problem:** Overwrite others' work
- **Fix:** Never force push without explicit permission

### Worktree not ignored
- **Problem:** Worktree contents tracked in git
- **Fix:** Always verify `.worktrees/` is in .gitignore

### Committing secrets
- **Problem:** Expose credentials
- **Fix:** Check for .env, credentials files before staging

### Vague commit messages
- **Problem:** Unclear history
- **Fix:** Use type prefix, describe the "why"

---

## Red Flags - STOP

**Never:**
- Push without explicit request
- Force push (especially to main/master)
- Commit without tests passing
- Delete branches without confirmation
- Proceed with failing tests

**Always:**
- Verify tests before commit
- Use meaningful commit messages
- Check what's staged before committing
- Get confirmation for destructive operations

---

## Quick Reference

```bash
# Worktree setup
git worktree add .worktrees/feature -b feature/name
cd .worktrees/feature && npm install && npm test

# Commit workflow
git status
npm test && npm run lint
git add <files>
git commit -m "type: description"

# Standard PR
git push -u origin feature/name
gh pr create

# Cleanup
git worktree remove .worktrees/feature
git branch -d feature/name
```

---

## Integration

**On-demand loading:** This is a Domain skill, loaded when git operations detected.

**Pairs with:**
- **tdd** - Tests pass before commits
- **verification** - Verify before PR submission
- **subagent-driven-development** - Feature branches for sub-agent work
