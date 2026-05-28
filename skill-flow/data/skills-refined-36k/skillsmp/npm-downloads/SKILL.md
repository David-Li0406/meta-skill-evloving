---
name: npm-downloads
description: Get download statistics for an npm package over time. Use when the user asks for package download counts, popularity metrics, or usage statistics.
---

# Get npm Download Statistics

Retrieve download statistics for an npm package over a specified time period.

## Usage

```bash
npx tsx scripts/downloads.ts <package-name> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package-name` | Yes | The exact package name (case-sensitive) |

### Options

| Option | Description |
|--------|-------------|
| `--period=PERIOD` | Time period: last-week, last-month, last-year (default: last-month) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
Downloads for react (last-month)
--------------------------------
Period: 2023-10-01 to 2023-10-31 (31 days)
Total downloads: 15,234,567
Average per day: 491,438
Peak day: 2023-10-15 (678,234 downloads)
```

## Script Execution (Preferred)

```bash
npx tsx scripts/downloads.ts <package-name> [options]
```

Options:
- `--period=PERIOD` - Time period: last-week, last-month, last-year (default: last-month)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npm-registry plugin directory: `~/.claude/plugins/cache/npm-registry/`

## Downloads API

```
GET https://api.npmjs.org/downloads/range/{period}:{package}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `period` | Yes | Time period: `last-week`, `last-month`, `last-year`, or date range (`YYYY-MM-DD:YYYY-MM-DD`) |
| `package` | Yes | The exact package name (case-sensitive) |

### Examples

Last week:
```
https://api.npmjs.org/downloads/range/last-week:react
```

Last month:
```
https://api.npmjs.org/downloads/range/last-month:react
```

Last year:
```
https://api.npmjs.org/downloads/range/last-year:react
```

Custom date range:
```
https://api.npmjs.org/downloads/range/2023-01-01:2023-12-31:react
```

## Response Format

```json
{
  "downloads": [
    {
      "downloads": 1234567,
      "day": "2023-10-01"
    }
  ],
  "start": "2023-10-01",
  "end": "2023-10-31",
  "package": "react"
}
```

| `last-month` | Past 30 days |
| `last-year` | Past 365 days |
| `YYYY-MM-DD:YYYY-MM-DD` | Custom date range |

Custom date ranges must be in ISO 8601 format (YYYY-MM-DD).

## Download Trends

The data can show:
- **Weekly patterns** - Higher weekday downloads for development tools
- **Release spikes** - Sudden increases after major version releases
- **Seasonal trends** - Patterns based on project cycles
- **Long-term growth** - Overall adoption trends

## Caching

Download statistics are cached for 24 hours. Historical download data doesn't change, so the cache provides the same data with better performance.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npm-info` to get package metadata alongside download stats
- Use `npm-search` to discover packages with high download counts
- Use NPMS.io for quality scores alongside download metrics

## Error Handling

**Package not found**: Download stats are only available for published packages. Use `npm-exists` to verify the package exists first.

**Invalid period**: Ensure the period format is correct. Date ranges must use colons to separate dates from the package name.

**No data**: Very new packages may not have download statistics yet. Statistics are typically available within 24-48 hours of first publish.

## Data Limitations

- **Delay**: Download counts are typically 24-48 hours behind
- **Granularity**: Data is available per day, not per hour
- **Scope**: Counts include all download sources (npm install, CDN, mirrors)
- **Accuracy**: Numbers are approximate and may include failed downloads
