---
name: open-pull-request
description: Drafts and submits pull requests via gh CLI. Use when opening PRs, writing PR descriptions, or submitting code for review.
---

# Open Pull Request

Draft a PR title and description, confirm with user, then submit via `gh pr create`.

## Workflow

- [ ] Ensure changes are committed
- [ ] Gather PR details from user
- [ ] Draft title and description
- [ ] Confirm with user
- [ ] Submit PR

## Step 1: Check for Uncommitted Changes

```bash
git status --porcelain
```

If there are uncommitted changes, use the **commit** skill to create logical commits first.

## Step 2: Gather Details

If not already clear from context, ask the user:

1. **Target branch** - Where should this merge? (e.g., `main`, `develop`)
2. **Fixes issue** - Does this close an issue? (e.g., "Fixes #123")
3. **Related issues** - Other relevant issues to reference
4. **Validation performed** - How was this tested?
5. **Pipeline links** - Links to CI/test runs if applicable

## Step 3: Draft Title and Description

### Writing a Good Title

Follow the same rules as commit messages:

- **Imperative mood**: "Add feature" not "Added feature"
- **50 characters or less** (GitHub truncates at 72)
- **Capitalize first word**
- **No trailing period**
- **Specific**: "Fix null pointer in UserService.validate" not "Fix bug"

The title should complete: "If merged, this PR will **___**"

✅ Good titles:
- "Add rate limiting to API endpoints"
- "Fix race condition in cache invalidation"
- "Refactor authentication to use JWT"

❌ Bad titles:
- "Fix bug" (vague)
- "Updates" (meaningless)
- "WIP" (not ready for PR)

### Writing a Good Description

A PR description is a permanent record. It must communicate:
1. **What** change is being made
2. **Why** the change is needed

**Minimum requirements:**
- Background/motivation OR linked issue
- Succinct description of changes

#### Template

```markdown
## Summary
[One paragraph: what does this PR do and why?]

## Changes
- [Bullet list of key changes]

## Testing
- [How was this validated?]
- [Link to CI runs if applicable]

## Related
- Fixes #123
- Related to #456
```

#### Examples

**Feature PR:**
```markdown
## Summary
Add rate limiting to prevent API abuse. Clients are currently able to
make unlimited requests, causing service degradation during peak load.

## Changes
- Add token bucket rate limiter middleware
- Configure default limit of 100 req/min per client
- Add rate limit headers to responses

## Testing
- Unit tests for rate limiter logic
- Load tested with 1000 concurrent clients
- [CI run](https://example.com/ci/12345)

Fixes #423
```

**Bug fix PR:**
```markdown
## Summary
Fix null pointer exception when user profile is missing optional fields.

The ProfileService.validate() method assumed all fields were present,
but email and phone are optional per the API spec.

## Changes
- Add null checks in ProfileService.validate()
- Add test coverage for optional field combinations

## Testing
- Added unit tests for edge cases
- Manually verified with production-like data

Fixes #891
```

**Small PR (minimal description is fine):**
```markdown
Fix typo in installation docs.

The command was `npm instal` instead of `npm install`.
```

## Step 4: Confirm with User

Present the draft title and description. Ask the user to confirm or request changes before submitting.

## Step 5: Submit PR

```bash
gh pr create \
  --title "Your title here" \
  --body "Your description here" \
  --base main
```

Useful flags:
- `--base <branch>` - Target branch
- `--draft` - Open as draft PR
- `--assignee @me` - Assign to yourself
- `--reviewer <user>` - Request review
- `--label <label>` - Add labels

After creation, display the PR URL to the user.

## Quick Reference

| Element | Guideline |
|---------|-----------|
| Title length | ≤50 chars (72 max) |
| Title mood | Imperative ("Add" not "Added") |
| Description minimum | Background + changes summary |
| Issue linking | "Fixes #123" to auto-close |
