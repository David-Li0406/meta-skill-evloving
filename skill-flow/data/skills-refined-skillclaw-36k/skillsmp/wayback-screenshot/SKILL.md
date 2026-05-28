---
name: wayback-screenshot
description: Retrieve screenshots from the Wayback Machine. Use when the user wants to see how a webpage looked, get a visual snapshot, find archived screenshots, or view historical page appearance.
---

# Retrieve Wayback Machine Screenshots

Access existing screenshots stored by the Wayback Machine.

## Usage

```bash
npx tsx scripts/screenshot.ts <url> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | The URL to find screenshots for |

### Options

| Option | Description |
|--------|-------------|
| `--timestamp=DATE` | Get screenshot from specific capture (YYYYMMDDhhmmss) |
| `--list` | List available screenshots for URL |
| `--download=PATH` | Download screenshot to file |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
Screenshots for: https://example.com/

January 15, 2024 12:34 (3 days ago)
  https://web.archive.org/web/20240115123456im_/https://example.com/

December 1, 2023 08:00 (46 days ago)
  https://web.archive.org/web/20231201080000im_/https://example.com/

Total: 2 screenshot(s)
```

## Script Execution (Preferred)

```bash
npx tsx scripts/screenshot.ts <url> [options]
```

Options:
- `--timestamp=DATE` - Get screenshot from specific capture (YYYYMMDDhhmmss)
- `--list` - List available screenshots for URL
- `--download=PATH` - Download screenshot to file
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## Screenshot URL Pattern

```
https://web.archive.org/screenshot/{URL}
```

### Direct Access

Get the most recent screenshot:
```
https://web.archive.org/screenshot/https://example.com/
```

### With Timestamp

Get screenshot from a specific capture:
```
https://web.archive.org/web/{timestamp}im_/https://example.com/
```

The `im_` modifier returns the screenshot image for that timestamp.

### List Available Screenshots

Use CDX API with wildcard to find all screenshots:
```
https://web.archive.org/cdx/search/cdx?url=web.archive.org/screenshot/https://example.com/*&output=json
```

Or browse visually:
```
https://web.archive.org/web/*/https://web.archive.org/screenshot/https://example.com/*
```

## Via Wayback Toolbar

When viewing any archived page:
1. Look for the camera icon (📷) in the top-right of the Wayback toolbar
2. Click to view available screenshots for that capture

## From SPN2 Response

When submitting with `capture_screenshot=1`, the response includes:
```json
{
  "status": "success",
  "screenshot": "https://web.archive.org/web/20240115123456im_/https://example.com/"
}
```

```

## Caveats

- **Not all captures have screenshots** - depends on whether `capture_screenshot=1` was used during archiving
- **Undocumented feature** - may be unreliable or change without notice
- **Indexing delays** - newly captured screenshots may not appear immediately
- **Coverage varies** - older archives typically don't have screenshots

## Caching

Availability API responses are cached for 24 hours using the OS temporary directory (`os.tmpdir()`). Cache keys are generated from the URL using SHA-256 hashing. Cached responses expire automatically and are deleted on access.

Use `wayback-cache` to manage cached data:
```bash
npx tsx scripts/cache.ts clear    # Clear all cache
npx tsx scripts/cache.ts status   # Show cache status
```

See `wayback-cache` skill for complete cache management documentation.

## Related

- Use `wayback-submit --capture-screenshot` to create a new screenshot
- Use `wayback-check` to verify if a URL is archived
- Use `wayback-list` to see all captures (not just those with screenshots)
