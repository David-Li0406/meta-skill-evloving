---
id: agile-hybrid-approaches
name: "Agile and Hybrid Approaches"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Agile and Hybrid Approaches

## Metadata
- **Category:** Project Management Framework 7 - Development Approach Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 9 min
- **Agent:** faion-pm-agent

---

## Problem

Not all projects fit one approach:
- Pure waterfall too rigid for uncertainty
- Pure agile challenging for fixed-scope contracts
- Teams struggle with "right" methodology
- Stakeholders expect different things

## Framework

### Approach Spectrum

```
Predictive ←————————————→ Adaptive
(Waterfall)              (Agile)
     ↓                      ↓
Requirements             Requirements
fixed early              evolve
     ↓                      ↓
Sequential               Iterative
phases                   sprints
     ↓                      ↓
Big bang                 Incremental
delivery                 delivery
```

### When to Use Each

| Factor | Predictive | Agile | Hybrid |
|--------|------------|-------|--------|
| Requirements | Clear, stable | Evolving, unclear | Partially known |
| Stakeholders | Formal, scheduled | Highly engaged | Mixed availability |
| Team | Less experienced | Self-organizing | Mixed experience |
| Risk | Low, well-understood | High, experimental | Moderate |
| Delivery | Big bang acceptable | Frequent preferred | Phased |
| Contracts | Fixed price | T&M, value-based | Mixed |

### Hybrid Approaches

Combine elements from both worlds:

**Option 1: Water-Scrum-Fall**
```
Plan (Waterfall) → Build (Scrum) → Deploy (Waterfall)
```

**Option 2: Agile Development + Predictive Governance**
```
Sprints for work + Phase gates for funding/approval
```

**Option 3: Predictive Core + Agile Discovery**
```
Agile discovery phase → Waterfall implementation
```

---

## Key Agile Practices

### Scrum Framework

```
Product Backlog → Sprint Backlog → Sprint → Increment
      ↑                              ↓
      ←——— Sprint Review ←——— Sprint Retrospective
```

**Scrum Events:**
| Event | Duration | Purpose |
|-------|----------|---------|
| Sprint Planning | 2-4 hours | Plan sprint work |
| Daily Scrum | 15 minutes | Sync, blockers |
| Sprint Review | 1-2 hours | Demo, feedback |
| Sprint Retrospective | 1-2 hours | Improve process |

**Scrum Roles:**
| Role | Responsibility |
|------|----------------|
| Product Owner | What to build, priority |
| Scrum Master | Process, impediments |
| Developers | How to build, delivery |

### Kanban Practices

```
Backlog → In Progress → Review → Done
           (WIP: 3)    (WIP: 2)
```

**Kanban Principles:**
1. Visualize workflow
2. Limit work in progress (WIP)
3. Manage flow
4. Make policies explicit
5. Continuous improvement

---

## Templates

### Sprint Planning Template

```markdown
## Sprint [N] Planning

**Sprint Goal:** [One sentence describing the objective]

**Duration:** [Start date] - [End date] (2 weeks)

### Capacity
| Team Member | Days Available | Commitment |
|-------------|----------------|------------|
| Alice | 9 | 80% |
| Bob | 10 | 100% |
| Carol | 8 | 100% |
| **Total** | **27 days** | **~20 points** |

### Sprint Backlog
| Story | Points | Owner | Priority |
|-------|--------|-------|----------|
| US-101: User login | 5 | Alice | P1 |
| US-102: Dashboard | 8 | Bob | P1 |
| US-103: Settings | 3 | Carol | P2 |
| BUG-45: Fix timeout | 2 | Alice | P1 |
| **Total** | **18** | | |

### Dependencies
- US-102 needs design from UX (ready by Wed)
- US-101 needs API endpoint from backend (done)

### Risks
- Alice on vacation last 2 days
- Third-party API might have changes
```

### Kanban Board Template

```markdown
## Kanban Board

### Backlog (No Limit)
- [ ] Feature A
- [ ] Feature B
- [ ] Feature C
- [ ] Bug fix X

### Ready (WIP: 5)
- [ ] Feature D (assigned to Alice)
- [ ] Feature E (assigned to Bob)

### In Progress (WIP: 3)
- [>] Feature F - Alice (2 days)
- [>] Bug Y - Carol (1 day)

### Review (WIP: 2)
- [?] Feature G - waiting for Bob review

### Done
- [x] Feature H - shipped Jan 15
- [x] Feature I - shipped Jan 14
```

---

## Examples

### Example 1: Hybrid for Fixed-Price Contract

**Situation:** Fixed-price contract, $100K, 4 months, scope somewhat defined.

**Approach:**
```
Phase 1: Discovery (2 weeks) - Agile
- User story workshops
- Prototype key screens
- Finalize scope

Phase 2: Development (10 weeks) - Scrum
- 5 two-week sprints
- Weekly demos to client
- Backlog refinement

Phase 3: Deployment (2 weeks) - Predictive
- Fixed test plan
- Staged rollout
- Documentation
```

**Governance:**
- Monthly steering committee (predictive)
- Weekly sprint reviews (agile)
- Change requests for scope changes (predictive)

### Example 2: Solopreneur Agile

```markdown
## Personal Kanban

### This Week's Focus (WIP: 3)
1. [>] Write blog post
2. [>] Update landing page
3. [>] Customer call

### Waiting
- [ ] Design review from contractor
- [ ] API access from partner

### Done This Week
- [x] Email newsletter sent
- [x] Invoice sent to client A

### Weekly Review (Sunday)
- What got done?
- What's stuck?
- What's priority next week?
```

---

## Choosing Your Approach

### Decision Framework

```markdown
## Approach Selection Checklist

Answer for your project:

1. How clear are the requirements?
   [ ] Very clear (Predictive)
   [ ] Somewhat clear (Hybrid)
   [ ] Unclear, evolving (Agile)

2. How available is the customer/stakeholder?
   [ ] Limited access (Predictive)
   [ ] Regular meetings (Hybrid)
   [ ] Highly engaged (Agile)

3. What's the risk tolerance?
   [ ] Low - must work first time (Predictive)
   [ ] Medium (Hybrid)
   [ ] High - can experiment (Agile)

4. How is the team experienced?
   [ ] Less experienced (Predictive)
   [ ] Mixed (Hybrid)
   [ ] Self-organizing (Agile)

5. Contract type?
   [ ] Fixed price, fixed scope (Predictive)
   [ ] Fixed price, flexible scope (Hybrid)
   [ ] Time & materials (Agile)
```

---

## Common Mistakes

1. **Dogmatic adherence** - "We MUST do pure Scrum"
2. **Agile in name only** - Waterfall with daily standups
3. **No adaptation** - Same approach for all projects
4. **Missing foundation** - Agile without backlog grooming
5. **Tool over principle** - Focus on Jira, not collaboration

---

## Related Methodologies

- **Project Integration:** Integrating project components
- **Work Breakdown Structure:** Decomposing work into packages
- **Jira Workflow Management:** PM tool workflows

---

*Methodology from Project Management Framework 7 - Development Approach Performance Domain*
