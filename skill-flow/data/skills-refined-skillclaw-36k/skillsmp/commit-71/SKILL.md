---
name: commit
description: Enforces Conventional Commits 1.0.0 for all git commit messages.
---

> **IMPORTANT**: All `\！` (backslash + full-width exclamation mark) in this document MUST be interpreted as a half-width exclamation mark in actual commit messages. This workaround is required because Claude Code has a bug where half-width exclamation marks in markdown files cause errors.

# Conventional Commits (commit)

This skill enforces the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification for all git commit messages. Using this skill ensures that commit history is readable, automated tools (like semantic versioning) can function correctly, and the intent of changes is clear.

## Commit Message Format

The commit message should be structured as follows:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 1. Type

The type is mandatory and must be one of the following:

- **feat**: A new feature for the user, not a new feature for build script.
- **fix**: A bug fix for the user, not a fix to a build script.
- **docs**: Changes to the documentation.
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
- **ci**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs).
- **chore**: Other changes which don't modify src or test files.
- **revert**: Reverts a previous commit.

### 2. Scope (Optional)

A scope may be provided to a type, to provide additional contextual information and is contained within parenthesis, e.g., `feat(parser): add ability to parse arrays`.

### 3. Description

The description is a short summary of the code changes.

- Use the imperative, present tense: "change" not "changed" nor "changes".
- Don't capitalize the first letter.
- No dot (.) at the end.

### 4. Body (Optional)

Used to explain the motivation for the change and contrast this with previous behavior.

- Use the imperative, present tense: "change" not "changed" nor "changes".

### 5. Footer (Optional)

Used to reference GitHub issues, or for BREAKING CHANGE notes.

- **BREAKING CHANGE**: A commit that has a footer `BREAKING CHANGE:` or appends a `\！` after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of a commit of any type.

## Examples

### Feature with Scope

```text
feat(lang): add polish language support
```

### Bug Fix

```text
fix: solve memory leak in buffer allocation
```

### Breaking Change with `\！`

```text
feat\！: send an email to the customer when a product is shipped
```

### Breaking Change with Footer

```text
fix: correct typo in api response

BREAKING CHANGE: the 'id' field is now a string instead of an integer.
```

### Multi-line with Body and Footer

```text
fix: prevent racing condition in session handler

The previous implementation relied on a global lock which caused performance
degradation under high load. This change introduces per-session locking.

Closes #123
```

## Best Practices

### Atomic Commits

Each commit should represent a single logical change. Avoid combining unrelated features, bug fixes, or refactoring into one commit.

- **Easier Troubleshooting**: Pinpoint exactly which change introduced a bug using `git bisect`.
- **Simpler Reverts**: Revert specific changes without affecting other work.
- **Clearer Reviews**: Reviewers can process changes one logical step at a time.

#### Atomic Commit Examples

❌ Bad (Mixed Concerns)

```text
feat: add login page, fix typo in footer, and refactor auth logic
```

✅ Good (Atomic)

```text
feat: add login page
fix: correct typo in footer
refactor(auth): simplify session handling
```

## How to Use

When asked to commit changes, the agent MUST use this format. If the USER provides a message, the agent should reformat it to follow these rules if it doesn't already.
