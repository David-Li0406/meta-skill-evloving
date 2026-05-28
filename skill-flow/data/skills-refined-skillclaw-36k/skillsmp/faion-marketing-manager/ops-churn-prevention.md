---
id: churn-prevention
name: "Churn Prevention"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Churn Prevention

## Metadata

| Field | Value |
|-------|-------|
| **ID** | churn-prevention |
| **Name** | Churn Prevention |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | subscription-models, customer-success, onboarding-emails |

---

## Problem

You're acquiring customers, but they keep leaving. Every churned customer costs you the acquisition spend plus all future revenue. At 5% monthly churn, you lose half your customers every year. Reducing churn from 5% to 3% can double your customer lifetime value.

Churn prevention means identifying why customers leave and stopping them before they do.

---

## Framework

Churn prevention follows this approach:

```
MEASURE   -> Know your churn rate and patterns
IDENTIFY  -> Find leading indicators
SEGMENT   -> Understand who churns and why
INTERVENE -> Act before they leave
RECOVER   -> Win back churned customers
```

### Step 1: Measure Churn

**Churn types:**

| Type | Definition | Formula |
|------|------------|---------|
| **Customer churn** | Customers who left | Lost / Starting customers |
| **Revenue churn** | Revenue lost | Lost MRR / Starting MRR |
| **Logo churn** | Accounts lost | Same as customer churn |
| **Net revenue retention** | Revenue including expansion | (Start + Expansion - Churn) / Start |

**Churn benchmarks:**

| Business Type | Monthly Churn | Annual Churn |
|---------------|---------------|--------------|
| Consumer SaaS | 5-7% | 45-60% |
| SMB SaaS | 3-5% | 30-45% |
| Mid-market | 1-2% | 10-20% |
| Enterprise | <1% | <10% |

**Calculate your churn:**
```
Monthly churn = Customers lost this month / Customers at start of month

Annual churn = 1 - (1 - monthly churn)^12
Example: 5% monthly = 1 - (0.95)^12 = 46% annual
```

### Step 2: Identify Warning Signs

**Leading indicators of churn:**

| Indicator | Signal | Risk Level |
|-----------|--------|------------|
| Login frequency | Decreasing logins | Medium |
| Feature usage | Using fewer features | High |
| Support tickets | Frustrated requests | High |
| Payment failures | Card declining | High |
| No engagement | Zero usage 14+ days | Critical |
| Feedback | Negative surveys | High |

**Build a health score:**

```
Health Score = (
  Login frequency (0-25) +
  Feature usage (0-25) +
  Support sentiment (0-25) +
  Account age (0-25)
) / 100

< 40 = At-risk
40-70 = Needs attention
> 70 = Healthy
```

### Step 3: Segment Churn Reasons

**Common churn reasons:**

| Reason | % of Churn | Preventable? |
|--------|------------|--------------|
| Not using product | 25-30% | Yes |
| Not seeing value | 20-25% | Yes |
| Switched to competitor | 15-20% | Sometimes |
| Budget/price | 15-20% | Partially |
| Business closed | 5-10% | No |
| Bad support experience | 5-10% | Yes |

**Churn survey:**
```markdown
We're sorry to see you go. To help us improve, could you share why?

- [ ] I wasn't using it enough
- [ ] It's too expensive
- [ ] Missing features I need
- [ ] Found a better alternative
- [ ] My needs changed
- [ ] Technical issues
- [ ] Other: [text field]
```

### Step 4: Intervene Early

**Intervention strategies by signal:**

| Signal | Intervention |
|--------|--------------|
| No login 7 days | Re-engagement email |
| No login 14 days | Personal outreach |
| Feature drop-off | "Did you know?" email |
| Support complaint | Manager follow-up |
| Cancel attempt | Save offer |
| Payment failure | Dunning sequence |

**Re-engagement email:**
```
Subject: We miss you, [Name]

Haven't seen you in a while. Is everything okay?

A few things you might have missed:
- [New feature]
- [Popular use case]

Need help? Just reply to this email.

[Your name]
```

**Save offer (at cancellation):**
```
Before you go...

We'd hate to lose you. How about:
- [ ] 50% off your next 2 months
- [ ] Free upgrade to [plan] for 1 month
- [ ] Pause your account for 30 days
- [ ] Schedule a call to discuss your needs

[Accept offer] [Continue cancellation]
```

### Step 5: Recover Churned Customers

**Win-back timing:**

| Time Since Churn | Message Focus | Offer |
|------------------|---------------|-------|
| 7 days | "Miss us?" | Extended trial |
| 30 days | "What's changed" | Discount |
| 90 days | New features | Fresh start |
| 6 months | Major update | Special offer |

**Win-back email:**
```
Subject: A lot has changed since you left

Hi [Name],

Since you left [X months ago], we've:
- Added [feature they requested]
- Fixed [issue they had]
- Improved [relevant area]

Would you give us another try?

[Special offer: X% off / free month]

[CTA: Come back]
```

---

## Templates

### Churn Analysis Dashboard

```markdown
## Churn Report: [Month]

### Overview
- Starting MRR: $X
- Churned MRR: $X
- Expansion MRR: $X
- Net change: $X

- Customer churn: X%
- Revenue churn: X%
- Net revenue retention: X%

### Churn by Reason
| Reason | Customers | MRR Lost | % |
|--------|-----------|----------|---|
| Not using | X | $X | X% |
| Price | X | $X | X% |
| Competitor | X | $X | X% |
| Other | X | $X | X% |

### Churn by Cohort
| Cohort | Start | Churned | Rate |
|--------|-------|---------|------|
| Jan | X | X | X% |
| Feb | X | X | X% |
| Mar | X | X | X% |

### At-Risk Accounts
| Account | Health Score | MRR | Issue | Action |
|---------|--------------|-----|-------|--------|
| [Name] | 35 | $X | No login | Outreach |
```

### Churn Prevention Playbook

```markdown
## Churn Prevention Playbook

### Early Warning Triggers
| Trigger | Condition | Action |
|---------|-----------|--------|
| No login | >7 days | Auto-email |
| No login | >14 days | Personal email |
| Support ticket | Negative sentiment | Escalate |
| Feature usage | <20% of norm | "Tips" email |
| Health score | <40 | Manual review |

### Save Offers
| Segment | Offer | Discount |
|---------|-------|----------|
| Price objection | 50% off 2 months | 50% |
| Time objection | Pause 30 days | N/A |
| Feature gap | Upgrade trial | Free upgrade |

### Win-Back Campaigns
| Timing | Subject | Offer |
|--------|---------|-------|
| Day 7 | "We want you back" | 30% off |
| Day 30 | "What's new" | Free month |
| Day 90 | "Major update" | 50% off |
```

---

## Examples

### Example 1: SaaS Churn Reduction

**Problem:** 7% monthly churn

**Analysis:**
- 40% churned without using product
- 30% cited price
- 30% other reasons

**Actions:**
1. Added onboarding sequence
2. Implemented health scoring
3. Created save offer (50% off)
4. Launched win-back campaign

**Results:**
- Churn reduced to 4%
- Save offer converts 25%
- Win-back recovers 10%

### Example 2: Membership Churn

**Problem:** Annual members not renewing

**Analysis:**
- Most churn at year 1 renewal
- Low engagement last 3 months
- "Got what I needed" reason

**Actions:**
1. Quarterly check-ins
2. New content announcements
3. Renewal discount for multi-year
4. Community engagement push

**Results:**
- First-year retention: 60% → 75%
- Multi-year commitments: 20%

---

## Implementation Checklist

### Measurement
- [ ] Calculate monthly churn rate
- [ ] Calculate revenue churn
- [ ] Set up churn tracking
- [ ] Implement exit survey

### Early Warning
- [ ] Define leading indicators
- [ ] Build health score
- [ ] Set up alerts
- [ ] Create at-risk dashboard

### Prevention
- [ ] Design re-engagement emails
- [ ] Create save offer flow
- [ ] Train on objection handling
- [ ] Set up dunning sequence

### Recovery
- [ ] Plan win-back campaigns
- [ ] Create win-back emails
- [ ] Track win-back success
- [ ] Learn from churned feedback

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Only measuring churn | Too late to act | Track leading indicators |
| No exit survey | Don't learn reasons | Ask every churner |
| Generic save offer | Doesn't address issue | Segment by reason |
| Giving up after cancel | Missing recovery | Run win-back campaigns |
| Ignoring low usage | Silent churn | Monitor engagement |
| Blaming customers | Don't improve | Own the problem |

---

## Churn Reduction Priorities

| Action | Impact | Effort | Priority |
|--------|--------|--------|----------|
| Onboarding improvement | High | Medium | 1 |
| Save offer implementation | High | Low | 2 |
| Health score alerts | Medium | Medium | 3 |
| Win-back campaigns | Medium | Low | 4 |
| Feature adoption emails | Medium | Low | 5 |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Analytics | Mixpanel, Amplitude, Heap |
| Health scoring | Vitally, Totango, Custom |
| Email | Customer.io, Intercom |
| Surveys | Typeform, SurveyMonkey |
| Dunning | Stripe, Churnkey, Chargebee |

---

## Related Methodologies

- **subscription-models:** Subscription Models (retention design)
- **customer-success:** Customer Success (proactive retention)
- **onboarding-emails:** Onboarding Emails (first-month retention)
- **customer-support:** Customer Support (satisfaction and retention)

---

*Methodology: churn-prevention | Operations & Business | faion-growth-agent*
