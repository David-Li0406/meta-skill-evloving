---
name: merge-worktree
description: Merge or cherry-pick a worktree branch back into the repo root using a single renderer script.
---

# Merge Worktree

Use this skill when a worktree contains changes that must be merged into the
default branch at the repo root. This workflow is driven by a single renderer
script in the repo root.

## Quick Start

1. Run `bash <path-to-skill>/render-instructions.sh` from the working dir.
2. Follow the steps in the rendered instructions to merge or cherry-pick.

## Workflow

1. Print the instructions with fields substituted.
2. Run the commands in order, using `git -C <worktree_path>` for worktree ops.
3. Resolve conflicts line-by-line with `apply_patch` only.
4. Verify `git status` is clean, then remove the worktree shown in the output
   (not the repo root).

## Helper Script

Use `render-instructions.sh` to render the instruction template with current
repo values (for example `bash <path-to-skill>/render-instructions.sh`).
