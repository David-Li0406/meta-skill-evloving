---
name: generating-conventional-commits
description: Use this skill to generate standardized commit messages from staged Git changes, ensuring clarity and consistency in your version control workflow.
---

## Overview

This skill automates the creation of well-formatted, informative commit messages that adhere to the conventional commits standard. It analyzes staged changes in your Git repository and generates messages that save time and improve collaboration.

## How It Works

1. **Analyze Staged Changes**: The skill examines the changes currently staged in the Git repository.
2. **Determine Commit Type**: It classifies changes as `feat`, `fix`, `docs`, etc., and identifies any breaking changes.
3. **Generate Commit Message**: Based on the analysis, it constructs a conventional commit message, including type, scope, and description.
4. **Present for Confirmation**: The generated message is displayed to the user for review and approval.

## When to Use This Skill

This skill activates when you need to:
- Create a commit message from staged changes.
- Generate a conventional commit message.
- Use commands like `/commit-smart` or `/gc`.
- Automate the commit message writing process.

## Examples

### Example 1: Adding a New Feature

User request: "Generate a commit message for adding user authentication"

The skill will:
1. Analyze the staged changes related to user authentication.
2. Generate a commit message like: `feat(auth): Implement user authentication module`.
3. Present the message to the user for confirmation.

### Example 2: Fixing a Bug

User request: "Create a commit for the bug fix."

The skill will:
1. Analyze the staged changes related to a bug fix.
2. Generate a commit message like: `fix: Resolve issue with incorrect password reset`.
3. Present the message to the user for confirmation.

## Best Practices

- **Stage Related Changes**: Ensure that only related changes are staged before generating the commit message.
- **Review Carefully**: Always review the generated commit message before committing to ensure accuracy and clarity.
- **Provide Context**: If necessary, provide additional context in the request to guide the AI analysis.

## Integration

This skill integrates directly with your Git workflow, providing a convenient way to generate commit messages within Claude Code. It complements other Git-related skills in the DevOps Automation Pack.

## Output Format

The generated commit message will follow this pattern:

```
type(scope): brief description

- Detailed explanation of changes
- Why the change was necessary
- Impact on existing functionality

BREAKING CHANGE: description if applicable
```

## Resources

- [Conventional Commits specification](https://www.conventionalcommits.org/)
- Git commit best practices documentation
- Project-specific commit guidelines