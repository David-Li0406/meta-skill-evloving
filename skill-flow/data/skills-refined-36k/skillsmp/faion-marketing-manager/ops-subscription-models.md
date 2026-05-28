---
id: subscription-models
name: "Subscription Models"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Subscription Models

## Metadata

| Field | Value |
|-------|-------|
| **ID** | subscription-models |
| **Name** | Subscription Models |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | pricing-strategy, churn-prevention, upselling-cross-selling |

---

## Problem

One-time sales mean you're always hunting for the next customer. Revenue is unpredictable, customer relationships are transactional, and growth requires constant new acquisition. Subscriptions flip this: predictable revenue, ongoing relationships, and compound growth.

But subscriptions are hard. You need to deliver continuous value, manage churn, and balance acquisition with retention.

---

## Framework

Subscription success follows this path:

```
MODEL     -> Choose the right subscription type
PRICING   -> Set tiers that maximize LTV
ONBOARD   -> Ensure first value quickly
RETAIN    -> Keep customers paying
EXPAND    -> Grow revenue per customer
```

### Step 1: Choose Subscription Model

**Subscription types:**

| Model | How It Works | Best For |
|-------|--------------|----------|
| **SaaS** | Software access | Tools, platforms |
| **Membership** | Community/content access | Education, communities |
| **Replenishment** | Regular product delivery | Consumables |
| **Curation** | Curated selections | Discovery products |
| **Access** | Exclusive availability | Premium services |

**Billing frequency:**

| Frequency | Pros | Cons |
|-----------|------|------|
| Monthly | Low commitment, easier start | Higher churn |
| Annual | Lower churn, cash flow | Harder to sell |
| Weekly | Very low barrier | Very high churn |
| Usage-based | Fair, scales with value | Unpredictable revenue |

**Recommendation for most:** Offer both monthly and annual with annual discount.

### Step 2: Design Tier Structure

**Common tier strategies:**

**Good-Better-Best:**
```
Basic ($9)   -> Core features
Pro ($29)    -> Full features (anchor)
Team ($79)   -> Collaboration + support
```

**Freemium:**
```
Free         -> Limited, lead gen
Pro ($X)     -> Full product
```

**Usage + Base:**
```
Base ($29)   -> Platform access
+ $0.01      -> Per API call/action
```

**Feature allocation:**

| Feature Type | Free | Basic | Pro | Team |
|--------------|------|-------|-----|------|
| Core value | Limited | Yes | Yes | Yes |
| Advanced features | - | - | Yes | Yes |
| Collaboration | - | - | - | Yes |
| Support | Community | Email | Priority | Dedicated |
| Usage limits | Low | Medium | High | Custom |

### Step 3: Set Key Metrics

**Essential subscription metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| **MRR** | Sum of monthly recurring revenue | Growth goal |
| **ARR** | MRR x 12 | Annual planning |
| **Churn rate** | Customers lost / Total customers | < 5% monthly |
| **Revenue churn** | Revenue lost / Total revenue | < 3% monthly |
| **LTV** | ARPU / Churn rate | > 3x CAC |
| **LTV:CAC** | LTV / CAC | > 3:1 |
| **Expansion MRR** | Upgrades + add-ons | Offset churn |

**Healthy subscription business:**
```
Net Revenue Retention > 100%
(Expansion revenue > Churn revenue)
```

### Step 4: Optimize Billing

**Billing best practices:**

| Practice | Why It Matters |
|----------|----------------|
| Annual discount (2 months) | Reduces churn, improves cash flow |
| Card update prompts | Reduces involuntary churn |
| Grace period | Recovers failed payments |
| Dunning emails | Automated payment recovery |
| Easy cancellation | Builds trust, reduces disputes |

**Payment recovery:**
```
Day 0: Payment fails
Day 1: Email + retry
Day 3: Email + retry
Day 7: Email + final retry
Day 10: Downgrade to free
```

### Step 5: Manage Subscription Lifecycle

**Customer lifecycle stages:**

```
TRIAL    -> First value (Day 1-7)
ACTIVE   -> Regular usage (Ongoing)
AT-RISK  -> Usage declining (Warning signs)
CHURN    -> Cancellation
WIN-BACK -> Re-acquisition
```

**Interventions by stage:**

| Stage | Trigger | Action |
|-------|---------|--------|
| Trial | Day 1 | Onboarding email |
| Trial | Day 3 | Check-in, help |
| Trial | Day 7 | Conversion offer |
| Active | Monthly | Usage report |
| At-risk | Usage drop | Outreach |
| Churn | Cancel request | Save offer |
| Churned | Day 30 | Win-back campaign |

---

## Templates

### Subscription Business Model

```markdown
## Subscription Model: [Product]

### Model Type
- [ ] SaaS
- [ ] Membership
- [ ] Replenishment
- [ ] Curation

### Billing
- Monthly: $X
- Annual: $X (X months free)
- Usage component: [Yes/No]

### Tiers
| Tier | Price | Target | Key Feature |
|------|-------|--------|-------------|
| Free | $0 | [Persona] | [Feature] |
| Pro | $X/mo | [Persona] | [Feature] |
| Team | $X/mo | [Persona] | [Feature] |

### Key Metrics (Targets)
- MRR Goal: $X
- Churn target: <X%
- LTV target: $X
- LTV:CAC target: X:1

### Lifecycle Automation
- Trial Day 1: [Action]
- Trial Day 7: [Action]
- At-risk trigger: [Condition]
- Save offer: [Offer]
```

### Dunning Email Sequence

```markdown
## Payment Recovery Emails

### Email 1: Payment Failed (Day 1)
Subject: Quick fix needed for your [Product] subscription

Your payment didn't go through. This happens sometimes.
[Update payment method]
Your subscription continues while you sort this out.

### Email 2: Second Attempt (Day 3)
Subject: Your [Product] access needs attention

We tried charging your card again but no luck.
Update your payment to keep your [key feature] working.
[Update payment method]

### Email 3: Final Notice (Day 7)
Subject: Last chance to keep your [Product] subscription

Your subscription will be paused in 3 days unless we can process payment.
You'll lose access to:
- [Feature 1]
- [Feature 2]
- [Your data - stored for 30 days]

[Update payment method]
```

---

## Examples

### Example 1: SaaS Subscription

**Product:** Email marketing tool

**Tier structure:**
| Tier | Price | Contacts | Emails/mo |
|------|-------|----------|-----------|
| Starter | $19/mo | 1,000 | 10,000 |
| Growth | $49/mo | 5,000 | 50,000 |
| Pro | $99/mo | 15,000 | 150,000 |

**Results:**
- 40% choose Growth (anchor)
- Net revenue retention: 115%
- Monthly churn: 3%

### Example 2: Membership Site

**Product:** Developer learning community

**Tier structure:**
| Tier | Price | Access |
|------|-------|--------|
| Free | $0 | Public content |
| Member | $29/mo | All courses, community |
| VIP | $99/mo | + Live sessions, mentorship |

**Results:**
- 5% free-to-paid conversion
- 85% annual retention
- VIP: 2% of paid, 15% of revenue

---

## Implementation Checklist

### Setup
- [ ] Choose subscription model type
- [ ] Design tier structure
- [ ] Set up payment processor (Stripe/Paddle)
- [ ] Configure billing portal

### Automation
- [ ] Trial onboarding sequence
- [ ] Dunning/payment recovery
- [ ] Usage alerts
- [ ] Renewal reminders

### Metrics
- [ ] Dashboard for MRR, churn, LTV
- [ ] Cohort analysis setup
- [ ] Revenue recognition (if needed)

### Operations
- [ ] Cancellation flow
- [ ] Upgrade/downgrade paths
- [ ] Proration rules
- [ ] Refund policy

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No annual option | Higher churn, less cash | Offer 2 months free |
| Too many tiers | Decision paralysis | Max 3-4 tiers |
| Free tier too generous | No reason to upgrade | Limit strategically |
| No dunning | Lost revenue | Automate recovery |
| Hard cancellation | Bad reviews, chargebacks | Make it easy |
| Ignoring expansion | Missing revenue | Build upgrade paths |

---

## Subscription Metrics Formulas

| Metric | Formula |
|--------|---------|
| MRR | Sum of all monthly subscriptions |
| ARR | MRR x 12 |
| ARPU | MRR / Active customers |
| Churn rate | Churned / Starting customers |
| LTV | ARPU / Monthly churn rate |
| CAC payback | CAC / (ARPU x Gross margin) |
| Net retention | (Start MRR + Expansion - Churn) / Start MRR |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Payments | Stripe, Paddle, Chargebee |
| Analytics | Baremetrics, ProfitWell, ChartMogul |
| Dunning | Stripe (built-in), Churnkey |
| Customer success | Vitally, Gainsight |
| Billing portal | Stripe Portal, custom |

---

## Related Methodologies

- **pricing-strategy:** Pricing Strategy (setting prices)
- **churn-prevention:** Churn Prevention (reducing churn)
- **upselling-cross-selling:** Upselling & Cross-selling (expansion revenue)
- **free-trial-optimization:** Free Trial Optimization (trial conversion)

---

*Methodology: subscription-models | Operations & Business | faion-growth-agent*
