---
name: north-star-metrics
description: Define and align organization around a single North Star Metric (NSM) that captures product value, drives growth, and focuses team efforts. Framework for choosing NSM by product type (social, marketplace, SaaS, content) with input metrics breakdown.
---

# North Star Metrics

Align your organization around the one metric that best captures value delivered to customers.

## When to Use

- Team working on different priorities (lack of alignment)
- Need single metric to track product health
- Preparing OKRs or goal-setting
- Building growth model or forecasting
- Deciding which features to prioritize
- Communicating product strategy to stakeholders
- Measuring product-market fit progress

## Core Concept

**North Star Metric (NSM)** = The single metric that best captures the core value you deliver to customers.

**Why It Matters:**
- **Alignment:** Everyone knows what success looks like
- **Focus:** Easy to say "no" to projects that don't move NSM
- **Leading Indicator:** NSM predicts revenue/growth
- **Accountability:** Clear metric for each team's contribution

**Key Principle:** NSM is about galvanizing the organization, not perfect measurement.

---

## Workflow

### Step 1: Choose Your North Star Metric

**Good NSM Characteristics:**

```markdown
## NSM Quality Checklist

✅ **Expresses Value**
Does it measure value delivered to customers (not vanity metric)?
- Good: "Minutes of content watched" (value = entertainment)
- Bad: "Total signups" (doesn't measure value received)

✅ **Leading Indicator of Revenue**
Does increasing NSM predict revenue growth?
- Test: Plot NSM vs. revenue over time. Correlation >0.7?

✅ **Actionable**
Can team influence it through product/marketing decisions?
- Good: "Weekly active creators" (build creator tools)
- Bad: "Market size" (can't control external factor)

✅ **Understandable**
Can everyone on team explain it in one sentence?
- Good: "Books finished per family per month"
- Bad: "Composite engagement score (formula...)"

✅ **Measurable**
Can you track it accurately and frequently?
- Good: Event tracking in product analytics
- Bad: Requires manual surveys every quarter

❌ **Not Too Narrow**
Shouldn't optimize for one feature at expense of overall value
- Bad: "Number of messages sent" (could spam to game metric)
- Good: "Weekly active teams" (captures overall usage)

❌ **Not Too Broad**
Should be specific enough to drive decisions
- Bad: "Customer happiness" (too vague)
- Good: "% of customers rating product 9/10+" (specific)
```

---

### Step 2: NSM Patterns by Product Type

**Common North Star Metrics:**

```markdown
## NSM by Category

### SOCIAL / NETWORK PRODUCTS
**NSM:** Weekly Active Users (WAU) or Daily Active Users (DAU)
- Facebook: DAU, MAU
- WhatsApp: Number of messages sent
- Instagram: Daily active stories users

**Why:** Network effects = more active users = more value for everyone

**Input Metrics:**
- New user signups
- Activation rate (% completing first action)
- Retention (D1, D7, D30)
- Resurrection rate (dormant → active)

---

### CONTENT / MEDIA PRODUCTS
**NSM:** Time spent (hours consumed) or Content consumed (items)
- Netflix: Hours watched per subscriber
- Spotify: Hours listened per user
- YouTube: Watch time per user

**Why:** More consumption = more value delivered (entertainment, learning)

**Input Metrics:**
- Content supply (new titles added)
- Discovery (% finding content they want)
- Repeat usage rate
- Completion rate (finish video/song)

---

### PRODUCTIVITY / SAAS TOOLS
**NSM:** Weekly Active Teams or Value Created (tasks completed, docs created)
- Slack: Messages sent by teams
- Notion: Collaborative workspaces created
- Figma: Design files collaborated on

**Why:** More usage = solving more problems = more value

**Input Metrics:**
- Team invites sent
- Feature adoption (% using core features)
- Collaboration events (multiplayer actions)
- Integrations connected

---

### MARKETPLACE / PLATFORM
**NSM:** Completed Transactions (GMV or order volume)
- Airbnb: Nights booked
- Uber: Rides completed
- Etsy: Gross merchandise value (GMV)

**Why:** Transactions = value exchanged (buyer + seller win)

**Input Metrics:**
- Supply (active sellers/listings)
- Demand (active buyers/searches)
- Liquidity (match rate)
- Repeat transaction rate

---

### B2B SAAS (REVENUE-FOCUSED)
**NSM:** Revenue (ARR, MRR) or Paying Customers
- Salesforce: Annual Recurring Revenue (ARR)
- Stripe: Payment volume processed
- HubSpot: Monthly Recurring Revenue (MRR)

**Why:** For mature B2B, revenue is the clearest value signal

**Input Metrics:**
- New customer acquisition
- Expansion revenue (upsells)
- Retention (logo, net revenue)
- Contraction/churn

---

### E-COMMERCE / CONSUMER
**NSM:** Orders per Buyer or Revenue per Customer
- Amazon: Orders per prime member
- Shopify (merchant): GMV per store
- Instacart: Orders delivered per week

**Why:** Repeat purchases = solving recurring need = value

**Input Metrics:**
- New customer acquisition
- Order frequency
- Average order value (AOV)
- Retention rate
```

---

### Step 3: Break Down NSM into Input Metrics

**NSM = f(Input Metrics)**

```markdown
## Input Metric Framework

**CONCEPT:** NSM is the OUTPUT. Input metrics are INPUTS you can control.

**Example (Social Product):**
NSM: Weekly Active Users (WAU)

WAU = New Users × Activation Rate × Retention Rate × Resurrection Rate

**Input Metrics (what you can control):**
1. **Acquisition:** New signups per week
2. **Activation:** % who complete aha moment in first week
3. **Retention:** % still active after 4 weeks
4. **Resurrection:** % of dormant users who return

**Team Ownership:**
- Growth team → Acquisition
- Product/Onboarding team → Activation
- Engagement team → Retention
- Lifecycle Marketing → Resurrection

---

**Example (Marketplace):**
NSM: Completed Transactions per Week

Transactions = Supply × Demand × Match Rate × Conversion Rate

**Input Metrics:**
1. **Supply:** Active listings (sellers posting)
2. **Demand:** Active buyers (searches, browses)
3. **Match Rate:** % of searches finding relevant listings
4. **Conversion:** % of matches → completed purchase

**Team Ownership:**
- Supply team → Recruit/retain sellers
- Demand team → Buyer acquisition/marketing
- Product team → Search/discovery (match rate)
- Conversion team → Checkout flow, trust/safety

---

**Example (SaaS Tool):**
NSM: Weekly Active Teams Using Core Feature

Active Teams = New Teams × Onboarding Success × Retention × Feature Adoption

**Input Metrics:**
1. **New Teams:** Signups (free trials, paid)
2. **Onboarding:** % completing setup & first value
3. **Retention:** % still active after 30 days
4. **Feature Adoption:** % using core feature weekly

**Team Ownership:**
- Sales/Marketing → New Teams
- Onboarding team → Setup success
- Product team → Feature adoption + retention
```

---

### Step 4: Track and Communicate NSM

**Build NSM Dashboard:**

```markdown
## NSM Tracking System

**DASHBOARD COMPONENTS:**

1. **NSM Headline (Big Number)**
   - Current value (this week/month)
   - % change vs. last period
   - Trend line (last 12 weeks/months)

2. **Input Metrics (Breakdown)**
   - Show contribution of each input
   - Identify which inputs are improving/declining
   - Example: Retention up 5%, Acquisition down 10%

3. **Cohort Analysis**
   - NSM by signup cohort (are newer cohorts better?)
   - Helps identify if product is improving

4. **Segment Breakdown**
   - NSM by user type, geography, channel
   - Find what's working (double down) vs. not (fix or cut)

5. **Forecast**
   - Project NSM based on current trends
   - Scenario planning (what if we improve X by Y%?)

**COMMUNICATION CADENCE:**
- Daily: Internal team dashboard (automated)
- Weekly: Team standup (discuss movers)
- Monthly: All-hands presentation (progress + goals)
- Quarterly: Board/investor update (NSM + revenue)
```

---

### Step 5: Use NSM for Prioritization

**Decision Framework:**

```markdown
## NSM-Driven Prioritization

**When evaluating projects, ask:**
1. Which input metric does this improve?
2. By how much (expected impact)?
3. What's the confidence level (high/med/low)?
4. What's the effort (person-weeks)?

**PRIORITIZATION FORMULA:**
Priority = (Expected NSM Impact × Confidence) / Effort

**EXAMPLE:**

| Project | Input Metric | Impact | Confidence | Effort | Score |
|---------|-------------|---------|-----------|--------|-------|
| Improve onboarding | Activation | +5% | High (80%) | 4 weeks | 1.0 |
| Referral program | Acquisition | +10% | Med (50%) | 8 weeks | 0.6 |
| Email re-engagement | Resurrection | +3% | High (90%) | 2 weeks | 1.4 |

→ **Prioritize:** Email re-engagement (highest score)

**RED FLAGS:**
❌ Project doesn't clearly map to input metric
❌ Impact is "nice to have" but not measurable
❌ No way to validate if it worked (no A/B test plan)
```

---

### Step 6: Common NSM Mistakes

```markdown
## Anti-Patterns to Avoid

❌ **MISTAKE 1: Vanity Metric as NSM**
"Total signups" or "Page views"
→ Problem: Doesn't measure value delivered
→ Fix: Use activation or engagement metric instead

❌ **MISTAKE 2: Lagging Indicator**
"Revenue" for early-stage product
→ Problem: Can't iterate fast enough (takes months to see impact)
→ Fix: Use leading indicator that predicts revenue

❌ **MISTAKE 3: Too Many NSMs**
"Our NSMs are DAU, revenue, and NPS"
→ Problem: Team is confused about priorities
→ Fix: One NSM. Everything else is input metric or health metric.

❌ **MISTAKE 4: Unchangeable Metric**
"Our NSM is market size"
→ Problem: Team can't influence it
→ Fix: Choose metric you can move through product/marketing

❌ **MISTAKE 5: Gaming the Metric**
Optimizing for NSM in ways that harm long-term value
→ Example: Spammy notifications to boost DAU (but increases uninstalls)
→ Fix: Add health metrics (churn, NPS) as guardrails

❌ **MISTAKE 6: Ignoring Segments**
Averaging across user types (power users + casual)
→ Problem: Hides what's really happening
→ Fix: Break NSM down by segment, optimize for best segments

❌ **MISTAKE 7: Never Updating NSM**
Using same NSM as you scale from 0→1, 1→10, 10→100
→ Problem: Early-stage NSM may not work at scale
→ Fix: Re-evaluate NSM annually (but change rarely)
```

---

### Step 7: NSM Evolution by Stage

**NSM changes as company matures:**

```markdown
## Stage-Appropriate NSM

### PRE-PRODUCT-MARKET FIT
**NSM:** Retention (D7, D30) or Aha Moment Completion
- Focus: Are users getting value?
- Why: Revenue doesn't matter if users churn
- Example: "% of users who complete 3+ sessions"

---

### EARLY PRODUCT-MARKET FIT
**NSM:** Weekly/Monthly Active Users (WAU/MAU)
- Focus: Growth + engagement
- Why: Scale the user base that's retained
- Example: "Weekly active users"

---

### GROWTH STAGE
**NSM:** Value Delivered (transactions, content consumed, tasks completed)
- Focus: Maximize value per user
- Why: Monetization follows value
- Example: "Hours of content watched per subscriber"

---

### MATURE / PUBLIC COMPANY
**NSM:** Revenue (ARR, GMV) + Efficiency (Rule of 40)
- Focus: Profitable growth
- Why: Investors care about revenue and margins
- Example: "ARR" + "Growth % + Profit Margin %"
```

---

## NSM Communication Template

**When presenting NSM:**

```markdown
## NSM Presentation Format

**SLIDE 1: The North Star**
"Our North Star Metric is [X]"
- Definition: [One sentence]
- Why it matters: [Captures value we deliver]
- Current value: [Number]
- Goal: [Target by when]

**SLIDE 2: Input Metrics**
[X] is driven by:
1. [Input 1]: [Current value], [Target]
2. [Input 2]: [Current value], [Target]
3. [Input 3]: [Current value], [Target]

**SLIDE 3: Team Ownership**
- Team A owns [Input 1]
- Team B owns [Input 2]
- Team C owns [Input 3]

**SLIDE 4: This Quarter's Focus**
We're doubling down on [Input Y] because [reason].
- Initiative 1: [Project], [Expected impact]
- Initiative 2: [Project], [Expected impact]
```

---

## Related Skills

- `/product-market-fit` - NSM helps measure PMF progress
- `/retention-engagement` - Retention often key input metric
- `/user-onboarding` - Activation is common input metric
- `/okrs-goals` - Use NSM to set team OKRs

---

**Last Updated**: 2026-01-22
