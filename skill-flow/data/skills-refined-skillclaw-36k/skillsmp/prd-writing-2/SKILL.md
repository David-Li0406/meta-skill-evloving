---
name: prd-writing
description: Creates developer-friendly PRDs with dual-format output (human-readable + machine-readable YAML). Use when users want to write a PRD, document feature requirements, create product specs, or turn ideas into structured requirements. Guides through 4 phases - requirement clarification, human sections, AI outline review, and final output. Supports bilingual (English/Chinese) PRD generation.
---

# PRD Writing Skill

Create clear, developer-friendly Product Requirements Documents with dual-format output.

## Core Principles

1. **Be a thinking partner** — Help PMs clarify thoughts, not just transcribe them
2. **No redundancy** — User perspective and system perspective are different views
3. **Right audience** — Overview/Metrics for leadership, requirements for developers, YAML for AI
4. **Filesystem as memory** — Write decisions to file immediately, read before each phase

## Workflow Overview

```
Phase 0: Requirement Clarification
         ↓ CREATE prd-[feature]-clarification.md
         ↓ CREATE prd-[feature].md

Phase 1: Write Human-Readable Sections
         ↓ UPDATE prd-[feature].md

Phase 2: Generate For-AI Outline (PM Review)
         ↓ APPEND outline to prd-[feature].md

Phase 3: Final Output + Bilingual Option
         ↓ UPDATE prd-[feature].md
         ↓ ASK: Generate Chinese version?
         ↓ IF YES: CREATE prd-[feature]-zh.md
```

## File Operations

| Phase | Action | Operation |
|-------|--------|-----------|
| Phase 0 Start | Create both files | CREATE clarification + PRD |
| Phase 0 During | Record each decision | UPDATE clarification log |
| Phase 1-3 Start | Refresh context | READ both files |
| Phase 3 End | Bilingual option | ASK user, sync both versions |

**Critical Rules:**
- Create files FIRST, before asking clarification questions
- Update clarification log after EACH decision, not in batches
- Read files before each phase to refresh context
- When updating bilingual PRDs, sync BOTH versions

---

## Phase 0: Requirement Clarification

**Input:** PM's raw requirement (bullet points, sentence, or rough document)

**FIRST ACTION:** Create two files using templates from [references/templates.md](references/templates.md)

### Clarification Strategy

Ask about these areas when unclear:

| Area | Example Questions |
|------|-------------------|
| Target User | Who exactly uses this? Different user types? |
| Problem | What specific pain point? Why solve it now? |
| Scope | What's included? What's explicitly excluded? |
| Metrics | How do we know it worked? What numbers? |
| Edge Cases | What happens when X fails? |
| Dependencies | New system or existing? Who owns it? |

### After Each PM Answer

UPDATE Key Decisions table in clarification log immediately:

```markdown
| Scope | Web or API? | Web only |
| Threshold | How many failures? | 5 in 5 minutes |
```

### When to Escalate

Log in Escalation Notes and suggest PM consult:
- Technical feasibility unclear → Tech Lead
- Complex business rules → Business/operations team
- Compliance/legal concerns → Legal team
- Cross-team dependencies → Other teams first

### Phase 0 Complete

When PM confirms requirements are clear:
1. Update Document Status: Clarification → ✅ Complete
2. Proceed to Phase 1

---

## Phase 1: Write Human-Readable Sections

**FIRST:** Read both files to refresh context.

Fill in PRD sections. See [references/templates.md](references/templates.md) for detailed section templates.

### Section Overview

1. **Overview** — Feature name, one-sentence summary, business context
2. **Success Metrics** — Metrics aligned with problem statement
3. **Impact Scope** — Systems affected (brief list)
4. **User Perspective** — User stories, happy path, edge cases, UI prototype
5. **System Perspective** — Architecture, functional requirements, NFRs
6. **Other Notes** — Dependencies, compliance, assumptions, risks, out of scope

### Phase 1 Complete

1. Update Document Status: Human Sections → ✅ Complete
2. Ask PM to review
3. After PM approval, proceed to Phase 2

---

## Phase 2: Generate For-AI Outline

**FIRST:** Read both files to refresh context.

APPEND outline to PRD (don't replace For AI section yet). See [references/templates.md](references/templates.md) for outline format.

### Outline Contents

1. **Entities Identified** — Data entities with fields
2. **APIs/Interfaces** — Endpoints (mark inferred ones)
3. **Business Rules** — Condition → action pairs
4. **Technical Details Added** — Defaults you assumed (PM must confirm)
5. **Open Questions** — Items needing PM clarification

### Why This Step Matters

- PM discovers gaps they hadn't considered
- Technical defaults are made explicit
- Unclear areas are surfaced before they become bugs

### Phase 2 Complete

1. Update Document Status: For AI Outline → ✅ Complete
2. Wait for PM approval before Phase 3

---

## Phase 3: Final Output + Bilingual Option

**FIRST:** Read both files to refresh context.

### Step 1: Update Human Sections

Add confirmed details back to human-readable sections:
- Add to Functional Requirements if significant
- Add to Other Notes if supplementary

### Step 2: Generate For-AI Section

Replace outline with complete YAML specification. See [references/yaml-spec.md](references/yaml-spec.md) for the full YAML schema.

### Step 3: Bilingual PRD Generation

After completing the English PRD, ASK the user:

> "PRD is complete. Would you like me to generate a Chinese version (prd-[feature]-zh.md)?"

**If YES:**
1. Create `prd-[feature]-zh.md` with translated content
2. Keep the same structure and section headers (translated)
3. Preserve technical terms, API names, and code in English
4. Add cross-reference link in both files:
   - English: `> **Chinese Version:** [prd-[feature]-zh.md](prd-[feature]-zh.md)`
   - Chinese: `> **English Version:** [prd-[feature].md](prd-[feature].md)`

**Bilingual Sync Rules:**
- When updating either version, ALWAYS update both
- Before making changes, READ both files
- After changes, verify both files are in sync
- Technical accuracy takes priority over translation elegance

### Step 4: Update Document Status

```markdown
| Phase | Status | Date |
|-------|--------|------|
| Clarification | ✅ Complete | YYYY-MM-DD |
| Human Sections | ✅ Complete | YYYY-MM-DD |
| For AI Outline | ✅ Complete | YYYY-MM-DD |
| Final | ✅ Complete | YYYY-MM-DD |
| Chinese Version | ✅ Complete | YYYY-MM-DD | (if applicable)
```

---

## Behavior Rules

### DO:
- Create files FIRST, before clarification questions
- Update clarification log after EACH decision
- Read files before each phase
- Challenge vague requirements ("what does 'fast' mean?")
- Mark inferred vs. stated requirements
- Ask about Chinese version after PRD completion
- Sync both language versions on any update

### DON'T:
- Write PRD without understanding the requirement
- Rely on memory (read the files!)
- Guess technical details without marking as assumptions
- Repeat same information in multiple sections
- Skip outline review step
- Update one language version without updating the other

---

## References

- **Templates:** [references/templates.md](references/templates.md) — File templates and section formats
- **YAML Spec:** [references/yaml-spec.md](references/yaml-spec.md) — Complete For-AI YAML schema
