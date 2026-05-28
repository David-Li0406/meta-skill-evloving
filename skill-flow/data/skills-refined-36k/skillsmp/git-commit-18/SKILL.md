---
name: git-commit
description: Standards and formatting for creating git commit messages. **REQUIRED** Invoke this skill BEFORE creating any git commit to ensure proper conventional commit format with type prefixes and descriptions. Use when committing changes or when user asks about commit message format.
---

# Git Commit

Create properly formatted git commit messages following conventional commit standards.

## Commit Message Format

Use conventional commit format: `{type}: {description}`

### Valid Types

- **feat** - New feature or functionality
- **fix** - Bug fix
- **chore** - Maintenance tasks (dependencies, config, etc.)
- **docs** - Documentation changes
- **style** - Code style/formatting (no logic changes)
- **refactor** - Code restructuring (no behavior changes)
- **test** - Adding or updating tests
- **perf** - Performance improvements
- **ci** - CI/CD pipeline changes
- **build** - Build system or external dependencies

### Examples

```
feat: add new authentication endpoint
fix: resolve null pointer exception in API handler
chore: update dependencies
docs: update README with deployment instructions
refactor: extract validation logic into separate service
test: add unit tests for user service
perf: optimize database query performance
ci: add automated deployment workflow
```

## Best Practices

- Keep descriptions concise and descriptive
- Use imperative mood ("add" not "added" or "adds")
- Start with lowercase after the colon
- No period at the end
- Focus on what changed, not why (details go in commit body if needed)
