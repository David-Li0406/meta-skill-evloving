---
name: manifest:complete
description: Complete work on the current feature. Use when the user has finished implementing and wants to record their work.
disable-model-invocation: true
---

Complete work on the current in-progress feature.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Find the in-progress feature:
   - Call `find_features` with `project_id` and `state: "in_progress"`
   - If no in-progress features, tell the user there's nothing to complete
   - If multiple in-progress features, list them and ask which one

3. Gather commit information:
   - Run `git log --oneline -10` to get recent commits
   - Present the commits and ask which ones are relevant to this feature
   - Format: `[sha] [message]`

4. Ask for a work summary:
   ```
   Please provide a summary of the work done on "[Feature Title]".

   Format: First line is a concise headline. Add details after a blank line if needed.

   Example:
   Implemented OAuth login flow

   - Added Google OAuth provider
   - Created session management
   - Updated user model with provider field
   ```

5. Complete the feature:
   - Call `complete_feature` with:
     - `feature_id`
     - `summary` from user input
     - `commits` array with selected commit SHAs and messages
     - `mark_implemented: true`

6. Display confirmation:
   ```
   Completed: [Title]
   State: in_progress → implemented

   Recorded [N] commits in history.

   Summary: [First line of summary]
   ```
