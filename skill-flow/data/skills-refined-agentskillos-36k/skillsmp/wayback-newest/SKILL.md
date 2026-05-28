---
name: wayback-newest
description: Find the most recent archived version of a URL from the Wayback Machine. Use when the user wants to see the latest capture, newest archive, or current version of a webpage.
---

# Find Newest Wayback Machine Capture

Find the most recent archived snapshot of a URL from the Wayback Machine.

## Usage

```bash
npx tsx scripts/oldest-newest.ts <url> --newest-only [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to search for |

### Options

| Option | Description |
|--------|-------------|
| `--full` | Include archive URL in output |
| `--json` | Output as JSON |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

**Default (compact):**
```
2024-01-15 14:30 (2 days ago)
```

**With --full:**
```
🆕 NEWEST:
  2024-01-15 14:30 (2 days ago)
  https://web.archive.org/web/20240115143000id_/https://example.com
```

## Script Execution

```bash
npx tsx scripts/oldest-newest.ts <url> --newest-only
```

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## CDX API Endpoint

```
https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=1&filter=statuscode:200&fastLatest=true
```

The `fastLatest=true` parameter efficiently returns the most recent capture without scanning the entire index.

## Caching

CDX API responses are cached for 1 hour. Use `--no-cache` to bypass.

## Related Skills

- **wayback-oldest** - Find the earliest capture
- **wayback-range** - Show both oldest and newest with archive span
- **wayback-list** - List all snapshots with pagination
