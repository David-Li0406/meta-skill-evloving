---
name: writing-rules
description: "Use when creating or updating rules in CLAUDE.md, settings, or rule files. Covers confidence thresholds and false positive prevention."
---

# Writing Rules

## Overview

Rules are constraints that guide behavior. Good rules are specific, testable, and have clear thresholds for when they apply.

## When to Create

**Create a rule when:**
- Same guidance given 3+ times manually
- Behavior needs to be consistent across sessions
- Mistake pattern keeps recurring
- Process discipline is required

**Don't create for:**
- Occasional edge cases (document as patterns instead)
- User preferences that change frequently
- One-time instructions

## Structure Template

```markdown
## Rule Name

**When:** [Specific trigger conditions]
**Confidence:** [high/medium/low - when to apply vs ask]
**Action:** [What to do]

### Examples
- Good: [Correct application]
- Bad: [Incorrect application]

### Exceptions
[When this rule doesn't apply]
```

## Quality Checklist

- [ ] Clear trigger condition (not vague)
- [ ] Confidence threshold defined
- [ ] Both good AND bad examples
- [ ] Exceptions explicitly listed
- [ ] Testable (can verify rule was followed)
- [ ] No overlap with existing rules
- [ ] Assigned to correct category (process/domain/project)

## Testing Requirements

1. **Create test cases** - 5+ scenarios where rule should apply
2. **Create negative cases** - 5+ scenarios where rule should NOT apply
3. **Run through agent** - Verify correct activation
4. **Measure false positive rate** - Target < 10%
5. **Monitor for 3 sessions** - Auto-rollback if quality drops

## Examples

**Good Rule:**
```markdown
## Import Path Verification

**When:** Adding or modifying import statements
**Confidence:** high
**Action:** Verify path exists by checking 3+ existing examples in codebase

### Examples
- Good: Check `src/components/Button.tsx` exists before importing
- Bad: Assume `@/components/Button` works without verification

### Exceptions
- Standard library imports (React, Node built-ins)
- Well-known packages from package.json
```

**Bad Rule:**
```markdown
## Be Careful

**When:** Doing things
**Action:** Think before acting
```
(Too vague, not testable, no examples)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Rule too broad | Narrow to specific trigger |
| No confidence threshold | Add high/medium/low guidance |
| Missing exceptions | List when rule doesn't apply |
| No examples | Add good AND bad examples |
| Overlaps existing rule | Merge or differentiate clearly |
| Not testable | Rewrite with observable outcome |
