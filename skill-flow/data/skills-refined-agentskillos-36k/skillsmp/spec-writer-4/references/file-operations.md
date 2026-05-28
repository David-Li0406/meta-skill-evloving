# File Update Specifications

This section provides exhaustive instructions on when to create, read, update, and archive each file and section. Treat these as invariant rules.

---

## discovery/SPEC.md

**Purpose**: The progressive deliverable. The source of truth for completed work.

**Create**: At session start if it doesn't exist. Initialize with template headers, all sections empty except metadata.

### Header Metadata
```markdown
**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Last Updated**: [DATE]
**Status**: In Progress | Ready for Review | Complete
```

| Field | Update When |
|-------|-------------|
| Feature Branch | Once, when user provides or you agree on naming convention |
| Created | Once, at file creation |
| Last Updated | Every time ANY content in SPEC.md changes |
| Status | When: (1) First story graduates → "In Progress", (2) All stories complete + user confirms → "Ready for Review", (3) User signs off → "Complete" |

### Problem Statement Section
```markdown
## Problem Statement
[One paragraph describing the core problem]
```

| Action | Trigger |
|--------|---------|
| Create draft | End of Phase 1, when problem understanding is stable |
| Graduate to SPEC | When user confirms problem statement is accurate |
| Update | Only if fundamental understanding of problem changes (rare - log to REVISIONS.md) |

**Do NOT update** for minor wording tweaks - only for substantive changes to problem understanding.

### Personas Section
```markdown
## Personas
| Persona | Description | Primary Goals |
```

| Action | Trigger |
|--------|---------|
| Add persona | When persona is confirmed during Phase 1/2 and at least one story references them |
| Update persona | When story development reveals new information about persona goals/context |
| Remove persona | Never remove - mark as deprecated if no longer relevant |

**Rule**: A persona must be referenced by at least one story to be in SPEC.md. Personas still being explored stay in STATE.md.

### User Scenarios & Testing Section

This is the core of the spec. Each story is a subsection.

#### Adding a New Story

| Trigger | Action |
|---------|--------|
| Story graduates from STATE.md | Write full story to SPEC.md |

**Graduation checklist** (ALL must be true):
- [ ] 100% confidence on story scope
- [ ] All 🔴 blocking questions for this story resolved
- [ ] Every acceptance scenario is specific and testable
- [ ] Edge cases identified with handling defined
- [ ] At least one FR-XXX requirement extractable
- [ ] Success criteria measurable
- [ ] User has confirmed story is complete

**Story format on graduation**:
```markdown
### User Story [N] - [Title] (Priority: P[X])

**Revision**: v1.0

[Full description]

**Why this priority**: [Rationale]

**Independent Test**: [How to test in isolation]

**Acceptance Scenarios**:
1. **Given** [specific], **When** [specific], **Then** [specific]

<details>
<summary>Supporting Decisions</summary>
- **D[N]**: [One-line] — *[date]*
</details>

<details>
<summary>Research References</summary>
- **R[N]**: [Topic] — *[date]*
</details>
```

#### Updating an Existing Story (Revision)

| Trigger | Action |
|---------|--------|
| New question answer affects graduated story | Flag in STATE.md Watching section |
| Research reveals gap in graduated story | Flag in STATE.md Watching section |
| User requests change to graduated story | Discuss scope of change |
| Confirmed revision needed | Update SPEC.md + log to REVISIONS.md |

**Revision protocol**:
1. Identify specific change needed
2. Confirm with user: "Story [X] needs revision: [what's changing]. Approve?"
3. If approved:
   - Update story content in SPEC.md
   - Increment revision: v1.0 → v1.1
   - Add entry to archive/REVISIONS.md
   - Update any affected FR-XXX, EC-XXX, SC-XXX entries
   - Add new decision reference if revision was driven by a decision

**Revision types**:
| Type | Example | Version Bump |
|------|---------|--------------|
| Additive | New acceptance scenario | v1.0 → v1.1 |
| Modificative | Changed scenario wording | v1.0 → v1.1 |
| Structural | Story split into two | v1.0 → v2.0 (major) |

#### Marking Story In-Progress (Placeholder)

When a story exists in the backlog but isn't graduated yet:
```markdown
### 🔄 User Story [N] - [Title] (Priority: P[X]) — IN PROGRESS

*This story is under development. See `discovery/STATE.md` for current working state.*

**Emerging Shape**: [1-2 sentences on current direction]
```

| Action | Trigger |
|--------|---------|
| Add placeholder | When story is crystallized (Phase 2) but not yet developed |
| Update "Emerging Shape" | Each iteration where story understanding improves |
| Replace with full story | When story graduates |

### Edge Cases Section
```markdown
## Edge Cases
| ID | Scenario | Handling | Stories Affected |
```

| Action | Trigger |
|--------|---------|
| Add edge case | When story graduates AND edge case is confirmed |
| Update edge case | When revision to story changes edge case handling |
| Add story reference | When existing edge case is found to affect additional story |

**Rules**:
- Edge cases only enter SPEC.md when their handling is CONFIRMED
- Draft edge cases stay in STATE.md under the story
- ID format: EC-001, EC-002, etc. (globally unique)
- Always reference which stories are affected

### Requirements Section
```markdown
## Requirements
### Functional Requirements
| ID | Requirement | Stories | Confidence |
```

| Action | Trigger |
|--------|---------|
| Add requirement (Confirmed) | Story graduates AND requirement is firm |
| Add requirement (Draft) | Story is in-progress but requirement is likely stable |
| Update requirement | Decision changes requirement wording |
| Change confidence | Draft → Confirmed when story graduates |
| Add story reference | When requirement found to affect additional story |

**Rules**:
- FR-XXX IDs are globally unique, never reused
- Requirements can be added as 🔄 Draft before story graduates IF high confidence
- Always track which stories drove the requirement
- Cross-cutting requirements reference multiple stories

#### Key Entities Subsection
```markdown
### Key Entities
- **[Entity]**: [Description, attributes, relationships]
```

| Action | Trigger |
|--------|---------|
| Add entity | When entity is identified and confirmed across stories |
| Update entity | When new attributes or relationships discovered |

**Rules**:
- Entities appear once, not per-story
- Add entity when it's referenced by acceptance scenarios
- Keep descriptions implementation-agnostic

### Success Criteria Section
```markdown
## Success Criteria
| ID | Criterion | Measurement | Stories |
```

| Action | Trigger |
|--------|---------|
| Add criterion | Story graduates AND criterion is measurable |
| Update criterion | Measurement approach changes or threshold adjusts |

**Rules**:
- Every criterion MUST have a number (not "fast" but "< 200ms")
- SC-XXX IDs globally unique
- Reference which stories drive each criterion

### Revision History Appendix
```markdown
## Appendix: Story Revision History
| Date | Story | Change | Reason |
```

| Action | Trigger |
|--------|---------|
| Add row | Any time a graduated story is modified |

**Rules**:
- This is a summary table only
- Full details go in archive/REVISIONS.md
- One row per revision, link to REV-XXX ID

---

## discovery/STATE.md

**Purpose**: Working memory for in-flight discovery. Should remain bounded.

**Create**: At session start if it doesn't exist.

**Read**: At start of EVERY session.

### Header
```markdown
# Discovery State: [Feature Name]
**Updated**: [timestamp]
**Iteration**: N
**Phase**: [...]
```

| Field | Update When |
|-------|-------------|
| Updated | Every iteration, after processing user answers |
| Iteration | Increment by 1 each Q&A cycle |
| Phase | When transitioning between phases (see phase criteria) |

**Phase transitions**:
| From | To | Trigger |
|------|----|---------|
| Problem Exploration | Story Crystallization | Problem statement confirmed, 2+ proto-stories identified |
| Story Crystallization | Story Development | User confirms initial story backlog |
| Story Development | Refinement | (Ongoing - always in refinement once stories graduate) |
| * | Complete | All stories graduated, no open questions, user confirms |

### Problem Understanding Section
```markdown
## Problem Understanding
### Problem Statement
### Personas
### Current State vs. Desired State
### Constraints
```

| Subsection | Update When |
|------------|-------------|
| Problem Statement | Each Phase 1 iteration until stable, then freeze (graduates to SPEC) |
| Personas | When new persona identified or existing refined |
| Current vs. Desired | When understanding of before/after state changes |
| Constraints | When new constraint discovered or existing clarified |

**Graduation rule**: Once Problem Statement is confirmed and in SPEC.md, remove from STATE.md (keep only: "See SPEC.md")

### Story Landscape Section

#### Status Overview Table
```markdown
| # | Story | Priority | Status | Confidence | Blocked By |
```

| Action | Trigger |
|--------|---------|
| Add row | New story crystallizes (Phase 2) |
| Update Status | Story progresses: ⏳ Queued → 🔄 In Progress → ✅ In SPEC |
| Update Confidence | After each iteration where story questions answered |
| Update Blocked By | When blocking questions change |
| Remove row | Never - completed stories stay as ✅ reference |

**Status values**:
- ⏳ Queued - identified but not active focus
- 🔄 In Progress - currently developing
- ✅ In SPEC - graduated
- 🆕 New - just emerged, needs prioritization
- ⏸️ Blocked - cannot proceed until dependency resolved

#### Story Dependencies
```markdown
### Story Dependencies
[Diagram or description of dependencies]
```

| Action | Trigger |
|--------|---------|
| Add dependency | When story B cannot be fully specified without story A complete |
| Remove dependency | When dependency resolved or found to not exist |
| Update diagram | Any dependency change |

#### Proto-Stories / Emerging Themes
```markdown
### Proto-Stories / Emerging Themes
- [Theme]: [Description]
```

| Action | Trigger |
|--------|---------|
| Add theme | When pattern emerges from Q&A that might be a story |
| Promote to story | When theme crystallizes (move to Status Overview as 🆕) |
| Remove | When theme is rejected or merged into existing story |

**Rules**:
- Proto-stories are informal - no IDs yet
- Must be promoted or rejected by end of Phase 2
- Can re-emerge during Phase 3/4 if new themes found

### Completed Stories Summary
```markdown
## Completed Stories Summary
| # | Story | Priority | Completed | Key Decisions | Revision Risk |
```

| Action | Trigger |
|--------|---------|
| Add row | Story graduates to SPEC.md |
| Update Revision Risk | When Watching item relates to this story |

**Revision Risk values**:
- 🟢 Low - no active questions that might affect this story
- 🟡 Medium - watching Q[N] which may affect
- 🔴 High - known issue, revision likely needed

**Rule**: This is a summary table. Full story content is in SPEC.md only.

### In-Progress Story Detail
```markdown
## In-Progress Story Detail
### Story [N]: [Title] (Priority: P[X])
**One-line**: [As a..., I want..., so that...]
**Current Confidence**: X%
**Working Understanding**: [...]
**Draft Acceptance Scenarios**: [...]
**Blocking Questions**: Q[N], Q[M]
**Clarifying Questions**: [...]
**Draft Edge Cases**: [...]
**Draft Requirements**: [...]
```

| Subsection | Update When |
|------------|-------------|
| One-line | When story is first created, refine until stable |
| Current Confidence | Every iteration (recalculate based on resolved questions) |
| Working Understanding | Every iteration as understanding develops |
| Draft Acceptance Scenarios | When scenarios identified, add confidence per scenario |
| Blocking Questions | When questions added/removed (sync with OPEN_QUESTIONS.md) |
| Clarifying Questions | When questions added/removed |
| Draft Edge Cases | When potential edge cases identified |
| Draft Requirements | When requirements emerge from story |

**Removal trigger**: Remove entire story section when story graduates to SPEC.md.

**Rules**:
- Only 1-2 stories should be "In Progress" at a time (focus!)
- Draft items have confidence levels: High/Medium/Low
- Questions reference OPEN_QUESTIONS.md IDs

### Watching List
```markdown
## Watching List
- **Q45**: [Question] — *If X, Story 2 needs revision*
```

| Action | Trigger |
|--------|---------|
| Add item | When question or finding MIGHT affect graduated story |
| Remove item | When question resolved AND doesn't affect story |
| Trigger revision | When question resolved AND DOES affect story |

**Rules**:
- Every Watching item must specify: what it's watching, what story affected, what change would be needed
- Review Watching list every iteration
- When triggered, follow revision protocol for SPEC.md

### Glossary
```markdown
## Glossary
- **[Term]**: [Definition]
```

| Action | Trigger |
|--------|---------|
| Add term | When domain-specific term is used and defined |
| Update definition | When understanding of term changes |
| Graduate to SPEC | When spec is finalized, copy glossary to SPEC.md appendix |

### Next Actions
```markdown
## Next Actions
- [Immediate next step]
```

| Action | Trigger |
|--------|---------|
| Replace | Every iteration - always reflects immediate next step |

**Rules**:
- Maximum 3 items
- Must be specific and actionable
- First item should be the very next thing to do

---

## discovery/OPEN_QUESTIONS.md

**Purpose**: Bounded list of questions awaiting answers. Single source of truth for what's unknown.

**Create**: At session start if it doesn't exist.

**Read**: At start of EVERY session.

### Section: 🔴 Blocking
```markdown
## 🔴 Blocking
### Story [N]: [Title]
- **Q[N]**: [Question]
  - *Context*: [Why needed]
  - *Options*: [If applicable]
  - *Blocking*: [What can't proceed]
```

| Action | Trigger |
|--------|---------|
| Add question | When discovery reveals something that MUST be answered to proceed |
| Remove question | When user answers + decision logged to DECISIONS.md |
| Move to Clarifying | When realized it's not actually blocking |

**Rules**:
- Grouped by story (or "Cross-Cutting")
- Every blocking question MUST have Context and Blocking fields
- Question IDs (Q1, Q2, ...) are globally unique, never reused
- Sync with TodoWrite 🔴 items

### Section: 🟡 Clarifying
```markdown
## 🟡 Clarifying
- **Q[N]**: [Question]
  - *Context*: [Why would improve quality]
```

| Action | Trigger |
|--------|---------|
| Add question | When question would improve spec but isn't blocking |
| Remove question | When answered |
| Move to Blocking | When realized it IS blocking after all |

### Section: 🔵 Research Pending
```markdown
## 🔵 Research Pending
- **Q[N]**: [Topic to investigate]
  - *Purpose*: [What we hope to learn]
  - *Affects*: [Stories this might impact]
```

| Action | Trigger |
|--------|---------|
| Add item | When research is needed before asking user questions |
| Remove item | When research complete + logged to RESEARCH.md |
| Spawn questions | Research may generate new 🔴 or 🟡 questions |

### Section: 🟠 Watching
```markdown
## 🟠 Watching (May Affect Graduated)
- **Q[N]**: If answer is X → Story [Y] needs [change]
```

| Action | Trigger |
|--------|---------|
| Add item | When open question might affect already-graduated story |
| Remove item | When question resolved (either triggers revision or doesn't) |

**Rules**:
- Sync with STATE.md Watching List
- Must specify the conditional: "If X, then Y"

### Question ID Management

- Format: Q1, Q2, Q3, ... (monotonically increasing)
- NEVER reuse IDs, even for removed questions
- Track highest ID used in STATE.md or as comment in OPEN_QUESTIONS.md
- When question answered, ID goes to archive/DECISIONS.md as reference

---

## archive/DECISIONS.md

**Purpose**: Permanent log of all decisions made. Append-only. Query when needed.

**Create**: When first decision is made (typically late Phase 1 or Phase 2).

**Read**: NEVER bulk read. Search/query for specific decisions when needed.

### Entry Format
```markdown
## D[N]: [Short Title] — [YYYY-MM-DD]
**Iteration**: [N]
**Phase**: [Current phase when decision made]
**Story**: [Story # or "Cross-cutting" or "Problem Space"]
**Question**: Q[N] - [question text]
**Options Considered**:
- [Option A]: [Pros/cons]
- [Option B]: [Pros/cons]
**Decision**: [What was decided]
**Rationale**: [Why this choice - can be brief]
**Impact**: [What this affects - requirements, stories, etc.]
**Graduated**: [Not yet | Yes - SPEC.md Story N | Yes - SPEC.md FR-XXX]

---
```

| Action | Trigger |
|--------|---------|
| Append new entry | When user answers a question (🔴 or 🟡) |
| Update Graduated field | When related story graduates to SPEC.md |

**Rules**:
- NEVER modify existing entries (append-only)
- Decision IDs (D1, D2, ...) globally unique, never reused
- Always reference the question ID (Q[N]) that triggered the decision
- Options Considered can be "N/A" for simple factual answers
- One decision per question (if question leads to multiple decisions, split)

**Querying protocol**:
```bash
# Find decisions about authentication
grep -n "auth" discovery/archive/DECISIONS.md

# Find decisions for Story 3
grep -n "Story: 3\|Story: Story 3" discovery/archive/DECISIONS.md

# Find decision D15
grep -A 15 "## D15:" discovery/archive/DECISIONS.md
```

---

## archive/RESEARCH.md

**Purpose**: Permanent log of all research conducted. Append-only. Query when needed.

**Create**: When first research is conducted (typically Phase 1).

**Read**: NEVER bulk read. Search/query for specific research when needed.

### Entry Format
```markdown
## R[N]: [Topic] — [YYYY-MM-DD]
**Iteration**: [N]
**Triggered By**: Q[N] / [Exploration of problem space] / [User request]
**Stories Affected**: [Story #s or "TBD" if Phase 1]
**Query/Focus**: [What was researched]
**Sources**: [Where you looked - can be general]
**Findings**:
- [Key point 1]
- [Key point 2]
- [Key point 3]
**Implications for Spec**:
- [How finding 1 affects requirements/design]
- [How finding 2 affects requirements/design]
**New Questions Raised**: Q[N], Q[M] (or "None")
**Graduated**: [Not yet | Yes - referenced in SPEC.md Story N]

---
```

| Action | Trigger |
|--------|---------|
| Append new entry | After research subagent completes investigation |
| Update Stories Affected | When research relevance to specific stories clarified |
| Update Graduated | When story referencing this research graduates |

**Rules**:
- NEVER modify existing entries
- Research IDs (R1, R2, ...) globally unique
- New Questions should be immediately added to OPEN_QUESTIONS.md
- Keep Findings factual, Implications interpretive

---

## archive/ITERATIONS.md

**Purpose**: Summary log of each iteration for audit trail. Append-only.

**Create**: After first complete iteration (first Q&A cycle).

**Read**: NEVER bulk read. Reference if asked "what did we do in iteration N" or for debugging.

### Entry Format
```markdown
## Iteration [N] — [YYYY-MM-DD HH:MM]
**Phase**: [Phase at start of iteration]
**Focus**: [What this iteration addressed - story or problem area]
**Duration**: [Approximate - optional]

**Questions Asked**: Q[N], Q[M], Q[O]
**Questions Answered**: Q[N], Q[M]
**Decisions Made**: D[X], D[Y]
**Research Conducted**: R[A], R[B] (or "None")

**Stories Progress**:
- Story [N]: [Confidence before]% → [Confidence after]%
- Story [M]: [Status change if any]

**New Items Identified**:
- [New questions, proto-stories, edge cases discovered]

**Watching List Changes**:
- Added: [items]
- Resolved: [items]

**Summary**: [One paragraph - what was accomplished, what's next]

---
```

| Action | Trigger |
|--------|---------|
| Append new entry | End of each iteration (after updating all other files) |

**Rules**:
- One entry per iteration, no modifications
- Create AFTER all other files updated (this is the "commit message")
- Summary should be useful for context recovery

---

## archive/REVISIONS.md

**Purpose**: Detailed log of changes to graduated stories. Append-only.

**Create**: When first revision to a graduated story is made.

**Read**: When user asks about revision history, or when checking revision risk.

### Entry Format
```markdown
## REV-[N]: Story [X] - [Change Type] — [YYYY-MM-DD]
**Iteration**: [N]
**Trigger**: [What prompted this revision - Q[N] answer, R[N] finding, user request]
**Story Version**: v[X.Y] → v[X.Z]

**Scope**: [Additive | Modificative | Structural]

**Before**:
```
[Exact content being changed]
```

**After**:
```
[New content]
```

**Related Changes**:
- [FR-XXX updated: description]
- [EC-XXX added: description]
- [SC-XXX modified: description]

**Decision Reference**: D[N]
**User Confirmed**: Yes — [date] / Pending

---
```

| Action | Trigger |
|--------|---------|
| Append new entry | When any change made to graduated story in SPEC.md |

**Rules**:
- NEVER modify existing entries
- REV IDs (REV-1, REV-2, ...) globally unique
- Before/After should be exact (copy-paste from SPEC.md)
- Related Changes captures ripple effects
- User Confirmed must be "Yes" before SPEC.md is actually modified

---

## TodoWrite Sync Rules

**Purpose**: Real-time dashboard for blocking items. Must stay in sync with files.

### When to Update TodoWrite

| File Change | TodoWrite Action |
|-------------|------------------|
| Add 🔴 question to OPEN_QUESTIONS.md | Add `- [ ] 🔴 Q[N]: [summary]` |
| Resolve 🔴 question | Remove or mark complete |
| Add 🟡 question | Add `- [ ] 🟡 Q[N]: [summary]` |
| Resolve 🟡 question | Remove or mark complete |
| Add 🔵 research item | Add `- [ ] 🔵 R: [topic]` |
| Complete research | Remove or mark complete |
| Add 🟠 watching item | Add `- [ ] 🟠 Q[N]: [what watching]` |
| Resolve watching (no revision) | Remove |
| Resolve watching (revision needed) | Move to `## Ready Actions` as revision task |
| Story ready to graduate | Add `- [ ] 🟢 Story [N]: Ready to graduate` |
| Story graduated | Remove 🟢 item |

### TodoWrite Structure
```
TodoWrite:
## Phase: [Current Phase]

## Current Focus: [Story N or "Problem Exploration"]
- [ ] 🔴 Q[N]: [summary]
- [ ] 🟡 Q[M]: [summary]

## Research Queue
- [ ] 🔵 [Topic]

## Other Stories
### Story [M]
- [ ] 🔴 Q[O]: [summary]

## Watching (Graduated Story Risk)
- [ ] 🟠 Q[P]: May affect Story [X]

## Ready Actions
- [ ] 🟢 Story [N]: Ready to graduate
- [ ] 🟢 REV: Story [X] needs revision per Q[P]
```

---

## Cross-File Consistency Rules

These invariants must ALWAYS be maintained:

| Rule | Enforcement |
|------|-------------|
| Question in OPEN_QUESTIONS.md ↔ Referenced in STATE.md story section | When adding question, add to both |
| Question resolved → Decision in DECISIONS.md | Every answered question = one decision entry |
| Story graduates → Remove detail from STATE.md, add to SPEC.md | Full graduation protocol |
| Story graduates → Update Completed Stories table in STATE.md | Add summary row |
| Revision to SPEC.md → Entry in REVISIONS.md | Every SPEC.md story change logged |
| Watching item triggers → Follows revision protocol | Don't modify SPEC.md without logging |
| TodoWrite reflects current OPEN_QUESTIONS.md | Sync after every question change |
| ID uniqueness | Q[N], D[N], R[N], REV[N], FR-XXX, EC-XXX, SC-XXX never reused |

---

## Sync Checkpoints

After EVERY iteration, verify:
```
1. [ ] STATE.md Updated timestamp current
2. [ ] STATE.md Iteration incremented
3. [ ] All answered questions removed from OPEN_QUESTIONS.md
4. [ ] All answered questions have entry in DECISIONS.md
5. [ ] TodoWrite matches OPEN_QUESTIONS.md
6. [ ] Any graduated stories removed from STATE.md detail
7. [ ] Any graduated stories added to SPEC.md
8. [ ] Watching list reviewed for any triggered items
9. [ ] ITERATIONS.md has entry for this iteration
10. [ ] Next Actions in STATE.md reflects actual next step
```

Run this checklist mentally (or explicitly for complex iterations) before ending each iteration.
