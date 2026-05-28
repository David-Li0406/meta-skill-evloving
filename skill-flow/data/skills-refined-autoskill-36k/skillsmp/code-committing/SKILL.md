---
name: code-committing
description: Generates semantic commit messages and commits code changes to version control. Use when staging changes, creating commits, writing commit messages, or when the user mentions git, commit, staging, or version control. Supports monorepo package updates tracking.
license: Unlicense
---

# Code Committing

## Step-by-Step Process

1. **Review the changes**: Carefully read the diff to understand what was modified
2. **Identify the type**: Determine the appropriate commit type (feat, fix, docs, etc.)
3. **Determine scope**: Identify the module or package name affected (for monorepo: use exact package name or `all`)
4. **Check for package updates**: Look for dependency version changes in package.json or similar files
5. **Write the summary**: Create a concise, imperative mood summary (≤50 characters)
6. **Add body bullets** (if needed): List additional details with emojis, each line ≤100 characters
7. **Add context** (optional): Include brief explanation of why the change was made, impact, or edge cases handled (keep it concise, this is a commit message not documentation)
8. **Include package updates**: Add a bullet for each updated package with version change
9. **Mark breaking changes** (if applicable): Add `!` to the type and include `BREAKING CHANGE:` footer

## Commit Message Format

- **ALWAYS write commit messages in English only** - no other languages allowed
- Use semantic commit style (also known as conventional commits)
 Format: `<type>(<scope>): summary` or `<type>: summary` (≤50 chars, imperative)
- Body (optional): bullets `- {emoji} {text}` (≤100 chars/line) following after blank line
- Wrap package names, file names, or code snippets in backticks (`) for better readability

### Examples

```text
feat(button): add loading state

- ✨ Add spinner icon during async operations
- 📦 @ui/icons: v1.0.0 → v1.1.0
```

```text
fix(text-input): prevent double focus events

- 🐛 Debounce focus handler to avoid duplicate calls
```

```text
feat(collapsible): add aria-expanded attribute

- ♿ Improve screen reader support for collapsed state
- 🎯 Fixes accessibility issue where panel state wasn't announced
```

```text
feat(theme)!: redesign color tokens

- ✨ Replace RGB values with HSL format
- 💄 Update all component styles to use new tokens
- 📦 @ui/theme: v2.1.0 → v3.0.0

BREAKING CHANGE: Color token values changed from RGB to HSL format
```

## Types and Emojis

- feat ✨, fix 🐛, docs 📚, style 💄, refactor ♻️, perf ⚡, test ✅, build 🔧, ci 👷, chore 🔨, revert ⏪
- Breaking: add `!` and `BREAKING CHANGE:` footer
- Scope: module or package name (monorepo: exact name or `all`)

## Issue Tracking

- When fixing issues, include them at the end of commit message body
- Format: - Fixes <ISSUE_NUMBER> (e.g., - Fixes #123 or - Fixes STL-1487)
- Add one bullet per issue

