# Sprint Plan Template

**Document ID:** P4-SPRINT-{XXX}  
**Sprint Number:** {X}  
**Sprint Duration:** {Start Date} - {End Date}  
**Author:** {Scrum Master / Tech Lead}  
**Traceability:** Links to P4-WBS-{XXX}

---

## 1. Sprint Overview

### 1.1 Sprint Goal
{One clear sentence describing what the sprint will achieve}

### 1.2 Sprint Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Sprint Duration | {X} weeks | |
| Team Capacity | {X} story points | Based on velocity |
| Committed Points | {X} story points | |
| Buffer | {X}% | For unknowns |

---

## 2. Sprint Backlog

### 2.1 User Stories

| ID | Story | Priority | Points | Assignee | Status |
|----|-------|----------|--------|----------|--------|
| US-001 | As a {user}, I want {feature} so that {benefit} | Must | {X} | {Name} | ⬜ To Do |
| US-002 | As a {user}, I want {feature} so that {benefit} | Must | {X} | {Name} | ⬜ To Do |
| US-003 | As a {user}, I want {feature} so that {benefit} | Should | {X} | {Name} | ⬜ To Do |
| US-004 | As a {user}, I want {feature} so that {benefit} | Could | {X} | {Name} | ⬜ To Do |

**Status Legend:**
- ⬜ To Do
- 🔄 In Progress
- 👀 In Review
-  Done
-  Blocked

### 2.2 Technical Tasks

| ID | Task | Story | Hours | Assignee | Status |
|----|------|-------|-------|----------|--------|
| TK-001 | {Task description} | US-001 | {X} | {Name} | ⬜ |
| TK-002 | {Task description} | US-001 | {X} | {Name} | ⬜ |
| TK-003 | {Task description} | US-002 | {X} | {Name} | ⬜ |

### 2.3 Bug Fixes

| ID | Bug | Severity | Hours | Assignee | Status |
|----|-----|----------|-------|----------|--------|
| BUG-001 | {Bug description} | Critical | {X} | {Name} | ⬜ |

### 2.4 Technical Debt

| ID | Debt Item | Justification | Hours | Assignee | Status |
|----|-----------|---------------|-------|----------|--------|
| TD-001 | {Technical debt item} | {Why now} | {X} | {Name} | ⬜ |

---

## 3. Capacity Planning

### 3.1 Team Capacity

| Team Member | Role | Available Days | Capacity (Hours) | Allocated |
|-------------|------|----------------|------------------|-----------|
| {Name} | Senior Dev | {X} | {Y} | {Z} |
| {Name} | Developer | {X} | {Y} | {Z} |
| {Name} | Developer | {X} | {Y} | {Z} |
| {Name} | QA Engineer | {X} | {Y} | {Z} |
| **Total** | | | **{Y}** | **{Z}** |

### 3.2 Planned Absences

| Team Member | Dates | Reason | Impact |
|-------------|-------|--------|--------|
| {Name} | {Dates} | PTO | {X} hours |

---

## 4. Definition of Done

### 4.1 Story Level DoD

- [ ] Code complete and follows coding standards
- [ ] Unit tests written with >80% coverage
- [ ] Code reviewed and approved by peer
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Security scan passed (no critical/high)
- [ ] Deployed to staging environment
- [ ] QA sign-off received
- [ ] Product Owner acceptance

### 4.2 Sprint Level DoD

- [ ] All committed stories meet Story DoD
- [ ] Sprint demo completed
- [ ] Release notes updated
- [ ] Technical documentation current
- [ ] No critical bugs open
- [ ] Retrospective conducted

---

## 5. Dependencies

### 5.1 Internal Dependencies

| Story | Depends On | Owner | Status |
|-------|------------|-------|--------|
| US-002 | US-001 API complete | Team | ⬜ |

### 5.2 External Dependencies

| Dependency | Owner | Due Date | Status | Risk |
|------------|-------|----------|--------|------|
| {External system API} | {Team} | {Date} | ⬜ | Medium |

---

## 6. Risks and Mitigations

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| {Risk description} | H/M/L | H/M/L | {Strategy} | {Name} |

---

## 7. Sprint Events

| Event | Date/Time | Duration | Participants |
|-------|-----------|----------|--------------|
| Sprint Planning | {DateTime} | 2 hours | Full team |
| Daily Standup | {Time} daily | 15 min | Dev team |
| Backlog Refinement | {DateTime} | 1 hour | Full team |
| Sprint Review | {DateTime} | 1 hour | Team + Stakeholders |
| Sprint Retrospective | {DateTime} | 1 hour | Full team |

---

## 8. Sprint Burndown

### 8.1 Ideal vs Actual

| Day | Ideal Remaining | Actual Remaining | Notes |
|-----|-----------------|------------------|-------|
| Day 1 | {X} | {Y} | Sprint start |
| Day 2 | {X} | {Y} | |
| Day 3 | {X} | {Y} | |
| ... | ... | ... | |
| Day 10 | 0 | {Y} | Sprint end |

### 8.2 Burndown Chart

```
Points
  ^
40|*
35|  *
30|    *
25|      *  Ideal
20|        *--------
15|          *     Actual
10|            *
 5|              *
 0+--+--+--+--+--+--+--+--+--+--+-> Days
   1  2  3  4  5  6  7  8  9 10
```

---

## 9. Sprint Commitment

### Team Commitment

We, the development team, commit to delivering the sprint goal by completing all "Must Have" stories and making best effort on "Should Have" items.

| Role | Name | Commitment Signature |
|------|------|---------------------|
| Tech Lead | | |
| Senior Developer | | |
| Developer | | |
| QA Engineer | | |

**Sprint Planning Date:** {Date}

---

## 10. Sprint Outcome (Post-Sprint)

*To be filled after sprint completion*

### 10.1 Velocity

| Metric | Planned | Actual |
|--------|---------|--------|
| Story Points | {X} | {Y} |
| Stories Completed | {X} | {Y} |
| Bugs Fixed | {X} | {Y} |

### 10.2 Carryover

| ID | Story/Task | Reason | Next Sprint |
|----|------------|--------|-------------|
| US-004 | {Story} | {Reason} | Sprint {N+1} |

### 10.3 Retrospective Actions

| Action | Owner | Due Date |
|--------|-------|----------|
| {Action item} | {Name} | {Date} |

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
