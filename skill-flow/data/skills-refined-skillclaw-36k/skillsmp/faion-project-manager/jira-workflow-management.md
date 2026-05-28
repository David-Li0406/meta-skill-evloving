---
id: jira-workflow-management
name: "Jira Workflow Management"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Jira Workflow Management

## Overview

Jira is Atlassian's industry-leading project management tool for agile teams. This methodology covers workflow configuration, issue type schemes, automation rules, and best practices for managing software development projects effectively.

## When to Use

- Setting up a new Jira project for Scrum or Kanban teams
- Migrating from another tool to Jira
- Optimizing existing Jira workflows for better team efficiency
- Creating custom workflows for specific project types
- Integrating Jira with CI/CD pipelines and development tools

## Process/Steps

### 1. Project Setup

```
Project Type Selection:
├── Software Projects
│   ├── Scrum (sprints, backlogs, velocity)
│   ├── Kanban (continuous flow, WIP limits)
│   └── Bug Tracking (simplified workflow)
├── Business Projects
│   ├── Task Management
│   └── Process Management
└── Service Projects (Jira Service Management)
```

### 2. Issue Type Configuration

**Standard Issue Types:**
| Type | Purpose | Fields |
|------|---------|--------|
| Epic | Large feature grouping | Summary, Description, Start/End Date |
| Story | User-facing functionality | Story Points, Acceptance Criteria |
| Task | Technical work item | Estimate, Component |
| Bug | Defect tracking | Severity, Steps to Reproduce |
| Sub-task | Breakdown of parent | Linked to parent issue |

### 3. Workflow Design

**Basic Development Workflow:**
```
To Do → In Progress → Code Review → QA → Done
  │         │            │          │
  └─────────┴────────────┴──────────┘
            (Can return to previous)
```

**Workflow States:**
```yaml
statuses:
  - name: "To Do"
    category: "To Do"
  - name: "In Progress"
    category: "In Progress"
  - name: "Code Review"
    category: "In Progress"
  - name: "QA Testing"
    category: "In Progress"
  - name: "Done"
    category: "Done"

transitions:
  - from: "To Do"
    to: "In Progress"
    trigger: "Start Work"
  - from: "In Progress"
    to: "Code Review"
    trigger: "Submit for Review"
    condition: "Branch linked"
  - from: "Code Review"
    to: "QA Testing"
    trigger: "Approve"
  - from: "QA Testing"
    to: "Done"
    trigger: "Pass QA"
```

### 4. Board Configuration

**Scrum Board Setup:**
- Backlog view with sprint planning
- Active sprint board with swimlanes
- Burndown and velocity charts
- Sprint retrospective integration

**Kanban Board Setup:**
- WIP limits per column
- Cumulative flow diagram
- Cycle time tracking
- Expedite lane for urgent items

### 5. Automation Rules

**Common Automation Examples:**

```yaml
# Auto-assign on transition
rule: auto_assign_reviewer
trigger: issue_transitioned_to_code_review
action: assign_to_field(code_reviewer)

# Auto-close linked issues
rule: close_subtasks
trigger: parent_issue_done
action: transition_subtasks_to_done

# Slack notification
rule: notify_on_blocker
trigger: priority_changed_to_blocker
action: send_slack_message(channel=#dev-alerts)
```

### 6. JQL Queries

**Essential JQL Examples:**
```sql
-- My open issues
assignee = currentUser() AND resolution = Unresolved

-- Sprint backlog
project = PROJ AND sprint in openSprints()

-- Bugs created this week
project = PROJ AND type = Bug AND created >= -7d

-- Blocked items
status = "In Progress" AND flagged = "Impediment"

-- Overdue issues
duedate < now() AND resolution = Unresolved

-- Release scope
fixVersion = "1.0.0" AND resolution = Unresolved
```

## Best Practices

### Workflow Design
1. **Keep workflows simple** - 5-7 statuses maximum
2. **Match team reality** - Reflect actual process, not ideal
3. **Use transitions wisely** - Not every state needs to connect to every other
4. **Add validators** - Ensure required fields before transitions

### Board Management
1. **Set WIP limits** - Prevent overloading team members
2. **Use swimlanes** - Group by epic, assignee, or priority
3. **Configure quick filters** - Easy access to common views
4. **Regular backlog grooming** - Keep backlog under 2 sprints worth

### Integration Points
1. **GitHub/GitLab** - Link branches and PRs to issues
2. **Slack/Teams** - Notifications for important events
3. **CI/CD** - Update issues on build/deploy
4. **Confluence** - Link documentation to requirements

## Templates/Examples

### Sprint Planning Template

```markdown
## Sprint [N] Planning

**Sprint Goal:** [One sentence goal]

**Capacity:**
- Team members: [N]
- Working days: [N]
- Velocity (avg): [N] story points

**Committed Items:**
| Key | Summary | Points | Assignee |
|-----|---------|--------|----------|
| PROJ-123 | Feature A | 5 | @dev1 |
| PROJ-124 | Bug fix B | 3 | @dev2 |

**Risks:**
- [Risk 1]
- [Risk 2]
```

### Definition of Done Checklist

```markdown
## Definition of Done

- [ ] Code complete and pushed
- [ ] Unit tests written (>80% coverage)
- [ ] Code review approved
- [ ] QA testing passed
- [ ] Documentation updated
- [ ] No critical/blocker bugs
- [ ] Product Owner accepted
```

### Custom Field Configuration

```yaml
custom_fields:
  - name: "Story Points"
    type: number
    screen: "Edit Issue"

  - name: "Acceptance Criteria"
    type: text_area
    screen: "Create/Edit Issue"

  - name: "Code Reviewer"
    type: user_picker
    screen: "Edit Issue"

  - name: "Environment"
    type: select
    options: ["Dev", "Staging", "Production"]
```

## References

- [Jira Software Documentation](https://support.atlassian.com/jira-software-cloud/)
- [Jira Automation](https://www.atlassian.com/software/jira/guides/automation)
- [JQL Reference](https://support.atlassian.com/jira-software-cloud/docs/jql-fields/)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
