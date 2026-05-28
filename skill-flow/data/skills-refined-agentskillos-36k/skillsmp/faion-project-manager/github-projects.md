---
id: github-projects
name: "GitHub Projects"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# GitHub Projects

## Overview

GitHub Projects is GitHub's native project management tool that integrates directly with issues, pull requests, and repositories. It offers both classic board views and the newer Projects (beta) with tables, custom fields, and automation powered by GitHub Actions.

## When to Use

- Teams already using GitHub for source control
- Open source projects requiring public project boards
- Organizations wanting tight integration between code and project management
- Smaller teams needing lightweight PM without additional tools
- Projects requiring transparency with community contributors

## Process/Steps

### 1. Project Types

**GitHub Projects (New):**
- Table, board, and roadmap views
- Custom fields and metadata
- Cross-repository support
- Built-in automation
- API and Actions integration

**Classic Projects (Legacy):**
- Simple kanban boards
- Per-repository or organization-wide
- Basic automation
- Limited customization

### 2. Project Structure

```
Organization
├── Project (Cross-repo view)
│   ├── Views (Table, Board, Roadmap)
│   ├── Custom Fields
│   ├── Workflows (Automation)
│   └── Items (Issues, PRs, Drafts)
└── Repository
    ├── Issues
    ├── Pull Requests
    └── Milestones
```

### 3. Setting Up a New Project

```yaml
project_configuration:
  name: "Product Roadmap Q1 2024"
  visibility: public  # or private

  custom_fields:
    - name: "Status"
      type: single_select
      options: ["Backlog", "Todo", "In Progress", "In Review", "Done"]

    - name: "Priority"
      type: single_select
      options: ["P0", "P1", "P2", "P3"]

    - name: "Estimate"
      type: number

    - name: "Sprint"
      type: iteration
      duration: 2_weeks

    - name: "Team"
      type: single_select
      options: ["Frontend", "Backend", "DevOps"]

    - name: "Release"
      type: single_select
      options: ["v1.0", "v1.1", "v2.0"]
```

### 4. Views Configuration

**Table View:**
```yaml
table_view:
  name: "All Issues"
  fields:
    - Title
    - Status
    - Priority
    - Assignee
    - Estimate
    - Sprint
    - Repository
  group_by: null
  sort_by: Priority
  filter: null
```

**Board View:**
```yaml
board_view:
  name: "Sprint Board"
  column_field: Status
  card_fields:
    - Assignee
    - Priority
    - Estimate
  filter: "sprint:@current"
  wip_limits:
    "In Progress": 5
    "In Review": 3
```

**Roadmap View:**
```yaml
roadmap_view:
  name: "Release Roadmap"
  date_field: iteration
  group_by: Release
  zoom_level: month
  markers:
    - "2024-03-01: v1.0 Release"
    - "2024-06-01: v2.0 Release"
```

### 5. Workflows (Automation)

**Built-in Workflows:**
```yaml
workflows:
  - name: "Item added to project"
    trigger: item_added
    action: set_field(Status, "Backlog")

  - name: "Item reopened"
    trigger: issue_reopened
    action: set_field(Status, "Todo")

  - name: "Item closed"
    trigger: issue_closed
    action: set_field(Status, "Done")

  - name: "Pull request merged"
    trigger: pr_merged
    action: set_field(Status, "Done")

  - name: "Code review requested"
    trigger: review_requested
    action: set_field(Status, "In Review")
```

**GitHub Actions Automation:**
```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, labeled]
  pull_request:
    types: [opened, ready_for_review]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/myorg/projects/1
          github-token: ${{ secrets.PROJECT_TOKEN }}
          labeled: bug, feature
          label-operator: OR

  set-fields:
    runs-on: ubuntu-latest
    steps:
      - uses: titoportas/update-project-fields@v0.1.0
        with:
          project-url: https://github.com/orgs/myorg/projects/1
          github-token: ${{ secrets.PROJECT_TOKEN }}
          item-id: ${{ github.event.issue.node_id }}
          field-keys: Priority,Team
          field-values: P1,Backend
```

### 6. Issue Templates

```yaml
# .github/ISSUE_TEMPLATE/feature.yml
name: Feature Request
description: Suggest a new feature
labels: ["enhancement"]
projects: ["myorg/1"]
body:
  - type: markdown
    attributes:
      value: "## Feature Request"

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should we solve this?
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - P0 - Critical
        - P1 - High
        - P2 - Medium
        - P3 - Low
    validations:
      required: true
```

### 7. Milestones Integration

```yaml
milestones:
  - title: "v1.0 Release"
    due_date: "2024-03-01"
    description: "Initial public release"

  - title: "v1.1 Release"
    due_date: "2024-04-15"
    description: "Bug fixes and minor improvements"
```

## Best Practices

### Project Organization
1. **Cross-repo projects** - Use organization-level projects for multi-repo work
2. **Consistent fields** - Standardize custom fields across projects
3. **Clear naming** - Project names should indicate scope and timeline
4. **Archive completed** - Close projects when done

### Issue Management
1. **Use templates** - Ensure consistent issue quality
2. **Label strategically** - Don't over-label
3. **Link PRs to issues** - Use "Fixes #123" syntax
4. **Close stale issues** - Regular cleanup

### Automation
1. **Start with built-in** - Use project workflows first
2. **Actions for complex** - GitHub Actions for advanced logic
3. **Document automation** - Team should understand what's automated
4. **Test carefully** - Automation can create noise

### Team Collaboration
1. **Regular triage** - Process new issues weekly
2. **Sprint planning** - Use iteration fields
3. **Async updates** - Comment on issues, not Slack
4. **Public transparency** - Open source benefits from visibility

## Templates/Examples

### Sprint Planning Issue

```markdown
## Sprint 24 Planning

### Sprint Goal
Complete user authentication overhaul and address critical bugs.

### Capacity
| Team Member | Days Available | Notes |
|-------------|----------------|-------|
| @dev1 | 10 | Full sprint |
| @dev2 | 8 | PTO Friday |
| @dev3 | 10 | Full sprint |

### Committed Issues
- [ ] #123 - OAuth integration (8 pts)
- [ ] #124 - MFA support (5 pts)
- [ ] #125 - Password reset flow (3 pts)
- [ ] #130 - Critical login bug (2 pts)

### Sprint Risks
- OAuth provider API instability
- Dependency on design review

### Definition of Done
- Code merged to main
- Tests passing
- Documentation updated
- Deployed to staging
```

### Release Checklist Issue

```markdown
## Release v1.0.0 Checklist

### Pre-Release
- [ ] All milestone issues closed
- [ ] Changelog updated
- [ ] Version bumped in package.json
- [ ] Integration tests passing
- [ ] Security scan completed
- [ ] Performance benchmarks met

### Release
- [ ] Create release branch
- [ ] Tag release
- [ ] Build production artifacts
- [ ] Deploy to production
- [ ] Verify deployment

### Post-Release
- [ ] Announce release
- [ ] Monitor for issues
- [ ] Update documentation site
- [ ] Close milestone
- [ ] Retrospective scheduled
```

### GraphQL API Query

```graphql
query GetProjectItems($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              state
              assignees(first: 3) {
                nodes {
                  login
                }
              }
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field {
                  ... on ProjectV2Field {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## References

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [GitHub CLI](https://cli.github.com/manual/gh_project)
