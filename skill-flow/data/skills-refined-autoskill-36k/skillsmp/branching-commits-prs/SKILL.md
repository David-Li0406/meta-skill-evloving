---
name: branching-commits-prs
description: All changes to the repository must be done through a pull request (PR). A branch must always be created, and commits grouped together logically. Whenever asked to create commit messages, to push code, or create a pull request (PR), use this skill so everything is done correctly.
---

# Branches and commit messages

To ensure good history, all code changes need to be grouped together logically into commits, with good messages, and a branch should always be used rather than committing directly to main. Follow these guidelines to ensure we are following these practices.

## Branch

Before performing any commits, ensure a branch has been created for the work. This branch must never be `main`, but should be a branch created specifically for the changes taking place. If no branch is already created, create a new one with a good name based on the changes being made.

## Commits

When committing changes:

1. Review all changes
2. Logically group the changes together
3. Create short commit messages for each group, then commit them

## Merging

**NEVER** merge to main unless explicitly instructed to do so by the user

## Pull request

Before creating a pull request, ensure all tests pass.

When creating a pull request:

- Provide a clear title describing the changes which have been made
- In the body content of the PR:
  - Start with a description of *why* the changes were made based on the conversation history
  - Include a quick list of changes as a bulleted list
  - Provide additional details grouped together logically, following good accessibility practices for headers
  - Include code snippets for important changes
