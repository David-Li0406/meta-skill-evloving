---
name: update-pr
description: Use this skill when you need to update the description or body of a GitHub pull request.
---

# Update Pull Request Description

This skill provides a comprehensive guide to updating an existing GitHub pull request (PR) description, ensuring that you can modify the content effectively.

## Instructions

### 1. Get the Current PR Number

If the PR number is not provided, retrieve it using the current branch name:

```bash
gh pr list --head "$(git branch --show-current)" --json number --jq '.[0].number'
```

### 2. View Current PR Information

To review the existing PR body, use:

```bash
gh pr view <pr-number> --json body -q '.body'
```

### 3. Write the New Body to a Temporary File

Use `printf` to avoid heredoc issues:

```bash
printf '%s\n' \
  '## Problem' \
  '' \
  'Description of the problem...' \
  '' \
  '## Solution' \
  '' \
  'Description of the solution...' \
  > /tmp/pr-body.md
```

For longer content, build it incrementally:

```bash
# Start fresh
> /tmp/pr-body.md

# Add sections
printf '%s\n' '## Problem' '' >> /tmp/pr-body.md
printf '%s\n' 'The issue is...' '' >> /tmp/pr-body.md
printf '%s\n' '## Solution' '' >> /tmp/pr-body.md
printf '%s\n' 'We fixed it by...' >> /tmp/pr-body.md
```

### 4. Update the PR

You can update the PR body using the body file:

```bash
gh pr edit <pr-number> --body-file /tmp/pr-body.md
```

If that fails, use the API directly:

```bash
gh api -X PATCH /repos/{owner}/{repo}/pulls/<pr-number> -f body="$(cat /tmp/pr-body.md)"
```

### 5. Verify the Update

Check the updated PR body to ensure the changes were applied:

```bash
gh pr view <pr-number> --json body -q '.body' | head -20
```

### 6. Clean Up

Remove the temporary file used for the PR body:

```bash
rm /tmp/pr-body.md
```

## Common Issues

- **GraphQL Projects Warning:** This warning may appear but the update usually still succeeds. Verify with `gh pr view`.
- **Heredoc Fails:** Use the `printf` approach to avoid issues in sandbox mode.
- **Body Too Long for Single `printf`:** Build the file incrementally with append (`>>`).
- **Special Characters:** Use single quotes for strings. For apostrophes, use `'Don'\''t'`.

## PR Body Structure

Follow this template for consistency:

```markdown
## Problem

[What issue exists?]

## Solution

[High-level approach]

### Key Design Decisions

**1. [Decision]**
[Explanation]

## Files Changed

| File           | Change      |
| -------------- | ----------- |
| `path/file.ts` | Description |

## Test Plan

- [ ] Test item

---

🤖 _PR by [Your Name](https://your-link.com)_
```

## Examples

**Quick Body Update:**

```bash
printf '%s\n' '## Problem' '' 'Users cannot login' '' '## Solution' '' 'Fixed auth token validation' '' '---' '🤖 _PR by [Your Name](https://your-link.com)_'
```