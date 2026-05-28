---
name: git-commit-management
description: Use this skill to create clear, informative, and well-structured Git commit messages following best practices and conventional commit standards.
---

# Commit Management Workflow

## Instructions

1. **Analyze Changes**: Review changes using:
   ```bash
   git status
   git diff --staged
   git diff
   ```

2. **Group Related Changes**: Organize changes into logical commits.

3. **Stage Files**: Stage files for commit:
   ```bash
   git add <files>
   # Or for all changes
   git add -A
   ```

4. **Check Branch**: Ensure you are not on the main/master branch; create a descriptive branch if necessary.

5. **Generate Commit Message**: Follow the conventional commit format:
   ```
   <type>(<scope>): <subject>

   [optional body]
   ```

6. **Execute Commit**: Create the commit:
   ```bash
   git commit -m "<message>"
   ```

## Conventional Commit Format

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no feature change |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |
| `security` | Security improvements |

### Scopes (optional)

- `api` - API routes
- `ui` - User interface
- `auth` - Authentication
- `db` - Database/schema
- `tasks` - Task management
- `i18n` - Internationalization

## Commit Message Guidelines

- Use imperative mood (e.g., "Add feature" not "Added feature").
- Keep the subject ≤72 characters.
- Write descriptive but concise messages.
- Include a body that explains **what/why**, not how.
- Reference issues when applicable (e.g., `Fixes #123`).
- Always include Co-Authored-By for AI assistance if applicable.

## Pre-Commit Checklist

- [ ] Changes are logically grouped.
- [ ] No unrelated changes included.
- [ ] No debug code left in.
- [ ] No secrets or PII.
- [ ] Commit message follows convention.

## Files to Never Commit

- `.env.local` (secrets)
- `node_modules/`
- `.next/`
- `generated/prisma/`
- `*.log`
- `.DS_Store`

## Branch Naming

Use descriptive branch names:
```
feature/add-task-completion
fix/missing-auth-check
refactor/split-tasklist-service
chore/update-dependencies
```

## Creating Pull Requests

After commits are ready, push and create a pull request:
```bash
git push -u origin <branch-name>
gh pr create --title "<type>: <description>" --body "..."
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| No changes | Inform user nothing to commit. |
| Incomplete changes | Flag observation to user. |
| Too diverse changes | Suggest splitting into multiple commits. |

## Examples

### Feature Commit
```
feat(auth): add JWT token refresh mechanism

- Implement automatic token refresh before expiration
- Add refresh token storage in secure cookie
```

### Bug Fix Commit
```
fix(api): prevent null pointer on empty response

Handle case where API returns empty body instead of
throwing unhandled exception in response parser.
```

### Refactor Commit
```
refactor(streamer): extract common mock to shared helper

- Move mockGRPCStreamClient to mock_query.go
- Consolidate duplicate mock implementations
```

### Multi-scope Commit
```
test(streamer): consolidate redundant tests

- Remove duplicate tests
- Merge similar test cases
```