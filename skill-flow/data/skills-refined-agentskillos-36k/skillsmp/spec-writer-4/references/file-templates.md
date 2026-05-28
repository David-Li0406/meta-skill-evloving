# File Templates Reference (Manual Operations Only)

This reference covers file sections and content that require manual creation. For automated operations, see the script tier references.

**Key Principle**: This guide focuses on what YOU must write manually. Scripts handle questions, decisions, research, iterations, and revisions.

---

## STATE.md - Manual Sections

STATE.md contains both manual sections (you write them) and automated sections (scripts manage them). This reference covers only the manual sections.

### Header Metadata (Manual)

Update these fields manually every time you make significant changes to STATE.md:

```markdown
**Updated**: 2026-01-19 14:32 UTC
**Iteration**: 3
**Phase**: Story Development
```

**When to update:**
- `Updated`: Every time ANY content in STATE.md changes
- `Iteration`: Increment when transitioning phases or after major milestones
- `Phase`: Update when transitioning between discovery phases

---

### Problem Understanding (Phase 1 - Manual)

**This entire section is manual.** You write it during Phase 1 (Problem Exploration) and evolve it through iterations.

```markdown
## Problem Understanding

### Problem Statement
[One paragraph: What problem are we solving? For whom? Why does it matter?]

Example:
Engineering teams struggle to understand how service dependencies affect their work. When upstream services change their APIs, downstream teams are caught off-guard, leading to broken builds and emergency fixes. This costs the company approximately 20 hours per week in reactive debugging.

### Personas
| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| Backend Engineer | Maintains microservices | Understand dependencies before making changes |
| DevOps Engineer | Manages deployment pipeline | Prevent breaking changes from reaching production |

### Current State vs. Desired State
**Today (without feature)**: Engineers manually check service documentation, ask in Slack, or discover dependencies through build failures.

**Tomorrow (with feature)**: Engineers see visual dependency graph, get notified of breaking changes before they merge, can test impact before deploying.

### Constraints
- Must integrate with existing CI/CD pipeline (Jenkins)
- Cannot add >500ms to build time
- No budget for new infrastructure (use existing monitoring tools)
```

**How this section evolves:**
- **Iteration 1-2**: Rough draft, many unknowns
- **Iteration 3-5**: Refined based on research and decisions
- **At graduation to SPEC.md**: Problem statement is stable and clear

---

### In-Progress Story Detail (Phase 3 - Manual)

**This entire section is manual.** This is where you do the deep-dive work on one story at a time.

```markdown
## In-Progress Story Detail

### Story 3: Service Dependency Visualization (Priority: P3)

**One-line**: As a backend engineer, I want to see a visual graph of my service's dependencies so that I can understand the impact of my changes before merging

**Current Confidence**: 75%

**Working Understanding**:
This story provides a real-time dependency graph showing:
- Direct dependencies (services my service calls)
- Reverse dependencies (services that call my service)
- Breaking change warnings from upstream services
- Historical change patterns

The graph should be interactive (zoom, filter) and update within 30 seconds of config changes.

**Draft Acceptance Scenarios**:
1. **Given** I open the dependency view for my service, **When** I view the graph, **Then** I see all direct and reverse dependencies with current versions
   - *Confidence*: High
   - *Open questions*: None

2. **Given** an upstream service has a pending breaking change, **When** I view dependencies, **Then** I see a warning badge on that service
   - *Confidence*: Medium
   - *Open questions*: Q25 (How to detect breaking changes?)

**Blocking Questions**: Q23 (Graph library choice), Q25 (Breaking change detection)
**Clarifying Questions**: Q27 (Historical view depth), Q28 (Mobile support?)

**Draft Edge Cases**:
- Circular dependencies (A → B → C → A)
- Service with 50+ dependencies (performance/readability)
- Dependency on external third-party API (not in our system)
- Service that's being deprecated (show differently?)

**Draft Requirements**:
- FR-007: System MUST display dependency graph within 30 seconds of config change
- FR-008: System MUST identify circular dependencies and highlight them
- FR-009: System MUST support filtering by dependency depth (1-3 levels)

**Confidence Gaps**:
- Graph library performance with 100+ nodes (need spike)
- Integration with Jenkins API (need technical exploration)
- Breaking change detection mechanism (blocked on Q25)
```

**Graduation criteria for this section:**
- All blocking questions resolved
- Confidence ≥80% overall
- Edge cases identified and addressed
- Requirements testable and complete
- User has reviewed and confirmed understanding

---

### Story Landscape Manual Updates (Ongoing)

Some parts of Story Landscape are managed by scripts (`update-story-status.py`, `graduate-story.py`), but these sections are manual:

#### Proto-Stories / Emerging Themes

```markdown
### Proto-Stories / Emerging Themes
*Potential stories not yet crystallized:*
- **Cross-service impact timeline**: Show historical view of how dependency changes affected build times — *Needs more exploration, may be Phase 2*
- **Notification preferences**: Let engineers customize which dependency changes they care about — *May merge with Story 2*
- **Dependency health score**: Aggregate metric showing overall dependency risk — *Not sure if valuable, watching user feedback*
```

**When to add proto-stories:**
- Research reveals a new theme (from `log-research.py`)
- Questions reveal a gap not covered by existing stories
- User mentions a related need that doesn't fit current backlog

**When to promote to real stories:**
- Proto-story is well-understood and scoped
- Priority is clear
- Dependencies on other stories are identified

#### Glossary

```markdown
### Glossary
| Term | Definition | Why it matters |
|------|------------|----------------|
| Breaking Change | API modification that requires downstream code changes | Core concept - triggers notifications |
| Dependency Depth | Number of hops from service A to service B | Affects graph performance and readability |
| Reverse Dependency | Service that depends on you (not you depend on it) | Critical for impact analysis |
```

**When to update:**
- New technical term emerges during research
- User uses term you don't understand
- Team debates meaning of a term (capture shared understanding)

#### Next Actions

```markdown
### Next Actions
- [ ] Spike: Test vis.js library with 100+ nodes (Story 3) — *Assigned to Backend Team*
- [ ] Research: How does GitHub detect breaking changes? (Q25) — *Claude*
- [ ] User Validation: Review Story 3 acceptance scenarios — *Waiting for User*
- [ ] Technical Spike: Jenkins API integration feasibility (Story 3) — *Assigned to DevOps*
```

**Update manually when:**
- New action emerges from research or questions
- Action is completed (move to done or note in iteration log)
- Ownership changes

---

## SPEC.md - Manual Sections

SPEC.md is mostly automated (scripts handle story graduation, requirements tables, edge cases). You only write these sections manually:

### Header Metadata (Manual)

```markdown
# Product Specification: [Feature Name]

**Status**: [Draft | Review | Approved | In Development]
**Last Updated**: 2026-01-19
**Author**: [Your name or team]
**Stakeholders**: [Product Manager, Engineering Lead, etc.]

**Version**: 1.2
*Latest changes: Added Story 5 (cross-service search), revised Story 1 FR-012 per REV-003*
```

**When to update:**
- `Last Updated`: Every time ANY content in SPEC.md changes
- `Status`: When spec moves through approval stages
- `Version`: When stories are added, removed, or significantly revised

### Problem Statement (Manual - Graduate from STATE.md)

When you graduate a story to SPEC.md, the Problem Statement from STATE.md moves here:

```markdown
## Problem Statement

Engineering teams struggle to understand how service dependencies affect their work. When upstream services change their APIs, downstream teams are caught off-guard, leading to broken builds and emergency fixes.

**Impact**: ~20 hours/week wasted on reactive debugging
**Affected Teams**: 12 backend teams, 3 DevOps engineers
**Business Value**: Reduce deployment failures by 60%, improve team confidence
```

**This is copied from STATE.md - don't write it fresh.**

### Story Revisions (Manual)

When a graduated story needs changes, you edit the story content in SPEC.md and log the revision:

**Process:**
1. Use `add-revision.py` to log the revision to archive/REVISIONS.md
2. Manually edit the story in SPEC.md (modify acceptance scenarios, requirements, etc.)
3. Update the Appendix: Story Revision History section (below)
4. Coordinate with user to confirm revision

**When manual editing is needed:**
- Adding a new acceptance scenario to graduated story
- Modifying a requirement based on new information
- Clarifying edge case handling
- Adjusting success criteria

**Example Appendix section:**
```markdown
## Appendix: Story Revision History

### Story 1: Service Dependency Visualization

**v1.1** (2026-01-18) — Added Scenario 3 for circular dependency handling
- *Trigger*: Story 3 revealed edge case not covered in Story 1
- *Decision*: D52
- *See*: REV-001

**v1.0** (2026-01-15) — Initial graduation

### Story 2: Breaking Change Notifications

**v1.0** (2026-01-16) — Initial graduation
```

---

## Reading vs Writing Operations

### Files You Must Read Manually

**STATE.md** - Read to:
- Resume session (understand current context)
- Check story progress (Status Overview table)
- Review in-progress story detail
- Identify next actions

**SPEC.md** - Read to:
- Review graduated stories
- Verify requirements are correct
- Share with stakeholders
- Track revision history

**OPEN_QUESTIONS.md** - Read to:
- Check for blockers
- Understand clarifications needed
- Review research questions
- Track resolution status

### Sections You Write Manually

| Section | File | When to Write |
|---------|------|---------------|
| Problem Understanding | STATE.md | Phase 1, evolve through iterations |
| In-Progress Story Detail | STATE.md | Phase 3, one story at a time |
| Proto-Stories | STATE.md | Ongoing as themes emerge |
| Glossary | STATE.md | Ongoing as terms are defined |
| Next Actions | STATE.md | Ongoing as actions emerge |
| Header metadata | STATE.md, SPEC.md | After every update |
| Problem Statement | SPEC.md | Copy from STATE.md at graduation |
| Story revisions | SPEC.md | When graduated stories need changes |
| Revision appendix | SPEC.md | After each revision |

### Operations Now Fully Scripted

These operations used to be manual but are now fully automated:

| Task | Script | Reference |
|------|--------|-----------|
| Adding questions | add-question.py | scripts-tier-1.md |
| Logging decisions | log-decision.py | scripts-tier-1.md |
| Finding decisions | find-decisions.py | scripts-tier-1.md |
| Resolving questions | resolve-question.py | scripts-tier-2.md |
| Logging research | log-research.py | scripts-tier-3.md |
| Finding research | find-research.py | scripts-tier-2.md |
| Recording revisions | add-revision.py | scripts-tier-3.md |
| Logging iterations | log-iteration.py | scripts-tier-3.md |
| Finding iterations | find-iterations.py | scripts-tier-3.md |
| Graduating stories | graduate-story.py | scripts-tier-2.md |
| Updating story status | update-story-status.py | scripts-tier-2.md |
| Adding edge cases | add-edge-case.py | scripts-tier-4.md |
| Adding requirements | add-functional-requirement.py | scripts-tier-4.md |
| Adding success criteria | add-success-criteria.py | scripts-tier-4.md |

**Never manually edit:**
- OPEN_QUESTIONS.md (use add-question.py, resolve-question.py)
- archive/DECISIONS.md (use log-decision.py)
- archive/RESEARCH.md (use log-research.py)
- archive/ITERATIONS.md (use log-iteration.py)
- archive/REVISIONS.md (use add-revision.py)
- Story Status Overview table (use update-story-status.py, graduate-story.py)
- Requirement tables in SPEC.md (use tier 4 scripts)

---

## File Maintenance Best Practices

### STATE.md Maintenance

**Every session:**
1. Update header timestamp
2. Review Story Status Overview (update manually if needed or use scripts)
3. Update In-Progress Story Detail as you learn
4. Add proto-stories as themes emerge
5. Update Next Actions

**Phase transitions:**
1. Increment Iteration number
2. Update Phase field
3. Log iteration summary with `log-iteration.py`

### SPEC.md Maintenance

**After graduating a story:**
1. Verify Problem Statement is accurate
2. Check all requirement IDs are correct
3. Update Last Updated timestamp
4. Increment Version if this is first story or major change

**After revising a graduated story:**
1. Edit story content in SPEC.md
2. Update Revision History appendix
3. Update Version
4. Update Last Updated timestamp
5. Coordinate user confirmation

### Daily Workflow

**Morning:**
1. Read STATE.md (check story status, blockers, next actions)
2. Read OPEN_QUESTIONS.md (understand what's blocking)
3. Run `story-status.sh` for quick overview

**During work:**
4. Update In-Progress Story Detail as you learn
5. Use scripts to log questions, decisions, research as you go
6. Update glossary when new terms emerge
7. Add proto-stories when themes emerge

**End of day:**
8. Update STATE.md header timestamp
9. Validate with `validate-spec.py`
10. Log iteration with `log-iteration.py` (if significant progress)
11. Update Next Actions

---

## Quick Reference: Manual vs Automated

**Manual = You Write It:**
- Problem Understanding (all of it)
- In-Progress Story Detail (all of it)
- Proto-Stories, Glossary, Next Actions
- Header metadata (timestamps, iterations, phases)
- Story revisions in SPEC.md
- Revision appendix in SPEC.md

**Automated = Scripts Handle It:**
- Questions (add-question.py, resolve-question.py)
- Decisions (log-decision.py, find-decisions.py)
- Research (log-research.py, find-research.py)
- Iterations (log-iteration.py, find-iterations.py)
- Revisions (add-revision.py)
- Story lifecycle (graduate-story.py, update-story-status.py)
- Requirements tables (tier 4 scripts)

**When in doubt**: If there's a script for it, use the script. This reference only covers what scripts can't do.

---

## Examples

### Example: Evolving Problem Statement

**Iteration 1 (rough draft):**
```
Engineers don't know what depends on their services. This causes problems.
```

**Iteration 3 (better):**
```
Backend engineers can't easily visualize service dependencies. When they make changes, they don't know which downstream services will be affected, leading to broken builds and emergency fixes.
```

**Iteration 5 (ready for SPEC.md):**
```
Engineering teams struggle to understand how service dependencies affect their work. When upstream services change their APIs, downstream teams are caught off-guard, leading to broken builds and emergency fixes. This costs the company approximately 20 hours per week in reactive debugging across 12 backend teams.
```

### Example: Building In-Progress Story Detail

**Confidence 20% (just starting):**
```
### Story 3: Service Dependency Visualization

**One-line**: Show engineers what depends on their service

**Working Understanding**:
Maybe a graph? Not sure what format yet.

**Blocking Questions**: Q23 (What should we show?), Q24 (How to get this data?)
```

**Confidence 60% (research done, still refining):**
```
### Story 3: Service Dependency Visualization

**One-line**: As a backend engineer, I want to see a visual graph of dependencies so that I understand impact

**Working Understanding**:
Interactive graph showing both direct and reverse dependencies. Updates in real-time from service registry. Research shows vis.js is popular for this (R5).

**Draft Acceptance Scenarios**:
1. **Given** I open dependency view, **When** graph loads, **Then** I see my service and all dependencies
   - *Confidence*: High
   - *Open questions*: None

**Blocking Questions**: Q25 (Breaking change detection)
**Clarifying Questions**: Q27 (Historical view?)
```

**Confidence 80% (ready to graduate):**
```
### Story 3: Service Dependency Visualization

**One-line**: As a backend engineer, I want to see a visual graph of my service's dependencies so that I can understand the impact of my changes before merging

**Working Understanding**:
Real-time interactive dependency graph using vis.js library. Shows direct dependencies, reverse dependencies, breaking change warnings. Updates within 30 seconds of config changes. Decision D15 chose vis.js based on research R5.

**Draft Acceptance Scenarios**:
[5 complete scenarios with high confidence]

**Draft Edge Cases**:
[4 edge cases identified and addressed]

**Draft Requirements**:
- FR-007: Display graph within 30 seconds
- FR-008: Identify circular dependencies
- FR-009: Support 1-3 level depth filtering

**Confidence Gaps**: None - ready to graduate
```
