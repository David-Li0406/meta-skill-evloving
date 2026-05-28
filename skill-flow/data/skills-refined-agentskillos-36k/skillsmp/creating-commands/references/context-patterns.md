---
title: Context Gathering Patterns
description: Bash command patterns for gathering contextual information that commands need to execute effectively. Includes git context, project structure, file references, and dynamic discovery patterns.
keywords: context gathering, git context, project context, bash patterns, file references, dynamic discovery
file-type: reference
skill: creating-commands
---

# Context Gathering Patterns

Context gathering provides information Claude needs to execute the command effectively. Use these patterns in your command's `## Context` section.

## Git Context

```markdown
- Recent commits: !`git log --oneline -10`
- Current diff (staged): !`git diff --cached`
- Current diff (all): !`git diff HEAD`
- Branch info: !`git branch -vv`
- Remote status: !`git status -sb`
```

## Project Context

```markdown
- Package.json: !`cat package.json 2>/dev/null || echo "not found"`
- Dependencies: !`npm list --depth=0`
- Project structure: !`tree -L 2 -I 'node_modules|dist|build'`
- Available scripts: !`npm run 2>&1 | grep -A 100 "available via"`
```

## Code Context with File References

Use `@` syntax to include file contents:

```markdown
- Implementation: @src/main.js
- Tests: @tests/main.test.js
- Configuration: @.eslintrc.json
- Documentation: @README.md
```

## Dynamic File Discovery

```markdown
- Modified files: !`git diff --name-only HEAD`
- Matching files: !`git ls-files '$ARGUMENTS'`
- Recent changes: !`git diff HEAD -- $ARGUMENTS`
```

## Usage in Commands

Copy these patterns into your command's `## Context` section. Select only the context needed for your command to execute effectively.

**Example:**
```markdown
## Context

- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Recent commits: !`git log --oneline -5`
- Implementation: @src/feature.js
```

## Best Practices

- **Be selective**: Only gather context that's actually needed
- **Be efficient**: Use head/tail to limit large outputs
- **Use @ for files**: Direct file references are more efficient than cat commands
- **Combine commands**: Use pipes to filter and format output appropriately
