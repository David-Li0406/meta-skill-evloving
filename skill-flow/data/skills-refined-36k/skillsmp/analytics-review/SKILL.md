---
name: analytics-review
description: |
  Website analytics with Pirsch. Use this skill when:
  - Reviewing website traffic and engagement
  - Analyzing visitor trends and patterns
  - Checking top pages and referrers
  - Comparing performance across time periods
  - Understanding UTM campaign effectiveness
allowed-tools:
  - mcp__pirsch__pirsch_list_domains
  - mcp__pirsch__pirsch_overview
  - mcp__pirsch__pirsch_total
  - mcp__pirsch__pirsch_visitors
  - mcp__pirsch__pirsch_pages
  - mcp__pirsch__pirsch_referrers
  - mcp__pirsch__pirsch_utm
  - mcp__pirsch__pirsch_growth
  - mcp__pirsch__pirsch_active
  - mcp__pirsch__pirsch_compare
---

# Analytics Review Skill

Analyze website performance with Pirsch using the **Overview-Drill Down-Insights** pattern.

## Phase 1: OVERVIEW (High-Level Metrics)

### List Available Domains

```javascript
mcp__pirsch__pirsch_list_domains({})
```

### Get Cached Overview

Quick snapshot of key metrics:

```javascript
mcp__pirsch__pirsch_overview({
  domainId: "<domain-id>"
})
```

### Get Detailed Totals

```javascript
mcp__pirsch__pirsch_total({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31"
})
```

Returns:

- Visitors
- Views
- Sessions
- Bounces
- Bounce rate
- Conversion rate

### Get Growth Metrics

```javascript
mcp__pirsch__pirsch_growth({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31"
})
```

### Check Real-Time Activity

```javascript
mcp__pirsch__pirsch_active({
  domainId: "<domain-id>",
  seconds: 600  // Last 10 minutes
})
```

## Phase 2: DRILL DOWN (Detailed Analysis)

### Visitor Time Series

```javascript
mcp__pirsch__pirsch_visitors({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31",
  scale: "day"  // day, week, month
})
```

### Top Pages

```javascript
mcp__pirsch__pirsch_pages({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31",
  limit: 20,
  includeAvgTimeOnPage: true
})
```

### Traffic Sources (Referrers)

```javascript
mcp__pirsch__pirsch_referrers({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31",
  limit: 20
})
```

### UTM Campaign Analysis

```javascript
// By source
mcp__pirsch__pirsch_utm({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31",
  dimension: "source"
})

// By medium
mcp__pirsch__pirsch_utm({
  domainId: "<domain-id>",
  dimension: "medium"
})

// By campaign
mcp__pirsch__pirsch_utm({
  domainId: "<domain-id>",
  dimension: "campaign"
})
```

## Phase 3: INSIGHTS (Comparative Analysis)

### Period Comparison

Compare two time periods:

```javascript
mcp__pirsch__pirsch_compare({
  domainId: "<domain-id>",
  from: "2025-01-01",
  to: "2025-01-31",
  compareFrom: "2024-12-01",
  compareTo: "2024-12-31",
  scale: "day"
})
```

Returns:

- Visitor trends for both periods
- Delta values (absolute change)
- Growth percentages

## Report Formatting

### Dashboard Summary

```text
## Website Analytics Dashboard
verygoodplugins.com | January 2025

### Key Metrics
| Metric | Value | vs Last Month |
|--------|-------|---------------|
| Visitors | 12,450 | +21.7% |
| Pageviews | 45,230 | +17.6% |
| Bounce Rate | 42.3% | -2.8pp |
| Avg Duration | 2m 34s | +16.7% |

### Top Pages
1. /pricing - 4,230 views
2. /features - 3,890 views
3. /blog/getting-started - 2,450 views
4. /docs/api - 1,890 views
5. /about - 1,230 views

### Top Referrers
1. google.com - 5,230 visitors
2. twitter.com - 1,890 visitors
3. github.com - 1,450 visitors
4. reddit.com - 890 visitors

### UTM Sources
1. newsletter - 2,340 visitors
2. twitter-organic - 1,230 visitors
3. google-ads - 890 visitors
```

### Trend Analysis

```text
## Weekly Trend Analysis

Week 1: 2,890 visitors
Week 2: 3,120 visitors (+8%)
Week 3: 3,450 visitors (+11%)
Week 4: 3,780 visitors (+10%)

Overall trend: Steady growth, averaging +9.7% week-over-week
```

## Common Analysis Scenarios

### Traffic Spike Investigation

1. Get daily visitors to identify the spike date
2. Check referrers for that date range
3. Check UTM sources for campaign attribution
4. Review top pages to see what content drove traffic

### Campaign Performance

1. Filter by UTM campaign name
2. Compare visitors, bounce rate, and time on site
3. Check which pages campaign traffic landed on
4. Compare to organic traffic for baseline

### Content Performance

1. Get top pages by views
2. Check average time on page
3. Identify high-bounce pages for optimization
4. Find underperforming content

## Best Practices

### Do

- Start with overview before drilling down
- Use appropriate date ranges for context
- Compare periods of equal length
- Look at trends, not just absolute numbers
- Consider seasonality in comparisons

### Don't

- Draw conclusions from single data points
- Ignore context (holidays, launches, etc.)
- Compare weekends to weekdays
- Forget to check mobile vs desktop
- Overlook bounce rate on landing pages
