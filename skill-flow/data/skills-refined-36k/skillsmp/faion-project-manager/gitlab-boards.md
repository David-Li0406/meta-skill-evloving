---
id: gitlab-boards
name: "GitLab Boards"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# GitLab Boards

## Overview

GitLab Issue Boards provide kanban-style project management integrated with GitLab's DevOps platform. Boards visualize issues through customizable lists based on labels, assignees, or milestones, enabling seamless workflow management alongside CI/CD pipelines.

## When to Use

- Teams using GitLab for source control and CI/CD
- Organizations wanting unified DevOps and PM in one platform
- Projects requiring multiple board views per project
- Teams practicing GitLab Flow or similar branching strategies
- Enterprise environments with compliance requirements

## Process/Steps

### 1. Board Types

**Issue Boards:**
- Project-level boards for single repo
- Group-level boards for cross-project visibility
- Multiple boards per project (Premium+)

**Board Lists:**
| List Type | Based On | Use Case |
|-----------|----------|----------|
| Label | Issue labels | Workflow stages |
| Assignee | Team member | Workload view |
| Milestone | Release target | Release planning |
| Iteration | Sprint | Sprint board |

### 2. Label-Based Workflow

```yaml
# Workflow Labels (scoped)
labels:
  workflow:
    - "workflow::backlog"
    - "workflow::ready"
    - "workflow::in-progress"
    - "workflow::review"
    - "workflow::testing"
    - "workflow::done"

  priority:
    - "priority::critical"
    - "priority::high"
    - "priority::medium"
    - "priority::low"

  type:
    - "type::feature"
    - "type::bug"
    - "type::tech-debt"
    - "type::docs"
```

**Scoped Labels:**
- Use `::` syntax for mutual exclusivity
- Issue can only have one `workflow::*` label
- Prevents conflicting states

### 3. Board Configuration

```yaml
board_configuration:
  name: "Development Board"

  lists:
    - type: label
      label: "workflow::backlog"
      position: 0

    - type: label
      label: "workflow::ready"
      position: 1
      limit: 10  # WIP limit (Premium)

    - type: label
      label: "workflow::in-progress"
      position: 2
      limit: 5

    - type: label
      label: "workflow::review"
      position: 3
      limit: 3

    - type: label
      label: "workflow::testing"
      position: 4

    - type: closed
      position: 5

  filters:
    milestone: "v1.0"
    assignee: null
    labels: ["type::feature"]
```

### 4. Multiple Boards Strategy

**Board Per Purpose:**
```
Project Boards:
├── Sprint Board
│   └── Filter: current iteration
├── Bug Triage Board
│   └── Filter: type::bug, open issues
├── Release Board
│   └── Filter: milestone v1.0
└── Tech Debt Board
    └── Filter: type::tech-debt
```

### 5. Issue Management

**Issue Template:**
```markdown
## Summary
Brief description of the issue.

## Details
Detailed explanation with context.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Approach
Implementation notes.

/label ~"workflow::backlog" ~"type::feature"
/milestone %"v1.0"
/weight 3
/estimate 2d
```

**Quick Actions:**
```
/label ~bug                    # Add label
/unlabel ~feature              # Remove label
/milestone %"v1.0"             # Set milestone
/assign @username              # Assign user
/weight 5                      # Set weight (story points)
/estimate 2d                   # Time estimate
/due 2024-03-01               # Set due date
/relate #123                   # Link related issue
/blocks #456                   # Mark as blocker
```

### 6. Iterations (Sprints)

```yaml
iteration_cadence:
  title: "Development Sprints"
  start_date: "2024-01-01"
  duration: 2  # weeks
  upcoming: 4  # number of iterations to create
  automatic: true

iterations:
  - title: "Sprint 1"
    start_date: "2024-01-01"
    due_date: "2024-01-14"

  - title: "Sprint 2"
    start_date: "2024-01-15"
    due_date: "2024-01-28"
```

### 7. Automation with GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy
  - notify

update_issue_on_mr:
  stage: notify
  script:
    - |
      curl --request PUT \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --data "labels=workflow::review" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/issues/$ISSUE_ID"
  rules:
    - if: $CI_MERGE_REQUEST_IID
      when: always

close_issue_on_merge:
  stage: notify
  script:
    - |
      # Issue is auto-closed if MR description contains "Closes #123"
      echo "Issue will be closed automatically"
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_PIPELINE_SOURCE == "merge_request_event"
```

### 8. Service Desk Integration

```yaml
service_desk:
  enabled: true
  email: "support+myproject@incoming.gitlab.com"

  templates:
    thank_you: |
      Thank you for contacting us!
      Your request has been logged as issue #{{ISSUE_ID}}.

  auto_labels:
    - "source::service-desk"
    - "workflow::triage"
```

## Best Practices

### Label Strategy
1. **Use scoped labels** - Prevent conflicting states
2. **Color coding** - Consistent colors across projects
3. **Limit label count** - 15-20 labels maximum
4. **Document labels** - Describe purpose in label description

### Board Design
1. **Match workflow** - Boards reflect actual process
2. **Set WIP limits** - Prevent overload
3. **Use filters** - Create focused views
4. **Archive done issues** - Keep boards clean

### Issue Quality
1. **Templates required** - Enforce structure
2. **Weight estimation** - Use consistently
3. **Link related issues** - Build traceability
4. **Update regularly** - Issues reflect current state

### Team Workflow
1. **Daily board review** - Quick standup via board
2. **Weekly grooming** - Clean up stale issues
3. **Sprint boundaries** - Respect iteration scope
4. **Retrospectives** - Use iteration reports

## Templates/Examples

### Bug Report Template

```markdown
<!-- .gitlab/issue_templates/Bug.md -->
## Bug Description
<!-- Brief description of the bug -->

## Environment
- GitLab Version: <!-- e.g., 16.5 -->
- Browser/OS: <!-- e.g., Chrome 120 / macOS -->
- Project: <!-- link to project -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Screenshots/Logs
<!-- Attach relevant evidence -->

## Severity
- [ ] Critical (system down)
- [ ] Major (feature broken)
- [ ] Minor (workaround exists)
- [ ] Low (cosmetic)

/label ~"type::bug" ~"workflow::triage"
/weight 0
```

### Feature Request Template

```markdown
<!-- .gitlab/issue_templates/Feature.md -->
## Feature Summary
<!-- One-line description -->

## Problem Statement
<!-- What user problem does this solve? -->

## Proposed Solution
<!-- High-level approach -->

## User Stories
<!-- As a [role], I want [capability] so that [benefit] -->
- As a user, I want to...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Design
<!-- Link to Figma/mockups if available -->

## Technical Considerations
<!-- API changes, database migrations, etc. -->

## Dependencies
<!-- Related issues or external dependencies -->

/label ~"type::feature" ~"workflow::backlog"
/milestone %"Backlog"
```

### Sprint Planning Issue

```markdown
## Sprint [N] Planning - [Date Range]

### Sprint Goal
<!-- One sentence describing sprint objective -->

### Capacity
| Team Member | Days | Notes |
|-------------|------|-------|
| @dev1 | 10 | Full |
| @dev2 | 8 | PTO |

### Committed Issues
<!-- Link to board filter: iteration = current -->
Total Weight: XX points

### Risks & Dependencies
- Risk 1: mitigation
- Dependency: #123 must complete first

### Definition of Done
- [ ] Code merged to main
- [ ] Tests passing in CI
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO acceptance

/label ~"meta::sprint-planning"
/iteration *current
```

### Merge Request Template

```markdown
<!-- .gitlab/merge_request_templates/Default.md -->
## Description
<!-- What does this MR do? -->

## Related Issue
Closes #<!-- issue number -->

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] Changelog updated (if applicable)

## Screenshots
<!-- For UI changes -->

/assign_reviewer @teammate
/label ~"workflow::review"
```

### API Examples

```bash
# Create issue
curl --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --data "title=New Feature&labels=workflow::backlog,type::feature&weight=5" \
  "https://gitlab.com/api/v4/projects/123/issues"

# Move issue on board
curl --request PUT \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --data "labels=workflow::in-progress" \
  "https://gitlab.com/api/v4/projects/123/issues/456"

# Get board lists
curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/123/boards/1/lists"
```

## References

- [GitLab Issue Boards](https://docs.gitlab.com/ee/user/project/issue_board.html)
- [GitLab Labels](https://docs.gitlab.com/ee/user/project/labels.html)
- [GitLab Iterations](https://docs.gitlab.com/ee/user/group/iterations/)
- [GitLab Quick Actions](https://docs.gitlab.com/ee/user/project/quick_actions.html)
- [GitLab API](https://docs.gitlab.com/ee/api/)
