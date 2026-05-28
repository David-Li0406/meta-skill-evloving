# Pull Request Review Workflows

Complete workflows for reviewing pull requests with Claude Code using the GitHub CLI.

## Pre-Review Setup

### Verify gh CLI

```bash
gh auth status    # Check authentication
gh auth login     # Login if needed
```

### Quick PR Overview

```bash
# View PR details
gh pr view 123

# View PR in browser
gh pr view 123 --web
```

## Standard PR Review Workflow

### Step 1: Gather PR Information

Run in parallel:

```bash
gh pr view 123                    # PR description and metadata
gh pr diff 123                    # Full diff
gh pr checks 123                  # CI status
gh api repos/{owner}/{repo}/pulls/123/commits  # Commit list
```

### Step 2: Checkout and Explore

```bash
gh pr checkout 123                # Switch to PR branch
```

### Step 3: Request Review from Claude

```
Review PR #123

Context:
gh pr view 123
gh pr diff 123

Focus areas:
- Does implementation match description?
- Are changes complete?
- Any obvious bugs?
- Test coverage adequate?
- Documentation updated?
```

### Step 4: Leave Review via gh CLI

```bash
# Approve
gh pr review 123 --approve

# Approve with comment
gh pr review 123 --approve --body "LGTM! Nice work on the error handling."

# Request changes
gh pr review 123 --request-changes --body "$(cat <<'EOF'
## Changes Requested

### Critical
- Line 42: SQL injection vulnerability in user input

### Suggestions
- Consider using a transaction for lines 55-60
- Missing test for error case

EOF
)"

# Comment only (no approval/rejection)
gh pr review 123 --comment --body "Some questions about the approach..."
```

## Review by PR Type

### Feature PR Review

```
Review feature PR #123

gh pr view 123
gh pr diff 123

Evaluate:
1. Feature Completeness
   - All acceptance criteria met?
   - Edge cases handled?
   - Error states covered?

2. Implementation Quality
   - Clean code patterns?
   - Appropriate abstractions?
   - No code duplication?

3. Testing
   - Unit tests for new code?
   - Integration tests for flows?
   - Edge case coverage?

4. Documentation
   - README updated if needed?
   - API docs current?
   - Code comments helpful?

5. Breaking Changes
   - Backward compatible?
   - Migration path if not?
```

### Bug Fix PR Review

```
Review bug fix PR #123

gh pr view 123
gh pr diff 123

Verify:
1. Bug Fix
   - Does it fix the described issue?
   - Root cause addressed (not just symptom)?
   - No regression introduced?

2. Reproduction
   - Can the bug be reproduced?
   - Is there a regression test?

3. Impact
   - Minimal change scope?
   - Side effects identified?
   - Related areas checked?

4. Testing
   - Test reproduces the bug?
   - Test passes with fix?
   - Edge cases tested?
```

### Refactor PR Review

```
Review refactor PR #123

gh pr view 123
gh pr diff 123

Evaluate:
1. Behavior Preservation
   - No functional changes?
   - Tests still pass?
   - Output identical?

2. Improvement
   - Code clearer?
   - Performance better?
   - Maintainability improved?

3. Scope
   - Focused refactor?
   - No mixed concerns?
   - Incremental steps?

4. Risk
   - High-traffic areas affected?
   - Rollback plan?
```

### Dependency Update PR Review

```
Review dependency update PR #123

gh pr view 123
gh pr diff 123

Check:
1. Security
   - Fixes vulnerabilities?
   - No new CVEs introduced?

2. Compatibility
   - Breaking changes in dep?
   - Migration steps followed?

3. Testing
   - Full test suite passes?
   - Manual testing done?

4. Changelog
   - Reviewed dep changelog?
   - Notable changes documented?
```

## PR Review Comment Templates

### Line-Specific Comments via API

```bash
# Add comment on specific line
gh api repos/{owner}/{repo}/pulls/123/comments \
  -f body="This could cause a null pointer if user is undefined" \
  -f commit_id="$(gh pr view 123 --json headRefOid -q .headRefOid)" \
  -f path="src/api/users.ts" \
  -F line=42
```

### Review Comment Templates

**Security Issue:**
```markdown
**Security:** Potential vulnerability

The user input on line 42 is not sanitized before use in the query.

```typescript
// Current - vulnerable
const result = await db.query(`SELECT * FROM users WHERE id = ${userId}`);

// Suggested - safe
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```
```

**Performance Concern:**
```markdown
**Performance:** N+1 query pattern

Lines 35-45 query the database in a loop. Consider:

```typescript
// Current - N+1
for (const id of userIds) {
  const user = await db.getUser(id);
}

// Suggested - batch
const users = await db.getUsersByIds(userIds);
```
```

**Code Quality:**
```markdown
**Suggestion:** Simplify conditional

Lines 22-28 could be simplified:

```typescript
// Current
if (condition) {
  return true;
} else {
  return false;
}

// Suggested
return condition;
```
```

**Question:**
```markdown
**Question:** Rationale for approach

Why was X approach chosen over Y? I'd expect Y to be more performant here.
```

## Batch PR Review

Review multiple PRs efficiently:

```bash
# List all open PRs
gh pr list

# View multiple PR diffs
for pr in 123 124 125; do
  echo "=== PR #$pr ==="
  gh pr diff $pr
done
```

Then:

```
Review PRs #123, #124, #125 in batch

For each PR, provide:
- Quick summary
- Key concerns (if any)
- Recommendation (approve/changes/discuss)

Prioritize critical issues.
```

## Draft PR Review

```
Review draft PR #123

gh pr view 123
gh pr diff 123

This is early feedback, so:
- Focus on architectural/design issues
- Don't nitpick style yet
- Identify potential blockers early
- Suggest direction if off-track

Provide feedback as:
## Direction
[On track / Needs adjustment / Major concerns]

## Early Feedback
[Suggestions for the draft stage]

## Questions
[Clarifications needed before full review]
```

## Reviewing Your Own PR

```
Self-review my changes before creating PR

git diff main...HEAD

Check:
1. No debugging code left
2. No console.log statements
3. No commented-out code
4. Tests added/updated
5. Documentation updated
6. Commit messages clean
7. No unrelated changes

List anything I should fix before creating the PR.
```

## PR Description Generation

When creating PRs, generate descriptions:

```
Generate PR description for my changes

git log main..HEAD --oneline
git diff main...HEAD

Create a PR description with:
- Summary (what and why)
- Changes list
- Test plan
- Breaking changes (if any)
- Related issues

Format for gh pr create command.
```

Output:

```bash
gh pr create --title "feat(auth): add OAuth2 support" --body "$(cat <<'EOF'
## Summary
Add OAuth2 authentication flow supporting Google and GitHub providers.

## Changes
- Add OAuth2 configuration and routes
- Implement token exchange flow
- Add provider-specific adapters
- Update user model for OAuth users

## Test plan
- [ ] Google OAuth flow works end-to-end
- [ ] GitHub OAuth flow works end-to-end
- [ ] Token refresh works correctly
- [ ] Logout clears OAuth session

## Breaking changes
None - existing session auth still works.

## Related
Closes #456
EOF
)"
```

## Addressing Review Feedback

### View Review Comments

```bash
# Get all review comments
gh api repos/{owner}/{repo}/pulls/123/comments

# Get review summaries
gh api repos/{owner}/{repo}/pulls/123/reviews
```

### Batch Address Feedback

```
Address review feedback on PR #123

Review comments:
[paste or fetch comments]

For each comment:
1. Acknowledge the feedback
2. Make the fix if agreed
3. Explain if disagreeing
4. Mark as resolved
```

### Commit Message for Fixes

```bash
git commit -m "$(cat <<'EOF'
fix: address review feedback

- Fix SQL injection vulnerability (reviewer: security concern)
- Add null check for user object
- Simplify conditional logic
- Add missing test case
EOF
)"
```

## CI Integration

### Check CI Status

```bash
gh pr checks 123              # View status
gh pr checks 123 --watch      # Watch until complete
```

### Wait for CI Before Review

```
Wait for CI to pass on PR #123, then review.

gh pr checks 123 --watch

Once green, perform full review.
If failing, identify the failure first.
```

## Merge Workflows

### Standard Merge

```bash
gh pr merge 123 --merge --delete-branch
```

### Squash Merge (Clean History)

```bash
gh pr merge 123 --squash --delete-branch
```

### Rebase Merge (Linear History)

```bash
gh pr merge 123 --rebase --delete-branch
```

### Auto-Merge When Ready

```bash
gh pr merge 123 --auto --squash
```

## PR Review Checklist

Before approving any PR:

- [ ] PR description clear and complete
- [ ] All commits relevant to the change
- [ ] CI checks passing
- [ ] Code compiles without warnings
- [ ] Tests adequate and passing
- [ ] No security vulnerabilities
- [ ] No obvious performance issues
- [ ] Error handling appropriate
- [ ] Documentation updated
- [ ] No unrelated changes included
- [ ] Follows project conventions

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not authenticated" | `gh auth login` |
| "PR not found" | Check repo and PR number |
| "Cannot review own PR" | Some repos restrict this |
| "Review dismissed" | New commits pushed, re-review |
| "Merge conflicts" | Ask author to resolve |
| "Checks failing" | Review failures before code |
