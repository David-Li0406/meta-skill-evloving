---
name: implementing-github-issue
description: You are an expert at implementing GitHub issues and you have been assigned an issue to work on.
---

# Implementing GitHub Issue Skill

This skill guides the process to implement a GitHub issue.

## GitHub Issue Implementation Notes

- You do NOT need to ask me to proceed at any stage, you should work with autonomy as much as possible unless explicity asked otherwise.
- You MUST carry out each implementation step in order, ensure that each step is successful before continuing to the next.
- You MUST use a git worktree to implement an issue.

## GitHub Issue Implementation Workflow

1. Ensure you have run ./utils/help.sh script to learn what scripts are available to use.
2. Ensure you are on the main git branch.
3. Ensure you have the pulled the latest from remote.
4. Ensure the branch is in a clean state.
5. Ensure you understand which issue id you should be working on, if you have not been explicitly told then stop working on this task.
6. Update the GitHub issue so that its status is "In Progress" if it wasn't already.
7. Add a comment onto the GitHub issue detailing what agent you are and the date / time that you have begun working on the issue.
8. Create a new git worktree under the folder /tmp/claude/ for working on the issue, use a name in the format "{PROJECT_NAME}-issue-{ISSUE_ID}".
9. Use the issue id to read the information such as title, description or comments from the issue to determine what your task is.
10. Carry out and complete the task.
11. Clean up the local git worktree.
12. Carry out a review of any errors that occurred when calling scripts during this task and explain how you managed to correct your understanding usage of the script, i.e. recommend changes to the way you used it for next time. Add the review summary as a comment on the GitHub issue.
13. Update the GitHub issue so that its status is "Todo", if human interaction is required because a PR needs to be merged or the issue could not be fully completed then update the GitHub issue by adding the "help wanted" label to it.
