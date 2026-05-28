# API Endpoints Reference

## Find a Tender Service (FTS) — OCDS API

FTS is the UK's national service for procurement notices. From 24 Feb 2025, it publishes above and below threshold notices for new UK procurements (except below-threshold in Scotland).

### OCDS Release Packages (Incremental Feed)

Primary endpoint for event-stream ingestion of notice changes.

```
GET https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages
```

**Query Parameters:**
| Parameter | Values | Description |
|-----------|--------|-------------|
| stages | planning,tender,award,contract | Filter by procurement stage |
| updatedFrom | ISO 8601 datetime | Notices updated after this time |
| updatedTo | ISO 8601 datetime | Notices updated before this time |
| limit | 1-100 | Results per page |
| cursor | string | Pagination cursor from previous response |

**Rate Limiting:** Returns `429 Too Many Requests` with `Retry-After` header (seconds).

**Example Request:**
```bash
curl "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?stages=tender,award&updatedFrom=2025-12-01T00:00:00Z&limit=100"
```

### OCDS Record Packages (Full Lifecycle)

Fetch complete procurement history for a specific OCID.

```
GET https://www.find-tender.service.gov.uk/api/1.0/ocdsRecordPackages/{ocid}
```

**OCID Format:** `ocds-h6vhtk-hhhhhh` (zero-padded hex)

**Response Structure:**
- `releases[]` — Each notice/release in the procurement
- `compiledRelease` — Latest combined view
- `versionedRelease` — Field-level change history

**Rate Limiting:** `429` and `503` both use `Retry-After` header.

### OCDS Data Paths

| Data Type | Path |
|-----------|------|
| Tender details | `tender` |
| Awards | `awards[]` |
| Contracts | `contracts[]` |
| Contract period | `contracts[].period.startDate` / `endDate` |
| Contract value | `contracts[].value` |
| Buyer name | `releases.buyer.name` |
| Buyer ID | `releases.buyer.identifier.id` |

### Notice Types (Procurement Act 2023)

| Code | Type | Use |
|------|------|-----|
| UK1 | Pipeline Notice | Contracts >£2m, 18-month horizon |
| UK2 | Preliminary Market Engagement | Pre-tender engagement |
| UK3 | Planned Procurement Notice | Optional pre-tender |
| UK4 | Tender Notice | Live opportunity |
| UK6 | Contract Award Notice | Award notification |
| UK12 | Procurement Termination Notice | Cancelled procurement |

---

## Contracts Finder API

Statutory repository for central government contracts >£12k and sub-central (police) contracts >£25k.

### Search API (POST)

Keyword and filter-based search for notices.

```
POST https://www.contractsfinder.service.gov.uk/Searches/Search
Content-Type: application/json
```

**Request Body:**
```json
{
  "searchCriteria": {
    "types": ["Contract", "Pipeline"],
    "statuses": ["Open", "Awarded", "Closed"],
    "keyword": "investigation OR investigator",
    "regions": "London,South East",
    "postcode": "SW1A 1AA",
    "radius": 50,
    "valueFrom": 25000,
    "valueTo": 500000,
    "publishedFrom": "2025-01-01T00:00:00",
    "publishedTo": "2025-12-31T23:59:59",
    "deadlineFrom": "2025-01-01T00:00:00",
    "deadlineTo": "2025-03-31T23:59:59",
    "awardedFrom": "2025-01-01T00:00:00",
    "awardedTo": "2025-12-31T23:59:59",
    "cpvCodes": ["79720000", "79620000"],
    "suitableForSme": true,
    "suitableForVco": false
  },
  "size": 100
}
```

**Response Fields:**
- `organisationName` — Buyer name
- `awardedSupplier` — Winner name
- `awardedValue` — Contract value
- `awardedDate` — Award date
- `publishedDate` — Notice publication date
- `deadlineDate` — Submission deadline
- `cpvCodes` — CPV classification codes

**Rate Limiting:** `403` response means wait 5 minutes.

### OCDS Feed (Backfill)

Uniform OCDS format for legacy data.

```
GET https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| publishedFrom | ISO 8601 start date |
| publishedTo | ISO 8601 end date |
| stages | planning,tender,award,implementation |
| limit | 1-100 |
| cursor | Pagination cursor |

**Rate Limiting:** `403` means wait 5 minutes.

### Get Full Notice

```
GET https://www.contractsfinder.service.gov.uk/api/rest/2/get_published_notice/{MimeType}/{id}
```

- `MimeType` = json or xml
- `id` = Notice GUID

Returns `FullNotice` object with buyer contact details and document attachments.

### Get Draft Awards

```
GET https://www.contractsfinder.service.gov.uk/api/rest/2/get_draft_awards/{MimeType}/{id}
```

Returns collection of `AwardDetail` objects with:
- `SupplierName` — Winner
- `Value` — Contract value in GBP
- `StartDate` / `EndDate` — Contract period

---

## Authentication (Contracts Finder v2)

Contracts Finder v2 API requires Sid4Gov OAuth-style authentication:

1. **Token Request:**
```
POST /token
Authorization: Basic {base64(username:password)}
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

2. **Token Response:**
```json
{
  "access_token": "2YotnFZFEjr1zCsicMWpAA",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

3. **Authenticated Requests:**
```
Authorization: Bearer {access_token}
Accept: application/json
```

---

## Deduplication Strategy

High-value notices appear on both FTS and Contracts Finder.

**OCID as Golden Thread:** Format `ocds-h6vhtk-{identifier}` links notices across platforms.

**Resolution Order:**
1. Ingest from FTS first (master source for >£214k)
2. Ingest from Contracts Finder
3. If CF notice has OCID already in FTS dataset, merge records
4. FTS = authoritative regulatory data; CF = often richer domestic details

---

## Ingestion Architecture

```python
# Primary stream (FTS)
def poll_fts():
    releases = fts_api.get_releases(updated_from=watermark, cursor=cursor)
    store_raw_packages(releases)  # Immutable storage
    
    for release in releases:
        if release.stage in ['award', 'contract'] or is_high_signal(release.notice_type):
            full_record = fts_api.get_record(release.ocid)
            build_lifecycle_view(full_record)
    
    # Respect rate limits
    if response.status == 429:
        time.sleep(int(response.headers['Retry-After']))

# Secondary stream (Contracts Finder)
def poll_cf():
    # Keyword/CPV alerting
    results = cf_api.search(keyword="investigation", cpv_codes=["79720000"])
    
    # OCDS backfill for uniformity
    ocds_data = cf_api.get_ocds_notices(published_from=watermark)
    
    if response.status == 403:
        time.sleep(300)  # 5 minutes
```
