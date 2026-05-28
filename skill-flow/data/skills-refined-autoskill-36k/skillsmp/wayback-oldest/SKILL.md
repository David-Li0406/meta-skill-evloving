---
name: wayback-oldest
description: Find the earliest archived version of a URL from the Wayback Machine. Use when the user wants to see the first capture, oldest archive, or original version of a webpage.
---

# Find Oldest Wayback Machine Capture

Find the earliest archived snapshot of a URL from the Wayback Machine.

## Usage

```bash
npx tsx scripts/oldest-newest.ts <url> --oldest-only [options]
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
1998-12-01 08:00 (9200 days ago)
```

**With --full:**
```
📜 OLDEST:
  1998-12-01 08:00 (9200 days ago)
  https://web.archive.org/web/19981201080000id_/https://example.com
```

## Script Execution

```bash
npx tsx scripts/oldest-newest.ts <url> --oldest-only
```

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## CDX API Endpoint

```
https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=1&filter=statuscode:200
```

The `limit=1` parameter with default ascending sort returns the oldest capture first.

## Caching

CDX API responses are cached for 1 hour. Use `--no-cache` to bypass.

## Related Skills

- **wayback-newest** - Find the most recent capture
- **wayback-range** - Show both oldest and newest with archive span
- **wayback-list** - List all snapshots with pagination
