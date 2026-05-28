# Real-Debrid Cleanup - API Reference

Complete API documentation and advanced configuration for the Real-Debrid cleanup skill.

## API Endpoints

### Base URL
```
https://api.real-debrid.com/rest/1.0
```

### Authentication
All requests require Bearer token authentication:
```bash
-H 'Authorization: Bearer YOUR_API_KEY'
```

---

### 1. List Torrents

**Endpoint**: `GET /torrents`

**Parameters**:
- `limit`: Number of torrents per page (max 100)
- `page`: Page number (1-indexed)
- `offset`: Alternative to page
- `filter`: Filter by status (optional)

**Example**:
```bash
curl -s 'https://api.real-debrid.com/rest/1.0/torrents?limit=100&page=1' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response**:
```json
[
  {
    "id": "4QMHWXG66PW64",
    "filename": "Naruto Complete",
    "hash": "a1b2c3d4e5f6...",
    "bytes": 53687091200,
    "host": "real-debrid.com",
    "split": 2000,
    "progress": 100,
    "status": "downloaded",
    "added": "2024-01-15T10:30:00.000Z",
    "links": ["https://..."],
    "ended": "2024-01-15T11:45:00.000Z"
  }
]
```

---

### 2. Get Torrent Info

**Endpoint**: `GET /torrents/info/{torrent_id}`

**Example**:
```bash
curl -s 'https://api.real-debrid.com/rest/1.0/torrents/info/4QMHWXG66PW64' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response**:
```json
{
  "id": "4QMHWXG66PW64",
  "filename": "Naruto Complete",
  "original_filename": "[Anime Time] Naruto...",
  "hash": "a1b2c3d4e5f6...",
  "bytes": 53687091200,
  "original_bytes": 53687091200,
  "host": "real-debrid.com",
  "split": 2000,
  "progress": 100,
  "status": "downloaded",
  "added": "2024-01-15T10:30:00.000Z",
  "files": [
    {
      "id": 1,
      "path": "/Naruto/Season 01/S01E01.mkv",
      "bytes": 450000000,
      "selected": 1
    }
  ],
  "links": ["https://real-debrid.com/d/..."],
  "ended": "2024-01-15T11:45:00.000Z",
  "speed": 0,
  "seeders": 42
}
```

---

### 3. Delete Torrent

**Endpoint**: `DELETE /torrents/delete/{torrent_id}`

**Example**:
```bash
curl -X DELETE 'https://api.real-debrid.com/rest/1.0/torrents/delete/ABC123' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response**: `204 No Content` (success)

**Error Responses**:
- `401 Unauthorized`: Invalid API key
- `403 Forbidden`: Can't delete active torrent
- `404 Not Found`: Torrent doesn't exist

---

### 4. Get User Info

**Endpoint**: `GET /user`

**Example**:
```bash
curl -s 'https://api.real-debrid.com/rest/1.0/user' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response**:
```json
{
  "id": 123456789,
  "username": "your_username",
  "email": "your@email.com",
  "points": 0,
  "locale": "en",
  "avatar": "https://...",
  "type": "premium",
  "premium": 1682899200,
  "expiration": "2026-01-11T00:00:00.000Z"
}
```

---

## Status Codes Reference

### Healthy Statuses (Don't Delete)
- **`downloaded`**: Fully downloaded and available
- **`downloading`**: Currently downloading (progress < 100)
- **`uploading`**: Magnet being processed/uploaded
- **`seeding`**: Available and seeding to others
- **`queued`**: Waiting in download queue
- **`compressing`**: Files being compressed by RD

### Dead Statuses (Safe to Delete)
- **`magnet_error`**: Failed to resolve magnet link (bad hash)
- **`dead`**: Files no longer available on RD servers
- **`virus`**: Flagged by Real-Debrid antivirus
- **`error`**: Generic error (timeout, corruption, etc.)
- **`magnet_conversion`**: Stuck converting magnet (>1 hour)
- **`timeout`**: Download timeout (stuck)

### Active Statuses (Wait Before Deleting)
- **`waiting_files_selection`**: Needs file selection
- **`processing`**: Being processed by RD

---

## Rate Limiting

Real-Debrid API limits:
- **500 requests per hour** per IP address
- **Burst limit**: 10 requests per second

### Script Rate Limit Handling

The cleanup script adds delays:
```python
time.sleep(0.5)  # 0.5s between each request
```

**For 500 torrents**:
- Listing: ~3 pages = 3 requests = 1.5s
- Deletion: 50 dead torrents = 50 requests = 25s
- **Total**: ~27s (well under rate limit)

**For 2000 torrents**:
- Listing: ~20 pages = 20 requests = 10s
- Deletion: 200 dead torrents = 200 requests = 100s
- **Total**: ~110s (still safe)

---

## Whitelist Configuration

### By Filename (Partial Match)
```python
WHITELIST = [
    "Naruto",          # Matches: "Naruto Complete", "[Anime] Naruto", etc.
    "Breaking Bad",    # Matches any torrent with "Breaking Bad"
    "Avatar"           # Matches: "Avatar (2009)", "Avatar: The Last Airbender"
]
```

### By Torrent ID (Exact Match)
```python
WHITELIST = [
    "4QMHWXG66PW64",   # Exact torrent ID
    "ABCDEF123456",
    "ZYXWVU987654"
]
```

### Mixed Approach
```python
WHITELIST = [
    "Naruto",              # By name
    "4QMHWXG66PW64",      # By ID
    "Breaking Bad",        # By name
    "XYZ789"              # By ID
]
```

### Dynamic Whitelist (Advanced)
Load from file:
```python
def load_whitelist():
    try:
        with open("/home/automation/config/rd_whitelist.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

WHITELIST = load_whitelist()
```

---

## Advanced Configuration

### Custom Dead Status List

Add more statuses to delete:
```python
DEAD_STATUSES = [
    "magnet_error",
    "dead",
    "virus",
    "error",
    "timeout",
    "magnet_conversion",  # Add this
    "waiting_files_selection"  # And this (if stuck >24h)
]
```

### Filter by Age

Only delete torrents older than X days:
```python
from datetime import datetime, timedelta

def is_old_enough(torrent, min_age_days=7):
    """Check if torrent is at least min_age_days old"""
    added = datetime.fromisoformat(torrent["added"].replace("Z", "+00:00"))
    age = datetime.now(timezone.utc) - added
    return age.days >= min_age_days

# In identify_dead_torrents():
if not is_old_enough(torrent, min_age_days=7):
    continue  # Skip recent torrents
```

### Filter by Size

Only delete small dead torrents (likely broken):
```python
def is_small_torrent(torrent, max_size_gb=1):
    """Check if torrent is smaller than max_size_gb"""
    size_gb = torrent.get("bytes", 0) / (1024**3)
    return size_gb < max_size_gb

# In identify_dead_torrents():
if not is_small_torrent(torrent, max_size_gb=1):
    continue  # Skip large dead torrents (might recover)
```

---

## Automation Setup

### Cron Job (Weekly Cleanup)

```bash
# Add to automation user crontab
crontab -e

# Run every Sunday at 3am
0 3 * * 0 /usr/bin/python3 /home/automation/scripts/cleanup_realdebrid.py --dry-run >> /home/automation/logs/rd-cleanup.log 2>&1
```

**Note**: Uses `--dry-run` for safety. Remove flag for actual deletion.

### Script with Email Notification

```bash
#!/bin/bash
# /home/automation/scripts/rd_cleanup_notify.sh

OUTPUT=$(python3 /home/automation/scripts/cleanup_realdebrid.py 2>&1)
DELETED=$(echo "$OUTPUT" | grep "Deleted:" | awk '{print $2}')

if [ "$DELETED" -gt 0 ]; then
    echo "$OUTPUT" | mail -s "RD Cleanup: $DELETED torrents deleted" your@email.com
fi
```

---

## Troubleshooting

### Issue: 401 Unauthorized

**Symptoms**:
```
❌ API Error: 401
```

**Causes**:
1. Invalid API key
2. Expired API key
3. Wrong API key format

**Solutions**:

1. **Get new API key**:
   - Go to https://real-debrid.com/apitoken
   - Generate new key
   - Update in `SECRETS.md`

2. **Set environment variable**:
   ```bash
   export RD_API_KEY="your_new_key"
   python3 cleanup_realdebrid.py
   ```

3. **Update script directly**:
   ```python
   # In cleanup_realdebrid.py
   API_KEY = "your_new_key_here"
   ```

---

### Issue: 403 Forbidden (Can't Delete)

**Symptoms**:
```
✗ Failed: TorrentName.mkv
```

**Causes**:
1. Torrent is actively downloading
2. Torrent is being processed
3. Torrent is locked by another process

**Solutions**:

1. **Wait for download to finish**:
   ```bash
   # Check torrent status
   curl -s 'https://api.real-debrid.com/rest/1.0/torrents/info/TORRENT_ID' \
     -H 'Authorization: Bearer YOUR_KEY' | jq .status
   ```

2. **Cancel download first**:
   - Go to Real-Debrid web UI
   - Stop/cancel the torrent
   - Run cleanup again

3. **Remove from whitelist** (if accidentally protected):
   ```python
   # Check if torrent ID or name is in WHITELIST
   # Remove it and try again
   ```

---

### Issue: 429 Too Many Requests

**Symptoms**:
```
❌ API Error: 429
```

**Cause**: Exceeded rate limit (>500 requests/hour)

**Solutions**:

1. **Wait 1 hour** and try again

2. **Increase delay** between requests:
   ```python
   time.sleep(1.0)  # Increase from 0.5 to 1.0 seconds
   ```

3. **Process in batches**:
   ```python
   # Delete only first 50 torrents
   for torrent in dead_torrents[:50]:
       delete_torrent(torrent["id"])
   ```

---

### Issue: Deleted Torrents Reappear

**Symptoms**: Run cleanup, but same torrents back next day

**Causes**:
1. Sonarr/Radarr re-adding torrents automatically
2. RSS feed auto-download
3. Jellyseerr requests

**Solutions**:

1. **Check Sonarr/Radarr**:
   - Settings → Indexers → Remove or disable problematic indexers
   - Series/Movies → Unmonitor content you don't want

2. **Check RSS feeds**:
   - Disable auto-download RSS feeds

3. **Blacklist in *arr apps**:
   - Add to release blacklist
   - Settings → Profiles → Release Profile → Must Not Contain

---

### Issue: Script Hangs During Cleanup

**Symptoms**: Script stuck at "Deleting torrents..."

**Causes**:
1. Network timeout
2. API not responding
3. Too many torrents

**Solutions**:

1. **Add timeout to requests**:
   ```python
   response = requests.delete(url, headers=HEADERS, timeout=10)
   ```

2. **Process in smaller batches**:
   ```python
   # Delete only 10 at a time
   for torrent in dead_torrents[:10]:
       ...
   ```

3. **Check Real-Debrid status**:
   - Visit https://real-debrid.com/
   - Check if site is down or slow

---

## Security Best Practices

### API Key Storage

**✅ Good**:
```bash
# Store in environment variable
export RD_API_KEY="key_here"

# Or in secrets file (gitignored)
echo "RD_API_KEY=key_here" >> ~/. secrets
source ~/.secrets
```

**❌ Bad**:
```python
# Hardcoded in script (gets committed to Git)
API_KEY = "HZLVDRPVBT7RPTNFQ6V2MEF2Z74UKJWCMJC"
```

### Permissions

```bash
# Make script readable only by automation user
chmod 700 /home/automation/scripts/cleanup_realdebrid.py

# Protect secrets file
chmod 600 ~/.secrets
```

---

## Related Documentation

- [SKILL.md](./SKILL.md) - Quick start guide
- [scripts/cleanup_realdebrid.py](./scripts/cleanup_realdebrid.py) - Full source code
- [Real-Debrid API docs](https://api.real-debrid.com/) - Official API reference
- [media-stack-refresh](../media-stack-refresh/SKILL.md) - Post-cleanup workflow
