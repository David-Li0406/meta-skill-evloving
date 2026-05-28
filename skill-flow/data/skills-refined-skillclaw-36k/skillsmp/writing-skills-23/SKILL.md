---
name: writing-skills
description: "Use when creating new skills, editing existing skills, or verifying skills work before deployment. Follows TDD methodology."
---

# Writing Skills

## Overview

**Writing skills IS TDD applied to documentation.**

Write test (pressure scenario), watch it fail (baseline), write skill, watch it pass, refactor (close loopholes).

## When to Create

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Well-documented standard practices
- Project-specific conventions (use CLAUDE.md)

## Structure Template

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions]. Third person, no workflow summary.
---

# Skill Title

## Overview
[Core principle in 1-2 sentences]

## When to Use
[Bullet list with symptoms and use cases]

## Core Process
[Main workflow/steps]

## Quick Reference
[Table or bullets for scanning]

## Common Mistakes
[What goes wrong + fixes]

## Examples
[Good and bad with explanations]
```

## Quality Checklist

- [ ] Name uses only letters, numbers, hyphens
- [ ] Description starts with "Use when..." (max 500 chars)
- [ ] Description in third person, no workflow summary
- [ ] Overview has core principle
- [ ] Quick reference table for scanning
- [ ] Common mistakes section
- [ ] Under 100 lines for lean skills, under 500 for comprehensive
- [ ] Keywords throughout for searchability

## Testing Requirements

**RED Phase:**
1. Create pressure scenarios (3+ combined pressures for discipline skills)
2. Run scenarios WITHOUT skill - document baseline behavior
3. Identify patterns in failures/rationalizations

**GREEN Phase:**
1. Write minimal skill addressing specific baseline failures
2. Run scenarios WITH skill - verify compliance

**REFACTOR Phase:**
1. Identify NEW rationalizations from testing
2. Add explicit counters
3. Re-test until bulletproof

## Examples

**Good Description:**
```yaml
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

**Bad Description:**
```yaml
description: For async testing - write test first, wait for condition, verify result
```
(Summarizes workflow - Claude may follow description instead of reading skill)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Workflow in description | Only triggers in description |
| No testing before deploy | Run RED-GREEN-REFACTOR cycle |
| Too verbose (500+ lines) | Split into SKILL.md + reference files |
| Generic labels (step1, helper2) | Use semantic names |
| Multi-language examples | One excellent example is enough |
