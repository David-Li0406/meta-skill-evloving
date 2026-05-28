# Plausible Query Patterns

Common query patterns and combinations for typical analytics use cases.

## Basic Metrics Queries

### Single Metric

Get a single metric for a time period:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "date_range": "7d"
}
```

### Multiple Metrics

Request multiple metrics in one query:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "date_range": "30d"
}
```

**Benefits:** Single request returns all metrics, more efficient than multiple queries.

## Traffic Source Analysis

### Top Traffic Sources

Identify where visitors come from:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]],
  "limit": 10
}
```

### Social Media Traffic

Filter for social media sources:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["or", [
      ["is", "visit:source", ["Twitter"]],
      ["is", "visit:source", ["Facebook"]],
      ["is", "visit:source", ["LinkedIn"]],
      ["is", "visit:source", ["Reddit"]]
    ]]
  ]
}
```

### Search Engine Traffic

Analyze search traffic:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "visit_duration"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
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

### Country Breakdown

Visitor distribution by country:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country"],
  "date_range": "month",
  "filters": [["is_not", "visit:country", [""]]],
  "order_by": [["visitors", "desc"]]
}
```

### City-Level Analysis

Drill down to cities:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country", "visit:city"],
  "date_range": "30d",
  "filters": [
    ["is", "visit:country", ["US"]]
  ],
  "order_by": [["visitors", "desc"]],
  "limit": 20
}
```

### Regional Comparison

Compare regions or states:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:region"],
  "date_range": "month",
  "filters": [
    ["is", "visit:country", ["US"]]
  ]
}
```

## Page Performance Analysis

### Top Pages

Most visited pages:

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "visitors"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "order_by": [["pageviews", "desc"]],
  "limit": 20
}
```

### Blog Post Performance

Analyze blog section:

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "bounce_rate", "visit_duration"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["contains", "event:page", ["/blog"]]
  ],
  "order_by": [["pageviews", "desc"]]
}
```

### High Bounce Rate Pages

Identify pages with engagement issues:

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "bounce_rate"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["is_not", "event:page", ["/"]]
  ],
  "order_by": [["bounce_rate", "desc"]],
  "limit": 20
}
```

### Pathname Analysis

Group by pathname (ignoring query parameters):

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "visitors"],
  "dimensions": ["event:page.pathname"],
  "date_range": "30d",
  "order_by": [["pageviews", "desc"]]
}
```

## Device and Browser Analysis

### Device Breakdown

Compare desktop, mobile, tablet:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "dimensions": ["visit:device"],
  "date_range": "30d"
}
```

### Browser Analysis

Top browsers:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:browser"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]],
  "limit": 10
}
```

### Mobile Browser Performance

Mobile-specific browser analysis:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate", "visit_duration"],
  "dimensions": ["visit:browser"],
  "date_range": "30d",
  "filters": [
    ["is", "visit:device", ["mobile"]]
  ]
}
```

## Time-Based Analysis

### Daily Trends

Track daily visitor trends:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["time:day"],
  "date_range": "30d"
}
```

### Hourly Patterns

Understand traffic patterns throughout the day:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["time:hour"],
  "date_range": "day"
}
```

### Weekly Trends

Week-over-week analysis:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["time:week"],
  "date_range": "12mo"
}
```

### Monthly Comparison

Monthly trends:

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

Track campaign effectiveness:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews", "bounce_rate"],
  "dimensions": ["visit:utm_campaign"],
  "date_range": "30d",
  "filters": [
    ["is_not", "visit:utm_campaign", [""]]
  ]
}
```

### UTM Source Analysis

Analyze traffic sources by UTM:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "visit_duration"],
  "dimensions": ["visit:utm_source", "visit:utm_medium"],
  "date_range": "month",
  "filters": [
    ["is_not", "visit:utm_source", [""]]
  ]
}
```

### Campaign Content Performance

Compare different content variations:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate"],
  "dimensions": ["visit:utm_content"],
  "date_range": "30d",
  "filters": [
    ["is", "visit:utm_campaign", ["summer_sale"]]
  ]
}
```

## Complex Filter Combinations

### Multi-Condition Filters

Combine multiple conditions:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["and", [
      ["contains", "event:page", ["/blog"]],
      ["is", "visit:country", ["US"]],
      ["is", "visit:device", ["mobile"]]
    ]]
  ]
}
```

### Exclude Internal Traffic

Filter out internal or test traffic:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["is_not", "event:page", ["/admin", "/test", "/staging"]]
  ]
}
```

### Specific Page Sections

Analyze specific sections of the site:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "visit_duration"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["or", [
      ["contains", "event:page", ["/docs"]],
      ["contains", "event:page", ["/guides"]]
    ]]
  ]
}
```

### Regex Pattern Matching

Use regex for flexible matching:

```json
{
  "site_id": "example.com",
  "metrics": ["pageviews"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "filters": [
    ["matches", "event:page", ["^/user/\\d+/profile$"]]
  ]
}
```

## Engagement Metrics

### Average Session Duration

Track how long visitors stay:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "visit_duration"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "order_by": [["visit_duration", "desc"]]
}
```

### Pages Per Visit

Understand content consumption:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "views_per_visit"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "order_by": [["views_per_visit", "desc"]]
}
```

### Bounce Rate Analysis

Identify high bounce sources:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "bounce_rate"],
  "dimensions": ["visit:source"],
  "date_range": "30d",
  "filters": [
    ["is_not", "visit:source", ["Direct"]]
  ],
  "order_by": [["bounce_rate", "desc"]]
}
```

## Combining Dimensions

### Source and Device

Understand device preferences by source:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:source", "visit:device"],
  "date_range": "30d",
  "order_by": [["visitors", "desc"]]
}
```

### Country and City

Geographic drill-down:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country", "visit:city"],
  "date_range": "month",
  "filters": [
    ["is", "visit:country", ["US", "GB", "CA"]]
  ],
  "limit": 50
}
```

### Page and Source

See which sources drive traffic to specific pages:

```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["event:page", "visit:source"],
  "date_range": "30d",
  "filters": [
    ["contains", "event:page", ["/blog"]]
  ],
  "limit": 50
}
```

## Best Practices for Patterns

1. **Start Simple** - Begin with basic queries, add complexity incrementally
2. **Use Filters Early** - Filter data before grouping to improve performance
3. **Limit Results** - Set appropriate limits to avoid large responses
4. **Combine Related Metrics** - Request multiple metrics in one query
5. **Order Results** - Use `order_by` to get most relevant data first
6. **Time Dimensions** - Use appropriate time dimensions for analysis period
7. **Pagination** - For large result sets, use pagination instead of high limits
