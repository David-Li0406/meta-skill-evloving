---
name: wayback-range
description: Show the archive time span for a URL from the Wayback Machine. Use when the user wants to see both the oldest and newest captures, the archive range, or how long a URL has been archived.
---

# Show Wayback Machine Archive Range

Show both the oldest and newest archived snapshots for a URL, displaying the full archive time span.

## Usage

```bash
npx tsx scripts/oldest-newest.ts <url> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to search for |

### Options

| Option | Description |
|--------|-------------|
| `--full` | Include archive URLs in output |
| `--json` | Output as JSON |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

**Default (compact):**
```
1998-12-01 08:00 (9200 days ago)
2024-01-15 14:30 (2 days ago)
```

**With --full:**
```
📜 OLDEST:
  1998-12-01 08:00 (9200 days ago)
  https://web.archive.org/web/19981201080000id_/https://example.com

🆕 NEWEST:
  2024-01-15 14:30 (2 days ago)
  https://web.archive.org/web/20240115143000id_/https://example.com

Archive span: 9198 days
```

## Script Execution

```bash
npx tsx scripts/oldest-newest.ts <url>
```

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## How It Works

Queries the CDX API twice:
1. Oldest capture: `limit=1` with default ascending sort
2. Newest capture: `limit=1` with `fastLatest=true`

Calculates the day span between first and last capture to show how long the URL has been tracked.

## Caching

CDX API responses are cached for 1 hour. Use `--no-cache` to bypass.

## Related Skills

- **wayback-oldest** - Find only the earliest capture
- **wayback-newest** - Find only the most recent capture
- **wayback-list** - List all snapshots with pagination
