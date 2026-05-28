---
name: resolve-git-conflicts
description: Resolve git merge conflicts, rebase conflicts, cherry-pick conflicts, and stash pop conflicts. Use when git status shows "unmerged paths", "rebase in progress", "cherry-pick in progress", or after failed stash pop. Handles overlapping edits, edit/delete conflicts, rename conflicts, binary conflicts, and helps user choose between ours/theirs or manual merge.
---

# Git Conflict Resolution

Resolve conflicts safely, asking for guidance on ambiguous decisions.

## Step 1: Diagnose

```bash
git status
git diff --name-only --diff-filter=U
```

Determine operation type from status output:

- "You have unmerged paths" + MERGE_HEAD = **merge**
- "rebase in progress" = **rebase**
- "cherry-pick in progress" = **cherry-pick**
- After `git stash pop` with conflicts = **stash**

Report: operation type, source/target branches, conflicted files.

## Step 2: Explain Context

**CRITICAL**: Ours/theirs meaning flips during rebase! Read `references/terminology.md` if needed.

Quick reference (explain to user before showing conflicts):

| Operation | `--ours` / HEAD | `--theirs` / incoming |
|-----------|-----------------|----------------------|
| merge | Your branch | Branch being merged |
| rebase | Target (main) | Your commits |
| cherry-pick | Your branch | Picked commit |
| stash pop | Working tree | Stashed changes |

## Step 3: For Each Conflicted File

1. Run `git diff <file>` to see conflict markers
2. Identify conflict type (see `references/conflict-types.md` if unclear)
3. **Explain the conflict to user in plain terms:**
   - What the file does (infer from name/content)
   - What "ours" changed and why it might matter
   - What "theirs" changed and why it might matter
   - Whether changes overlap or are independent
4. **Ask user** which approach with clear options:
   - Keep ours: [summarize what stays/goes]
   - Keep theirs: [summarize what stays/goes]
   - Merge both: [if feasible, explain how]
   - Skip commit (rebase only)

**Context matters**: Users may not remember what changes they made days ago. Always summarize the actual code differences, not just "ours vs theirs".

## Step 4: After Each File

```bash
git add <file>
```

## Step 5: Continue Operation

| Operation | Command |
|-----------|---------|
| merge | `git commit` |
| rebase | `git rebase --continue` |
| cherry-pick | `git cherry-pick --continue` |
| stash | Done (optionally `git stash drop`) |

If rebase/cherry-pick shows more conflicts, repeat from Step 1.

## Abort Options

Always remind user they can abort safely:

- `git merge --abort`
- `git rebase --abort`
- `git cherry-pick --abort`

## Safety Rules

1. **Never auto-resolve** when both sides have meaningful changes
2. **Never run destructive commands** without explicit confirmation
3. **Show diffs before applying** any resolution
4. **Warn about data loss** when discarding changes

## Example Flow

```text
$ git status
rebase in progress; onto abc123
You have unmerged paths.
  Unmerged paths:
    both modified:   src/config.js

$ git diff src/config.js
<<<<<<< HEAD
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature-branch
```

→ "Conflict in `src/config.js` (app configuration).

**What happened**: Both branches changed the API timeout value.

- **main** (current target): timeout = 5000ms (5 seconds)
- **your feature branch**: timeout = 10000ms (10 seconds)

This looks like your feature branch doubled the timeout—maybe for slower API calls?

**Options**:

1. Keep 5000ms (main's value) - faster timeout, may cause issues if your feature needs longer
2. Keep 10000ms (your value) - longer timeout you added
3. Different value - if neither is right

Which do you want?"

User: "Keep mine"

→ `git checkout --theirs src/config.js && git add src/config.js && git rebase --continue`

## Reference Files

- `references/terminology.md` - Ours vs theirs for each operation type
- `references/conflict-types.md` - Different conflict scenarios (read when conflict type unclear)
- `references/commands.md` - Diagnostic and resolution commands
- `references/safety.md` - Abort procedures and safety checks
