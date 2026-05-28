---
name: commit
description: This skill should be used when the user wants to commit staged changes to git. It analyzes the staged changes, generates an appropriate commit message, and executes the commit after user approval.
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff --cached), Bash(git commit -m:*)
---

# Git Commit Helper

This skill helps create well-formatted git commit messages based on staged changes.

## Context

```
% git status
!`git status`

% git diff --cached
!`git diff --cached`

% git branch --show-current
!`git branch --show-current`

% git log --oneline -10
!`git log --oneline -10`
```

## Instructions:

1. Check the current branch. If it is 'main', abort the commit and ask the user to switch to a different branch.

2. If not on 'main', analyze the staged changes in the git diff.

3. Generate a commit message following this format:

   ```
   {one line commit summary}

   {more detailed description of changes if necessary}
   ```

4. Ensure your commit message adheres to these rules:
   - Do not mention Claude Code, AI assistance, or any related terms
   - Do not include co-author information
   - Keep the summary line concise and informative
   - Provide a more detailed description only if necessary

5. If you need to revise your commit message, do so until it meets all criteria.

Before generating the final commit message, wrap your analysis inside <git_analysis> tags in your thinking block. This analysis should include:

- A summary of the git status, diff, and recent commits
- A list of all files changed and the type of changes (added, modified, deleted)
- Identification of the main theme or purpose of the changes
- Brainstorming of a few potential commit messages

This will help ensure a thorough interpretation of the git diff and status.

Here's an example of a good commit message format:

```
Implement user authentication feature

- Add login and registration endpoints
- Create user model
- Set up JWT token generation
```

Remember, the key is to be descriptive yet concise, focusing on what was changed and why.

Now, please proceed with your analysis and commit message generation based on the provided git information. Once the user has approve the commit message, commit the changes.
