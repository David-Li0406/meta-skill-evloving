---
name: wayback-cache
description: Manage Wayback Machine API cache. Use when clearing cached data, checking cache status, or bypassing cache for fresh API responses. Applies to all wayback operations (check, list, screenshot).
---

# Wayback Cache Management

Manage the OS tmpdir-based cache for Wayback Machine API responses.

## Usage

```bash
npx tsx scripts/cache.ts <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `clear` | Clear all cached Wayback data |
| `status` | Show cache directory location and file count |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache for single operation |

## Cache Location

Cached responses are stored in the OS temporary directory:
```
os.tmpdir()/wayback-cache/
```

Cache keys are generated from URLs and parameters using SHA-256 hashing.

## Cache TTL by Operation

| Operation | TTL | Rationale |
|-----------|-----|-----------|
| Availability API | 24 hours | Snapshots don't change often |
| CDX API | 1 hour | Snapshot list can change |
| Save status | 30 seconds | Only during polling |

Cached entries expire automatically and are deleted on access.

## Script Execution

```bash
npx tsx scripts/cache.ts <command> [options]
```

Commands:
- `clear` - Clear all cached Wayback data
- `status` - Show cache directory location and file count

## Clear Cache

Remove all cached API responses:
```bash
npx tsx scripts/cache.ts clear
```

This deletes all `.json` cache files from the cache directory.

## Check Cache Status

Display cache information:
```bash
npx tsx scripts/cache.ts status
```

Shows:
- Cache directory path
- Number of cached files
- Total cache size (if available)

## Usage Examples

```bash
# Clear all cache before checking a URL
npx tsx scripts/cache.ts clear
npx tsx scripts/check.ts https://example.com

# Clear cache, then list snapshots
npx tsx scripts/cache.ts clear
npx tsx scripts/list.ts https://example.com 20

# Check cache status
npx tsx scripts/cache.ts status
```

## Bypass Cache for Single Operation

Individual scripts support `--no-cache` to skip cache for one operation without clearing all cached data:

```bash
npx tsx scripts/check.ts https://example.com --no-cache
npx tsx scripts/list.ts https://example.com --no-cache
npx tsx scripts/screenshot.ts https://example.com --no-cache
```

The `--no-cache` flag bypasses reading from cache but still caches the fresh response for future requests.

## Cache Key Format

Cache keys are 16-character hexadecimal strings:
```
a1b2c3d4e5f6g7h8.json
```

Each key represents a unique URL + parameter combination.

## Manual Cache Inspection

View cache directory contents:
```bash
# On macOS/Linux
ls -la $(getconf DARWIN_USER_TEMP_DIR)/wayback-cache/
# Or
ls -la /tmp/wayback-cache/

# View individual cache file
cat /tmp/wayback-cache/a1b2c3d4e5f6g7h8.json | jq
```

## Related

- Use `wayback-check` to verify if a URL is archived
- Use `wayback-list` to see all captures with filtering options
- Use `wayback-screenshot` to retrieve visual screenshots
- Use `wayback-submit` to create a new archive
