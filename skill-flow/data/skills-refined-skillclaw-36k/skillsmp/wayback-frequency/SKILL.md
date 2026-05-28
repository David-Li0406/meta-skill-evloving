---
name: wayback-frequency
description: Analyze Wayback Machine capture frequency and rate for a URL. Use when the user wants to see how often a URL is archived, capture statistics, or archive density over time.
---

# Analyze Wayback Machine Capture Frequency

Analyze the capture frequency and rate for a URL over a specified time range.

## Usage

```bash
npx tsx scripts/frequency.ts <url> [from] [to] [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to analyze |
| `from` | No | Start date (YYYYMMDD or YYYY-MM). Default: oldest capture |
| `to` | No | End date (YYYYMMDD or YYYY-MM). Default: newest capture |

### Options

| Option | Description |
|--------|-------------|
| `--full` | Include detailed breakdown by year |
| `--json` | Output as JSON |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

**Default (compact):**
```
1423 captures over 3652 days
Average: 0.39/day, 11.87/month, 142.3/year
```

**With --full:**
```
📊 CAPTURE FREQUENCY ANALYSIS

URL: https://example.com
Range: 2015-01-01 12:00 to 2025-01-01 08:00 (3652 days)

Total captures: 1423
Average rate:
  0.39 captures per day
  11.87 captures per month
  142.3 captures per year

By year:
  2015: 156 captures
  2016: 203 captures
  2017: 189 captures
  ...
```

## Script Execution

```bash
npx tsx scripts/frequency.ts <url> [from] [to] [options]
```

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## Examples

```bash
# Analyze entire archive history
npx tsx scripts/frequency.ts https://example.com

# Analyze specific date range
npx tsx scripts/frequency.ts https://example.com 2020 2023

# Full breakdown with year-by-year stats
npx tsx scripts/frequency.ts https://example.com 2020 2023 --full

# Specific dates
npx tsx scripts/frequency.ts https://example.com 20200101 20231231
```

## Caching

CDX API responses are cached for 1 hour. Use `--no-cache` to bypass.

## Related Skills

- **wayback-range** - Show oldest and newest captures with archive span
- **wayback-list** - List all snapshots with pagination
- **wayback-oldest** - Find the earliest capture
- **wayback-newest** - Find the most recent capture
