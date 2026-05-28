---
name: clarify
description: Clarify ambiguous requirements then auto-enter Plan Mode. Required on first prompt of session.
---

# Clarify (Meeting Context Hub)

Skill for clarifying requirements and auto-entering Plan Mode.

## Workflow

```
/clarify
    │
    ├─ Phase 1: Record Original
    │   └─ Record original request as-is
    │
    ├─ Phase 2: Question
    │   └─ Resolve ambiguities via AskUserQuestion
    │
    ├─ Phase 3: Summary
    │   └─ Before/After comparison
    │
    └─ Phase 4: Auto-enter Plan Mode
        └─ Call EnterPlanMode()
```

## Phase 1: Record Original

```markdown
## Original Requirement
"{original request as-is}"

Identified ambiguities:
- Scope: [unclear scope areas]
- Behavior: [unclear behavior areas]
- Data: [unclear data format areas]
- Constraints: [unclear constraint areas]
```

## Phase 2: Question

Use AskUserQuestion tool. Multiple questions allowed at once.

**Question Design Principles**:
- Specific > Abstract
- Provide options > Open questions
- One concern at a time

```
AskUserQuestion:
question: "Which authentication method should we use?"
options:
  - label: "Supabase Auth (Recommended)"
    description: "Email/password + OAuth"
  - label: "NextAuth"
    description: "Various provider support"
```

## Phase 3: Summary

```markdown
## Requirement Clarification Summary

### Before (Original)
"{original request}"

### After (Clarified)
**Goal**: [precise goal]
**Scope**: [inclusions/exclusions]
**Constraints**: [constraints]
**Success Criteria**: [completion criteria]

**Decisions Made**:
| Question | Decision |
|----------|----------|
| [Question 1] | [Decision] |
| [Question 2] | [Decision] |
```

## Phase 4: Auto-enter Plan Mode

After clarification, **always** call EnterPlanMode:

```
Requirement clarification complete. Entering Plan Mode.
```
→ Call `EnterPlanMode()`

**Important**: After clarify completes, auto-enter Plan Mode without asking user.

## Meeting Context Hub Example

### Input
```
"Implement meeting summary feature"
```

### Phase 2 Questions

```
AskUserQuestion:
1. Summary format? → PRD (problem/goal/scope/requirements)
2. Include Action Items? → Yes, assignee/deadline
3. Storage location? → Supabase + Obsidian
4. Auto-generate tags? → Reuse existing tags
```

### Phase 3 Summary

```markdown
### Before
"Implement meeting summary feature"

### After
**Goal**: Summarize meeting text to PRD format + extract Action Items
**Scope**:
- Include: PRD extraction, Action Items, auto-tagging, Obsidian storage
- Exclude: Speech recognition, real-time recording
**Constraints**: Use Claude API, Zod schema validation
**Success Criteria**: Meeting input generates PRD + Action Items saved
```

### Phase 4

```
Requirement clarification complete. Entering Plan Mode.
```
→ Call EnterPlanMode()

## Rules

1. **No assumptions**: Question if unclear
2. **PRD level**: Specific enough to implement
3. **Auto-enter**: Always call EnterPlanMode after clarification
4. **Reference plans**: Check existing PLAN.md, implementation-plan.md

## Next Steps

After Plan Mode:
- User approval
- Start implementation with `/implement` skill
