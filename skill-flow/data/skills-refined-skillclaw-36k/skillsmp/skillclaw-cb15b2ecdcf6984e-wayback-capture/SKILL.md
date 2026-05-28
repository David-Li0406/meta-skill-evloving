---
name: wayback-capture
description: Use this skill to find either the most recent or the earliest archived version of a URL from the Wayback Machine, depending on your needs.
---

# Find Wayback Machine Capture

Find either the most recent or the earliest archived snapshot of a URL from the Wayback Machine.

## Usage

To find the most recent capture:
```bash
npx tsx scripts/oldest-newest.ts <url> --newest-only [options]
```

To find the earliest capture:
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

**For the most recent capture (with --full):**
```
🆕 NEWEST:
  2024-01-15 14:30 (2 days ago)
  https://web.archive.org/web/20240115143000id_/https://example.com
```

**For the earliest capture (with --full):**
```
📜 OLDEST:
  1998-12-01 08:00 (9200 days ago)
  https://web.archive.org/web/19981201080000id_/https://example.com
```

## Script Execution

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## CDX API Endpoint

For the most recent capture:
```
https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=1&filter=statuscode:200&fastLatest=true
```

For the earliest capture:
```
https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=1&filter=statuscode:200
```

### Caching

CDX API responses are cached for 1 hour. Use `--no-cache` to bypass.

## Related Skills

- **wayback-range** - Show both oldest and newest with archive span
- **wayback-list** - List all snapshots with pagination