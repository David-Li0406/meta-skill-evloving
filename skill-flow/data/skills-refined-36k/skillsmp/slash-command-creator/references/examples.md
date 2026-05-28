# Slash Command Examples

## Simple Commands

### Code Review Command
```markdown
---
description: Review code for bugs and improvements
---

Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
- Potential bugs

$ARGUMENTS
```

### Explain Command
```markdown
---
description: Explain code in simple terms
---

Explain the following code in simple, easy-to-understand terms:

$ARGUMENTS
```

## Commands with Arguments

### Single Argument (`$ARGUMENTS`)
```markdown
---
description: Fix a GitHub issue
---

Fix issue #$ARGUMENTS following our coding standards.
```

### Positional Arguments (`$1`, `$2`, etc.)
```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

## Commands with Bash Execution

Slash commands can execute shell commands before running using the exclamation-backtick syntax.

**Requirements**:
- Add allowed-tools in frontmatter to specify permitted bash commands
- Use exclamation mark followed by backtick-wrapped command in the body

**Example structure**:
- Frontmatter: `allowed-tools: Bash(git status:*), Bash(git diff:*)`
- Body: Use `!` prefix with backtick-wrapped commands like git status, git diff, etc.

See the official Claude Code documentation for detailed bash execution syntax:
https://docs.anthropic.com/en/docs/claude-code/slash-commands

## Commands with File References

Use `@` prefix to include file contents.

### Review Implementation
```markdown
---
description: Review implementation against spec
---

Review the implementation in @src/utils/helpers.js against the specification.
```

### Compare Files
```markdown
---
argument-hint: [old-file] [new-file]
description: Compare two files
---

Compare @$1 with @$2 and summarize the differences.
```

## Namespaced Commands

Commands in subdirectories appear with namespace in description.

### Frontend Component (`.claude/commands/frontend/component.md`)
```markdown
---
description: Generate a React component
---

Generate a React component with the following requirements:

$ARGUMENTS

Follow our frontend coding standards and use TypeScript.
```

### Backend API (`.claude/commands/backend/api.md`)
```markdown
---
description: Generate API endpoint
---

Generate a REST API endpoint for:

$ARGUMENTS

Include validation, error handling, and documentation.
```

## Extended Thinking Commands

Include thinking keywords to trigger extended thinking.

```markdown
---
description: Analyze architecture deeply
---

Think step by step about the architecture implications of:

$ARGUMENTS

Consider scalability, maintainability, and performance.
```
