---
name: generating-smart-commits
description: Use this skill when you need to generate conventional commit messages from staged Git changes, ensuring clarity and adherence to standards.
---

# Skill body

## Overview

This skill empowers you to create well-formatted, informative commit messages automatically. By analyzing staged changes, it generates messages that adhere to conventional commit standards, saving time and ensuring consistency.

## How It Works

1. **Analyzing Staged Changes**: The skill examines the changes currently staged in the Git repository.
2. **Determining Commit Type**: It classifies changes as feat, fix, docs, style, refactor, test, or chore.
3. **Identifying Scope**: The skill extracts the affected module or component from file paths.
4. **Detecting Breaking Changes**: It looks for API changes, removed features, or incompatible modifications.
5. **Generating Commit Message**: Based on the analysis, it constructs a conventional commit message, including type, scope, and description.
6. **Presenting for Confirmation**: The generated message is displayed to you for review and approval.

## When to Use This Skill

This skill activates when you need to:
- Create a commit message from staged changes.
- Generate a conventional commit message.
- Use the `/commit-smart` or `/gc` command.
- Automate the commit message writing process.

## Examples

### Example 1: Adding a New Feature

User request: "Generate a commit message for adding user authentication"

The skill will:
1. Analyze the staged changes related to user authentication.
2. Generate a commit message like: `feat(auth): Implement user authentication module`.
3. Present the message to you for confirmation.

### Example 2: Fixing a Bug

User request: "/gc fix for login issue"

The skill will:
1. Analyze the staged changes related to the login issue.
2. Generate a commit message like: `fix(login): Resolve issue with incorrect password validation`.
3. Present the message to you for confirmation.

## Best Practices

- **Stage Related Changes**: Ensure that only related changes are staged before generating the commit message.
- **Review Carefully**: Always review the generated commit message before committing to ensure accuracy and clarity.
- **Provide Context**: If necessary, provide additional context in the request to guide the AI analysis (e.g., `/gc - emphasize that this fixes a security vulnerability`).

## Error Handling

Common issues and solutions:

- **No Staged Changes**: Ensure you have staged files using `git add <files>` before generating a commit message.
- **Git Not Initialized**: Initialize git with `git init` or navigate to the repository root if you encounter "Not a git repository".
- **Uncommitted Changes**: Stage relevant changes or use `git stash` for unrelated modifications if you see warnings about unstaged changes.
- **Invalid Commit Format**: Review and manually adjust the generated message if it doesn't follow the conventional format.

## Integration

This skill integrates directly with your Git workflow, enhancing your commit message generation process.