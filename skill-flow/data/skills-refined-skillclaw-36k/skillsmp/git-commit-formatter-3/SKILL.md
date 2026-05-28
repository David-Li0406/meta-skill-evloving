---
name: git-commit-formatter
description: Formats git commit messages according to Conventional Commits specification. Use this when the user asks to commit changes or write a commit message.
---

# Git Commit Formatter Skill

When writing a git commit message, you MUST follow the Conventional Commits specification.

## Format
`<type>[optional scope]: <description>`

## Allowed Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Instructions
1. Scope of Analysis: Analyze only the Staged Changes (the diff between the Index and HEAD). Ignore all Unstaged Changes.
2. Determine Type: Identify the primary `type` based on allowed types.
3. Identify Scope: Identify the scope if applicable, representing the specific module, component, or file path affected (e.g., (api), (ui), (auth)).
4. Subject Line: Write a concise description in the imperative mood (e.g., "add feature" not "added feature").
   - Constraint: Limit the subject to 50 characters.
   - Format: type(scope): description
5. Body: Provide a detailed body explaining the motivation (why) and the summary of changes (how).
   - Constraint: Wrap lines at 72 characters.
   - Separation: Use a blank line between the subject and the body.
6. Breaking Changes: If the changes break backward compatibility, add a footer starting with BREAKING CHANGE: followed by a description of the change.
7. Security: Always use GPG signing for the commit. Ensure the final command does not include the --no-gpg-sign flag.
8. User Confirmation: Proactively present the generated commit message (subject and body) to the user and ask for their confirmation before executing the `git commit` command.


Example
`feat(auth): implement login with google`
