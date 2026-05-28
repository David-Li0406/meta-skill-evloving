# DELTA_CONTEXT | <PROJECT_NAME> | <TIMESTAMP>

## Baseline

**Prior:** `<OLD_COMMIT_HASH>` (<OLD_TIMESTAMP>)
**Current:** `<NEW_COMMIT_HASH>` (<NEW_TIMESTAMP>)
**Commits:** <COUNT> commits since baseline

## Changes Since Baseline

### Files Modified
- `path/file.ts` - [brief description of change]
- `path/other.ts` - [brief description of change]

### Files Added
- `path/new-file.ts` - NEW: [purpose]

### Files Deleted
- `path/old-file.ts` - REMOVED: [reason]

## Implications

What these changes mean for agents:

- [Implication 1 - e.g., "New endpoint requires updating tests"]
- [Implication 2 - e.g., "Config change affects local dev setup"]

## New Decisions

Decisions made since last compile:

- **[Topic]:** [Decision] (Rationale: [why])

## Risks / Blockers

Known issues or risks:

- [Risk/Blocker] → [Workaround if known]
- [none] if no blockers

## Agent Actions

What agents should do based on these changes:

1. [Action 1 - e.g., "When working on API, note new auth middleware"]
2. [Action 2 - e.g., "Run migrations before testing data layer"]
3. [Action 3 - e.g., "Check config.json for new required fields"]

## Feature Impact

Features affected by these changes:

| Feature | Impact | Action |
|---------|--------|--------|
| api | Modified | Reload bundle |
| ui | None | - |
| data | New files | Reload bundle |

---
*Updated: <TIMESTAMP> | Baseline: <OLD_COMMIT> → <NEW_COMMIT>*
