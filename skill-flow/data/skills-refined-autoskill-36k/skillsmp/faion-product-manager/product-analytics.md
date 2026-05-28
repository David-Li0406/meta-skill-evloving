---
id: product-analytics
name: "Product Analytics"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Product Analytics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #analytics, #data |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Teams collect data but don't know what to do with it. Issues:
- Tracking everything, understanding nothing
- No connection between metrics and decisions
- Dashboards nobody looks at
- Analysis paralysis

**The root cause:** No framework for connecting analytics to product decisions.

---

## Framework

### What is Product Analytics?

Product analytics is measuring and analyzing user behavior to make better product decisions. It answers: "What are users doing and why?"

### Analytics Maturity Levels

| Level | Focus | Capabilities |
|-------|-------|--------------|
| 1. Basic | What happened | Page views, signups |
| 2. Intermediate | Who did what | User segmentation |
| 3. Advanced | Why and what if | Funnels, cohorts |
| 4. Predictive | What will happen | ML, forecasting |

**Start at Level 2 minimum.**

### Key Metric Categories

#### Acquisition
- Visitors, signups, sources
- Conversion rates
- Cost per acquisition

#### Activation
- Onboarding completion
- Time to value
- First key action

#### Engagement
- DAU/WAU/MAU
- Session frequency
- Feature usage

#### Retention
- D1, D7, D30 retention
- Cohort retention curves
- Churn rate

#### Revenue
- MRR, ARPU, LTV
- Upgrade/downgrade rates
- Revenue per cohort

### Analytics Implementation Process

#### Step 1: Define Key Questions

**Before implementing, answer:**
- What decisions will this data inform?
- What behavior are we trying to understand?
- What's the minimum we need to track?

**Bad:** "Track everything"
**Good:** "Track if users complete onboarding"

#### Step 2: Create Tracking Plan

**For each event:**
- Event name (standardized)
- When it fires
- Properties captured
- Owner

**Naming convention:**
```
[Object] [Action]
Example: Account Created, Feature Used, Upgrade Started
```

#### Step 3: Implement Tracking

**Best practices:**
- Server-side for critical events
- Client-side for UX insights
- Consistent user identification
- Property standardization

#### Step 4: Build Dashboards

**Dashboard types:**

| Dashboard | Purpose | Audience |
|-----------|---------|----------|
| Exec summary | High-level health | Leadership |
| Product health | Core metrics | Product team |
| Feature deep-dive | Specific feature | Feature owner |
| Experiment | Test results | Product/Growth |

#### Step 5: Establish Rituals

- **Daily:** Glance at key metrics
- **Weekly:** Review dashboard, note anomalies
- **Monthly:** Deep dive analysis
- **Quarterly:** Goal vs actual, planning

---

## Templates

### Tracking Plan

```markdown
## Tracking Plan: [Product]

### User Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| user_id | string | Unique user ID | "usr_123" |
| plan | string | Subscription tier | "pro" |
| signup_date | date | When they signed up | "2024-01-15" |
| company_size | number | Team size | 25 |

### Events

#### Onboarding Events

| Event | Trigger | Properties |
|-------|---------|------------|
| signup_started | Click signup button | source |
| signup_completed | Form submitted | method (email/google) |
| onboarding_step_completed | Each step done | step_name, duration |
| onboarding_completed | All steps done | total_duration |

#### Core Feature Events

| Event | Trigger | Properties |
|-------|---------|------------|
| [feature]_viewed | Page/modal opened | entry_point |
| [feature]_created | Item created | type, count |
| [feature]_shared | Share action | share_method |

#### Conversion Events

| Event | Trigger | Properties |
|-------|---------|------------|
| upgrade_initiated | Click upgrade | from_plan, to_plan |
| checkout_started | Enter payment | plan, billing_period |
| purchase_completed | Payment success | amount, plan |
| purchase_failed | Payment failed | error_type |
```

### Analytics Dashboard Spec

```markdown
## Dashboard: Product Health

### Purpose
Track overall product health and spot issues quickly.

### Metrics

| Metric | Formula | Target | Alert |
|--------|---------|--------|-------|
| DAU | Unique active users/day | [X] | <80% target |
| WAU | Unique active users/week | [X] | <80% target |
| D1 Retention | % back on day 1 | 40% | <35% |
| D7 Retention | % back on day 7 | 20% | <15% |
| Activation Rate | % completing onboarding | 60% | <50% |

### Charts

1. **DAU Trend** (7-day rolling)
2. **Retention Cohort** (weekly cohorts)
3. **Feature Usage** (top 5 features by usage)
4. **Conversion Funnel** (signup to paid)

### Segments
- By plan (free/paid)
- By cohort (signup week)
- By source (organic/paid)

### Refresh
- Real-time for DAU
- Daily for retention
- Weekly for cohorts
```

### Analysis Report Template

```markdown
## Analysis: [Topic]

### Question
[What we're trying to understand]

### Methodology
- Data source: [Tool/database]
- Time period: [Dates]
- Segments: [How split]
- Sample size: [N]

### Findings

#### Key Insight 1: [Title]
[Chart or table]
**Observation:** [What we see]
**Implication:** [What it means]

#### Key Insight 2: [Title]
...

### Recommendations
1. [Action based on findings]
2. [Action based on findings]

### Limitations
- [What we couldn't measure]
- [Potential biases]

### Next Steps
- [Follow-up analysis]
- [Experiment to run]
```

---

## Examples

### Example 1: Onboarding Analysis

**Question:** Why is activation low?

**Findings:**
- 60% start onboarding
- 40% complete step 1
- 15% complete step 3 (big drop)
- 10% fully activate

**Insight:** Step 3 (connect data source) has 62% dropoff.

**Root cause:** Integration takes too long, users give up.

**Action:** Add sample data option to skip integration.

### Example 2: Feature Usage Analysis

**Question:** Which features drive retention?

**Findings:**
| Feature | Usage | 30-day Retention |
|---------|-------|------------------|
| Dashboard | 90% | 45% |
| Reports | 30% | 75% |
| Integrations | 20% | 80% |

**Insight:** Low-usage features correlate with high retention.

**Action:** Promote Reports and Integrations in onboarding.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tracking everything | Start with key questions |
| No naming convention | Standardize event names |
| Only looking at averages | Segment and cohort |
| Vanity metrics | Focus on actionable metrics |
| No documentation | Maintain tracking plan |
| Dashboard overload | One dashboard per audience |
| Never analyzing | Schedule regular reviews |

---

## Related Methodologies

- **success-metrics-definition:** Success Metrics Definition
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **cohort-analysis:** Cohort Analysis
- **funnel-optimization:** Funnel Optimization
- **ab-testing-framework:** A/B Testing Framework

---

## Agent

**faion-market-researcher-agent** helps with analytics. Invoke with:
- "Create a tracking plan for [feature]"
- "What metrics should I track for [goal]?"
- "Analyze this data: [data]"
- "Design a dashboard for [audience]"

---

*Methodology | Product | Version 1.0*
