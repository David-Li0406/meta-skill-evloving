---
name: manifest:feature
description: Search for and display feature details. Use when the user wants to find a specific feature or asks about a feature by name.
disable-model-invocation: true
argument-hint: "[search query]"
---

Search for and display feature details.

## Arguments

`$ARGUMENTS` - Search query to find the feature (title or content)

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Search for features:
   - Call `find_features` with `project_id` and `query` set to `$ARGUMENTS`
   - If no matches found, tell the user and suggest checking spelling or using `/manifest:tree`

3. If multiple matches, list them and ask which one:
   ```
   Found N features matching "[query]":
   1. [Title] ([state])
   2. [Title] ([state])

   Which feature would you like to see details for?
   ```

4. Get full feature details:
   - Call `get_feature` with `feature_id` and `include_history: true`

5. Display the feature:
   ```
   Feature: [Title] ([state])
   Parent: [Parent title if any]
   Priority: [priority]
   Version: [target version if assigned]

   ## Description
   [Feature details]

   ## History
   [List of history entries with dates and summaries]
   ```
