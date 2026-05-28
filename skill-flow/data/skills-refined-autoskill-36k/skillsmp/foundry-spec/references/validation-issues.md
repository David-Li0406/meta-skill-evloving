# Validation Issues

This reference describes the types of issues detected during spec validation.

## Issue Categories

### Structural Issues

| Issue | Severity | Auto-Fix |
|-------|----------|----------|
| Incorrect task count rollups | Error | Yes |
| Missing metadata blocks | Error | Yes |
| Orphaned nodes (no parent) | Error | Yes |
| Parent/child hierarchy mismatches | Error | Yes |
| Missing required fields | Error | Yes |
| Invalid node types | Error | Yes |

### Format Issues

| Issue | Severity | Auto-Fix |
|-------|----------|----------|
| Malformed timestamps | Warning | Yes |
| Invalid status values | Error | Yes |
| Invalid priority values | Warning | Yes |
| Non-ISO date formats | Warning | Yes |

### Dependency Issues

| Issue | Severity | Auto-Fix |
|-------|----------|----------|
| Circular dependencies | Error | No |
| Orphaned dependency references | Error | No |
| Deadlocks (mutual blocking) | Error | No |
| Bottlenecks (blocking many) | Warning | No |
| Bidirectional inconsistencies | Error | Yes |

### Quality Issues

| Issue | Severity | Auto-Fix |
|-------|----------|----------|
| Duplicate task titles | Warning | No |
| Similar descriptions | Warning | No |
| Overlapping acceptance criteria | Warning | No |
| Missing descriptions | Warning | No |
| Missing estimates | Warning | No |
| Missing verification tasks | Warning | No |

## Dependency Analysis Details

Use `spec action="analyze-deps"` to detect:

### Cycles

Circular dependency chains that prevent any task from starting.

```
Example: task-3-2 → task-3-5 → task-3-2
```

### Orphaned Dependencies

Tasks referencing dependencies that don't exist.

```
Example: task-5-2 references non-existent "task-2-9"
```

### Deadlocks

Tasks that block each other (mutual circular dependency).

```
Example: task-A depends on task-B, task-B depends on task-A
```

### Bottlenecks

Tasks that block many others (configurable threshold).

```
Example: task-1-1 blocks 5 other tasks (threshold: 3)
```

## Completeness Scoring

Use `spec action="completeness-check"` for quality scoring:

| Category | Weight | Checks |
|----------|--------|--------|
| Structure | 25% | All tasks have parents, no orphans, valid hierarchy |
| Metadata | 25% | Descriptions, estimates, acceptance criteria present |
| Dependencies | 25% | Dependencies declared, no cycles, proper ordering |
| Verification | 25% | Verify tasks present, coverage adequate |

### Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Ready for implementation |
| 75-89 | Good | Minor improvements recommended |
| 50-74 | Fair | Address gaps before proceeding |
| 0-49 | Poor | Significant work needed |

## Duplicate Detection

Use `spec action="duplicate-detection"` to find:

| Type | Detection Method | Severity |
|------|-----------------|----------|
| Exact title match | String equality | High |
| Similar description | >80% fuzzy match | Medium |
| Overlapping criteria | Shared text | Low |
| Redundant verification | Same scope | Medium |

## Example Validation Output

```
❌ Validation found 12 errors
   8 auto-fixable, 4 require manual intervention

   Errors:
   - 5 incorrect task count rollups
   - 2 missing metadata blocks
   - 1 orphaned node (task-5-3)
   - 2 circular dependencies
   - 2 parent/child mismatches

   Run 'spec action="fix"' to auto-fix 8 issues
```

## Resolution Priority

1. **First**: Run auto-fix for all auto-fixable issues
2. **Second**: Resolve circular dependencies (blocks progress)
3. **Third**: Fix orphaned dependency references
4. **Fourth**: Address quality warnings (duplicates, missing metadata)
