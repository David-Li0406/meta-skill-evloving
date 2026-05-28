# Pricing Strategy Framework

## Purpose

Set the right price for your product. Pricing is positioning - it signals value and attracts the right customers.

---

## Pricing Principles

### Core Truths

1. **Price for value, not cost** - What's it worth to the customer?
2. **You can always lower later** - Starting too low is hard to fix
3. **Simple beats complex** - Fewer tiers, clearer decision
4. **Free is expensive** - Free users cost time and resources
5. **Price is a filter** - Right price attracts right customers

---

## Pricing Models

### Model Comparison

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **Flat rate** | Simple products | Easy to understand | No expansion |
| **Tiered** | SaaS with features | Upgrade path | Complexity |
| **Usage-based** | Variable value | Scales with value | Unpredictable |
| **Freemium** | Viral products | Volume, converts | Support burden |
| **Free trial** | High consideration | Qualified leads | Friction |
| **Lifetime** | Cash injection | Upfront cash | No recurring |

### Model Selection

```
Is your product viral/network-effect?
├── Yes → Consider Freemium
└── No
    ├── Does value scale with usage?
    │   ├── Yes → Usage-based
    │   └── No
    │       ├── Simple product?
    │       │   ├── Yes → Flat rate
    │       │   └── No → Tiered pricing
    │       └── Need quick cash?
    │           └── Yes → Consider Lifetime deal
```

---

## Tier Structure

### The Classic SaaS Tiers

| Tier | Purpose | Typical |
|------|---------|---------|
| **Free/Starter** | Acquisition, try before buy | Limited features |
| **Pro/Growth** | Core paying customers | Full features |
| **Team/Business** | Collaboration, scale | Team features |
| **Enterprise** | Large orgs (if needed) | Custom |

### Solo Builder Recommendation

**Start with 2 tiers:**
1. **Free** - Limited but useful (if appropriate)
2. **Pro** - Full features, reasonable price

**Add Team tier only when:**
- You have actual team demand
- Team features exist
- Support capacity ready

### Tier Design Principles

| Principle | Application |
|-----------|-------------|
| Clear upgrade trigger | User hits limit, needs more |
| Value-based limits | Limit by value metric, not arbitrary |
| No punishment | Free tier should be genuinely useful |
| Simple comparison | 3-5 differences max between tiers |

---

## Price Point Selection

### Anchoring to Value

**Formula:**
```
Price = (Value delivered to customer) × (Your capture rate)

Typical capture rate: 10-20% of value
```

**Example:**
- Customer saves 10 hours/month
- Their time worth $100/hour
- Value = $1000/month
- Your price: $100-200/month (10-20%)

### Competitor Benchmarking

| Position | Price vs Market | When to Use |
|----------|-----------------|-------------|
| Premium | 2-3x average | Significantly better product |
| Market rate | ~Average | Comparable product |
| Budget | 0.5-0.75x average | Simpler/fewer features |
| Free | $0 | Freemium strategy |

### Solo Builder Price Ranges

| Product Type | Typical Range |
|--------------|---------------|
| Side project/hobby | $5-15/mo |
| Prosumer tool | $15-50/mo |
| Professional tool | $50-200/mo |
| Team tool | $10-50/user/mo |
| High-value B2B | $200-1000/mo |

---

## Pricing Psychology

### Tactics

| Tactic | How | Why |
|--------|-----|-----|
| **Charm pricing** | $49 not $50 | Feels cheaper |
| **Anchoring** | Show higher price first | Makes target feel reasonable |
| **Decoy** | Add unattractive middle tier | Pushes to desired tier |
| **Annual discount** | 2 months free | Increases commitment |
| **Round numbers** | $50 not $49 | Signals quality |

### What to Use

**For B2C/prosumer:** Charm pricing ($29, $49, $99)
**For B2B/premium:** Round numbers ($50, $100, $200)
**For all:** Annual discounts (16-20% off)

---

## Freemium Strategy

### When Freemium Works

- Product has viral/network effects
- Low marginal cost per user
- Clear upgrade triggers
- Can sustain free user support

### When Freemium Fails

- High support burden
- No clear upgrade trigger
- Generous free tier cannibalizes paid
- Wrong users attracted

### Freemium Design

| Free Tier | Paid Tier |
|-----------|-----------|
| Core functionality | Full functionality |
| Limited quantity | Unlimited |
| Personal use | Team features |
| Community support | Priority support |
| Watermark/branding | White label |

---

## Pricing Page Best Practices

### Layout

```
┌─────────────────────────────────────────────────────┐
│                   PRICING HEADER                     │
│    Clear value proposition + pricing philosophy     │
└─────────────────────────────────────────────────────┘

┌──────────┐  ┌──────────┐  ┌──────────┐
│  FREE    │  │   PRO    │  │  TEAM    │
│          │  │(Popular) │  │          │
│  $0/mo   │  │ $49/mo   │  │ $99/mo   │
│          │  │          │  │          │
│ Features │  │ Features │  │ Features │
│  - X     │  │  - All   │  │  - All   │
│  - Y     │  │  - Plus  │  │  - Plus  │
│          │  │          │  │          │
│ [Start]  │  │ [Start]  │  │ [Start]  │
└──────────┘  └──────────┘  └──────────┘

┌─────────────────────────────────────────────────────┐
│                      FAQ                             │
└─────────────────────────────────────────────────────┘
```

### Essential Elements

- [ ] Clear tier names
- [ ] Monthly/annual toggle
- [ ] Feature comparison
- [ ] Highlighted recommended tier
- [ ] Clear CTAs
- [ ] FAQ section
- [ ] Money-back guarantee

### What to Include

| Element | Why |
|---------|-----|
| Annual discount | Increase commitment |
| Feature comparison table | Easy comparison |
| "Most popular" badge | Social proof |
| Money-back guarantee | Reduce risk |
| FAQ | Handle objections |

---

## Pricing Changes

### When to Change

- Not getting enough signups (maybe too high)
- Too easy to convert (probably too low)
- Customer feedback
- Market changes
- Costs change significantly

### How to Change

**Raising prices:**
- Grandfather existing customers
- Give advance notice
- Add value to justify
- Be transparent about why

**Lowering prices:**
- Just do it
- Optional: credit existing customers

### Testing Prices

- A/B test with new visitors
- Test different copy, same price
- Ask willingness-to-pay in surveys
- Monitor conversion rates

---

## Special Pricing

### Lifetime Deals

| Aspect | Consideration |
|--------|---------------|
| Pricing | 12-24x monthly price |
| Where | AppSumo, own site |
| Risk | Losing recurring revenue |
| Benefit | Quick cash, user base |

**When to consider:**
- Need initial cash
- Product is stable
- Can handle support spike

### Discounts

| Discount | When to Use |
|----------|-------------|
| Annual | Always offer (16-20% off) |
| Launch | Limited time launch special |
| Student/nonprofit | If aligned with mission |
| Grandfathering | When raising prices |

---

## Output Format

```markdown
## Pricing Strategy

### Model
{Flat rate / Tiered / Usage-based / Freemium}

### Tiers

| Tier | Price | Target | Key Features |
|------|-------|--------|--------------|
| {name} | ${X}/mo | {who} | {features} |

### Rationale
{Why this pricing}

### Competitor Comparison
| Competitor | Price | Our Position |
|------------|-------|--------------|
| {name} | ${X} | {comparison} |

### Upgrade Triggers
{What causes users to upgrade}

### Risk Mitigation
- Money-back guarantee: {Yes/No}
- Annual discount: {X}%
- Free tier: {Yes/No}
```
