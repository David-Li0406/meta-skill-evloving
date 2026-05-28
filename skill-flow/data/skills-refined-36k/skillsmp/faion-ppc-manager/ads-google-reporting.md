---
id: google-reporting
name: "Google Ads Reporting & Optimization"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Google Ads Reporting & Optimization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | google-reporting |
| **Name** | Google Ads Reporting & Optimization |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | google-campaign-setup, conversion-tracking, attribution-models |

---

## Problem

You're checking your Google Ads but don't know what to look for. Data is everywhere but insights are nowhere. You make changes based on gut feeling instead of data.

This methodology teaches you how to read reports, diagnose issues, and optimize systematically.

---

## Framework

Google Ads optimization follows a data-driven cycle:

```
MONITOR   -> Check key metrics regularly
ANALYZE   -> Understand what's happening
DIAGNOSE  -> Find root causes
OPTIMIZE  -> Make targeted improvements
```

### Step 1: Essential Reports

**Reports to check:**

| Report | Where to Find | What It Shows |
|--------|---------------|---------------|
| Overview | Dashboard | High-level performance |
| Campaigns | Campaigns tab | Campaign-level metrics |
| Keywords | Keywords tab | Keyword performance |
| Search Terms | Keywords → Search Terms | Actual searches |
| Ads | Ads & Assets | Ad performance |
| Auction Insights | Campaigns → Auction Insights | Competitive position |

**Custom columns to add:**
- Impressions
- Clicks
- CTR
- Avg CPC
- Cost
- Conversions
- Conv. rate
- Cost/conv
- Conv. value
- ROAS
- Quality Score
- Impression share

### Step 2: Key Metrics Deep Dive

**Understanding each metric:**

| Metric | What It Tells You | Action If Bad |
|--------|-------------------|---------------|
| Impressions | Reach potential | Increase budget, broaden targeting |
| CTR | Ad relevance | Improve ad copy, tighten targeting |
| Quality Score | Overall health | Improve ads, landing pages, CTR |
| Conv. rate | Landing page effectiveness | Optimize landing page |
| CPA | Cost efficiency | Reduce bids, improve quality |
| Impression share | Market capture | Increase budget or bids |

**Quality Score breakdown:**
- Expected CTR: Predicted click rate
- Ad relevance: Keyword to ad match
- Landing page experience: User experience

### Step 3: Segment Analysis

**Break down by segments:**

| Segment | Reveals |
|---------|---------|
| Device | Mobile vs desktop performance |
| Time | Day of week, hour patterns |
| Network | Search vs partners |
| Location | Geographic performance |
| Audience | Audience layer performance |

**How to use segments:**
1. Add segment columns
2. Identify best/worst performers
3. Adjust bids by segment
4. Exclude poor performers

### Step 4: Search Terms Analysis

**Search Terms report (critical):**

1. Go to Keywords → Search Terms
2. Sort by cost (descending)
3. Review each search term

**Actions based on findings:**

| Finding | Action |
|---------|--------|
| Relevant + converting | Add as keyword |
| Relevant + not converting | Monitor |
| Irrelevant + high cost | Add as negative |
| Irrelevant + low cost | Add as negative |

**Weekly routine:**
- Export Search Terms
- Filter by cost > $5
- Add negatives for irrelevant
- Add as keywords if valuable

### Step 5: Optimization Actions

**By metric issue:**

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Low impressions | Budget, targeting | Increase budget, broaden keywords |
| Low CTR | Poor ads | Improve headlines, test new ads |
| Low Quality Score | Relevance issues | Tighter ad groups, better landing pages |
| Low conv rate | Landing page | Optimize page, check offer |
| High CPA | Multiple factors | Reduce bids, add negatives, improve quality |
| Low impression share | Budget or bid | Increase budget or bids |

**Bid adjustments:**
- Increase bids for high-performing segments
- Decrease or exclude poor performers
- Consider automated bidding after data collection

### Step 6: Reporting Schedule

**Daily (5 min):**
- Check spend pacing
- Look for anomalies
- Ensure no disapprovals

**Weekly (30 min):**
- Full performance review
- Search Terms analysis
- Add negatives
- Bid adjustments
- Quality Score review

**Monthly (1 hour):**
- Trend analysis
- Budget reallocation
- Strategy assessment
- Test new features

---

## Templates

### Weekly Optimization Checklist

```markdown
## Week of [Date]

### Performance Review
- Total spend: $[X] (budget: $[X])
- Conversions: [X]
- CPA: $[X] (target: $[X])
- ROAS: [X]:1

### Campaigns
| Campaign | Spend | Conv | CPA | Action |
|----------|-------|------|-----|--------|
| [Name]   | $X    | X    | $X  | [action] |

### Search Terms Actions
- [ ] Added negatives: [list]
- [ ] Added keywords: [list]

### Optimization Actions
- [ ] [Action 1]
- [ ] [Action 2]

### Next Week Focus
- [Priority 1]
- [Priority 2]
```

### Performance Report

```markdown
## Google Ads Report: [Date Range]

### Summary
| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Spend  | $X          | $X          | +X%    |
| Clicks | X           | X           | +X%    |
| Conv   | X           | X           | +X%    |
| CPA    | $X          | $X          | -X%    |

### Campaign Performance
| Campaign | Spend | CTR | Conv | CPA | Status |
|----------|-------|-----|------|-----|--------|
| [Name]   | $X    | X%  | X    | $X  | [status] |

### Top Keywords
| Keyword | Clicks | Conv | CPA | QS |
|---------|--------|------|-----|-----|
| [word]  | X      | X    | $X  | X   |

### Issues Identified
1. [Issue + action taken]
2. [Issue + action taken]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Examples

### Diagnosis Example

**Situation:** CPA increased 40% month over month

**Analysis steps:**
1. Check overall metrics: CTR stable, conv rate down
2. Check Search Terms: Many irrelevant searches
3. Check Quality Score: Dropped for main keywords
4. Check landing page: No changes

**Diagnosis:**
- Match types too broad
- Irrelevant clicks consuming budget
- Quality Score declining due to low CTR on irrelevant searches

**Actions:**
1. Add 50 negative keywords
2. Move to phrase/exact match
3. Tighten ad groups
4. Improve landing page relevance

### Budget Reallocation Example

**Current:**
```
Campaign A: $100/day, CPA $20 (target $25) - 80% imp share
Campaign B: $100/day, CPA $45 (target $25) - 60% imp share
Campaign C: $50/day, CPA $15 (target $25) - 40% imp share
```

**Decision:**
```
Campaign A: Keep at $100/day (performing well)
Campaign B: Reduce to $50/day, optimize (over target)
Campaign C: Increase to $100/day (best CPA, low share)
```

---

## Implementation Checklist

### Setup
- [ ] Create custom column set
- [ ] Set up automated reports
- [ ] Define KPI targets
- [ ] Create conversion tracking

### Weekly Routine
- [ ] Review all campaigns
- [ ] Check Search Terms
- [ ] Add negatives
- [ ] Review Quality Scores
- [ ] Make bid adjustments

### Monthly Routine
- [ ] Full trend analysis
- [ ] Competitive review (Auction Insights)
- [ ] Budget reallocation
- [ ] Strategy assessment

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Looking at wrong metrics | Focus on CPA/ROAS, not clicks | Define success metrics |
| Ignoring Search Terms | Wasted spend | Review weekly |
| Over-optimizing | Resets learning | Major changes monthly |
| No segments | Missing insights | Break down by device, time |
| Vanity metrics | Clicks don't matter | Focus on conversions |

---

## Optimization Priority Matrix

| Impact | Effort | Examples |
|--------|--------|----------|
| High / Low | Do first | Add negatives, pause bad keywords |
| High / High | Plan for | Landing page optimization |
| Low / Low | Quick wins | Bid adjustments |
| Low / High | Skip | Major restructure for marginal gains |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Reporting | Google Ads, Looker Studio |
| Bulk edits | Google Ads Editor |
| Automation | Scripts, Rules |
| Competitive | Auction Insights |
| Attribution | GA4 |

---

## Related Methodologies

- **google-campaign-setup:** Google Campaign Setup
- **google-keywords:** Google Keywords
- **conversion-tracking:** Conversion Tracking
- **ab-testing-ads:** A/B Testing Ads

---

*Methodology: google-reporting | Ads API | faion-ads-agent*
