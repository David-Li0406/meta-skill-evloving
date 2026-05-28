---
name: generating-quarterly-charters
description: Use when planning a quarter and need to convert signals (truth base, VOC, KTLO) into 3-5 strategic charters with clear problem statements and success metrics.
---

# Generating Quarterly Charters

## Overview

Converts accumulated PM signals into a coherent quarterly plan. Produces 3-5 charters that define strategic bets with clear problems, target users, success metrics, and risks.

## When to Use

- Quarterly planning cycle starting
- Need to present roadmap to leadership
- Have accumulated insights and need to prioritize
- Want structured format for eng/design alignment

## Output Formats

By default, produces full charters. Use `--format` for audience-specific outputs:

| Format | Command | Audience | Content |
|--------|---------|----------|---------|
| `full` (default) | `generating-quarterly-charters` | Planning team | Complete charter with all sections |
| `exec` | `generating-quarterly-charters --format exec` | Executives | 1-page summary: problems, metrics, risks, timeline |
| `eng` | `generating-quarterly-charters --format eng` | Engineering | Scope, dependencies, technical constraints only |

### Exec Format (`--format exec`)

Produces a 1-page executive summary:

```markdown
# Q[X] [YYYY] Quarterly Plan - Executive Summary

## Strategic Bets
| Charter | Problem | Success Metric | Confidence |
|---------|---------|----------------|------------|
| [Name] | [1-line] | [KPI + target] | High/Med/Low |

## Key Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Top 3 risks across all charters] |

## Resource Asks
[Any leadership decisions or resources needed]

## Timeline
[High-level milestones only]
```

### Eng Format (`--format eng`)

Produces engineering-focused summary:

```markdown
# Q[X] [YYYY] Engineering Context

## Charter Scope Summary
| Charter | In Scope | Out of Scope | Dependencies |
|---------|----------|--------------|--------------|
| [Name] | [Bullet list] | [Bullet list] | [Teams/systems] |

## Cross-Charter Dependencies
[Shared dependencies, sequencing constraints]

## Technical Risks
| Risk | Charter | Mitigation |
|------|---------|------------|
| [Technical risks only] |

## Open Technical Questions
[Questions that need eng input]
```

## Core Pattern

**Step 1: Gather Context**

Follow protocol in `.claude/rules/pm-core/context-gathering.md`:

1. **Detect available inputs** in outputs/ and inputs/:
   - `outputs/truth_base/truth-base.md` - Product understanding
   - `outputs/insights/voc-synthesis-*.md` - Customer signals
   - `outputs/ktlo/ktlo-triage-*.md` - Operational burden
   - `outputs/insights/kb-gaps-*.md` - Documentation gaps
   - `inputs/voc/*.md` - Raw interview notes
   - `inputs/context/*.md` - COMPASS context files

2. **Present options to user** via AskUserQuestion:
   - List each relevant file found with brief description
   - Include option: "Point me to another document"
   - Include option: "Describe what you need"

3. **Read `.beads/insights.jsonl`** for relevant learnings from past charters

4. **Proceed with selected context**

**If user skips/describes:** Use their description as context, mark claims as Assumption in Claims Ledger.

**Step 2: Synthesize Signals**

Extract from each source:
- **Truth base:** Current roadmap themes, constraints, open questions
- **VOC:** Top themes, opportunities, customer pain
- **KTLO:** Critical issues, patterns, tech debt
- **KB gaps:** User struggle points, AI opportunities

**Step 3: Identify Charter Candidates**

Look for convergence:
- Pain point mentioned in VOC + KTLO ticket cluster = strong signal
- Roadmap theme + customer evidence = validated bet
- Gap in truth base + customer complaints = opportunity

Aim for 5-7 candidates, then narrow to 3-5.

**Step 4: Draft Each Charter**

For each charter:

| Section | Content | Source Required |
|---------|---------|-----------------|
| Problem | Specific user pain | VOC/KTLO evidence |
| Target Users | Who feels this pain | Explicit segment |
| Success Metrics | How we'll know it worked | Measurable KPIs |
| Scope | What's in | Clear boundaries |
| Non-Scope | What's out | Explicit exclusions |
| Dependencies | What we need from others | Named teams/systems |
| Risks | What could go wrong | Mitigations |
| Why Now | Why this quarter | Business/strategic reason |

**Step 5: Strategic Reasoning (Meta-Prompt)**

Before generating the main charter document, create a "Strategic Reasoning" section following `.claude/rules/pm-core/meta-prompt-reasoning.md`:

- **Problem & Goals:** What makes a high-quality charter? (Stakeholders can explain bets, engineering can scope work)
- **Context & Constraints:** Available evidence (VOC, KTLO, truth base) and resource constraints
- **Options Evaluated:** What charter candidates were considered? (aim for 5-7 initial, narrow to 3-5)
- **Selection Rationale:** Why these 3-5 bets beat alternatives (show evidence scoring)

This helps stakeholders understand why certain initiatives made the cut and others didn't.

**Step 6: Generate Output**

Write to `outputs/roadmap/Qx-YYYY-charters.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: generating-quarterly-charters
sources:
  - outputs/truth_base/truth-base.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-*.md (modified: YYYY-MM-DD)
  - outputs/ktlo/ktlo-triage-*.md (modified: YYYY-MM-DD)
downstream:
  - outputs/delivery/prds/*.md
---

# Q[X] [YYYY] Charters

## Strategic Reasoning

### Problem & Goals
**Problem:** Choose [N] strategic bets from [M] possible initiatives for Q[X], maximizing value with constrained resources.
**Success Criteria:** [What makes these charters high-quality]

### Context & Constraints
**Available Evidence:**
- VOC: [Key findings from synthesis]
- KTLO: [Key patterns from triage]
- Truth base: [Relevant context]

**Constraints:**
- [Resource/capacity limitations]
- [Timeline constraints]

**Gaps:**
- [What we don't know that matters]

### Charter Candidates Evaluated

| Candidate | VOC Signal | KTLO Signal | Evidence Score | Decision |
|-----------|------------|-------------|----------------|----------|
| [Initiative A] | [High/Med/Low] | [High/Med/Low] | High/Med/Low | ✅ Charter 1 |
| [Initiative B] | [High/Med/Low] | [High/Med/Low] | High/Med/Low | ✅ Charter 2 |
| [Initiative C] | [High/Med/Low] | [High/Med/Low] | High/Med/Low | ✅ Charter 3 |
| [Initiative D] | [High/Med/Low] | [High/Med/Low] | High/Med/Low | ❌ Deferred |
| [Initiative E] | [High/Med/Low] | [High/Med/Low] | High/Med/Low | ❌ Rejected |

### Selection Rationale
**Chosen:** [List selected charters]

**Why chosen beat alternatives:**
1. [Reason 1 with evidence]
2. [Reason 2 with evidence]
3. [Reason 3 with evidence]

**Deferred to next quarter:** [List with brief reason]

**What would change these priorities:**
- [Condition that would shift charter priorities]

---

## Executive Summary
[3-5 sentences: What are we betting on this quarter? Why?]

## Charter Overview

| # | Charter | Problem | Target | Confidence |
|---|---------|---------|--------|------------|
| 1 | [Name] | [1-line problem] | [Segment] | High/Med/Low |
| 2 | [Name] | [1-line problem] | [Segment] | High/Med/Low |
| ... | ... | ... | ... | ... |

---

## Charter 1: [Name]

### Problem Statement
[2-3 sentences describing the user pain. Must cite evidence.]

**Evidence:**
- VOC: [N sources mention this]
- KTLO: [N tickets related]
- Quote: "[verbatim]" — [source]

### Target Users
| Segment | Description | Why Them |
|---------|-------------|----------|
| [Segment] | [Description] | [Reason] |

### Success Criteria

| Criterion | Baseline | Target | Measurement Source | Owner |
|-----------|----------|--------|-------------------|-------|
| [User outcome] | [Current] | [Goal] | [Dashboard/Survey/etc] | [Name/TBD] |
| [Business outcome] | [Current] | [Goal] | [Data source] | [Name/TBD] |
| [Technical outcome] | [Current] | [Goal] | [System metrics] | [Name/TBD] |

**Verification Plan:**
- [ ] Baseline measured before work starts (Date: ___)
- [ ] Mid-point check scheduled (Date: ___)
- [ ] Final measurement planned (Date: ___)

### Scope
**In scope:**
- [Feature/capability 1]
- [Feature/capability 2]

**Out of scope:**
- [Explicitly excluded item]

### Dependencies
| Dependency | Team/System | Status |
|------------|-------------|--------|
| [What we need] | [Who owns it] | [Known/Unknown] |

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | High/Med/Low | [Action] |

### Why Now
[1-2 sentences: business context, competitive pressure, customer urgency]

---

## Charter 2: [Name]
[Same structure]

---

## What We're NOT Doing This Quarter
| Item | Reason |
|------|--------|
| [Deprioritized item] | [Why not now] |

## Open Questions for Leadership
1. [Decision needed]
2. [Resource question]

## Sources Used
- [file paths with dates]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Problem affects X users] | Evidence | [VOC/KTLO file] |
| [Metric baseline is Y] | Evidence/Unknown | [data source or "Need data"] |
```

**Step 6: Copy to History & Update Tracker**

- Run `pm-os mirror --quiet` to copy to `history/generating-quarterly-charters/Qx-YYYY-charters-YYYY-MM-DD.md`
- Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md`

**Step 7: Post-Skill Reflection (MANDATORY)**

Follow protocol in `.claude/rules/pm-core/post-skill-reflection.md`:

1. **Extract key learnings** (3-5 insights):
   - What charter candidates were evaluated vs selected?
   - What patterns emerged in evidence strength (VOC+KTLO)?
   - What made scope/non-scope clear vs ambiguous?
   - How did risk identification go?
   - Connections to past charters?

2. **Create learning entry:**
   - Write to `history/learnings/YYYY-MM-DD-generating-quarterly-charters.md`
   - Use template from post-skill-reflection rule

3. **Create insight beads:**
   - For each significant, reusable insight
   - Append to `.beads/insights.jsonl`
   - Types: insight (new learning), pattern (recurring theme), question (raised)

4. **Request output rating:**
   ```
   Rate this charter (1-5, or 'skip'):
   1 - Needs major revision
   2 - Below expectations
   3 - Meets expectations
   4 - Exceeds expectations
   5 - Outstanding, exactly what I needed
   ```
   - If rated: Create output-rating bead
   - Capture any qualitative feedback

5. **Detect decisions:**
   - Charter creation = high confidence decision
   - Auto-log: "Prioritized [N] bets: [list] over [alternatives]"
   - Write to `outputs/decisions/YYYY-MM-DD-qN-charter-prioritization.md`

6. **Report completion:**
   ```
   ✅ Quarterly charters complete → outputs/roadmap/Qx-YYYY-charters.md
      Mirrored to history/generating-quarterly-charters/Qx-YYYY-charters-YYYY-MM-DD.md

   📝 Captured learnings: [N] insights, [N] beads → history/learnings/YYYY-MM-DD-generating-quarterly-charters.md
   📋 Logged decision: Q[N] charter prioritization → outputs/decisions/

   Rate this charter (1-5, or 'skip'): [prompt for rating]
   ```

## Quick Reference

| Input | What It Provides |
|-------|------------------|
| Truth base | Context, constraints, themes |
| VOC | Customer pain, opportunities |
| KTLO | Operational reality, patterns |
| KB gaps | User struggles, AI opps |

## Common Mistakes

- **No evidence:** "Users want X" → Must cite VOC/KTLO source
- **Vague metrics:** "Improve satisfaction" → Specific: "NPS +10 points"
- **Too many charters:** 8 charters = no focus → Max 5
- **Missing scope:** "Build feature X" → What's in AND out
- **Ignoring risks:** "This will be easy" → Every charter has risks
- **Stale inputs:** Using 3-month-old VOC → Check source dates

## Verification Checklist

- [ ] All upstream outputs read (truth base, VOC, KTLO, KB)
- [ ] Source dates checked (not stale)
- [ ] 3-5 charters (not more)
- [ ] Every problem has VOC/KTLO evidence
- [ ] Success metrics are measurable
- [ ] Scope and non-scope explicit
- [ ] Dependencies named
- [ ] Risks documented with mitigations
- [ ] "What we're NOT doing" section included
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Goal-Backward Verification

**Before marking complete, run goal-backward check** (see `.claude/rules/pm-core/goal-backward-verification.md`):

**Goal:** Stakeholders can explain the quarter's bets and why they matter.

**Observable truths (must all pass):**
- [ ] Stakeholder can explain the quarter's bets in 2 minutes
- [ ] Each bet has clear "we'll know it worked if..." statement
- [ ] Risks section would survive "what could kill this?" challenge
- [ ] Dependencies name actual teams (not all "TBD")

**On failure:** Do not mark complete. Note which checks failed in Open Questions section.

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Problem exists] | Evidence | [VOC/KTLO citations] |
| [Target segment] | Evidence | [explicit in sources] |
| [Metric baseline] | Evidence/Unknown | [data or "Need to measure"] |
