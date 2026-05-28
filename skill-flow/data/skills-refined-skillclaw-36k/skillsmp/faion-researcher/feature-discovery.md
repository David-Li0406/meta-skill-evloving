---
id: feature-discovery
name: "Feature Discovery"
domain: RES
skill: faion-researcher
category: "research"
---

# Feature Discovery

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #features, #discovery |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-idea-generator-agent |

---

## Problem

Feature decisions are often based on gut feeling, competitor copying, or loudest customer requests. Issues:
- Building features nobody uses
- Missing features that drive adoption
- Feature bloat killing simplicity
- No connection between features and outcomes

**The root cause:** No systematic process for discovering and validating features.

---

## Framework

### What is Feature Discovery?

Feature discovery is the process of identifying, prioritizing, and validating potential product capabilities. It answers: "What should we build and why?"

### Feature Discovery Sources

#### 1. Customer Research

| Source | Method | Signal Quality |
|--------|--------|----------------|
| Interviews | Direct conversation | High (if done well) |
| Support tickets | Pattern analysis | High (real problems) |
| Feature requests | Tracking and analysis | Medium (stated ≠ needed) |
| Churn interviews | Exit conversations | High (critical gaps) |
| NPS detractors | Follow-up on low scores | High (improvement needs) |

#### 2. Usage Analytics

| Metric | Insight |
|--------|---------|
| Feature adoption | What's used vs. ignored |
| Drop-off points | Where users struggle |
| Power user behavior | What advanced users need |
| Time in feature | Engagement vs. friction |
| Error rates | What's broken |

#### 3. Competitive Analysis

| Source | What to Look For |
|--------|------------------|
| Competitor features | Standard expectations |
| Competitor gaps | Differentiation opportunities |
| Competitor reviews | What customers hate |
| New entrants | Emerging patterns |

#### 4. Market Trends

| Source | What to Track |
|--------|---------------|
| Industry reports | Where market is heading |
| Technology changes | What's now possible |
| Regulatory changes | New requirements |
| Adjacent markets | Cross-pollination |

### Feature Discovery Process

#### Step 1: Collect Feature Ideas

**Feature idea capture template:**
```
Feature: [Name]
Source: [Where idea came from]
Problem solved: [What pain it addresses]
Requested by: [Customer segment]
Frequency: [How often requested]
Impact estimate: [Adoption/Revenue/Retention]
```

#### Step 2: Categorize Features

**Feature types:**

| Type | Description | Examples |
|------|-------------|----------|
| Core | Essential functionality | Basic CRUD operations |
| Performance | Make existing better | Speed, reliability |
| Excitement | Unexpected delight | AI suggestions |
| Threshold | Basic expectations | Login, security |

**Using Kano Model:**

```
                  Satisfaction
                      ↑
    Delighters        |        Must-haves
    (Excitement)      |        (Threshold)
                      |
    ──────────────────.────────────────→ Implementation
                      |
    Indifferent       |        Performance
                      |        (More is better)
                      ↓
```

#### Step 3: Validate Importance

**Opportunity Scoring (ODI):**

For each feature, ask users:
1. "When [job], how important is [outcome]?" (1-10)
2. "How satisfied are you with current solutions?" (1-10)

**Opportunity = Importance + (Importance - Satisfaction)**

**High opportunity:** High importance, low satisfaction

#### Step 4: Estimate Effort

**Effort categories:**

| Level | Description | Team Days |
|-------|-------------|-----------|
| XS | Trivial | <1 day |
| S | Small | 1-3 days |
| M | Medium | 1-2 weeks |
| L | Large | 2-4 weeks |
| XL | Very large | 1-3 months |

#### Step 5: Prioritize

**RICE Scoring:**

| Factor | Description | Scale |
|--------|-------------|-------|
| Reach | How many affected | Users/quarter |
| Impact | Effect magnitude | 0.25, 0.5, 1, 2, 3 |
| Confidence | Evidence level | 50%, 80%, 100% |
| Effort | Person-weeks | Number |

**RICE = (Reach × Impact × Confidence) / Effort**

#### Step 6: Validate Before Building

**Validation methods:**

| Method | Effort | Confidence |
|--------|--------|------------|
| Fake door test | Low | Medium |
| Prototype | Medium | High |
| Wizard of Oz | Medium | High |
| Limited beta | High | Very high |
| Pre-sales | Medium | Very high |

---

## Templates

### Feature Discovery Board

```markdown
## Feature Discovery: [Product]
**Period:** [Quarter/Month]

### Collection Sources Active
- [ ] Customer interviews (N=X)
- [ ] Support ticket analysis
- [ ] Feature request log
- [ ] Analytics review
- [ ] Competitor monitoring

### Feature Ideas Collected

| ID | Feature | Source | Problem | Segment | Frequency |
|----|---------|--------|---------|---------|-----------|
| F1 | [Name] | [Source] | [Problem] | [Seg] | High |
| F2 | [Name] | [Source] | [Problem] | [Seg] | Medium |

### Categorization

| Feature | Kano Type | Priority |
|---------|-----------|----------|
| [F1] | Must-have | High |
| [F2] | Performance | Medium |
| [F3] | Delighter | Low |

### Opportunity Scoring

| Feature | Importance | Satisfaction | Opportunity |
|---------|------------|--------------|-------------|
| [F1] | 9 | 4 | 14 |
| [F2] | 7 | 5 | 9 |

### RICE Prioritization

| Feature | Reach | Impact | Confidence | Effort | RICE |
|---------|-------|--------|------------|--------|------|
| [F1] | 1000 | 2 | 80% | 2 | 800 |
| [F2] | 500 | 1 | 100% | 1 | 500 |

### Validation Plan

| Feature | Method | Timeline | Success Criteria |
|---------|--------|----------|------------------|
| [F1] | Prototype | Week 1-2 | 50% positive feedback |
| [F2] | Fake door | Week 1 | 10% click rate |
```

### Feature Request Log

```markdown
## Feature Request: [Feature Name]

### Metadata
- **ID:** FR-[XXX]
- **Created:** [Date]
- **Status:** [New/Validating/Planned/Building/Shipped/Rejected]

### Request Details
- **Source:** [Customer/Prospect/Internal/Competitor]
- **Requester:** [Name/Segment]
- **Request count:** [N times requested]

### Problem
[What problem does this solve?]

### Proposed Solution
[Customer's suggestion or our interpretation]

### Impact Assessment
- **Users affected:** [Segment and estimate]
- **Retention impact:** [High/Medium/Low]
- **Revenue impact:** [High/Medium/Low]
- **Effort estimate:** [T-shirt size]

### Validation
- [ ] Validated problem exists
- [ ] Validated solution fits
- [ ] Estimated demand: [N users]

### Decision
**Status:** [Planned/Rejected/Deferred]
**Reasoning:** [Why]
**Timeline:** [When if planned]

### Related
- Similar requests: [Links]
- Competing priorities: [Links]
```

---

## Examples

### Example 1: SaaS Dashboard Feature Discovery

**Problem:** Dashboard too cluttered, key metrics buried

**Discovery process:**
1. **Interviews (N=15):** "What's the first thing you look for?"
2. **Analytics:** 80% users only view 3 of 12 widgets
3. **Support tickets:** 23 requests for "simpler view"

**Features identified:**
| Feature | RICE Score |
|---------|------------|
| Customizable dashboard | 1200 |
| Focus mode (3 metrics) | 900 |
| Saved views | 600 |

**Validation:** Prototype test with 10 users, 8/10 preferred simplified view

**Decision:** Build "Focus mode" first (highest RICE, lowest effort)

### Example 2: Mobile App Feature Discovery

**Problem:** Low daily active users after download

**Discovery process:**
1. **Churn interviews:** "I forget the app exists"
2. **Analytics:** 90% users never enable notifications
3. **Competitor analysis:** Push notifications with value

**Features identified:**
| Feature | Opportunity Score |
|---------|-------------------|
| Smart notifications | 16 |
| Daily digest | 12 |
| Widget for home screen | 10 |

**Validation:** A/B test notification types, measure open rates

**Decision:** Smart notifications first, then widget

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Building every request | Prioritize ruthlessly |
| No validation | Test before building |
| Copying competitors | Understand why they built it |
| Only listening to loudest | Weight by segment value |
| No effort estimation | Always estimate before committing |
| Ignoring analytics | Usage data is truth |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **user-interviews:** User Interviews
- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **feature-prioritization-moscow:** Feature Prioritization (MoSCoW)
- **usability-testing:** Usability Testing

---

## Agent

**faion-idea-generator-agent** helps with feature discovery. Invoke with:
- "What features should I build for [product]?"
- "Prioritize these features: [list]"
- "How should I validate [feature idea]?"
- "Analyze feature requests for [product]"

---

*Methodology | Research | Version 1.0*
