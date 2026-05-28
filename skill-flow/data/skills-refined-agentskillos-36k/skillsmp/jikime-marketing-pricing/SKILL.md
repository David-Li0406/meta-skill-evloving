---
name: jikime-marketing-pricing
description: SaaS pricing and monetization strategy specialist covering pricing research methods (Van Westendorp, MaxDiff), tier structure, value metrics, and packaging decisions.
version: 1.0.0
tags: ["marketing", "pricing", "monetization", "saas", "strategy"]
triggers:
  keywords: ["pricing", "pricing tiers", "freemium", "free trial", "packaging", "value metric", "Van Westendorp", "willingness to pay", "가격", "가격 전략", "프리미엄"]
  phases: ["plan"]
  agents: ["manager-strategy", "architect"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~7000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Pricing Strategy

## Quick Reference (30 seconds)

Pricing Strategy Specialist - Design pricing that captures value, drives growth, and aligns with customer willingness to pay.

Core Philosophy:
- **Value-Based**: Price based on value delivered, not cost to serve
- **Research-Driven**: Use data (Van Westendorp, MaxDiff) for decisions
- **Segment-Aware**: Different personas have different willingness to pay

Key Capabilities:
- Pricing research methodologies
- Tier structure design (Good-Better-Best)
- Value metric selection
- Freemium vs. Free Trial decision framework

---

## Implementation Guide (5 minutes)

### The Three Pricing Axes

Every pricing decision involves three dimensions:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRICING DECISION MATRIX                      │
├─────────────────────────────────────────────────────────────────┤
│  1. PACKAGING           2. PRICING METRIC      3. PRICE POINT   │
│  ┌─────────────┐       ┌─────────────┐        ┌─────────────┐  │
│  │ What's      │       │ What do you │        │ How much    │  │
│  │ included    │       │ charge for? │        │ do you      │  │
│  │ at each     │       │             │        │ charge?     │  │
│  │ tier?       │       │ Per user?   │        │             │  │
│  │             │       │ Per usage?  │        │ $X/month    │  │
│  │ Features    │       │ Flat fee?   │        │             │  │
│  │ Limits      │       │             │        │             │  │
│  │ Support     │       │             │        │             │  │
│  └─────────────┘       └─────────────┘        └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Value-Based Pricing Framework

```
┌─────────────────────────────────────────────────────────────────┐
│  Customer's perceived value                          $1000     │
│  ──────────────────────────────────────────────────────────    │
│                     ↑ Value captured (your opportunity)        │
│  Your price                                          $500      │
│  ──────────────────────────────────────────────────────────    │
│                     ↑ Consumer surplus (value customer keeps)  │
│  Next best alternative                               $300      │
│  ──────────────────────────────────────────────────────────    │
│                     ↑ Differentiation value                    │
│  Your cost to serve                                  $50       │
└─────────────────────────────────────────────────────────────────┘

Key insight: Price between alternative and perceived value.
             Cost is a floor, not a basis.
```

---

## Pricing Research Methods

### Van Westendorp Price Sensitivity Meter

**The Four Questions:**

| # | Question | Measures |
|---|----------|----------|
| 1 | At what price would it be SO EXPENSIVE you wouldn't buy? | Too expensive |
| 2 | At what price would it be SO CHEAP you'd question quality? | Too cheap |
| 3 | At what price is it starting to get EXPENSIVE but you'd still consider? | Expensive/high |
| 4 | At what price is it a BARGAIN—great value? | Cheap/good value |

**Analysis Output:**

```
Price Sensitivity Analysis Results:
─────────────────────────────────────
Point of Marginal Cheapness (PMC):  $29/mo  ← Floor
Optimal Price Point (OPP):          $49/mo  ← Sweet spot
Indifference Price Point (IDP):     $59/mo  ← Neutral
Point of Marginal Expensiveness:    $79/mo  ← Ceiling

Acceptable Range: $29 - $79
Optimal Zone: $49 - $59
```

**Survey Tips:**
- Need 100-300 respondents
- Segment by persona (different WTP)
- Use realistic product descriptions
- Add purchase intent questions

### MaxDiff Analysis (Feature Prioritization)

MaxDiff identifies which features customers value most for packaging decisions.

**How It Works:**
1. List 8-15 features
2. Show sets of 4-5 features
3. Ask: "Which is MOST important? LEAST important?"
4. Repeat across sets
5. Statistical analysis produces utility scores

**Using Results for Packaging:**

| Utility Score | Packaging Decision |
|---------------|-------------------|
| Top 20% | Include in all tiers (table stakes) |
| 20-50% | Use to differentiate tiers |
| 50-80% | Higher tiers only |
| Bottom 20% | Premium add-on or cut |

---

## Value Metrics

### Common Value Metrics

| Metric | Best For | Examples |
|--------|----------|----------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per contact/record | CRM, email tools | Mailchimp, HubSpot |
| Per transaction | Payments, marketplaces | Stripe, Shopify |
| Flat fee | Simple products | Basecamp |
| Revenue share | High-value outcomes | Affiliate platforms |

### Choosing Your Value Metric

**Value Metric Test:**
```
As customer uses more [metric], do they get more value?

✅ Yes → Good value metric
❌ No  → Price doesn't align with value
```

**Mapping Usage to Value:**

| Usage Pattern | Value Delivered | Metric |
|---------------|-----------------|--------|
| More team members | More collaboration | Per user |
| More data processed | More insights | Per record |
| More revenue generated | Direct ROI | Revenue share |
| More projects managed | More organization | Per project |

---

## Tier Structure

### Good-Better-Best Framework

```
┌────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                │ Good (Entry)    │ Better (Target) │ Best (Premium)  │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Purpose        │ Remove barriers │ Where most land │ Capture high    │
│                │                 │                 │ value customers │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Features       │ Core, limited   │ Full, reasonable│ Everything +    │
│                │                 │ limits          │ advanced        │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Price          │ Low, accessible │ Anchor price    │ 2-3x "Better"   │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Target         │ Small teams,    │ Growing teams,  │ Large teams,    │
│                │ try before buy  │ serious users   │ power users     │
└────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Tier Differentiation Strategies

| Strategy | How It Works | Best For |
|----------|--------------|----------|
| **Feature Gating** | Advanced features in higher tiers | Clear feature value differences |
| **Usage Limits** | Same features, different limits | Value scales with usage |
| **Support Level** | Email → Priority → Dedicated | Implementation complexity |
| **Access Controls** | API, SSO, custom branding | Enterprise differentiation |

### Example Tier Structure

```
┌────────────────┬───────────┬───────────┬───────────┐
│                │ Starter   │ Pro       │ Business  │
│                │ $29/mo    │ $79/mo    │ $199/mo   │
├────────────────┼───────────┼───────────┼───────────┤
│ Users          │ Up to 5   │ Up to 20  │ Unlimited │
│ Projects       │ 10        │ Unlimited │ Unlimited │
│ Storage        │ 5 GB      │ 50 GB     │ 500 GB    │
│ Integrations   │ 3         │ 10        │ Unlimited │
│ Analytics      │ Basic     │ Advanced  │ Custom    │
│ Support        │ Email     │ Priority  │ Dedicated │
│ API Access     │ ✗         │ ✓         │ ✓         │
│ SSO            │ ✗         │ ✗         │ ✓         │
└────────────────┴───────────┴───────────┴───────────┘
```

---

## Freemium vs. Free Trial

### Decision Framework

| Factor | Freemium | Free Trial |
|--------|----------|------------|
| Network effects | Strong | Weak |
| Time to value | Immediate | Requires setup |
| Product complexity | Simple | Complex |
| Market size | Large (volume play) | Smaller (quality) |
| Marginal cost | Low | Any |

### Freemium Works When

- Product has viral/network effects
- Free users provide value (content, data, referrals)
- Large market where % conversion drives volume
- Clear upgrade triggers

### Free Trial Works When

- Product needs time to demonstrate value
- Onboarding/setup investment required
- B2B with buying committees
- Higher price points

### Credit Card Upfront Trade-off

| Approach | Conversion Rate | Trial Volume | Lead Quality |
|----------|-----------------|--------------|--------------|
| CC Required | 40-50% trial→paid | Lower | Higher |
| No CC | 15-25% trial→paid | Higher | Lower |

---

## Pricing Psychology

### Key Principles

| Principle | Application |
|-----------|-------------|
| **Anchoring** | Show higher price first (enterprise, "was $X") |
| **Decoy Effect** | Add inferior option to make target look better |
| **Charm Pricing** | $99 feels much cheaper than $100 |
| **Round Pricing** | $100 signals premium, $99 signals value |
| **Rule of 100** | Under $100: use %, Over $100: use $ off |

### Pricing Page Best Practices

- [ ] Recommended tier highlighted visually
- [ ] Monthly/annual toggle with savings shown
- [ ] Feature comparison table
- [ ] FAQ section for objections
- [ ] Money-back guarantee visible
- [ ] "Most Popular" or "Best Value" badge
- [ ] Contact sales for enterprise

---

## When to Raise Prices

### Signs It's Time

| Signal Type | Indicators |
|-------------|------------|
| **Market** | Competitors raised prices, you're significantly cheaper |
| **Business** | High conversion (>40%), low churn (<3%) |
| **Product** | Significant new value added since last pricing |
| **Customer** | "It's so cheap!" feedback, no price flinch |

### Price Increase Strategies

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Grandfather existing | New price for new only | No churn risk | Revenue left on table |
| Delayed increase | Announce 3-6 months out | Fair, drives annual | Some churn |
| Tied to value | Add features with increase | Justified | Requires new value |
| Plan restructure | Change plans entirely | Clean slate | Disruptive |

---

## Pricing Checklist

```
Before Setting Prices:
- [ ] Defined target customer personas
- [ ] Researched competitor pricing
- [ ] Identified value metric
- [ ] Conducted WTP research (Van Westendorp/surveys)
- [ ] Mapped features to tiers

Pricing Structure:
- [ ] Chosen number of tiers (typically 3)
- [ ] Differentiated tiers clearly
- [ ] Set prices based on research
- [ ] Created annual discount (15-20%)
- [ ] Planned enterprise/custom tier

Validation:
- [ ] Tested with target customers
- [ ] Reviewed with sales team
- [ ] Validated unit economics
- [ ] Planned for future increases
```

---

## Works Well With

Skills:
- `jikime-marketing-page-cro` - For pricing page optimization
- `jikime-marketing-copywriting` - For pricing page copy
- `jikime-marketing-psychology` - For pricing psychology
- `jikime-marketing-ab-test` - For testing price changes

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
