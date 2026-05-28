# Analytics Framework

## Purpose

Establish what to measure, how to track it, and how to make decisions from data. You can't improve what you don't measure.

---

## Metrics Hierarchy

### North Star Metric

**Definition:** The one metric that best captures the value you deliver to customers.

**Characteristics:**
- Correlates with revenue
- Reflects user value
- Leading indicator
- Within your control

**Examples:**
| Product Type | North Star |
|--------------|------------|
| SaaS | Weekly active users |
| Marketplace | Transactions completed |
| Content | Time spent reading |
| Tool | Actions completed |

### Supporting Metrics

Build a hierarchy:

```
         NORTH STAR METRIC
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 ACQUISITION RETENTION  REVENUE
    │          │          │
    ▼          ▼          ▼
 Traffic    DAU/WAU     MRR
 Signups    D7 Ret.     ARPU
 CAC        Churn       LTV
```

---

## The AARRR Framework (Pirate Metrics)

### Overview

| Stage | Question | Key Metrics |
|-------|----------|-------------|
| **Acquisition** | How do users find us? | Traffic, channels, cost |
| **Activation** | Do they have a great first experience? | Sign-up rate, onboarding |
| **Retention** | Do they come back? | DAU/MAU, D1/D7/D30 |
| **Revenue** | Do they pay? | Conversion, MRR, LTV |
| **Referral** | Do they tell others? | NPS, K-factor |

### Acquisition Metrics

| Metric | Formula | What it Tells You |
|--------|---------|-------------------|
| Traffic | Unique visitors | Reach |
| Traffic by channel | Visitors per source | What's working |
| Cost per visit | Spend / visits | Channel efficiency |
| CAC | Spend / new customers | Acquisition cost |

### Activation Metrics

| Metric | Formula | What it Tells You |
|--------|---------|-------------------|
| Sign-up rate | Signups / visitors | Landing page effectiveness |
| Onboarding completion | Completed / started | First experience quality |
| Time to value | Time to "aha moment" | Onboarding friction |
| Setup completion | % with setup done | Product readiness |

### Retention Metrics

| Metric | Formula | What it Tells You |
|--------|---------|-------------------|
| DAU/MAU ratio | DAU / MAU | Engagement intensity |
| D1 retention | Users Day 1 / Signed up | First day experience |
| D7 retention | Users Day 7 / Signed up | Short-term stickiness |
| D30 retention | Users Day 30 / Signed up | Long-term retention |
| Churn rate | Lost customers / Total | Customer loss rate |

### Revenue Metrics

| Metric | Formula | What it Tells You |
|--------|---------|-------------------|
| MRR | Monthly recurring revenue | Revenue scale |
| ARPU | Revenue / Users | Revenue per user |
| LTV | ARPU × Average lifespan | Customer value |
| Conversion rate | Paid / Free users | Monetization |

### Referral Metrics

| Metric | Formula | What it Tells You |
|--------|---------|-------------------|
| NPS | Promoters - Detractors | Likelihood to recommend |
| K-factor | Invites × Conversion | Virality |
| Referral rate | Referred / Total users | Word of mouth |

---

## Setting Up Analytics

### Essential Events to Track

**Acquisition:**
- Page view
- Landing page visits
- Source/medium/campaign

**Activation:**
- Sign-up started
- Sign-up completed
- Onboarding step X completed
- First [key action]

**Engagement:**
- Session started
- Feature X used
- [Core action] completed

**Revenue:**
- Checkout started
- Purchase completed
- Subscription changed

### Event Naming Convention

```
[Object]_[Action]

Examples:
- user_signed_up
- project_created
- subscription_started
- feature_used
```

### Properties to Include

| Event | Properties |
|-------|------------|
| user_signed_up | source, plan, referrer |
| project_created | template_used, project_type |
| subscription_started | plan, price, trial |

---

## Cohort Analysis

### What is a Cohort?

A group of users who share a common characteristic (usually signup date).

### Basic Retention Cohort

| Cohort | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|--------|
| Jan 1 | 100% | 40% | 30% | 25% | 20% |
| Jan 8 | 100% | 45% | 35% | 28% | - |
| Jan 15 | 100% | 50% | 38% | - | - |

**What to look for:**
- Improving over time? (Later cohorts better)
- Stabilizing? (Flat after certain point)
- Declining? (Problem with experience)

### Cohort Query (Supabase)

```sql
WITH cohorts AS (
  SELECT
    id,
    date_trunc('week', created_at) as cohort_week,
    created_at
  FROM profiles
),
activity AS (
  SELECT
    user_id,
    date_trunc('week', created_at) as activity_week
  FROM events
  WHERE event_name = 'session_started'
)
SELECT
  c.cohort_week,
  a.activity_week,
  COUNT(DISTINCT c.id) as users
FROM cohorts c
LEFT JOIN activity a ON c.id = a.user_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

## Dashboard Design

### Executive Dashboard

| Section | Metrics |
|---------|---------|
| North Star | {Primary metric} + trend |
| Acquisition | New users, traffic, CAC |
| Activation | Conversion rate, onboarding % |
| Retention | D7 retention, DAU/MAU |
| Revenue | MRR, growth rate |

### Operational Dashboard

**Daily check:**
- Sign-ups today
- Active users today
- Errors/issues
- Support tickets

**Weekly review:**
- Funnel conversion
- Retention trends
- Revenue metrics
- Experiment results

---

## Tools

### Analytics Tools

| Tool | Best For | Cost |
|------|----------|------|
| Vercel Analytics | Basic web stats | Free |
| Plausible | Privacy-focused | $9/mo |
| PostHog | Product analytics | Free tier |
| Mixpanel | Event tracking | Free tier |
| Amplitude | Product analytics | Free tier |

### For Solo Builders

**Recommended stack:**
1. **Vercel Analytics** - Basic traffic (free)
2. **PostHog or Plausible** - Events (free tier)
3. **Supabase queries** - Custom analysis (included)

---

## Making Decisions

### Data-Informed vs Data-Driven

| Data-Driven | Data-Informed |
|-------------|---------------|
| Only do what data says | Data + intuition + context |
| Can miss innovation | Balanced approach |
| Reactive | Proactive |

**Solo builder tip:** Be data-informed. You don't have enough data for pure data-driven decisions.

### Reading Metrics

**Ask:**
1. Is this statistically significant?
2. What's the sample size?
3. What else changed?
4. Is this a trend or noise?
5. What action does this suggest?

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Vanity metrics | Feel good, don't matter | Focus on actionable |
| Survivorship bias | Ignore churned users | Include all users |
| Small samples | Noise looks like signal | Wait for significance |
| Correlation ≠ causation | Misleading conclusions | A/B test to prove |

---

## Output Format

```markdown
## Analytics Setup

### North Star Metric
**Metric:** {metric name}
**Current:** {value}
**Target:** {target}

### Key Metrics Dashboard

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| {metric} | {value} | {target} | {🟢/🟡/🔴} |

### Events Tracked
| Event | Trigger | Properties |
|-------|---------|------------|
| {event} | {when} | {props} |

### Cohort Health
{Retention cohort table}

### Key Insights
1. {insight}
2. {insight}
3. {insight}
```
