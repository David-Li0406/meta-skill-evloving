---
name: update-pr
description: Use this skill when you need to update, edit, or modify a GitHub pull request description or body.
---

# Update GitHub Pull Request Body

This skill provides a workflow for updating the body of an existing GitHub pull request (PR), accommodating various methods to ensure successful updates.

## Instructions

### 1. Get Current PR Information

If the PR number is not provided, retrieve it based on the current branch:

```bash
gh pr list --head "$(git branch --show-current)" --json number --jq '.[0].number'
```

To view the current PR body:

```bash
gh pr view <pr-number> --json body -q '.body'
```

### 2. Write the New Body to a Temporary File

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
> /tmp/pr-body.md
printf '%s\n' '## Problem' '' >> /tmp/pr-body.md
printf '%s\n' 'The issue is...' '' >> /tmp/pr-body.md
printf '%s\n' '## Solution' '' >> /tmp/pr-body.md
printf '%s\n' 'We fixed it by...' >> /tmp/pr-body.md
```

### 3. Update the PR

You can update the PR body using the following methods:

Using the body file:

```bash
gh pr edit <pr-number> --body-file /tmp/pr-body.md
```

If that fails, use the API directly:

```bash
gh api -X PATCH /repos/{owner}/{repo}/pulls/<pr-number> -f body="$(cat /tmp/pr-body.md)"
```

### 4. Verify the Update

Check the updated PR body:

```bash
gh pr view <pr-number> --json body -q '.body' | head -20
```

### 5. Clean Up

Remove the temporary file:

```bash
rm /tmp/pr-body.md
```

## Common Issues

- **GraphQL Projects Warning:** This warning may appear but the update usually succeeds. Verify with `gh pr view`.
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

### Key design decisions

**1. [Decision]**
[Explanation]

## Files changed

| File           | Change      |
| -------------- | ----------- |
| `path/file.ts` | Description |

## Test plan

- [ ] Test item

---

🤖 _PR by [Your Name](https://yourprofile.com)_
```

## Examples

**Quick Body Update:**

```bash
printf '%s\n' '## Problem' '' 'Users cannot login' '' '## Solution' '' 'Fixed auth token validation' '' '---' '🤖 _PR by [Your Name](https://yourprofile.com)_' > /tmp/pr-body.md
gh pr edit <pr-number> --body-file /tmp/pr-body.md
```

**Using API Fallback:**

```bash
gh api -X PATCH /repos/{owner}/{repo}/pulls/<pr-number> -f body="$(cat /tmp/pr-body.md)"
```

**Append to Existing Body:**

```bash
CURRENT_BODY=$(gh pr view <pr-number> --json body -q '.body')
gh api -X PATCH /repos/{owner}/{repo}/pulls/<pr-number> -f body="${CURRENT_BODY}

## Additional Notes
New content appended here."
```