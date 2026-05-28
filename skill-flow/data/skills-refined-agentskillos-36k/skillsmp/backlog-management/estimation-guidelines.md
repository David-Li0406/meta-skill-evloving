# Token Estimation Guidelines

This document provides guidance for estimating task complexity and token usage.

---

## Quick Reference

| Task Type | Typical Range | Notes |
|-----------|---------------|-------|
| Simple bug fix | 5K-15K | Single file, clear cause |
| Complex bug fix | 20K-50K | Multiple files, investigation needed |
| Small feature | 15K-30K | 1-2 files, clear spec |
| Medium feature | 30K-60K | 3-5 files, some decisions |
| Large feature | 60K-150K | Many files, architecture impact |
| Refactor (small) | 10K-25K | Extract function/component |
| Refactor (large) | 50K-200K | Service layer, patterns |
| Test coverage | 10K-30K | Per test file |
| Documentation | 5K-15K | Per document |

---

## Estimation Formula

```
Base Estimate = (Files Touched × 8K) + (Decisions × 5K) + (Tests × 5K)
Adjusted = Base × Category Multiplier
```

### Category Multipliers

| Category | Multiplier | Reason |
|----------|------------|--------|
| bug | 1.0 | Standard baseline |
| feature | 1.2 | New code, more decisions |
| refactor | 0.8 | Existing patterns, less research |
| test | 0.7 | Mechanical, patterns known |
| docs | 0.5 | No code execution |
| schema | 1.5 | High risk, careful changes |
| security | 1.5 | Requires research, validation |

---

## Historical Data

From completed sprints:

### SPRINT-041 (Bug Fixes)
| Task | Est | Actual | Variance |
|------|-----|--------|----------|
| TASK-1109 | ~30K | 25K | -17% |
| TASK-1110 | ~15K | 12K | -20% |
| TASK-1111 | ~20K | 18K | -10% |
| TASK-1112 | ~25K | 22K | -12% |
| TASK-1113 | ~20K | 28K | +40% |
| **Average** | | | **-4%** |

### SPRINT-040 (UI Design)
| Task | Est | Actual | Variance |
|------|-----|--------|----------|
| TASK-1100 | ~25K | 30K | +20% |
| TASK-1101 | ~20K | 18K | -10% |
| **Average** | | | **+5%** |

---

## Estimation Checklist

Before estimating, consider:

- [ ] **File count**: How many files will be touched?
- [ ] **Test coverage**: Are tests required? How many?
- [ ] **Dependencies**: Will this need IPC changes? Schema changes?
- [ ] **Investigation**: Is root cause known or needs research?
- [ ] **Review complexity**: Will SR Engineer need deep review?
- [ ] **Risk level**: Could this break existing functionality?

---

## Red Flags (Add Buffer)

Add 50-100% buffer when:
- Task involves debugging intermittent issues
- Multiple services need coordination
- Database schema changes required
- Security-sensitive code
- First time touching this area of codebase
- Previous similar tasks had large overruns

---

## Estimation Examples

### Example 1: Simple Bug Fix

**Task:** Fix button not disabling during form submit

```
Files: 1 (FormComponent.tsx)
Decisions: 0 (clear fix)
Tests: 1 (update existing)

Base: (1 × 8K) + (0 × 5K) + (1 × 5K) = 13K
Category: bug × 1.0 = 13K
Estimate: ~15K (round up)
```

### Example 2: New Feature

**Task:** Add export to CSV functionality

```
Files: 3 (ExportService, ExportButton, types)
Decisions: 2 (format, columns)
Tests: 2 (service, component)

Base: (3 × 8K) + (2 × 5K) + (2 × 5K) = 44K
Category: feature × 1.2 = 53K
Estimate: ~55K
```

### Example 3: Large Refactor

**Task:** Extract sync logic to SyncScheduler service

```
Files: 8 (service + 7 consumers)
Decisions: 3 (API, state, coordination)
Tests: 4 (service + integration)

Base: (8 × 8K) + (3 × 5K) + (4 × 5K) = 99K
Category: refactor × 0.8 = 79K
Red flag: First major service pattern = +50%
Estimate: ~120K
```

---

## Tracking Accuracy

After completing tasks, update backlog.csv with actual tokens:

```csv
BACKLOG-XXX,Title,category,priority,completed,SPRINT-XXX,~30K,28K,-7%,[BACKLOG-XXX.md]
```

This builds historical data for better future estimates.
