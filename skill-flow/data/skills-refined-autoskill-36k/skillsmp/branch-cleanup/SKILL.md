---
name: branch-cleanup
description: Squash fixup commits and consolidate branch before merge
disable-model-invocation: true
allowed-tools: Bash, Read
---

Consolidate fixup commits into clean logical commits before merge.

## When to Use

- Before merging a feature branch to main
- After iterative development with multiple fixup commits
- When commit history needs cleanup for review

## Process

1. Verify clean working tree: `git status`
2. Create backup branch: `git branch backup-$(git branch --show-current)-$(date +%s)`
3. Show current commits: `git log --oneline origin/main..HEAD`
4. Run autosquash rebase:
   ```bash
   GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main
   ```
5. Verify result: `nix flake check`
6. Compare with backup: `git diff backup-*..HEAD` should be empty
7. Show final commits: `git log --oneline origin/main..HEAD`

## Manual Cleanup (requires user approval)

If autosquash rebase is not sufficient due to complex interleaved changes:

1. ASK USER for approval before proceeding with soft reset
2. `git reset --soft origin/main`
3. `git reset HEAD -- .`
4. Stage and commit in logical groups using `/commit` skill
5. Verify: `nix flake check`

Soft reset rewrites history more aggressively than rebase. Only use when rebase
cannot produce clean commits.

## Principles

- One logical change per final commit
- Squash all fixups into their target commits
- Drop commits that are immediately superseded
- Preserve struggle documentation in code comments, not commit history
- Separate CLAUDE.md changes from code commits

## Rules

- NEVER force push without user confirmation
- NEVER delete backup branch automatically
- ALWAYS verify nix flake check passes after rebase
- ALWAYS show before/after commit list to user
