---
name: writing-prds-from-charters
description: Use when you have an approved charter and need to produce a detailed PRD that engineering and design can execute.
---

# Writing PRDs from Charters

## Overview

Converts an approved quarterly charter into a detailed Product Requirements Document. Produces executable specs with requirements, edge cases, telemetry, rollout plan, and GTM notes.

## When to Use

- Charter approved, ready to spec
- Eng/design needs detailed requirements
- Starting sprint planning for a charter
- Need to document edge cases and telemetry

## Output Formats

By default, produces full PRD. Use `--format` for audience-specific outputs:

| Format | Command | Audience | Content |
|--------|---------|----------|---------|
| `full` (default) | `writing-prds-from-charters` | Full team | Complete PRD with all sections |
| `exec` | `writing-prds-from-charters --format exec` | Executives | 1-page: problem, metrics, timeline, risks |
| `eng` | `writing-prds-from-charters --format eng` | Engineering | Requirements, data model, edge cases, telemetry only |

### Exec Format (`--format exec`)

Produces a 1-page executive summary:

```markdown
# PRD Summary: [Feature Name]

## At a Glance
| Field | Value |
|-------|-------|
| Problem | [1 sentence] |
| Target Users | [Segment] |
| Success Metric | [KPI + target] |
| Target Release | Q[X] YYYY |

## Key Risks
| Risk | Mitigation |
|------|------------|
| [Top 2-3 risks] |

## Timeline
| Milestone | Date |
|-----------|------|
| Alpha | [Date] |
| GA | [Date] |

## Decisions Needed
[Any leadership decisions required]
```

### Eng Format (`--format eng`)

Produces engineering-focused spec:

```markdown
# Engineering Spec: [Feature Name]

## Functional Requirements
[FR-1 through FR-N with acceptance criteria]

## Non-Functional Requirements
[Performance, security, accessibility]

## Data Model
[Entities, fields, types, constraints]

## Edge Cases & Error Handling
[Full table of scenarios]

## Telemetry
[Events, dimensions, dashboards]

## Feature Flags
[Flags and rollout controls]

## Technical Open Questions
[Questions that need eng input]
```

## Core Pattern

**Step 1: Gather Context**

Follow protocol in `.claude/rules/pm-core/context-gathering.md`:

1. **Detect available inputs** in outputs/ and inputs/:
   - `outputs/roadmap/Qx-YYYY-charters.md` - Quarterly charters
   - `outputs/insights/voc-synthesis-*.md` - VOC synthesis
   - `outputs/truth_base/truth-base.md` - Product understanding
   - `inputs/knowledge_base/` - Knowledge base articles
   - `inputs/voc/*.md` - Raw customer feedback

2. **Present options to user** via AskUserQuestion:
   - List each relevant charter/VOC/truth base file found
   - Include option: "Point me to another document"
   - Include option: "Describe what you need"

3. **Read `.beads/insights.jsonl`** for relevant learnings from past PRDs

4. **Proceed with selected context**

**If user skips/describes:** Use their description as context, mark claims as Assumption in Claims Ledger.

**Step 2: Validate Charter Completeness**

Check the charter has:
- [ ] Clear problem statement with evidence
- [ ] Defined target users
- [ ] Success metrics
- [ ] Scope boundaries

**If missing, ask user to update charter first.**

**Step 3: Expand Requirements**

For each scope item, define:

| Requirement Type | Content |
|------------------|---------|
| **Functional** | What the system must do (behavior) |
| **Non-Functional** | Performance, security, accessibility |
| **Edge Cases** | What happens when things go wrong |
| **Data** | What's stored, what's computed |

Use format: "The system SHALL [verb] [object] when [condition]"

**Step 4: Define Telemetry**

For each success metric in the charter:
- What events to track
- What dimensions to capture
- Where data is stored

**Step 5: Plan Rollout**

| Phase | Audience | Duration | Success Gate |
|-------|----------|----------|--------------|
| Alpha | Internal | 1 week | No P0 bugs |
| Beta | 10% users | 2 weeks | Metrics stable |
| GA | 100% | - | Success criteria met |

**Step 6: Note GTM Needs**

- Documentation updates needed
- Support training required
- Sales enablement materials
- Customer communication

**Step 7: Generate Output**

Write to `outputs/delivery/prds/[charter-name]-prd.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: writing-prds-from-charters
sources:
  - outputs/roadmap/Qx-YYYY-charters.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-*.md (if used)
downstream: []
---

# PRD: [Feature Name]

## Overview
| Field | Value |
|-------|-------|
| Charter | [Link to charter section] |
| Status | Draft / In Review / Approved |
| Author | [Name] |
| Last Updated | YYYY-MM-DD |
| Target Release | Q[X] YYYY |

## Problem Statement
[From charter, with evidence citations]

## Target Users
[From charter]

## Success Metrics
| Metric | Current | Target | Tracking Method |
|--------|---------|--------|-----------------|
| [KPI] | [X] | [Y] | [Event/Dashboard] |

---

## Functional Requirements

### FR-1: [Requirement Name]
**Description:** The system SHALL [verb] [object] when [condition].

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

**Priority:** Must / Should / Could

### FR-2: [Requirement Name]
...

---

## Non-Functional Requirements

### NFR-1: Performance
- [Latency requirement]
- [Throughput requirement]

### NFR-2: Security
- [Auth requirements]
- [Data handling]

### NFR-3: Accessibility
- [WCAG level]
- [Specific requirements]

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior | Error Message |
|----------|-------------------|---------------|
| [User does X when Y] | [System does Z] | [Message shown] |
| [Data is invalid] | [Validation fails] | [Error text] |
| [Service unavailable] | [Graceful degradation] | [Fallback behavior] |

---

## Data Model

### New/Modified Entities
| Entity | Field | Type | Notes |
|--------|-------|------|-------|
| [Entity] | [field] | [type] | [constraints] |

### Data Flow
[Brief description or diagram reference]

---

## Telemetry & Analytics

### Events to Track
| Event | Trigger | Dimensions | Purpose |
|-------|---------|------------|---------|
| [event_name] | [when fired] | [user_id, action, etc.] | [what it measures] |

### Dashboards Needed
- [Dashboard 1]: [What it shows]

---

## Rollout Plan

| Phase | Audience | Duration | Entry Criteria | Exit Criteria |
|-------|----------|----------|----------------|---------------|
| Alpha | Internal QA | 1 week | Build complete | No P0/P1 bugs |
| Beta | 10% of [segment] | 2 weeks | Alpha exit | Metrics stable |
| GA | All users | - | Beta exit | Success metrics met |

### Feature Flags
| Flag | Default | Description |
|------|---------|-------------|
| [flag_name] | off | [What it controls] |

---

## GTM Requirements

### Documentation
- [ ] KB article: [topic]
- [ ] In-app help: [location]

### Support Training
- [ ] [Training topic]
- [ ] [Escalation path]

### Sales Enablement
- [ ] [Material needed]

### Customer Communication
- [ ] [Release notes]
- [ ] [In-app announcement]

---

## Open Questions
| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | [Question] | [Name/TBD] | [Date] |

## Risks
| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| [From charter + new] | H/M/L | [Action] | Open/Mitigated |

## Out of Scope
[From charter]

---

## Appendix

### User Stories
- As a [persona], I want [action], so that [benefit].

### Wireframes / Mockups
[Links or descriptions]

### Technical Notes
[Any implementation guidance for eng]

---

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Requirement based on X] | Evidence | [VOC/charter] |
```

**Step 8: Copy to History & Update Tracker**

- Run `pm-os mirror --quiet` to copy to `history/writing-prds-from-charters/[name]-prd-YYYY-MM-DD.md`
- Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md`

**Step 9: Post-Skill Reflection (MANDATORY)**

Follow protocol in `.claude/rules/pm-core/post-skill-reflection.md`:

1. **Extract key learnings** (3-5 insights):
   - What requirements were clearest vs most ambiguous?
   - What edge cases were hardest to specify?
   - How well did telemetry map to success metrics?
   - What rollout challenges were identified?
   - Connections to past PRDs?

2. **Create learning entry:**
   - Write to `history/learnings/YYYY-MM-DD-writing-prds-from-charters.md`
   - Use template from post-skill-reflection rule

3. **Create insight beads:**
   - For each significant, reusable insight
   - Append to `.beads/insights.jsonl`
   - Types: insight (new learning), pattern (recurring theme), question (raised)

4. **Request output rating:**
   ```
   Rate this PRD (1-5, or 'skip'):
   1 - Needs major revision
   2 - Below expectations
   3 - Meets expectations
   4 - Exceeds expectations
   5 - Outstanding, exactly what I needed
   ```
   - If rated: Create output-rating bead
   - Capture any qualitative feedback

5. **Detect decisions:**
   - PRD creation = high confidence decision
   - Auto-log: "Converted charter [name] to PRD with [N] requirements"
   - Write to `outputs/decisions/YYYY-MM-DD-prd-[charter-name].md`

6. **Report completion:**
   ```
   ✅ PRD complete → outputs/delivery/prds/[name]-prd.md
      Mirrored to history/writing-prds-from-charters/[name]-prd-YYYY-MM-DD.md

   📝 Captured learnings: [N] insights, [N] beads → history/learnings/YYYY-MM-DD-writing-prds-from-charters.md
   📋 Logged decision: PRD for [charter name] → outputs/decisions/

   Rate this PRD (1-5, or 'skip'): [prompt for rating]
   ```

## Quick Reference

| Section | Purpose |
|---------|---------|
| Functional Reqs | What system does |
| Non-Functional | How well it does it |
| Edge Cases | What happens when wrong |
| Telemetry | How we measure success |
| Rollout | How we ship safely |
| GTM | What else needs to happen |

## Common Mistakes

- **Vague requirements:** "Improve the UX" → "System SHALL display error within 100ms"
- **Missing edge cases:** "User submits form" → What if invalid? Empty? Duplicate?
- **No telemetry:** "We'll know it works" → Specific events and dimensions
- **No rollout plan:** "Just ship it" → Alpha/Beta/GA phases
- **Forgetting GTM:** Code ships, docs don't → List all GTM needs
- **Disconnected from charter:** PRD scope creep → Trace back to charter

## Verification Checklist

- [ ] Charter loaded and validated
- [ ] All scope items have requirements
- [ ] Requirements are testable (SHALL + acceptance criteria)
- [ ] Edge cases documented
- [ ] Telemetry maps to success metrics
- [ ] Rollout plan has phases and gates
- [ ] GTM needs listed
- [ ] Open questions have owners
- [ ] Risks from charter carried over
- [ ] Out of scope from charter included
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Goal-Backward Verification

**Before marking complete, run goal-backward check** (see `.claude/rules/pm-core/goal-backward-verification.md`):

**Goal:** Engineering can build the right thing without coming back with questions.

**Observable truths (must all pass):**
- [ ] Engineer can start work without asking "what do you mean by X?"
- [ ] Edge cases cover realistic failure scenarios
- [ ] Success metrics have measurement plan (not just targets)
- [ ] Rollout plan has exit criteria, not just entry

**On failure:** Do not mark complete. Note which checks failed in Open Questions section.

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Requirement X] | Evidence | [Charter/VOC reference] |
| [Performance target] | Assumption | [Industry standard / "Need benchmark"] |
| [Rollout duration] | Assumption | [Team estimate] |
