---
id: technical-debt-management
name: "Technical Debt Management"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Technical Debt Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #technical-debt, #engineering |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-code-agent |

---

## Problem

Technical debt silently slows teams until crisis. Issues:
- Velocity decreasing over time
- "Quick fixes" accumulate
- No visibility into debt
- Debt never prioritized against features

**The root cause:** Technical debt is invisible to non-technical stakeholders and never systematically addressed.

---

## Framework

### What is Technical Debt?

Technical debt is the implied cost of additional rework caused by choosing easy solutions now instead of better approaches that take longer. It's "borrowing" against future productivity.

### Types of Technical Debt

| Type | Description | Example |
|------|-------------|---------|
| Deliberate | Conscious shortcuts | "Ship now, refactor later" |
| Accidental | Learned better way | "Didn't know about X pattern" |
| Bit rot | Environment changed | "Dependencies outdated" |
| Design debt | Architecture limitations | "Can't scale current approach" |
| Documentation debt | Missing docs | "No one knows how this works" |
| Test debt | Missing tests | "Can't safely change X" |

### Technical Debt Quadrant

```
            Deliberate
                |
    Reckless    |    Prudent
   "No time for |  "Ship now,
    design"     |   refactor later"
   ─────────────┼─────────────────
   "What's a    |  "Now we know
    design?"    |   how to do it"
    Reckless    |    Prudent
                |
            Inadvertent
```

**Prudent debt is acceptable; reckless is not.**

### Technical Debt Management Process

#### Step 1: Make Debt Visible

**Tracking methods:**
- Tag in issue tracker (tech-debt label)
- Dedicated backlog
- Code comments (TODO/FIXME with tickets)
- Tech debt register

**For each item:**
- What is the debt
- Why it exists
- Impact (time tax)
- Cost to fix

#### Step 2: Quantify Impact

**Metrics:**
- Time tax: How much slower are we?
- Risk: What could break?
- Opportunity cost: What can't we do?

**Formula:**
```
Interest = (Development slowdown × Frequency) + Risk cost
```

#### Step 3: Prioritize Debt

**Factors:**
| Factor | Weight | Description |
|--------|--------|-------------|
| Interest rate | 40% | How much it slows us |
| Contagion | 20% | Does it spread? |
| Effort to fix | 20% | How hard to address |
| Alignment | 20% | Related to planned work |

**Priority = Impact × Alignment / Effort**

#### Step 4: Allocate Capacity

**Common approaches:**

| Approach | Description | When |
|----------|-------------|------|
| Dedicated % | 20% of each sprint | Continuous |
| Debt sprints | Full sprint quarterly | Periodic |
| Boy Scout | Clean as you touch | Continuous |
| Spike work | Specific investigation | As needed |

**Recommended:** 15-20% continuous + quarterly focused time

#### Step 5: Pay Down Strategically

**Strategies:**
- Fix during related features (lowest marginal cost)
- Fix highest-interest first (biggest impact)
- Fix blocking debt (enables future work)
- Batch related debt (efficiency)

#### Step 6: Prevent New Debt

**Policies:**
- Definition of Done includes no new debt
- Code review catches debt
- Architecture decisions documented
- Refactoring is normal, not special

---

## Templates

### Technical Debt Register

```markdown
## Technical Debt Register: [Product]

### Summary
- **Total items:** [X]
- **High priority:** [X]
- **Est. fix time:** [X] days
- **Last reviewed:** [Date]

### Debt Items

#### TD-001: [Name]
**Type:** [Deliberate/Accidental/Bit rot/Design/Docs/Test]
**Created:** [Date]
**Location:** [File/module/system]

**Description:**
[What the debt is]

**Why it exists:**
[How it was created]

**Impact:**
- Time tax: [Hours/sprint slowed]
- Risk: [What could happen]
- Affected areas: [What's impacted]

**Fix effort:** [T-shirt size]
**Priority:** [High/Medium/Low]
**Related work:** [Upcoming features that touch this]

**Fix approach:**
[How to address]

---

#### TD-002: [Name]
...
```

### Debt Prioritization Matrix

```markdown
## Debt Prioritization: [Quarter]

### Scoring

| ID | Debt | Interest | Contagion | Effort | Alignment | Score |
|----|------|----------|-----------|--------|-----------|-------|
| TD-001 | [Name] | 5 | 3 | 2 | 5 | 8.5 |
| TD-002 | [Name] | 3 | 2 | 4 | 3 | 4.0 |

### This Quarter's Plan

**Capacity allocated:** [X]% = [Y] days

| ID | Debt | Effort | Sprint | Owner |
|----|------|--------|--------|-------|
| TD-001 | [Name] | 2 days | Sprint 1 | [Name] |
| TD-004 | [Name] | 3 days | Sprint 2 | [Name] |

### Deferred

| ID | Debt | Reason | Revisit |
|----|------|--------|---------|
| TD-003 | [Name] | Low alignment | Q3 |
```

### Sprint Debt Budget

```markdown
## Sprint [X] Debt Work

### Budget
- **Available:** [X] days (20% of capacity)
- **Planned:** [X] days

### Items

| Item | Description | Effort | Owner | Status |
|------|-------------|--------|-------|--------|
| [TD-X] | [Description] | 1d | [Name] | Done |
| [TD-Y] | [Description] | 0.5d | [Name] | In Progress |
| Boy Scout | Ad-hoc improvements | 0.5d | Team | Ongoing |

### Outcomes
- [What was improved]
- [Velocity impact expected]
```

---

## Examples

### Example 1: Legacy API Debt

**Debt:** Old API v1 still maintained alongside v2

**Impact:**
- 3 hours/sprint maintaining both
- Risk of v1 bugs affecting v2 users
- Can't deprecate without migration plan

**Interest:** High (ongoing time tax)
**Effort:** Medium (need migration path for 20 users)
**Alignment:** High (API work planned next quarter)

**Decision:** Prioritize in Q2 with API improvements

### Example 2: Missing Test Coverage

**Debt:** Billing module has 10% test coverage

**Impact:**
- 2 hours extra manual testing per release
- Fear of changing billing code
- Previous billing bug cost $5K

**Interest:** Medium-High
**Effort:** High (complex business logic)
**Alignment:** Medium

**Decision:** Add tests as part of billing feature work

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring debt | Make it visible |
| All or nothing | Continuous small payments |
| No prioritization | Score and rank debt |
| Only refactoring | Include docs, tests |
| Not tracking new debt | Add to register immediately |
| No business case | Quantify impact |
| Debt vacation | Consistent allocation |

---

## Related Methodologies

- **roadmap-design:** Roadmap Design
- **quality-gates-confidence:** Quality Gates & Confidence
- **change-control:** Change Control
- **code-review:** Code Review
- **refactoring:** Refactoring

---

## Agent

**faion-code-agent** helps with technical debt. Invoke with:
- "Audit technical debt in [codebase]"
- "Prioritize this debt: [list]"
- "How should I address [debt item]?"
- "Create a debt paydown plan for [quarter]"

---

*Methodology | Product | Version 1.0*
