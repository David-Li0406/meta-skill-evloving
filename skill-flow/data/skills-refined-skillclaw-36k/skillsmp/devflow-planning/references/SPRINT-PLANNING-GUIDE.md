# Sprint Planning Guide

Comprehensive guide for AI-assisted sprint planning with capacity calculations and load recommendations.

## Planning Phases

### Phase 1: Velocity Analysis

Before planning, analyze recent sprint performance:

```
Required Data:
- Last 3-5 closed sprints
- Story points completed per sprint
- Completion rates (done vs committed)
```

### Phase 2: Capacity Calculation

Calculate team capacity for upcoming sprint:

```
Team Capacity Formula:
Capacity = Σ(member_days × availability_factor)

Example:
- Dev A: 10 days × 0.8 = 8 effective days
- Dev B: 10 days × 1.0 = 10 effective days
- Dev C: 10 days × 0.5 = 5 effective days (part-time)
Total: 23 effective person-days
```

### Phase 3: Load Recommendation

```
Recommended Load = Average Velocity × Confidence Factor

Confidence Factors:
| Velocity Trend | Team Stability | Factor |
|----------------|----------------|--------|
| Increasing     | Stable         | 1.0    |
| Stable         | Stable         | 0.95   |
| Stable         | Some changes   | 0.85   |
| Decreasing     | Stable         | 0.80   |
| Decreasing     | Changes        | 0.70   |
```

### Phase 4: Risk Assessment

Evaluate each candidate issue:

| Risk Factor | Weight | Description |
|-------------|--------|-------------|
| Size (>8 pts) | High | Large items have higher variance |
| Dependencies | High | Blocked items may spill |
| Complexity | Medium | Unknown tech = risk |
| Assignee load | Medium | Overloaded = risk |
| Previous spillover | High | Repeat offenders |

## Capacity Templates

### Standard Sprint (2 weeks)

```
Team Size: 5 developers
Sprint Days: 10
Meetings overhead: 15%
Effective Days: 10 × 0.85 = 8.5 days/person
Total Capacity: 42.5 person-days
```

### High-Ceremony Sprint

```
Team Size: 5 developers
Sprint Days: 10
Meetings overhead: 25% (demos, planning, retro)
Effective Days: 10 × 0.75 = 7.5 days/person
Total Capacity: 37.5 person-days
```

## Sprint Load Targets

| Load Level | Percentage | When to Use |
|------------|------------|-------------|
| Conservative | 70% | New team, high uncertainty |
| Standard | 80% | Stable team, known work |
| Aggressive | 90% | Experienced team, clear scope |
| Full | 100% | Never recommended |

## Spillover Prevention

### Warning Signs

1. **Issue blocked >2 days**: Escalate dependency
2. **No progress in 3 days**: Check for obstacles
3. **Scope creep detected**: Raise with PO
4. **>50% work not started mid-sprint**: Re-assess

### Intervention Actions

```
Day 1-3:  Monitor and remove blockers
Day 4-6:  Escalate risks, adjust assignments
Day 7-8:  Consider scope reduction
Day 9-10: Focus on completing started work
```

## Planning Checklist

Before sprint starts:

- [ ] All stories have acceptance criteria
- [ ] All stories are estimated
- [ ] Dependencies identified and tracked
- [ ] Team capacity calculated
- [ ] Sprint goal defined
- [ ] Load within recommended range

## Example Sprint Plan

```
Project: WEBAPP
Sprint: Sprint 23
Duration: Jan 6 - Jan 17 (10 days)

Capacity Analysis:
- Team velocity (last 3): 42, 38, 45 → Avg: 41.7
- Trend: Stable
- Team: No changes
- Confidence factor: 0.95

Recommended Load: 41.7 × 0.95 = 39.6 points

Proposed Scope:
- WEBAPP-101 (8 pts) - Feature A
- WEBAPP-102 (5 pts) - Feature B
- WEBAPP-103 (3 pts) - Bug fix
- WEBAPP-104 (8 pts) - Feature C
- WEBAPP-105 (5 pts) - Refactor
- WEBAPP-106 (8 pts) - Feature D
Total: 37 points (93% of recommended)

Risk Assessment:
- WEBAPP-101: Depends on INFRA-55 (Medium risk)
- WEBAPP-104: New technology (Medium risk)
- Others: Low risk

Sprint Goal:
"Complete Feature A-D for Q1 release"
```

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Stuffing | >100% load | Use recommended max |
| No buffer | 0% contingency | Keep 10-20% buffer |
| Carry-over | Repeat spillovers | Address root causes |
| Estimate gaming | Inflated points | Calibrate with team |
