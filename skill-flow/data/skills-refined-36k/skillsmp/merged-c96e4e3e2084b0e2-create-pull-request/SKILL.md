---
name: create-pull-request
description: Use this skill to create or update a pull request for the current branch to the main branch.
---

# Create Pull Request

## Instructions

1. Ensure you are not on the main or master branch.
2. Check for uncommitted changes and warn if present.
3. Get the diff between the current branch and the main branch.
4. Review recent commits on this branch to understand the changes.
5. Create a pull request (PR) with:
   - A clear, descriptive title (override with `--title` if needed).
   - A summary of changes in the body.
   - A test plan section.
6. Push the branch if needed and create the PR using `gh pr create`.

## PR Format

```
Title: <descriptive-title>

## Summary
- <list of changes>

## Test Plan
- <list of testing methods>
```

## Options

| Option     | Description                                           |
|------------|-------------------------------------------------------|
| `--title`  | Override the auto-generated PR title                  |
| `--draft`  | Create as a draft pull request                        |
| `--ready`  | Mark draft PR as ready for review                     |
| `--comments` | Retrieve and display PR review comments              |
| `--analyze` | Analyze comments for requirements compliance (requires `--comments`) |

## What It Does

1. Checks if a PR already exists for the branch.
2. Pushes the branch to origin if needed.
3. Creates a new PR or updates an existing one using the repository's PR template if available, or generates a default description.

## Example Output

```
## Pull Request Created

### Branch
- **Head**: <current-branch>
- **Base**: main

### Pull Request
- **Number**: #<pr-number>
- **Title**: <pr-title>
- **URL**: <pr-url>
```

## Requirements

- Must be run inside a git worktree.
- `git` CLI for branch operations.
- `gh` CLI for PR creation (authenticated).
- Cannot be on the main or master branch.