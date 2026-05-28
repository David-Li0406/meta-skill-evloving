---
name: wayback-submit
description: Submit a URL to the Wayback Machine for archiving. Use when the user wants to archive a webpage, save a page to the Internet Archive, preserve a URL, or create a snapshot.
---

# Submit URL to Wayback Machine

Submit a URL to the Internet Archive's Wayback Machine using the Save Page Now 2 (SPN2) API.

## Usage

```bash
npx tsx scripts/submit.ts <url> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `url` | Yes | URL to archive |

### Options

| Option | Description |
|--------|-------------|
| `--no-raw` | Include Wayback toolbar in archived URL |
| `--key=ACCESS:SECRET` | Use API authentication (get keys at https://archive.org/account/s3.php) |

### Output

When submission succeeds:
```
✓ Archive submitted successfully
  Job ID: spn2-abc123...
  Check status: https://web.archive.org/save/status/spn2-abc123...

  Waiting for capture...
  ✓ Capture complete
  URL: https://web.archive.org/web/20240115123456id_/https://example.com
```

## Script Execution (Preferred)

```bash
npx tsx scripts/submit.ts <url> [options]
```

Options:
- `--no-raw` - Include Wayback toolbar in archived URL
- `--key=ACCESS:SECRET` - Use API authentication

Run from the wayback plugin directory: `~/.claude/plugins/cache/wayback/`

## Authentication

Get API keys at https://archive.org/account/s3.php (requires free account).

**Header format:**
```
Authorization: LOW {access_key}:{secret_key}
```

### Rate Limits

| Limit | Authenticated | Anonymous |
|-------|---------------|-----------|
| Concurrent captures | 12 | 6 |
| Daily captures | 100,000 | 4,000 |
| Per-URL daily | 10 | 10 |
| Capture timeout | 50s page load, 2min total |

## SPN2 API

**Endpoint:** `POST https://web.archive.org/save`

### Basic Request

```bash
curl -X POST https://web.archive.org/save \
  -H "Accept: application/json" \
  -H "Authorization: LOW myaccesskey:mysecret" \
  -d "url=https://example.com"
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `url` | URL to archive (required) |
| `capture_all=1` | Capture even 4xx/5xx error pages |
| `capture_outlinks=1` | Also archive linked pages (first 100) |
| `capture_screenshot=1` | Generate PNG screenshot |
| `delay_wb_availability=1` | Delay indexing ~12 hours (reduces load) |
| `skip_first_archive=1` | Skip check if URL was already archived |
| `if_not_archived_within=30d` | Skip if archived within timeframe (e.g., `30d`, `1h`) |
| `js_behavior_timeout=10` | Run JavaScript for N seconds (max 30) |
| `force_get=1` | Use simple HTTP GET instead of browser |
| `capture_cookie=name=value` | Include custom cookie in request |
| `target_username` / `target_password` | Login credentials for protected pages |

### Response

**Success:**
```json
{
  "url": "https://example.com",
  "job_id": "spn2-abc123..."
}
```

## Check Job Status

```bash
curl "https://web.archive.org/save/status/{job_id}" \
  -H "Authorization: LOW myaccesskey:mysecret"
```

**Pending:**
```json
{"status": "pending", "resources": []}
```

**Success:**
```json
{
  "status": "success",
  "timestamp": "20240115123456",
  "original_url": "https://example.com",
  "resources": ["https://example.com/style.css"],
  "outlinks": {},
  "screenshot": "https://web.archive.org/web/.../screenshot.png"
}
```

**Error codes:** `error:blocked-url`, `error:too-many-daily-captures`, `error:soft-time-limit-exceeded`, `error:invalid-host-resolution`

## Check Your Quota

```bash
curl "https://web.archive.org/save/status/user" \
  -H "Authorization: LOW myaccesskey:mysecret"
```

Returns: `{"available": 99950, "processing": 2}`

## Simple Method (No Auth)

For quick one-off saves without authentication:

```
https://web.archive.org/save/{URL}
```

Lower rate limits apply (6 concurrent, 4k daily).

2. Use `delay_wb_availability=1` for batch jobs (reduces server load)
3. Check job status for captures that take time (JS-heavy pages)
4. Use `capture_screenshot=1` for visual verification
