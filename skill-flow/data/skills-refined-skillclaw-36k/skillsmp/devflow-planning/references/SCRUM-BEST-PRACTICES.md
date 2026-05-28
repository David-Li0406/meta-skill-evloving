# Scrum Best Practices

Scrum ceremonies, anti-patterns, and team health indicators for AI-assisted planning.

## Ceremony Guidelines

### Sprint Planning

| Aspect | Best Practice |
|--------|---------------|
| Duration | 2 hrs per sprint week (4 hrs for 2-week sprint) |
| Attendees | PO, Scrum Master, Dev Team |
| Output | Sprint Goal, Sprint Backlog |
| Prep | Backlog refined, stories estimated |

### Daily Standup

| Aspect | Best Practice |
|--------|---------------|
| Duration | 15 minutes max |
| Time | Same time daily, near board |
| Focus | Yesterday, Today, Blockers |
| Anti-pattern | Status reports to manager |

### Sprint Review

| Aspect | Best Practice |
|--------|---------------|
| Duration | 1 hr per sprint week |
| Attendees | Team + stakeholders |
| Focus | Demo working software |
| Output | Feedback, backlog updates |

### Retrospective

| Aspect | Best Practice |
|--------|---------------|
| Duration | 45 min per sprint week |
| Attendees | Scrum Team only |
| Focus | What worked, what didn't, actions |
| Output | 2-3 actionable improvements |

## Story Quality Checklist

### Definition of Ready

- [ ] Acceptance criteria defined
- [ ] Story points estimated
- [ ] Dependencies identified
- [ ] Technical approach discussed
- [ ] Fits in one sprint

### Definition of Done

- [ ] Code complete and reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO accepted

## Anti-Patterns to Detect

### Planning Anti-Patterns

| Pattern | Symptoms | Impact |
|---------|----------|--------|
| Stuffing | >100% capacity planned | Spillover |
| Sandbagging | Very low commitments | Wasted capacity |
| No Goal | Missing sprint goal | Lack of focus |
| Scope Creep | Mid-sprint additions | Unpredictability |

### Execution Anti-Patterns

| Pattern | Symptoms | Impact |
|---------|----------|--------|
| Cherry Picking | Only fun tasks done | Stalled stories |
| Late Integration | End-sprint merge rush | Quality issues |
| Silent Blockers | Unreported impediments | Delays |
| Hero Culture | One person does all | Bus factor risk |

### Team Anti-Patterns

| Pattern | Symptoms | Impact |
|---------|----------|--------|
| Seagull Manager | Fly-by decisions | Demotivation |
| Absent PO | No feedback | Wrong features |
| Fake Scrum | Ceremonies without purpose | Waste |
| Metric Gaming | Inflated points | Lost visibility |

## Team Health Indicators

### Positive Signs

```
- Consistent velocity (CV <20%)
- High completion rate (>90%)
- Short time to merge PRs (<1 day)
- Active retrospective actions
- Team self-organization
```

### Warning Signs

```
- Declining velocity (3+ sprints)
- Increasing spillover
- Stale in-progress items (>5 days)
- No retrospective changes
- Heavy dependency on individuals
```

## Velocity Expectations

### New Team

| Sprint | Expected | Notes |
|--------|----------|-------|
| 1-2 | Low, variable | Finding rhythm |
| 3-4 | Increasing | Process settling |
| 5+ | Stabilizing | Baseline forming |

### Established Team

| Scenario | Impact | Duration |
|----------|--------|----------|
| New member | -10-20% | 2-3 sprints |
| Member leaves | -15-25% | 2-3 sprints |
| Tech change | -10-20% | 2-4 sprints |
| Process change | ±10% | 1-2 sprints |

## Estimation Guidance

### Story Point Scale

| Points | Complexity | Typical Duration |
|--------|------------|------------------|
| 1 | Trivial | Hours |
| 2 | Simple | 1 day |
| 3 | Moderate | 1-2 days |
| 5 | Complex | 2-3 days |
| 8 | Very complex | 3-5 days |
| 13 | Epic-level | Should be split |

### Estimation Rules

```
1. Estimate relative complexity, not time
2. Compare to reference stories
3. Include testing and review time
4. Whole team participates
5. Discuss disagreements
```

## Sprint Success Criteria

### Healthy Sprint

- Goal achieved
- 90%+ items completed
- No critical bugs introduced
- Team morale maintained
- Stakeholders satisfied

### Sprint Recovery

If mid-sprint issues:

```
1. Identify root cause
2. Remove blockers immediately
3. Consider scope reduction
4. Focus on sprint goal
5. Document lessons learned
```

## Continuous Improvement

### Retrospective Actions

| Type | Example | Track |
|------|---------|-------|
| Quick Win | Fix flaky test | Next sprint |
| Process | Improve PR reviews | 2 sprints |
| Technical | Reduce build time | Quarterly |
| Cultural | Better estimation | Ongoing |

### Metrics to Track

```
Sprint-level:
- Velocity (points completed)
- Completion rate
- Spillover items
- Bugs introduced

Team-level:
- Velocity trend (3+ sprints)
- Lead time (idea to production)
- Cycle time (start to done)
- Team satisfaction
```
