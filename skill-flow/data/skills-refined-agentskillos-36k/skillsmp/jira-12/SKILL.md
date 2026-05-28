---
name: jira
description: Use for all Jira-related tasks. When user mentions a ticket (PROJ-123) or shares a Jira URL, use
  the jira CLI instead of web fetching.
user-invocable: false
allowed-tools: Bash
---

# Jira CLI

Use the `jira` CLI for all Jira operations. Never web fetch Jira URLs.

## Common Commands

```bash
# View issue details
jira issue view PROJ-123

# List issues in a project
jira issue list -p PROJ

# List issues assigned to me
jira issue list -a$(jira me)

# Search with JQL
jira issue list -q "project = PROJ AND status = 'In Progress'"

# Create an issue
jira issue create -p PROJ -t Task -s "Title here" -b "Description here"

# Move issue to different status
jira issue move PROJ-123 "In Progress"

# Add a comment
jira issue comment add PROJ-123 "Comment text here"

# Assign to someone
jira issue assign PROJ-123 "email@example.com"

# Link issues
jira issue link PROJ-123 PROJ-456 "blocks"
```

## When User Shares Jira URL

Extract the ticket key from URLs like `https://company.atlassian.net/browse/PROJ-123` and run:

```bash
jira issue view PROJ-123
```
