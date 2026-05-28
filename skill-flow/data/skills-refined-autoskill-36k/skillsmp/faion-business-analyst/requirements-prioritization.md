---
id: requirements-prioritization
name: "Requirements Prioritization"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Requirements Prioritization

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #prioritization #requirements #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

All requirements seem equally important. Stakeholders fight for their requirements. Everything is marked "high priority." Resources are spread thin trying to do everything. The most valuable features are not delivered first.

Without prioritization:
- No focus on value
- Resource conflicts
- Delayed ROI
- Stakeholder frustration

---

## Framework

### Why Prioritize?

- Limited resources (time, money, people)
- Need to deliver value early
- Not all requirements are equally important
- Stakeholders have different perspectives

### Prioritization Criteria

| Criterion | Question |
|-----------|----------|
| **Business value** | How much value does this provide? |
| **Cost** | How expensive to implement? |
| **Risk** | What is the risk of doing/not doing? |
| **Dependencies** | What must come first? |
| **Urgency** | Is there a deadline? |
| **Regulatory** | Is it legally required? |

### Step 1: Choose Prioritization Method

| Method | Best For |
|--------|----------|
| **MoSCoW** | Simple categorization |
| **RICE** | Data-driven prioritization |
| **Kano** | Customer satisfaction focus |
| **Value vs. Effort** | Visual quadrant analysis |
| **Weighted scoring** | Multiple criteria |

### Step 2: Gather Input

Collect stakeholder perspectives:
- Business value assessment
- Technical complexity estimate
- Risk evaluation
- Dependency mapping

### Step 3: Apply Method

Use chosen method consistently across all requirements.

### Step 4: Resolve Conflicts

When stakeholders disagree:
- Understand each perspective
- Reference criteria
- Facilitate discussion
- Escalate if needed
- Document decision

### Step 5: Communicate Results

Share prioritization:
- Explain method used
- Show results
- Explain rationale
- Get buy-in

---

## Prioritization Methods

### MoSCoW Method

| Priority | Meaning | Guideline |
|----------|---------|-----------|
| **Must** | Essential, non-negotiable | ~60% of effort |
| **Should** | Important, not critical | ~20% of effort |
| **Could** | Nice to have | ~20% of effort |
| **Won't** | Not this time | Track for future |

**Rules:**
- "Must" means the release fails without it
- "Should" means significant value but can work around
- "Could" means low cost, low impact
- "Won't" means explicitly excluded this iteration

### RICE Scoring

| Factor | Description | Calculation |
|--------|-------------|-------------|
| **Reach** | How many users affected | Number per time period |
| **Impact** | Effect on each user | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| **Confidence** | Certainty of estimates | 100%=high, 80%=medium, 50%=low |
| **Effort** | Person-months to build | Estimate |

**Formula:**
```
RICE Score = (Reach x Impact x Confidence) / Effort
```

### Kano Model

| Category | Description | Priority |
|----------|-------------|----------|
| **Basic** | Expected, absence causes dissatisfaction | Must have |
| **Performance** | More is better, linear satisfaction | Competitive advantage |
| **Delighters** | Unexpected, create satisfaction | Differentiation |
| **Indifferent** | No impact on satisfaction | Deprioritize |
| **Reverse** | Presence causes dissatisfaction | Remove |

### Value vs. Effort Matrix

```
HIGH VALUE
    |
    | Quick Wins     |  Major Projects
    | (Do First)     |  (Plan Carefully)
    |----------------|------------------
    | Fill-Ins       |  Thankless Tasks
    | (If Time)      |  (Avoid)
    |
LOW VALUE -------- LOW EFFORT -- HIGH EFFORT
```

---

## Templates

### MoSCoW Prioritization Template

```markdown
# MoSCoW Prioritization: [Release/Project]

**Date:** [Date]
**Participants:** [Names]
**Scope:** [What is being prioritized]

## Must Have (Essential)
| ID | Requirement | Rationale |
|----|-------------|-----------|
| [ID] | [Requirement] | [Why essential] |

## Should Have (Important)
| ID | Requirement | Rationale |
|----|-------------|-----------|
| [ID] | [Requirement] | [Why important] |

## Could Have (Nice to Have)
| ID | Requirement | Rationale |
|----|-------------|-----------|
| [ID] | [Requirement] | [Low cost/impact] |

## Won't Have (Not This Time)
| ID | Requirement | Rationale | Future? |
|----|-------------|-----------|---------|
| [ID] | [Requirement] | [Why excluded] | [Yes/No] |

## Summary
- Must Have: [X] requirements ([X]% of effort)
- Should Have: [X] requirements ([X]% of effort)
- Could Have: [X] requirements ([X]% of effort)
- Won't Have: [X] requirements (excluded)
```

### RICE Scoring Template

```markdown
# RICE Prioritization: [Feature Set]

**Date:** [Date]
**Analyst:** [Name]

## Scoring Criteria

| Factor | Scale |
|--------|-------|
| Reach | Users per [month/quarter] |
| Impact | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| Confidence | 100%, 80%, 50% |
| Effort | Person-months |

## Scores

| ID | Requirement | Reach | Impact | Confidence | Effort | RICE Score | Rank |
|----|-------------|-------|--------|------------|--------|------------|------|
| [ID] | [Name] | [X] | [X] | [X%] | [X] | [Score] | [#] |
| [ID] | [Name] | [X] | [X] | [X%] | [X] | [Score] | [#] |

## Prioritized List
1. [Requirement] - Score: [X]
2. [Requirement] - Score: [X]
3. [Requirement] - Score: [X]
```

### Value-Effort Matrix Template

```markdown
# Value-Effort Analysis: [Scope]

**Date:** [Date]
**Participants:** [Names]

## Scores

| ID | Requirement | Value (1-5) | Effort (1-5) | Quadrant |
|----|-------------|-------------|--------------|----------|
| [ID] | [Name] | [X] | [X] | [Quadrant] |

## Quadrant Summary

### Quick Wins (High Value, Low Effort)
- [Requirement 1]
- [Requirement 2]

### Major Projects (High Value, High Effort)
- [Requirement 1]
- [Requirement 2]

### Fill-Ins (Low Value, Low Effort)
- [Requirement 1]

### Avoid (Low Value, High Effort)
- [Requirement 1]

## Recommendation
1. Start with Quick Wins
2. Plan Major Projects
3. Consider Fill-Ins for slack time
4. Avoid low-value high-effort items
```

---

## Examples

### Example 1: MoSCoW for MVP

**Context:** E-commerce MVP, 3-month timeline

**Must Have:**
- User registration and login
- Product catalog
- Shopping cart
- Checkout with payment

**Should Have:**
- User reviews
- Wishlist
- Order history

**Could Have:**
- Product recommendations
- Social sharing

**Won't Have:**
- Mobile app
- Loyalty program

### Example 2: RICE Scoring

| Feature | Reach | Impact | Conf | Effort | Score |
|---------|-------|--------|------|--------|-------|
| Export to PDF | 5000 | 2 | 80% | 1 | 8000 |
| Dark mode | 3000 | 0.5 | 100% | 2 | 750 |
| API access | 500 | 3 | 50% | 3 | 250 |
| Bulk upload | 200 | 3 | 80% | 1 | 480 |

**Priority:** Export to PDF > Bulk upload > Dark mode > API access

---

## Common Mistakes

1. **Everything is Must** - No real prioritization
2. **HiPPO effect** - Highest Paid Person's Opinion dominates
3. **Ignoring effort** - All focus on value
4. **No criteria** - Gut feeling decisions
5. **One-time exercise** - Not revisiting priorities

---

## Handling Disagreements

**When stakeholders conflict:**

1. **Revisit criteria** - Remind everyone of the framework
2. **Use data** - Bring metrics and evidence
3. **Consider perspectives** - Each stakeholder sees different value
4. **Find compromise** - Phase approach, conditions
5. **Escalate** - Product Owner or Sponsor decides

---

## Prioritization in Agile

**Backlog prioritization:**
- Product Owner owns priority
- BA provides analysis support
- Stack rank (ordered list, not categories)
- Re-prioritize each sprint

**Release prioritization:**
- MoSCoW for release scope
- Stories ordered within categories
- Continuous refinement

---

## Next Steps

After prioritization:
1. Communicate to team
2. Update backlog order
3. Plan implementation
4. Review regularly
5. Connect to Interface Analysis methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Prioritization Guidelines
