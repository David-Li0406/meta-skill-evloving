---
id: risk-register
name: "Risk Register"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Risk Register

## Metadata
- **Category:** Project Management Framework / Uncertainty Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #methodology #pmbok #risk #uncertainty #project-management
- **Agent:** faion-pm-agent

---

## Problem

Bad things happen that you did not anticipate. Key team member quits. Third-party API changes. Customer requirements shift dramatically. When risks materialize without plans, you scramble and usually fail.

Without risk management:
- Surprises derail progress
- No prepared responses
- Reactive crisis mode
- Stakeholder confidence erodes

---

## Framework

### Step 1: Identify Risks

Brainstorm what could go wrong (threats) or right (opportunities).

**Risk categories:**
- **Technical** - Technology fails, complexity higher than expected
- **External** - Vendor delays, market changes, regulations
- **Organizational** - Resource unavailable, priority shifts
- **Project Management** - Poor estimates, scope creep

**Identification techniques:**
- Team brainstorming
- Expert interviews
- Checklist review
- Historical project analysis
- SWOT analysis

### Step 2: Analyze Risks

For each risk, assess:

**Probability:** How likely to occur?

| Level | Description | Percentage |
|-------|-------------|------------|
| Very Low | Rare | < 10% |
| Low | Unlikely | 10-30% |
| Medium | Possible | 30-50% |
| High | Likely | 50-70% |
| Very High | Almost certain | > 70% |

**Impact:** How severe if it occurs?

| Level | Description | Effect |
|-------|-------------|--------|
| Very Low | Negligible | < 5% budget/schedule |
| Low | Minor | 5-10% budget/schedule |
| Medium | Moderate | 10-20% budget/schedule |
| High | Major | 20-40% budget/schedule |
| Very High | Critical | > 40% or project failure |

### Step 3: Calculate Risk Score

**Risk Score = Probability x Impact**

Create a matrix:

```
             IMPACT
           VL  L   M   H  VH
         +--------------------
      VH | 5  10  15  20  25
      H  | 4   8  12  16  20
PROB  M  | 3   6   9  12  15
      L  | 2   4   6   8  10
      VL | 1   2   3   4   5
```

| Score | Priority |
|-------|----------|
| 15-25 | High - Immediate attention |
| 8-14 | Medium - Monitor closely |
| 1-7 | Low - Periodic review |

### Step 4: Plan Responses

For each significant risk, choose a strategy:

**For Threats (negative risks):**

| Strategy | Description | Example |
|----------|-------------|---------|
| **Avoid** | Eliminate the threat | Change approach, remove risky feature |
| **Transfer** | Shift to third party | Insurance, outsource, contracts |
| **Mitigate** | Reduce probability or impact | Prototype first, add testing |
| **Accept** | Acknowledge, plan contingency | Budget reserve for if it happens |

**For Opportunities (positive risks):**

| Strategy | Description | Example |
|----------|-------------|---------|
| **Exploit** | Ensure it happens | Assign best resources |
| **Share** | Partner for benefit | Joint venture, revenue share |
| **Enhance** | Increase probability | More marketing, better timing |
| **Accept** | Take benefit if it occurs | No special action |

### Step 5: Assign Owners

Every risk needs one owner responsible for:
- Monitoring triggers
- Executing response if needed
- Updating status

### Step 6: Monitor and Update

- Review risks weekly in team meetings
- Add new risks as discovered
- Update probability/impact as situation changes
- Close risks that pass or materialize
- Track response effectiveness

---

## Templates

### Risk Register Template

```markdown
# Risk Register: [Project Name]

**Last Updated:** [Date]
**Risk Manager:** [Name]

| ID | Risk Description | Category | Prob | Impact | Score | Strategy | Response | Owner | Status |
|----|------------------|----------|------|--------|-------|----------|----------|-------|--------|
| R-01 | [Description] | Technical | M | H | 12 | Mitigate | [Action] | [Name] | Open |
| R-02 | [Description] | External | L | VH | 10 | Transfer | [Action] | [Name] | Open |
| R-03 | [Description] | Resource | H | M | 12 | Accept | [Contingency] | [Name] | Open |
```

### Individual Risk Card

```markdown
# Risk: R-[XX] - [Short Name]

## Description
[Detailed risk description]

## Category
[Technical / External / Organizational / PM]

## Assessment
- **Probability:** [VL/L/M/H/VH] - [Rationale]
- **Impact:** [VL/L/M/H/VH] - [Rationale]
- **Risk Score:** [1-25]
- **Priority:** [High/Medium/Low]

## Response Strategy
- **Strategy:** [Avoid/Transfer/Mitigate/Accept]
- **Response Plan:** [Detailed actions]
- **Contingency:** [If risk materializes]
- **Trigger:** [How we know risk is occurring]

## Ownership
- **Risk Owner:** [Name]
- **Response Owner:** [Name if different]

## Tracking
| Date | Status | Notes |
|------|--------|-------|
| [Date] | Open | Initial identification |
| [Date] | Monitoring | [Update] |
```

---

## Examples

### Example 1: Software Project Risk Register

| Risk | P | I | Score | Strategy | Response |
|------|---|---|-------|----------|----------|
| Key developer leaves | M | H | 12 | Mitigate | Document code, cross-train |
| Third-party API deprecated | L | VH | 10 | Accept | Build abstraction layer, monitor |
| Scope creep | H | M | 12 | Avoid | Change control process |
| Performance issues | M | M | 9 | Mitigate | Early load testing |
| Budget cut | L | H | 8 | Accept | Identify optional features |

### Example 2: Opportunity Risks

| Opportunity | P | I | Score | Strategy | Response |
|-------------|---|---|-------|----------|----------|
| Early delivery possible | M | H | 12 | Enhance | Fast-track critical path |
| Partnership offer | L | VH | 10 | Exploit | Prioritize integration |
| Positive press coverage | M | M | 9 | Share | Prepare press kit |

---

## Common Mistakes

1. **One-time exercise** - Identifying risks once, never updating
2. **No owners** - Risks without accountability
3. **All accept** - Not planning actual responses
4. **Missing positive risks** - Only focusing on threats
5. **Too vague** - "Something might go wrong" is not actionable

---

## Risk Review Checklist

Weekly review should cover:
- [ ] Any new risks identified?
- [ ] Any risks probability/impact changed?
- [ ] Any triggers activated?
- [ ] Any responses in progress?
- [ ] Any risks to close?
- [ ] Top 5 risks still accurate?

---

## Next Steps

After building your risk register:
1. Share with stakeholders for buy-in
2. Integrate into project status meetings
3. Link risks to schedule/budget contingencies
4. Connect to Change Control methodology

---

## References

- Project Management Framework Guide 7th Edition - Uncertainty Performance Domain
- PM industry practice standard for Project Risk Management
