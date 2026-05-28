---
name: board-manager
description: Manage GitHub Project board items - add issues, update status, and move between columns. Use when user asks to add issues to the board, change status, or organize the project.
---

# Board Manager Skill

## Purpose

Add issues to the project board and update their status. This skill has **write permissions** for board operations.

## When to Use This

- User asks "add this issue to the board"
- User asks "move #X to In Progress"
- User asks "update status of issue"
- After creating a new issue (auto-add to board)
- After completing work (move to Done)

## Project Board Configuration

**Project:** Specify the project name and number (e.g., Development (#X))  
**URL:** Provide the project URL (e.g., https://github.com/orgs/your-org/projects/X)

### IDs Reference

| Resource        | ID                               |
| --------------- | -------------------------------- |
| Project ID      | `<project-id>`                  |
| Status Field ID | `<status-field-id>`             |

### Status Option IDs

| Status      | Option ID  | Description                 |
| ----------- | ---------- | --------------------------- |
| Backlog     | `<backlog-id>` | Not ready / needs triage    |
| Next        | `<next-id>` | Ready to pick up            |
| In Progress | `<in-progress-id>` | Currently being worked on   |
| Blocked     | `<blocked-id>` | PR created, awaiting review |
| Done        | `<done-id>` | Merged to main              |
| Todo        | `<todo-id>` | Not started                 |

## Commands

### Add Issue to Project Board

```bash
gh project item-add <project-number> --owner <owner> --url https://github.com/<owner>/<repo>/issues/<number>
```

### Get Item ID for an Issue

```bash
gh project item-list <project-number> --owner <owner> --format json | \
  jq -r '.items[] | select(.content.number == <issue-number>) | .id'
```

Or via GraphQL:

```bash
gh api graphql -f query='
  query {
    organization(login: "<org-name>") {
      projectV2(number: <project-number>) {
        items(first: 100) {
          nodes {
            id
            content { ... on Issue { number } }
          }
        }
      }
    }
  }' | jq -r '.data.organization.projectV2.items.nodes[] | select(.content.number == <issue-number>) | .id'
```

### Update Issue Status

```bash
gh api graphql \
  -f projectId="<project-id>" \
  -f itemId="<item-id>" \
  -f fieldId="<status-field-id>" \
  -f optionId="<option-id>" \
  -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }'
```

### Remove Issue from Project

```bash
gh project item-delete <project-number> --owner <owner> --id <item-id>
```

## Helper Functions

### Move Issue to Status

```bash
move_issue_status() {
  local issue_number=$1
  local option_id=$2  # e.g., <backlog-id>, <in-progress-id>, <done-id>
  local status_name=$3

  # Get item ID
  local item_id=$(gh project item-list <project-number> --owner <owner> --format json | \
    jq -r '.items[] | select(.content.number == '$issue_number') | .id')

  if [ -z "$item_id" ]; then
    echo "Issue #$issue_number not found on project board"
    return 1
  fi

  # Update status
  gh api graphql \
    -f projectId="<project-id>" \
    -f itemId="$item_id" \
    -f fieldId="<status-field-id>" \
    -f optionId="$option_id" \
    -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { singleSelectOptionId: $optionId }
      }) { projectV2Item { id } }
    }'

  echo "Moved #$issue_number to $status_name"
}
```

## Workflow Integration

### Start Working on Issue

1. Add issue to project (if not already)
2. Set status to "In Progress"

```bash
# Add to project
gh project item-add <project-number> --owner <owner> --url "https://github.com/<owner>/<repo>/issues/<number>"

# Get item ID and move to In Progress
ITEM_ID=$(gh project item-list <project-number> --owner <owner> --format json | \
  jq -r '.items[] | select(.content.number == <number>) | .id')

gh api graphql \
  -f projectId="<project-id>" \
  -f itemId="$ITEM_ID" \
  -f fieldId="<status-field-id>" \
  -f optionId="<in-progress-id>" \
  -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) { projectV2Item { id } }
  }'
```

### Complete Issue

Set status to "Done" (PR merge will auto-close issue).

## Status Mapping

| Action | Status | Option ID |
|--------|--------|-----------|
| New issue, not started | Todo | `<todo-id>` |
| New issue, not ready | Backlog | `<backlog-id>` |
| Ready to work | Next | `<next-id>` |
| Started work | In Progress | `<in-progress-id>` |
| PR created | Blocked | `<blocked-id>` |
| PR merged | Done | `<done-id>` |

## Query Current IDs (if they change)

```bash
gh api graphql -f query='
query {
  organization(login: "<org-name>") {
    projectV2(number: <project-number>) {
      id
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}'
```

## Output Format

After operations, confirm:

```markdown
**Board Update:** Issue #X moved to [Status]
**URL:** https://github.com/<owner>/projects/<project-number>
```