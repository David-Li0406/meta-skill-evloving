---
name: manifest:assign
description: Assign a feature to a version. Use when the user wants to schedule a feature for a release.
disable-model-invocation: true
argument-hint: "[feature] [version]"
---

Assign a feature to a target version.

## Arguments

`$ARGUMENTS` - Feature name and version name, e.g., "Router v0.2.0"

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Parse arguments:
   - Extract feature search term and version name from $ARGUMENTS
   - If unclear, ask for clarification:
     ```
     Please specify both feature and version:
     /manifest:assign [feature name] [version name]

     Example: /manifest:assign Router v0.2.0
     ```

3. Find the feature:
   - Call `find_features` with `project_id` and `query`
   - If no matches or multiple matches, clarify with user

4. Find the version:
   - Call `list_versions` with the project ID
   - Match by name
   - If not found, list available versions

5. Assign the feature:
   - Call `set_feature_version` with `feature_id` and `version_id`

6. Display result:
   ```
   Assigned: [Feature title] → [Version name]

   [Version name] now has [N] features.
   ```

## Unassigning

To remove a feature from a version, the user can say "unassign [feature]" and you should:
- Call `set_feature_version` with `feature_id` and `version_id: null`
- Confirm: "Unassigned: [Feature title] (now in backlog)"
