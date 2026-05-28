---
name: issue
description: This skill should be used when the user asks to "create an issue", "write an issue", "add an issue", "log an issue", "report a bug", "document a problem", or wants to track tasks, bugs, or feature requests as GitHub issues.
---

# Issue Writing Guidelines

Create and manage issues using GitHub Issues via the `gh` CLI.

## Workflow

1. Gather information about the issue from the user or context
2. Write the issue body to a temporary file (`/tmp/issue-body.md`)
3. Create the issue using `gh issue create --title "..." --body-file /tmp/issue-body.md`
4. Return the created issue URL to the user

## Issue Format

Use GitHub-flavored Markdown with the following structure:

```markdown
## Description

<Detailed description of the issue, bug, or feature request>

## Context

<Any relevant context, steps to reproduce, or background information>

## Related Files

- `path/to/file1`
- `path/to/file2`
```

## Creating Issues

Always write the body to a temporary file first to avoid shell escaping issues:

```bash
# Write body to tmp file (using Write tool)
# Then create issue:
gh issue create --title "Issue title" --body-file /tmp/issue-body.md
```

### With Labels

```bash
gh issue create --title "Bug: Parser crash" --body-file /tmp/issue-body.md --label bug
```

### With Assignees

```bash
gh issue create --title "Feature request" --body-file /tmp/issue-body.md --assignee @me
```

## Managing Issues

### List Issues

```bash
gh issue list
gh issue list --state open
gh issue list --label bug
```

### View Issue

```bash
gh issue view 123
```

### Close Issue

```bash
gh issue close 123
gh issue close 123 --comment "Fixed in commit abc123"
```

### Add Comment

```bash
gh issue comment 123 --body "Progress update: ..."
```

## Writing Good Issue Descriptions

- Be specific about the problem or feature
- Include steps to reproduce for bugs
- Mention expected vs actual behavior
- Reference related files or code when relevant
- Keep descriptions focused and actionable
- Use code blocks for error messages and code snippets

## Example Issue

**Title:** Parser fails on empty input

**Body:**
```markdown
## Description

The parser crashes with an index out of bounds error when given an empty string as input.

## Context

- File: `Ziku/Parser.lean`
- Error occurs in the `parse` function
- Expected: Return an empty AST or appropriate error
- Actual: Crashes with uncaught exception

## Steps to Reproduce

1. Run `ziku parse ""`
2. Observe the crash

## Related Files

- `Ziku/Parser.lean`
- `Ziku/Lexer.lean`
```
