---
name: wayback-check
description: Check if a URL is archived in the Wayback Machine. Use when the user asks to check archive status, verify if a page is saved, or find archived versions of a URL.
---

# Check Wayback Machine Archive Status

Check if a URL has been archived by the Internet Archive's Wayback Machine.

## Usage

```bash
npx tsx scripts/check.ts <url> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to check |

### Options

| Option | Description |
|--------|-------------|
| `--no-raw` | Include Wayback toolbar in archived URL |
| `--timestamp=DATE` | Find snapshot closest to date (YYYYMMDD or YYYYMMDDhhmmss) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

When archived:
```
✓ Archived
  Timestamp: January 1, 2024 (3 days ago)
  URL: https://web.archive.org/web/20240101120000id_/https://example.com
```

When not archived:
```
✗ Not archived
  Consider using wayback-submit to archive this URL.
```

## Script Execution (Preferred)

```bash
npx tsx scripts/check.ts <url> [options]
```

Options:
- `--no-raw` - Include Wayback toolbar in archived URL
- `--timestamp=DATE` - Find snapshot closest to date (YYYYMMDD or YYYYMMDDhhmmss)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## Availability API

```
https://archive.org/wayback/available?url={URL}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | The URL to check |
| `timestamp` | No | Find snapshot closest to this date (YYYYMMDDhhmmss, partial dates OK) |
| `callback` | No | JSONP callback for cross-domain requests |

### Examples

Latest snapshot:
```
https://archive.org/wayback/available?url=https://example.com
```

Snapshot closest to a specific date:
```
https://archive.org/wayback/available?url=https://example.com&timestamp=20200101
```

## Response Interpretation

**Archived** - Response contains `archived_snapshots.closest` with:
- `available`: true
- `url`: The archived URL (format: `https://web.archive.org/web/{timestamp}/{original_url}`)
- `timestamp`: Archive timestamp (YYYYMMDDhhmmss format)
- `status`: HTTP status code

**Not Archived** - Response has empty `archived_snapshots` object.

## Raw Mode

By default, append `id_` after the timestamp in URLs to get raw content without the Wayback toolbar:
- With toolbar: `https://web.archive.org/web/20240101120000/https://example.com`
- Raw (no toolbar): `https://web.archive.org/web/20240101120000id_/https://example.com`

## URL Modifiers

| Modifier | URL Pattern | Description |
|----------|-------------|-------------|
| (none) | `/web/{ts}/` | Page with Wayback toolbar |
| `id_` | `/web/{ts}id_/` | Raw page content (no toolbar) |
| `im_` | `/web/{ts}im_/` | Screenshot image |
| `js_` | `/web/{ts}js_/` | JavaScript content |
| `cs_` | `/web/{ts}cs_/` | CSS content |

## Related

- Use `wayback-screenshot` to retrieve visual screenshots of archived pages
- Use `wayback-list` to see all captures with filtering options
- Use `wayback-submit` to create a new archive (with optional screenshot)

## Caching

Availability API responses are cached for 24 hours using the OS temporary directory (`os.tmpdir()`). Cache keys are generated from the URL and timestamp parameters using SHA-256 hashing. Cached responses expire automatically and are deleted on access.

Use `wayback-cache` to manage cached data:
```bash
npx tsx scripts/cache.ts clear    # Clear all cache
npx tsx scripts/cache.ts status   # Show cache status
```

See `wayback-cache` skill for complete cache management documentation.

## Error Handling

If the Wayback Machine API returns an error or is unavailable, retry after a brief delay. The API may be rate-limited during high traffic periods.
