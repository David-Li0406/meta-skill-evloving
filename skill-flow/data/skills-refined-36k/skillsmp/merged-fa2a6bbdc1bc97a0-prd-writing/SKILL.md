---
name: prd-writing
description: Use this skill to create comprehensive Product Requirements Documents (PRD) that define what to build and why, focusing on goals, scope, user stories, and success criteria without implementation details.
---

# PRD Writing

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING FILES**:
   - Look in `docs/reference/pm/versions/` directory.
   - If a version file already exists, READ it first and ask the user if they want to update it.
   - DO NOT create duplicate version files.

2. **ALWAYS USE THIS SKILL**:
   - When the user says "write PRD", "create PRD", or "write requirements" → USE THIS SKILL.
   - DO NOT write PRD files directly without using this skill to ensure proper format and validation.

3. **ALWAYS SAVE TO CORRECT PATH**:
   - Path: `docs/reference/pm/versions/{version-name}.md`.
   - NO exceptions, NO other locations.

4. **READ CONSTITUTION FIRST**:
   - ALWAYS read `docs/reference/pm/constitution.md` before writing PRD.
   - Use constraints and domain info from the constitution.

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Gather context**: Check `docs/reference/pm/` for existing product context.
2. **Define problem & solution**: Start with a clear problem statement and high-level solution.
3. **Set boundaries**: Clearly separate Goals from Non-Goals.
4. **Document requirements**: List functional requirements (FR-XXX format).
5. **Define success**: Set measurable success criteria.
6. **Track unknowns**: Document open questions for later clarification.
7. **Save PRD**: ALWAYS write to `docs/reference/pm/versions/{version-name}.md`.

## PRD Template

```markdown
# [Feature Name] PRD

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD

## 1. Overview

- Problem statement
- Proposed solution (high-level)
- Success metrics

## 2. Background

- Current state
- User pain points
- Market context (if relevant)

## 3. Goals & Non-Goals

### Goals

- What this feature WILL accomplish

### Non-Goals

- What this feature will NOT address

## 4. User Stories

[Link to or embed user stories]

## 5. Functional Requirements

- FR-001: [Requirement description]
- FR-002: [Requirement description]

## 6. User Experience

- Key user flows
- Interaction patterns
- Edge cases

## 7. Success Criteria

- Measurable outcomes
- Acceptance criteria

## 8. Open Questions

- Unresolved decisions
- Items needing clarification
```

## Key Rules

- ALWAYS focus on WHAT to build, NOT HOW to implement.
- MUST include quantifiable success metrics.
- ALWAYS explicitly state what's out of scope in Non-Goals.
- MUST save output to `docs/reference/pm/versions/` directory.

## Common Mistakes

- ❌ Include implementation details → ✅ Focus on WHAT, not HOW.
- ❌ Vague success metrics → ✅ Quantifiable outcomes.
- ❌ Missing non-goals → ✅ Explicitly state what's out of scope.

---

## Iron Law

**NO PRD WITHOUT VALIDATED REQUIREMENTS**

This rule is non-negotiable. Before writing PRD:

1. User pain points must be documented.
2. Success metrics must be defined.
3. Scope must be explicitly approved by the user.

### Rationalization Defense

| Excuse                          | Reality                                 |
| ------------------------------- | --------------------------------------- |
| "Requirements are clear enough" | Implicit requirements cause scope creep |
| "We can refine the PRD later"   | Late changes cost 10x more to implement |
| "User will accept anything"     | Users always have hidden expectations   |
| "It's just a small feature"     | Small features grow into big problems   |