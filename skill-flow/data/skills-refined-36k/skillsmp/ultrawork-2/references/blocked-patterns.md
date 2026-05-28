# Blocked Patterns

## Zero Tolerance List

These phrases trigger automatic completion block:

### Speculation
| Pattern | Why Blocked |
|---------|-------------|
| "should work" | No evidence |
| "should be fine" | No evidence |
| "probably works" | Uncertainty |
| "might work" | Uncertainty |
| "seems to work" | No verification |

### Incompleteness
| Pattern | Why Blocked |
|---------|-------------|
| "basic implementation" | Partial work |
| "basic version" | Partial work |
| "simplified version" | Partial work |
| "minimal implementation" | Partial work |
| "skeleton" | Incomplete |
| "placeholder" | Not real |
| "stub" | Not implemented |

### Deferred Work
| Pattern | Why Blocked |
|---------|-------------|
| "TODO" | Unfinished |
| "FIXME" | Known issue |
| "HACK" | Technical debt |
| "for now" | Temporary |
| "temporary" | Not permanent |
| "you can add" | Not done |
| "you can extend" | Not done |
| "left as exercise" | Not done |

### False Completion
| Pattern | Why Blocked |
|---------|-------------|
| "implementation complete" | (without evidence) |
| "feature complete" | (without evidence) |
| "done" | (without evidence) |
| "finished" | (without evidence) |
| "all set" | (without evidence) |

## Detection Rules

### Simple Pattern Match
```python
BLOCKED_PATTERNS = [
    r"should\s+(work|be\s+fine)",
    r"probably\s+works?",
    r"basic\s+(implementation|version)",
    r"simplified\s+version",
    r"TODO",
    r"FIXME",
    r"you\s+can\s+(add|extend)",
]
```

### Context-Aware Check
Some patterns only block without counter-evidence:

```
"basic implementation" + "per user's MVP scope request" → OK
"basic implementation" + nothing → BLOCKED
```

## Override Mechanism

Worker can override with explicit justification:

```markdown
## Evidence

Note: Using "basic version" pattern.
Justification: User explicitly requested MVP scope.
Reference: AskUserQuestion response at 12:34
```

## Enforcement Points

| Point | Check |
|-------|-------|
| Worker output | Scan for blocked patterns |
| TaskUpdate comment | Validate no blocked phrases |
| Phase transition | Full scan before COMPLETE |
| /ultrawork-status | Highlight any blocked patterns found |

## User Notification

When blocked pattern detected:

```
⚠️  BLOCKED PATTERN DETECTED

Task: Implement auth
Pattern: "basic implementation"
Location: Worker output line 42

Cannot mark complete without:
1. Evidence that work is actually complete, OR
2. Explicit user approval of scope reduction

Options:
- Fix the implementation
- Provide counter-evidence
- Cancel session
```
