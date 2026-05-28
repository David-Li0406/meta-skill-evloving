---
name: wayback-list
description: List Wayback Machine snapshots for a URL. Use when the user wants to see archive history, view all snapshots, find older versions, or browse archived copies of a webpage.
---

# List Wayback Machine Snapshots

Retrieve a list of archived snapshots for a URL from the Wayback Machine CDX API.

## Usage

```bash
npx tsx scripts/list.ts <url> [limit] [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to search for |
| `limit` | No | Max number of results (default: unlimited) |

### Options

| Option | Description |
|--------|-------------|
| `--no-raw` | Include Wayback toolbar in URLs |
| `--with-screenshots` | Cross-reference to show which captures have screenshots (📷) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
January 1, 2024 (3 days ago)
  https://web.archive.org/web/20240101120000id_/https://example.com

December 15, 2023 (20 days ago)
  https://web.archive.org/web/20231215100000id_/https://example.com

Total: 2 snapshot(s)
```

## Script Execution (Preferred)

```bash
npx tsx scripts/list.ts <url> [limit] [options]
```

Options:
- `--no-raw` - Include Wayback toolbar in URLs
- `--with-screenshots` - Cross-reference to show which captures have screenshots (📷)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## CDX API Endpoint

```
https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit={N}
```

## Authentication (Optional)

Most CDX queries don't require authentication. For restricted data access:

```bash
# Cookie-based auth for restricted content
curl "https://web.archive.org/cdx/search/cdx?url=..." \
  --cookie "cdx-auth-token=YOUR_TOKEN"
```

Get API keys at https://archive.org/account/s3.php

## Parameters

| Parameter | Description |
|-----------|-------------|
| `url` | The URL to search for (required) |
| `output` | Response format: `json` (recommended) |
| `matchType` | `exact` (default), `prefix`, `host`, or `domain` |
| `limit` | Max results. Use `-N` for last N results |
| `offset` | Skip first N records |
| `from` | Start date (YYYYMMDD or partial like "2020") |
| `to` | End date (YYYYMMDD or partial) |
| `filter` | Field filter: `[!]field:regex` (e.g., `statuscode:200`, `!mimetype:image.*`) |
| `collapse` | Dedupe: `field` or `field:N` (e.g., `timestamp:8` = daily) |
| `fl` | Fields to return: comma-separated (urlkey, timestamp, original, mimetype, statuscode, digest, length) |
| `fastLatest` | `true` for efficient recent results |
| `showResumeKey` | `true` to get pagination token |
| `resumeKey` | Continue from previous query |

## How to List Snapshots

Use WebFetch to query the CDX API:

```
https://web.archive.org/cdx/search/cdx?url=https://example.com&output=json&limit=10
```

## Response Format

JSON array where first row is headers:
```json
[
  ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"],
  ["com,example)/", "20240101120000", "https://example.com/", "text/html", "200", "ABC123", "1234"]
]
```

## Constructing Archive URLs

From timestamp, build the archived URL:
```
https://web.archive.org/web/{timestamp}/{original_url}
```

For raw content (no Wayback toolbar):
```
https://web.archive.org/web/{timestamp}id_/{original_url}
```

## Common Queries

```
# Only successful pages
&filter=statuscode:200

# Exclude images
&filter=!mimetype:image.*

# One snapshot per day (collapse on first 8 digits of timestamp)
&collapse=timestamp:8

# One snapshot per hour
&collapse=timestamp:10

# Date range (partial dates work)
&from=2023&to=2024

# All pages under a path (prefix match)
&url=example.com/blog/&matchType=prefix

# Entire domain including subdomains
&url=example.com&matchType=domain

# Get last 5 snapshots efficiently
&limit=-5&fastLatest=true

# Paginate large results
&showResumeKey=true&limit=1000
# Then continue with: &resumeKey={token_from_previous}
```

## Checking for Screenshots

The CDX API doesn't include a screenshot field. To find captures with screenshots, cross-reference with:

```
https://web.archive.org/cdx/search/cdx?url=web.archive.org/screenshot/{URL}/*&output=json
```

The `--with-screenshots` flag in the script does this automatically, showing 📷 next to captures that have screenshots.

## Caching

CDX API responses are cached for 1 hour using the OS temporary directory (`os.tmpdir()`). Cache keys are generated from the URL and query parameters using SHA-256 hashing. Cached responses expire automatically and are deleted on access.

Use `wayback-cache` to manage cached data:
```bash
npx tsx scripts/cache.ts clear    # Clear all cache
npx tsx scripts/cache.ts status   # Show cache status
```

See `wayback-cache` skill for complete cache management documentation.

## Output Format (with --with-screenshots)

```
2024-01-15 12:34 (3 days ago) 📷
  https://web.archive.org/web/20240115123456id_/https://example.com/
  📷 https://web.archive.org/web/20240115123456im_/https://example.com/

2024-01-10 08:00 (8 days ago)
  https://web.archive.org/web/20240110080000id_/https://example.com/

Total: 2 snapshot(s)
Screenshots: 1 capture(s) have screenshots
```
