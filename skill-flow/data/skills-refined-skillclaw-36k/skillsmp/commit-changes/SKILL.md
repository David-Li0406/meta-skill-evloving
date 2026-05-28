---
name: commit-changes
description: |
  Create clear, informative, and well-structured Git commit messages following best practices and conventional commit standards.
---
# Commit Changes

## Instructions

1. **Analyze Changes**: Run `git diff --staged`, `git diff`, and `git status`
2. **Stage All**: Use `git add -A` if needed
3. **Understand Context**: What changed, why, type, scope, patterns
4. **Check Branch**: If on main/master, create descriptive branch first
5. **Generate Message**: Subject ≤72 chars, imperative, conventional type
6. **Execute**: `git commit -m "<message>"`

## Commit Message Format

```
<type>(<scope>): <subject>

<body>
```

### Types

| Type | Use Case |
|------|----------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |

### Rules

- Imperative mood ("Add feature" not "Added feature")
- No trailing period
- Subject ≤72 characters
- Body explains **what/why**, not how
- No co-author credits or "Generated with..." tags

## Quality Standards

- Meaningful to someone reading git log months later
- Avoid generic: "fix bug", "update code"
- Group related changes conceptually
- Flag if changes too diverse for single message

## Edge Cases

| Situation | Action |
|-----------|--------|
| No changes | Inform user nothing to commit |
| Incomplete changes | Flag observation to user |
| On main/master | Create feature branch first |
| Too diverse | Note to user, suggest splitting |

## Examples

### Example 1: Feature Commit

```
feat(auth): add JWT token refresh mechanism

- Implement automatic token refresh before expiration
- Add refresh token storage in secure cookie
- Include retry logic for failed refresh attempts
```

### Example 2: Bug Fix Commit

```
fix(api): prevent null pointer on empty response

Handle case where API returns empty body instead of
throwing unhandled exception in response parser.
```

### Example 3: Refactor Commit

```
refactor(streamer): extract common mock to shared helper

- Move mockGRPCStreamClient to mock_query.go
- Consolidate 4 duplicate mock implementations
- Reduce test file coupling
```

### Example 4: Multi-scope Commit

```
test(streamer): consolidate redundant tests

- Remove TestRemoteStream_Success (duplicate of Recv_EventDelivery)
- Merge Close_Idempotent into TestRemoteStream_Close
- Delete tests with no real assertions
```
