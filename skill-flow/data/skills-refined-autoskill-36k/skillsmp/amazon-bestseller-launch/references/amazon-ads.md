# Amazon Ads Playbook for Authors

## Campaign Structure Overview

```
Account
├── Sponsored Products (80% of budget)
│   ├── Exact Match Campaign
│   ├── Phrase Match Campaign
│   ├── Broad Match Campaign
│   ├── Product Targeting Campaign
│   └── Auto Campaign (research)
└── Sponsored Brands (20% of budget) [if 3+ books]
    └── Video Ads
```

## Phase 1: Launch Week Campaigns

### Auto Campaign (Research)

**Purpose:** Discover converting keywords

```
Campaign Name: [BOOK] - Auto - Research
Daily Budget: $10
Bid: $0.50
Targeting: Automatic
Duration: Run for 14 days
```

**After 14 days:** Export search term report, move winners to manual campaigns.

### Exact Match Campaign

**Purpose:** High-intent, proven converters

```
Campaign Name: [BOOK] - Exact - Core
Daily Budget: $15
Default Bid: $0.75
Keywords: 20-30 high-intent terms
```

**Keyword Sources:**
- Book title variations
- Author name
- Core topic keywords
- Competitor book titles

### Product Targeting Campaign

**Purpose:** Appear on competitor book pages

```
Campaign Name: [BOOK] - Product - Competitors
Daily Budget: $10
Bid: $0.60
Targets: 30-50 competitor ASINs
```

**Target Selection Criteria:**
- Same category
- Similar topic
- 100+ reviews (proven audience)
- Published within 2 years

## Keyword Research Process

### Step 1: Seed Keywords

Start with 10 core terms:
```
[main topic]
[main topic] book
[main topic] guide
how to [main topic]
[main topic] for beginners
[author name]
[book title]
books about [topic]
[problem] solution
[audience] [topic]
```

### Step 2: Expand with Tools

**Free Methods:**
- Amazon search autocomplete
- "Customers also bought" ASINs
- Competitor book keywords

**Paid Tools:**
- Publisher Rocket ($97)
- Helium 10 ($97/mo)
- Keyword Tool ($89/mo)

### Step 3: Organize by Intent

| Intent Level | Example | Bid Modifier |
|-------------|---------|--------------|
| High (buying) | "best [topic] book" | 1.5x |
| Medium (researching) | "how to [topic]" | 1.0x |
| Low (browsing) | "[topic]" alone | 0.5x |

## Bid Optimization Strategy

### Initial Bids by Match Type

| Match Type | Starting Bid | Adjustment After 7 Days |
|-----------|--------------|------------------------|
| Exact | $0.75 | Based on ACoS |
| Phrase | $0.60 | -15% from Exact |
| Broad | $0.45 | -25% from Exact |
| Auto | $0.50 | Pause losers, keep winners |

### Bid Adjustment Rules

```
If ACoS < 30%: Increase bid 20%
If ACoS 30-50%: Maintain bid
If ACoS 50-70%: Decrease bid 15%
If ACoS > 70%: Pause keyword (7+ days)
If 0 sales after $10 spend: Pause
```

### Target ACoS by Phase

| Phase | Target ACoS | Rationale |
|-------|-------------|-----------|
| Launch (Week 1-2) | 100%+ OK | Visibility trumps profit |
| Growth (Week 3-8) | 50-70% | Balance ranking + profit |
| Maintenance (Month 3+) | 30-50% | Sustainable profitability |

## Budget Allocation

### Launch Week ($50/day)

```
Auto Campaign: $10 (20%)
Exact Match: $20 (40%)
Phrase Match: $10 (20%)
Product Targeting: $10 (20%)
```

### Post-Launch ($30/day)

```
Exact Match: $15 (50%)
Phrase Match: $8 (27%)
Product Targeting: $7 (23%)
Auto: Pause or $0
```

## Negative Keywords

### Immediate Negatives (Add Day 1)

```
free
pdf
download
used
library
summary
audiobook (unless selling audiobook)
kindle unlimited (unless in KU)
```

### Weekly Negative Review

Export search term report, add negatives for:
- Keywords with $5+ spend, 0 sales
- Keywords with ACoS >150% after 14 days
- Irrelevant search terms

## Campaign Optimization Schedule

| Day | Action |
|-----|--------|
| Daily | Check spend, pause runaway keywords |
| Day 3 | Add negative keywords from auto |
| Day 7 | First bid adjustments |
| Day 14 | Pause underperformers, boost winners |
| Day 30 | Full restructure based on data |

## Advanced: Dayparting Strategy

Best performing hours for book sales (adjust bids +20%):
- 7-9 AM EST (morning commute)
- 12-1 PM EST (lunch break)
- 8-11 PM EST (evening reading)

Lower bids -20% during:
- 2-5 AM EST (low traffic)
- 3-5 PM EST (work hours)

## Reporting Metrics

### Key Metrics to Track Weekly

| Metric | Formula | Target |
|--------|---------|--------|
| ACoS | Ad Spend / Sales | <50% |
| CTR | Clicks / Impressions | >0.3% |
| CVR | Orders / Clicks | >10% |
| CPC | Spend / Clicks | <$0.60 |

### Dashboard Template

```
Week of: [DATE]
Total Spend: $[X]
Total Sales: $[X]
Orders: [X]
ACoS: [X]%
Top 3 Keywords: [LIST]
Worst 3 Keywords: [LIST]
Action Items: [LIST]
```
