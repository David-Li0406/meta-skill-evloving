---
id: north-star-metric
name: "North Star Metric"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# North Star Metric

## Metadata

| Field | Value |
|-------|-------|
| **ID** | north-star-metric |
| **Name** | North Star Metric |
| **Category** | Growth |
| **Difficulty** | Beginner |
| **Agent** | faion-growth-agent |
| **Related** | aarrr-pirate-metrics, funnel-optimization, product-led-growth |

---

## Problem

Your team tracks 50 different metrics. Everyone has a different idea of what matters. Marketing optimizes for clicks. Product optimizes for features. Sales optimizes for revenue. The result: no alignment, no progress.

You need ONE metric that:
- Captures customer value
- Predicts long-term success
- Aligns the entire company

---

## Framework

### What is a North Star Metric?

The North Star Metric (NSM) is the single metric that best captures the core value your product delivers to customers.

**Characteristics:**
- Measures customer value, not company value
- Leading indicator of revenue
- Reflects product vision
- Actionable (teams can move it)
- Understandable by everyone

### Finding Your North Star Metric

```
Step 1: What is the core value your product provides?
        ↓
Step 2: What action shows customers received that value?
        ↓
Step 3: What metric measures that action?
        ↓
Step 4: Validate: Does improving this metric improve revenue?
```

### Framework: Value Equation

```
NSM = Action that delivers value x Frequency x Number of users
```

**Examples:**

| Product | Core Value | NSM |
|---------|-----------|-----|
| Airbnb | Unique stays | Nights booked |
| Spotify | Music enjoyment | Time spent listening |
| Slack | Team communication | Daily active users x Messages sent |
| Uber | Reliable transport | Rides completed |
| Netflix | Entertainment | Hours watched |
| Shopify | Merchant success | GMV (Gross Merchandise Volume) |

### Not a North Star Metric

| Metric | Why Not |
|--------|---------|
| Revenue | Lags, doesn't show value delivery |
| Sign-ups | No value exchange yet |
| Page views | Vanity, not value |
| DAU/MAU alone | Activity without value |

---

## Templates

### North Star Metric Definition Template

```markdown
# North Star Metric: [Your NSM]

## Definition
[Precise definition of how to calculate]

## Why This Metric?
1. **Customer value:** [How it represents value delivered]
2. **Revenue correlation:** [Evidence it predicts revenue]
3. **Actionability:** [What teams can do to move it]

## Current State
- Value: [number]
- Trend: [up/down/flat] [%] vs last period
- Target: [number] by [date]

## Input Metrics (Levers)
1. [Input 1] - owned by [team]
2. [Input 2] - owned by [team]
3. [Input 3] - owned by [team]

## Dashboard Link
[URL]
```

### Input Metrics Tree

```
                    North Star Metric
                          |
        +-----------------+-----------------+
        |                 |                 |
   New Users         Active Users      Value/User
        |                 |                 |
    +---+---+        +---+---+        +---+---+
    |   |   |        |   |   |        |   |   |
 [input metrics for each branch]
```

---

## Examples

### Example 1: Project Management Tool

**Product:** Task management SaaS

**Core value:** Helping teams complete work efficiently

**NSM candidates:**
1. Tasks completed
2. Projects completed
3. Active teams using daily
4. Tasks completed per active user

**Chosen NSM:** Weekly tasks completed per active team

**Why:**
- Shows value delivery (work getting done)
- Combines engagement + value
- Correlates with retention and revenue

**Input metrics:**
- Number of active teams (growth)
- Tasks created per team (adoption)
- Task completion rate (product quality)

### Example 2: E-learning Platform

**Product:** Online courses

**Core value:** Helping people learn new skills

**NSM:** Lessons completed

**Why not "Hours watched":** Watching isn't learning. Completion means value.

**Input metrics:**
- New enrollments
- Enrollment to start rate
- Lesson completion rate
- Re-engagement (returning students)

### Example 3: Marketplace

**Product:** Freelance platform

**Core value:** Connecting clients with freelancers for successful projects

**NSM:** Projects completed with positive review

**Why:**
- Shows successful value exchange
- Both sides happy
- Predicts repeat usage

**Input metrics:**
- Active freelancers
- Jobs posted
- Job-to-hire rate
- Delivery rate
- Satisfaction rate

---

## Implementation Checklist

### Phase 1: Define (Week 1)

- [ ] List your product's core value
- [ ] Brainstorm 5-10 candidate metrics
- [ ] Test each against criteria:
  - [ ] Measures customer value?
  - [ ] Leading indicator?
  - [ ] Actionable?
  - [ ] Simple to understand?
- [ ] Validate with data: Does it correlate with retention/revenue?
- [ ] Get leadership buy-in

### Phase 2: Instrument (Week 2)

- [ ] Define exact calculation
- [ ] Set up tracking
- [ ] Create dashboard
- [ ] Identify 3-5 input metrics
- [ ] Assign input metrics to teams

### Phase 3: Operationalize (Ongoing)

- [ ] Include in weekly reviews
- [ ] Set quarterly targets
- [ ] Align OKRs to NSM
- [ ] Review correlation quarterly

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Choosing revenue as NSM | Teams focus on short-term extraction | Pick metric that drives long-term revenue |
| Multiple North Stars | No alignment | Pick ONE. Use input metrics for teams |
| NSM too complex | Nobody understands it | Simplify: one sentence explanation |
| Not validating | Optimizing wrong thing | Prove correlation with revenue |
| Set and forget | Becomes outdated | Review quarterly |

---

## Validation Test

Your NSM is valid if:

```
When NSM goes UP:
  → Customer satisfaction goes UP
  → Retention goes UP
  → Revenue eventually goes UP

When NSM goes DOWN:
  → Churn increases
  → Revenue decreases
```

Run this correlation analysis quarterly.

---

## North Star vs OKRs

```
               North Star Metric
                      ↓
          Company-level Objective
                      ↓
    +--------+--------+--------+
    |        |        |        |
 Team KR   Team KR   Team KR   Team KR
    ↓        ↓        ↓        ↓
 [input metrics feeding into NSM]
```

**NSM:** What we optimize for (rarely changes)
**OKRs:** Quarterly goals that move the NSM

---

## Tools

| Purpose | Tools |
|---------|-------|
| Tracking | Amplitude, Mixpanel, Posthog |
| Dashboards | Metabase, Looker, Mode |
| Correlation analysis | Python/R, BigQuery |

---

## Industry Benchmarks

| Category | Typical NSM | Good Growth Rate |
|----------|-------------|------------------|
| B2B SaaS | Active teams, features used | 5-7% MoM |
| Consumer app | DAU, actions per user | 3-5% WoW |
| Marketplace | Transactions | 10-15% MoM |
| E-commerce | Repeat purchases | 5% MoM |
| Media | Time spent, content consumed | 2-3% WoW |

---

## Related Methodologies

- **aarrr-pirate-metrics:** AARRR Pirate Metrics (NSM fits within this framework)
- **funnel-optimization:** Funnel Optimization (optimize funnel toward NSM)
- **product-led-growth:** Product-Led Growth (NSM drives PLG strategy)

---

*Methodology: north-star-metric | Growth | faion-growth-agent*
