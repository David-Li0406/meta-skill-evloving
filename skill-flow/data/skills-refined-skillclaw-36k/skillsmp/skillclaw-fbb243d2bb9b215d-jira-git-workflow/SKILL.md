---
name: jira-git-workflow
description: Use this skill when you need to integrate JIRA ticket management with Git branching and planning for a systematic development workflow.
---

# Skill body

This skill implements a standard JIRA-to-Git workflow by combining JIRA integration and ticket-branching logic. It provides a structured approach to managing development tasks tracked in JIRA.

## Core Workflow Steps

### Step 1: Identify JIRA Project
**Purpose**: Retrieve the JIRA project and cloud ID for subsequent operations.

**Tools Used**: `atlassian_getAccessibleAtlassianResources`, `atlassian_getVisibleJiraProjects`

```bash
# Get accessible resources
atlassian_getAccessibleAtlassianResources

# List available JIRA projects
atlassian_getVisibleJiraProjects
```

**Expected Output**:
```json
[
  {
    "key": "PROJECT_KEY",
    "name": "Project Name"
  }
]
```

### Step 2: Create JIRA Ticket
**Purpose**: Create a new task or issue in the specified JIRA project.

**Tools Used**: `atlassian_createJiraIssue`, `atlassian_atlassianUserInfo`

```bash
# Get current user info for assignment
atlassian_atlassianUserInfo

# Create a new JIRA issue
atlassian_createJiraIssue --cloudId "CLOUD_ID" --projectKey "PROJECT_KEY" --issueTypeName "Task" --summary "Issue Summary" --description "Detailed description" --assignee_account_id "ACCOUNT_ID"
```

**Expected Output**:
```json
{
  "key": "PROJECT_KEY-101"
}
```

### Step 3: Create Git Branch
**Purpose**: Create a new Git branch named after the JIRA ticket.

```bash
# Create and checkout a new branch
git checkout -b "PROJECT_KEY-101"
```

### Step 4: Create PLAN.md
**Purpose**: Generate a PLAN.md file for the implementation structure.

```bash
# Create PLAN.md with implementation details
echo "# Implementation Plan" > PLAN.md
```

### Step 5: Commit PLAN.md
**Purpose**: Commit the PLAN.md file with a semantic commit message.

```bash
# Commit the PLAN.md file
git add PLAN.md
git commit -m "feat: add implementation plan for PROJECT_KEY-101"
```

### Step 6: Update JIRA Ticket
**Purpose**: Add a comment to the JIRA ticket with progress details.

**Tools Used**: `git-issue-updater`

```bash
# Update the JIRA ticket with commit details
git-issue-updater --issue "PROJECT_KEY-101" --comment "Progress updated with commit details."
```

## When to use me
Use this skill when:
- You are starting a new development task tracked in JIRA.
- You need a systematic approach to manage JIRA tickets, branching, and planning.
- You want to ensure that your workflow adheres to best practices in ticket management and version control.

## Prerequisites
- Active Atlassian/JIRA account with appropriate permissions.
- Git repository initialized.
- Write access to the repository.