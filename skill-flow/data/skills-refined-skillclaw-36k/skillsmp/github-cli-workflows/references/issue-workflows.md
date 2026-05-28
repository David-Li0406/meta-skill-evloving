# Issue Workflows

Comprehensive patterns for managing issues using GitHub CLI.

## Quick Reference

```bash
gh issue create         # Create new issue (interactive or with flags)
gh issue list           # List issues with filters
gh issue view [number]  # View issue details
gh issue close [number] # Close issue
gh issue reopen [number]# Reopen closed issue
gh issue comment [number] # Add comment
gh issue edit [number]  # Edit issue properties
gh issue delete [number]# Delete issue
gh issue pin [number]   # Pin issue to repository
gh issue unpin [number] # Unpin issue
gh issue transfer [number] # Transfer to another repo
```

**Remember:** Use `gh issue <subcommand> --help` for detailed options and examples.

## Creating Issues

### Basic Issue Creation

**Interactive mode:**
```bash
gh issue create
```

**Non-interactive with flags:**
```bash
gh issue create \
  --title "Bug: Login fails with SSO" \
  --body "Users cannot log in when SSO is enabled. Error: 'Invalid state parameter'"
```

### Advanced Issue Creation

**With labels and assignees:**
```bash
gh issue create \
  --title "Feature: Add dark mode" \
  --body "Implement dark mode toggle in settings" \
  --label enhancement,ui \
  --assignee @me
```

**From template:**
```bash
gh issue create --template bug_report.md
```

**With milestone and project:**
```bash
gh issue create \
  --title "Update documentation" \
  --body "..." \
  --milestone "v2.0" \
  --project "Documentation Sprint"
```

**Multiline body with heredoc:**
```bash
gh issue create --title "Bug: Memory leak in worker" --body "$(cat << 'EOF'
## Description
Memory usage grows unbounded when processing large files.

## Steps to Reproduce
1. Upload file >100MB
2. Monitor memory usage
3. Observe continuous growth

## Expected Behavior
Memory should stabilize after processing.

## Environment
- Version: 1.2.3
- OS: Ubuntu 22.04
- Node: 18.16.0
EOF
)"
```

### Creating Issues with JSON Output

```bash
# Get issue number and URL
ISSUE=$(gh issue create \
  --title "Bug: Crash on startup" \
  --body "..." \
  --json number,url)

ISSUE_NUM=$(echo "$ISSUE" | jq -r '.number')
ISSUE_URL=$(echo "$ISSUE" | jq -r '.url')

echo "Created issue #$ISSUE_NUM: $ISSUE_URL"
```

## Listing and Filtering Issues

### Basic Listing

```bash
gh issue list                 # Open issues in current repo
gh issue list --state all     # All issues (open and closed)
gh issue list --state closed  # Only closed issues
```

### Filtering Issues

**By assignee:**
```bash
gh issue list --assignee username
gh issue list --assignee @me
gh issue list --assignee ""   # Unassigned issues
```

**By author:**
```bash
gh issue list --author username
gh issue list --author @me
```

**By label:**
```bash
gh issue list --label bug
gh issue list --label "priority-high,bug"
gh issue list --label bug --label enhancement  # Issues with BOTH labels
```

**By milestone:**
```bash
gh issue list --milestone "v2.0"
gh issue list --milestone ""  # Issues without milestone
```

**By search query:**
```bash
gh issue list --search "in:title login"
gh issue list --search "is:open author:username"
gh issue list --search "label:bug created:>2024-01-01"
```

### Listing with JSON

**Get structured data:**
```bash
gh issue list \
  --json number,title,author,state,labels,createdAt,updatedAt \
  --limit 100
```

**Filter and process:**
```bash
# Get issue numbers for specific label
gh issue list --json number,labels \
  --jq '.[] | select(.labels[].name == "needs-triage") | .number'

# Find stale issues (not updated in 30 days)
gh issue list --json number,title,updatedAt \
  --jq '.[] | select(.updatedAt < (now - 2592000 | todate))'

# Count issues by label
gh issue list --json labels --jq '[.[].labels[].name] | group_by(.) | map({label: .[0], count: length})'
```

## Viewing Issue Details

### Basic View

```bash
gh issue view 456              # View in terminal
gh issue view 456 --web        # Open in browser
```

### Detailed Information

```bash
# View with comments
gh issue view 456 --comments

# View with JSON output
gh issue view 456 --json title,body,author,state,labels,assignees,comments

# Get specific fields
gh issue view 456 --json title --jq '.title'
gh issue view 456 --json labels --jq '.labels[].name'
gh issue view 456 --json assignees --jq '.assignees[].login'
```

## Commenting on Issues

### Simple Comments

```bash
gh issue comment 456 --body "Thanks for reporting! Investigating now."

gh issue comment 456 --body "This is a duplicate of #123"
```

### Comments from Files

```bash
gh issue comment 456 --body-file response.md
```

### Multiline Comments

```bash
gh issue comment 456 --body "$(cat << 'EOF'
## Investigation Results

I've identified the root cause:
- Database connection timeout is too short
- Retry logic is missing

## Proposed Solution
Increase timeout to 30s and add exponential backoff.

I'll create a PR shortly.
EOF
)"
```

### Add Comment When Closing

```bash
gh issue close 456 --comment "Fixed in #789"
```

## Editing Issues

### Update Title

```bash
gh issue edit 456 --title "New improved title"
```

### Update Body

```bash
gh issue edit 456 --body "Updated description with more details"
gh issue edit 456 --body-file updated-description.md
```

### Modify Labels

```bash
# Add labels
gh issue edit 456 --add-label bug,priority-high

# Remove labels
gh issue edit 456 --remove-label enhancement

# Replace all labels
gh issue edit 456 --label bug,confirmed
```

### Modify Assignees

```bash
# Add assignees
gh issue edit 456 --add-assignee alice,bob

# Remove assignees
gh issue edit 456 --remove-assignee alice

# Replace all assignees
gh issue edit 456 --assignee bob,charlie
```

### Update Milestone

```bash
gh issue edit 456 --milestone "v2.1"
gh issue edit 456 --milestone ""  # Remove milestone
```

### Update Project

```bash
gh issue edit 456 --add-project "Sprint 5"
gh issue edit 456 --remove-project "Sprint 4"
```

### Batch Edit Multiple Issues

```bash
# Add label to multiple issues
for issue in 123 124 125; do
  gh issue edit "$issue" --add-label needs-review
done

# Close multiple issues
gh issue list --label wontfix --json number \
  | jq -r '.[].number' \
  | while read issue; do
    gh issue close "$issue" --comment "Closing as won't fix"
  done
```

## Closing and Reopening Issues

### Close Issue

```bash
gh issue close 456
gh issue close 456 --comment "Fixed in v2.0"
gh issue close 456 --reason "not planned"  # Mark as "not planned" vs "completed"
```

### Reopen Issue

```bash
gh issue reopen 456
gh issue reopen 456 --comment "Reopening due to regression"
```

## Pinning Issues

### Pin Important Issues

```bash
gh issue pin 456     # Pin to repository (visible on issues page)
```

### Unpin Issues

```bash
gh issue unpin 456
```

## Transferring Issues

### Transfer to Another Repository

```bash
gh issue transfer 456 --repo owner/other-repo
```

## Deleting Issues

**Use with caution - this is permanent:**

```bash
gh issue delete 456
gh issue delete 456 --yes  # Skip confirmation
```

## Issue Triage Workflows

### Triage New Issues

**Systematic approach:**

```bash
# 1. List new issues (created in last 24 hours)
gh issue list --json number,title,createdAt \
  --jq '.[] | select(.createdAt > (now - 86400 | todate))'

# 2. For each new issue, view details
gh issue view 789 --comments

# 3. Apply appropriate labels
gh issue edit 789 --add-label bug,needs-investigation

# 4. Assign if applicable
gh issue edit 789 --add-assignee @me

# 5. Add triage comment
gh issue comment 789 --body "Thanks for the report! Investigating this issue."

# 6. Update milestone if appropriate
gh issue edit 789 --milestone "v2.1"
```

### Automated Triage Script

```bash
#!/bin/bash
# triage-new-issues.sh

# Get issues created today without labels
gh issue list --json number,title,labels,createdAt \
  --jq '.[] | select(.labels | length == 0) | select(.createdAt > (now - 86400 | todate)) | .number' \
  | while read issue; do
    echo "Triaging issue #$issue"

    # View issue content
    TITLE=$(gh issue view "$issue" --json title --jq '.title')
    BODY=$(gh issue view "$issue" --json body --jq '.body')

    # Apply labels based on content (customize logic)
    if echo "$TITLE $BODY" | grep -qi "bug\|error\|fail"; then
      gh issue edit "$issue" --add-label bug
    fi

    if echo "$TITLE $BODY" | grep -qi "feature\|enhancement"; then
      gh issue edit "$issue" --add-label enhancement
    fi

    # Add triage comment
    gh issue comment "$issue" --body "Thank you for opening this issue! We'll review it shortly."

    echo "Triaged issue #$issue"
  done
```

### Close Stale Issues

```bash
# Find issues not updated in 60 days
gh issue list --json number,title,updatedAt \
  --jq '.[] | select(.updatedAt < (now - 5184000 | todate)) | .number' \
  | while read issue; do
    gh issue close "$issue" \
      --comment "Closing due to inactivity. Please reopen if this is still relevant."
  done
```

### Bulk Label Management

**Add "needs-response" to all issues awaiting author:**

```bash
gh issue list --search "is:open label:waiting-for-author" --json number \
  | jq -r '.[].number' \
  | while read issue; do
    gh issue edit "$issue" --add-label needs-response
  done
```

**Remove "needs-triage" after initial review:**

```bash
gh issue list --label needs-triage --json number \
  | jq -r '.[].number' \
  | while read issue; do
    # Check if issue has any other labels
    LABELS=$(gh issue view "$issue" --json labels --jq '.labels | length')
    if [ "$LABELS" -gt 1 ]; then
      gh issue edit "$issue" --remove-label needs-triage
    fi
  done
```

## Issue Response Workflows

### Standard Response Templates

**Bug Report Response:**
```bash
gh issue comment 456 --body "$(cat << 'EOF'
Thank you for the detailed bug report!

I've confirmed this issue and added it to our backlog. Here's what happens next:
1. We'll prioritize it in our next planning meeting
2. A team member will be assigned to investigate
3. We'll update this issue with our findings

In the meantime, here's a workaround: [workaround details]
EOF
)"
```

**Feature Request Response:**
```bash
gh issue comment 456 --body "$(cat << 'EOF'
Thank you for the feature suggestion!

This is an interesting idea. To help us evaluate it:
- Could you share your use case in more detail?
- How often would you use this feature?
- Are there any workarounds you're currently using?

We'll discuss this with the team and update the issue.
EOF
)"
```

**Request for More Information:**
```bash
gh issue edit 456 --add-label needs-more-info

gh issue comment 456 --body "$(cat << 'EOF'
Thank you for the report! To help us investigate:

**Additional Information Needed:**
- What version are you using?
- Can you provide steps to reproduce?
- Do you see any error messages in the console?

Please provide these details so we can investigate further.
EOF
)"
```

### Duplicate Issue Handling

```bash
# Mark as duplicate and close
gh issue close 456 --comment "Duplicate of #123" --reason "not planned"

# Link to canonical issue in comment
gh issue comment 456 --body "This is a duplicate of #123. Please follow that issue for updates. Closing this one to avoid fragmentation."

# Add duplicate label
gh issue edit 456 --add-label duplicate
```

## Working with Issue Templates

### Use Template When Creating

```bash
gh issue create --template bug_report.md
gh issue create --template feature_request.md
```

### View Available Templates

```bash
ls .github/ISSUE_TEMPLATE/
```

## Linking Issues and PRs

### Reference Issues in PR

When creating PRs, reference issues in the body:

```bash
gh pr create \
  --title "fix: Resolve login bug" \
  --body "Fixes #456. This PR resolves the SSO login issue by..."
```

**Keywords that auto-close issues when PR merges:**
- `Fixes #456`
- `Closes #456`
- `Resolves #456`

### Link Issues to Each Other

```bash
gh issue comment 456 --body "Related to #123"
gh issue comment 456 --body "Blocked by #789"
gh issue comment 456 --body "Depends on #234"
```

## Issue Metrics and Reporting

### Count Open Issues by Label

```bash
gh issue list --label bug --json number | jq 'length'
gh issue list --label enhancement --json number | jq 'length'
```

### Average Time to Close

```bash
gh issue list --state closed --json number,createdAt,closedAt \
  --jq 'map((.closedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) | add / length / 86400' \
  | xargs -I {} echo "Average days to close: {}"
```

### Issues by Author

```bash
gh issue list --json author --jq '[.[].author.login] | group_by(.) | map({author: .[0], count: length})'
```

## Error Handling

### Common Issues

**Issue not found:**
```
! issue not found
```
**Solution:** Verify issue number with `gh issue list`

**Permission denied:**
```
! HTTP 403: Forbidden
```
**Solution:** Check repository permissions, ensure you have write access

**Invalid label:**
```
! label not found: xyz
```
**Solution:** Check available labels with `gh label list`

### Verification Before Operations

**Check if issue exists:**
```bash
gh issue view 456 &>/dev/null && echo "Issue exists" || echo "Issue not found"
```

**Verify issue is open:**
```bash
STATE=$(gh issue view 456 --json state --jq '.state')
if [ "$STATE" = "OPEN" ]; then
  echo "Issue is open"
else
  echo "Issue is closed"
fi
```

**Check for specific label:**
```bash
gh issue view 456 --json labels --jq '.labels[].name' | grep -q "bug" && echo "Has bug label"
```

## Best Practices

1. **Use descriptive titles** that summarize the issue clearly
2. **Provide context** in the issue body (steps to reproduce, environment, etc.)
3. **Apply appropriate labels** immediately during triage
4. **Assign issues** to team members or yourself when starting work
5. **Link related issues** and PRs for context
6. **Update issues** as status changes (add comments, update labels)
7. **Close with resolution** explanation (fixed, duplicate, won't fix)
8. **Use templates** for consistent issue format
9. **Respond promptly** to issue authors, especially for clarifications
10. **Track metrics** to improve issue resolution times

## Related Commands

- `gh pr` - Link issues to pull requests
- `gh label` - Manage label definitions
- `gh milestone` - Manage milestones
- `gh project` - Add issues to projects
- `gh api` - Custom issue operations

See `api-usage.md` for advanced issue operations using `gh api`.
