# Plausible Analytics API v2 Reference

Complete reference for the Plausible Analytics API v2 query endpoint.

## Endpoint

**URL:** `https://plausible.io/api/v2/query`  
**Method:** `POST`  
**Content-Type:** `application/json`  
**Authentication:** Bearer token in Authorization header

## Request Structure

### Headers

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Request Body

All fields except `site_id`, `metrics`, and `date_range` are optional.

```json
{
  "site_id": "string (required)",
  "metrics": ["string"] (required),
  "date_range": "string | [string, string] (required)",
  "dimensions": ["string"] (optional),
  "filters": [filter] (optional),
  "limit": number (optional, default: 10000),
  "page": number (optional, default: 1),
  "order_by": [[string, "asc" | "desc"]] (optional)
}
```

## Required Fields

### site_id

**Type:** `string`  
**Description:** The domain of your site as configured in Plausible  
**Example:** `"example.com"`

### metrics

**Type:** `array of strings`  
**Description:** Metrics to calculate. Must include at least one metric.  
**Example:** `["visitors", "pageviews"]`

### date_range

**Type:** `string | [string, string]`  
**Description:** Time period to analyze

**String formats:**
- `"day"` - Last 24 hours
- `"7d"` - Last 7 days
- `"30d"` - Last 30 days
- `"month"` - Current month
- `"6mo"` - Last 6 months
- `"12mo"` - Last 12 months

**Array format (custom range):**
- `["2024-01-01", "2024-01-31"]` - ISO 8601 dates (YYYY-MM-DD)

## Optional Fields

### dimensions

**Type:** `array of strings`  
**Description:** Properties to group results by. Only one dimension type can be used per query.

**Available dimensions:** See Dimensions section below.

**Example:** `["visit:source", "visit:country"]`

**Note:** Time dimensions are mutually exclusive. Event and visit dimensions can be combined.

### filters

**Type:** `array of filter expressions`  
**Description:** Conditions to filter the data

**Filter syntax:** `[operator, dimension, values]`

**Operators:**
- `"is"` - Exact match
- `"is_not"` - Exclusion
- `"contains"` - Contains substring
- `"contains_not"` - Does not contain
- `"matches"` - Regular expression match
- `"matches_not"` - Does not match regex

**Combining filters:**
- `["and", [filter1, filter2, ...]]` - All conditions must match
- `["or", [filter1, filter2, ...]]` - Any condition can match

**Example:**
```json
{
  "filters": [
    ["is", "visit:country", ["US", "GB"]],
    ["contains", "event:page", ["/blog"]]
  ]
}
```

### limit

**Type:** `number`  
**Description:** Maximum number of results to return  
**Default:** `10000`  
**Example:** `100`

### page

**Type:** `number`  
**Description:** Page number for pagination (1-indexed)  
**Default:** `1`  
**Example:** `2`

### order_by

**Type:** `array of [string, "asc" | "desc"]`  
**Description:** Sort results by metric or dimension

**Example:** `[["pageviews", "desc"], ["visitors", "asc"]]`

## Metrics

Complete list of available metrics:

| Metric | Description | Type |
|--------|-------------|------|
| `visitors` | Number of unique visitors | Count |
| `visits` | Number of visits/sessions | Count |
| `pageviews` | Number of pageview events | Count |
| `bounce_rate` | Percentage of visits with only one page view | Percentage |
| `visit_duration` | Average visit duration in seconds | Duration |
| `views_per_visit` | Average pages viewed per visit | Average |
| `events` | Total number of events (pageviews + custom events) | Count |

**Notes:**
- Request multiple metrics by including them in the array
- Metrics in response correspond to order in request
- Some metrics may not be available for all dimension combinations

## Dimensions

### Event Dimensions

Group by page or event properties:

| Dimension | Description | Example Values |
|-----------|-------------|----------------|
| `event:name` | Event name | `"pageview"`, `"download"`, `"click"` |
| `event:page` | Full page URL with query parameters | `"https://example.com/page?utm_source=google"` |
| `event:page.pathname` | Page path without query parameters | `"/page"`, `"/blog/post"` |
| `event:props:*` | Custom event properties | `event:props:author`, `event:props:category` |

### Visit Dimensions

Group by visitor or session properties:

| Dimension | Description | Example Values |
|-----------|-------------|----------------|
| `visit:source` | Traffic source | `"Google"`, `"Twitter"`, `"Direct"` |
| `visit:referrer` | Full referrer URL | `"https://google.com/search?q=..."` |
| `visit:utm_medium` | Marketing medium | `"cpc"`, `"social"`, `"email"` |
| `visit:utm_source` | UTM source parameter | `"google"`, `"newsletter"` |
| `visit:utm_campaign` | UTM campaign name | `"summer_sale"`, `"product_launch"` |
| `visit:utm_content` | UTM content parameter | `"banner"`, `"link"` |
| `visit:utm_term` | UTM term parameter | `"keyword"` |
| `visit:device` | Device type | `"desktop"`, `"mobile"`, `"tablet"` |
| `visit:browser` | Browser name | `"Chrome"`, `"Firefox"`, `"Safari"` |
| `visit:browser_version` | Browser version | `"120.0"`, `"119.1"` |
| `visit:os` | Operating system | `"Windows"`, `"macOS"`, `"Linux"` |
| `visit:os_version` | OS version | `"14.0"`, `"11"` |
| `visit:country` | Country code (ISO 3166-1 alpha-2) | `"US"`, `"GB"`, `"DE"` |
| `visit:country_name` | Full country name | `"United States"`, `"United Kingdom"` |
| `visit:region` | Region/state code | `"CA"`, `"NY"`, `"ON"` |
| `visit:region_name` | Full region/state name | `"California"`, `"New York"` |
| `visit:city` | City name | `"San Francisco"`, `"London"` |

### Time Dimensions

Group results by time periods. Only one time dimension can be used per query.

| Dimension | Description | Compatible date_ranges |
|-----------|-------------|----------------------|
| `time:minute` | Group by minute | `"day"` only |
| `time:hour` | Group by hour | `"day"` only |
| `time:day` | Group by day | All date ranges |
| `time:week` | Group by week | `"month"`, `"6mo"`, `"12mo"`, custom ranges |
| `time:month` | Group by month | `"6mo"`, `"12mo"`, custom ranges |

**Important:** Time dimensions are mutually exclusive. When using a time dimension, results are automatically sorted chronologically.

## Filter Operators

### is

Exact match. Values must match exactly.

**Syntax:** `["is", dimension, [value1, value2, ...]]`

**Example:**
```json
["is", "visit:country", ["US", "GB", "CA"]]
```

### is_not

Exclusion. Values must not match.

**Syntax:** `["is_not", dimension, [value1, value2, ...]]`

**Example:**
```json
["is_not", "event:page", ["/admin", "/login"]]
```

### contains

Contains substring. Dimension value must contain any of the specified strings.

**Syntax:** `["contains", dimension, [substring1, substring2, ...]]`

**Example:**
```json
["contains", "event:page", ["/blog", "/articles"]]
```

### contains_not

Does not contain substring.

**Syntax:** `["contains_not", dimension, [substring1, substring2, ...]]`

**Example:**
```json
["contains_not", "event:page", ["/test", "/staging"]]
```

### matches

Regular expression match. Dimension value must match the regex pattern.

**Syntax:** `["matches", dimension, [pattern1, pattern2, ...]]`

**Example:**
```json
["matches", "event:page", ["^/user/\\d+$", "^/post/[a-z]+$"]]
```

**Note:** Use double backslashes for escape sequences in JSON.

### matches_not

Does not match regular expression.

**Syntax:** `["matches_not", dimension, [pattern1, pattern2, ...]]`

**Example:**
```json
["matches_not", "event:page", ["^/admin", "^/private"]]
```

## Combining Filters

### AND

All conditions must match.

**Syntax:** `["and", [filter1, filter2, ...]]`

**Example:**
```json
{
  "filters": [
    ["and", [
      ["is", "visit:country", ["US"]],
      ["is", "visit:device", ["mobile"]],
      ["contains", "event:page", ["/blog"]]
    ]]
  ]
}
```

### OR

Any condition can match.

**Syntax:** `["or", [filter1, filter2, ...]]`

**Example:**
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

### Nested Combinations

Combine AND and OR for complex logic.

**Example:**
```json
{
  "filters": [
    ["and", [
      ["or", [
        ["is", "visit:country", ["US"]],
        ["is", "visit:country", ["CA"]]
      ]],
      ["is", "visit:device", ["mobile"]]
    ]]
  ]
}
```

## Response Structure

### Success Response

**Status Code:** `200 OK`

**Body:**
```json
{
  "results": [
    {
      "metrics": [number, number, ...],
      "dimensions": [string, string, ...]
    }
  ],
  "meta": {
    "imports_included": boolean,
    "total_rows": number
  },
  "query": {
    // Echo of submitted query with any backend modifications
  }
}
```

**Fields:**
- `results`: Array of result objects
  - `metrics`: Array of metric values in same order as request
  - `dimensions`: Array of dimension values in same order as request
- `meta`: Metadata
  - `imports_included`: Whether imported data is included
  - `total_rows`: Total number of rows available
- `query`: Echo of the submitted query

### Error Response

**Status Codes:**
- `400` - Bad Request (invalid query parameters)
- `401` - Unauthorized (invalid or missing API key)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

**Body:**
```json
{
  "error": "Error message description"
}
```

## Rate Limits

- **Default:** 600 requests per hour per API key
- **Rate limit header:** `X-RateLimit-Remaining` (when available)
- **Contact:** Plausible support for increased limits

## Pagination

For large result sets, use pagination:

```json
{
  "limit": 100,
  "page": 1
}
```

Check `meta.total_rows` to determine total pages needed.

## Best Practices

1. **Request only necessary metrics** - Reduces response time
2. **Use specific date ranges** - Avoid very broad ranges when possible
3. **Apply filters early** - Filter before grouping when possible
4. **Set appropriate limits** - Avoid requesting more data than needed
5. **Handle rate limits** - Implement exponential backoff for 429 errors
6. **Validate inputs** - Check required fields before sending requests
7. **Use pagination** - For queries returning many rows

## Common Errors

### Invalid site_id

**Error:** `400 Bad Request`  
**Cause:** Site not found or API key doesn't have access  
**Solution:** Verify site_id matches domain in Plausible settings

### Invalid dimension combination

**Error:** `400 Bad Request`  
**Cause:** Using incompatible dimensions (e.g., multiple time dimensions)  
**Solution:** Use only one time dimension, or compatible event/visit dimensions

### Rate limit exceeded

**Error:** `429 Too Many Requests`  
**Cause:** Exceeded 600 requests per hour  
**Solution:** Implement rate limiting, batch queries, or request limit increase

### Invalid date range

**Error:** `400 Bad Request`  
**Cause:** Invalid date format or range  
**Solution:** Use supported formats: "day", "7d", "30d", "month", "6mo", "12mo", or ["YYYY-MM-DD", "YYYY-MM-DD"]
