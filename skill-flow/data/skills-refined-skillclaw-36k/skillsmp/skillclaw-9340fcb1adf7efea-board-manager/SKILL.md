---
name: board-manager
description: Use this skill to manage GitHub Project board items, including adding issues, updating their status, and moving them between columns.
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

**Project:** [Project Name] (#<project-number>)  
**URL:** [Project URL]

### IDs Reference

| Resource        | ID                               |
| --------------- | -------------------------------- |
| Project ID      | `<project-id>`                   |
| Status Field ID | `<status-field-id>`              |

### Status Option IDs

| Status      | Option ID  | Description                 |
| ----------- | ---------- | --------------------------- |
| Backlog     | `<backlog-id>` | Not ready / needs triage    |
| Todo        | `<todo-id>`    | Not started                 |
| In Progress | `<in-progress-id>` | Currently being worked on   |
| Blocked     | `<blocked-id>` | PR created, awaiting review |
| Done        | `<done-id>`    | Merged to main              |

## Commands

### Add Issue to Project Board

```bash
gh project item-add <project-number> --owner <owner> --url <issue-url>
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
    organization(login: "<owner>") {
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
  local item_id=$1
  local option_id=$2
  # Add logic to move the issue status
}
```