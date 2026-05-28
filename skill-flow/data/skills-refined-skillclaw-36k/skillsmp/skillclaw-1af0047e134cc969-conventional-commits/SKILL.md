---
name: conventional-commits
description: Use this skill when creating Git commits to ensure they follow the Conventional Commits specification, providing guidance on message structure, types, and best practices for clear and consistent commit messages.
---

# Conventional Commits

This skill provides guidance for writing Git commits that follow the Conventional Commits specification (v1.0.0).

## Purpose

Conventional Commits is a specification for adding human and machine-readable meaning to commit messages. It provides an easy set of rules for creating an explicit commit history, which makes it easier to understand project changes and improve collaboration.

## When to Use This Skill

Use this skill when:
- Creating Git commits
- Reviewing commit messages in PRs
- Writing clear, structured commit messages
- Collaborating on projects with multiple contributors

## Commit Message Structure

### Basic Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```
feat: add user authentication
feat(api): add JWT token generation
fix: resolve memory leak in image processor
docs: update README with setup instructions
refactor(database): optimize user query performance
```

## Commit Types

### Primary Types

**feat** - A new feature for the user
```
feat: add export to PDF functionality
feat(api): add webhook signature verification
```

**fix** - A bug fix for the user
```
fix: resolve login redirect loop
fix(api): handle null response from GitHub webhook
```

**docs** - Documentation only changes
```
docs: update API endpoint documentation
docs(readme): add troubleshooting section
```

**style** - Changes that don't affect code meaning (formatting, whitespace)
```
style: format code with StandardRB
style(css): update button padding
```

**refactor** - Code change that neither fixes a bug nor adds a feature
```
refactor: extract user validation to service object
refactor(models): simplify tenant scoping logic
```

**perf** - Performance improvements
```
perf: add database index for user lookups
perf(queries): reduce N+1 queries in artifacts index
```

**test** - Adding or updating tests
```
test: add specs for user authentication
test(integration): add webhook processing tests
```

**chore** - Changes to build process, dependencies, or maintenance
```
chore: update Rails to 7.2.0
chore(deps): bump dependency version
```