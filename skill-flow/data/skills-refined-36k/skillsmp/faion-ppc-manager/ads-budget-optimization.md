---
id: budget-optimization
name: "Budget Optimization"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Budget Optimization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | budget-optimization |
| **Name** | Budget Optimization |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | attribution-models, paid-acquisition, meta-reporting |

---

## Problem

You have a fixed budget but don't know how to allocate it. You're spreading money evenly across campaigns when some deserve more. Without optimization, you're leaving conversions on the table.

Budget optimization means putting money where it works hardest.

---

## Framework

Budget optimization follows the data-driven approach:

```
MEASURE   -> Know your numbers (CPA, ROAS)
COMPARE   -> Rank campaigns/channels by efficiency
ALLOCATE  -> Move budget to winners
MONITOR   -> Watch for diminishing returns
```

### Step 1: Know Your Constraints

**Before optimizing:**

| Metric | How to Calculate | Target |
|--------|------------------|--------|
| **Target CPA** | LTV / 3 or CLV / payback period | $[X] |
| **Target ROAS** | 1 / (Margin x acceptable CAC ratio) | [X]:1 |
| **Total budget** | What you can spend | $[X]/month |
| **Minimum per channel** | Enough to learn | $500-1000/channel |

**Example CPA calculation:**
```
Average customer value: $500
Target LTV:CAC ratio: 3:1
Target CPA = $500 / 3 = $167
```

### Step 2: Audit Current Performance

**Performance by campaign:**

| Campaign | Spend | Conv | CPA | vs Target | Status |
|----------|-------|------|-----|-----------|--------|
| A | $1,000 | 50 | $20 | -60% | Scale |
| B | $1,000 | 20 | $50 | 0% | Hold |
| C | $1,000 | 10 | $100 | +100% | Cut |

**Calculate efficiency ratio:**
```
Efficiency = Target CPA / Actual CPA

> 1 = Beating target (scale)
= 1 = At target (hold)
< 1 = Missing target (optimize or cut)
```

### Step 3: Reallocation Framework

**The 70-20-10 rule:**

| Category | % of Budget | Purpose |
|----------|-------------|---------|
| **Proven** | 70% | Scale what works |
| **Promising** | 20% | Optimize potential winners |
| **Testing** | 10% | Try new things |

**Reallocation decision matrix:**

| Current Performance | Action |
|---------------------|--------|
| CPA < 0.7x target | Increase budget 30-50% |
| CPA 0.7-1x target | Increase budget 10-20% |
| CPA 1-1.3x target | Hold, optimize creative |
| CPA 1.3-2x target | Decrease budget 50% |
| CPA > 2x target | Pause, rethink |

### Step 4: Account for Diminishing Returns

**Scaling effects:**

```
Budget  → CPA change (typical)
+20%    → +5-10% CPA
+50%    → +10-20% CPA
+100%   → +20-40% CPA
```

**Why diminishing returns happen:**
- Best audiences reached first
- Frequency increases
- Competition for ad space
- Audience fatigue

**How to scale sustainably:**
- Increase budget 20-30% at a time
- Wait 3-5 days between increases
- Watch efficiency metrics closely
- Expand audiences when scaling

### Step 5: Cross-Channel Optimization

**Compare across channels:**

| Channel | Spend | Conv | CPA | ROAS | Share |
|---------|-------|------|-----|------|-------|
| Meta | $5K | 100 | $50 | 4:1 | 50% |
| Google | $3K | 50 | $60 | 3:1 | 30% |
| LinkedIn | $2K | 20 | $100 | 1.5:1 | 20% |

**Reallocation decision:**
- Meta: Best CPA, increase share
- Google: Good, maintain
- LinkedIn: Below target, reduce or optimize

**Consider:**
- Different intent (LinkedIn may be higher quality)
- Different funnel stages
- Different audiences
- Incrementality (does cutting hurt others?)

### Step 6: Budget Pacing

**Pacing strategies:**

| Strategy | When to Use |
|----------|-------------|
| Standard | Even daily spend |
| Accelerated | Time-sensitive campaigns |
| Front-loaded | Launch periods |
| Back-loaded | End of month/quarter |

**Monitor pacing:**
```
Expected spend (day X): Budget * (Day / Days in month)
Actual spend: Check dashboard
Variance: Actual / Expected

> 105%: Spending too fast
95-105%: On track
< 95%: Underspending
```

---

## Templates

### Monthly Budget Allocation

```markdown
## Budget Allocation: [Month]

### Total Budget: $[X]

### By Channel
| Channel | Allocation | % | Last Month | Change |
|---------|------------|---|------------|--------|
| Meta    | $X         | X% | $X         | +X%    |
| Google  | $X         | X% | $X         | -X%    |
| LinkedIn| $X         | X% | $X         | 0%     |
| Testing | $X         | X% | $X         | +X%    |

### By Campaign Type
| Type | Allocation | % |
|------|------------|---|
| Prospecting | $X | X% |
| Retargeting | $X | X% |
| Brand | $X | X% |

### Rationale
- Increasing Meta because [reason]
- Decreasing Google because [reason]

### Goals
- Target CPA: $X
- Expected conversions: X
```

### Weekly Reallocation Review

```markdown
## Weekly Budget Review: [Date]

### Performance Summary
| Campaign | Spend | Conv | CPA | Target | Action |
|----------|-------|------|-----|--------|--------|
| [Name]   | $X    | X    | $X  | $X     | Scale/Hold/Cut |

### Changes Made
- Campaign A: $X → $X (+X%)
- Campaign B: $X → $X (-X%)

### Testing Updates
- New test launched: [Description]
- Test concluded: [Result]

### Next Week Focus
1. [Priority 1]
2. [Priority 2]
```

---

## Examples

### Example: Monthly Reallocation

**Current state (end of month):**
```
Total budget: $10,000
Meta: $5,000, 100 conv, $50 CPA
Google: $3,000, 40 conv, $75 CPA
LinkedIn: $2,000, 15 conv, $133 CPA
Target CPA: $60
```

**Analysis:**
- Meta: 20% under target - scale
- Google: 25% over target - optimize
- LinkedIn: 122% over target - cut

**New allocation:**
```
Meta: $6,000 (+$1,000)
Google: $2,500 (-$500)
LinkedIn: $1,000 (-$1,000)
Testing: $500 (new)
```

**Expected improvement:**
- More budget to best performer
- Still testing LinkedIn with reduced risk
- Room for new experiments

### Example: Diminishing Returns

**Situation:** Meta at $100/day, $40 CPA

**Scaling test:**
```
Week 1: $100/day → $40 CPA (baseline)
Week 2: $150/day → $45 CPA (+12%)
Week 3: $200/day → $52 CPA (+30%)
Week 4: $250/day → $65 CPA (+63%)
```

**Decision:**
$200/day seems optimal. Beyond that, efficiency drops too much. Better to add new campaigns than scale this one further.

---

## Implementation Checklist

### Setup
- [ ] Define target CPA/ROAS
- [ ] Audit current performance
- [ ] Create tracking spreadsheet
- [ ] Set review schedule

### Weekly Actions
- [ ] Review all campaign performance
- [ ] Identify winners and losers
- [ ] Make budget adjustments
- [ ] Document changes and reasoning

### Monthly Actions
- [ ] Full reallocation review
- [ ] Cross-channel comparison
- [ ] Update targets if needed
- [ ] Plan next month's tests

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Equal budgets | Ignores performance | Allocate by efficiency |
| Scaling too fast | Crashes performance | 20-30% increases |
| No testing budget | No innovation | Keep 10% for tests |
| Cutting too quickly | Doesn't learn | Give time to optimize |
| Ignoring quality | Cheap leads may not convert | Track to revenue |

---

## Budget Rules of Thumb

| Situation | Guideline |
|-----------|-----------|
| Starting out | $1K-2K/channel minimum |
| Testing new channel | 2-4 weeks at min budget |
| Scaling winner | Max 30% increase per week |
| Cutting loser | 50% cut, then reassess |
| Testing budget | 10-15% of total |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Tracking | Spreadsheet, Looker Studio |
| Automation | Platform budget rules |
| Analysis | GA4, platform analytics |
| Forecasting | Historical data extrapolation |

---

## Related Methodologies

- **attribution-models:** Attribution Models (understanding credit)
- **paid-acquisition:** Paid Acquisition Overview
- **meta-reporting:** Meta Reporting
- **google-reporting:** Google Reporting

---

*Methodology: budget-optimization | Ads API | faion-ads-agent*
