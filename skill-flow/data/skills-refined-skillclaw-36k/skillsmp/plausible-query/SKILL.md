---
name: plausible-query
description: This skill should be used when the user asks to "query Plausible", "get Plausible analytics", "fetch Plausible stats", "query Plausible API", "get analytics data from Plausible", "plausible metrics", "plausible dimensions", or needs guidance on constructing Plausible Analytics API queries, understanding metrics, dimensions, filters, or time ranges.
---

# Plausible Analytics Query Guide

Guide for querying Plausible Analytics API v2 to retrieve website analytics data. Use when constructing API queries, understanding available metrics and dimensions, applying filters, or formatting time ranges.

## Overview

Plausible Analytics provides a single `/api/v2/query` endpoint for retrieving analytics data. All queries use POST requests with JSON bodies containing site identification, metrics to calculate, optional dimensions for grouping, time ranges, and filters.

## Authentication

Retrieve the API key using one of these methods:

**From 1Password:**
```bash
op read "op://Development/plausible api/notesPlain"
```

**From environment variable:**
```bash
export PLAUSIBLE_API_KEY=your_api_key_here
```

Include the key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

## Basic Query Structure

All queries POST to `https://plausible.io/api/v2/query` with a JSON body.

### Required Fields

- `site_id`: Domain configured in Plausible (e.g., "example.com")
- `metrics`: Array of metric names to calculate (e.g., ["visitors", "pageviews"])
- `date_range`: Time period string or array (e.g., "7d", "30d", ["2024-01-01", "2024-01-31"])

### Optional Fields

- `dimensions`: Array of properties to group by (e.g., ["visit:source", "visit:country"])
- `filters`: Array of filter conditions
- `limit`: Maximum number of results (default: 10000)
- `page`: Page number for pagination (default: 1)
- `order_by`: Array of [metric, direction] pairs for sorting

## Metrics

Available metrics to calculate:

- `visitors`: Number of unique visitors
- `visits`: Number of visits/sessions
- `pageviews`: Number of pageview events
- `bounce_rate`: Percentage of visits with only one page view
- `visit_duration`: Average visit duration in seconds
- `views_per_visit`: Average pages viewed per visit
- `events`: Total number of events (pageviews + custom events)

Request multiple metrics by including them in the array: `["visitors", "pageviews", "bounce_rate"]`.

## Dimensions

Dimensions group results by specific properties. Only one dimension type can be used per query.

### Event Dimensions

Group by page or event properties:

- `event:name`: Event name (e.g., "pageview", "download")
- `event:page`: Full page URL including query parameters
- `event:page.pathname`: Page path without query parameters
- `event:props:*`: Custom event properties (e.g., `event:props:author`)

### Visit Dimensions

Group by visitor or session properties:

- `visit:source`: Traffic source (e.g., "Google", "Twitter", "Direct")
- `visit:referrer`: Full referrer URL
- `visit:utm_medium`: Marketing medium (e.g., "cpc", "social")
- `visit:utm_source`: UTM source parameter
- `visit:utm_campaign`: UTM campaign name
- `visit:utm_content`: UTM content parameter
- `visit:utm_term`: UTM term parameter
- `visit:device`: Device type ("desktop", "mobile", "tablet")
- `visit:browser`: Browser name
- `visit:browser_version`: Browser version
- `visit:os`: Operating system
- `visit:os_version`: OS version
- `visit:country`: Country code (e.g., "US", "GB")
- `visit:country_name`: Full country name
- `visit:region`: Region/state code
- `visit:region_name`: Full region/state name
- `visit:city`: City name

### Time Dimensions

Group results by time periods. Only one time dimension can be used:

- `time:minute`: Group by minute (only with "day" date_range)
- `time:hour`: Group by hour (only with "day" date_range)
- `time:day`: Group by day (available with any date_range)
- `time:week`: Group by week (available with "month", "6mo", "12mo", or custom ranges)
- `time:month`: Group by month (available with "6mo", "12mo", or custom ranges)

Time dimensions are mutually exclusive. When using time dimensions, results sort chronologically automatically.

## Time Ranges

Specify the time period to analyze:

**Relative ranges:**
- `"day"`: Last 24 hours
- `"7d"`: Last 7 days
- `"30d"`: Last 30 days
- `"month"`: Current month
- `"6mo"`: Last 6 months
- `"12mo"`: Last 12 months

**Custom date range:**
```json
["2024-01-01", "2024-01-31"]
```

Use ISO 8601 format (YYYY-MM-DD) for custom ranges.

## Filtering

Apply filters to narrow results. Filters use array syntax with operator, dimension, and values.

### Filter Operators

- `is`: Exact match (e.g., `["is", "visit:country", ["US", "GB"]]`)
- `is_not`: Exclusion (e.g., `["is_not", "event:page", ["/admin"]]`)
- `contains`: Contains substring (e.g., `["contains", "event:page", ["/blog"]]`)
- `contains_not`: Does not contain (e.g., `["contains_not", "event:page", ["/test"]]`)
- `matches`: Regular expression match (e.g., `["matches", "event:page", ["^/user/\\d+$"]]`)
- `matches_not`: Does not match regex

### Combining Filters

Use `and` and `or` to combine multiple conditions:

**AND example:**
```json
{
  "filters": [
    ["and", [
      ["is", "visit:country", ["US"]],
      ["is", "visit:device", ["mobile"]]
    ]]
  ]
}
```

**OR example:**
```json
{
  "filters": [
    ["or", [
      ["is", "visit:source", ["Google"]],
      ["is", "visit:source", ["Bing"]]
    ]]
  ]
}
```

## Response Structure

The API returns JSON with three sections:

```json
{
  "results": [
    {
      "metrics": [99, 98, 94],
      "dimensions": ["Estonia", "Tallinn"]
    }
  ],
  "meta": {
    "imports_included": false,
    "total_rows": 342
  },
  "query": {
    // Echo of your query with backend modifications
  }
}
```

- `results`: Array of result objects with metrics array and dimensions array
- `meta`: Metadata including total_rows and imports_included flag
- `query`: Echo of the submitted query

Metrics in results correspond to the order of metrics in the request. Dimensions correspond to the order of dimensions in the request.

## Best Practices

**Performance:**
- Request only necessary metrics to reduce response time
- Use filters to narrow data before grouping
- Set appropriate limits to avoid large result sets
- Use pagination for queries returning many rows

**Rate Limits:**
- Default: 600 requests per hour
- Contact Plausible support for increased limits if needed
- Batch related queries when possible

**Query Optimization:**
- Start with simple queries, add complexity incrementally
- Use specific date ranges rather than very broad ranges
- Combine related metrics in single queries
- Use dimensions only when grouping is needed

**Error Handling:**
- Check response status codes
- Handle rate limit errors (429) with exponential backoff
- Validate required fields before sending requests
- Provide clear error messages for invalid queries

## Common Query Patterns

For detailed query patterns and examples, see:
- **`references/query-patterns.md`** - Common patterns and combinations
- **`references/examples.md`** - Real-world query examples
- **`examples/common-queries.json`** - Copy-paste ready JSON queries

## Quick Examples

**Basic visitor count:**
```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "date_range": "7d"
}
```

**Traffic sources breakdown:**
```json
{
  "site_id": "example.com",
  "metrics": ["visitors", "pageviews"],
  "dimensions": ["visit:source"],
  "date_range": "30d"
}
```

**Top pages with bounce rate:**
```json
{
  "site_id": "example.com",
  "metrics": ["pageviews", "bounce_rate"],
  "dimensions": ["event:page"],
  "date_range": "30d",
  "order_by": [["pageviews", "desc"]],
  "limit": 10
}
```

**Geographic analysis:**
```json
{
  "site_id": "example.com",
  "metrics": ["visitors"],
  "dimensions": ["visit:country", "visit:city"],
  "date_range": "month",
  "filters": [["is_not", "visit:country", [""]]]
}
```

## Additional Resources

For complete API documentation:
- **`references/api-reference.md`** - Full endpoint documentation, all metrics, dimensions, and operators

For detailed examples and use cases:
- **`references/examples.md`** - Comprehensive examples with explanations
- **`examples/common-queries.json`** - JSON query templates
