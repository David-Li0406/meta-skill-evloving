---
id: notion-pm
name: "Notion PM"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Notion PM

## Overview

Notion is a flexible all-in-one workspace that combines documents, databases, and project management. Its strength lies in customizable databases, relation fields, and template systems that allow teams to build tailored PM solutions without rigid structure.

## When to Use

- Teams wanting highly customizable PM setup
- Organizations combining docs and tasks in one tool
- Startups needing flexible, evolving processes
- Teams requiring rich documentation alongside task tracking
- Cross-functional teams with diverse workflow needs

## Process/Steps

### 1. Workspace Structure

```
Workspace
├── Teamspace: Engineering
│   ├── Projects Database
│   ├── Tasks Database
│   ├── Sprint Database
│   ├── Documentation
│   └── Meeting Notes
├── Teamspace: Product
│   ├── Roadmap Database
│   ├── Feature Requests
│   └── User Research
└── Teamspace: Shared
    ├── OKRs
    ├── Team Directory
    └── Company Wiki
```

### 2. Database Design

**Projects Database:**
```yaml
database: Projects
properties:
  - name: "Name"
    type: title

  - name: "Status"
    type: select
    options: ["Planning", "In Progress", "On Hold", "Completed", "Cancelled"]

  - name: "Priority"
    type: select
    options: ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"]

  - name: "Owner"
    type: person

  - name: "Team"
    type: multi_select
    options: ["Frontend", "Backend", "Design", "DevOps"]

  - name: "Start Date"
    type: date

  - name: "Target Date"
    type: date

  - name: "Progress"
    type: formula
    formula: "Tasks Completed / Total Tasks"

  - name: "Tasks"
    type: relation
    database: "Tasks"

  - name: "Documents"
    type: relation
    database: "Docs"
```

**Tasks Database:**
```yaml
database: Tasks
properties:
  - name: "Task"
    type: title

  - name: "Status"
    type: status
    groups:
      not_started: ["Backlog", "Todo"]
      in_progress: ["In Progress", "In Review"]
      complete: ["Done"]

  - name: "Priority"
    type: select
    options: ["Urgent", "High", "Medium", "Low"]

  - name: "Assignee"
    type: person

  - name: "Project"
    type: relation
    database: "Projects"

  - name: "Sprint"
    type: relation
    database: "Sprints"

  - name: "Estimate"
    type: number
    format: "number"

  - name: "Due Date"
    type: date

  - name: "Tags"
    type: multi_select
    options: ["Bug", "Feature", "Tech Debt", "Docs", "Design"]

  - name: "Blocked By"
    type: relation
    database: "Tasks"
    self_relation: true
```

### 3. Views Configuration

**Board View:**
```yaml
view: "Sprint Board"
type: board
group_by: Status
filter:
  - Sprint equals "Current Sprint"
sort: Priority ascending
card_preview: "Page Cover"
card_size: medium
properties_shown:
  - Assignee
  - Priority
  - Estimate
  - Due Date
```

**Table View:**
```yaml
view: "All Tasks"
type: table
filter: none
sort:
  - Status ascending
  - Priority ascending
properties:
  - Task (title)
  - Status
  - Priority
  - Assignee
  - Project
  - Sprint
  - Due Date
  - Tags
```

**Timeline View:**
```yaml
view: "Roadmap"
type: timeline
date_property: "Date Range"
group_by: Project
filter:
  - Status not equals "Cancelled"
show_table: true
```

**Calendar View:**
```yaml
view: "Deadlines"
type: calendar
date_property: "Due Date"
filter:
  - Status not equals "Done"
```

### 4. Template System

**Task Template:**
```markdown
# {Task Title}

## Description
[What needs to be done]

## Context
[Why this task exists, background]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
[Implementation details]

## Resources
- [Link 1]()
- [Link 2]()

## Sub-tasks
- [ ] Sub-task 1
- [ ] Sub-task 2

## Updates
| Date | Update |
|------|--------|
| | |
```

**Sprint Template:**
```markdown
# Sprint {Number}

**Duration:** {Start Date} - {End Date}

## Sprint Goal
[One sentence goal]

## Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Points Committed | | |
| Points Completed | | |
| Velocity | | |

## Sprint Backlog
{Linked Database - Tasks filtered by this Sprint}

## Daily Standups
### Day 1
- **Done:**
- **Doing:**
- **Blockers:**

### Day 2
...

## Retrospective
### What went well
-

### What could improve
-

### Action items
- [ ]
```

### 5. Automations

**Using Notion Automations:**
```yaml
automation_1:
  trigger: "Property edited"
  condition: "Status is Done"
  action: "Set Completion Date to Today"

automation_2:
  trigger: "Property edited"
  condition: "Priority is Urgent"
  action: "Notify @{Assignee}"

automation_3:
  trigger: "Page added"
  condition: "Database is Tasks"
  action: "Set Status to Backlog"
```

**Using Zapier/Make:**
```yaml
zap_1:
  trigger: notion_page_created
  filter: database = "Tasks"
  action: slack_post_message
  channel: "#task-updates"

zap_2:
  trigger: notion_property_updated
  filter: Status = "Done"
  action: notion_update_page
  set: "Completed Date" = now()
```

### 6. Relations & Rollups

**Example Relations:**
```yaml
# Tasks ←→ Projects (bidirectional)
tasks_database:
  - property: "Project"
    type: relation
    relates_to: "Projects"

projects_database:
  - property: "Tasks"
    type: relation
    relates_to: "Tasks"

# Rollup: Task Count per Project
projects_database:
  - property: "Task Count"
    type: rollup
    relation: "Tasks"
    property_to_rollup: "Task"
    calculation: "Count all"

  - property: "Completed Tasks"
    type: rollup
    relation: "Tasks"
    property_to_rollup: "Status"
    calculation: "Count values"
    filter: "Done"

  - property: "Total Points"
    type: rollup
    relation: "Tasks"
    property_to_rollup: "Estimate"
    calculation: "Sum"
```

### 7. Formulas

**Useful Formulas:**
```javascript
// Days until due
if(empty(prop("Due Date")), "No due date",
  dateBetween(prop("Due Date"), now(), "days") + " days")

// Progress percentage
if(prop("Total Tasks") == 0, 0,
  round(prop("Completed Tasks") / prop("Total Tasks") * 100))

// Priority emoji
if(prop("Priority") == "Urgent", "🔴",
if(prop("Priority") == "High", "🟠",
if(prop("Priority") == "Medium", "🟡", "🟢")))

// Status with emoji
if(prop("Status") == "Done", "✅ Done",
if(prop("Status") == "In Progress", "🔄 In Progress",
if(prop("Status") == "In Review", "👀 In Review", "📋 " + prop("Status"))))

// Overdue check
if(empty(prop("Due Date")), false,
  and(prop("Status") != "Done", prop("Due Date") < now()))
```

## Best Practices

### Database Design
1. **Start simple** - Add properties as needed
2. **Use relations** - Connect related data
3. **Rollups for metrics** - Aggregate data automatically
4. **Templates for consistency** - Standardize page structure

### View Organization
1. **Purpose-driven views** - Each view serves specific need
2. **Smart filters** - Show relevant data only
3. **Consistent naming** - Clear view names
4. **Favorite views** - Quick access to common views

### Team Collaboration
1. **Permissions** - Set appropriate access levels
2. **Comments** - Use @mentions for discussions
3. **Page history** - Track changes
4. **Synced blocks** - Share content across pages

### Performance
1. **Limit properties** - 15-20 max per database
2. **Archive old data** - Move completed items
3. **Use linked databases** - Instead of duplicating
4. **Optimize formulas** - Complex formulas slow down

## Templates/Examples

### Product Roadmap Page

```markdown
# Product Roadmap 2024

## Vision
[Product vision statement]

## Q1 Themes
{Linked Database: Projects | Filter: Q1 | View: Board by Status}

## Q2 Themes
{Linked Database: Projects | Filter: Q2 | View: Board by Status}

## Timeline View
{Linked Database: Projects | View: Timeline}

## Key Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Features Shipped | 12 | {Rollup} |
| Customer Satisfaction | 4.5 | {API} |
```

### Sprint Planning Page

```markdown
# Sprint 24 Planning

## Sprint Info
| Property | Value |
|----------|-------|
| Start | Jan 15, 2024 |
| End | Jan 28, 2024 |
| Goal | Launch user dashboard |

## Team Capacity
| Member | Days | Focus |
|--------|------|-------|
| @alice | 10 | Frontend |
| @bob | 8 | Backend |

## Sprint Backlog
{Linked Database: Tasks | Filter: Sprint = Sprint 24 | View: Table}

## Sprint Board
{Linked Database: Tasks | Filter: Sprint = Sprint 24 | View: Board}

## Notes
### Planning Notes
-

### Mid-Sprint Check
-

### Retrospective
**Good:**
-

**Improve:**
-

**Actions:**
- [ ]
```

### Bug Report Template

```markdown
# 🐛 {Bug Title}

## Summary
[One line description]

## Environment
- **Version:** [e.g., 2.1.0]
- **Browser:** [e.g., Chrome 120]
- **OS:** [e.g., macOS 14]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[What should happen]

## Actual Behavior
[What happens instead]

## Screenshots
[Attach screenshots]

## Severity
- [ ] Critical (system down)
- [ ] Major (feature broken)
- [ ] Minor (workaround exists)
- [ ] Low (cosmetic)

## Investigation Notes
[Technical findings]

## Related
- [Link to related issues]
```

### API Integration

```javascript
// Notion API - Create Task
const response = await notion.pages.create({
  parent: { database_id: "tasks-database-id" },
  properties: {
    "Task": {
      title: [{ text: { content: "New Task" } }]
    },
    "Status": {
      status: { name: "Backlog" }
    },
    "Priority": {
      select: { name: "High" }
    },
    "Assignee": {
      people: [{ id: "user-id" }]
    },
    "Estimate": {
      number: 5
    }
  }
});

// Query Tasks
const response = await notion.databases.query({
  database_id: "tasks-database-id",
  filter: {
    and: [
      { property: "Status", status: { does_not_equal: "Done" } },
      { property: "Assignee", people: { contains: "user-id" } }
    ]
  },
  sorts: [{ property: "Priority", direction: "ascending" }]
});
```

## References

- [Notion Documentation](https://www.notion.so/help)
- [Notion API](https://developers.notion.com/)
- [Notion Templates](https://www.notion.so/templates)
- [Notion Formulas](https://www.notion.so/help/formulas)
- [Notion Automations](https://www.notion.so/help/automations)
