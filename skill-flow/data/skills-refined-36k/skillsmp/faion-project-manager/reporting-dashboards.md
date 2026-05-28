---
id: reporting-dashboards
name: "Reporting & Dashboards"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Reporting & Dashboards

## Overview

Effective reporting and dashboards transform raw project data into actionable insights. This methodology covers dashboard design principles, key metrics selection, automated reporting, and stakeholder-specific views across different PM tools.

## When to Use

- Setting up new project visibility systems
- Improving existing reporting capabilities
- Creating stakeholder-specific dashboards
- Automating status reporting
- Implementing portfolio-level visibility

## Process/Steps

### 1. Metrics Framework

**Metric Categories:**
```yaml
metrics:
  delivery_metrics:
    - velocity: "Story points completed per sprint"
    - throughput: "Issues completed per time period"
    - cycle_time: "Time from start to completion"
    - lead_time: "Time from request to delivery"
    - burndown: "Work remaining in sprint"
    - burnup: "Work completed over time"

  quality_metrics:
    - escaped_defects: "Bugs found in production"
    - defect_density: "Bugs per story point"
    - rework_rate: "Reopened issues percentage"
    - test_coverage: "Code coverage percentage"

  flow_metrics:
    - wip: "Work in progress count"
    - flow_efficiency: "Active time / total time"
    - cumulative_flow: "Status distribution over time"
    - aging_wip: "Time items spend in each state"

  team_metrics:
    - capacity_utilization: "Actual vs planned hours"
    - focus_factor: "Productive time ratio"
    - team_happiness: "Satisfaction score"
    - predictability: "Commitment vs delivery"
```

### 2. Dashboard Types

**Team Dashboard:**
```yaml
team_dashboard:
  purpose: "Daily team visibility"
  audience: ["developers", "scrum master"]
  refresh: real_time

  widgets:
    - sprint_burndown:
        type: chart
        shows: remaining_work_by_day

    - sprint_board:
        type: kanban
        shows: current_sprint_items

    - blocker_list:
        type: list
        filter: "label:blocked"

    - team_workload:
        type: bar_chart
        shows: issues_per_assignee

    - recent_activity:
        type: feed
        shows: last_24h_updates
```

**Management Dashboard:**
```yaml
management_dashboard:
  purpose: "Sprint/release status"
  audience: ["product owner", "managers"]
  refresh: hourly

  widgets:
    - sprint_progress:
        type: gauge
        shows: percent_complete

    - velocity_trend:
        type: line_chart
        shows: last_6_sprints

    - release_burnup:
        type: chart
        shows: scope_vs_completed

    - risk_register:
        type: list
        shows: open_risks

    - milestone_timeline:
        type: timeline
        shows: upcoming_milestones

    - blockers_summary:
        type: count
        shows: blocked_items_count
```

**Executive Dashboard:**
```yaml
executive_dashboard:
  purpose: "Portfolio health"
  audience: ["executives", "stakeholders"]
  refresh: daily

  widgets:
    - portfolio_status:
        type: status_grid
        shows: all_projects_health

    - delivery_confidence:
        type: gauge
        shows: on_track_percentage

    - resource_allocation:
        type: pie_chart
        shows: team_distribution

    - budget_vs_actual:
        type: bar_chart
        shows: cost_tracking

    - key_milestones:
        type: timeline
        shows: next_90_days

    - risk_heatmap:
        type: matrix
        shows: impact_vs_probability
```

### 3. Tool-Specific Dashboards

**Jira Dashboard:**
```yaml
jira_dashboard:
  gadgets:
    - name: "Sprint Burndown"
      type: "agile-burndown-chart"
      config:
        board: "Team Board"
        sprint: "current"

    - name: "Sprint Health"
      type: "sprint-health-gadget"
      config:
        board: "Team Board"

    - name: "Created vs Resolved"
      type: "two-dimensional-filter-statistics"
      config:
        filter: "project = PROJ"
        x_axis: "created"
        y_axis: "resolved"

    - name: "Pie Chart - Priority"
      type: "pie-chart"
      config:
        filter: "project = PROJ AND status != Done"
        statistic_type: "priority"

    - name: "Filter Results"
      type: "filter-results"
      config:
        filter: "My Open Issues"
        columns: ["Key", "Summary", "Status", "Priority"]
```

**Linear Dashboard Views:**
```yaml
linear_views:
  cycle_view:
    type: board
    group_by: status
    filter: "cycle:current"

  insights:
    built_in:
      - cycle_velocity
      - issue_completion
      - bug_count
      - team_workload

  roadmap:
    type: timeline
    filter: "project:*"
    group_by: project
```

**ClickUp Dashboard:**
```yaml
clickup_dashboard:
  widgets:
    - type: "Sprint Widget"
      shows: current_sprint

    - type: "Workload"
      group_by: assignee
      show_capacity: true

    - type: "Time Tracking"
      shows: logged_vs_estimated

    - type: "Custom Chart"
      chart_type: line
      x_axis: date
      y_axis: completed_tasks

    - type: "Table"
      filter: "status:in progress"
      columns: ["Name", "Assignee", "Due Date"]
```

### 4. Key Performance Indicators

**Scrum KPIs:**
```yaml
scrum_kpis:
  velocity:
    formula: "SUM(story_points) WHERE sprint = X AND status = Done"
    target: "Trending up or stable"
    display: line_chart_last_10_sprints

  sprint_commitment:
    formula: "completed_points / committed_points * 100"
    target: ">= 85%"
    display: gauge

  sprint_goal_achieved:
    formula: "Count where sprint_goal = met"
    target: "100%"
    display: binary_indicator

  escaped_defects:
    formula: "bugs_in_production per sprint"
    target: "< 2"
    display: number_with_trend
```

**Kanban KPIs:**
```yaml
kanban_kpis:
  throughput:
    formula: "COUNT(issues) WHERE completed_date in period"
    target: "Trending up"
    display: bar_chart_weekly

  cycle_time:
    formula: "AVG(completed_date - started_date)"
    target: "< 5 days"
    display: histogram

  wip_compliance:
    formula: "COUNT(issues in_progress) <= WIP_limit"
    target: "100%"
    display: percentage

  flow_efficiency:
    formula: "active_time / (active_time + wait_time) * 100"
    target: "> 40%"
    display: gauge
```

### 5. Automated Reporting

**Scheduled Reports:**
```yaml
automated_reports:
  daily_standup:
    schedule: "09:00 weekdays"
    channel: slack_team_channel
    content:
      - in_progress_items
      - blocked_items
      - completed_yesterday

  weekly_status:
    schedule: "Friday 16:00"
    recipients: [stakeholders@company.com]
    format: email
    content:
      - sprint_progress
      - key_accomplishments
      - upcoming_work
      - risks_and_blockers
      - metrics_snapshot

  sprint_report:
    schedule: "sprint_end"
    format: pdf
    content:
      - sprint_goal_status
      - completed_items
      - incomplete_items
      - velocity
      - burndown_chart
      - retrospective_actions
```

**Slack Integration:**
```yaml
slack_reporting:
  daily_digest:
    time: "09:00"
    channel: "#team-updates"
    template: |
      *Daily Digest - {{ date }}*

      📊 *Sprint Progress:* {{ progress }}%
      ✅ *Completed Yesterday:* {{ completed_count }}
      🚧 *In Progress:* {{ in_progress_count }}
      🚫 *Blocked:* {{ blocked_count }}

      <{{ dashboard_url }}|View Dashboard>

  alert_notifications:
    - trigger: "blocked_item_created"
      channel: "#alerts"
      message: "🚨 Item blocked: {{ issue_title }}"

    - trigger: "milestone_approaching"
      channel: "#releases"
      message: "📅 Milestone {{ milestone_name }} due in 3 days"
```

### 6. Report Templates

**Weekly Status Report:**
```markdown
# Weekly Status Report
**Project:** [Project Name]
**Period:** [Start Date] - [End Date]
**Prepared by:** [Name]

## Executive Summary
[1-2 sentence summary of project health]

## Overall Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Key Accomplishments
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

## Metrics
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Sprint Velocity | 40 pts | 38 pts | → |
| Bug Count | < 5 | 3 | ↓ |
| Cycle Time | 4 days | 3.5 days | ↓ |

## Risks & Issues
| # | Description | Impact | Mitigation | Status |
|---|-------------|--------|------------|--------|
| 1 | [Risk] | High | [Action] | Open |

## Next Week's Focus
- [Priority 1]
- [Priority 2]

## Decisions Needed
- [Decision 1 - Owner - By Date]

## Appendix
- [Link to dashboard]
- [Link to detailed metrics]
```

**Sprint Report:**
```markdown
# Sprint [N] Report

## Sprint Overview
| Attribute | Value |
|-----------|-------|
| Sprint Goal | [Goal] |
| Duration | [Start] - [End] |
| Team Size | [N] |

## Goal Achievement: ✅ Met / ⚠️ Partial / ❌ Not Met

## Delivery Summary
| Metric | Committed | Completed | Delta |
|--------|-----------|-----------|-------|
| Stories | 8 | 7 | -1 |
| Points | 34 | 31 | -3 |
| Bugs Fixed | 5 | 6 | +1 |

## Burndown Chart
[Chart Image]

## Completed Items
| Key | Title | Points | Type |
|-----|-------|--------|------|
| #123 | Story A | 5 | Feature |
| #124 | Story B | 3 | Feature |

## Incomplete Items
| Key | Title | Points | Reason |
|-----|-------|--------|--------|
| #130 | Story X | 3 | Blocked by API |

## Velocity Trend
[Chart: Last 6 sprints]

## Quality Metrics
- Bugs Found: [N]
- Bugs Fixed: [N]
- Escaped Defects: [N]
- Test Coverage: [N]%

## Retrospective Highlights
**Continue:** [Item]
**Stop:** [Item]
**Start:** [Item]

## Action Items
| Action | Owner | Status |
|--------|-------|--------|
| [Action] | @name | ⏳ |
```

### 7. Dashboard Design Principles

**Information Hierarchy:**
```
Level 1: Overall Health (traffic light)
├── Level 2: Key Metrics (numbers)
│   ├── Level 3: Trend Charts (graphs)
│   │   └── Level 4: Detailed Data (tables)
```

**Color Coding:**
```yaml
status_colors:
  green: "On track, no issues"
  yellow: "At risk, needs attention"
  red: "Off track, requires escalation"
  blue: "Information, neutral"
  gray: "Not started, N/A"
```

**Widget Layout:**
```
+------------------+------------------+
|   Main Metric    |  Secondary       |
|   (Large)        |  Metric          |
+------------------+------------------+
|                                     |
|   Primary Chart                     |
|   (Wide, important trend)           |
|                                     |
+------------------+------------------+
| Quick Stats | Quick Stats | Quick   |
| (Small)     | (Small)     | Stats   |
+------------------+------------------+
|                                     |
|   Detailed Table (scrollable)       |
|                                     |
+-------------------------------------+
```

## Best Practices

### Dashboard Design
1. **Less is more** - Focus on actionable metrics
2. **Context matters** - Include targets and trends
3. **Update automatically** - Real-time when possible
4. **Mobile-friendly** - Accessible anywhere
5. **Consistent layout** - Familiar patterns

### Metric Selection
1. **Align with goals** - Measure what matters
2. **Balance lagging/leading** - Past and predictive
3. **Avoid vanity metrics** - Must drive decisions
4. **Limit to 5-7 key metrics** - Prevent overload

### Reporting
1. **Know your audience** - Tailor detail level
2. **Lead with insights** - Not just data
3. **Include actions** - What to do next
4. **Regular cadence** - Build trust through consistency

### Continuous Improvement
1. **Review effectiveness** - Are dashboards used?
2. **Gather feedback** - Ask stakeholders
3. **Iterate design** - Improve based on usage
4. **Archive old dashboards** - Keep system clean

## Templates/Examples

### Portfolio Dashboard Config

```yaml
portfolio_dashboard:
  title: "Engineering Portfolio"
  refresh: 15_minutes

  row_1:
    - widget: status_overview
      width: 4
      config:
        projects: all
        show: health_status

    - widget: delivery_confidence
      width: 4
      config:
        metric: on_time_percentage
        target: 90

    - widget: resource_utilization
      width: 4
      config:
        show: percentage

  row_2:
    - widget: burnup_chart
      width: 8
      config:
        scope: quarterly_roadmap
        show_scope_changes: true

    - widget: risk_summary
      width: 4
      config:
        show: top_5_risks
        sort_by: impact

  row_3:
    - widget: project_table
      width: 12
      columns:
        - name
        - status
        - progress
        - owner
        - due_date
        - risk_level
```

### Jira JQL Queries for Dashboards

```sql
-- Sprint Scope (current sprint)
project = PROJ AND sprint in openSprints()

-- Completed This Sprint
project = PROJ AND sprint in openSprints() AND status = Done

-- In Progress
project = PROJ AND status = "In Progress"

-- Blocked Items
project = PROJ AND labels = blocked AND status != Done

-- Bugs by Priority (pie chart)
project = PROJ AND type = Bug AND status != Done

-- Created vs Resolved (2D filter)
project = PROJ AND created >= -30d

-- Velocity Data (custom field)
project = PROJ AND sprint in closedSprints() AND status = Done
-- Group by sprint, sum story points

-- Aging Issues
project = PROJ AND status = "In Progress" AND updated < -7d

-- Release Scope
project = PROJ AND fixVersion = "1.0.0"
```

### PowerBI Connection

```python
# Connect PM tool to PowerBI
import requests
import pandas as pd

def fetch_jira_data(jql_query):
    """Fetch Jira data for PowerBI"""
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Authorization": f"Bearer {JIRA_TOKEN}"}
    params = {
        "jql": jql_query,
        "fields": "summary,status,priority,customfield_10026",  # story points
        "maxResults": 1000
    }

    response = requests.get(url, headers=headers, params=params)
    issues = response.json()["issues"]

    return pd.DataFrame([{
        "key": i["key"],
        "summary": i["fields"]["summary"],
        "status": i["fields"]["status"]["name"],
        "priority": i["fields"]["priority"]["name"],
        "story_points": i["fields"].get("customfield_10026", 0)
    } for i in issues])

# Example: Velocity trend
velocity_data = fetch_jira_data(
    "project = PROJ AND sprint in closedSprints() AND status = Done"
)
```

## References

- [Jira Dashboards](https://support.atlassian.com/jira-software-cloud/docs/create-and-customize-a-dashboard/)
- [Linear Insights](https://linear.app/docs/insights)
- [Scrum Metrics](https://www.scrum.org/resources/blog/agile-metrics)
- [Kanban Metrics](https://www.kanbanize.com/kanban-resources/kanban-analytics)
- [Information Dashboard Design (Stephen Few)](https://www.perceptualedge.com/library.php)
