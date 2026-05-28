---
id: meta-reporting
name: "Meta Ads Reporting & Analysis"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Meta Ads Reporting & Analysis

## Metadata

| Field | Value |
|-------|-------|
| **ID** | meta-reporting |
| **Name** | Meta Ads Reporting & Analysis |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | meta-campaign-setup, conversion-tracking, attribution-models |

---

## Problem

You're spending money but don't know what's working. The default Meta reports are overwhelming. You make decisions based on the wrong metrics and waste budget on underperforming ads.

This methodology teaches you what to measure, how to analyze it, and what actions to take based on data.

---

## Framework

Reporting follows the analyze-decide-act cycle:

```
MEASURE   -> Track the right metrics
ANALYZE   -> Understand what's happening
DIAGNOSE  -> Identify problems and opportunities
ACT       -> Make data-driven decisions
```

### Step 1: Set Up Custom Columns

**Essential columns to add:**

| Column | Why |
|--------|-----|
| Amount spent | Total investment |
| Impressions | Reach |
| Reach | Unique people |
| Frequency | Avg times seen |
| Link clicks | Interest |
| CTR (link clicks) | Click efficiency |
| Cost per click | Click cost |
| Conversions | Results |
| Cost per conversion | Efficiency |
| Conversion rate | Landing page effectiveness |
| ROAS | Return on ad spend |

**Create column presets:**
- Overview (high-level metrics)
- Prospecting (focus on CTR, CPA)
- Retargeting (focus on ROAS)
- Creative testing (focus on CTR, engagement)

### Step 2: Understand Key Metrics

**Metric hierarchy:**

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| **CPM** | (Spend / Impressions) x 1000 | Audience competitiveness |
| **CTR** | (Clicks / Impressions) x 100 | Creative + audience fit |
| **CPC** | Spend / Clicks | Cost of interest |
| **CVR** | (Conversions / Clicks) x 100 | Landing page effectiveness |
| **CPA** | Spend / Conversions | Acquisition efficiency |
| **ROAS** | Revenue / Spend | Overall return |

**What good looks like:**

| Metric | Below Average | Average | Good |
|--------|---------------|---------|------|
| CTR | <0.5% | 0.8-1.2% | >1.5% |
| CVR | <1% | 2-3% | >5% |
| Frequency | >3 | 1.5-2.5 | <1.5 |
| ROAS | <2 | 2-3 | >4 |

### Step 3: Breakdown Analysis

**Use breakdowns to understand:**

| Breakdown | Reveals |
|-----------|---------|
| Age | Best performing demographics |
| Gender | Targeting efficiency |
| Placement | Where ads work best |
| Platform | Facebook vs Instagram |
| Device | Mobile vs desktop |
| Time | Day/hour performance |
| Region | Geographic winners |

**How to analyze breakdowns:**
1. Export data with breakdown
2. Identify segments with best CPA
3. Create dedicated campaigns for winners
4. Exclude poor performers

### Step 4: Diagnose Common Issues

**Diagnosis framework:**

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| High CPM, low CTR | Poor creative/audience fit | New creative, tighter targeting |
| Good CTR, low CVR | Landing page issue | Optimize landing page |
| Rising CPA | Audience fatigue or creative fatigue | Refresh creative, expand audience |
| High frequency | Audience too small | Expand or refresh |
| Inconsistent results | Learning phase or low budget | Increase budget, consolidate |

**The metrics diagnostic flow:**
```
High CPA?
├── Is CTR low? → Creative issue
├── Is CVR low? → Landing page issue
├── Is CPM high? → Audience issue
└── Is frequency high? → Fatigue issue
```

### Step 5: Reporting Cadence

**Daily checks:**
- Spend pacing
- Any errors or issues
- Major metric changes

**Weekly analysis:**
- Full performance review
- Breakdowns analysis
- Optimization decisions
- Creative refresh planning

**Monthly review:**
- Overall ROAS/CPA trends
- Audience performance comparison
- Budget reallocation
- Strategy adjustments

### Step 6: Custom Reports

**Build reports in Ads Manager:**

1. Go to Ads Reporting
2. Choose metrics (columns)
3. Add filters (campaigns, dates)
4. Save as template
5. Schedule email delivery

**Report types:**

| Report | Frequency | Focus |
|--------|-----------|-------|
| Executive summary | Weekly | Spend, ROAS, key wins |
| Campaign performance | Weekly | All campaigns, CPA trends |
| Creative analysis | Weekly | Ad-level CTR, spend |
| Audience insights | Monthly | Breakdown by segment |

---

## Templates

### Weekly Performance Report

```markdown
## Meta Ads Weekly Report: [Date Range]

### Summary
- **Total Spend:** $X
- **Conversions:** X
- **CPA:** $X (target: $X)
- **ROAS:** X:1

### Campaign Performance
| Campaign | Spend | Conv | CPA | ROAS | Status |
|----------|-------|------|-----|------|--------|
| [Name]   | $X    | X    | $X  | X:1  | Scale/Hold/Pause |

### Top Performing Ads
| Ad | CTR | Conv | CPA |
|----|-----|------|-----|
| [Name] | X% | X | $X |

### Insights
- **What worked:** [Details]
- **What didn't:** [Details]
- **Learnings:** [Details]

### Actions for Next Week
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]
```

### Creative Performance Analysis

```markdown
## Creative Analysis: [Date Range]

### By Format
| Format | Spend | CTR | CPA | Winner? |
|--------|-------|-----|-----|---------|
| Image  | $X    | X%  | $X  | Yes/No  |
| Video  | $X    | X%  | $X  | Yes/No  |
| Carousel | $X  | X%  | $X  | Yes/No  |

### Top 5 Creatives
| Creative | Hook | Spend | CTR | CVR | CPA |
|----------|------|-------|-----|-----|-----|
| [Name]   | [Type] | $X | X% | X% | $X |

### Fatigue Signals
- [ ] Any creative with CTR decline >20%?
- [ ] Any creative with frequency >3?

### Recommendations
- [New creative ideas based on winners]
- [What to kill]
- [What to iterate on]
```

---

## Examples

### Diagnosis Example

**Situation:** CPA increased from $10 to $18 over 2 weeks

**Analysis:**
- CTR: Stable at 1.2%
- CVR: Dropped from 4% to 2.5%
- CPM: Stable
- Frequency: Increased from 1.8 to 3.2

**Diagnosis:**
- Landing page conversion issue (CVR drop)
- Audience fatigue (frequency increase)

**Actions:**
1. A/B test landing page
2. Expand audience or add new lookalike
3. Refresh creative
4. Exclude recent converters

### Budget Reallocation Example

**Current state:**
```
Campaign A: $50/day, CPA $12 (target $15)
Campaign B: $50/day, CPA $22 (target $15)
Campaign C: $50/day, CPA $8 (target $15)
```

**Decision:**
```
Campaign A: Keep at $50
Campaign B: Reduce to $25, test new creative
Campaign C: Increase to $100
```

---

## Implementation Checklist

### Setup
- [ ] Create custom column presets
- [ ] Set up automated reports
- [ ] Define success metrics
- [ ] Create reporting schedule

### Daily
- [ ] Check spend pacing
- [ ] Monitor for errors
- [ ] Flag major changes

### Weekly
- [ ] Run full analysis
- [ ] Check breakdowns
- [ ] Make optimization decisions
- [ ] Plan creative updates

### Monthly
- [ ] Review trends
- [ ] Reallocate budget
- [ ] Update strategy
- [ ] Report to stakeholders

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Wrong metrics | Vanity metrics don't matter | Focus on CPA, ROAS |
| Too frequent checking | Noise, not signal | Daily check, weekly analysis |
| No breakdowns | Missing insights | Use age, placement, device |
| Ignoring trends | Slow decline missed | Track week-over-week |
| No action from data | Reports without decisions | Every report = actions |
| Comparing unequal periods | Misleading conclusions | Same days, same conditions |

---

## Metrics Reference

| Metric | Definition | Calculation |
|--------|------------|-------------|
| Impressions | Times ad shown | Counted by Meta |
| Reach | Unique people | Counted by Meta |
| Frequency | Avg impressions/person | Impressions / Reach |
| CTR | Click-through rate | Clicks / Impressions |
| CPC | Cost per click | Spend / Clicks |
| CPM | Cost per 1000 impressions | (Spend / Impressions) x 1000 |
| CVR | Conversion rate | Conversions / Clicks |
| CPA | Cost per acquisition | Spend / Conversions |
| ROAS | Return on ad spend | Revenue / Spend |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Reporting | Meta Ads Manager, Ads Reporting |
| Visualization | Google Sheets, Looker Studio |
| Attribution | Meta Attribution, Triple Whale |
| Export | Supermetrics, Funnel.io |

---

## Related Methodologies

- **meta-campaign-setup:** Meta Campaign Setup
- **conversion-tracking:** Conversion Tracking
- **attribution-models:** Attribution Models
- **ab-testing-ads:** A/B Testing Ads

---

*Methodology: meta-reporting | Ads API | faion-ads-agent*
