---
name: manifest:tree
description: Display the feature hierarchy for the current project. Use when the user wants to see features, project structure, or asks "what features exist?"
disable-model-invocation: true
---

Display the feature tree for the current project.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Render the feature tree:
   - Call `render_feature_tree` with the project ID
   - Use default `max_depth` of 3

3. Display the ASCII tree directly in your response with the legend:
   - ◇ proposed
   - ○ in_progress
   - ● implemented
   - ✗ deprecated
