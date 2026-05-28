---
id: linear-issue-tracking
name: "Linear Issue Tracking"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Linear Issue Tracking

## Overview

Linear is a modern, streamlined issue tracking tool designed for high-velocity software teams. Known for its speed, keyboard-first interface, and opinionated workflows, Linear emphasizes efficiency and developer experience over configurability.

## When to Use

- Building software products with engineering-focused teams
- Teams that value speed and keyboard-driven workflows
- Startups and growth-stage companies
- Organizations wanting minimal configuration overhead
- Teams practicing continuous deployment

## Process/Steps

### 1. Workspace Structure

```
Workspace (Organization)
├── Team (Product Area)
│   ├── Projects (Initiatives)
│   │   └── Issues (Work Items)
│   ├── Cycles (Sprints)
│   └── Roadmap
└── Team
```

**Linear Philosophy:**
- Teams own their workflow
- Projects span multiple cycles
- Cycles provide time-boxing
- Roadmap shows long-term vision

### 2. Team Configuration

```yaml
team_settings:
  name: "Backend"
  key: "BAK"  # Issue prefix: BAK-123

  workflow:
    - Backlog
    - Todo
    - In Progress
    - In Review
    - Done
    - Canceled

  cycle:
    duration: 2_weeks
    start_day: monday
    auto_archive: true
    upcoming_cycles: 2

  estimates:
    type: points  # or hours
    scale: [0, 1, 2, 3, 5, 8, 13]

  triage:
    enabled: true
    default_assignee: null
```

### 3. Issue Management

**Issue Properties:**
| Property | Purpose | Values |
|----------|---------|--------|
| Status | Workflow state | Backlog, Todo, In Progress, etc. |
| Priority | Urgency level | Urgent, High, Medium, Low, No Priority |
| Estimate | Effort sizing | Fibonacci points |
| Cycle | Sprint assignment | Current, Next, Future |
| Project | Initiative grouping | Product features, Tech debt |
| Label | Categorization | Bug, Feature, Improvement |
| Assignee | Responsibility | Team member |
| Parent | Hierarchy | Sub-issues under parent |

**Issue Creation:**
```markdown
# Issue Title
Brief description of what needs to be done.

## Context
Why this issue exists and relevant background.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
Implementation details or constraints.

## Links
- Design: [Figma link]
- Spec: [Notion link]
- Related: BAK-456
```

### 4. Projects & Roadmap

**Project Structure:**
```yaml
project:
  name: "User Authentication Overhaul"
  lead: "@engineer"
  target_date: "2024-Q2"
  status: "In Progress"  # Planned, In Progress, Completed, Canceled

  milestones:
    - name: "OAuth Integration"
      target_date: "2024-02-15"
      issues: [BAK-100, BAK-101, BAK-102]

    - name: "MFA Support"
      target_date: "2024-03-01"
      issues: [BAK-110, BAK-111]
```

**Roadmap Configuration:**
- Quarterly or monthly view
- Projects plotted on timeline
- Dependencies between projects
- Status indicators and progress

### 5. Cycles (Sprints)

**Cycle Workflow:**
```
1. Cycle Planning (Start of cycle)
   - Pull from backlog into cycle
   - Set cycle scope/goals
   - Estimate all issues

2. During Cycle
   - Daily updates via status changes
   - Scope adjustments if needed
   - Track velocity

3. Cycle Completion
   - Auto-archive completed issues
   - Incomplete → Next cycle or Backlog
   - Review metrics
```

**Cycle Goals Template:**
```markdown
## Cycle 24 Goals

### Primary
- Complete OAuth integration (BAK-100 series)
- Ship performance improvements

### Secondary
- Address critical bugs
- Update documentation

### Success Metrics
- Velocity: 40+ points
- Bugs closed: 10+
- No rollbacks
```

### 6. Triage Process

```
Inbox (Triage)
    │
    ├── Is it valid? ──No──→ Close/Duplicate
    │
    ├── Is it urgent? ──Yes──→ Current Cycle + High Priority
    │
    ├── Is it scoped? ──No──→ Needs Refinement label
    │
    └── Ready ──→ Backlog + Appropriate Labels
```

### 7. GitHub Integration

```yaml
github_integration:
  link_prs:
    - pattern: "Fixes BAK-\\d+"
    - auto_transition: "In Review"

  auto_close:
    - on_merge: true
    - target_status: "Done"

  branch_format:
    - pattern: "{username}/bak-{issue_number}-{issue_title}"

  status_sync:
    - pr_opened: "In Review"
    - pr_merged: "Done"
    - pr_closed: null  # No change
```

## Best Practices

### Issue Quality
1. **Atomic issues** - One issue, one deliverable
2. **Clear acceptance criteria** - Testable conditions
3. **Proper sizing** - Break down large issues
4. **Link related issues** - Use "relates to", "blocks"

### Workflow Efficiency
1. **Use keyboard shortcuts** - `C` create, `S` status, `P` priority
2. **Leverage views** - Custom filtered views for focus
3. **Batch operations** - Select multiple issues
4. **Use templates** - Consistent issue creation

### Cycle Management
1. **Protect cycle scope** - Resist mid-cycle additions
2. **Track velocity** - Use for future planning
3. **Review incomplete** - Understand why work wasn't finished
4. **Celebrate wins** - Acknowledge completed work

### Team Coordination
1. **Daily standups via Linear** - Check "My Issues" view
2. **Weekly sync** - Review backlog and priorities
3. **Async updates** - Comment on issues, not Slack
4. **Document decisions** - Add context to issues

## Templates/Examples

### Bug Report Template

```markdown
## Bug: [Brief Description]

### Environment
- Version: 2.1.0
- Browser/OS: Chrome 120 / macOS
- User role: Admin

### Steps to Reproduce
1. Navigate to /settings
2. Click "Save" without changes
3. Error appears

### Expected Behavior
Save button should be disabled when no changes.

### Actual Behavior
500 error thrown, console shows validation error.

### Evidence
- Screenshot: [attached]
- Error log: `ValidationError: field required`

### Severity
- [ ] Critical (system down)
- [x] Major (feature broken)
- [ ] Minor (workaround exists)
- [ ] Trivial (cosmetic)
```

### Feature Request Template

```markdown
## Feature: [Title]

### Problem Statement
What user problem does this solve?

### Proposed Solution
High-level approach to solving the problem.

### User Stories
- As a [role], I want [capability] so that [benefit]

### Success Metrics
- Metric 1: [target]
- Metric 2: [target]

### Out of Scope
- Explicitly excluded items

### Design
- [Figma link]

### Dependencies
- Requires BAK-200
- Blocked by API changes
```

### Sprint Retrospective

```markdown
## Cycle 24 Retrospective

### Velocity
- Planned: 45 points
- Completed: 42 points
- Completion rate: 93%

### What Went Well
- OAuth shipped on time
- Good collaboration with frontend team
- Zero production incidents

### What Needs Improvement
- Late scope additions disrupted flow
- Flaky tests caused delays
- Documentation lagged behind

### Action Items
- [ ] BAK-300: Fix flaky test suite
- [ ] BAK-301: Add docs to Definition of Done
- [ ] Process: Freeze scope after Day 2
```

### Custom Views

```yaml
views:
  my_work:
    filter: "assignee:me status:active"
    group_by: priority

  team_board:
    filter: "team:backend"
    group_by: status
    show_estimates: true

  bugs_triage:
    filter: "label:bug status:triage"
    sort_by: created_date

  release_scope:
    filter: "project:v2.0 status:-canceled"
    group_by: status
```

## References

- [Linear Documentation](https://linear.app/docs)
- [Linear Method](https://linear.app/method)
- [Linear Keyboard Shortcuts](https://linear.app/docs/keyboard-shortcuts)
- [Linear API](https://developers.linear.app/)
- [Linear Integrations](https://linear.app/integrations)
