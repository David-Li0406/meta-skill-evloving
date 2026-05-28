---
template: investigation
status: active
date: {{DATE}}
backlog_id: {{BACKLOG_ID}}
title: "{{TITLE}}"
author: Hephaestus
session: {{SESSION}}
lifecycle_phase: hypothesize
spawned_by: null
related: []
memory_refs: []
version: "2.0"
generated: 2025-12-22
last_updated: 2025-12-22T23:16:24
---
# Investigation: {{TITLE}}

@docs/README.md
@docs/epistemic_state.md

<!-- FILE REFERENCE REQUIREMENTS (MUST - Session 171 Learning)

     1. MUST use full @ paths for prior work:
        CORRECT: @docs/work/active/INV-052/SECTION-17-MODULAR-ARCHITECTURE.md
        WRONG:   INV-052, "See INV-052"

     2. MUST read ALL @ referenced files BEFORE starting EXPLORE phase:
        - Read each @path listed at document top
        - For directory references (@docs/work/active/INV-052/), MUST Glob to find all files
        - Document key findings in Prior Work Query section
        - Do NOT proceed to EXPLORE until references are read

     3. MUST Glob referenced directories:
        @docs/work/active/INV-052/ → Glob("docs/work/active/INV-052/**/*.md")
        Then read key files (SECTION-*.md, WORK.md, investigations/*.md)

     Rationale: Session 171 wasted ~15% context searching for INV-052 in wrong
     location because agent ignored @ references and guessed file locations.
-->

<!-- TEMPLATE GOVERNANCE (v2.0 - E2-144)

     INVESTIGATION CYCLE: HYPOTHESIZE -> EXPLORE -> CONCLUDE

     SKIP RATIONALE REQUIREMENT:
     If ANY section below is omitted or marked N/A, you MUST provide rationale.

     Format for skipped sections:

     ## [Section Name]

     **SKIPPED:** [One-line rationale explaining why this section doesn't apply]

     Examples:
     - "SKIPPED: Pure discovery, no design outputs needed"
     - "SKIPPED: Single hypothesis, no complex mapping required"
     - "SKIPPED: External research only, no codebase evidence"

     This prevents silent section deletion and ensures conscious decisions.

     SUBAGENT REQUIREMENT (L3):
     For EXPLORE phase, you MUST invoke investigation-agent subagent:
     Task(prompt='EXPLORE: {hypothesis}', subagent_type='investigation-agent')

     Rationale: Session 101 proved L2 ("RECOMMENDED") guidance is ignored ~20% of time.
     L3 enforcement ensures structured evidence gathering.
-->

---

## Discovery Protocol (RFC 2119)

| Requirement | Level | Action |
|-------------|-------|--------|
| Query memory first | SHOULD | Search for prior investigations on topic before starting |
| Document hypotheses | SHOULD | State what you expect to find before exploring |
| Use investigation-agent | MUST | Delegate EXPLORE phase to subagent for structured evidence |
| Capture findings | MUST | Fill Findings section with evidence, not assumptions |

---

## Context

<!-- HYPOTHESIZE PHASE: Describe background before exploring -->

**Trigger:** [What event, observation, or question initiated this investigation?]

**Problem Statement:** [One sentence: What gap, issue, or unknown are we investigating?]

**Prior Observations:**
- [Observation 1 that led to this investigation]
- [Observation 2]

---

## Prior Work Query

<!-- MUST query memory before starting investigation -->

**Memory Query:** `memory_search_with_experience` with query: "[investigation topic keywords]"

| Concept ID | Content Summary | Relevance |
|------------|-----------------|-----------|
| [ID] | [What was learned] | [How it applies] |

**Prior Investigations:**
- [ ] Searched for related INV-* documents
- [ ] No prior work found / Found: [INV-xxx]

---

## Objective

<!-- One clear question this investigation will answer -->

[What specific question will be answered when this investigation is complete?]

---

## Scope

### In Scope
- [Specific thing to investigate 1]
- [Specific thing to investigate 2]

### Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

### Scope Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Files to examine | [N] | Glob pattern or list |
| Hypotheses to test | [N] | Listed below |
| Expected evidence sources | [N] | Codebase / Memory / External |
| Estimated complexity | [Low/Med/High] | Based on scope |

---

## Hypotheses

<!-- HYPOTHESIZE PHASE: Define BEFORE exploring
     Each hypothesis MUST have confidence and test method -->

| # | Hypothesis | Confidence | Test Method | Priority |
|---|------------|------------|-------------|----------|
| **H1** | [Primary hypothesis] | [High/Med/Low] | [How to verify - specific files, queries, or experiments] | 1st |
| **H2** | [Secondary hypothesis] | [High/Med/Low] | [How to verify] | 2nd |
| **H3** | [Alternative hypothesis] | [High/Med/Low] | [How to verify] | 3rd |

---

## Exploration Plan

<!-- EXPLORE PHASE: Execute these steps in order
     MUST invoke investigation-agent for each major step -->

### Phase 1: Evidence Gathering
1. [ ] Query memory for prior learnings on topic
2. [ ] Search codebase for relevant patterns (Grep/Glob)
3. [ ] Read identified files and document findings

### Phase 2: Hypothesis Testing
4. [ ] Test H1: [Specific actions]
5. [ ] Test H2: [Specific actions]
6. [ ] Test H3: [Specific actions]

### Phase 3: Synthesis
7. [ ] Compile evidence table
8. [ ] Determine verdict for each hypothesis
9. [ ] Identify spawned work items

---

## Evidence Collection

<!-- EXPLORE PHASE: Document ALL evidence with sources
     MUST include file:line references for codebase evidence -->

### Codebase Evidence

| Finding | Source (file:line) | Supports Hypothesis | Notes |
|---------|-------------------|---------------------|-------|
| [What was found] | `path/file.py:123-145` | H1/H2/H3 | [Context] |

### Memory Evidence

| Concept ID | Content | Supports Hypothesis | Notes |
|------------|---------|---------------------|-------|
| [ID] | [Summary] | H1/H2/H3 | [How it applies] |

### External Evidence (if applicable)

| Source | Finding | Supports Hypothesis | URL/Reference |
|--------|---------|---------------------|---------------|
| [Doc/Article] | [Summary] | H1/H2/H3 | [Link] |

---

## Findings

<!-- EXPLORE PHASE: Document findings as discovered
     CONCLUDE PHASE: Synthesize into coherent narrative

     DoD: This section MUST have actual content, not placeholder text -->

### Hypothesis Verdicts

| Hypothesis | Verdict | Key Evidence | Confidence |
|------------|---------|--------------|------------|
| H1 | Confirmed/Refuted/Inconclusive | [1-2 sentence summary with source] | [High/Med/Low] |
| H2 | Confirmed/Refuted/Inconclusive | [1-2 sentence summary with source] | [High/Med/Low] |
| H3 | Confirmed/Refuted/Inconclusive | [1-2 sentence summary with source] | [High/Med/Low] |

### Detailed Findings

#### [Finding 1 Title]

**Evidence:**
```
[Code snippet, query result, or observation with source reference]
```

**Analysis:** [What this evidence means]

**Implication:** [What action or design this suggests]

#### [Finding 2 Title]

**Evidence:**
```
[Code snippet, query result, or observation]
```

**Analysis:** [What this evidence means]

**Implication:** [What action or design this suggests]

---

## Design Outputs

<!-- If investigation produces architectural designs, document them here
     SKIP this section if investigation is pure discovery with no design outputs -->

### Schema Design (if applicable)

```yaml
# [Name of schema]
field_name: type
  description: [What this field does]
```

### Mapping Table (if applicable)

| Source | Target | Relationship | Notes |
|--------|--------|--------------|-------|
| [A] | [B] | [How A relates to B] | |

### Mechanism Design (if applicable)

```
TRIGGER: [What initiates the mechanism]

ACTION:
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]

OUTCOME: [What results from the mechanism]
```

### Key Design Decisions

| Decision | Choice | Rationale (WHY) |
|----------|--------|-----------------|
| [Decision point] | [What was chosen] | [Why this choice - most important part] |

---

## Spawned Work Items

<!-- CONCLUDE PHASE: Create items via /new-* commands
     Each item MUST have spawned_by: {this_investigation_id}

     DoD: This section MUST have entries, not "None yet"
     If truly no spawns, explain why in rationale -->

### Immediate (Can implement now)

- [ ] **{ID}: {Title}**
  - Description: [What this item does]
  - Fixes: [What problem from investigation this addresses]
  - Spawned via: `/new-plan {ID} "{Title}"`

### Future (Requires more work first)

- [ ] **{ID}: {Title}**
  - Description: [What this item does]
  - Blocked by: [What must happen first]

### Not Spawned Rationale (if no items)

**RATIONALE:** [Why this investigation produced no spawned items - rare, explain thoroughly]

---

## Session Progress Tracker

<!-- Track progress across sessions for multi-session investigations -->

| Session | Date | Phase | Progress | Notes |
|---------|------|-------|----------|-------|
| {{SESSION}} | {{DATE}} | HYPOTHESIZE | Started | Initial context and hypotheses |
| - | - | - | - | No additional sessions yet |

---

## Ground Truth Verification

<!-- CONCLUDE PHASE: Verify findings before closing
     MUST read/check each item, not just claim -->

| Item to Verify | Expected State | Verified | Notes |
|----------------|---------------|----------|-------|
| Hypothesis verdicts documented | All H1-HN have verdict | [ ] | |
| Evidence has sources | All findings have file:line or concept ID | [ ] | |
| Spawned items created | Items exist in backlog or via /new-* | [ ] | |
| Memory stored | ingester_ingest called, memory_refs populated | [ ] | |

**Binary Verification (Yes/No):**

| Question | Answer | If NO, explain |
|----------|--------|----------------|
| Did you invoke investigation-agent for EXPLORE phase? | [Yes/No] | |
| Are all evidence sources cited with file:line or concept ID? | [Yes/No] | |
| Were all hypotheses tested with documented verdicts? | [Yes/No] | |
| Are spawned items created (not just listed)? | [Yes/No] | |
| Is memory_refs populated in frontmatter? | [Yes/No] | |

---

## Closure Checklist

<!-- CONCLUDE PHASE: Complete ALL items before /close -->

### Required (MUST complete)
- [ ] **Findings synthesized** - Answer to objective documented in Findings section
- [ ] **Evidence sourced** - All findings have file:line or concept ID citations
- [ ] **Hypotheses resolved** - All hypotheses have Confirmed/Refuted/Inconclusive verdict
- [ ] **Spawned items created** - Via /new-* commands with `spawned_by` field (or rationale if none)
- [ ] **Memory stored** - `ingester_ingest` called with findings summary
- [ ] **memory_refs populated** - Frontmatter updated with concept IDs
- [ ] **lifecycle_phase updated** - Set to `conclude`
- [ ] **Ground Truth Verification complete** - All items checked above

### Optional
- [ ] Design outputs documented (if applicable)
- [ ] Session progress updated (if multi-session)

---

## References

- [Spawned by: Session/Investigation/Work item that triggered this]
- [Related investigation 1]
- [Related ADR or spec]

---
