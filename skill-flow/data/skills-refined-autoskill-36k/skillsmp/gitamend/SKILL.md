---
name: git:amend
description: Amend Commit - modifies the last commit with staged changes or new message
---

# Amend Commit

Modifies the most recent commit by adding staged changes, updating the message, or both. Follows Conventional Commits specification for message formatting.

## When to use

Use this skill when the user needs to:
- Add forgotten files to the last commit
- Fix a typo in the last commit message
- Combine small fixes into the previous commit
- Update commit message to follow conventions

## Instructions

### Step 1: Check Current State

1. Run `git log -1 --pretty=format:"%h %s"` to show the last commit
2. Run `git diff --cached --stat` to see if there are staged changes
3. Run `git diff --stat` to see unstaged changes

Display to user:
```
Last commit: a1b2c3d feat(auth): add login form

Staged changes: 2 files
Unstaged changes: 1 file
```

### Step 2: Determine Amend Type

Based on state and user intent:

| Scenario | Action |
|----------|--------|
| Staged changes, no message provided | Add changes, keep message |
| No staged changes, message provided | Update message only |
| Staged changes + message provided | Add changes + update message |
| No staged changes, no message | Ask what user wants to do |

### Step 3: Handle Staged Changes

If there are staged changes to add:
1. Show the diff summary
2. Confirm these should be added to the last commit
3. Warn if changes seem unrelated to the original commit

### Step 4: Handle Message Update

If updating the message:

1. **Parse current message** - Extract type, scope, description
2. **Apply changes**:
   - If user provides full message → use it
   - If user provides partial (e.g., just type) → merge with existing
3. **Validate format** - Ensure Conventional Commits compliance

**Quick fixes:**
- `git:amend fix` → Change type to `fix`, keep rest
- `git:amend (api)` → Change scope to `api`, keep rest
- `git:amend "better description"` → Update description only

### Step 5: Confirm and Execute

Show the planned changes:
```
Amending commit a1b2c3d

Current:  feat(auth): add login form
New:      fix(auth): add login form validation

Adding: 2 files (+15, -3 lines)

Proceed? [Y/n]
```

If approved, run:
```bash
# Message change only
git commit --amend -m "<new message>"

# Changes only (keep message)
git commit --amend --no-edit

# Both
git commit --amend -m "<new message>"
```

**Important:** Do NOT add `Co-Authored-By`, `Signed-off-by`, or any other trailers to the commit message.

### Step 6: Safety Checks

**Before amending, verify:**

1. **Not pushed** - Warn if commit exists on remote:
   ```
   ⚠️ Warning: This commit appears to be pushed to origin.
   Amending will require force push. Continue? [y/N]
   ```

2. **Not a merge commit** - Refuse to amend merge commits:
   ```
   ❌ Cannot amend merge commits. Use git revert instead.
   ```

3. **Clean working tree** - If there are unstaged changes, ask:
   ```
   You have unstaged changes. Options:
   1. Stage all and include in amend
   2. Amend with only currently staged changes
   3. Cancel
   ```

## Error Handling

- If amend fails, show the error and suggest fixes
- If there's nothing to amend (no changes, same message), inform user
- If in rebase/merge state, refuse and explain

## Arguments

- `<args>` - Optional. Can include:
  - New type: `feat`, `fix`, `docs`, etc.
  - New scope: `(auth)`, `(api)`
  - New message: `"full commit message"`
  - `--no-edit` - Keep current message, just add staged changes

Examples:
- `git:amend` - Interactive: ask what to change
- `git:amend --no-edit` - Add staged changes, keep message
- `git:amend fix` - Change commit type to fix
- `git:amend (api)` - Change scope to api
- `git:amend "feat(auth): add login validation"` - Replace entire message
