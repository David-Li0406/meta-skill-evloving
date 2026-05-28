---
name: pr
description: Create a branch and GitHub pull request from current changes (draft by default). Use when the user says "create PR", "open pull request", "submit changes", or wants to push their work for review.
argument-hint: [base-branch]
disable-model-invocation: true
allowed-tools: Bash(gh:*), Bash(git:*)
---

# Pull Request

## Context

- Git status: !`git status -b --porcelain`
- Current branch: !`git rev-parse --abbrev-ref HEAD`
- Diff summary: !`git diff HEAD --stat`
- Remote: !`git remote -v | head -1`

## Rules

- Branch naming: `<type>/<description>` or `#<issue>_<type>/<description>` (for auto issue linking)
- Commit format: Check CONTRIBUTING.md, .gitmessage first, fallback to Conventional Commits (respect project conventions)
- Base branch: `$ARGUMENTS` if provided, otherwise default branch
- PR body ends with a trailing newline

## Steps

1. **Validate**: If no changes exist, inform user and exit

2. **Branch**: If on `main`/`master`, create new branch first

   ```sh
   git switch -c <branch-name>
   ```

3. **Commit**:

   ```sh
   # if more context needed
   git diff HEAD

   git add .
   git commit -m "<type>(scope): <description>"
   ```

4. **Push**:

   ```sh
   git push -u origin <branch-name>
   ```

5. **Create PR** (or update if exists):

   ```sh
   # Get default branch if $ARGUMENTS not provided
   gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'

   # New PR (if branch starts with #<number>_, prepend "closes #<number>" to body)
   gh pr create --title "<title>" --body "<body>" --base <base-branch> --assignee @me --draft

   # Existing PR
   gh pr edit --title "<title>" --body "<body>"
   gh pr view --web
   ```

   Body template:

   ```markdown
   ## Summary

   <description>
   ```

   With issue linking (`#<number>_` branch):

   ```markdown
   closes #<number>

   ---

   ## Summary

   <description>
   ```

## Conventional Commits Types

`chore`, `docs`, `feat`, `fix`, `perf`, `refactor`, `style`, `test`
