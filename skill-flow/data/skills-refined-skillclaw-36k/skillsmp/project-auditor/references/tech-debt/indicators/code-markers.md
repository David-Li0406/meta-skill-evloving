# Code Markers

Debt markers embedded in source code indicating acknowledged technical debt.

## Marker Types

### High Severity Markers

| Pattern | Regex | Weight | Description |
|---------|-------|--------|-------------|
| FIXME | `FIXME[:\s]` | 1.5 | Known bug or issue that needs fixing |
| HACK | `HACK[:\s]` | 3.0 | Workaround or shortcut that should be replaced |
| XXX | `XXX[:\s]` | 3.0 | Requires attention, often dangerous code |
| KLUDGE | `KLUDGE[:\s]` | 3.0 | Clumsy or inelegant solution |
| BUG | `BUG[:\s]` | 2.5 | Known bug in code |
| SECURITY | `SECURITY[:\s]\|INSECURE` | 5.0 | Security concern in code |

### Medium Severity Markers

| Pattern | Regex | Weight | Description |
|---------|-------|--------|-------------|
| TODO | `TODO[:\s]` | 0.5 | Task to be completed later |
| REFACTOR | `REFACTOR[:\s]` | 1.0 | Code needs restructuring |
| DEPRECATED | `@[Dd]eprecated\|DEPRECATED` | 1.5 | Code marked for removal |
| TEMP | `TEMP[:\s]\|TEMPORARY[:\s]` | 2.0 | Temporary code that should be removed |

### Low Severity Markers

| Pattern | Regex | Weight | Description |
|---------|-------|--------|-------------|
| OPTIMIZE | `OPTIMIZE[:\s]` | 0.5 | Performance improvement needed |
| REVIEW | `REVIEW[:\s]\|NEEDS.?REVIEW` | 0.5 | Code requires review |

## Examples

```python
# TODO: implement caching
# FIXME: race condition here
# HACK: bypassing validation
# XXX: security concern
# BUG: off-by-one error
# SECURITY: input not sanitized
```

## Age Multipliers

Older debt accumulates higher scores to incentivize cleanup.

| Age (Days) | Multiplier | Label |
|------------|------------|-------|
| < 180 | 1.0x | Recent |
| 180-365 | 1.25x | Aging |
| 365-730 | 1.5x | Old |
| > 730 | 2.0x | Ancient |

## Context Multipliers

| Context | Multiplier | Notes |
|---------|------------|-------|
| Critical Path | 1.5x | Debt in critical code paths is more impactful |
| Public API | 1.3x | Debt in public APIs affects consumers |
| Test File | 0.5x | Debt in tests is less critical |
| Generated Code | 0.1x | Generated code markers are often false positives |

## Score Caps

| Scope | Maximum Score |
|-------|---------------|
| Per Marker Type | 30 |
| Total Category | 100 |

## Remediation Priority

1. **SECURITY**: Address immediately - security vulnerabilities
2. **XXX/HACK/KLUDGE**: High priority - workarounds and dangerous code
3. **BUG/FIXME**: Medium-high priority - known issues
4. **TEMP/DEPRECATED**: Medium priority - cleanup needed
5. **TODO/REFACTOR**: Lower priority - improvements
6. **OPTIMIZE/REVIEW**: Lowest priority - enhancements
