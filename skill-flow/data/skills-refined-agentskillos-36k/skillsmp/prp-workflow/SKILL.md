---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic feature implementation. PRPs are PRDs engineered for AI - they include complete context, implementation blueprints, and validation gates for one-pass success.

  Use when user: (1) wants to implement a complex feature systematically, (2) asks to "create/generate a PRP", (3) mentions "PRP workflow" or "context engineering", (4) has a feature file to implement, (5) asks to "clarify" or "review" a PRP for ambiguities, (6) asks to "execute" an existing PRP.

  Three modes: Generation (create PRP from requirements), Clarification (resolve ambiguities before execution), Execution (implement from PRP with validation loops).
---

# PRP Workflow

Three-phase workflow: **Generation** -> **Clarification** (recommended) -> **Execution**

---

## Mode 1: PRP Generation

Generate a comprehensive PRP from a feature request.

### Process

1. **Launch 2 parallel Opus agents** for research:

   **Agent #1 - Codebase Research**: Search for similar features/patterns in the codebase. Identify conventions (imports, naming, structure), test patterns, and architecture. Return a summary of patterns found and a list of 5-10 key files to read.

   **Agent #2 - External Research**: Search the web for library documentation, implementation examples, best practices, and known gotchas. Return URLs, version-specific details, and recommendations.

2. **Read key files** identified by agents to build deep understanding

3. **Clarify with user** (if needed) using AskUserQuestion for patterns to follow, integration requirements, constraints

4. **Generate PRP** using the template in [references/prp-template.md](references/prp-template.md)

5. **Save** to `plans/{XXX}-{feature-name}.md`
   - Auto-increment from highest number in `plans/`
   - Filename: lowercase, hyphens, max 50 chars

6. **Report** confidence score (1-10) and ask: clarify or execute?

---

## Mode 2: PRP Clarification

Identify and resolve underspecified areas BEFORE implementation.

### Process

1. **Locate PRP** - Ask user or search `plans/*.md`

2. **Launch an Opus agent** to analyze the PRP for ambiguities:

   The agent should analyze the PRP against the coverage taxonomy in [references/clarification-taxonomy.md](references/clarification-taxonomy.md). Mark each category (Functional Scope, Data Model, UX Flow, Non-Functional, Integration, Edge Cases, Constraints, Terminology, Completion Signals) as Clear/Partial/Missing. Return a coverage summary table and up to 5 recommended clarification questions prioritized by (Impact × Uncertainty).

3. **Present questions** to user using AskUserQuestion (max 5, up to 4 per batch):
   ```typescript
   AskUserQuestion({
     questions: [
       {
         question: "Which authentication method should the system use?",
         header: "Auth",
         multiSelect: false,
         options: [
           { label: "OAuth 2.0 + JWT", description: "Stateless, scalable" },
           { label: "Session cookies", description: "Traditional, requires storage" }
         ]
       }
     ]
   })
   ```

4. **Integrate answers** into PRP:
   - Add `## Clarifications` section with `### Session YYYY-MM-DD`
   - Record: `- Q: <question> → A: <answer>`
   - Update relevant PRP sections per integration table in taxonomy reference

5. **Report** coverage summary and recommend next step

### Early Exit
- No critical gaps: proceed to execution
- PRP missing: generate first (Mode 1)

---

## Mode 3: PRP Execution

Implement a feature using an existing PRP.

### Process

1. **Load PRP** - Read completely, note success criteria and validation gates

2. **Launch an Opus agent** to execute the implementation:

   The agent should:
   - Create a TodoWrite task list from the PRP's implementation blueprint
   - Work through tasks systematically, keeping ONE task in_progress at a time
   - Follow patterns from PRP exactly (don't introduce new patterns)
   - Run validation commands after each major step
   - Fix failures immediately (don't accumulate)
   - Return: implementation summary, files modified, validation results, any deviations from PRP

3. **Handle blockers** - If agent returns with issues, help resolve

4. **Report** completion summary

### Validation Philosophy

If validation fails:
1. Read error carefully
2. Understand root cause
3. Fix underlying issue (don't patch)
4. Re-run validation
5. Repeat until passing

---

## Quick Reference

### File Locations
- PRPs: `plans/{XXX}-{feature-name}.md`
- Template: [references/prp-template.md](references/prp-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

### Agent Summary
| Phase | Agents | Model |
|-------|--------|-------|
| Generation | 2 parallel (codebase + external research) | Opus |
| Clarification | 1 (coverage analysis) | Opus |
| Execution | 1 (implementation) | Opus |

### Key Constraints
- Clarification: max 5 questions, 4 per AskUserQuestion batch
- Execution: one task in_progress at a time
- Validate after each major step
- If CLAUDE.md exists, follow its rules

### Anti-Patterns
- Skipping research to save time
- Implementing without reading full PRP
- Ignoring validation failures
- Creating new patterns instead of following existing ones
