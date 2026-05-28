---
name: github-merge-pr
description: Merges a pull request after verifying checks pass.
---

# Merge Pull Request

## Instructions
1. If no PR number provided, find the PR for the current branch
2. Check PR status (reviews, CI checks)
3. Warn if checks are failing or reviews are pending
4. Merge the PR using squash merge by default
5. Optionally delete the branch after merge
