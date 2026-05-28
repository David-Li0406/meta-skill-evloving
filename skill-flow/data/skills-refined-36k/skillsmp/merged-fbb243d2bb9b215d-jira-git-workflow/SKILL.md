---
name: jira-git-workflow
description: Use this skill for integrating JIRA ticket management with Git workflows, including ticket creation, branch management, and progress updates.
---

## What I do

I provide a comprehensive workflow for integrating JIRA ticket management with Git operations, combining functionalities from JIRA and Git frameworks:

1. **Get JIRA Resources**: Detect and retrieve Atlassian cloud ID, visible projects, and accessible resources.
2. **Get JIRA User Info**: Retrieve current user's account ID for ticket assignment.
3. **Create JIRA Tickets**: Create new tasks, stories, or bugs in specified JIRA projects.
4. **Add JIRA Comments**: Add comments to existing JIRA tickets with Markdown formatting.
5. **Upload Images to JIRA**: Upload local images as JIRA attachments and retrieve attachment URLs.
6. **Generate JIRA Branch Names**: Create consistent branch names from JIRA tickets.
7. **Fetch JIRA Issue Details**: Retrieve ticket information including status, assignee, and description.
8. **Create Git Branch**: Create a branch named after the JIRA ticket.
9. **Create PLAN.md**: Generate a PLAN.md file with implementation structure.
10. **Commit PLAN.md**: Use semantic commit formatting for the PLAN.md commit.
11. **Update JIRA Ticket**: Add progress comments to JIRA tickets with commit details.
12. **Transition JIRA Ticket Status**: Update JIRA ticket status after PR merge.

## When to use me

Use this workflow when:
- You need to start a new development task tracked in JIRA.
- You want a systematic approach: JIRA ticket → branch → PLAN.md.
- You need to ensure consistent branch naming and ticket management across Git workflows.

## Core Workflow Steps

### Step 1: Get Accessible Atlassian Resources

**Purpose**: Retrieve cloud ID and list of accessible Atlassian resources.

```bash
# Get accessible resources (includes cloud IDs)
atlassian_getAccessibleAtlassianResources
```

### Step 2: Get JIRA User Information

**Purpose**: Retrieve current user's account ID for ticket assignment.

```bash
# Get current user info
atlassian_atlassianUserInfo
```

### Step 3: Get Visible JIRA Projects

**Purpose**: List all JIRA projects the user has access to.

```bash
# Get visible projects
atlassian_getVisibleJiraProjects --cloudId <CLOUD_ID>
```

### Step 4: Create JIRA Ticket

**Purpose**: Create a new ticket in specified JIRA project.

```bash
# Create new ticket
atlassian_createJiraIssue \
  --cloudId <CLOUD_ID> \
  --projectKey <PROJECT_KEY> \
  --issueTypeName <ISSUE_TYPE> \
  --summary "<Ticket Title>" \
  --description "<Ticket Description>" \
  --assignee_account_id <USER_ACCOUNT_ID>
```

### Step 5: Add Comment to JIRA Ticket

**Purpose**: Add a comment to an existing JIRA ticket.

```bash
# Add comment
atlassian_addCommentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --commentBody "<Comment Content>"
```

### Step 6: Upload Image to JIRA

**Purpose**: Upload a local image file as a JIRA attachment.

```bash
# Upload image
atlassian_addAttachmentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --attachment <IMAGE_FILE_PATH>
```

### Step 7: Generate JIRA Branch Name

**Purpose**: Create a consistent branch name from a JIRA ticket key.

```bash
# Generate branch name from ticket key
BRANCH_NAME="<TICKET_KEY>"
git checkout -b "$BRANCH_NAME"
```

### Step 8: Create PLAN.md

**Purpose**: Generate a comprehensive plan document for the work.

```markdown
# Plan: <Ticket Title>

## Overview
Brief description of what this issue implements.

## Ticket Reference
- Ticket: <TICKET_KEY>
- URL: <TICKET_URL>

## Files to Modify
1. `src/path/to/file1.ts` - Description
2. `src/path/to/file2.tsx` - Description

## Approach
Detailed steps or methodology for implementation.

## Success Criteria
- All files modified correctly
- No build errors
- Tests pass
```

### Step 9: Commit PLAN.md Using Semantic Commits

**Purpose**: Commit PLAN.md as the first commit on the new branch with semantic formatting.

```bash
# Stage PLAN.md
git add PLAN.md
git commit -m "docs(PLAN): add planning document for <TICKET_KEY>"
```

### Step 10: Update JIRA Ticket with Initial Commit

**Purpose**: Add progress comment to JIRA ticket with commit details.

```bash
# Update JIRA ticket
atlassian_addCommentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --commentBody "<Formatted comment with commit details>"
```

### Step 11: Transition JIRA Ticket Status

**Purpose**: Update JIRA ticket status after PR merge.

```bash
# Get available transitions
TRANSITIONS=$(atlassian_getTransitionsForJiraIssue --cloudId <CLOUD_ID> --issueIdOrKey <TICKET_KEY>)
TARGET_TRANSITION_ID=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .id' | head -1)

# Execute transition
atlassian_transitionJiraIssue --cloudId <CLOUD_ID> --issueIdOrKey <TICKET_KEY> --transition '{"id": "<TRANSITION_ID>"}'
```

## Best Practices

- Use consistent branch naming with ticket keys.
- Always create a PLAN.md as the first commit.
- Update JIRA tickets with commit details after significant changes.
- Use semantic commit messages for clarity and traceability.

## Common Issues

### Permission Denied on JIRA

**Issue**: Cannot create JIRA ticket.

**Solution**: Ensure your account has create permissions for the project.

### Branch Already Exists

**Issue**: Branch with the same name already exists.

**Solution**: Use `git checkout -B <branch-name>` to force creation.

### Missing Cloud ID

**Issue**: Cannot create JIRA ticket without cloud ID.

**Solution**: Retrieve cloud ID using `atlassian_getAccessibleAtlassianResources`.

## Related Skills

- `jira-git-integration`: Provides JIRA-specific operations.
- `ticket-branch-workflow`: Core workflow for ticket-to-branch logic.
- `git-issue-updater`: For updating issues with commit progress.