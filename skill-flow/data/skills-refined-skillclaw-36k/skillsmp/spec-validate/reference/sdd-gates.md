# SDD Pre-Implementation Gates

Reference for gates applied to Initiative-type specs before implementation.

## Applicability

| Issue Type | Gates Applied |
|------------|---------------|
| Initiative | All gates |
| Feature | None (opt-in) |
| Task | None |

## Gates

### Simplicity Gate

Prevents over-engineering before implementation begins.

Checklist:
- [ ] Solution uses minimal projects/components
- [ ] No future-proofing or speculative features
- [ ] Complexity is justified by requirements

### Anti-Abstraction Gate

Prevents premature abstraction.

Checklist:
- [ ] Using framework/tools directly (no wrapper layers)
- [ ] Single representation of core concepts
- [ ] No "just in case" abstractions

### Integration-First Gate

Ensures integration points are defined before implementation.

Checklist:
- [ ] API contracts defined (if applicable)
- [ ] Integration points identified in spec
- [ ] Contract tests planned (if applicable)

## Gate Status

Gates are tracked in `validation.yaml` under the `gates` section:

```yaml
gates:
  simplicity:
    status: passed|failed|n/a
    reason: "[explanation if failed or n/a]"
  anti_abstraction:
    status: passed|failed|n/a
    reason: "[explanation]"
  integration_first:
    status: passed|failed|n/a
    reason: "[explanation]"
```

## Blocking Behavior

When gates are checked by task-dispatch:
1. Read validation.yaml from spec directory
2. If issue_type is Initiative and any gate status is "failed":
   - Block dispatch
   - Report which gates failed
   - Prompt user to resolve via /clarify or manual edit
3. If all gates passed or issue_type is not Initiative: proceed

## Resolution

Failed gates can be resolved by:
1. `/clarify` - Interactive resolution
2. Manual edit of validation.yaml with justification
3. Changing issue_type (if scope was misclassified)
