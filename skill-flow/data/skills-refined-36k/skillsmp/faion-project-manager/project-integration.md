---
id: project-integration
name: "Project Integration Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Project Integration Management

## Metadata
- **Category:** Project Management Framework 7 - Development Approach Domain
- **Difficulty:** Advanced
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 8 min
- **Agent:** faion-pm-agent

---

## Problem

Projects fail from lack of integration:
- Decisions in one area break another
- No single view of project health
- Conflicting priorities between teams
- Knowledge silos prevent optimization

## Framework

### Integration Role

The PM as integrator coordinates across all knowledge areas:

```
Scope ←→ Schedule ←→ Cost
   ↖       ↑        ↗
    ↘   INTEGRATION  ↙
   ↗       ↓        ↖
Risk ←→ Quality ←→ Resources
```

### Integration Activities

| Activity | Description | Timing |
|----------|-------------|--------|
| **Project Charter** | Authorize project, define high-level | Initiation |
| **Project Plan** | Integrate all subsidiary plans | Planning |
| **Direct Work** | Lead and manage execution | Execution |
| **Monitor/Control** | Track and adjust | Monitoring |
| **Change Control** | Evaluate and integrate changes | Throughout |
| **Close Project** | Final acceptance, lessons learned | Closure |

### Step 1: Create Project Charter

Establish project authorization:

**Charter Elements:**
- Project purpose and objectives
- High-level requirements
- Success criteria
- Key stakeholders
- PM authority level
- Budget and timeline (high-level)

### Step 2: Develop Project Plan

Integrate all component plans:

| Component Plan | Content |
|----------------|---------|
| Scope Plan | What's included/excluded |
| Schedule Plan | Timeline, milestones |
| Cost Plan | Budget, tracking |
| Quality Plan | Standards, metrics |
| Resource Plan | Team, equipment |
| Risk Plan | Risk register, responses |
| Communications Plan | Who, what, when |
| Procurement Plan | External purchases |

### Step 3: Integrated Change Control

When changes occur:
1. Assess impact across ALL areas
2. Update affected plans
3. Re-baseline if necessary
4. Communicate changes

---

## Templates

### Project Charter

```markdown
## Project Charter

### Project Information
| Field | Value |
|-------|-------|
| Project Name | [Name] |
| Project Manager | [Name] |
| Sponsor | [Name] |
| Date | [Date] |

### Business Case
[Why this project exists, problem it solves, benefits]

### Objectives
1. [SMART objective 1]
2. [SMART objective 2]
3. [SMART objective 3]

### Scope (High-Level)
**In Scope:**
- [Major deliverable 1]
- [Major deliverable 2]

**Out of Scope:**
- [Exclusion 1]
- [Exclusion 2]

### Success Criteria
| Criterion | Measure | Target |
|-----------|---------|--------|
| On time | Delivery date | [Date] |
| On budget | Total cost | [Amount] |
| Quality | Defect rate | < [X]% |
| Satisfaction | NPS | > [Score] |

### Key Stakeholders
| Stakeholder | Role | Involvement |
|-------------|------|-------------|
| [Name] | Sponsor | Approve budget, major decisions |
| [Name] | Product Owner | Requirements, acceptance |
| [Name] | Tech Lead | Architecture, technical decisions |

### Constraints
- Budget: $[Amount]
- Timeline: [Duration]
- Resources: [Team size]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Risks (High-Level)
- [Major risk 1]
- [Major risk 2]

### Approval
| Name | Role | Signature | Date |
|------|------|-----------|------|
| [Name] | Sponsor | _________ | _____ |
| [Name] | PM | _________ | _____ |
```

### Project Status Report

```markdown
## Project Status Report - [Date]

### Overall Status: [GREEN/YELLOW/RED]

| Dimension | Status | Trend | Notes |
|-----------|--------|-------|-------|
| Schedule | GREEN | → | On track |
| Budget | YELLOW | ↘ | 5% over, mitigation in progress |
| Scope | GREEN | → | No changes |
| Quality | GREEN | ↗ | Improving |
| Risk | YELLOW | → | 2 high risks being managed |
| Team | GREEN | → | Fully staffed |

### Accomplishments This Period
- [Accomplishment 1]
- [Accomplishment 2]

### Planned Next Period
- [Plan 1]
- [Plan 2]

### Issues Needing Attention
| Issue | Impact | Action | Owner | Due |
|-------|--------|--------|-------|-----|
| [Issue 1] | [Impact] | [Action] | [Name] | [Date] |

### Key Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Velocity | 40 points | 38 points |
| Defects | < 5 | 3 |
| Burndown | 50% | 48% |
```

---

## Examples

### Example 1: Integration Decision

**Situation:** New feature requested, adds 2 weeks to schedule.

**Integration Analysis:**
| Area | Impact |
|------|--------|
| Scope | +1 major feature |
| Schedule | +2 weeks delay |
| Cost | +$8,000 development |
| Quality | Needs testing time |
| Risk | Dependencies on third-party API |
| Resources | Team has capacity |

**Decision:** Approve with trade-off - remove lower priority feature to maintain timeline.

### Example 2: Solopreneur Integration

For solopreneurs, integration = keeping everything aligned:

```markdown
## Weekly Integration Check

### What I'm Working On
- [ ] Project A: On track?
- [ ] Project B: On track?
- [ ] Marketing: Consistent?
- [ ] Admin: Caught up?

### Cross-Project Dependencies
- Does Project A delay affect Project B?
- Am I over-committed this week?
- Any scope creep sneaking in?

### Decisions Needed
- [Decision 1]: Affects [areas]
- [Decision 2]: Affects [areas]

### Adjustments
- [Adjustment needed]
- [Trade-off to make]
```

---

## Common Mistakes

1. **Silo management** - Optimize parts, sub-optimize whole
2. **No single source of truth** - Multiple conflicting plans
3. **Change without integration** - Scope changes without schedule update
4. **Missing charter** - No formal authorization
5. **Status reports without action** - Reports that no one reads/acts on

---

## Related Methodologies

- **Change Control:** Managing integrated changes
- **Stakeholder Engagement:** Stakeholder communication
- **Solution Evaluation:** BA solution assessment

---

*Methodology from Project Management Framework 7 - Development Approach Performance Domain*
