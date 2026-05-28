# Feature: <FEATURE_NAME>

## Purpose

[1-2 sentences: What this feature does and why it exists]

## Key Files

Files this feature owns (with line pointers for critical sections):

| File | Lines | Purpose |
|------|-------|---------|
| `src/feature/main.ts` | all | Main entry point |
| `src/feature/utils.ts` | L10-50 | Helper functions |
| `src/feature/types.ts` | all | Type definitions |

## Invariants

Rules specific to this feature:

- [Invariant 1 - e.g., "All state changes emit events"]
- [Invariant 2 - e.g., "Input validation before processing"]

## Current Tasks

From CONTEXT.md or recent work:

- [ ] [Pending task]
- [→] [Active task - in progress]
- [x] [Recently completed for reference]

## Known Issues

Current bugs or limitations:

- **[Issue]:** [Description] → Workaround: [if any]
- [none] if no known issues

## Interface

### Inputs
- [Input 1]: [Type] - [Description]
- [Input 2]: [Type] - [Description]

### Outputs
- [Output 1]: [Type] - [Description]
- [Output 2]: [Type] - [Description]

### Events Emitted
- `event:name` - [When emitted]

### Events Consumed
- `event:name` - [What triggers action]

## Dependencies

### Depends On
- `<other_feature>` - [What it needs from that feature]

### Depended On By
- `<other_feature>` - [What depends on this feature]

## How to Work on This Feature

**Before making changes:**
1. Read this entire bundle
2. Check DELTA_CONTEXT for recent changes to these files
3. Understand the invariants

**Testing:**
- Run: `[test command for this feature]`
- Key test files: `tests/feature/`

**Common pitfalls:**
- [Pitfall 1]
- [Pitfall 2]

---
*Last updated: <TIMESTAMP> | Files: <COUNT>*
