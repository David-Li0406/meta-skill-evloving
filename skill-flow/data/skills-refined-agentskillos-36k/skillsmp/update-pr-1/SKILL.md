---
name: update-pr
description: Update a pull request description. Use when asked to update PR description, edit PR body, or refresh PR details.
---

# Update Pull Request Description

Update an existing PR's description, working around sandbox heredoc limitations.

## Instructions

### 1. Get current PR info

```bash
# View current PR (assumes on feature branch)
gh pr view --json number,title,body

# Or specify PR number
gh pr view 123 --json number,title,body
```

### 2. Write the new body to a temp file

Use printf to avoid heredoc issues:

```bash
printf '%s\n' \
  '## Problem' \
  '' \
  'Description of the problem...' \
  '' \
  '## Solution' \
  '' \
  'Description of the solution...' \
  > /tmp/claude/pr-body.md
```

For longer content, build it incrementally:

```bash
# Start fresh
> /tmp/claude/pr-body.md

# Add sections
printf '%s\n' '## Problem' '' >> /tmp/claude/pr-body.md
printf '%s\n' 'The issue is...' '' >> /tmp/claude/pr-body.md
printf '%s\n' '## Solution' '' >> /tmp/claude/pr-body.md
printf '%s\n' 'We fixed it by...' >> /tmp/claude/pr-body.md
```

### 3. Update the PR

```bash
# Using body-file (may show GraphQL warning but still works)
gh pr edit 123 --body-file /tmp/claude/pr-body.md

# If that fails, use the API directly
gh api repos/{owner}/{repo}/pulls/123 --method PATCH \
  -f body="$(cat /tmp/claude/pr-body.md)"
```

### 4. Verify the update

```bash
gh pr view 123 --json body -q '.body' | head -20
```

### 5. Clean up

```bash
rm /tmp/claude/pr-body.md
```

## Common Issues

**GraphQL Projects (classic) warning:**
This warning appears but the update usually still succeeds. Verify with `gh pr view`.

**Heredoc fails:**
Expected in sandbox mode. Use printf approach.

**Body too long for single printf:**
Build the file incrementally with append (>>).

**Special characters:**
Use single quotes. For apostrophes: `'Don'\''t'`

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

🤖 _PR by [Claude Code](https://claude.com/claude-code)_
```

## Examples

**Quick body update:**

```bash
printf '%s\n' '## Problem' '' 'Users cannot login' '' '## Solution' '' 'Fixed auth token validation' '' '---' '🤖 _PR by [Claude Code](https://claude.com/claude-code)_' > /tmp/claude/pr-body.md
gh pr edit 123 --body-file /tmp/claude/pr-body.md
```

**Using API fallback:**

```bash
gh api repos/myorg/myrepo/pulls/123 --method PATCH \
  -f body="$(cat /tmp/claude/pr-body.md)"
```
