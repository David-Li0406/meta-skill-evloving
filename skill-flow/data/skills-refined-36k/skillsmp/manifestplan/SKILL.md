---
name: manifest:plan
description: Interactive feature planning session. Use when the user wants to plan features, break down a PRD, or design the feature tree.
disable-model-invocation: true
---

Run an interactive feature planning session.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, offer to run `init_project` first

2. Gather input:
   - Ask the user what they want to plan:
     ```
     What would you like to plan?

     Options:
     - Paste a PRD, spec, or feature description
     - Describe the capabilities you want to add
     - Say "analyze" to let me examine the codebase
     ```

3. Design the feature tree:
   - Apply the user story test to each feature: "As a [user], I can [capability]..."
   - Name features by capability (e.g., "Router" not "Implement routing")
   - Group related features under parent nodes
   - Assign priorities (lower = implement first)

4. Present the proposal:
   - Call `plan` with `confirm: false` to get a preview
   - Display the proposed tree:
     ```
     Proposed Feature Tree:

     ◇ [Parent Feature]
     │  [Description]
     ├── ◇ [Child Feature 1] (priority: 1)
     │      [Description]
     └── ◇ [Child Feature 2] (priority: 2)
             [Description]

     Does this look right? I can adjust the structure, add details, or create it.
     ```

5. Iterate or confirm:
   - If user wants changes, modify and re-present
   - If user approves, call `plan` with `confirm: true`

6. Display result:
   ```
   Created [N] features.

   Use /manifest:tree to see the full hierarchy.
   Use /manifest:start to begin work on the first feature.
   ```
