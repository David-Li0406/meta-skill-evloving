---
# === CONTEXT WORKNOTES TEMPLATE ===
# PRD-level sticky pad for agent notes and observations during development
# This file can start empty or nearly empty and grows as agents add notes
# Optimized for token-efficient queries by AI agents

# Metadata: Identification and Scope
type: context
prd: "[PRD_ID]"                          # e.g., "artifact-flow-modal-redesign"
title: "[PRD_NAME] - Development Context"
status: "active"                         # active|archived|abandoned
created: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

# Quick Reference (for fast agent queries)
critical_notes_count: 0                  # Number of critical observations
implementation_decisions_count: 0        # Number of key decisions documented
active_gotchas_count: 0                  # Number of unresolved gotchas
agent_contributors: []                   # List of agents who have added notes

# Agent Communication Index (for efficient lookups)
# Format: { agent: "agent-name", note_count: N, last_contribution: "YYYY-MM-DD" }
agents: []
---

# [PRD_NAME] - Development Context

**Status**: Active Development
**Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]

> **Purpose**: This is a shared worknotes file for all AI agents working on this PRD. Add brief observations, decisions, gotchas, and implementation notes that future agents should know. Think of this as a sticky-note pad for the development team.

---

## Quick Reference

**Agent Notes**: [COUNT] notes from [N] agents
**Critical Items**: [COUNT] items requiring attention
**Last Contribution**: [AGENT_NAME] on [DATE]

---

## Implementation Decisions

> Key architectural and technical decisions made during development

### [YYYY-MM-DD] - [Agent Name] - [Brief Decision Title]

**Decision**: [What was decided in 1-2 sentences]

**Rationale**: [Why in 1-2 sentences]

**Location**: `path/to/file.ext:line`

**Impact**: [What this affects]

---

## Gotchas & Observations

> Things that tripped us up or patterns discovered during implementation

### [YYYY-MM-DD] - [Agent Name] - [Brief Gotcha Title]

**What**: [What happened in 1-2 sentences]

**Why**: [Root cause in 1 sentence]

**Solution**: [How to avoid/fix in 1-2 sentences]

**Affects**: [Which files/components/phases]

---

## Integration Notes

> How components interact and connect

### [YYYY-MM-DD] - [Agent Name] - [Integration Point]

**From**: [Component A]
**To**: [Component B]
**Method**: [API call, prop passing, event, etc.]
**Notes**: [Brief context, gotchas, or important details]

---

## Performance Notes

> Performance considerations discovered during implementation

### [YYYY-MM-DD] - [Agent Name] - [Performance Item]

**Issue**: [What performs poorly]
**Impact**: [How bad and where]
**Fix**: [What was done or needs to be done]

---

## Agent Handoff Notes

> Quick context for agents picking up work

### [YYYY-MM-DD] - [Agent Name] → [Next Agent]

**Completed**: [What was just finished]
**Next**: [What should be done next]
**Watch Out For**: [Any gotchas or warnings]

---

## References

**Related Files**:
- [Link to progress tracking]
- [Link to implementation plan]
- [Link to design specs]

---

## Template Examples

<details>
<summary>Example: Implementation Decision</summary>

### 2025-11-29 - ui-engineer-enhanced - Use SVG paths for flow connectors

**Decision**: Flow banner will use SVG `<path>` elements with quadraticCurveTo for curved arrows instead of CSS transforms

**Rationale**: SVG provides pixel-perfect curves and is easier to position action buttons along the path

**Location**: `components/entity/sync-status/artifact-flow-banner.tsx:45`

**Impact**: Requires SVG viewBox calculations, but gives exact control over connector styling

</details>

<details>
<summary>Example: Gotcha/Observation</summary>

### 2025-11-29 - ui-engineer-enhanced - React Query cache invalidation pattern

**What**: Calling `queryClient.invalidateQueries(['artifacts'])` was causing full page re-renders

**Why**: Too broad a key pattern was invalidating unrelated queries

**Solution**: Use specific keys like `queryClient.invalidateQueries(['artifacts', entity.id])`

**Affects**: All hooks in `hooks/useSync.ts`, `hooks/useDeploy.ts`

</details>

<details>
<summary>Example: Integration Note</summary>

### 2025-11-29 - ui-engineer-enhanced - SyncStatusTab ↔ DiffViewer

**From**: SyncStatusTab (orchestrator)
**To**: DiffViewer (existing component)
**Method**: Props `diff={currentDiff}` and `selectedFile={selectedFile}`
**Notes**: DiffViewer already handles all diff parsing. Just pass through the API response from `/artifacts/{id}/diff` endpoint.

</details>

<details>
<summary>Example: Agent Handoff</summary>

### 2025-11-29 - ui-engineer-enhanced → refactoring-expert

**Completed**: All 5 Phase 1 components built and integrated into SyncStatusTab

**Next**: Wire all action buttons to real API calls (useSync, useDeploy hooks). See phase-1-progress.md TASK-4.1

**Watch Out For**: "Push to Collection" button needs "Coming Soon" tooltip - backend endpoint doesn't exist yet

</details>
