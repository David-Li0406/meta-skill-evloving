---
id: attribution-models
name: "Attribution Models"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Attribution Models

## Metadata

| Field | Value |
|-------|-------|
| **ID** | attribution-models |
| **Name** | Attribution Models |
| **Category** | Ads API |
| **Difficulty** | Advanced |
| **Agent** | faion-ads-agent |
| **Related** | conversion-tracking, analytics-setup, paid-acquisition |

---

## Problem

Every ad platform claims credit for your conversions. Facebook says 100 conversions. Google says 80. But you only had 120 total sales. Someone's counting wrong.

Attribution models determine how credit is assigned across touchpoints. Understanding them is crucial for accurate budget allocation.

---

## Framework

Attribution answers one question:

```
Which marketing touchpoints deserve credit for a conversion?
```

### Step 1: Understand the Attribution Problem

**The customer journey:**
```
Day 1: Sees Facebook ad (impression)
Day 3: Clicks Facebook ad (click)
Day 5: Searches Google, clicks ad (click)
Day 7: Direct visit, purchases (conversion)
```

**Who gets credit?**
- Facebook: "We showed them first and drove the click"
- Google: "They searched for us and clicked"
- Reality: Both contributed

**Why it matters:**
- Over-attribution = overspending on a channel
- Under-attribution = underspending on a channel
- Wrong decisions = wasted budget

### Step 2: Attribution Models Explained

**Common models:**

| Model | How It Works | Best For |
|-------|--------------|----------|
| **Last-click** | 100% to final click | Simple, conservative |
| **First-click** | 100% to first touch | Awareness campaigns |
| **Linear** | Equal credit to all | Understanding full journey |
| **Time decay** | More credit to recent | Longer sales cycles |
| **Position-based** | 40% first, 40% last, 20% middle | Balanced view |
| **Data-driven** | ML-based credit | Large data sets |

**Visual comparison:**
```
Journey: FB click → Google click → Email click → Purchase

Last-click:     FB: 0%   | Google: 0%   | Email: 100%
First-click:    FB: 100% | Google: 0%   | Email: 0%
Linear:         FB: 33%  | Google: 33%  | Email: 33%
Position-based: FB: 40%  | Google: 20%  | Email: 40%
Time-decay:     FB: 10%  | Google: 30%  | Email: 60%
```

### Step 3: Platform Default Attribution

**What each platform uses:**

| Platform | Default Model | Window |
|----------|---------------|--------|
| Meta | 7-day click, 1-day view | View-through counted |
| Google Ads | Last Google click | 30 days |
| Google Analytics 4 | Data-driven | 90 days |
| LinkedIn | 30-day click, 7-day view | View-through counted |

**The overlap problem:**
- Each platform claims its own conversions
- User clicks FB, then Google = both claim
- Total platform conversions > actual conversions

### Step 4: Choose Your Approach

**Strategy options:**

| Approach | How It Works | Pros | Cons |
|----------|--------------|------|------|
| **Trust GA4** | Single source of truth | Unified view | Misses view-through |
| **Platform data** | Trust each platform | Detailed | Over-counts |
| **Deduplication** | Custom attribution | Accurate | Complex |
| **Incrementality** | Test-based measurement | True lift | Requires tests |

**Practical approach for most:**
1. Use GA4 for unified view
2. Use platform data for optimization within platform
3. Recognize totals won't match
4. Focus on trends, not absolute numbers

### Step 5: Configure Attribution Settings

**GA4 attribution settings:**
1. Admin → Attribution settings
2. Reporting attribution model: Data-driven
3. Lookback window: 30-90 days
4. Acquisition conversion events: Configure

**Meta attribution:**
1. Events Manager → Attribution settings
2. Attribution window: 7-day click, 1-day view
3. Consider shortening for faster cycles

**Google Ads:**
1. Tools → Measurement → Conversions
2. Each conversion → Attribution model
3. Consider position-based or data-driven

### Step 6: Incrementality Testing

**The gold standard:**

Incrementality tests measure true impact by:
1. Holding out a geographic region
2. Measuring conversion lift vs. holdout
3. Calculating true incremental ROAS

**Types of incrementality tests:**

| Test Type | How It Works |
|-----------|--------------|
| Geo holdout | No ads in test regions |
| Conversion lift | Platform measures lift |
| Ghost ads | Control sees no ads |

**When to run:**
- Spending $10K+/month
- Need to validate channel investment
- Making major budget decisions

---

## Templates

### Attribution Analysis Template

```markdown
## Attribution Analysis: [Date Range]

### Conversion Summary
| Source | Platform Data | GA4 Data | Variance |
|--------|---------------|----------|----------|
| Meta   | X             | X        | X%       |
| Google | X             | X        | X%       |
| Total  | X             | X        | X%       |

Actual sales: X
Total claimed: X
Overlap: X%

### Model Comparison (GA4)
| Channel | Last-click | Data-driven | Difference |
|---------|------------|-------------|------------|
| Meta    | X          | X           | +X%        |
| Google  | X          | X           | -X%        |
| Email   | X          | X           | +X%        |

### Insights
- [Channel] gets more credit under [model] because [reason]
- Consider increasing/decreasing spend on [channel]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

### Budget Allocation Template

```markdown
## Budget Allocation Based on Attribution

### Current Spend
| Channel | Spend | Conv (platform) | CPA (platform) |
|---------|-------|-----------------|----------------|
| Meta    | $X    | X               | $X             |
| Google  | $X    | X               | $X             |
| Total   | $X    | X               | $X             |

### Adjusted View (GA4 data-driven)
| Channel | Conv (GA4) | Adj. CPA | vs. Platform |
|---------|------------|----------|--------------|
| Meta    | X          | $X       | +X%          |
| Google  | X          | $X       | -X%          |

### Recommendation
Based on adjusted attribution:
- Reallocate $X from [channel] to [channel]
- Expected impact: [estimate]
```

---

## Examples

### Example: Multi-Channel Analysis

**Situation:**
- Meta reports 100 conversions, $5K spend ($50 CPA)
- Google reports 80 conversions, $4K spend ($50 CPA)
- GA4 shows 150 total conversions

**Analysis:**
- Platform total: 180 conversions
- Actual: 150 conversions
- Overlap: 30 (20%)

**GA4 data-driven attribution:**
- Meta: 70 conversions ($71 CPA)
- Google: 60 conversions ($67 CPA)
- Direct/organic: 20 conversions

**Insight:**
Both channels are slightly less efficient than platform data suggests, but still profitable. Google shows slightly better efficiency in unified view.

---

## Implementation Checklist

### Setup
- [ ] Configure GA4 attribution model
- [ ] Understand each platform's defaults
- [ ] Document your attribution approach
- [ ] Set up reporting template

### Analysis
- [ ] Weekly: Platform vs GA4 comparison
- [ ] Monthly: Attribution model comparison
- [ ] Quarterly: Budget reallocation review

### Testing
- [ ] Plan incrementality test
- [ ] Run for 4+ weeks
- [ ] Analyze true lift
- [ ] Apply learnings

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Trusting platform totals | Over-counting | Use GA4 unified view |
| Last-click only | Ignores journey | Use data-driven |
| Ignoring view-through | Undervalues awareness | Consider all touchpoints |
| No source of truth | Conflicting data | Pick one (usually GA4) |
| No incrementality tests | Unknown true impact | Test periodically |

---

## Attribution Window Guidelines

| Sales Cycle | Recommended Window |
|-------------|-------------------|
| Impulse (<1 day) | 1-day click |
| Short (1-7 days) | 7-day click |
| Medium (1-4 weeks) | 30-day click |
| Long (1-3 months) | 90-day click |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Unified attribution | GA4, Segment |
| Multi-touch attribution | Rockerbox, Triple Whale |
| Incrementality | Meta Lift, GeoLift |
| Analysis | Looker Studio |

---

## Related Methodologies

- **conversion-tracking:** Conversion Tracking (data foundation)
- **analytics-setup:** Analytics Setup (analytics foundation)
- **budget-optimization:** Budget Optimization (using attribution)
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: attribution-models | Ads API | faion-ads-agent*
