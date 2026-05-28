---
name: git-master
description: Git operations mastery. Atomic commits, rebase/squash, history search (blame, bisect, log -S). Triggers on 'commit', 'rebase', 'squash', 'who wrote', 'when was X added', 'find the commit that'.
---

# Git Master Skill

## When to Load This Skill

- Creating commits (atomic, well-messaged)
- Rebasing or squashing commits
- History search (blame, bisect, log -S)
- Finding "who wrote" or "when was X added"
- Any complex git operations

---

## Atomic Commits

Each commit should be:
- **Single purpose** - one logical change
- **Self-contained** - builds and tests pass
- **Well-messaged** - explains WHY, not just WHAT

### Commit Message Format

```
<type>(<scope>): <subject>

<body - optional, explains WHY>

<footer - optional, references issues>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Examples

```bash
# ✅ GOOD
git commit -m "feat(auth): add JWT refresh token support

Enables seamless token refresh without user re-authentication.
Tokens refresh 5 minutes before expiration.

Closes #123"

# ❌ BAD
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "update"
```

---

## History Search

### Find Who Wrote a Line

```bash
git blame <file>
git blame -L 10,20 <file>  # lines 10-20 only
git blame -w <file>        # ignore whitespace
```

### Find When Code Was Added

```bash
# Search commit messages
git log --grep="keyword"

# Search code changes (pickaxe)
git log -S "function_name"
git log -S "exact string" --all

# Search with regex
git log -G "pattern.*regex"
```

### Find Bug Introduction (Bisect)

```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Git will checkout commits, you test each:
git bisect good  # or
git bisect bad
# When done:
git bisect reset
```

---

## Interactive Rebase

### Squash Recent Commits

```bash
git rebase -i HEAD~3  # last 3 commits
```

In editor, change `pick` to:
- `squash` (s) - combine with previous, keep message
- `fixup` (f) - combine with previous, discard message
- `reword` (r) - change commit message
- `edit` (e) - stop to amend
- `drop` (d) - delete commit

### Rebase onto Main

```bash
git fetch origin
git rebase origin/main
# Resolve conflicts if any:
git add <file>
git rebase --continue
```

---

## Safety Rules (CRITICAL)

| Action | Safety |
|--------|--------|
| `git commit` | Safe |
| `git commit --amend` | Safe if NOT pushed |
| `git rebase` | Safe if NOT pushed |
| `git push --force` | ⚠️ DESTRUCTIVE - ask first |
| `git reset --hard` | ⚠️ DESTRUCTIVE - ask first |

**NEVER force push to main/master without explicit user approval.**

---

## Common Workflows

### Amend Last Commit (Not Pushed)

```bash
git add <files>
git commit --amend --no-edit
# OR to also change message:
git commit --amend -m "new message"
```

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Stash Work in Progress

```bash
git stash
git stash pop
git stash list
git stash drop stash@{0}
```

### Create Feature Branch

```bash
git checkout -b feature/my-feature
# work, commit...
git push -u origin feature/my-feature
```

---

## Pull Request Workflow

```bash
# Ensure up to date
git fetch origin
git rebase origin/main

# Push branch
git push -u origin feature/my-feature

# Create PR
gh pr create --title "feat: description" --body "## Summary
- Change 1
- Change 2"
```
