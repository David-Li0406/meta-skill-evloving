---
id: risk-management
name: "Risk Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Risk Management

## Metadata
- **Category:** Project Management Framework 7 - Uncertainty Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 9 min
- **Agent:** faion-pm-agent

---

## Problem

Projects face uncertainty. Without risk management:
- Surprises become crises
- No time/budget for problems
- Opportunities are missed
- Team reacts instead of plans

## Framework

### Risk Types

| Type | Description | Examples |
|------|-------------|----------|
| **Threat** | Negative risk | Key person leaves, vendor fails |
| **Opportunity** | Positive risk | New tech, market opening |
| **Known Risk** | Identified, can plan | Integration complexity |
| **Unknown Risk** | Cannot predict | Black swan events |

### Step 1: Identify Risks

Use multiple techniques:

**Brainstorming Questions:**
- What could go wrong?
- What happened on similar projects?
- What assumptions are we making?
- What external factors could affect us?

**Risk Categories (Prompt List):**
| Category | Example Risks |
|----------|--------------|
| Technical | New technology, integration, performance |
| External | Market, regulations, suppliers |
| Organizational | Resources, priorities, politics |
| Project | Scope, schedule, budget |

### Step 2: Analyze Risks

**Qualitative Analysis:**

Probability × Impact Matrix:

```
         |  Low  | Medium | High |
---------|-------|--------|------|
High P   |  Med  |  High  | Crit |
Medium P |  Low  |  Med   | High |
Low P    |  Low  |  Low   | Med  |
```

**Quantitative Analysis (for major risks):**

Expected Monetary Value (EMV):
```
EMV = Probability × Impact

Example:
Risk: Key developer quits
P = 20%, Impact = $30,000 delay
EMV = 0.20 × $30,000 = $6,000

Add $6,000 to contingency for this risk
```

### Step 3: Plan Risk Responses

**For Threats:**

| Strategy | Description | Example |
|----------|-------------|---------|
| **Avoid** | Eliminate the risk | Don't use unproven technology |
| **Transfer** | Shift to third party | Insurance, fixed-price contracts |
| **Mitigate** | Reduce probability/impact | Hire backup, add testing |
| **Accept** | Acknowledge, have plan B | Budget for contingency |

**For Opportunities:**

| Strategy | Description | Example |
|----------|-------------|---------|
| **Exploit** | Ensure it happens | Hire star performer |
| **Enhance** | Increase probability | Early marketing |
| **Share** | Partner to maximize | Joint ventures |
| **Accept** | Take it if it comes | Bonus if market grows |

### Step 4: Implement and Monitor

- Assign risk owners
- Track risk triggers
- Update risk register weekly
- Conduct risk reviews at milestones

---

## Templates

### Risk Register

```markdown
## Risk Register - [Project Name]

| ID | Risk | Category | P | I | Score | Response | Owner | Trigger | Status |
|----|------|----------|---|---|-------|----------|-------|---------|--------|
| R1 | Key dev leaves | Resource | M | H | High | Mitigate: Cross-train | PM | Resignation signals | Active |
| R2 | API changes | Technical | L | H | Med | Accept: Buffer time | Dev | API announcements | Active |
| R3 | Early adopters | Market | M | M | Med | Enhance: Beta program | Marketing | Sign-up rate | Active |
| R4 | Scope creep | Project | H | H | Crit | Avoid: Freeze scope | PM | Change requests | Active |
```

### Risk Response Plan

```markdown
## Risk Response Plan: R1 - Key Developer Leaves

**Risk:** Key developer (Alex) leaves during critical development phase

**Category:** Resource
**Probability:** Medium (30%)
**Impact:** High ($30,000 + 4-week delay)
**EMV:** $9,000

### Prevention (Mitigate)
- [ ] Cross-train second developer on Alex's modules
- [ ] Document all architectural decisions
- [ ] Weekly knowledge sharing sessions
- [ ] Retention discussion with HR

### Response Plan (If Risk Occurs)
1. Immediate: Activate backup developer
2. Week 1: Assess knowledge gaps
3. Week 2: Intensive knowledge transfer
4. Week 3-4: Parallel work with oversight

### Triggers
- Alex mentions job hunting
- Unusual resume activity
- Decreased engagement
- External recruiter contact

**Owner:** Project Manager
**Review:** Weekly
```

---

## Examples

### Example 1: SaaS Startup Risk Register

| Risk | P | I | Response |
|------|---|---|----------|
| No product-market fit | H | H | Mitigate: Validate before building |
| Competitor launches first | M | M | Accept: Focus on differentiation |
| Technical debt | H | M | Mitigate: Code reviews, refactoring |
| Funding runs out | L | H | Transfer: Secure runway, backup plan |
| Key hire doesn't work out | M | H | Mitigate: Trial period, backup candidates |

### Example 2: Solopreneur Risk Awareness

```markdown
## My Business Risks

**Critical (Must Address):**
1. Single point of failure (me)
   - Mitigate: Document processes, create SOPs
   - Accept: Emergency fund (6 months)

2. Client concentration
   - Mitigate: Maximum 30% revenue from one client
   - Enhance: Actively pursue new clients

**Monitor:**
- Market changes
- Technology shifts
- Health/burnout

**Opportunity:**
- AI automation → Enhance: Learn and apply
```

---

## Common Mistakes

1. **Only tracking threats** - Opportunities are risks too
2. **Set and forget** - Risks change, register must update
3. **No owners** - Risks without owners are ignored
4. **Hiding risks** - Transparency enables response
5. **Over-analyzing** - Not all risks need deep analysis

---

## Related Methodologies

- **Cost Estimation:** Contingency planning
- **Change Control:** Risk-triggered changes
- **Uncertainty Performance Domain:** Managing project uncertainty

---

*Methodology from Project Management Framework 7 - Uncertainty Performance Domain*
