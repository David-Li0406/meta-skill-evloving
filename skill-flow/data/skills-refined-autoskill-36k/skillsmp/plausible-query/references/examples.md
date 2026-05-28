# Plausible Query Examples

Real-world examples with explanations for common analytics queries.

## Basic Analytics Queries

### Get Total Visitors for Last Week

**Use Case:** Quick check of recent traffic

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "date_range": "7d"
}
```

**Response:** Single result with total visitor count for the last 7 days.

### Compare Multiple Metrics

**Use Case:** Dashboard overview with key metrics

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"],
  "date_range": "30d"
}
```

**Response:** Aggregated metrics for the entire 30-day period.

## Content Analysis

### Most Popular Blog Posts

**Use Case:** Identify top-performing content

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "visitors", "bounce_rate"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["contains", "event:page", ["/blog"]]
  ],
  "order_by": [["pageviews", "desc"]],
  "limit": 10
}
```

**Explanation:** Filters for blog pages, orders by pageviews descending, returns top 10.

### Pages with High Engagement

**Use Case:** Find content that keeps visitors engaged

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "visit_duration", "views_per_visit"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["is_not", "event:page", ["/"]]
  ],
  "order_by": [["visit_duration", "desc"]],
  "limit": 20
}
```

**Explanation:** Excludes homepage, orders by visit duration to find engaging content.

### Documentation Page Performance

**Use Case:** Analyze help/documentation usage

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "dimensions": ["event:page.pathname"],
  "date_range": "month",
  "filters": [
    ["contains", "event:page.pathname", ["/docs"]]
  ],
  "order_by": [["pageviews", "desc"]]
}
```

**Explanation:** Uses pathname to ignore query parameters, focuses on docs section.

## Traffic Source Analysis

### Top Referrers

**Use Case:** Understand where traffic originates

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]],
  "limit": 15
}
```

**Response:** List of traffic sources sorted by visitor count.

### Social Media Campaign Performance

**Use Case:** Measure social media marketing effectiveness

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate", "visit_duration"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["or", [
      ["is", "visit:source", ["Twitter"]],
      ["is", "visit:source", ["Facebook"]],
      ["is", "visit:source", ["LinkedIn"]],
      ["is", "visit:source", ["Reddit"]]
    ]]
  ],
  "order_by": [["visitors", "desc"]]
}
```

**Explanation:** Filters for social platforms, shows engagement metrics.

### Search Engine Comparison

**Use Case:** Compare performance across search engines

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "dimensions": ["visit:source"],
  "date_range": "month",
  "filters": [
    ["or", [
      ["is", "visit:source", ["Google"]],
      ["is", "visit:source", ["Bing"]],
      ["is", "visit:source", ["DuckDuckGo"]]
    ]]
  ]
}
```

## Geographic Analysis

### International Visitor Distribution

**Use Case:** Understand global reach

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country"],
  "date_range": "month",
  "filters": [
    ["is_not", "visit:country", [""]]
  ],
  "order_by": [["visitors", "desc"]],
  "limit": 20
}
```

**Explanation:** Filters out empty country values, shows top 20 countries.

### US City Analysis

**Use Case:** Regional marketing insights

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:city"],
  "date_range": "30d",
  "filters": [
    ["is", "visit:country", ["US"]]
  ],
  "order_by": [["visitors", "desc"]],
  "limit": 25
}
```

### European Traffic

**Use Case:** Regional performance analysis

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country"],
  "date_range": "month",
  "filters": [
    ["is", "visit:country", ["GB", "DE", "FR", "ES", "IT", "NL", "BE"]]
  ],
  "order_by": [["visitors", "desc"]]
}
```

## Device and Browser Analysis

### Mobile vs Desktop Performance

**Use Case:** Understand device preferences and behavior

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"],
  "dimensions": ["visit:device"],
  "date_range": "30d"
}
```

**Response:** Comparison of desktop, mobile, and tablet metrics.

### Browser Compatibility Check

**Use Case:** Ensure site works across browsers

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate"],
  "dimensions": ["visit:browser"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]],
  "limit": 10
}
```

### Mobile Browser Analysis

**Use Case:** Optimize for mobile experience

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "visit_duration", "bounce_rate"],
  "dimensions": ["visit:browser"],
  "date_range": "30d",
  "filters": [
    ["is", "visit:device", ["mobile"]]
  ],
  "order_by": [["visitors", "desc"]]
}
```

## Time-Based Analysis

### Daily Traffic Trends

**Use Case:** Identify traffic patterns and anomalies

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["time:day"],
  "date_range": "30d"
}
```

**Response:** Day-by-day breakdown for trend analysis.

### Hourly Traffic Patterns

**Use Case:** Understand peak usage times

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["time:hour"],
  "date_range": "day"
}
```

**Note:** Requires "day" date_range for hour dimension.

### Weekly Growth Trends

**Use Case:** Track week-over-week growth

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["time:week"],
  "date_range": "12mo"
}
```

### Monthly Comparison

**Use Case:** Long-term trend analysis

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["time:month"],
  "date_range": "12mo"
}
```

## Marketing Campaign Analysis

### UTM Campaign Performance

**Use Case:** Measure campaign effectiveness

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"],
  "dimensions": ["visit:utm_campaign"],
  "date_range": "30d",
  "filters": [
    ["is_not", "visit:utm_campaign", [""]]
  ],
  "order_by": [["visitors", "desc"]]
}
```

**Explanation:** Filters out visits without UTM campaigns, shows campaign performance.

### Email Campaign Analysis

**Use Case:** Track email marketing results

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "dimensions": ["visit:utm_source"],
  "date_range": "30d",
  "filters": [
    ["and", [
      ["is", "visit:utm_medium", ["email"]],
      ["is_not", "visit:utm_source", [""]]
    ]]
  ]
}
```

### Paid Search Performance

**Use Case:** Analyze paid advertising ROI

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"],
  "dimensions": ["visit:utm_source", "visit:utm_campaign"],
  "date_range": "month",
  "filters": [
    ["and", [
      ["is", "visit:utm_medium", ["cpc"]],
      ["is_not", "visit:utm_campaign", [""]]
    ]]
  ]
}
```

## Complex Filter Examples

### Mobile Users from US on Blog Pages

**Use Case:** Highly specific audience analysis

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "visit_duration"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["and", [
      ["contains", "event:page", ["/blog"]],
      ["is", "visit:country", ["US"]],
      ["is", "visit:device", ["mobile"]]
    ]]
  ],
  "order_by": [["pageviews", "desc"]]
}
```

### Exclude Internal Traffic

**Use Case:** Get accurate external visitor metrics

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["and", [
      ["is_not", "event:page", ["/admin", "/test", "/staging"]],
      ["is_not", "visit:source", ["localhost", "127.0.0.1"]]
    ]]
  ]
}
```

### Specific User Paths

**Use Case:** Track user journeys through specific sections

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["or", [
      ["matches", "event:page", ["^/docs/.*"]],
      ["matches", "event:page", ["^/guides/.*"]]
    ]]
  ],
  "order_by": [["pageviews", "desc"]]
}
```

## Engagement Analysis

### High Engagement Sources

**Use Case:** Identify sources that drive engaged visitors

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "visit_duration", "views_per_visit"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["is_not", "visit:source", ["Direct"]]
  ],
  "order_by": [["visit_duration", "desc"]],
  "limit": 15
}
```

### Low Bounce Rate Pages

**Use Case:** Find pages that keep visitors engaged

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "bounce_rate"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["is_not", "event:page", ["/"]]
  ],
  "order_by": [["bounce_rate", "asc"]],
  "limit": 20
}
```

**Explanation:** Orders by bounce rate ascending to find pages with low bounce rates (high engagement).

## Multi-Dimension Analysis

### Source and Device Combination

**Use Case:** Understand device preferences by traffic source

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:source", "visit:device"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]],
  "limit": 30
}
```

### Geographic and Source Analysis

**Use Case:** Understand traffic sources by geography

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country", "visit:source"],
  "date_range": "month",
  "filters": [
    ["is", "visit:country", ["US", "GB", "CA"]]
  ],
  "limit": 50
}
```

## Tips for Using Examples

1. **Replace site_id** - Use your actual domain
2. **Adjust date ranges** - Modify based on your analysis needs
3. **Modify filters** - Customize filters for your specific use case
4. **Combine patterns** - Mix and match patterns from different examples
5. **Test incrementally** - Start with simple queries, add complexity
6. **Use pagination** - For large result sets, add page parameter
7. **Check rate limits** - Be mindful of 600 requests/hour limit
