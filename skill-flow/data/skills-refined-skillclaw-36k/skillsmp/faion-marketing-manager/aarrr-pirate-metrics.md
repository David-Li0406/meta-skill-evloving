---
id: aarrr-pirate-metrics
name: "AARRR Pirate Metrics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# AARRR Pirate Metrics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | aarrr-pirate-metrics |
| **Name** | AARRR Pirate Metrics |
| **Category** | Growth |
| **Difficulty** | Beginner |
| **Agent** | faion-growth-agent |
| **Related** | north-star-metric, cohort-analysis, funnel-optimization |

---

## Problem

You need a framework to measure and optimize the entire customer journey. Without it, you focus on vanity metrics like page views instead of metrics that drive revenue.

Most startups track everything or nothing. Both approaches fail. You need 5 key metrics that tell the complete story of your growth.

---

## Framework

AARRR (also called "Pirate Metrics") breaks the customer journey into 5 stages:

```
Acquisition → Activation → Retention → Revenue → Referral
     ↓            ↓            ↓          ↓          ↓
 How users     First       Coming     Making    Spreading
 find you      value       back       money     the word
```

### Stage 1: Acquisition

**Question:** How do users find you?

**Metrics:**
- Website visitors (by channel)
- App downloads
- Sign-ups
- Cost per acquisition (CPA)

**Channels to track:**
- Organic search (SEO)
- Paid ads (Google, Meta, LinkedIn)
- Social media
- Referrals
- Direct traffic
- Email

**Formula:**
```
CPA = Total Marketing Spend / Number of New Users
```

### Stage 2: Activation

**Question:** Do users have a great first experience?

**Metrics:**
- Sign-up completion rate
- Onboarding completion rate
- Time to first value (TTFV)
- Activation rate

**Formula:**
```
Activation Rate = Users Who Completed Key Action / Total Sign-ups x 100%
```

**Key action examples:**
- Completed profile
- Made first post
- Sent first message
- Created first project

### Stage 3: Retention

**Question:** Do users come back?

**Metrics:**
- Day 1, Day 7, Day 30 retention
- Weekly active users (WAU)
- Monthly active users (MAU)
- Churn rate

**Formula:**
```
D7 Retention = Users Active on Day 7 / Users Who Signed Up 7 Days Ago x 100%

Churn Rate = Users Lost This Period / Users at Start of Period x 100%
```

**Benchmarks (SaaS):**
- Good D1 retention: 40-60%
- Good D7 retention: 20-30%
- Good D30 retention: 10-15%

### Stage 4: Revenue

**Question:** How do you make money?

**Metrics:**
- Monthly Recurring Revenue (MRR)
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (LTV)
- Conversion rate (free to paid)

**Formulas:**
```
MRR = Number of Paying Customers x Average Monthly Price

ARPU = Total Revenue / Number of Users

LTV = ARPU x Average Customer Lifespan (months)
```

### Stage 5: Referral

**Question:** Do users tell others?

**Metrics:**
- Net Promoter Score (NPS)
- Referral rate
- Viral coefficient (K-factor)
- Referral revenue

**Formula:**
```
K-factor = Invites Sent x Conversion Rate of Invites

Referral Rate = Users Who Referred / Total Users x 100%
```

---

## Templates

### AARRR Dashboard Template

```markdown
## Weekly AARRR Report - Week of [DATE]

### Acquisition
| Channel | Visitors | Sign-ups | CPA | Change |
|---------|----------|----------|-----|--------|
| Organic | 5,000 | 500 | $0 | +12% |
| Paid | 3,000 | 300 | $5 | -3% |
| Social | 1,000 | 50 | $0 | +25% |
| **Total** | **9,000** | **850** | **$1.76** | **+10%** |

### Activation
- Activation rate: 45% (target: 50%)
- Avg time to first value: 4 min (target: <3 min)
- Onboarding completion: 68%

### Retention
| Cohort | D1 | D7 | D30 |
|--------|-----|-----|------|
| This week | 52% | - | - |
| Last week | 48% | 22% | - |
| 4 weeks ago | 50% | 21% | 12% |

### Revenue
- MRR: $45,000 (+5%)
- New MRR: $3,500
- Churned MRR: $1,200
- ARPU: $45

### Referral
- Referrals sent: 340
- Referral conversions: 68 (20%)
- K-factor: 0.08
```

### One-Page AARRR Tracker

```markdown
# AARRR Metrics - [Product Name]

## North Star Metric: [Your NSM]

## Funnel (Last 30 Days)

Acquisition:  [===========================] 10,000 visitors
                           ↓ 8%
Activation:   [==========] 800 activated users
                           ↓ 25%
Retention:    [======] 200 retained (D30)
                           ↓ 5%
Revenue:      [==] 10 paying customers
                           ↓ 20%
Referral:     [=] 2 referrals

## Key Actions This Week
1. Improve activation: [specific action]
2. Reduce churn: [specific action]
3. Increase referral rate: [specific action]
```

---

## Examples

### Example 1: SaaS Product

**Product:** Project management tool

| Stage | Metric | Current | Target | Status |
|-------|--------|---------|--------|--------|
| Acquisition | Monthly signups | 2,000 | 2,500 | Below |
| Activation | Completed 1st project | 35% | 50% | Below |
| Retention | D30 retention | 18% | 20% | Close |
| Revenue | Free to paid conversion | 3% | 5% | Below |
| Referral | K-factor | 0.05 | 0.15 | Below |

**Priority:** Activation (35% is too low)

**Action:** Simplify onboarding, add interactive tutorial

### Example 2: E-commerce

**Product:** Online store

| Stage | Metric | Value |
|-------|--------|-------|
| Acquisition | Monthly visitors | 50,000 |
| Activation | Add to cart rate | 12% |
| Retention | Repeat purchase rate (30d) | 8% |
| Revenue | Conversion rate | 2.5% |
| Referral | Share rate | 1% |

### Example 3: Mobile App

**Product:** Fitness app

```
ACQUISITION
- App store: 5,000 downloads/month
- CAC: $2.50

ACTIVATION
- Created first workout: 40%
- Time to first workout: 2 days

RETENTION
- D1: 55%
- D7: 30%
- D30: 15%

REVENUE
- Free to premium: 4%
- ARPU: $8/month
- LTV: $48

REFERRAL
- Invite sent rate: 5%
- Invite conversion: 15%
- K-factor: 0.075
```

---

## Implementation Checklist

- [ ] Identify key metric for each stage
- [ ] Set up tracking (analytics, product analytics)
- [ ] Define "activation" event clearly
- [ ] Create weekly dashboard
- [ ] Set targets for each metric
- [ ] Review weekly with team
- [ ] Prioritize worst-performing stage
- [ ] Run experiments to improve

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Tracking too many metrics | No focus, analysis paralysis | Pick ONE key metric per stage |
| Focusing only on acquisition | Users leak out at other stages | Fix worst stage first |
| Wrong activation metric | False signal of user value | Track action tied to retention |
| Ignoring referral | Missing free growth | Add referral program early |
| Not segmenting | Averages hide problems | Segment by cohort, channel, plan |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Web analytics | Google Analytics, Plausible, Mixpanel |
| Product analytics | Amplitude, Posthog, Heap |
| Retention | Mixpanel, Amplitude |
| Revenue | Stripe, ChartMogul, ProfitWell |
| Referral | ReferralCandy, Viral Loops |

---

## Further Reading

- Dave McClure's original "Startup Metrics for Pirates" (2007)
- Sean Ellis, "Hacking Growth"
- Andrew Chen, "The Cold Start Problem"

---

## Related Methodologies

- **north-star-metric:** North Star Metric (the one metric that matters most)
- **cohort-analysis:** Cohort Analysis (analyze retention properly)
- **funnel-optimization:** Funnel Optimization (fix conversion drop-offs)
- **viral-coefficient:** Viral Coefficient (maximize referral)

---

*Methodology: aarrr-pirate-metrics | Growth | faion-growth-agent*
