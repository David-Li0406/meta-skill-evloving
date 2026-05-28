---
name: uk-public-sector-procurement
description: Build procurement monitoring workflows for UK police forces using government APIs
model: haiku
---

# UK Public Sector Procurement for Police Forces

Build procurement monitoring workflows for UK police forces using government APIs and market intelligence signals.

## Platform Priority (Post-Feb 2025)

**Primary: Find a Tender Service (FTS)** — system of record for all UK procurements (above and below threshold, except Scotland below-threshold). Use the OCDS API for automated ingestion.

**Secondary: Contracts Finder** — legacy procurements started before 24 Feb 2025, plus useful for keyword-based searching and backfill.

## Quick Start: Ingestion Pattern

```python
# Poll FTS OCDS feed (primary stream)
fts_url = "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages"
params = {
    "stages": "planning,tender,award",
    "updatedFrom": last_poll_timestamp,  # ISO 8601
    "limit": 100
}
# Handle 429 (Retry-After header) and cursor pagination

# For full procurement lifecycle
record_url = f"https://www.find-tender.service.gov.uk/api/1.0/ocdsRecordPackages/{ocid}"
```

```python
# Contracts Finder keyword search (secondary)
cf_url = "https://www.contractsfinder.service.gov.uk/Searches/Search"
body = {
    "searchCriteria": {
        "types": ["Contract"],
        "statuses": ["Open"],
        "keyword": "investigation OR investigator OR disclosure",
        "cpvCodes": ["79720000", "79620000"]
    },
    "size": 100
}
# Handle 403 rate limit (wait 5 minutes)
```

## Police Buyer Detection

Filter by `buyer.name` containing:
- `Police`, `Constabulary`, `PCC`, `OPCC`, `Commissioner`
- `BlueLight`, `MOPAC`, `NCA`, `British Transport Police`

Build a canonical buyer table mapping variants:
- "Police and Crime Commissioner for Sussex" → `FORCE_SUSSEX`
- "Chief Constable of Sussex" → `FORCE_SUSSEX`

## Early Warning Signals

| Notice Type | Signal Strength | Meaning |
|-------------|-----------------|---------|
| UK1 Pipeline | Very High | Planned contracts >£2m, 18-month horizon |
| UK2 PME | High | Active market engagement, tender imminent |
| UK3 Planned | Medium-High | Optional pre-tender signal |
| UK4 Tender | High (urgent) | Live opportunity |
| UK6 Award | Intel only | Competitor/renewal tracking |

## Alert Tiers for Sales Teams

**Tier 1 (Sales-ready):** UK4 tender notices; open CF opportunities; approaching deadlines  
**Tier 2 (Pre-sales):** UK2 PME notices; UK3 planned; market engagement events  
**Tier 3 (Strategic):** UK1 pipeline (>£2m); budget settlement updates; HMICFRS findings

## Reference Files

- **[references/api-endpoints.md](references/api-endpoints.md)** — Full API documentation for FTS and Contracts Finder
- **[references/frameworks.md](references/frameworks.md)** — BlueLight Commercial, CCS frameworks, regional hubs
- **[references/timing-windows.md](references/timing-windows.md)** — Budget cycles, Q4 sprint, election impacts
- **[references/cpv-keywords.md](references/cpv-keywords.md)** — CPV codes and keyword taxonomies for investigation services
- **[references/thresholds.md](references/thresholds.md)** — Procurement thresholds and Procurement Act 2023 rules

## Data Model (Core Tables)

```
procurement_process (ocid)
├── notice_release (release_id, stage, notice_type, published_date, buyer_id)
├── award (award_id, supplier_id, value)
└── contract (contract_id, supplier_id, start_date, end_date, value)

buyer_entity (canonical_name, variants[], region, type)
supplier (canonical_name, identifiers[])
```

**Derived signals:**
- `incumbent_supplier(force, category)` from latest active contract
- `reprocurement_window_start` = end_date - 270 days
- `competitor_share_of_awards` by force and service category

## Renewal Forecasting Defaults

| Contract Type | Initial Term | Extensions | Alert Before End |
|---------------|--------------|------------|------------------|
| Managed service | 24-36 months | 1+1 years | 9-12 months |
| Framework call-off | Varies | Within framework | 6-9 months |
| Framework agreement | Up to 4 years | Rare | 12-18 months |
