---
name: improving-jarvis
description: "Use when identifying opportunities to improve the Jarvis system, adding patterns, creating skills, or updating rules based on repeated guidance."
---

# Improving Jarvis

## Overview

Jarvis improves through captured patterns, new skills, and refined rules. This skill guides when and how to enhance the system.

## When to Trigger

**Automatic triggers:**
- Same instruction given manually 3+ times
- Discovered pattern not in library
- Workflow inefficiency noticed
- User explicitly requests improvement

**Ask user:** "This [pattern/workaround] seems reusable. Should I capture it?"

## Improvement Types

### 1. Add Pattern
**When:** Reusable solution discovered
**Action:**
1. Document in patterns/ with keywords
2. Add to pattern index
3. Test with 3 example prompts

### 2. Create Skill
**When:** Complex workflow needs guidance
**Action:**
1. Follow writing-skills (TDD approach)
2. Run RED-GREEN-REFACTOR cycle
3. Add to skill-rules.json

### 3. Update Rule
**When:** Behavior needs consistency
**Action:**
1. Modify existing rule or create new
2. Test for false positive rate < 10%
3. Preserve backward compatibility

### 4. Add Hook
**When:** Automation should apply to all events
**Action:**
1. Follow writing-hooks guide
2. Test edge cases and timeouts
3. Add graceful failure handling

### 5. Update CLAUDE.md
**When:** Project conventions change
**Action:**
1. Follow writing-claude-md guide
2. Respect token budgets
3. Test with real prompts

## Validation Process

```
Create component following guide
        |
        v
Run component-specific tests
        |
        v
Monitor for 3 sessions
        |
        v
Issues found? --> Fix and retest
        |
        v (no issues)
Mark as stable
```

## Rollback Triggers

**Auto-rollback if:**
- False positive rate > 10%
- User reverts change manually
- Component causes quality degradation
- Test failures after change

**Rollback process:**
1. Revert to previous version
2. Document what went wrong
3. Analyze root cause
4. Create improved version with lessons

## Quality Checklist

Before marking improvement complete:

- [ ] Followed relevant writing-* skill
- [ ] Tested with real scenarios
- [ ] No regression in existing functionality
- [ ] Token budget respected
- [ ] Documented in appropriate location
- [ ] skill-rules.json updated (if skill)
- [ ] User approved improvement

## Improvement Tracking

Log improvements in `.claude/improvements.log`:

```
YYYY-MM-DD | TYPE | NAME | REASON
2025-01-04 | skill | git-expert | Repeated git guidance
2025-01-04 | pattern | optimistic-updates | Discovered in feature work
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Improve without testing | Run validation process |
| Skip user approval | Always confirm significant changes |
| Forget skill-rules.json | Update triggers for new skills |
| Too aggressive rollout | Monitor for 3 sessions first |
| No documentation | Log all improvements |
| Ignore false positives | Track and maintain < 10% rate |
