---
name: pr-push
description: |
  Push local commits to remote, check for uncommitted changes, and create a PR with structured summary, changes list, and test plan.
---
# PR Push

## Instructions

1. **Gather Info**: `git status`, `git log origin/<branch>..HEAD --oneline`, `git remote -v`
2. **Check Uncommitted**: If exist, ask user whether to commit first
3. **Push**: `git push -u origin <current-branch>`
4. **Check Existing PR**: Run `gh pr view --json url -q .url 2>/dev/null` to check if a PR already exists for this branch
   - If PR exists: inform user and provide the PR URL, skip PR creation
   - If no PR exists: proceed to create one
5. **Analyze Diff**: Compare branch vs base (main/master/develop)
6. **Create PR**: Use `gh pr create` with structured body

## Commands Reference

```bash
# Check commits to push
git log origin/<branch>..HEAD --oneline

# Compare with base branch
git log <base>..HEAD --oneline
git diff <base>...HEAD --stat
git diff <base>...HEAD

# Push with upstream
git push -u origin <branch>

# Check if PR already exists for current branch
gh pr view --json url -q .url 2>/dev/null

# Create PR with heredoc
gh pr create --title "<type>: <subject>" --body "$(cat <<'EOF'
## Summary
...

## Changes
- ...

## Test Plan
...
EOF
)"
```

## PR Message Format

```markdown
## Summary
Brief description of what this PR accomplishes.

## Changes
- Bullet points of specific changes
- Reference actual files/functions modified
- Group related changes together

## Test Plan
How to verify the changes work correctly.
```

## PR Title Convention

| Type | Use Case |
|------|----------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `test:` | Test changes |
| `chore:` | Build/config |

## Guidelines

- Always write PR messages in **English**
- Be specific, reference actual changes from diff
- Avoid verbosity - focus on what/why
- No co-author credits or "Generated with..." tags

## Edge Cases

| Situation | Action |
|-----------|--------|
| No commits to push | Inform user |
| Push fails | Report error, suggest solutions |
| Uncommitted changes | Ask user to commit first |
| No base branch | Ask user which branch to compare |
| PR already exists | Inform user and provide PR URL, skip creation |

## Examples

### Example 1: Feature PR

**Title**: `feat(auth): add JWT token refresh mechanism`

**Body**:
```markdown
## Summary
Implement automatic JWT token refresh to prevent session expiration during active use.

## Changes
- Add `refreshToken()` method in `auth/token.go`
- Implement secure cookie storage for refresh tokens
- Add retry logic with exponential backoff
- Update auth middleware to trigger refresh

## Test Plan
1. Login and wait for token to near expiration
2. Verify automatic refresh occurs without logout
3. Check refresh token rotates correctly
```

### Example 2: Bug Fix PR

**Title**: `fix(api): handle empty response body gracefully`

**Body**:
```markdown
## Summary
Fix null pointer exception when API returns empty body instead of JSON.

## Changes
- Add nil check in `parseResponse()` before JSON unmarshal
- Return empty struct instead of error for 204 responses
- Add unit test for empty body case

## Test Plan
1. Send request that returns 204 No Content
2. Verify no panic, returns empty result
```

### Example 3: Refactor PR

**Title**: `refactor(streamer): consolidate test mocks`

**Body**:
```markdown
## Summary
Extract common mock implementations to reduce duplication across test files.

## Changes
- Move `mockGRPCStreamClient` to `mock_query.go`
- Remove 4 duplicate mock definitions
- Update all test files to use shared mock

## Test Plan
Run `make test` - all tests should pass unchanged.
```
