---
name: manifest:start
description: Begin work on a feature. Use when the user wants to start working on a feature or says "let's work on X".
disable-model-invocation: true
argument-hint: "[feature name or blank for next]"
---

Begin work on a feature.

## Arguments

`$ARGUMENTS` - Optional feature name to start. If blank, starts the next priority feature.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Find the feature to start:

   **If $ARGUMENTS is provided:**
   - Call `find_features` with `project_id` and `query` set to `$ARGUMENTS`
   - If no matches, tell the user and suggest `/manifest:tree`
   - If multiple matches, list them and ask which one

   **If $ARGUMENTS is blank:**
   - Call `get_next_feature` with the project ID
   - If no feature found, tell the user there's nothing to work on

3. Start the feature:
   - Call `start_feature` with the feature ID

4. Display the result:
   ```
   Started: [Title]
   State: [previous state] → in_progress

   ## Specification
   [Feature details - this is what you're implementing]

   ## Acceptance Criteria
   [Any criteria from the feature details]

   ## History
   [Previous work if any - check before starting fresh]
   ```

5. Remind the user:
   ```
   When you're done, use /manifest:complete to record your work.
   ```

## Important

**Do not change the feature's target version during implementation.** The version assignment is locked while work is in progress. If a feature needs to be moved to a different version, complete or pause the work first.
