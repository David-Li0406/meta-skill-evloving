# Architecture Comparison Report

> Comparing **{{PREVIOUS_DATE}}** → **{{CURRENT_DATE}}**

---

## Summary

{{COMPARISON_SUMMARY}}

---

## Metrics Comparison

| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Total Files | {{PREV_FILES}} | {{CURR_FILES}} | {{FILES_CHANGE}} |
| Lines of Code | {{PREV_LOC}} | {{CURR_LOC}} | {{LOC_CHANGE}} |
| Components | {{PREV_COMPONENTS}} | {{CURR_COMPONENTS}} | {{COMPONENTS_CHANGE}} |
| API Routes | {{PREV_ROUTES}} | {{CURR_ROUTES}} | {{ROUTES_CHANGE}} |
| External Dependencies | {{PREV_DEPS}} | {{CURR_DEPS}} | {{DEPS_CHANGE}} |
| Circular Dependencies | {{PREV_CIRCULAR}} | {{CURR_CIRCULAR}} | {{CIRCULAR_CHANGE}} |
| Orphaned Files | {{PREV_ORPHANED}} | {{CURR_ORPHANED}} | {{ORPHANED_CHANGE}} |
| TODO Comments | {{PREV_TODOS}} | {{CURR_TODOS}} | {{TODOS_CHANGE}} |

---

## Structural Changes

### New Directories

{{#if NEW_DIRECTORIES}}
{{NEW_DIRECTORIES_LIST}}
{{else}}
No new directories.
{{/if}}

### Removed Directories

{{#if REMOVED_DIRECTORIES}}
{{REMOVED_DIRECTORIES_LIST}}
{{else}}
No directories removed.
{{/if}}

### Significant File Changes

#### Added Files ({{ADDED_FILES_COUNT}})

{{#if ADDED_FILES}}
{{ADDED_FILES_LIST}}
{{else}}
No files added.
{{/if}}

#### Removed Files ({{REMOVED_FILES_COUNT}})

{{#if REMOVED_FILES}}
{{REMOVED_FILES_LIST}}
{{else}}
No files removed.
{{/if}}

---

## Dependency Changes

### Added Dependencies

{{#if ADDED_DEPS}}
| Package | Category |
|---------|----------|
{{ADDED_DEPS_TABLE}}
{{else}}
No new dependencies.
{{/if}}

### Removed Dependencies

{{#if REMOVED_DEPS}}
| Package | Category |
|---------|----------|
{{REMOVED_DEPS_TABLE}}
{{else}}
No dependencies removed.
{{/if}}

### Internal Dependency Changes

{{INTERNAL_DEP_CHANGES}}

---

## API Surface Changes

### New Routes

{{#if NEW_ROUTES}}
| Method | Path | Handler |
|--------|------|---------|
{{NEW_ROUTES_TABLE}}
{{else}}
No new routes.
{{/if}}

### Removed Routes

{{#if REMOVED_ROUTES}}
| Method | Path | Handler |
|--------|------|---------|
{{REMOVED_ROUTES_TABLE}}
{{else}}
No routes removed.
{{/if}}

### Modified Routes

{{#if MODIFIED_ROUTES}}
{{MODIFIED_ROUTES_LIST}}
{{else}}
No routes modified.
{{/if}}

---

## Component Changes

### New Components

{{#if NEW_COMPONENTS}}
| Component | File |
|-----------|------|
{{NEW_COMPONENTS_TABLE}}
{{else}}
No new components.
{{/if}}

### Removed Components

{{#if REMOVED_COMPONENTS}}
| Component | File |
|-----------|------|
{{REMOVED_COMPONENTS_TABLE}}
{{else}}
No components removed.
{{/if}}

---

## Anomaly Changes

### Resolved Issues

{{#if RESOLVED_ANOMALIES}}
{{RESOLVED_ANOMALIES_LIST}}
{{else}}
No issues resolved since last review.
{{/if}}

### New Issues

{{#if NEW_ANOMALIES}}
{{NEW_ANOMALIES_LIST}}
{{else}}
No new issues detected.
{{/if}}

### Persistent Issues

{{#if PERSISTENT_ANOMALIES}}
{{PERSISTENT_ANOMALIES_LIST}}
{{else}}
No persistent issues.
{{/if}}

---

## Pattern Changes

{{PATTERN_CHANGES_DESCRIPTION}}

---

## Health Indicators

| Indicator | Previous | Current | Trend |
|-----------|----------|---------|-------|
| Code Organization | {{PREV_ORG_SCORE}} | {{CURR_ORG_SCORE}} | {{ORG_TREND}} |
| Dependency Health | {{PREV_DEP_SCORE}} | {{CURR_DEP_SCORE}} | {{DEP_TREND}} |
| Technical Debt | {{PREV_DEBT_SCORE}} | {{CURR_DEBT_SCORE}} | {{DEBT_TREND}} |

---

## Recommendations

### Based on Changes

{{CHANGE_BASED_RECOMMENDATIONS}}

### Ongoing

{{ONGOING_RECOMMENDATIONS}}

---

## Review History

| Date | Files | LOC | Components | Key Changes |
|------|-------|-----|------------|-------------|
{{HISTORY_TABLE}}

---

*Report generated {{CURRENT_DATE}}. Previous review: {{PREVIOUS_DATE}}.*
