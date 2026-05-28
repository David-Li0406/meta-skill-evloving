---
title: Phase 6 - Learning Documentation
description: What to document, learnings.md format, and converting learnings to process improvements
keywords: learning, documentation, improvements, retrospective, patterns
file-type: reference
skill: executing-tasks
---

# Phase 6: Learning Documentation

## What to Document

**Always document:**
- [ ] Blockers encountered and resolutions
- [ ] Unexpected complexity discovered
- [ ] Patterns that worked well
- [ ] Patterns that failed
- [ ] Missing documentation discovered
- [ ] Tool/skill gaps identified

**Skip documenting:**
- Routine execution without issues
- Standard patterns applied successfully
- Information already in existing docs

## learnings.md Format

**Location:** `specs/<epic-id>/<story-id>/learnings.md` or task-level notes

**Structure:**
```markdown
# Learnings - [Task/Story ID]

## Date: [ISO date]

### Blockers Encountered
- **[Blocker]:** [Description]
  - Resolution: [How resolved]
  - Time impact: [Duration]

### Patterns Discovered
- **[Pattern name]:** [When to use]
  - Example: [Concrete example]

### Process Improvements
- **[Improvement]:** [Recommendation]
  - Impact: [Expected benefit]

### Missing Documentation
- [Doc that should exist but doesn't]
- [Doc that was outdated/incorrect]
```

## Converting to Improvements

**Improvement pipeline:**
| Learning Type | Converts To | Action |
|---------------|-------------|--------|
| Missing doc | Documentation task | Create issue |
| Skill gap | Skill enhancement | Update skill |
| Process friction | Workflow update | Update CLAUDE.md |
| Pattern discovery | Reference addition | Add to references |
| Tool limitation | Tool improvement | Create enhancement issue |

**Conversion checklist:**
- [ ] Review learnings for actionable items
- [ ] Categorize by improvement type
- [ ] Create issues/tasks for significant items
- [ ] Update relevant skills/docs for quick wins
- [ ] Link improvements to original learning

## Learning Quality Criteria

**Good learning entry:**
- Specific and actionable
- Includes resolution or recommendation
- References concrete example
- Estimates impact

**Poor learning entry:**
- Vague ("things were hard")
- No resolution path
- Missing context
- No actionable outcome
