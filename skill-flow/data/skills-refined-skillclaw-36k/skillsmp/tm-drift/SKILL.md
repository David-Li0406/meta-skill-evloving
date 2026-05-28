---
name: tm-drift
description: Detect changes in the threat model since the last baseline snapshot. Identifies new assets, changed flows, new threats, and control status changes. Use when comparing threat model versions, tracking security drift, monitoring for new risks, or validating changes after updates.
allowed-tools: Read, Write, Glob
---

# Drift Detection

## Purpose

Compare current threat model state against a baseline to:

- Identify new or removed assets
- Detect changed data flows
- Find new attack surface entries
- Track control status changes
- Highlight new potential threats

## Usage

```
/tm-drift [--baseline <path>] [--create-baseline] [--watch]
```

**Arguments**:
- `--baseline`: Specific baseline file to compare against
- `--create-baseline`: Create new baseline after comparison
- `--watch`: Continuous monitoring mode (future feature)

## Drift Categories

### Asset Changes
- **Added**: New components discovered
- **Removed**: Components no longer present
- **Modified**: Properties changed (classification, owner, etc.)

### Data Flow Changes
- **Added**: New data flows between components
- **Removed**: Flows no longer present
- **Modified**: Protocol, encryption, or authentication changed

### Attack Surface Changes
- **Added**: New entry points exposed
- **Removed**: Entry points removed
- **Modified**: Authentication or configuration changed

### Trust Boundary Changes
- **Added**: New boundaries defined
- **Removed**: Boundaries removed
- **Modified**: Controls or scope changed

### Control Status Changes
- **Implemented → Partial**: Control degraded
- **Implemented → Missing**: Control removed
- **Missing → Implemented**: Control added
- **Verification status changed**

## Baseline Structure

Baselines are snapshots of the complete threat model state:

```json
{
  "version": "1.0",
  "created": "ISO-8601",
  "project": "Project Name",
  "snapshot": {
    "assets": [...],
    "dataflows": [...],
    "trust_boundaries": [...],
    "attack_surface": [...],
    "threats": [...],
    "controls": [...],
    "gaps": [...]
  },
  "metadata": {
    "commit": "git-commit-hash",
    "author": "name",
    "reason": "baseline reason"
  }
}
```

## Drift Report Format

### drift-report.md
```markdown
# Threat Model Drift Report

**Baseline**: 2025-01-15 (snapshot-20250115.json)
**Current**: 2025-01-20
**Period**: 5 days

---

## Summary

| Category | Added | Removed | Modified |
|----------|-------|---------|----------|
| Assets | 2 | 0 | 1 |
| Data Flows | 3 | 1 | 0 |
| Attack Surface | 2 | 0 | 1 |
| Trust Boundaries | 0 | 0 | 0 |
| Controls | 1 | 0 | 2 |

**Risk Impact**: New assets and attack surfaces require threat analysis.

---

## Asset Changes

### Added Assets

#### asset-015: Redis Cache
- **Type**: data-store
- **Classification**: internal
- **Added in**: commit abc123
- **Risk**: Cache poisoning, data exposure

#### asset-016: Email Service Integration
- **Type**: integration
- **Classification**: confidential
- **Added in**: commit def456
- **Risk**: Email injection, SSRF

### Modified Assets

#### asset-005: User Database
- **Change**: Classification upgraded from internal to restricted
- **Reason**: Now stores payment data
- **Impact**: Additional controls required

---

## Attack Surface Changes

### Added Entry Points

#### as-010: Cache Invalidation API
- **Asset**: asset-015
- **Exposure**: internal
- **Authentication**: none ⚠️
- **Risk**: Unauthenticated cache manipulation

#### as-011: Email Webhook Receiver
- **Asset**: asset-016
- **Exposure**: public
- **Authentication**: signature validation
- **Risk**: Webhook forgery

### Modified Entry Points

#### as-003: Admin API
- **Change**: New endpoints added
- **Endpoints**: /api/admin/cache, /api/admin/email
- **Risk**: Expanded attack surface

---

## Control Status Changes

### Degraded Controls

#### control-005: Input Validation
- **Previous**: implemented
- **Current**: partial
- **Reason**: New endpoints missing validation
- **Files Changed**: src/routes/admin.ts

### Improved Controls

#### control-012: Rate Limiting
- **Previous**: missing
- **Current**: implemented
- **Evidence**: src/middleware/rateLimiter.ts

---

## New Potential Threats

Based on changes, the following new threats should be analyzed:

1. **Cache Poisoning** (asset-015)
   - Unauthenticated cache invalidation
   - Data corruption via cache

2. **Email Header Injection** (asset-016)
   - Malicious email content
   - SSRF via email service

3. **Admin API Abuse** (as-003)
   - New endpoints may lack authorization

---

## Recommendations

1. **Immediate**: Add authentication to cache invalidation endpoint
2. **Immediate**: Run /tm-threats --focus asset-015,asset-016
3. **Short-term**: Review admin API authorization
4. **Short-term**: Update threat model with new components

---

## Baseline Created

New baseline: `.threatmodel/baseline/snapshot-20250120.json`
```

## Instructions for Claude

When executing this skill:

1. **Load current state**:
   - Read all files from `.threatmodel/state/`

2. **Load baseline**:
   - If `--baseline` specified, use that file
   - Otherwise, find most recent in `.threatmodel/baseline/`
   - If no baseline exists, report and offer to create one

3. **Compare each category**:
   - Assets: Compare by ID, check all properties
   - Data Flows: Compare by ID, check configuration
   - Attack Surface: Compare by ID, check endpoints
   - Trust Boundaries: Compare by ID, check scope
   - Controls: Compare by ID, check status

4. **Identify changes**:
   - New items (in current, not in baseline)
   - Removed items (in baseline, not in current)
   - Modified items (in both, but different)

5. **Assess risk impact**:
   - New assets may introduce threats
   - New attack surface expands exposure
   - Degraded controls increase risk
   - Removed flows may indicate architectural change

6. **Generate recommendations**:
   - Run threat analysis on new components
   - Review authorization on modified surfaces
   - Investigate degraded controls

7. **Create baseline if requested**:
   - Snapshot current state
   - Include metadata (timestamp, commit, author)
   - Save to baseline directory

8. **Report summary**:
   ```
   Drift Detection Complete
   ========================

   Compared against: baseline/snapshot-20250115.json (5 days ago)

   Changes Detected:
     + 2 new assets
     + 3 new data flows
     + 2 new attack surface entries
     ~ 2 controls changed status

   Risk Impact: MEDIUM
     - New unauthenticated endpoint detected
     - Control degradation in admin routes

   New Potential Threats: 3
     - Cache poisoning
     - Email header injection
     - Admin API abuse

   Recommendations:
     1. Run /tm-threats --focus asset-015,asset-016
     2. Review authentication on as-010
     3. Update input validation for admin routes

   Files Created:
     .threatmodel/reports/drift-report.md
     .threatmodel/baseline/snapshot-20250120.json (new baseline)

   Next Steps:
     Address identified changes
     Re-run /tm-verify after fixes
   ```
