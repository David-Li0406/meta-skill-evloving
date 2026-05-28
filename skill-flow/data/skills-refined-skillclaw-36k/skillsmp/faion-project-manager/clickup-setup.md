---
id: clickup-setup
name: "ClickUp Setup"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# ClickUp Setup

## Overview

ClickUp is an all-in-one productivity platform that combines project management, docs, goals, and time tracking. This methodology covers workspace architecture, hierarchy design, automations, and effective use of ClickUp's unique features like ClickApps and views.

## When to Use

- Starting a new organization or team in ClickUp
- Migrating from another PM tool to ClickUp
- Restructuring existing ClickUp workspace for scalability
- Setting up cross-functional team collaboration
- Implementing OKRs and goal tracking alongside tasks

## Process/Steps

### 1. Workspace Hierarchy

```
Workspace (Organization)
├── Space (Department/Team)
│   ├── Folder (Project/Initiative)
│   │   ├── List (Phase/Category)
│   │   │   └── Tasks
│   │   │       └── Subtasks
│   │   │           └── Checklists
│   │   └── List
│   └── Folder
└── Space
```

**Hierarchy Best Practices:**
| Level | Use For | Example |
|-------|---------|---------|
| Workspace | Company | Acme Corp |
| Space | Department/Product | Engineering, Marketing |
| Folder | Project/Initiative | Q1 Product Launch |
| List | Phase/Category | Backend, Frontend, QA |
| Task | Work item | Implement API endpoint |

### 2. ClickApps Configuration

**Essential ClickApps:**

```yaml
recommended_clickapps:
  - name: "Time Tracking"
    scope: workspace
    settings:
      billable_rates: true
      estimates: true

  - name: "Sprints"
    scope: space
    settings:
      sprint_duration: 2_weeks
      auto_close: true

  - name: "Custom Fields"
    scope: workspace

  - name: "Priorities"
    scope: workspace
    levels: [Urgent, High, Normal, Low]

  - name: "Multiple Assignees"
    scope: workspace

  - name: "Time Estimates"
    scope: workspace
```

### 3. Custom Status Configuration

**Development Workflow:**
```
Statuses:
├── To Do (Open)
│   ├── Backlog
│   └── Ready for Dev
├── In Progress (Active)
│   ├── In Development
│   ├── Code Review
│   └── QA Testing
└── Done (Closed)
    ├── Completed
    └── Won't Do
```

**Status Template (JSON):**
```json
{
  "statuses": [
    {"status": "backlog", "type": "open", "color": "#d3d3d3"},
    {"status": "ready", "type": "open", "color": "#6fddff"},
    {"status": "in progress", "type": "custom", "color": "#4169e1"},
    {"status": "review", "type": "custom", "color": "#ff8c00"},
    {"status": "qa", "type": "custom", "color": "#9370db"},
    {"status": "complete", "type": "closed", "color": "#6bc950"},
    {"status": "won't do", "type": "closed", "color": "#808080"}
  ]
}
```

### 4. Views Configuration

**Essential Views:**

| View Type | Purpose | Configuration |
|-----------|---------|---------------|
| List | Detailed task management | Group by status, show all fields |
| Board | Kanban workflow | Group by status, WIP limits |
| Gantt | Timeline planning | Show dependencies, milestones |
| Calendar | Deadline tracking | Show due dates, sprints |
| Workload | Capacity planning | Time estimates per assignee |
| Dashboard | Metrics & reporting | Widgets for velocity, burndown |

### 5. Custom Fields Setup

```yaml
custom_fields:
  - name: "Story Points"
    type: number
    location: space

  - name: "Sprint"
    type: dropdown
    options: ["Sprint 1", "Sprint 2", "Sprint 3"]

  - name: "Component"
    type: labels
    options: ["Frontend", "Backend", "Database", "DevOps"]

  - name: "PR Link"
    type: url

  - name: "Reviewer"
    type: people

  - name: "Acceptance Criteria"
    type: text
```

### 6. Automations

**Key Automation Examples:**

```yaml
# Auto-assign on status change
automation_1:
  trigger: status_changed_to("In Development")
  action: assign_from_custom_field("Developer")

# Create subtasks from template
automation_2:
  trigger: task_created_in_list("Features")
  action: apply_task_template("Feature Template")

# Notify on overdue
automation_3:
  trigger: due_date_arrives
  condition: status_not_in(["Complete", "Won't Do"])
  action:
    - send_email(assignee)
    - add_comment("Task is overdue!")

# Move to sprint folder
automation_4:
  trigger: custom_field_changed("Sprint")
  action: move_to_list("Sprint {{sprint_value}}")
```

### 7. Templates

**Task Template Example:**
```markdown
## Task: [Feature Name]

### Description
[What needs to be built]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Technical Notes
[Implementation details]

### Dependencies
- Depends on: [TASK-XXX]
- Blocks: [TASK-YYY]

### Checklist
- [ ] Implementation complete
- [ ] Unit tests written
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] QA passed
```

## Best Practices

### Hierarchy Design
1. **Keep hierarchy shallow** - 3-4 levels maximum
2. **Use Spaces for isolation** - Separate permissions, workflows
3. **Folders for related work** - Group by project, not timeline
4. **Lists for workflow stages** - Match your actual process

### Custom Fields
1. **Create at highest applicable level** - Workspace > Space > Folder
2. **Use dropdown for consistency** - Prevent typos and variants
3. **Required fields sparingly** - Only what's truly necessary
4. **Archive unused fields** - Keep field list clean

### Automations
1. **Start simple** - Add complexity gradually
2. **Test thoroughly** - Use test tasks before production
3. **Document automations** - Maintain automation inventory
4. **Avoid automation loops** - Check for circular triggers

### Team Adoption
1. **Training sessions** - Onboard team properly
2. **Document conventions** - Create team handbook
3. **Regular reviews** - Optimize based on feedback
4. **Champion users** - Identify power users for support

## Templates/Examples

### Sprint Planning Dashboard

```yaml
dashboard_widgets:
  - type: "sprint_burndown"
    data_source: current_sprint

  - type: "workload"
    group_by: assignee
    metric: time_estimate

  - type: "status_distribution"
    chart_type: pie

  - type: "overdue_tasks"
    filter: due_date < today

  - type: "velocity"
    sprints: last_5
```

### Folder Structure for Software Project

```
Space: Product Development
├── Folder: Feature Development
│   ├── List: Backlog
│   ├── List: Current Sprint
│   ├── List: In Review
│   └── List: Done
├── Folder: Bug Tracking
│   ├── List: Reported
│   ├── List: Triaged
│   ├── List: In Progress
│   └── List: Resolved
├── Folder: Tech Debt
│   ├── List: Identified
│   └── List: Addressed
└── Folder: Documentation
    ├── List: API Docs
    └── List: User Guides
```

### Integration Setup

```yaml
integrations:
  github:
    - link_prs_to_tasks: true
    - auto_status_on_merge: "Complete"
    - branch_naming: "clickup-{task_id}-{task_name}"

  slack:
    - channel: "#dev-updates"
    - notify_on: ["status_change", "comment", "assignee_change"]

  time_tracking:
    - provider: "Toggl"
    - sync_estimates: true
    - billable_tracking: true
```

## References

- [ClickUp Documentation](https://docs.clickup.com/)
- [ClickUp University](https://university.clickup.com/)
- [ClickUp API](https://clickup.com/api)
- [ClickUp Templates](https://clickup.com/templates)
