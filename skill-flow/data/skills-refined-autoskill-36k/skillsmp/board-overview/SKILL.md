---
name: board-overview
description: Commands for viewing the Guidr GitHub Projects board and tracking progress. Includes filtering by status, assignee, labels, and board health checks to understand project status.
---

# Board Overview Skill

Commands for viewing the Guidr GitHub Projects board and tracking progress.

## View Project Board

**Board URL**: https://github.com/users/stevendejongnl/projects/3

View directly in GitHub UI for full board visualization.

## Command Line Overview

```bash
# List all issues with project status
gh issue list --json number,title,state,assignees,projectItems

# Filter by status (requires labels or project fields)
gh issue list --json number,title,assignees --state open

# List issues assigned to you
gh issue list --assignee @me --json number,title,state

# Count issues by state
gh issue list --json state | jq '.[] | .state' | sort | uniq -c
```

## Check Your Active Tickets

```bash
# View all your assigned issues
gh issue list --assignee @me --state open

# View detailed info on your tickets
gh issue list --assignee @me --json number,title,state,updatedAt

# View specific ticket
gh issue view 123
```

## Board Statuses

The Guidr project board has three statuses:

1. **Todo** - Not yet started
2. **In Progress** - Currently being worked on
3. **Done** - Completed and merged

## Progress Tracking

```bash
# Get count of open issues
gh issue list --state open | wc -l

# Get issues needing attention (no assignee)
gh issue list --state open --json number,title | jq '.[] | select(.assignees | length == 0)'

# Check recently updated issues
gh issue list --state open --json number,title,updatedAt --sort updated --limit 10
```

## Review Issues by Category

```bash
# Mobile issues
gh issue list --label "mobile" --json number,title,assignees

# API issues
gh issue list --label "api" --json number,title,assignees

# Bug reports
gh issue list --label "bug" --json number,title,state

# Features in progress
gh issue list --state open --label "feature" --json number,title,assignees
```

## Board Insights

```bash
# Who's working on what?
gh issue list --state open --json assignees,number,title

# What's blocked?
gh issue list --label "blocked" --json number,title

# What's high priority?
gh issue list --label "priority:high" --json number,title

# How many items per person?
gh issue list --state open --json assignees | jq -r '.[] | .assignees[].login' | sort | uniq -c
```

## Filter by Project Field

For detailed project board queries (requires advanced gh CLI):

```bash
# View raw project data
gh api repos/stevendejongnl/guidr/projects/3/columns

# List project items with status
gh api graphql -f query='
  query {
    repository(owner: "stevendejongnl", name: "guidr") {
      projectNext(number: 3) {
        items(first: 20) {
          nodes {
            title
            content {
              __typename
              ... on Issue {
                number
                title
              }
            }
          }
        }
      }
    }
  }
'
```

## Quick Status Check

```bash
# Show all open issues in one view
gh issue list --state open --limit 50

# Show issues you should be working on
gh issue list --assignee @me --state open

# Show recently closed issues (celebrating wins!)
gh issue list --state closed --limit 10 --json number,title
```

## Board Health

- **Ideal**: Most items are assigned and have statuses
- **Watch for**: Items stuck in "In Progress" with no updates
- **Good practice**: Regularly review "Todo" items to prioritize

## Integration with Development

When starting work:
1. View the board to see available "Todo" items
2. Assign yourself to a ticket
3. Update status to "In Progress"
4. Link commits to the issue number
5. Move to "Done" when PR is merged

## Tips

- Check the board regularly for blocked items
- Keep statuses updated so others know what's happening
- Use labels to categorize work
- Review project board before starting a new task
