---
name: useful-commits
description: Use this skill when you need to create, review, or improve commit messages following the Conventional Commits specification with Angular convention.
---

# Skill body

## Purpose

Guide the creation of concise, conventional commit messages that follow the Conventional Commits specification with Angular convention. Enforce strict formatting rules to prevent verbose, unclear commit messages. Focus on communicating what changed and why it changed, not stylistic flourishes.

## Conventional Commits Structure

Follow this exact format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Components

- **Type** (required): Describes the category of change
- **Scope** (optional): Specifies what part of the codebase changed
- **Description** (required): Brief summary of the change
- **Body** (optional): Detailed explanation of what and why
- **Footer** (optional): Breaking changes, issue references, git trailers

## Allowed Types (Angular Convention)

Use exactly these types, no others:

- `feat` - New feature for the user
- `fix` - Bug fix for the user
- `docs` - Documentation only changes
- `style` - Code style changes (formatting, missing semicolons, etc.) that don't affect code meaning
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `perf` - Code change that improves performance
- `test` - Adding or correcting tests
- `build` - Changes to build system or external dependencies
- `ci` - Changes to CI configuration files and scripts
- `chore` - Other changes that don't modify src or test files

## Critical Formatting Rules

### Subject Line (type + scope + description)

- **Character limit**: Maximum 70 characters including type and scope
- **Mood**: Use imperative mood (command form: "add", "fix", "update", not "added", "fixes", "updating")
- **Capitalization**: Do not capitalize the first letter of description
- **Punctuation**: Do not end with a period
- **Format**: `type(scope): description` or `type: description`

### Examples

```
feat(auth): add JWT token refresh mechanism
fix: prevent race condition in event handlers
docs: update API documentation for v2 endpoints
```

### Anti-patterns

- Avoid vague descriptions
- Do not use past tense
- Avoid unnecessary details in the subject line