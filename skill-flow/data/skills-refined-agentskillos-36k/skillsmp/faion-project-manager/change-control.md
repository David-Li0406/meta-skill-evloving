---
id: change-control
name: "Change Control"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Change Control

## Metadata
- **Category:** Project Management Framework 7 - Delivery Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 7 min
- **Agent:** faion-pm-agent

---

## Problem

Uncontrolled changes cause:
- Scope creep destroying budgets
- Quality compromises from rushed additions
- Team confusion about current requirements
- Stakeholder disappointment from unmet expectations

## Framework

### Change Control Process

```
Request → Log → Analyze → Decide → Implement → Close

   ↓       ↓       ↓        ↓          ↓         ↓
Stakeholder → PM → Team → CCB → PM/Team → PM
```

### Step 1: Receive Change Request

Capture every change request formally:

**Required Information:**
- Requester name and role
- Date submitted
- Description of change
- Business justification
- Priority/urgency

### Step 2: Log in Change Register

Assign unique ID, track status:

| Status | Meaning |
|--------|---------|
| Submitted | Received, not yet reviewed |
| Under Review | Being analyzed |
| Approved | Will be implemented |
| Rejected | Will not be implemented |
| Deferred | Postponed to future |
| Implemented | Completed |

### Step 3: Analyze Impact

For each change, assess:

| Impact Area | Questions |
|-------------|-----------|
| **Scope** | What features affected? |
| **Schedule** | How many days added? |
| **Cost** | What additional budget? |
| **Quality** | Does it affect standards? |
| **Risk** | New risks introduced? |
| **Resources** | Who needs to work on it? |

### Step 4: Decision

**Decision Authority:**

| Change Size | Decision Maker |
|-------------|----------------|
| Minor (< 1 day, < $500) | Project Manager |
| Medium (1-5 days, < $5,000) | Sponsor |
| Major (> 5 days, > $5,000) | Change Control Board (CCB) |

### Step 5: Implement or Reject

**If Approved:**
1. Update project documents (scope, schedule, budget)
2. Communicate to team
3. Track implementation

**If Rejected:**
1. Document reason
2. Communicate to requester
3. Close request

---

## Templates

### Change Request Form

```markdown
## Change Request Form

**CR ID:** CR-2024-015
**Date:** 2024-03-15
**Requester:** John Smith (Product Owner)
**Priority:** High

### Description
Add social login (Google, Facebook) to existing email/password authentication.

### Business Justification
User research shows 40% of users prefer social login. Expected to increase signup conversion by 25%.

### Impact Analysis

| Area | Impact |
|------|--------|
| Scope | +2 new auth methods, updated UI |
| Schedule | +8 days development |
| Cost | +$4,000 development |
| Quality | Minimal - standard OAuth flow |
| Risk | Low - well-documented APIs |
| Resources | 1 backend developer, 1 frontend |

### Options

| Option | Days | Cost | Recommendation |
|--------|------|------|----------------|
| A: Both Google + Facebook | 8 | $4,000 | Recommended |
| B: Google only | 4 | $2,000 | Alternative |
| C: Post-launch | 0 | TBD | Defer |

### Decision
- [ ] Approve (Option A/B/C)
- [ ] Reject
- [ ] Defer

**Decided By:** ________________
**Date:** ________________
**Notes:** ________________
```

### Change Register

```markdown
## Change Register - [Project Name]

| CR ID | Date | Description | Requester | Priority | Impact | Status | Decision Date |
|-------|------|-------------|-----------|----------|--------|--------|---------------|
| CR-001 | 3/1 | Add export to PDF | User | Medium | 3d, $1.5K | Approved | 3/5 |
| CR-002 | 3/5 | Change color scheme | Marketing | Low | 2d, $1K | Rejected | 3/8 |
| CR-003 | 3/10 | Social login | PO | High | 8d, $4K | Under Review | - |
| CR-004 | 3/12 | Mobile responsive | Sponsor | High | 5d, $2.5K | Approved | 3/14 |
```

---

## Examples

### Example 1: Scope Change Management

**Situation:** Client wants to add payment integration mid-project.

**Analysis:**
```markdown
CR-010: Add Stripe Payment Integration

Impact:
- Scope: +Payment module, checkout flow
- Schedule: +3 weeks (15 days)
- Cost: +$7,500
- Dependencies: Delays user testing phase
- Risk: Stripe API changes, PCI compliance

Options:
1. Add now: +3 weeks, +$7,500
2. Launch without, add in Phase 2
3. Use Stripe checkout (hosted) - 1 week, $2,500

Recommendation: Option 3 for MVP, Option 1 for Phase 2
```

### Example 2: Change Prevention

Best change control is preventing unnecessary changes:

```markdown
## Change Prevention Checklist

Before starting project:
- [ ] Scope clearly defined and signed off
- [ ] Key stakeholders identified
- [ ] Requirements frozen date agreed
- [ ] Change process communicated
- [ ] Budget contingency for changes

During project:
- [ ] Scope freeze enforced
- [ ] Change request process visible
- [ ] "Say no" culture established
- [ ] Trade-offs discussed openly
```

---

## Common Mistakes

1. **No formal process** - Changes happen informally
2. **PM approves everything** - Escalate appropriately
3. **Impact not analyzed** - Hidden costs emerge later
4. **Too bureaucratic** - Process slows value delivery
5. **Not tracking rejected changes** - Same requests repeat

---

## Related Methodologies

- **Work Breakdown Structure:** Scope baseline management
- **Risk Management:** Risk-related changes
- **Project Integration:** Coordinating changes across areas

---

*Methodology from Project Management Framework 7 - Delivery Performance Domain*
