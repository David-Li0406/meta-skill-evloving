---
id: azure-devops-boards
name: "Azure DevOps Boards"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Azure DevOps Boards

## Overview

Azure DevOps Boards is Microsoft's enterprise project management solution that integrates with Azure Pipelines, Repos, and Test Plans. It supports multiple process templates (Agile, Scrum, CMMI, Basic) and offers extensive customization for complex enterprise workflows.

## When to Use

- Enterprise organizations using Microsoft ecosystem
- Teams requiring compliance and audit trails
- Projects needing advanced reporting (Analytics)
- Organizations using Azure cloud services
- Teams requiring custom process templates

## Process/Steps

### 1. Process Templates

**Built-in Processes:**
| Process | Work Items | Best For |
|---------|------------|----------|
| Basic | Issue, Task | Simple projects |
| Agile | Epic, Feature, User Story, Task, Bug | Agile teams |
| Scrum | Epic, Feature, PBI, Task, Bug, Impediment | Scrum teams |
| CMMI | Epic, Feature, Requirement, Task, Bug, Change Request, Review, Risk | Regulated industries |

### 2. Work Item Hierarchy

**Agile Process:**
```
Portfolio Backlog
├── Epic (large initiative)
│   └── Feature (shippable capability)
│       └── User Story (user value)
│           └── Task (technical work)
│               └── Bug (defect - can be at any level)
```

**Work Item Configuration:**
```yaml
work_item_types:
  epic:
    fields:
      - title
      - description
      - business_value
      - time_criticality
      - effort
      - start_date
      - target_date
    states: [New, Active, Resolved, Closed]

  user_story:
    fields:
      - title
      - description
      - acceptance_criteria
      - story_points
      - priority
      - risk
      - value_area
    states: [New, Active, Resolved, Closed]

  task:
    fields:
      - title
      - description
      - remaining_work
      - original_estimate
      - completed_work
      - activity
    states: [New, Active, Closed]
```

### 3. Board Configuration

**Kanban Board Settings:**
```yaml
board_settings:
  columns:
    - name: "New"
      state_mapping: ["New"]
      wip_limit: null
      split: false

    - name: "Active"
      state_mapping: ["Active"]
      wip_limit: 5
      split: true  # Doing/Done split

    - name: "Resolved"
      state_mapping: ["Resolved"]
      wip_limit: 3

    - name: "Closed"
      state_mapping: ["Closed"]

  swimlanes:
    - name: "Expedite"
      default: false
    - name: "Default"
      default: true
    - name: "Tech Debt"
      default: false

  card_fields:
    core: [ID, Title, Assigned To, State]
    additional: [Story Points, Tags, Priority]

  card_styles:
    rules:
      - name: "Blocked"
        condition: "Tags Contains 'Blocked'"
        style:
          background_color: "#FF0000"
```

### 4. Sprint Configuration

```yaml
iteration_path:
  root: "MyProject"
  iterations:
    - path: "MyProject\\Release 1"
      children:
        - path: "MyProject\\Release 1\\Sprint 1"
          start_date: "2024-01-01"
          end_date: "2024-01-14"
        - path: "MyProject\\Release 1\\Sprint 2"
          start_date: "2024-01-15"
          end_date: "2024-01-28"
    - path: "MyProject\\Release 2"
      children:
        - path: "MyProject\\Release 2\\Sprint 3"
          # ...
```

### 5. Area Path Organization

```yaml
area_paths:
  - path: "MyProject\\Frontend"
    team: "Frontend Team"
  - path: "MyProject\\Backend"
    team: "Backend Team"
  - path: "MyProject\\DevOps"
    team: "Platform Team"
  - path: "MyProject\\Shared"
    team: null  # Multiple teams
```

### 6. Queries

**WIQL Examples:**
```sql
-- My Active Items
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.State] IN ('New', 'Active')
ORDER BY [Microsoft.VSTS.Common.Priority]

-- Sprint Burndown
SELECT [System.Id], [System.Title], [System.State],
       [Microsoft.VSTS.Scheduling.RemainingWork]
FROM WorkItems
WHERE [System.IterationPath] = @CurrentIteration
  AND [System.WorkItemType] IN ('User Story', 'Bug', 'Task')

-- Bugs by Priority
SELECT [System.Id], [System.Title], [System.State],
       [Microsoft.VSTS.Common.Priority]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.State] <> 'Closed'
ORDER BY [Microsoft.VSTS.Common.Priority]

-- Features without Stories
SELECT [System.Id], [System.Title]
FROM WorkItems
WHERE [System.WorkItemType] = 'Feature'
  AND [System.State] <> 'Closed'
  AND NOT [System.Id] IN (
    SELECT [System.Parent]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'User Story'
  )
```

### 7. Automation Rules

```yaml
# Automation rules (Boards settings)
rules:
  - name: "Auto-close parent when children done"
    trigger: child_state_changed
    conditions:
      - all_children_state: "Closed"
    actions:
      - set_state: "Closed"

  - name: "Set iteration on activation"
    trigger: state_changed_to_active
    conditions:
      - iteration_is_empty: true
    actions:
      - set_iteration: "@CurrentIteration"

  - name: "Notify on blocked"
    trigger: tag_added
    conditions:
      - tag: "Blocked"
    actions:
      - send_email:
          to: "@[Assigned To]"
          subject: "Item blocked: @[Title]"
```

### 8. Pipeline Integration

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - feature/*

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: UpdateWorkItem@1
            inputs:
              workItemId: $(Build.SourceVersionMessage)
              updateRule: "AddComment"
              comment: "Build $(Build.BuildNumber) started"

  - stage: Deploy
    jobs:
      - deployment: DeployProd
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - task: UpdateWorkItem@1
                  inputs:
                    workItemId: $(WorkItemId)
                    updateRule: "State"
                    state: "Resolved"
```

## Best Practices

### Process Selection
1. **Match team maturity** - Basic for new teams, Scrum for experienced
2. **Inherit vs customize** - Start with inheritance, customize minimally
3. **Standardize across org** - Use same process template
4. **Document changes** - Track customizations

### Hierarchy Design
1. **Portfolio for visibility** - Epics for executive reporting
2. **Features for releases** - Align with deployable increments
3. **Stories for value** - Each delivers user value
4. **Tasks for tracking** - Optional detailed tracking

### Board Optimization
1. **WIP limits** - Enforce to prevent overload
2. **Definition of Done** - Document per column
3. **Card styles** - Visual cues for blockers, priority
4. **Swimlanes** - Separate work types or priorities

### Team Configuration
1. **Area paths** - Clear ownership
2. **Iteration paths** - Consistent sprint structure
3. **Capacity planning** - Set team capacity per sprint
4. **Velocity tracking** - Use for forecasting

## Templates/Examples

### User Story Template

```markdown
## User Story: [Title]

**As a** [persona],
**I want** [capability],
**So that** [benefit].

### Acceptance Criteria
```gherkin
Given [precondition]
When [action]
Then [result]

Given [precondition]
When [action]
Then [result]
```

### Description
[Additional context and details]

### Design
[Link to mockups]

### Technical Notes
[Implementation considerations]

### Dependencies
- Depends on: [#123]
- Blocks: [#456]

### Out of Scope
- [Explicitly excluded items]
```

### Sprint Planning Template

```markdown
## Sprint [N] Planning

### Sprint Goal
[One sentence describing the primary objective]

### Capacity
| Team Member | Days Available | Hours/Day | Focus Areas |
|-------------|----------------|-----------|-------------|
| @dev1 | 10 | 6 | Backend |
| @dev2 | 8 | 6 | Frontend |
| @dev3 | 10 | 6 | Full-stack |

**Total Capacity:** XX hours

### Sprint Backlog
| ID | Title | Points | Assignee | Hours |
|----|-------|--------|----------|-------|
| 123 | Story A | 5 | @dev1 | 20 |
| 124 | Story B | 3 | @dev2 | 12 |

**Total Committed:** XX points / XX hours

### Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Risk 1 | High | Action |

### Definition of Done
- [ ] Code complete and reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO accepted
```

### Dashboard Widgets

```yaml
dashboard:
  name: "Team Dashboard"
  widgets:
    - type: "burndown"
      title: "Sprint Burndown"
      iteration: "@CurrentIteration"

    - type: "velocity"
      title: "Team Velocity"
      sprints: 6

    - type: "cumulative-flow"
      title: "CFD"
      time_period: 30_days

    - type: "query-tile"
      title: "Open Bugs"
      query: "Shared Queries/Open Bugs"

    - type: "work-item-chart"
      title: "Story Points by Area"
      chart_type: "stacked-bar"
      group_by: "Area Path"
      measure: "Sum of Story Points"
```

### REST API Examples

```bash
# Create work item
curl -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $PAT" \
  -d '[
    {"op": "add", "path": "/fields/System.Title", "value": "New Story"},
    {"op": "add", "path": "/fields/System.IterationPath", "value": "Project\\Sprint 1"},
    {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": 5}
  ]' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/\$User%20Story?api-version=7.0"

# Update work item state
curl -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $PAT" \
  -d '[{"op": "add", "path": "/fields/System.State", "value": "Active"}]' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/123?api-version=7.0"

# Query work items
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $PAT" \
  -d '{"query": "SELECT [System.Id] FROM WorkItems WHERE [System.State] = '\''Active'\''"}' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.0"
```

## References

- [Azure Boards Documentation](https://learn.microsoft.com/en-us/azure/devops/boards/)
- [Process Customization](https://learn.microsoft.com/en-us/azure/devops/organizations/settings/work/customize-process)
- [WIQL Syntax](https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/)
- [Analytics Service](https://learn.microsoft.com/en-us/azure/devops/report/powerbi/)
