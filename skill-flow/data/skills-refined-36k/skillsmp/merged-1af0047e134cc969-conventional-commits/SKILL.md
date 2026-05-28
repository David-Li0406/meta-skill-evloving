---
name: conventional-commits
description: Use this skill when creating Git commits to ensure they follow the Conventional Commits specification, providing guidance on message structure, types, scopes, and best practices for clear and consistent commit messages.
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
fix: resolve memory leak in image processor
docs: update README with setup instructions
refactor(database): optimize user query performance
```

## Commit Types

### Primary Types

**feat** - A new feature for the user
```
feat: add export to PDF functionality
```

**fix** - A bug fix for the user
```
fix: resolve login redirect loop
```

**docs** - Documentation only changes
```
docs: update API endpoint documentation
```

**style** - Changes that don't affect code meaning (formatting, whitespace)
```
style: format code with gofmt
```

**refactor** - Code change that neither fixes a bug nor adds a feature
```
refactor: extract user validation to service
```

**perf** - Performance improvements
```
perf: add database index for user lookups
```

**test** - Adding or updating tests
```
test: add tests for user authentication
```

**chore** - Changes to build process, dependencies, or maintenance
```
chore: update Go to 1.23.5
```

### Additional Types

**build** - Changes to build system or dependencies
```
build: configure Docker for production
```

**ci** - Changes to CI configuration
```
ci: add security scanning to workflow
```

**revert** - Reverts a previous commit
```
revert: revert "feat: add export feature"
```

## Scope (Optional)

Scope provides additional context about what part of the codebase changed:
```
feat(auth): add two-factor authentication
fix(api): handle rate limit errors
```

**Common scope examples:**
- `auth` - Authentication/authorization
- `api` - API endpoints
- `ui` - User interface components
- `database` - Database models/migrations
- `services` - Service objects
- `tests` - Test suite
- `deps` - Dependencies
- `docs` - Documentation

## Description

The description is a short summary of the code change:

**Rules:**
- Use imperative, present tense: "add" not "added" or "adds"
- Don't capitalize first letter
- No period (.) at the end
- Keep under 72 characters (ideally under 50)

**Good descriptions:**
```
add user profile page
fix memory leak in file upload
```

**Bad descriptions:**
```
Added user profile page          # Past tense
Fix Memory Leak In File Upload   # Capitalized
```

## Body (Optional)

The body provides additional context about the change:

**When to include a body:**
- Complex changes needing explanation
- Non-obvious design decisions
- Breaking changes
- Migration instructions

**Format:**
- Separate from description with blank line
- Use imperative mood like description
- Wrap at 72 characters
- Can include multiple paragraphs

**Example:**
```
feat(api): add webhook signature verification

Add HMAC-SHA256 signature verification for all incoming webhooks
to prevent unauthorized access and replay attacks.
```

## Footer (Optional)

Footers provide metadata about the commit:

### Breaking Changes

Use `BREAKING CHANGE:` footer for incompatible API changes:
```
feat(api): change authentication endpoint

BREAKING CHANGE: The /auth endpoint now requires a client_id parameter.
```

### Issue References

Reference issues and pull requests:
```
fix(auth): resolve session timeout bug

Fixes #123
```

### Co-authors

Credit multiple contributors:
```
feat: add data export feature

Co-authored-by: Jane Doe <jane@example.com>
```

## Complete Examples

### Simple Feature
```
feat: add password reset functionality
```

### Bug Fix with Body
```
fix(api): handle rate limit errors

When external API returns 429 status, retry the request
with exponential backoff up to 3 attempts before failing.
```

### Breaking Change
```
feat(api)!: redesign webhook payload structure

BREAKING CHANGE: Webhook payloads now use a nested structure.
```

## Best Practices

### Do:
- Use present tense imperative mood ("add" not "added")
- Keep first line under 50 characters when possible
- Reference issues/PRs in footer
- Explain "why" in body, not "what" (code shows what)
- Break up large changes into multiple commits
- Make commits atomic (one logical change per commit)

### Don't:
- Use vague descriptions ("fix stuff", "updates")
- Combine multiple unrelated changes in one commit
- Capitalize first letter of description
- End description with period
- Use past tense ("added", "fixed")
- Commit broken code (each commit should work)

## Summary

Conventional Commits provide:
- Clear, consistent commit history
- Better collaboration through explicit intent
- Easier code review and git history navigation
- Improved project documentation through structured messages

**Key formula:**
```
<type>(<scope>): <description>

[body]

[footer]
```