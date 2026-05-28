---
name: devflow-planning
description: AI-powered sprint planning, velocity analysis, and capacity forecasting. Use for planning sprints, predicting outcomes, and providing agile recommendations based on historical data.
license: MIT
compatibility: Requires mcp-jira with configured Jira instance
metadata:
  author: ximplicity
  version: "1.0"
  category: planning
---

# DevFlow Planning Skill

Sprint planning, velocity analysis, and predictive analytics for agile teams.

## Allowed Operations

- Analyze sprint velocity and trends
- Generate capacity forecasts
- Predict sprint success probability
- Recommend optimal sprint load
- Identify spillover risks
- Cross-project dependency mapping
- Generate documentation from issues
- Compile release notes

## Forbidden Operations

These require explicit user approval:

- Auto-commit sprint changes
- Modify issue estimates without review
- Move issues to sprints automatically
- Create issues from predictions

## Sprint Planning Workflow

```
1. Analyze velocity → Get historical data
2. Calculate capacity → Team availability
3. Recommend load → Based on trends
4. Assess risks → Per-issue spillover
5. Validate plan → Sprint success prediction
```

## Quick Velocity Reference

| Metric | Description | Use For |
|--------|-------------|---------|
| Avg Velocity | Points completed per sprint | Baseline planning |
| Trend Direction | Increasing/Stable/Decreasing | Adjust forecasts |
| Completion Rate | Done vs Committed ratio | Risk assessment |
| Variance | Sprint-to-sprint deviation | Confidence levels |

For complete velocity patterns, see [VELOCITY-PATTERNS.md](references/VELOCITY-PATTERNS.md).

## Quick Capacity Reference

```
Team Capacity = Sum(member availability × sprint days)
Recommended Load = Avg Velocity × (1 - Buffer%)

Buffer Guidelines:
- Stable team: 10%
- New members: 20%
- High uncertainty: 30%
```

For sprint planning details, see [SPRINT-PLANNING-GUIDE.md](references/SPRINT-PLANNING-GUIDE.md).

## Proactive Recommendations

| Context | Trigger | Action |
|---------|---------|--------|
| Sprint >80% filled | Overcommit risk | Suggest scope reduction |
| Velocity declining 3+ sprints | Trend alert | Recommend retrospective focus |
| Issue blocked >2 days | Dependency risk | Escalate blocker |
| Unestimated work in sprint | Planning gap | Flag for refinement |
| Branch stale >5 days | GitFlow alert | Review or close |

## GitFlow Integration

When planning work:

1. Feature branches from `develop`
2. Naming: `feature/<issue-key>-<description>`
3. One issue = one branch
4. Complete sprint items before merge

For GitFlow details, see [GITFLOW-RECOMMENDATIONS.md](references/GITFLOW-RECOMMENDATIONS.md).

## Scrum Constraints

- Stories must have acceptance criteria
- Epics should have child estimates
- Sprint goals align with epic objectives
- Retrospective actions tracked

For Scrum patterns, see [SCRUM-BEST-PRACTICES.md](references/SCRUM-BEST-PRACTICES.md).

## Example Usage

```
Analyze velocity for project PROJ over last 5 sprints
Plan next sprint with 80% capacity buffer
Show spillover risks for current sprint items
Predict success rate for proposed sprint scope
Map dependencies between PROJ and INFRA projects
```
