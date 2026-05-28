---
name: create-pr
description: A skill to create a pull request on a GitHub repository. Use this skill when the user wants to create a pull request for the changes you have made.
allowed-tools:
  - Read
  - Bash(gh:*)
  - Bash(git:*)
---

# Create Pull Request Skill

To satisfy the user's request to create a pull request on a GitHub repository, follow these steps:

1. Create a new branch for the changes (if not already done).
2. Commit the changes to the new branch.
3. Push the branch to the remote repository.
4. Use the `gh` CLI to create a pull request. The target branch is `master` unless specified otherwise.

Then inform the user that the pull request has been created successfully, providing the URL to the pull request.

## Merging the Pull Request

After the user reviews the pull request and requests to merge it, you can use the `gh` CLI to merge the pull request. Confirm with the user before merging.
