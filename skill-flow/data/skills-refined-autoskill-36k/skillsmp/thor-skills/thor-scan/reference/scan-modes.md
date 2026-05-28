# Scan Modes

THOR has six main scan modes. They can be combined where sensible.

## Default Mode

No special flags. Recommended for endpoint sweeps. Runtime: 1-6 hours typical.
- Auto-activates "Soft" mode on limited systems (single-core or <1024MB RAM)
- Balanced coverage and performance

## Quick Mode (`--quick`)

Fast scan: ~20% of default runtime for ~80% coverage.

Disables: Eventlog, Firewall, User Profiles, Hotfixes, MFT analysis.
Skips files not modified in last 3 days (except 40+ predefined directories).

Use for: rapid triage, time-constrained sweeps.

## Soft Mode (`--soft`)

Prioritizes system stability over thoroughness.

Disables: Mutexes, Firewall, Logons, Network sessions, LSA sessions, archive decompression.
Auto-activates on: single-core systems or <1024MB RAM.
Override with `--nosoft`.

Use for: fragile production systems, legacy hardware.

## Intense Mode (`--intense`)

Maximum coverage. Not recommended for production endpoints.

Enables:

- Every file scanned regardless of extension/magic header
- Max file size: 200MB (vs 30MB default)
- MFT analysis by default
- All safeguards disabled

Use for: lab analysis, forensic workstations.

**Note:** The `--lab` flag already includes `--intense`. Do NOT combine `--lab --intense` - it's redundant.

## Diff Mode (`--diff`)

Incremental scanning. Only scans elements changed since last scan.

Requires: completed previous scan with ThorDB enabled.
Susceptible to timestomping (attacker-modified timestamps).

Use for: follow-up scans after initial baseline.

## Lookback Mode (`--lookback <days>`)

Time-restricted scanning. Only scans elements created/modified within N days.

Applies to: FileScan, Registry, Services, Registry Hives, EVTX Scan.
Add `--global-lookback` to apply to all applicable modules.

Use for: quick recent-activity triage, SIEM verification.

## Mode Combinations

| Combination | Typical Use Case |
|-------------|------------------|
| `--soft --diff` | Follow-up on fragile systems |
| `--lab` | Forensic image analysis (already includes `--intense`) |
| `--quick --lookback 7` | Fast 7-day activity check |

**Invalid combinations:**

- `--lab --intense` – Redundant, `--lab` already enables intense mode
- `--quick --intense` – Conflicting goals
