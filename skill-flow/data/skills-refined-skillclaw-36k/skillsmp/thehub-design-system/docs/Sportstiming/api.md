# SCF License Portal API Integration

## Overview

TheHUB integrates with Svenska Cykelförbundet's (SCF) License Portal API to verify and synchronize rider license information.

## API Information

- **Base URL**: `https://licens.scf.se/api/1.0`
- **Authentication**: Bearer token in HTTP header
- **Format**: JSON responses
- **Rate Limit**: 25 UCI IDs per batch, 600ms between requests

## Endpoints

### UCI ID Lookup (Batch)

Look up licenses by UCI ID. Supports batch queries of up to 25 IDs.

```
GET /ucilicenselookup?year=2026&uciids=ID1,ID2,...
```

**Parameters:**
- `year` (required): License year (e.g., 2026)
- `uciids` (required): Comma-separated list of UCI IDs (max 25)

**Response:**
```json
{
  "licenses": [
    {
      "uci_id": "10108943209",
      "firstname": "Erik",
      "lastname": "Svensson",
      "gender": "M",
      "birthdate": "1990-05-15",
      "nationality": "SWE",
      "club_name": "Stockholm CK",
      "license_type": "Elite",
      "uci_road": true,
      "uci_mtb": true,
      "uci_cross": false,
      "uci_track": false,
      "uci_bmx": false,
      "uci_ecycling": false,
      "uci_gravel": true,
      "valid_until": "2026-12-31"
    }
  ]
}
```

### Name Lookup

Look up licenses by name. Use for finding potential matches for riders without UCI ID.

```
GET /licenselookup?year=2026&firstname=Erik&lastname=Svensson&gender=M&birthdate=1990-01-15
```

**Parameters:**
- `year` (required): License year
- `firstname` (required): First name
- `lastname` (required): Last name
- `gender` (required): M or F
- `birthdate` (optional): YYYY-MM-DD format for exact matching

**Response:**
Same format as UCI ID lookup, may return multiple matches for ambiguous queries.

## Disciplines

Available discipline flags in the API response:

| Field | Description |
|-------|-------------|
| `uci_road` | Road cycling |
| `uci_mtb` | Mountain bike |
| `uci_cross` | Cyclocross |
| `uci_track` | Track cycling |
| `uci_bmx` | BMX |
| `uci_ecycling` | E-cycling |
| `uci_gravel` | Gravel |

## TheHUB Integration

### Configuration

Add to `.env`:
```
SCF_API_KEY=your_api_key_here
```

### Database Tables

The integration creates the following tables:

- `scf_license_cache` - Cached license data from SCF
- `scf_license_history` - License history per rider
- `scf_sync_log` - Sync operation logs
- `scf_match_candidates` - Potential matches for review

Additional columns in `riders` table:
- `scf_license_verified_at` - When last verified
- `scf_license_year` - Year of verified license
- `scf_license_type` - License type from SCF
- `scf_disciplines` - JSON array of active disciplines
- `scf_club_name` - Club name from SCF

### Files

```
includes/
  SCFLicenseService.php    # API client class

admin/
  scf-sync-status.php      # Sync dashboard
  scf-match-review.php     # Match review interface

cron/
  sync_scf_licenses.php    # Batch sync script
  find_scf_matches.php     # Match finder script

Tools/migrations/
  019_scf_license_sync.sql # Database migration
```

### Cron Jobs

```bash
# Daily license verification at 03:00
0 3 * * * cd /path/to/TheHUB/cron && php sync_scf_licenses.php --year=2026 >> /var/log/scf-sync.log 2>&1

# Weekly match search on Sunday at 04:00
0 4 * * 0 cd /path/to/TheHUB/cron && php find_scf_matches.php --limit=500 >> /var/log/scf-match.log 2>&1
```

### Admin Interface

Access via: **System > SCF Licens**

Features:
- Sync status dashboard
- License verification progress
- Recent sync operations
- Match review interface
- Bulk confirm/reject matches

## Usage Examples

### Manual Sync

```bash
# Sync all unverified riders for 2026
php cron/sync_scf_licenses.php --year=2026 --debug

# Sync with history
php cron/sync_scf_licenses.php --year=2026 --history-years=2025,2024

# Dry run (no database changes)
php cron/sync_scf_licenses.php --year=2026 --dry-run
```

### Find Matches

```bash
# Find matches for riders without UCI ID
php cron/find_scf_matches.php --min-score=75 --debug

# Auto-confirm high-confidence matches
php cron/find_scf_matches.php --auto-confirm=95
```

## Match Scoring

The system calculates a confidence score (0-100) for potential matches:

| Factor | Points |
|--------|--------|
| First name match | 20 |
| Last name match | 20 |
| Gender match | 15 |
| Birth year exact | 25 |
| Birth year ±1 | 15 |
| Nationality match | 10 |
| Club similarity | 10 |

**Thresholds:**
- 90%+ = High confidence (green)
- 75-89% = Medium confidence (yellow)
- <75% = Low confidence (red)

## Error Handling

All API operations use try/catch with logging to `scf_sync_log`.

Rate limiting is enforced with 600ms delays between requests to avoid API throttling.

Network errors trigger retries with exponential backoff (2s, 4s, 8s, 16s).

## Security

- API key stored in environment variable (not committed to git)
- Admin authentication required for all SCF pages
- CSRF protection on all forms
- Audit trail in sync logs
