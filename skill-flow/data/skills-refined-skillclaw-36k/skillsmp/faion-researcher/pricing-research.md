---
id: pricing-research
name: "Pricing Research"
domain: RES
skill: faion-researcher
category: "research"
---

# Pricing Research

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #pricing, #monetization |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-pricing-researcher-agent |

---

## Problem

Pricing is often guesswork or copied from competitors without understanding. Issues:
- Underpricing (leaving money on table)
- Overpricing (losing potential customers)
- Wrong model (subscription when one-time fits better)
- No validation (gut feeling pricing)

**The root cause:** Pricing set without systematic research on willingness to pay.

---

## Framework

### What is Pricing Research?

Pricing research determines what customers will pay, what model works best, and how to structure tiers. It answers: "What's the optimal price that maximizes revenue without losing customers?"

### The Pricing Research Process

#### Step 1: Understand Value Delivered

**Value metrics:**

| Metric Type | Examples |
|-------------|----------|
| Time saved | Hours/week freed up |
| Money saved | Reduced costs |
| Money earned | New revenue enabled |
| Risk reduced | Problems prevented |
| Quality improved | Better outcomes |

**Formula:**
```
Max Price = (Value Delivered × Capture Rate) - Switching Cost

Typical capture rate: 10-20% of value delivered
```

**Example:**
- Tool saves 5 hours/week
- User's time worth $50/hour
- Value = 5 × $50 × 4 weeks = $1,000/month
- Capture 10% = $100/month max price

#### Step 2: Research Competitor Pricing

**Build a pricing matrix:**

| Competitor | Free | Entry | Pro | Enterprise |
|------------|------|-------|-----|------------|
| Comp A | Yes | $29/mo | $99/mo | Custom |
| Comp B | No | $19/mo | $49/mo | $199/mo |
| Comp C | Yes | $0 | $79/mo | Custom |

**Analyze:**
- What's included at each tier?
- What's the most common price point?
- Where are gaps?
- Monthly vs annual discounts?

#### Step 3: Test Willingness to Pay

**Van Westendorp Price Sensitivity:**

Ask these 4 questions:

1. "At what price would this be too expensive to consider?" (Too Expensive)
2. "At what price would this be expensive but worth considering?" (Expensive)
3. "At what price would this be a good deal?" (Cheap)
4. "At what price would this be too cheap to trust?" (Too Cheap)

**Interpretation:**
- Optimal price = intersection of "Too Cheap" and "Too Expensive"
- Acceptable range = between "Cheap" and "Expensive"

**Simplified approach:**

Ask in interviews:
- "What would you expect to pay for this?"
- "Would you pay $X?" (test specific price)
- "What would make $X feel like a bargain?"

#### Step 4: Choose Pricing Model

**Model options:**

| Model | Best For | Examples |
|-------|----------|----------|
| Subscription | Ongoing value, sticky | SaaS tools |
| One-time | Discrete value, courses | Templates, guides |
| Usage-based | Variable consumption | API calls, storage |
| Freemium | Growth priority | PLG products |
| Tiered | Different customer sizes | Most B2B |
| Hybrid | Complex needs | Sub + usage |

**Decision factors:**

| Factor | Suggests |
|--------|----------|
| Ongoing usage | Subscription |
| One-time use | One-time purchase |
| Variable usage | Usage-based |
| Network effects | Freemium |
| Different needs | Tiered |

#### Step 5: Design Tier Structure

**Classic 3-tier approach:**

| Tier | Purpose | Pricing Psychology |
|------|---------|-------------------|
| Starter | Get foot in door | Low friction |
| Pro | Main revenue | Most value/price |
| Enterprise | Big customers | Anchor high |

**Tier design rules:**
- Clear differentiation between tiers
- 2-3x price jump between tiers
- Each tier has "one more thing" that's compelling
- Don't give everything in mid-tier

**Feature distribution:**

| Feature | Free | Starter | Pro | Enterprise |
|---------|------|---------|-----|------------|
| Core feature | Yes | Yes | Yes | Yes |
| Key differentiator | Limited | Yes | Yes | Yes |
| Advanced | No | No | Yes | Yes |
| Support | Community | Email | Priority | Dedicated |
| Limits | Low | Medium | High | Unlimited |

#### Step 6: Validate with Real Sales

**Methods:**

| Method | How |
|--------|-----|
| Pre-launch pricing page | See clicks/signups by tier |
| A/B test prices | Different cohorts, measure conversion |
| Launch at higher price | Easier to discount than raise |
| Grandfather pricing | Keep early adopters happy |

---

## Templates

### Pricing Research Report

```markdown
## Pricing Research: [Product]

### Value Analysis

**Core value delivered:**
- [Value 1]: [Quantified impact]
- [Value 2]: [Quantified impact]

**Value calculation:**
- Time saved: [X] hours × $[rate] = $[X]/month
- Money saved/earned: $[X]/month
- Total value: $[X]/month
- Target capture (15%): $[X]/month

### Competitor Analysis

| Competitor | Entry | Mid | Pro | Notes |
|------------|-------|-----|-----|-------|
| [Name] | $X | $X | $X | [Model notes] |

**Market positioning:**
- Low end: $[X]/month
- Mid market: $[X]/month
- Premium: $[X]/month

### Customer Research

**Van Westendorp results (N=[X]):**
- Too expensive: $[X]
- Expensive but worth it: $[X]
- Good deal: $[X]
- Too cheap: $[X]
- **Optimal price point:** $[X]

**Interview insights:**
1. "[Quote about pricing]"
2. "[Quote about value]"

### Recommended Pricing

**Model:** [Subscription/One-time/Usage]

**Tier structure:**

| Tier | Price | Target | Key Features |
|------|-------|--------|--------------|
| Starter | $[X]/mo | [Who] | [Features] |
| Pro | $[X]/mo | [Who] | [Features] |
| Enterprise | Custom | [Who] | [Features] |

**Annual discount:** [X]% (equals [X] months free)

### Validation Plan
- [ ] A/B test pricing page
- [ ] Track conversion by tier
- [ ] Interview churned customers

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Priced too low | Start high, discount available |
| Priced too high | 14-day trial, money-back guarantee |
| Wrong model | Monitor usage patterns, adjust |
```

### Quick Pricing Check

```markdown
## Pricing Quick Check: [Product]

### Competitor benchmark
Average: $[X]/mo
Range: $[X] - $[X]

### Value-based estimate
Value delivered: ~$[X]/mo
10% capture: $[X]/mo

### Customer feedback
"Would pay": $[X] average (N=[X])

### Recommended price
$[X]/mo

### Confidence: [Low/Medium/High]
```

---

## Examples

### Example 1: Email Marketing Tool Pricing

**Value analysis:**
- Saves 3 hours/week on email management
- User time: $50/hour
- Value: $600/month
- Capture 15%: $90/month

**Competitor pricing:**
- Mailchimp: Free to $350+
- ConvertKit: $9 to $300+
- Buttondown: $9 to $29

**Research findings:**
- Solopreneurs expect $10-30/month
- Price sensitivity around $50
- Annual discount important

**Recommendation:**
- Starter: $15/month (up to 1,000 subscribers)
- Pro: $39/month (up to 10,000 subscribers)
- Annual: 2 months free

### Example 2: Online Course Pricing

**Value analysis:**
- Teaches skill worth $5,000+ salary increase
- Course completion enables freelance work: $1,000+/project
- Value: $5,000+
- Capture 5%: $250

**Competitor pricing:**
- Udemy courses: $10-50 (discounted)
- Premium courses: $200-500
- Bootcamps: $2,000+

**Research findings:**
- Perceived value higher for live/cohort
- Completion rates matter
- Payment plans requested

**Recommendation:**
- Self-paced: $199 one-time
- Cohort-based: $499 one-time
- Payment plan: 3 × $179 = $537

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Copying competitor exactly | Adjust for your positioning |
| Pricing too low | Start higher, discount if needed |
| Only one tier | Offer 2-3 options |
| Free tier too generous | Limit to create upgrade pressure |
| No annual option | Annual = retention + cash flow |
| Never raising prices | Review and adjust quarterly |
| Ignoring willingness to pay | Always validate with customers |

---

## Related Methodologies

- **competitor-analysis:** Competitor Analysis
- **mvp-scoping:** MVP Scoping
- **gtm-strategy:** GTM Strategy
- **revenue-model-design:** Revenue Model Design
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

## Agent

**faion-pricing-researcher-agent** helps determine pricing. Invoke with:
- "Research pricing for [product type]"
- "Analyze competitor pricing in [market]"
- "What should I charge for [product]?"
- "Design pricing tiers for [product]"

---

*Methodology | Research | Version 1.0*
