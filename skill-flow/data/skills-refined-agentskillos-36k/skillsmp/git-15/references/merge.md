# Git Merge (Trunk-Based)

Merge current feature branch into main branch (Trunk-Based Development).

## Workflow

```
[1] Check current branch
       ↓
[2] Update main branch
       ↓
[3] Checkout to main
       ↓
[4] Merge feature branch (--no-ff)
       ↓
[5] Push main
       ↓
[6] Ask about feature branch deletion
```

## Step-by-Step Details

### 1. Check Current Branch

```bash
git branch --show-current
```

**If on main branch**: Stop and notify
```
⚠️ Currently on main branch.
   Please checkout to a feature branch to merge first.
```

### 2. Check for Changes

```bash
git status
```

**If uncommitted changes exist**: Stop and notify
```
⚠️ Uncommitted changes detected.
   Please commit or stash first, then try again.
```

### 3. Update Main Branch

```bash
git fetch origin main
git checkout main
git pull origin main
```

### 4. Merge Feature Branch

```bash
git merge --no-ff <feature-branch> -m "🔀 merge: <feature-branch> → main

- Feature summary (based on change analysis)"
```

**Reason for `--no-ff`**: Creates merge commit to clarify branch history

**Note**: Merge commits use emoji + merge format since it's not a Conventional Commits standard type.

### 5. Push Main

```bash
git push origin main
```

### 6. Feature Branch Deletion

**Use AskUserQuestion**:
```
Delete feature branch '<branch-name>'?

Options:
1. Delete (local + remote)
2. Delete local only
3. Keep
```

**If deletion selected**:
```bash
# Delete local
git branch -d <feature-branch>

# Delete remote (if selected)
git push origin --delete <feature-branch>
```

## Output Format

```
═══════════════════════════════════════
🔀 Git Merge (Trunk-Based) Started
═══════════════════════════════════════

[1/5] Checking current branch...
      Branch: feature/user-auth

[2/5] Updating main branch...
      ✅ Main updated

[3/5] Checking out to main...
      ✅ Main checkout complete

[4/5] Merging feature branch...
      ✅ Merge complete (--no-ff)

[5/5] Pushing main...
      ✅ Push complete

───────────────────────────────────────
✅ Git Merge Complete
───────────────────────────────────────
```

## Examples

### Execute from Feature Branch

Current branch: `feature/user-auth`

1. Update main
2. Checkout main
3. `git merge --no-ff feature/user-auth -m "🔀 merge: feature/user-auth → main"`
4. Push main
5. Ask about branch deletion

### Merge Commit Message Example

```
🔀 merge: feature/user-auth → main

- Implement user authentication feature
- Add login/signup flow
```

## Cautions

- Stop if executed from main branch
- Stop if uncommitted changes exist
- Guide manual resolution if merge conflict occurs
- Never perform force push
- Never add `Co-Authored-By` pattern
