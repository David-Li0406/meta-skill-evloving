---
name: pr-review
description: View the PR associated with the current Jujutsu branch/bookmark, including its diff, changes, and any review comments. Use when the user asks to see the PR, check changes, view the diff, or see review feedback for their current branch.
---

# PR Review

View review comments and details for the pull request associated with the current or parent Jujutsu bookmark.

## Usage

Run the script to find and display the PR:

```bash
bash scripts/get_pr_reviews.sh
```

The script will:
1. Find the bookmark on current revision, or traverse parent revisions if needed
2. Search for a PR matching that bookmark/branch name
3. Display the PR details including review comments using `gh pr view`

## How It Works

The script uses:
- `jj log` to find bookmarks on current (@), parent (@-), or grandparent (@--) revisions
- `gh pr list` to find the PR number for the branch
- `gh pr view` to display full PR details with reviews and comments

## Manual Alternative

If needed, you can manually find the bookmark and query GitHub:

```bash
# Find bookmark on current or parent revisions
jj log -r '@|@-|@--' -T 'bookmarks'

# List recent PRs to find the one for your branch
gh pr list --state all --limit 10

# View specific PR
gh pr view <pr-number>
```

## Troubleshooting

- **No bookmark found**: The current and parent revisions don't have bookmarks. Use `jj bookmark list` and `jj bookmark create` to add one.
- **No PR found**: No PR exists for the branch name. Check if the PR uses a different branch name or hasn't been created yet.
