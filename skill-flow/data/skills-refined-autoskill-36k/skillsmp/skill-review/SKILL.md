---
name: skill-review
description: Review and propose improvements for Claude skills based on usage patterns.
---

# Skill Review

Analyze current session patterns and propose skill improvements.

## Skill Count Rule

**1 in, 1 out** - When adding a new skill, remove or merge an existing one.

Exception: Only when introducing a genuinely new concept that cannot be covered by existing skills.

## When to Propose New Skills

Only when ALL of these conditions are met:

1. Introduces a new concept not covered by existing skills
2. Same pattern repeated 3+ times
3. Cannot be achieved by improving an existing skill

## When to Propose Skill Improvements

- Manual corrections needed after skill execution
- Skill output requires consistent post-processing
- Skill doesn't cover edge cases encountered
- Skill conflicts with other skills or CLAUDE.md

## Review Process

1. **Identify patterns** - What repetitive work occurred this session?
2. **Evaluate value** - Would a skill reduce context/effort significantly?
3. **Check existing skills** - Is this covered? Needs update?
4. **Propose action** - New skill, update existing, or no action needed

## Output Format

```
## Skill Review Summary

### Patterns Observed
- [Pattern description]

### Recommendations
- [ ] New skill: `skill-name` - [reason]
- [ ] Update skill: `skill-name` - [what to change]
- [ ] No action needed - [reason]
```
