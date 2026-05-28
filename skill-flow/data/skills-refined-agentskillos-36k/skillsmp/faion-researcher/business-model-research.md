---
id: business-model-research
name: "Business Model Research"
domain: RES
skill: faion-researcher
category: "research"
---

# Business Model Research

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #business-model, #monetization |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Entrepreneurs build products without viable business models. Common issues:
- "We'll figure out monetization later"
- Wrong revenue model for the product type
- Unsustainable unit economics
- Misaligned with customer expectations

**The root cause:** No systematic analysis of how value translates to revenue.

---

## Framework

### What is Business Model Research?

Business model research is analyzing how a business will create, deliver, and capture value. It answers: "How will this make money sustainably?"

### The Business Model Canvas

Nine building blocks:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Key Partners │ Key Activities │ Value        │ Customer    │ Customer │
│              │                │ Proposition  │ Relationships│ Segments │
│              │ Key Resources  │              │              │          │
│              │                │              │ Channels     │          │
├──────────────┴────────────────┴──────────────┴──────────────┴──────────┤
│     Cost Structure                    │    Revenue Streams            │
└───────────────────────────────────────┴───────────────────────────────┘
```

### Revenue Model Options

#### 1. Subscription/SaaS

**How it works:** Recurring payment for ongoing access

| Variant | Description | Example |
|---------|-------------|---------|
| Flat rate | Same price for all | Basecamp |
| Tiered | Different feature levels | Slack |
| Per-seat | Per user pricing | Salesforce |
| Usage-based | Pay for consumption | AWS |
| Freemium | Free + paid tiers | Spotify |

**Best for:** Ongoing value delivery, sticky products

**Key metrics:** MRR, churn, LTV, CAC

#### 2. One-Time Purchase

**How it works:** Single payment for perpetual access

| Variant | Description | Example |
|---------|-------------|---------|
| Digital product | Courses, templates | Gumroad products |
| Software license | Perpetual license | Sketch |
| Physical product | Goods | E-commerce |

**Best for:** Discrete value, impulse buys

**Key metrics:** Units sold, revenue per product, repeat purchase

#### 3. Transaction-Based

**How it works:** Fee per transaction

| Variant | Description | Example |
|---------|-------------|---------|
| Percentage | % of transaction | Stripe 2.9% |
| Flat fee | Fixed per transaction | PayPal |
| Hybrid | Base + percentage | Shopify |

**Best for:** Marketplaces, payments, brokerage

**Key metrics:** GMV, take rate, transaction volume

#### 4. Advertising

**How it works:** Revenue from advertisers, free to users

| Variant | Description | Example |
|---------|-------------|---------|
| Display | Banner ads | News sites |
| Sponsored | Native content | Instagram |
| Affiliate | Commission on sales | Blogs |

**Best for:** High traffic, content platforms

**Key metrics:** DAU, CPM, CTR, ad inventory

#### 5. Marketplace/Commission

**How it works:** Connect buyers and sellers, take cut

| Variant | Description | Example |
|---------|-------------|---------|
| Service marketplace | Service providers | Upwork |
| Product marketplace | Product sellers | Etsy |
| Lead generation | Qualified leads | Thumbtack |

**Best for:** Matching problems, network effects

**Key metrics:** GMV, take rate, liquidity

### Business Model Analysis Process

#### Step 1: Map Value Chain

```
[Suppliers] → [Your Product] → [Customers]
      ↑                              ↓
   [Partners]                   [End Users]
```

**Questions:**
- Where is value created?
- Who captures the value?
- What's your role in the chain?

#### Step 2: Identify Revenue Opportunities

For each value point:
- Who benefits?
- What would they pay?
- How would they pay?
- How often?

#### Step 3: Analyze Comparable Models

Research similar products:
- What models do they use?
- What's their pricing?
- What's working/not working?
- What's their churn/growth?

#### Step 4: Calculate Unit Economics

**Key calculations:**

```
Customer Acquisition Cost (CAC):
= Total marketing & sales spend / New customers acquired

Lifetime Value (LTV):
= ARPU × Gross margin × (1 / Churn rate)

LTV:CAC Ratio:
= LTV / CAC (target: 3:1 or higher)

Payback Period:
= CAC / (ARPU × Gross margin) (target: <12 months)
```

#### Step 5: Stress Test

| Test | Question |
|------|----------|
| Scale | Does this work at 10x, 100x? |
| Competition | What if prices drop 50%? |
| Churn | What if churn doubles? |
| CAC | What if acquisition costs rise? |
| Time | How long until profitable? |

---

## Templates

### Business Model Canvas

```markdown
## Business Model Canvas: [Product]

### Customer Segments
- **Primary:** [Segment 1]
- **Secondary:** [Segment 2]

### Value Propositions
For [segment 1]: [Value delivered]
For [segment 2]: [Value delivered]

### Channels
- **Awareness:** [How they find us]
- **Evaluation:** [How they evaluate]
- **Purchase:** [How they buy]
- **Delivery:** [How they receive value]
- **After sales:** [How we support]

### Customer Relationships
- [Type: Self-serve / Assisted / Automated]
- [Retention mechanisms]

### Revenue Streams
| Stream | Model | Price | % Revenue |
|--------|-------|-------|-----------|
| [Stream 1] | [Model] | $X | X% |
| [Stream 2] | [Model] | $X | X% |

### Key Resources
- **Physical:** [Assets]
- **Intellectual:** [IP, data]
- **Human:** [Key roles]
- **Financial:** [Capital needed]

### Key Activities
1. [Critical activity 1]
2. [Critical activity 2]
3. [Critical activity 3]

### Key Partners
| Partner | What They Provide | What They Get |
|---------|-------------------|---------------|
| [Partner 1] | [Value] | [Value] |

### Cost Structure
| Cost | Type | Amount |
|------|------|--------|
| [Cost 1] | Fixed | $X/mo |
| [Cost 2] | Variable | $X/unit |

**Cost structure type:** [ ] Cost-driven [ ] Value-driven
```

### Unit Economics Calculator

```markdown
## Unit Economics: [Product]

### Revenue Metrics
- **ARPU (Monthly):** $[X]
- **ARPU (Annual):** $[X]
- **Gross margin:** [X]%

### Acquisition Metrics
- **Marketing spend:** $[X]/month
- **Sales spend:** $[X]/month
- **New customers:** [X]/month
- **CAC:** $[X]

### Retention Metrics
- **Monthly churn:** [X]%
- **Average lifetime:** [X] months

### Calculations

**LTV:**
= $[ARPU] × [Gross margin] × (1 / [Churn rate])
= $[X]

**LTV:CAC Ratio:**
= $[LTV] / $[CAC]
= [X]:1 ([Good/Bad] - target 3:1+)

**Payback Period:**
= $[CAC] / ($[ARPU] × [Gross margin])
= [X] months ([Good/Bad] - target <12)

### Break-even Analysis
- Fixed costs: $[X]/month
- Contribution margin: $[X]/customer
- Break-even point: [X] customers

### Verdict
[ ] Unit economics work
[ ] Need to improve [metric]
[ ] Model not viable
```

---

## Examples

### Example 1: SaaS Project Management

**Canvas highlights:**
- Segments: Freelancers, small agencies
- Value prop: Simple project tracking with client visibility
- Channels: Content marketing, Product Hunt
- Revenue: Subscription $15-49/month

**Unit economics:**
- ARPU: $29/month
- CAC: $50 (content-driven)
- Churn: 3%/month
- LTV: $29 × 0.80 × (1/0.03) = $773
- LTV:CAC: 15:1 (excellent)

**Verdict:** Viable model, focus on reducing churn.

### Example 2: Online Course Platform

**Canvas highlights:**
- Segments: Working professionals, career changers
- Value prop: Career skills in 4 weeks
- Channels: LinkedIn, YouTube
- Revenue: One-time $299 + upsell $49/month community

**Unit economics:**
- Average revenue per customer: $350 (first year)
- CAC: $80 (ads + content)
- LTV:CAC: 4.4:1 (good)

**Verdict:** Viable, community upsell critical for sustainability.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "We'll monetize later" | Design revenue model day one |
| Copying competitor pricing | Understand YOUR unit economics |
| Ignoring CAC | Account for acquisition costs |
| Underestimating churn | Use realistic churn assumptions |
| Single revenue stream | Diversify where possible |
| Not stress testing | Run scenarios before committing |

---

## Related Methodologies

- **market-research-tam-sam-som:** Market Research (TAM/SAM/SOM)
- **pricing-research:** Pricing Research
- **mvp-scoping:** MVP Scoping
- **gtm-strategy:** GTM Strategy
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

## Agent

**faion-market-researcher-agent** helps with business models. Invoke with:
- "Analyze business model for [product]"
- "What revenue model fits [idea]?"
- "Calculate unit economics for [numbers]"
- "Compare these business models: [list]"

---

*Methodology | Research | Version 1.0*
