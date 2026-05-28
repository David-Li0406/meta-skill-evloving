---
id: success-metrics-definition
name: "Success Metrics Definition"
domain: RES
skill: faion-researcher
category: "research"
---

# Success Metrics Definition

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #metrics, #kpis |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Teams measure the wrong things or too many things. Common issues:
- Vanity metrics that don't drive decisions
- Too many KPIs, no focus
- Metrics that don't connect to business outcomes
- No targets or baselines

**The root cause:** No structured process for identifying what truly matters.

---

## Framework

### What are Success Metrics?

Success metrics are quantifiable measures that indicate whether you're achieving your goals. They answer: "How do we know if we're winning?"

### Metric Types

#### 1. Input vs Output Metrics

| Type | Description | Example |
|------|-------------|---------|
| Input (Leading) | Activities you control | Blog posts published |
| Output (Lagging) | Results of activities | Organic traffic |

**Rule:** Track both. Inputs predict outputs.

#### 2. Vanity vs Actionable Metrics

| Type | Description | Example |
|------|-------------|---------|
| Vanity | Looks good, not actionable | Total signups (ever) |
| Actionable | Drives decisions | Weekly active users |

**Test:** "If this metric changes, will we do something different?"

#### 3. Metric Hierarchy

```
North Star Metric
       │
       ├── Primary KPIs (3-5)
       │       │
       │       ├── Secondary metrics
       │       └── Leading indicators
       │
       └── Health metrics (guardrails)
```

### The AARRR Framework (Pirate Metrics)

**For each stage, define metrics:**

| Stage | Question | Example Metrics |
|-------|----------|-----------------|
| **Acquisition** | How do users find us? | Visitors, signups, CAC |
| **Activation** | Do they have a great first experience? | Onboarding completion, time to value |
| **Retention** | Do they come back? | DAU/MAU, churn rate |
| **Revenue** | Do they pay? | MRR, ARPU, LTV |
| **Referral** | Do they tell others? | NPS, referral rate, K-factor |

### Metric Definition Process

#### Step 1: Define Business Goals

**Template:**
```
Goal: [Objective statement]
Timeframe: [When]
Target: [Quantified result]
```

**Example:**
```
Goal: Achieve product-market fit
Timeframe: 6 months
Target: 40%+ would be "very disappointed" without product
```

#### Step 2: Identify North Star Metric

**Characteristics:**
- Measures core value delivered
- Leads to revenue
- Measurable and understandable
- Actionable

**Examples:**

| Product Type | North Star |
|--------------|------------|
| SaaS | Weekly active users |
| Marketplace | Transactions per week |
| Media | Time spent reading |
| E-commerce | Purchases per month |

#### Step 3: Break Down into Primary KPIs

**For each AARRR stage:**
- Primary metric (1)
- Target (quantified)
- Tracking method

**Limit:** 3-5 primary KPIs total.

#### Step 4: Set Targets

**Target-setting approaches:**

| Approach | How | When |
|----------|-----|------|
| Baseline + improvement | Current + X% | Have data |
| Benchmark | Industry average | No data |
| Goal-backward | What's needed to hit goal | Strategic |
| Experimental | Test and learn | New metric |

**Good target criteria:**
- Specific number
- Time-bound
- Achievable but challenging
- Based on data or research

#### Step 5: Establish Measurement

For each metric:
- Definition (exactly what counts)
- Data source
- Calculation method
- Reporting frequency
- Owner

---

## Templates

### Metrics Framework

```markdown
## Metrics Framework: [Product]

### Business Goals
1. [Goal 1]: [Target] by [Date]
2. [Goal 2]: [Target] by [Date]

### North Star Metric
**Metric:** [Name]
**Definition:** [Exactly what it measures]
**Current:** [Baseline]
**Target:** [Goal]
**Rationale:** [Why this metric]

### Primary KPIs

#### Acquisition
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| [Metric] | [Definition] | [X] | [Y] | [Name] |

#### Activation
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| [Metric] | [Definition] | [X] | [Y] | [Name] |

#### Retention
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| [Metric] | [Definition] | [X] | [Y] | [Name] |

#### Revenue
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| [Metric] | [Definition] | [X] | [Y] | [Name] |

#### Referral
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| [Metric] | [Definition] | [X] | [Y] | [Name] |

### Health Metrics (Guardrails)
| Metric | Threshold | Action if crossed |
|--------|-----------|-------------------|
| [Metric] | [Limit] | [What to do] |

### Reporting Cadence
- **Daily:** [Metrics]
- **Weekly:** [Metrics]
- **Monthly:** [Metrics]
```

### Metric Specification

```markdown
## Metric: [Name]

### Definition
**What it measures:** [Description]
**Formula:** [Calculation]

### Examples
- **Counts as:** [What's included]
- **Doesn't count as:** [What's excluded]

### Data Source
- **System:** [Where data comes from]
- **Query/Dashboard:** [Link]
- **Update frequency:** [How often]

### Targets
| Period | Target | Rationale |
|--------|--------|-----------|
| Q1 | [X] | [Why] |
| Q2 | [X] | [Why] |

### Segments
Break down by:
- [Segment 1]
- [Segment 2]

### Related Metrics
- **Leads to:** [Downstream metric]
- **Influenced by:** [Upstream metric]

### Owner
**Primary:** [Name]
**Backup:** [Name]

### Review
**Frequency:** [How often reviewed]
**Forum:** [Where discussed]
```

---

## Examples

### Example 1: B2B SaaS Metrics

**North Star:** Weekly Active Teams

**Primary KPIs:**

| Stage | Metric | Target |
|-------|--------|--------|
| Acquisition | Marketing Qualified Leads | 200/month |
| Activation | Onboarding completion (7 days) | 60% |
| Retention | Monthly logo retention | 95% |
| Revenue | Net Revenue Retention | 110% |
| Referral | NPS | 50+ |

**Guardrails:**
- Support tickets per user < 0.5/month
- Page load time < 2 seconds

### Example 2: Consumer App Metrics

**North Star:** Daily Active Users

**Primary KPIs:**

| Stage | Metric | Target |
|-------|--------|--------|
| Acquisition | Daily app installs | 500/day |
| Activation | Day 1 retention | 40% |
| Retention | Day 7 retention | 20% |
| Revenue | ARPDAU | $0.05 |
| Referral | Organic install % | 30% |

**Guardrails:**
- Crash rate < 0.5%
- App store rating > 4.5

### Example 3: Marketplace Metrics

**North Star:** Weekly GMV (Gross Merchandise Value)

**Primary KPIs:**

| Stage | Metric | Target |
|-------|--------|--------|
| Acquisition (Demand) | New buyer signups | 1000/week |
| Acquisition (Supply) | New seller signups | 100/week |
| Activation | First purchase rate | 25% |
| Retention | Repeat purchase rate (30 days) | 40% |
| Revenue | Take rate | 15% |

**Guardrails:**
- Search-to-purchase rate > 3%
- Seller satisfaction > 80%

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many metrics | Focus on 3-5 primary KPIs |
| No North Star | Define single most important metric |
| Vanity metrics | Test if metric drives decisions |
| No targets | Set quantified goals |
| Undefined metrics | Document exact definition |
| No baselines | Measure current state first |
| Ignoring segments | Break down by user type |

---

## Related Methodologies

- **business-model-research:** Business Model Research
- **okr-setting:** OKR Setting
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **north-star-metric:** North Star Metric
- **cohort-analysis:** Cohort Analysis

---

## Agent

**faion-market-researcher-agent** helps define metrics. Invoke with:
- "What metrics should I track for [product]?"
- "Define a North Star metric for [business]"
- "Set up an AARRR metrics framework for [product]"
- "What targets should I set for [metric]?"

---

*Methodology | Research | Version 1.0*
