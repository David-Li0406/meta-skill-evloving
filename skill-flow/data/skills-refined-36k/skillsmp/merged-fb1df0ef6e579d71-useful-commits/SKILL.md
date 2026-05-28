---
name: useful-commits
description: Use this skill when you need guidance on creating, reviewing, or improving commit messages following the Conventional Commits specification with Angular convention.
---

# Useful Commits

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

**Examples:**
```
feat(auth): add JWT token refresh mechanism
fix: prevent race condition in event handlers
docs: update API documentation for v2 endpoints
```

**Anti-patterns:**
```
feat: Added new feature.        ❌ Capitalized, ends with period
Fix bug                         ❌ Not lowercase type, missing colon
refactor: Refactored code       ❌ Not imperative mood, capitalized
feat(Auth): adds feature        ❌ Capitalized scope, present tense
```

### Body

- **Line wrapping**: Wrap at 90 characters
- **Maximum length**: 700 characters total (excluding footers/git trailers)
- **Capitalization**: Do capitalize the first letter of sentences in body
- **Blank line**: Separate subject from body with one blank line
- **Content**: Explain what and why, not how
- **Bullet points**: Maximum 8 bullet points if using bullets
- **Paragraph structure**: Keep succinct, prefer bullets for lists

**Purpose**: Answer these questions:
- Why have I made these changes?
- What effect have my changes made?
- Why was the change needed?
- What are the changes in reference to?

### Footers (Git Trailers)

**Format**: `FOOTER-TOKEN: footer value` or `FOOTER-TOKEN #value`

**Common footers:**
- `BREAKING CHANGE: description` - For breaking changes
- `Refs: #123` - Reference to issue
- `Co-Authored-By: Name <email>` - Co-authors

**Not counted** toward 700 character body limit

## Scope Guidelines

Use scopes sparingly and consistently:

- **Consistency**: Once established, always use the same scope name
- **Lowercase only**: Scopes must be lowercase
- **Concept-focused**: Use the concept/component name, not filenames
- **Multiple scopes**: Comma-separated if change affects multiple areas
- **Omit when unclear**: If scope is unclear or change is global, omit it

## Breaking Changes

Always include breaking change notation unless explicitly told "this is prerelease, don't worry about breaking changes"

**Format**: Both are required
1. Add `!` after type/scope: `feat!:` or `feat(api)!:`
2. Add `BREAKING CHANGE:` footer with description

## Prohibited Content

**Never include:**
- References to local spec files
- GitHub issue numbers are allowed: `Refs: #123`, `Fixes #456`

## Writing Good Commit Messages

### Include What Changed + Why

Don't assume the reader understands the context. They may not have access to the story or ticket.

### Check for Logical Separation

If it's difficult to summarize the commit within 700 characters or 8 bullet points, the commit likely includes several logical changes and should be split.

## Quick Examples

### Good Commits

```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh when tokens expire within 5 minutes
of API calls. This prevents users from being logged out during active
sessions. Refresh happens transparently in the background.
```

### Bad Commits (with explanations)

```
feat: Added new feature to the app.
```
**Problems**: Capitalized, ends with period, vague description, past tense

## Additional Resources

For comprehensive guidance, consult:
- **`references/scopes.md`** - Detailed scope usage patterns and consistency guidelines
- **`references/breaking-changes.md`** - Complete breaking change notation and pre-release handling
- **`references/conventional-commits-spec.md`** - Full Conventional Commits specification
- **`references/writing-guide.md`** - Extended philosophy on writing meaningful commit messages

## Workflow Integration

When creating commits:

1. Review staged changes with `git diff --staged`
2. Identify the primary type (feat, fix, refactor, etc.)
3. Determine if scope is clear and consistent
4. Draft subject line (imperative mood, lowercase, no period)
5. Check subject line length (≤70 chars including type and scope)
6. If body needed, explain what and why (not how)
7. Wrap body at 90 characters, keep under 700 characters
8. Add breaking change notation if applicable
9. Verify no local spec references
10. Double-check imperative mood and capitalization rules

Apply these rules strictly to every commit message without exception.