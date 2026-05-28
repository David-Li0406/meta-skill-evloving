---
name: cross-project-changes
description: Guidance for applying changes across multiple projects. Use when user wants to make changes across multiple projects or apps simultaneously.
---

# Cross-Project Changes

Follow these steps when applying changes across multiple projects.

## Step 1: Identify Target Projects

Determine which projects need the change:
- "all my projects", "all my apps", "all projects" or "all apps" means all folders in `~/code/own/`
- If unsure, ask the user to specify the target projects
- Projects might be nested subfolders under `~/code/own/`, not only direct children
- When searching for files across projects using `ripgrep`, use `**/` globs to handle nested app roots (e.g., `**/find/this/file.rb`)

## Step 2: Determine the Changes

Identify what changes to apply:
- Check if the user described the changes in their prompt
- If they mentioned "changes from the last commit" or similar, inspect the last git commit in the current folder

## Step 3: Apply Changes to Each Project

Process each project individually:
- The implementation may differ between projects based on their structure
- If changes cannot be applied to a project, skip it and continue with the others
- Track which projects succeeded and which were skipped

## Step 4: Run Relevant Tests

For each project where changes were applied:
- Identify tests related to the modified code
- Run those tests to verify the changes work correctly
- Note any projects that lack test coverage for the changes

## Step 5: Report Results

After completing all projects:
- Summarize which projects were updated successfully
- List any projects that were skipped and why
- Mention any projects missing test coverage for the changes
- Do NOT commit changes to git unless explicitly requested
- Remind the user that changes have not been committed yet
