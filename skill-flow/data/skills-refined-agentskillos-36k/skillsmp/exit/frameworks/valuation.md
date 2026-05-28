# Valuation Framework

## Purpose

Understand what your business is worth and how to maximize it.

---

## Valuation Methods

### 1. Revenue Multiple

**Formula:** `Valuation = ARR × Multiple`

**When to use:**
- SaaS businesses
- Growing companies
- Revenue is meaningful

**Multiples by growth:**

| Annual Growth | Typical Multiple |
|---------------|------------------|
| < 10% | 2-3x ARR |
| 10-30% | 3-5x ARR |
| 30-50% | 5-8x ARR |
| 50-100% | 8-12x ARR |
| > 100% | 12-20x ARR |

**Solo builder reality:** Most exits at solo scale are 2-5x ARR.

---

### 2. Profit Multiple (SDE/EBITDA)

**Formula:** `Valuation = Annual Profit × Multiple`

**When to use:**
- Profitable businesses
- Lifestyle businesses
- Individual buyers

**SDE (Seller's Discretionary Earnings):**
```
Net Profit
+ Owner's salary
+ Owner's benefits
+ One-time expenses
+ Non-cash expenses
= SDE
```

**Multiples:**

| SDE | Typical Multiple |
|-----|------------------|
| < $100K | 2-3x |
| $100K-500K | 3-4x |
| $500K-1M | 3.5-4.5x |
| > $1M | 4-6x |

---

### 3. User-Based Valuation

**Formula:** `Valuation = Users × Value per User`

**When to use:**
- Pre-revenue companies
- Consumer apps
- High engagement

**Rough benchmarks:**

| User Type | Value/User |
|-----------|------------|
| Registered user | $1-10 |
| Active user (MAU) | $10-50 |
| Paying user | $100-500 |
| Enterprise user | $1,000+ |

**Note:** Highly variable based on engagement, monetization potential.

---

### 4. Comparable Transactions

**Method:** Look at what similar companies sold for.

**Where to find comps:**
- TechCrunch, news coverage
- MicroAcquire sold listings
- Industry reports
- Network conversations

**How to apply:**
1. Find 3-5 similar transactions
2. Calculate multiple for each
3. Apply median to your metrics
4. Adjust for differences

---

### 5. Discounted Cash Flow (DCF)

**Formula:** Sum of future cash flows discounted to present value.

**When to use:**
- Mature, predictable businesses
- Sophisticated buyers

**Note:** Rarely used for small SaaS; too many assumptions.

---

## Valuation Factors

### Positive Factors (Increase Value)

| Factor | Impact | Why |
|--------|--------|-----|
| High growth (>50%) | +2-4x | Future potential |
| Strong retention (>90%) | +1-2x | Predictable revenue |
| Low churn (<5%) | +1-2x | Sticky customers |
| Diverse customers | +1x | Less risk |
| Recurring revenue | +1-2x | Predictability |
| Clean code/docs | +0.5-1x | Lower risk |
| Strong brand | +0.5-1x | Moat |
| Strategic fit | +1-3x | Synergies |

### Negative Factors (Decrease Value)

| Factor | Impact | Why |
|--------|--------|-----|
| Customer concentration | -1-2x | Risk if they leave |
| High churn (>10%) | -1-2x | Leaky bucket |
| Declining growth | -1-2x | Trend matters |
| Technical debt | -0.5-1x | Future cost |
| Key person dependency | -0.5-1x | Risk |
| Legal issues | -1-3x | Uncertainty |
| Competitive pressure | -0.5-1x | Margin pressure |

---

## Valuation Calculation Example

```
Base case:
- ARR: $500,000
- Growth: 40% YoY
- Churn: 4% monthly
- Base multiple: 5x (40% growth)

Adjustments:
+ Strong retention: +1x
- Key person dependency: -0.5x
+ Strategic interest: +1x

Adjusted multiple: 6.5x

Valuation range: $500K × 5x to $500K × 8x
               = $2.5M to $4M

Target: $3.25M (6.5x)
```

---

## Valuation Negotiation

### Anchor High, Justify Well

**Anchoring strategy:**
- Start negotiations high
- Have data to support
- Create room for concession
- Show comparable exits

### Value Drivers to Highlight

| Driver | How to Present |
|--------|----------------|
| Growth | "40% YoY, accelerating" |
| Retention | "90% NRR, industry-leading" |
| Customer quality | "Enterprise customers, low churn" |
| Technology | "Modern stack, well-documented" |
| Market | "Growing market, early mover" |

### Common Negotiation Points

| Buyer Says | Your Response |
|------------|---------------|
| "Too expensive" | Show comps, growth trajectory |
| "High churn" | Show cohort improvement |
| "Small market" | Show expansion opportunity |
| "Competition" | Show differentiation, moat |
| "Key person risk" | Show documentation, systems |

---

## Maximizing Valuation

### 12-Month Prep Plan

| Month | Action | Impact |
|-------|--------|--------|
| 12 | Fix churn issues | +1x |
| 10 | Document everything | +0.5x |
| 8 | Clean up tech debt | +0.5x |
| 6 | Diversify customers | +0.5x |
| 4 | Show growth trajectory | +1x |
| 2 | Build buyer interest | Competition |

### Quick Wins

| Action | Time | Impact |
|--------|------|--------|
| Calculate and show NRR | 1 day | Better multiple |
| Document revenue drivers | 1 week | Buyer confidence |
| Clean up financials | 1 week | Faster DD |
| Remove key person risk | 1 month | Higher multiple |

---

## Valuation Reality Check

### Solo Builder Context

Most solo builder exits are:
- **$50K-500K** for acqui-hires
- **$100K-2M** for small SaaS sales
- **$1M-10M** for successful SaaS

Very few solo builder exits exceed $10M.

### Set Realistic Expectations

| Your Situation | Realistic Range |
|----------------|-----------------|
| Pre-revenue, good team | $50K-200K |
| <$10K MRR, growing | $100K-500K |
| $10K-50K MRR, stable | $300K-1.5M |
| $50K-100K MRR, growing | $1M-4M |
| >$100K MRR, strong growth | $3M-10M+ |

---

## Output Format

```markdown
## Valuation Analysis

### Metrics Summary
| Metric | Value |
|--------|-------|
| ARR | ${X} |
| MRR | ${X} |
| Growth rate | {X}% |
| Net retention | {X}% |
| Churn | {X}% |

### Base Valuation
| Method | Multiple | Value |
|--------|----------|-------|
| Revenue | {X}x ARR | ${X} |
| Profit | {X}x SDE | ${X} |

### Adjustments
| Factor | Adjustment |
|--------|------------|
| {factor} | {+/-X}x |
| {factor} | {+/-X}x |

### Final Range
**Low:** ${X} ({X}x)
**Target:** ${X} ({X}x)
**High:** ${X} ({X}x)

### Value Improvement Opportunities
1. {Opportunity}: +{$X} potential
2. {Opportunity}: +{$X} potential
```
