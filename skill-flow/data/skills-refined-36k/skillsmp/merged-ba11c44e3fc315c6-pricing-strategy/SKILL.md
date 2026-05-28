---
name: pricing-strategy
description: Use this skill when you need assistance with pricing decisions, packaging, or monetization strategy, including topics like 'freemium,' 'free trial,' 'pricing tiers,' and 'willingness to pay.'
---

# Pricing Strategy

You are an expert in SaaS pricing and monetization strategy with access to pricing research data and analysis tools. Your goal is to help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

## Before Starting

Gather this context (ask if not provided):

### 1. Business Context
- What type of product? (SaaS, marketplace, e-commerce, service)
- What's your current pricing (if any)?
- What's your target market? (SMB, mid-market, enterprise)
- What's your go-to-market motion? (self-serve, sales-led, hybrid)

### 2. Value & Competition
- What's the primary value you deliver?
- What alternatives do customers consider?
- How do competitors price?
- What makes you different/better?

### 3. Current Performance
- What's your current conversion rate?
- What's your average revenue per user (ARPU)?
- What's your churn rate?
- Any feedback on pricing from customers/prospects?

### 4. Goals
- Are you optimizing for growth, revenue, or profitability?
- Are you trying to move upmarket or expand downmarket?
- Any pricing changes you're considering?

---

## Pricing Fundamentals

### The Three Pricing Axes

Every pricing decision involves three dimensions:

**1. Packaging** — What's included at each tier?
- Features, limits, support level
- How tiers differ from each other

**2. Pricing Metric** — What do you charge for?
- Per user, per usage, flat fee
- How price scales with value

**3. Price Point** — How much do you charge?
- The actual dollar amounts
- The perceived value vs. cost

### Value-Based Pricing Framework

Price should be based on value delivered, not cost to serve:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Customer's perceived value of your solution            │
│  ────────────────────────────────────────────── $1000   │
│                                                         │
│  ↑ Value captured (your opportunity)                    │
│                                                         │
│  Your price                                             │
│  ────────────────────────────────────────────── $500    │
│                                                         │
│  ↑ Consumer surplus (value customer keeps)              │
│                                                         │
│  Next best alternative                                  │
│  ────────────────────────────────────────────── $300    │
│                                                         │
│  ↑ Differentiation value                                │
│                                                         │
│  Your cost to serve                                     │
│  ────────────────────────────────────────────── $50     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** Price between the next best alternative and perceived value. Cost is a floor, not a basis.

---

## Pricing Research Methods

### Van Westendorp Price Sensitivity Meter

The Van Westendorp survey identifies the acceptable price range for your product.

**The Four Questions:**

Ask each respondent:
1. "At what price would you consider [product] to be so expensive that you would not consider buying it?" (Too expensive)
2. "At what price would you consider [product] to be priced so low that you would question its quality?" (Too cheap)
3. "At what price would you consider [product] to be starting to get expensive, but you still might consider it?" (Expensive/high side)
4. "At what price would you consider [product] to be a bargain—a great buy for the money?" (Cheap/good value)

**How to Analyze:**

1. Plot cumulative distributions for each question
2. Find the intersections:
   - **Point of Marginal Cheapness (PMC):** "Too cheap" crosses "Expensive"
   - **Point of Marginal Expensiveness (PME):** "Too expensive" crosses "Cheap"
   - **Optimal Price Point (OPP):** "Too cheap" crosses "Too expensive"
   - **Indifference Price Point (IDP):** "Expensive" crosses "Cheap"

**The acceptable price range:** PMC to PME  
**Optimal pricing zone:** Between OPP and IDP

**Survey Tips:**
- Need 100-300 respondents for reliable data
- Segment by persona (different willingness to pay)
- Use realistic product descriptions
- Consider adding purchase intent questions

**Sample Van Westendorp Analysis Output:**

```
Price Sensitivity Analysis Results:
─────────────────────────────────
Point of Marginal Cheapness:  $29/mo
Optimal Price Point:          $49/mo
Indifference Price Point:     $59/mo
Point of Marginal Expensiveness: $79/mo

Recommended range: $49-59/mo
Current price: $39/mo (below optimal)
Opportunity: 25-50% price increase without significant demand impact
```

### MaxDiff Analysis (Best-Worst Scaling)

MaxDiff identifies which features customers value most, informing packaging decisions.

**How It Works:**

1. List 8-15 features you could include
2. Show respondents sets of 4-5 features at a time
3. Ask: "Which is MOST important? Which is LEAST important?"
4. Repeat across multiple sets until all features compared
5. Statistical analysis produces importance scores

**Example Survey Question:**

```
Which feature is MOST important to you?
Which feature is LEAST important to you?

□ Unlimited projects
□ Custom branding
□ Priority support
□ API access
□ Advanced analytics
```

**Analyzing Results:**

Features are ranked by utility score:
- High utility = Must-have (include in base tier)
- Medium utility = Differentiator (use for tier separation)
- Low utility = Nice-to-have (premium tier or cut)

**Using MaxDiff for Packaging:**

| Utility Score | Packaging Decision |
|---------------|-------------------|
| Top 20% | Include in all tiers (table stakes) |
| 20-50% | Use to differentiate tiers |
| 50-80% | Higher tiers only |
| Bottom 20% | Consider cutting or premium add-on |

### Willingness to Pay Surveys

**Direct method (simple but biased):**
"How much would you pay for [product]?"

**Better: Gabor-Granger method:**
"Would you buy [product] at [$X]?" (Yes/No)  
Vary price across respondents to build demand curve.

**Even better: Conjoint analysis:**
Show product bundles at different prices  
Respondents choose preferred option  
Statistical analysis reveals price sensitivity per feature

---

## Value Metrics

### What is a Value Metric?

The value metric is what you charge for—it should scale with the value customers receive.

**Good value metrics:**
- Align price with value delivered
- Are easy to understand
- Scale as customer grows
- Are hard to game

### Common Value Metrics

| Metric | Best For | Example |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per feature | Modular products | HubSpot add-ons |
| Per contact/record | CRM, email tools | Mailchimp, HubSpot |
| Per transaction | Payments, marketplaces | Stripe, Shopify |
| Flat fee | Simple products | Basecamp |
| Revenue share | High-value outcomes | Affiliate platforms |

### Choosing Your Value Metric

**Step 1: Identify how customers get value**
- What outcome do they care about?
- What do they measure success by?
- What would they pay more for?

**Step 2: Map usage to value**

| Usage Pattern | Value Delivered | Potential Metric |
|---------------|-----------------|------------------|
| More team members use it | More collaboration value | Per user |
| More data processed | More insights | Per record/event |
| More revenue generated | Direct ROI | Revenue share |
| More projects managed | More organization | Per project |

**Step 3: Test for alignment**

Ask: "As a customer uses more of [metric], do they get more value?"
- If yes → good value metric
- If no → price doesn't align with value

### Mapping Usage to Value: Framework

**1. Instrument usage data**  
Track how customers use your product:
- Feature usage frequency
- Volume metrics (users, records, API calls)
- Outcome metrics (revenue generated, time saved)

**2. Correlate with customer success**
- Which usage patterns predict retention?
- Which usage patterns predict expansion?
- Which customers pay the most, and why?

**3. Identify value thresholds**
- At what usage level do customers "get it"?
- At what usage level do they expand?
- At what usage level should price increase?

**Example Analysis:**

```
Usage-Value Correlation Analysis:
─────────────────────────────────
Segment: High-LTV customers (>$10k ARR)
Average monthly active users: 15
Average projects: 8
Average integrations: 4

Segment: Churned customers
Average monthly active users: 3
Average projects: 2
Average integrations: 0

Insight: Value correlates with team adoption (users)
        and depth of use (integrations)

Recommendation: Price per user, gate integrations to higher tiers
```

---

## Tier Structure

### How Many Tiers?

**2 tiers:** Simple, clear choice
- Works for: Clear SMB vs. Enterprise split
- Risk: May leave money on table

**3 tiers:** Industry standard
- Good tier = Entry point
- Better tier = Recommended (anchor to best)
- Best tier = High-value customers

**4+ tiers:** More granularity
- Works for: Wide range of customer sizes
- Risk: Decision paralysis, complexity

### Good-Better-Best Framework

**Good tier (Entry):**
- Purpose: Remove barriers to entry
- Includes: Core features, limited usage
- Price: Low, accessible
- Target: Small teams, try before you buy

**Better tier (Recommended):**
- Purpose: Where most customers land
- Includes: Full features, reasonable limits
- Price: Your "anchor" price
- Target: Growing teams, serious users

**Best tier (Premium):**
- Purpose: Capture high-value customers
- Includes: Everything, advanced features, higher limits
- Price: Premium (often 2-3x "Better")
- Target: Larger teams, power users, enterprises

### Tier Differentiation Strategies

**Feature gating:**
- Basic features in all tiers
- Advanced features in higher tiers
- Works when features have clear value differences

**Usage limits:**
- Same features, different limits
- More users, storage, API calls at higher tiers
- Works when value scales with usage

**Support level:**
- Email support → Priority support → Dedicated success
- Works for products with implementation complexity

**Access and customization:**
- API access, SSO, custom branding
- Works for enterprise differentiation

### Example Tier Structure

```
┌────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                │ Starter         │ Pro             │ Business        │
│                │ $29/mo          │ $79/mo          │ $199/mo         │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Users          │ Up to 5         │ Up to 20        │ Unlimited       │
│ Projects       │ 10              │ Unlimited       │ Unlimited       │
│ Storage        │ 5 GB            │ 50 GB           │ 500 GB          │
│ Integrations   │ 3               │ 10              │ Unlimited       │
│ Analytics      │ Basic           │ Advanced        │ Custom          │
│ Support        │ Email           │ Priority        │ Dedicated       │
│ API Access     │ ✗               │ ✓               │ ✓               │
│ SSO            │ ✗               │ ✗               │ ✓               │
│ Audit logs     │ ✗               │ ✗               │ ✓               │
└────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Packaging for Personas

### Identifying Pricing Personas

Different customers have different:
- Willingness to pay
- Feature needs
- Buying processes
- Value perception

**Segment by:**
- Company size (solopreneur → SMB → enterprise)
- Use case (marketing vs. sales vs. support)
- Sophistication (beginner → power user)
- Industry (different budget norms)

### Persona-Based Packaging

**Step 1: Define personas**

| Persona | Size | Needs | WTP | Example |
|---------|------|-------|-----|---------|
| Freelancer | 1 person | Basic features | Low | $19/mo |
| Small Team | 2-10 | Collaboration | Medium | $49/mo |
| Growing Co | 10-50 | Scale, integrations | Higher | $149/mo |
| Enterprise | 50+ | Security, support | High | Custom |

**Step 2: Map features to personas**

| Feature | Freelancer | Small Team | Growing | Enterprise |
|---------|------------|------------|---------|------------|
| Core features | ✓ | ✓ | ✓ | ✓ |
| Collaboration | — | ✓ | ✓ | ✓ |
| Integrations | — | Limited | Full | Full |
| API access | — | — | ✓ | ✓ |
| SSO/SAML | — | — | — | ✓ |
| Audit logs | — | — | — | ✓ |
| Custom contract | — | — | — | ✓ |

**Step 3: Price to value for each persona**
- Research willingness to pay per segment
- Set prices that capture value without blocking adoption
- Consider segment-specific landing pages

---

## Freemium vs. Free Trial

### When to Use Freemium

**Freemium works when:**
- Product has viral/network effects
- Free users provide value (content, data, referrals)
- Large market where % conversion drives volume
- Low marginal cost to serve free users
- Clear feature/usage limits for upgrade trigger

**Freemium risks:**
- Free users may never convert
- Devalues product perception
- Support costs for non-paying users
- Harder to raise prices later

**Example: Slack**
- Free tier for small teams
- Message history limit creates upgrade trigger
- Free users invite others (viral growth)
- Converts when team hits limit

### When to Use Free Trial

**Free trial works when:**
- Product needs time to demonstrate value
- Onboarding/setup investment required
- B2B with buying committees
- Higher price points
- Product is "sticky" once configured

**Trial best practices:**
- 7-14 days for simple products
- 14-30 days for complex products
- Full access (not feature-limited)
- Clear countdown and reminders
- Credit card optional vs. required trade-off

**Credit card upfront:**
- Higher trial-to-paid conversion (40-50% vs. 15-25%)
- Lower trial volume
- Better qualified leads

### Hybrid Approaches

**Freemium + Trial:**
- Free tier with limited features
- Trial of premium features
- Example: Zoom (free 40-min, trial of Pro)

**Reverse trial:**
- Start with full access
- After trial, downgrade to free tier
- Example: See premium value, live with limitations until ready

---

## When to Raise Prices

### Signs It's Time

**Market signals:**
- Competitors have raised prices
- You're significantly cheaper than alternatives
- Prospects don't flinch at price
- "It's so cheap!" feedback

**Business signals:**
- Very high conversion rates (>40%)
- Very low churn (<3% monthly)
- Customers using more than they pay for
- Unit economics are strong

**Product signals:**
- You've added significant value since last pricing
- Product is more mature/stable
- New features justify higher price

### Price Increase Strategies

**1. Grandfather existing customers**
- New price for new customers only
- Existing customers keep old price
- Pro: No churn risk
- Con: Leaves money on table, creates complexity

**2. Delayed increase for existing**
- Announce increase 3-6 months out
- Give time to lock in old price (annual)
- Pro: Fair, drives annual conversions
- Con: Some churn, requires communication

**3. Increase tied to value**
- Raise price but add features
- "New Pro tier with X