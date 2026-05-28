---
name: generating-smart-commits
description: Use this skill when generating conventional commit messages from staged Git changes, triggered by commands like "create commit message", "generate smart commit", "/commit-smart", or "/gc".
---

# Overview

This skill automates the generation of well-formatted, informative commit messages based on staged changes in a Git repository. It adheres to conventional commit standards, saving developers time and ensuring consistency.

## How It Works

1. **Analyzing Staged Changes**: The skill examines the changes currently staged in the Git repository.
2. **Determining Commit Type**: It classifies changes as feat, fix, docs, style, refactor, test, or chore.
3. **Identifying Scope**: The skill extracts the affected module or component from file paths.
4. **Detecting Breaking Changes**: It looks for API changes, removed features, or incompatible modifications.
5. **Formatting Message**: The skill constructs a message following the pattern: `type(scope): description`.
6. **Presenting for Confirmation**: The generated message is displayed to the user for review and approval.

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
3. Present the message to the user for confirmation.

### Example 2: Fixing a Bug

User request: "/gc fix for login issue"

The skill will:
1. Analyze the staged changes related to the login issue.
2. Generate a commit message like: `fix(login): Resolve issue with incorrect password validation`.
3. Present the message to the user for confirmation.

## Best Practices

- **Stage Related Changes**: Ensure that only related changes are staged before generating the commit message.
- **Review Carefully**: Always review the generated commit message before committing to ensure accuracy and clarity.
- **Provide Context**: If necessary, provide additional context in the request to guide the AI analysis (e.g., `/gc - emphasize that this fixes a security vulnerability`).

## Error Handling

Common issues and solutions:

- **No Staged Changes**: Ensure files are staged using `git add <files>` before generating a commit message.
- **Git Not Initialized**: Initialize Git with `git init` or navigate to the repository root if you encounter "Not a git repository".
- **Uncommitted Changes**: Stage relevant changes or use `git stash` for unrelated modifications if you see "Unstaged changes detected".
- **Invalid Commit Format**: Review and manually adjust type, scope, or description if the generated message doesn't follow the conventional format.

## Resources

- [Conventional Commits specification](https://www.conventionalcommits.org/)
- Git commit best practices documentation
- Project-specific commit guidelines in `{baseDir}/000-docs/007-DR-GUID-contributing.md`