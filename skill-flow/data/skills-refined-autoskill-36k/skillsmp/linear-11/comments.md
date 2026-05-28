# Comments

Comments enable discussion on issues. They support mentions, markdown, and time-aware formatting.

## Listing Comments

```bash
linctl comment list LIN-123 --json
linctl comment ls LIN-123 --json    # Alias
```

### List Options

| Flag | Description | Example |
|------|-------------|---------|
| `--limit`, `-l` | Max results (default 50) | `--limit 100` |
| `--sort`, `-o` | Sort order | `--sort created` |

### JSON Response Structure

```json
[
  {
    "id": "uuid",
    "body": "Comment text with **markdown** support",
    "user": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "createdAt": "2024-01-20T14:30:00Z",
    "updatedAt": "2024-01-20T14:30:00Z",
    "editedAt": null
  }
]
```

### List Examples

```bash
# All comments on an issue
linctl comment list LIN-123 --json

# Latest 5 comments
linctl comment list LIN-123 --limit 5 --json

# Comments sorted by creation (oldest first)
linctl comment list LIN-123 --sort created --json | jq 'reverse'

# Find comments by a specific user
linctl comment list LIN-123 --json | jq '.[] | select(.user.email == "john@example.com")'

# Get just comment bodies
linctl comment list LIN-123 --json | jq -r '.[].body'

# Count comments
linctl comment list LIN-123 --json | jq 'length'
```

## Creating Comments

```bash
linctl comment create LIN-123 --body "Comment text"
linctl comment add LIN-123 --body "Comment text"    # Alias
linctl comment new LIN-123 --body "Comment text"    # Alias
```

### Short Flag

```bash
linctl comment create LIN-123 -b "Comment text"
```

### Markdown Support

Comments support full markdown:

```bash
# Bold and italic
linctl comment create LIN-123 --body "This is **bold** and *italic*"

# Code blocks
linctl comment create LIN-123 --body "Fixed with:
\`\`\`javascript
const fix = true;
\`\`\`"

# Lists
linctl comment create LIN-123 --body "Changes made:
- Updated config
- Fixed tests
- Added docs"

# Links
linctl comment create LIN-123 --body "See [PR #456](https://github.com/org/repo/pull/456)"
```

### Multiline Comments

Use shell quoting for multiline:

```bash
linctl comment create LIN-123 --body "## Summary

Made the following changes:

1. Fixed the authentication bug
2. Added error handling
3. Updated tests

**Testing notes:** Run \`npm test\` to verify"
```

Or use heredoc:

```bash
linctl comment create LIN-123 --body "$(cat <<'EOF'
## Investigation Results

Found the root cause:
- The timeout was set to 5 seconds
- Network latency averages 6 seconds

**Fix:** Increased timeout to 10 seconds.
EOF
)"
```

## Mentions

Mention users with `@`:

```bash
# Mention someone
linctl comment create LIN-123 --body "@jane please review this"

# Mention multiple people
linctl comment create LIN-123 --body "@john @jane Can you both take a look?"
```

Note: Linear resolves mentions by name/email. Use the name as it appears in Linear.

## Common Comment Patterns

### Status Updates

```bash
# Starting work
linctl comment create LIN-123 --body "Starting work on this. ETA: end of day."

# Progress update
linctl comment create LIN-123 --body "Progress update:
- [x] Backend changes complete
- [ ] Frontend updates pending
- [ ] Tests needed"

# Blocked
linctl comment create LIN-123 --body "**Blocked** - waiting on API access. @admin can you help?"
```

### Code References

```bash
# Reference a commit
linctl comment create LIN-123 --body "Fixed in commit \`abc123\`"

# Reference a PR
linctl comment create LIN-123 --body "PR ready for review: https://github.com/org/repo/pull/456"

# Reference another issue
linctl comment create LIN-123 --body "Related to LIN-456. Will fix both together."
```

### Handoffs

```bash
# Reassigning
linctl comment create LIN-123 --body "@jane Taking over this one. Here's context:
- Bug occurs on mobile Safari
- Repro steps in description
- I started debugging in \`auth.js\`"

# Review request
linctl comment create LIN-123 --body "@john Ready for review. Key changes:
1. Refactored the auth flow
2. Added retry logic
3. Updated error messages"
```

### Closing Notes

```bash
# Resolution summary
linctl comment create LIN-123 --body "## Resolution

**Root cause:** Race condition in session handling

**Fix:** Added mutex lock around session operations

**Testing:**
- Unit tests added
- Verified in staging
- Monitored for 24h in production"
```

## Workflow Examples

### Add Comment When Starting Issue

```bash
# Claim and comment in one flow
linctl issue update LIN-123 --assignee me --state "In Progress"
linctl comment create LIN-123 --body "Starting work on this."
```

### Document Investigation

```bash
#!/bin/bash
ISSUE="LIN-123"

# Add investigation notes
linctl comment create $ISSUE --body "## Investigation

**Steps taken:**
1. Checked logs - found timeout errors
2. Traced to database connection pool
3. Pool was exhausted under load

**Proposed fix:** Increase pool size from 10 to 50

Will implement and test."
```

### Batch Comment Multiple Issues

```bash
#!/bin/bash
# Add the same comment to multiple issues
COMMENT="Deprioritized for Q2. Moving to backlog."

for issue in LIN-100 LIN-101 LIN-102; do
  linctl comment create $issue --body "$COMMENT"
  linctl issue update $issue --state "Backlog"
done
```

### Daily Activity Log

```bash
#!/bin/bash
# List today's comments across my issues

echo "# My Comments Today"
for issue in $(linctl issue list --assignee me --json | jq -r '.[].identifier'); do
  comments=$(linctl comment list $issue --json | jq --arg today "$(date +%Y-%m-%d)" '
    [.[] | select(.createdAt | startswith($today))]
  ')
  if [ "$(echo $comments | jq 'length')" -gt 0 ]; then
    echo "## $issue"
    echo "$comments" | jq -r '.[].body'
  fi
done
```

### Get Comment History for Report

```bash
# Export all comments on an issue
linctl comment list LIN-123 --json | jq -r '.[] | "[\(.createdAt)] \(.user.name):\n\(.body)\n"'
```
