# Ours vs Theirs Terminology

## The Rebase Trap

During rebase, terminology is **counter-intuitive**. Your commits are replayed onto the target branch, so your own commits become "theirs" while the target branch is "ours".

## Quick Reference Table

| Operation | `HEAD` / `--ours` | `--theirs` / incoming |
|-----------|-------------------|----------------------|
| **merge** | Your current branch | Branch being merged in |
| **rebase** | Target branch (main/master) | Your feature branch commits |
| **cherry-pick** | Your current branch | The cherry-picked commit |
| **stash pop** | Your working tree | The stashed changes |
| **pull** | Your local branch | Remote changes |
| **pull --rebase** | Remote branch | Your local commits |

## Conflict Marker Anatomy

Standard markers:
```
<<<<<<< HEAD
(ours - meaning depends on operation!)
=======
(theirs - meaning depends on operation!)
>>>>>>> branch-name or commit-sha
```

With diff3 style (recommended):
```
<<<<<<< HEAD
(ours)
||||||| merged common ancestor
(original - what both started from)
=======
(theirs)
>>>>>>> branch-name
```

## During Rebase - Detailed Explanation

When rebasing `feature` onto `main`:

1. Git checks out `main` (this becomes HEAD/ours)
2. Git replays each `feature` commit one by one (each is theirs)
3. If commit #3 conflicts, your code from commit #3 is "theirs"

So to keep your feature branch changes: use `--theirs`
To keep main branch state: use `--ours`

## Commands for Each Side

Keep current branch / HEAD:
```bash
git checkout --ours <file>
```

Keep incoming changes:
```bash
git checkout --theirs <file>
```

## Verifying Which is Which

When confused, check the actual content:
```bash
# Show ours version
git show :2:<file>

# Show theirs version
git show :3:<file>

# Show base version (common ancestor)
git show :1:<file>
```
