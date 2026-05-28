# Comment Commands

Reference for managing comments on Jira issues using `jira-cli`.

## Getting Help

```bash
jira issue comment add --help
```

## Add Comment

```bash
jira issue comment add [ISSUE-KEY] [BODY]
```

### Options

| Flag                | Description                               |
| ------------------- | ----------------------------------------- |
| `--template <path>` | Load comment from template file           |
| `--internal`        | Make comment internal (Service Desk only) |

### Examples

```bash
# Interactive comment (opens editor)
jira issue comment add
jira issue comment add PROJ-123

# Add comment directly
jira issue comment add PROJ-123 "This is my comment"

# Multiline comment (use quotes)
jira issue comment add PROJ-123 "Line 1
Line 2
Line 3"

# Internal comment (for Service Desk projects)
jira issue comment add PROJ-123 "Internal note for team" --internal

# Comment from file
jira issue comment add PROJ-123 --template /path/to/comment.md

# Comment from stdin
echo "Comment from pipeline" | jira issue comment add PROJ-123

# Comment with markdown formatting
jira issue comment add PROJ-123 "## Update

- Fixed the login issue
- Added unit tests
- Ready for review

See PR #456 for details."
```

## Comment Formatting

Comments support both GitHub-flavored and Jira-flavored markdown.

### Supported Markdown

| Syntax        | Result        |
| ------------- | ------------- |
| `**bold**`    | **bold**      |
| `*italic*`    | _italic_      |
| `` `code` ``  | `code`        |
| `[text](url)` | link          |
| `# Heading`   | heading       |
| `- item`      | bullet list   |
| `1. item`     | numbered list |
| ` ``` `       | code block    |

### Example Formatted Comment

```bash
jira issue comment add PROJ-123 "## Status Update

**Progress:**
- [x] Backend implementation complete
- [x] Unit tests added
- [ ] Integration tests pending

**Notes:**
The API endpoint is now available at \`/api/v2/users\`.

See [PR #456](https://github.com/org/repo/pull/456) for code changes."
```

## Comment During Transitions

You can add comments while transitioning issues:

```bash
# Add comment when moving to In Progress
jira issue move PROJ-123 "In Progress" --comment "Starting work on this"

# Add comment when closing
jira issue move PROJ-123 Done -RFixed --comment "Completed in PR #456"
```

## Common Use Cases

### Status Update

```bash
jira issue comment add PROJ-123 "## Progress Update

Completed initial implementation. Moving to code review.

**Changes:**
- Added new endpoint
- Updated database schema
- Added unit tests

**Next steps:**
- Code review
- Integration testing"
```

### Request Information

```bash
jira issue comment add PROJ-123 "Could you provide more details about the expected behavior?

Specifically:
1. What should happen when the input is empty?
2. Should we log the error or fail silently?"
```

### Block Notification

```bash
jira issue comment add PROJ-123 "**Blocked**

Waiting on API access from external team. ETA unknown.

Contacted: john@external.com on $(date +%Y-%m-%d)"
```

### Code Reference

```bash
jira issue comment add PROJ-123 "Fixed in commit abc123

\`\`\`diff
- old_function()
+ new_function()
\`\`\`

The issue was caused by incorrect parameter ordering."
```

### Handoff Comment

```bash
jira issue comment add PROJ-123 "Handing this off to @jane.doe

**Context:**
- Root cause identified in auth module
- Fix approach discussed in standup
- Related to PROJ-100

**Files to check:**
- src/auth/login.py
- tests/auth/test_login.py"
```

## Best Practices

1. **Be concise** - Keep comments focused and actionable
2. **Use formatting** - Headers and lists improve readability
3. **Include context** - Reference PRs, commits, or related issues
4. **Mention users** - Use @username for notifications
5. **Use internal comments** - For sensitive internal discussions (Service Desk)
6. **Confirm before posting** - Review comment content with user

## Scripting Patterns

### Add Comment from Script Output

```bash
# Add test results as comment
test_output=$(npm test 2>&1)
jira issue comment add PROJ-123 "## Test Results

\`\`\`
${test_output}
\`\`\`"
```

### Bulk Comment

```bash
# Add comment to multiple issues
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue comment add "$issue" "Sprint planning: Moved to Sprint 42"
done
```

### Template-Based Comments

```bash
# Create a template file
cat > /tmp/comment-template.md << 'EOF'
## Investigation Complete

**Root Cause:**
**Fix:**
**Testing:**
**Rollback Plan:**
EOF

# Use template
jira issue comment add PROJ-123 --template /tmp/comment-template.md
```
