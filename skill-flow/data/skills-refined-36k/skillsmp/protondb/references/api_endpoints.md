# API Endpoints

Complete documentation of ProtonDB and Steam API endpoints for game compatibility analysis.

## ProtonDB APIs

### 1. Game Summary API

Get overall compatibility rating and statistics for a game.

**Endpoint:**
```
https://www.protondb.com/api/v1/reports/summaries/<APP_ID>.json
```

**Method:** GET

**Parameters:**
- `APP_ID` - Steam Application ID (integer)

**Example:**
```bash
curl -s 'https://www.protondb.com/api/v1/reports/summaries/1285190.json' | jq .
```

**Response Structure:**
```json
{
  "bestReportedTier": "platinum",
  "confidence": "strong",
  "score": 0.95,
  "tier": "platinum",
  "total": 243,
  "trendingTier": "platinum"
}
```

**Fields:**
- `bestReportedTier` - Highest compatibility tier reported
- `confidence` - Confidence level (strong/moderate/weak)
- `score` - Numeric compatibility score (0-1)
- `tier` - Overall recommended tier
- `total` - Total number of reports
- `trendingTier` - Recent trend in ratings

**Tier Values:**
- `native` - Official Linux support
- `platinum` - Works perfectly out-of-box
- `gold` - Works with minor tweaks
- `silver` - Runs with workarounds
- `bronze` - Runs poorly, significant issues
- `borked` - Does not run

**Confidence Levels:**
- `strong` - 50+ reports, reliable data
- `moderate` - 10-49 reports, fairly reliable
- `weak` - <10 reports, experimental

### 2. Community Reports API (Third-Party)

Get detailed user reports from the community.

**Endpoint:**
```
https://protondb-community-api.fly.dev/reports?appId=<APP_ID>&limit=<COUNT>
```

**Method:** GET

**Parameters:**
- `appId` - Steam Application ID
- `limit` - Number of reports to return (default: 10, max: 100)

**Example:**
```bash
curl -s 'https://protondb-community-api.fly.dev/reports?appId=1285190&limit=50'
```

**Note:** This is a third-party API and may be unavailable. Always have fallback data sources.

**Response Structure:**
```json
{
  "reports": [
    {
      "tier": "platinum",
      "protonVersion": "Proton 9.0-1",
      "gpu": "AMD Radeon RX 7900 XTX",
      "os": "Arch Linux",
      "kernel": "6.6.x",
      "notes": "Works perfectly with...",
      "specs": {
        "cpu": "AMD Ryzen 9 7950X",
        "ram": "32GB",
        "gpu": "RX 7900 XTX"
      }
    }
  ]
}
```

## Steam APIs

### 1. App Details API (via ProtonDB Proxy)

Get comprehensive game information from Steam.

**Endpoint:**
```
https://www.protondb.com/proxy/steam/api/appdetails/?appids=<APP_ID>
```

**Method:** GET

**Parameters:**
- `appids` - Steam Application ID (can provide multiple comma-separated)

**Example:**
```bash
curl -s 'https://www.protondb.com/proxy/steam/api/appdetails/?appids=1285190' | jq .
```

**Response Structure:**
```json
{
  "1285190": {
    "success": true,
    "data": {
      "name": "Game Name",
      "type": "game",
      "is_free": false,
      "detailed_description": "...",
      "short_description": "...",
      "platforms": {
        "windows": true,
        "mac": false,
        "linux": false
      },
      "categories": [...],
      "genres": [...],
      "pc_requirements": {
        "minimum": "...",
        "recommended": "..."
      }
    }
  }
}
```

**Key Fields:**
- `name` - Game title
- `platforms` - Supported platforms
- `pc_requirements` - System requirements (HTML formatted)
- `categories` - Game categories (single-player, multiplayer, etc.)
- `genres` - Game genres

### 2. Direct Steam Store API

Alternative endpoint for Steam data (use ProtonDB proxy when possible).

**Endpoint:**
```
https://store.steampowered.com/api/appdetails/?appids=<APP_ID>
```

**Method:** GET

**Note:** Rate-limited, prefer ProtonDB proxy for caching.

## Alternative Data Sources

### GitHub Proton Issues

Search for game-specific issues and solutions.

**URL Pattern:**
```
https://github.com/ValveSoftware/Proton/issues?q=<GAME_NAME>
```

**Example:**
```
https://github.com/ValveSoftware/Proton/issues?q=Elden+Ring
```

**Usage:**
- Check for open issues with game
- Review closed issues for historical problems
- Look for Proton version mentions in comments
- Check labels: `linux-testing`, `wine-staging`, `dxvk`

### ProtonDB Website

Main ProtonDB website (browser-based).

**URL Pattern:**
```
https://www.protondb.com/app/<APP_ID>
```

**Example:**
```
https://www.protondb.com/app/1285190
```

**Features:**
- User reports with detailed configurations
- Filtering by Proton version, GPU, distro
- Comments and discussions
- Configuration recommendations

**Note:** Requires browser, cannot be accessed programmatically for detailed reports.

## Steam App ID Lookup

### Finding Steam App ID

**Method 1: Steam Store URL**
```
https://store.steampowered.com/app/1285190/Borderlands_4/
                                    ^^^^^^^
                                    App ID
```

**Method 2: SteamDB**
```
https://steamdb.info/search/?a=app&q=<GAME_NAME>
```

**Method 3: Steam Community**
Right-click game in library → View Community Hub → Check URL

**Method 4: steamid.io**
```
https://steamid.io/lookup/<GAME_NAME>
```

## Rate Limiting and Best Practices

### ProtonDB API
- **Rate Limit:** Not publicly documented, be respectful
- **Caching:** Results cached on ProtonDB side
- **Retry:** Implement exponential backoff on failures

### Steam API
- **Rate Limit:** ~200 requests per 5 minutes per IP
- **Proxy Usage:** Use ProtonDB proxy when available
- **Caching:** Cache responses locally to reduce calls

### Best Practices

1. **Cache locally:** Store API responses to avoid repeat calls
2. **Batch requests:** Use comma-separated app IDs when possible
3. **Error handling:** Check for HTTP errors and empty responses
4. **Fallback sources:** Have multiple data sources ready
5. **Respect limits:** Implement rate limiting in scripts

## API Response Parsing

### Extracting ProtonDB Tier

```bash
TIER=$(curl -s "https://www.protondb.com/api/v1/reports/summaries/$APP_ID.json" | jq -r '.tier')
echo "Compatibility: $TIER"
```

### Extracting Steam Requirements

```bash
REQUIREMENTS=$(curl -s "https://www.protondb.com/proxy/steam/api/appdetails/?appids=$APP_ID" | \
  jq -r ".[\"$APP_ID\"].data.pc_requirements.minimum")
echo "$REQUIREMENTS"
```

### Checking Native Linux Support

```bash
LINUX_SUPPORT=$(curl -s "https://www.protondb.com/proxy/steam/api/appdetails/?appids=$APP_ID" | \
  jq -r ".[\"$APP_ID\"].data.platforms.linux")

if [ "$LINUX_SUPPORT" = "true" ]; then
  echo "Native Linux support available"
else
  echo "Requires Proton"
fi
```

## Error Handling

### Common Errors

**404 Not Found:**
- App ID doesn't exist
- Game not in ProtonDB database yet
- Typo in App ID

**Empty Response:**
- API temporarily unavailable
- Network connectivity issues
- Rate limit exceeded

**Invalid JSON:**
- Partial response received
- API endpoint changed structure
- Proxy issue

### Error Handling Example

```bash
RESPONSE=$(curl -s -w "%{http_code}" "https://www.protondb.com/api/v1/reports/summaries/$APP_ID.json")
HTTP_CODE="${RESPONSE: -3}"
JSON_DATA="${RESPONSE:0:${#RESPONSE}-3}"

if [ "$HTTP_CODE" = "200" ]; then
  echo "$JSON_DATA" | jq .
elif [ "$HTTP_CODE" = "404" ]; then
  echo "Error: Game not found in ProtonDB"
else
  echo "Error: HTTP $HTTP_CODE"
fi
```

## API Updates and Monitoring

### Checking API Status

Monitor API availability:
```bash
curl -s -o /dev/null -w "%{http_code}" "https://www.protondb.com/api/v1/reports/summaries/1.json"
```

Should return `200` if API is operational.

### API Change Detection

ProtonDB API structure may change over time. Check:
- ProtonDB GitHub: https://github.com/bdefore/protondb
- Community discussions: Reddit /r/ProtonDB
- API response schema changes

### Version Compatibility

Current API version (as of documentation):
- ProtonDB API: v1
- Steam API: Stable (no version number)
- Community API: Unofficial (may change without notice)
