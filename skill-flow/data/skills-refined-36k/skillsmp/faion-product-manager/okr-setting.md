---
id: okr-setting
name: "OKR Setting"
domain: PRD
skill: faion-product-manager
category: "product"
---

# OKR Setting

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #okr, #goals |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-impl-planner-agent |

---

## Problem

Goal-setting is either too vague or too rigid. Common issues:
- Goals like "improve the product" (unmeasurable)
- Too many objectives (no focus)
- Key results that are really tasks
- OKRs set and forgotten

**The root cause:** No structured framework connecting ambition to measurable progress.

---

## Framework

### What are OKRs?

OKRs (Objectives and Key Results) is a goal-setting framework that combines:
- **Objectives:** Qualitative, inspiring goals
- **Key Results:** Quantitative measures of success

### OKR Structure

```
OBJECTIVE: [What we want to achieve - inspiring, qualitative]
│
├── KR1: [Measure 1 - specific, measurable, time-bound]
├── KR2: [Measure 2]
└── KR3: [Measure 3]
```

**Rule:** 3-5 Objectives, each with 3-5 Key Results.

### Objective Characteristics

**Good Objectives are:**

| Characteristic | Description | Example |
|----------------|-------------|---------|
| Inspiring | Motivates the team | "Delight our users" |
| Qualitative | Not a number | "Build world-class onboarding" |
| Time-bound | Clear period | "This quarter" |
| Ambitious | Stretch goal | "Industry-leading retention" |
| Memorable | Easy to recall | Short, punchy |

**Bad Objectives:**
- "Increase signups by 20%" (that's a KR)
- "Launch feature X" (that's a task)
- "Improve stuff" (too vague)

### Key Result Characteristics

**Good KRs are:**

| Characteristic | Description | Example |
|----------------|-------------|---------|
| Measurable | Clear number | "Reduce churn from 5% to 3%" |
| Specific | No ambiguity | "NPS score of 50+" |
| Time-bound | Deadline | "By end of Q2" |
| Outcome-focused | Not output | "Activation rate 60%" not "ship 5 features" |
| Challenging | 70% confidence | Stretch but achievable |

**Scoring:**
- 0.0-0.3 = Failed
- 0.4-0.6 = Progress made
- 0.7-1.0 = Success (0.7 is ideal target)

### OKR Setting Process

#### Step 1: Align to Strategy

**Inputs:**
- Company mission/vision
- Annual goals
- Previous period learnings
- Market conditions

**Question:** What must we accomplish this quarter to move toward our vision?

#### Step 2: Draft Objectives

**Brainstorm:**
1. What's most important right now?
2. If we could only achieve one thing, what would it be?
3. What would make this quarter a success?

**Limit:** 3-5 objectives maximum.

#### Step 3: Define Key Results

**For each Objective:**
1. How will we know we achieved it?
2. What metrics matter?
3. What's the target number?

**Test:** Can you answer with just a number at EOQ?

#### Step 4: Validate

**Checklist:**
- [ ] Objectives are inspiring and qualitative
- [ ] KRs are measurable outcomes (not tasks)
- [ ] 70% confidence on achieving KRs
- [ ] Connected to higher-level goals
- [ ] Not too many (focus!)

#### Step 5: Communicate & Commit

- Share with stakeholders
- Get buy-in
- Make visible (dashboard, wiki)

#### Step 6: Track & Adjust

- Weekly check-ins
- Monthly scoring
- EOQ retrospective

---

## Templates

### OKR Template

```markdown
## OKRs: [Team/Product] - [Quarter Year]

### Objective 1: [Inspiring goal statement]

**Why this matters:** [Context and strategic connection]

| Key Result | Baseline | Target | Current | Score |
|------------|----------|--------|---------|-------|
| KR 1.1: [Measurable outcome] | [Starting point] | [Goal] | [Now] | [0-1] |
| KR 1.2: [Measurable outcome] | [Starting point] | [Goal] | [Now] | [0-1] |
| KR 1.3: [Measurable outcome] | [Starting point] | [Goal] | [Now] | [0-1] |

**Owner:** [Name]
**Status:** [On Track / At Risk / Off Track]

---

### Objective 2: [Inspiring goal statement]

**Why this matters:** [Context]

| Key Result | Baseline | Target | Current | Score |
|------------|----------|--------|---------|-------|
| KR 2.1: | | | | |
| KR 2.2: | | | | |
| KR 2.3: | | | | |

---

### Summary

| Objective | Avg Score | Status |
|-----------|-----------|--------|
| O1 | [X] | [Status] |
| O2 | [X] | [Status] |

### Last Updated: [Date]
```

### Weekly OKR Check-in

```markdown
## OKR Check-in: Week [X] of [Quarter]

### Overall Progress
- On Track: [X] KRs
- At Risk: [X] KRs
- Off Track: [X] KRs

### By Objective

#### O1: [Name]
| KR | Progress | Confidence | Notes |
|----|----------|------------|-------|
| KR 1.1 | [X]% | High/Med/Low | [Updates] |
| KR 1.2 | [X]% | High/Med/Low | [Updates] |

**Blockers:** [Any blockers]
**Help needed:** [Requests]

#### O2: [Name]
...

### Actions This Week
1. [Action to improve KR X]
2. [Action to unblock Y]

### Risks & Concerns
- [Risk 1]
- [Risk 2]
```

---

## Examples

### Example 1: SaaS Product OKRs

**O1: Achieve product-market fit**
- KR1: Increase "very disappointed" survey response from 25% to 40%
- KR2: Improve Day 30 retention from 20% to 35%
- KR3: Reach 100 paying customers with <10% monthly churn

**O2: Build scalable acquisition engine**
- KR1: Launch content marketing, publish 12 blog posts
- KR2: Achieve 5,000 monthly organic visitors
- KR3: Reduce CAC from $200 to $100

**O3: Delight early adopters**
- KR1: NPS score of 50+
- KR2: Average support response time under 4 hours
- KR3: 10 customer testimonials collected

### Example 2: Solo Creator OKRs

**O1: Establish newsletter as primary channel**
- KR1: Grow subscriber list from 500 to 2,000
- KR2: Maintain 45%+ open rate
- KR3: Convert 50 subscribers to paid product

**O2: Launch first digital product**
- KR1: Complete and launch course by [date]
- KR2: Generate $5,000 in first month
- KR3: Achieve 4.5+ star rating from first 20 customers

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| KRs are tasks | Focus on outcomes, not outputs |
| Too many OKRs | Max 3-5 objectives |
| 100% targets | Aim for 70% achievable (stretch) |
| Set and forget | Weekly check-ins |
| Sandbagging | Celebrate ambitious failure |
| No baseline | Always know starting point |
| Not connected | Link to company strategy |
| Punishing misses | OKRs are learning tools |

---

## Related Methodologies

- **success-metrics-definition:** Success Metrics Definition
- **roadmap-design:** Roadmap Design
- **north-star-metric:** North Star Metric
- **stakeholder-engagement:** Stakeholder Engagement
- **quality-management:** Quality Management

---

## Agent

**faion-mlp-impl-planner-agent** helps with OKRs. Invoke with:
- "Help me set OKRs for [quarter/product]"
- "Is this a good Key Result: [description]?"
- "Review my OKRs: [list]"
- "How should I track [OKR set]?"

---

*Methodology | Product | Version 1.0*
