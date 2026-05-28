---
name: git-commit
description:
  Iteratively, commit atomic changes to the respository. Use when the
  user or agent needs to autonomously commit atomic changes to the
  repository. Employs the "git-add", "git-message", and "git-status" in
  skills in sequence to perform the commit.
---

# Commit changes in the git repository

**`GOAL`**: use the `git-add`, `git-message` and `git-status` skills in
sequence to commit changes in the repository and clean it.

**`WHEN`**: use when the user or agent needs to commit changes in the
repository.

**`NOTE`:** _Await user approval of commit messages before committing.
Make commits only after the user has approved the commit message._

## Workflow

Follow these steps in sequence:

### Step 1: Stage atomic changes

- Invoke the `git-add` skill.
- Capture the status from skill output (`SUCCESS`, `WARN`, or `ERROR`).
- Handle the status:
  - If `ERROR`: Halt and report the error to the user.
  - If `WARN` (no files available): Skip to Step 5.
  - If `SUCCESS` (files staged): Continue to Step 2.

### Step 2: Generate commit message and await approval

- Invoke the `git-message` skill.
- Capture the status from skill output (`APPROVED`,
  `REJECTED_EDIT_FILES`, `REJECTED_REGENERATE`, `REJECTED_ABORT`, or
  `ERROR`).
- Handle the status:
  - If `ERROR`: Halt and report the error to the user.
  - If `APPROVED`: Continue to Step 3.
  - If `REJECTED_EDIT_FILES`: `Unstage` all files with
    `git restore --staged .`, then loop back to Step 1.
  - If `REJECTED_REGENERATE`: Loop back to Step 2.
  - If `REJECTED_ABORT`: Halt and report abort to the user.

### Step 3: Commit changes

**`IMPORTANT`**: _To avoid a recursive loop, **`DON'T`** invoke the
`git-commit` skill here._

- Without using the `git-commit` skill, perform a direct commit with git
  using the approved message.
- If success: report the commit `SHA` and continue to Step 4.
- If failure: Halt and report the error to the user.

### Step 4: Check for more commits (automatic loop control)

- Run `git status --porcelain=v2` to check for remaining changes.
- If no changes: Continue to Step 5.
- If changes remain: automatically loop back to Step 1 (no user prompt
  needed).

### Step 5: Present final status

- Invoke the `git-status` skill.
- **`DONE`**

## Efficiency directives

- Optimize all operations for agent, token, and context efficiency
- Batch operations on file groups, avoid individual file processing
- Use parallel execution when possible
- Target only relevant files
- Reduce token usage
