# AIRAC Cycle Schedule

AIRAC (Aeronautical Information Regulation And Control) cycles for FAA data updates.

## Cycle Format

AIRAC cycle identifiers use format: `YYCC`
- YY = Two-digit year
- CC = Cycle number within year (01-13)

## 2025 AIRAC Schedule

| Cycle | Effective Date | Cron Expression | Data Available |
|-------|----------------|-----------------|----------------|
| 2501 | 2025-01-23 | `0 9 23 1 *` | 2025-01-09 |
| 2502 | 2025-02-20 | `0 9 20 2 *` | 2025-02-06 |
| 2503 | 2025-03-20 | `0 9 20 3 *` | 2025-03-06 |
| 2504 | 2025-04-17 | `0 9 17 4 *` | 2025-04-03 |
| 2505 | 2025-05-15 | `0 9 15 5 *` | 2025-05-01 |
| 2506 | 2025-06-12 | `0 9 12 6 *` | 2025-05-29 |
| 2507 | 2025-07-10 | `0 9 10 7 *` | 2025-06-26 |
| 2508 | 2025-08-07 | `0 9 7 8 *` | 2025-07-24 |
| 2509 | 2025-09-04 | `0 9 4 9 *` | 2025-08-21 |
| 2510 | 2025-10-02 | `0 9 2 10 *` | 2025-09-18 |
| 2511 | 2025-10-30 | `0 9 30 10 *` | 2025-10-16 |
| 2512 | 2025-11-27 | `0 9 27 11 *` | 2025-11-13 |
| 2513 | 2025-12-25 | `0 9 25 12 *` | 2025-12-11 |

## 2026 AIRAC Schedule

| Cycle | Effective Date | Cron Expression | Data Available |
|-------|----------------|-----------------|----------------|
| 2601 | 2026-01-22 | `0 9 22 1 *` | 2026-01-08 |
| 2602 | 2026-02-19 | `0 9 19 2 *` | 2026-02-05 |
| 2603 | 2026-03-19 | `0 9 19 3 *` | 2026-03-05 |
| 2604 | 2026-04-16 | `0 9 16 4 *` | 2026-04-02 |
| 2605 | 2026-05-14 | `0 9 14 5 *` | 2026-04-30 |
| 2606 | 2026-06-11 | `0 9 11 6 *` | 2026-05-28 |
| 2607 | 2026-07-09 | `0 9 9 7 *` | 2026-06-25 |
| 2608 | 2026-08-06 | `0 9 6 8 *` | 2026-07-23 |
| 2609 | 2026-09-03 | `0 9 3 9 *` | 2026-08-20 |
| 2610 | 2026-10-01 | `0 9 1 10 *` | 2026-09-17 |
| 2611 | 2026-10-29 | `0 9 29 10 *` | 2026-10-15 |
| 2612 | 2026-11-26 | `0 9 26 11 *` | 2026-11-12 |
| 2613 | 2026-12-24 | `0 9 24 12 *` | 2026-12-10 |

## Chart Update Cycles (56-Day)

VFR/IFR charts update every other AIRAC cycle:

**2025 Chart Cycles:**
- 2501 (Jan 23)
- 2503 (Mar 20)
- 2505 (May 15)
- 2507 (Jul 10)
- 2509 (Sep 4)
- 2511 (Oct 30)
- 2513 (Dec 25)

**2026 Chart Cycles:**
- 2601 (Jan 22)
- 2603 (Mar 19)
- 2605 (May 14)
- 2607 (Jul 9)
- 2609 (Sep 3)
- 2611 (Oct 29)
- 2613 (Dec 24)

## Data Update Frequencies

| Data Type | Update Cycle | Source |
|-----------|--------------|--------|
| NASR (Airports, NAVAIDs, etc.) | 28 days | nfdc.faa.gov |
| CIFP (Procedures) | 28 days | aeronav.faa.gov |
| d-TPP (Charts) | 28 days | aeronav.faa.gov |
| VFR Sectionals | 56 days | aeronav.faa.gov |
| IFR Enroute | 56 days | aeronav.faa.gov |
| DOF (Obstacles) | Daily | aeronav.faa.gov |
| TFRs | Real-time | tfr.faa.gov |
| METARs/TAFs | Hourly | aviationweather.gov |

## Calculating AIRAC Dates

```python
from datetime import datetime, timedelta

# AIRAC epoch (known cycle start)
AIRAC_EPOCH = datetime(2024, 1, 4)  # Cycle 2401
CYCLE_DAYS = 28

def get_current_cycle():
    """Get current AIRAC cycle info."""
    today = datetime.now()
    days_since_epoch = (today - AIRAC_EPOCH).days
    cycle_num = days_since_epoch // CYCLE_DAYS

    effective_date = AIRAC_EPOCH + timedelta(days=cycle_num * CYCLE_DAYS)

    year = effective_date.year
    year_start = datetime(year, 1, 1)
    days_into_year = (effective_date - year_start).days
    cycle_in_year = (days_into_year // CYCLE_DAYS) + 1

    cycle_id = f"{year % 100:02d}{cycle_in_year:02d}"

    return {
        'cycle_id': cycle_id,
        'effective_date': effective_date,
        'expires_date': effective_date + timedelta(days=CYCLE_DAYS)
    }

def get_next_cycle():
    """Get next AIRAC cycle info."""
    current = get_current_cycle()
    next_effective = current['expires_date']

    year = next_effective.year
    year_start = datetime(year, 1, 1)
    days_into_year = (next_effective - year_start).days
    cycle_in_year = (days_into_year // CYCLE_DAYS) + 1

    cycle_id = f"{year % 100:02d}{cycle_in_year:02d}"

    return {
        'cycle_id': cycle_id,
        'effective_date': next_effective,
        'data_available': next_effective - timedelta(days=14)
    }
```

## GitHub Actions Scheduling

For automated data pipelines, schedule workflows to run:
- **NASR/CIFP**: 14 days before effective date (when data becomes available)
- **DOF**: Daily at a consistent time
- **Charts**: 14 days before chart effective date

Example cron for NASR (runs 14 days before each effective date):
```yaml
on:
  schedule:
    # 2501: Jan 9, 2025
    - cron: '0 9 9 1 *'
    # 2502: Feb 6, 2025
    - cron: '0 9 6 2 *'
    # ... etc
```
