---
id: feature-prioritization-rice
name: "Feature Prioritization (RICE)"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Feature Prioritization (RICE)

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Beginner |
| **Tags** | #product, #prioritization, #rice |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-feature-proposer-agent |

---

## Problem

Feature prioritization is often driven by gut feeling or loudest voices. Issues:
- HiPPO (Highest Paid Person's Opinion) decides
- No consistent framework across decisions
- Effort ignored, leading to scope creep
- Customer requests override strategy

**The root cause:** No quantitative framework for comparing features objectively.

---

## Framework

### What is RICE?

RICE is a scoring framework developed by Intercom for prioritizing features and projects based on four factors:
- **R**each - How many users affected
- **I**mpact - How much it affects them
- **C**onfidence - How sure we are
- **E**ffort - How much work required

### RICE Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Higher score = Higher priority**

### Factor Definitions

#### Reach (R)

**What it measures:** Number of users/customers affected in a time period.

**How to estimate:**

| Method | How |
|--------|-----|
| Analytics | Actual users of related feature |
| Funnel data | Users at that stage |
| Market size | % of total users × total |
| Guess | Conservative estimate |

**Units:** Users per quarter (or month)

**Example:**
- Feature affects checkout flow
- 10,000 users reach checkout monthly
- Reach = 10,000

#### Impact (I)

**What it measures:** How much the feature moves the goal.

**Standardized scale:**

| Score | Description | Example |
|-------|-------------|---------|
| 3 | Massive impact | Core differentiator |
| 2 | High impact | Significant improvement |
| 1 | Medium impact | Noticeable improvement |
| 0.5 | Low impact | Minor improvement |
| 0.25 | Minimal impact | Marginal improvement |

**Tips:**
- Tie to specific metric (conversion, retention)
- Consider both direct and indirect effects
- Be conservative

#### Confidence (C)

**What it measures:** How sure you are about R, I, and ability to execute.

**Scale:**

| Score | Description | Evidence Level |
|-------|-------------|----------------|
| 100% | High confidence | Data-backed, tested |
| 80% | Medium confidence | Some data, reasonable assumptions |
| 50% | Low confidence | Opinions, limited data |

**Reduce confidence when:**
- No user research
- Technical unknowns
- Never done before
- External dependencies

#### Effort (E)

**What it measures:** Person-months (or person-weeks) to complete.

**Estimation:**
- Include all work: design, dev, QA, docs
- Use T-shirt sizes, convert to numbers
- Account for unknowns

**Scale:**
- 0.5 = Few days
- 1 = About a month
- 2 = Two months
- 3 = Quarter
- 6+ = Major project

### RICE Calculation Example

```
Feature: One-click signup with Google

Reach: 5,000 users/month see signup
Impact: 2 (high - reduces friction significantly)
Confidence: 80% (tested similar features before)
Effort: 0.5 (one-week project)

RICE = (5,000 × 2 × 0.8) / 0.5 = 16,000
```

### RICE Process

#### Step 1: List All Candidates

Gather all potential features/projects.

#### Step 2: Score Each Factor

For each item, estimate R, I, C, E.

#### Step 3: Calculate RICE

Apply the formula.

#### Step 4: Rank by Score

Sort highest to lowest.

#### Step 5: Sanity Check

Does the ranking make sense? Adjust if obviously wrong.

#### Step 6: Consider Constraints

Factor in:
- Dependencies between features
- Strategic priorities
- Team availability
- Technical debt needs

---

## Templates

### RICE Scoring Spreadsheet

```markdown
## RICE Prioritization: [Product] - [Quarter]

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Rank |
|---------|-------|--------|------------|--------|------------|------|
| [Feature A] | 5,000 | 2 | 80% | 0.5 | 16,000 | 1 |
| [Feature B] | 10,000 | 1 | 100% | 2 | 5,000 | 2 |
| [Feature C] | 2,000 | 3 | 50% | 1 | 3,000 | 3 |
| [Feature D] | 8,000 | 0.5 | 80% | 3 | 1,067 | 4 |

### Notes

**Feature A:**
- Reach: Based on signup funnel analytics
- Impact: Tested with prototype, 40% improvement
- Confidence: High - similar feature worked before

**Feature B:**
- Reach: All active users monthly
- Impact: Medium - quality of life improvement
- Confidence: High - straightforward implementation
```

### RICE Decision Record

```markdown
## RICE Decision: [Feature Name]

### Scoring

| Factor | Score | Rationale |
|--------|-------|-----------|
| Reach | [X] users/quarter | [How estimated] |
| Impact | [X] | [Why this rating] |
| Confidence | [X]% | [Evidence level] |
| Effort | [X] person-months | [Breakdown] |

### Calculation
RICE = ([R] × [I] × [C]) / [E] = [Score]

### Rank
#[X] out of [Y] candidates

### Decision
[ ] Prioritize for [quarter]
[ ] Backlog for later
[ ] Reject

### Additional Considerations
- Dependencies: [Any blockers?]
- Strategic alignment: [How it fits strategy]
- Risks: [What could go wrong]
```

---

## Examples

### Example 1: E-commerce Feature Prioritization

| Feature | R | I | C | E | RICE | Decision |
|---------|---|---|---|---|------|----------|
| Guest checkout | 15K | 2 | 90% | 1 | 27,000 | Sprint 1 |
| Wishlist | 8K | 1 | 80% | 2 | 3,200 | Sprint 2 |
| Size guide | 5K | 1 | 70% | 0.5 | 7,000 | Sprint 1 |
| Gift wrapping | 2K | 0.5 | 60% | 1 | 600 | Backlog |

**Insight:** Guest checkout wins despite medium effort due to high reach and impact.

### Example 2: SaaS Dashboard Features

| Feature | R | I | C | E | RICE | Decision |
|---------|---|---|---|---|------|----------|
| Export to CSV | 3K | 1 | 100% | 0.25 | 12,000 | Sprint 1 |
| Custom dashboards | 1K | 3 | 50% | 3 | 500 | Later |
| Email reports | 2K | 2 | 80% | 1 | 3,200 | Sprint 2 |
| Dark mode | 5K | 0.5 | 100% | 0.5 | 5,000 | Sprint 2 |

**Insight:** CSV export wins due to low effort and high confidence. Custom dashboards deprioritized due to effort and confidence.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inflating Impact | Use standardized scale strictly |
| Underestimating Effort | Include all work, add buffer |
| 100% Confidence overuse | Reserve for data-backed items |
| Ignoring the ranking | Trust the math, check sanity |
| One-time scoring | Re-score quarterly |
| Skipping Reach | Don't assume "everyone" |
| No documentation | Record rationale for scores |

---

## Related Methodologies

- **feature-prioritization-moscow:** Feature Prioritization (MoSCoW)
- **feature-discovery:** Feature Discovery
- **roadmap-design:** Roadmap Design
- **mvp-scoping:** MVP Scoping
- **decision-analysis:** Decision Analysis

---

## Agent

**faion-mlp-feature-proposer-agent** helps with RICE scoring. Invoke with:
- "Score these features with RICE: [list]"
- "What's the RICE score for [feature]?"
- "Help me prioritize [feature list]"
- "Is [feature] worth building based on RICE?"

---

*Methodology | Product | Version 1.0*
