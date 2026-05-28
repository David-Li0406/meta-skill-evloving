---
name: finish-plan
description: Merge completed plan to main, cleanup feature branch, and mark plan as done
---

# Finish Plan

Merge a completed plan to main and cleanup.

**Usage**: "finish plan `<id>`"

---

## Instructions

When the user asks to finish a plan:

### 1. Find and Verify Plan

```bash
ls plan/<id>-*.md
```

Read the plan file and verify:
- All tasks are marked `[x]` complete
- If incomplete tasks exist, **ask user** if they want to proceed anyway

### 2. Verify Current State

```bash
git status
git branch --show-current
```

Ensure:
- Working directory is clean
- Currently on the feature branch `feature/<id>-<title>`

### 3. Switch to Main and Update

```bash
git checkout main
git pull origin main
```

### 4. Merge Feature Branch

Use squash merge to combine all commits:

```bash
git merge --squash feature/<id>-<title>
```

### 5. Create Final Commit

```bash
git commit -m "feat: <title> (#<id>)"
```

Use the plan's objective to write a meaningful commit message.

### 6. Delete Feature Branch

```bash
git branch -d feature/<id>-<title>
```

### 7. Update Plan Status

Edit the plan file:
- Change `**Status**: in-progress` to `**Status**: done`

---

## Example

**User**: "finish plan 001"

**Assistant**:

1. Reads `plan/001-qr-code.md`
2. Verifies all tasks are `[x]`
3. Runs:
   ```bash
   git checkout main
   git pull origin main
   git merge --squash feature/001-qr-code
   git commit -m "feat: add qr code generation support (#001)"
   git branch -d feature/001-qr-code
   ```
4. Updates plan status to `done`

---

## Handling Incomplete Plans

If some tasks are not marked complete:

```
Plan 001-qr-code has incomplete tasks:

Step 2: Template Integration
- [ ] Add positioning and sizing support

Step 3: Documentation (not started)
- [ ] Add QR code usage examples
- [ ] Update API documentation

Do you want to:
1. Finish anyway (merge current progress)
2. Cancel and complete remaining tasks first
```

Wait for user decision.

---

## Important Rules

1. **Verify completion** - Check all tasks before merging
2. **Pull before merge** - Always `git pull` on main first
3. **Squash merge** - Keep main history clean
4. **Meaningful commit** - Final commit should describe the feature
5. **Cleanup** - Delete the feature branch after merge

---

## Do NOT Push

This skill merges locally only. The user should push when ready:

```bash
git push origin main
```

Inform the user they can push when ready.

---

## Checklist

- [ ] All plan tasks verified complete (or user confirmed proceed)
- [ ] Main branch updated with `git pull`
- [ ] Feature branch squash-merged
- [ ] Final commit created with descriptive message
- [ ] Feature branch deleted
- [ ] Plan status updated to `done`
- [ ] User informed about pushing
