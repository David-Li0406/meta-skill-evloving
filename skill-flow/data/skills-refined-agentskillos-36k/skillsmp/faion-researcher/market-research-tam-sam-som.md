---
id: market-research-tam-sam-som
name: "Market Research (TAM/SAM/SOM)"
domain: RES
skill: faion-researcher
category: "research"
---

# Market Research (TAM/SAM/SOM)

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #market, #tam, #sam, #som |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Entrepreneurs either overestimate markets ("It's a billion dollar opportunity!") or underestimate them ("Is this big enough?"). Common issues:
- Using top-down numbers without grounding
- Confusing TAM with realistic potential
- Not knowing how to calculate market size
- Presenting unrealistic projections

**The root cause:** No practical method to size markets for solo products.

---

## Framework

### What is TAM/SAM/SOM?

Three nested circles representing market potential:

```
    ┌─────────────────────────────────────┐
    │               TAM                    │
    │    Total Addressable Market          │
    │   "Everyone who could ever buy"      │
    │                                      │
    │    ┌─────────────────────────┐       │
    │    │          SAM            │       │
    │    │  Serviceable Available  │       │
    │    │     "Our segment"       │       │
    │    │                         │       │
    │    │    ┌─────────────┐      │       │
    │    │    │     SOM     │      │       │
    │    │    │ Serviceable │      │       │
    │    │    │ Obtainable  │      │       │
    │    │    │ "Realistic" │      │       │
    │    │    └─────────────┘      │       │
    │    └─────────────────────────┘       │
    └─────────────────────────────────────┘
```

### TAM: Total Addressable Market

**Definition:** Total revenue if you captured 100% of the market.

**Formula:**
```
TAM = Total potential customers × Average revenue per customer
```

**Example:**
- All small businesses in the world: 400M
- Average spend on software: $1,000/year
- TAM = 400M × $1,000 = $400B

**Use case:** Show the ceiling. Not realistic, but shows opportunity size.

### SAM: Serviceable Available Market

**Definition:** Portion of TAM you can actually serve given constraints.

**Constraints:**
- Geography (US only vs. global)
- Language (English speakers only)
- Industry (Only e-commerce, not all retail)
- Size (Only 1-10 person companies)
- Tech (Only cloud users)

**Formula:**
```
SAM = TAM × Segment percentage
```

**Example:**
- TAM: $400B small business software
- Segment: US-based, e-commerce, 1-50 employees
- SAM = $400B × 2% = $8B

### SOM: Serviceable Obtainable Market

**Definition:** Realistic market share you can capture in 3-5 years.

**Reality checks:**
- You're new with no brand
- Competitors exist
- Marketing budget is limited
- You can only serve X customers

**Formula:**
```
SOM = SAM × Realistic market share
```

**Realistic share guidelines:**

| Stage | Market Share | Justification |
|-------|-------------|---------------|
| Year 1 | 0.1-0.5% | Just starting |
| Year 3 | 1-3% | Established |
| Year 5 | 3-10% | Market leader position |

**Example:**
- SAM: $8B
- Year 3 target: 0.5% share
- SOM = $8B × 0.5% = $40M

### Calculation Methods

#### Method 1: Top-Down (Research-Based)

Start with industry reports, narrow down:

```
Industry Size → Segment → Geography → SOM

$400B Global SaaS
→ $50B Project Management
→ $5B Freelancer/Solopreneur segment
→ $1B English-speaking markets
→ $5M Year 3 SOM (0.5%)
```

**Pros:** Uses established data
**Cons:** Can be disconnected from reality

#### Method 2: Bottom-Up (Customer-Based)

Start with customers, multiply up:

```
Customers × Price = Revenue

1000 customers × $100/mo × 12 = $1.2M ARR
10,000 customers × $100/mo × 12 = $12M ARR
```

**Calculation:**
1. Find number of potential customers (use LinkedIn, industry data)
2. Estimate % you can reach
3. Estimate conversion rate
4. Multiply by price

**Pros:** Grounded in reality
**Cons:** May underestimate opportunity

#### Method 3: Competitor-Based

Use competitor revenues to estimate:

```
Competitor 1: $50M ARR (10% share)
Competitor 2: $30M ARR (6% share)
Competitor 3: $20M ARR (4% share)

Estimated market = $500M
Your SOM (1% in 3 years) = $5M
```

**Where to find:**
- Crunchbase funding data
- SimilarWeb traffic estimates
- LinkedIn employee count × $200K revenue per employee
- Pricing × estimated customers

### Validation Checks

| Check | How |
|-------|-----|
| Does TAM feel real? | Compare to public market data |
| Is SAM specific enough? | Can you name 100 target customers? |
| Is SOM achievable? | Can you explain how to get there? |
| Bottom-up matches top-down? | Within 2x is good |

---

## Templates

### Market Sizing Report

```markdown
## Market Sizing: [Product/Niche]

### Executive Summary
- **TAM:** $X
- **SAM:** $X
- **SOM (3-year):** $X
- **Confidence:** [High/Medium/Low]

### TAM Calculation (Top-Down)

**Industry:** [Name]
**Global market size:** $X (Source: [X])
**Growth rate:** X% CAGR

**Calculation:**
- Total potential buyers: X
- Average spend: $X/year
- TAM = X × $X = $X

### SAM Calculation

**Constraints applied:**

| Constraint | % of TAM | Value |
|------------|----------|-------|
| Geography ([X]) | X% | $X |
| Industry ([X]) | X% | $X |
| Company size ([X]) | X% | $X |
| Other ([X]) | X% | $X |

**SAM = TAM × [combined %] = $X**

### SOM Calculation (Bottom-Up)

**Target customers:**
- LinkedIn search: X results for [criteria]
- Industry databases: X companies
- Estimated reachable: X

**Conversion funnel:**
- Visitors: X/month
- Signups (5%): X
- Paid (10%): X
- Annual customers: X

**Revenue:**
- Customers: X
- Price: $X/year
- Year 3 SOM = $X

### Validation

| Method | Result | Confidence |
|--------|--------|------------|
| Top-down | $X | Medium |
| Bottom-up | $X | High |
| Competitor-based | $X | Medium |

**Variance:** X% (within acceptable range)

### Market Dynamics

**Growth drivers:**
1. [Driver 1]
2. [Driver 2]

**Risks:**
1. [Risk 1]
2. [Risk 2]

### Conclusion
[Is this market worth pursuing?]
```

### Quick Market Check (15 min)

```markdown
## Quick Market Check: [Idea]

### TAM (Rough)
Industry: [X]
Google search: "[industry] market size"
Result: $X (Source: [X])

### SAM (Segment)
My segment: [X]
Estimate: X% of TAM = $X

### SOM (Reality)
Year 1 target: X customers × $X = $X
Year 3 target: X customers × $X = $X

### Verdict
[ ] Big enough (SOM > $1M)
[ ] Too small (SOM < $500K)
[ ] Need more research
```

---

## Examples

### Example 1: Project Management SaaS for Freelancers

**TAM:**
- Global project management software: $6B
- Growth: 10% CAGR

**SAM:**
- Freelancer segment: 15% of PM market = $900M
- English-speaking: 60% = $540M
- Digital freelancers: 50% = $270M

**SOM (Bottom-up):**
- 15M freelancers in target segment
- 0.5% can reach and convert = 75,000 potential
- 1% Year 1 conversion = 750 customers
- $20/mo × 750 × 12 = $180K Year 1
- Year 3 at 5,000 customers = $1.2M

**Verdict:** Viable but competitive. Need differentiation.

### Example 2: Analytics Tool for E-commerce

**TAM:**
- E-commerce analytics: $5B

**SAM:**
- Shopify stores only: 4M stores
- Store analytics spend: $100/year avg
- SAM = 4M × $100 = $400M

**SOM (Bottom-up):**
- Reachable stores (marketing): 100,000
- Trial conversion: 5% = 5,000
- Paid conversion: 20% = 1,000
- Year 1: 1,000 × $50/mo × 12 = $600K
- Year 3 projection: $3M

**Verdict:** Strong opportunity. Clear path to $1M+ ARR.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only using TAM | Always calculate SOM for realism |
| Trusting one source | Cross-reference 3+ sources |
| No bottom-up validation | Always do customer-based math |
| Ignoring competition | Factor competitor share into SOM |
| Static market | Consider growth rates |
| Precision theater | Estimates are OK, show assumptions |

---

## Related Methodologies

- **niche-evaluation:** Niche Evaluation
- **competitor-analysis:** Competitor Analysis
- **pricing-research:** Pricing Research
- **mvp-scoping:** MVP Scoping
- **roadmap-design:** Roadmap Design

---

## Agent

**faion-market-researcher-agent** helps size markets. Invoke with:
- "Calculate TAM/SAM/SOM for [market]"
- "What's the market size for [niche]?"
- "Validate my market sizing: [assumptions]"
- "Find market data for [industry]"

---

*Methodology | Research | Version 1.0*
