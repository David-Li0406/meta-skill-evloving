---
name: session-handoff
description: "Generate Sarah Briefs and maintain STATUS/TODO files for session continuity. Use for: (1) End-of-session documentation, (2) STATUS.md updates, (3) TODO.md task management, (4) Session context preservation. Triggers: Sarah Brief, brief, handoff, session end, status update, TODO update, documentation, end session."
---

# Session Handoff Skill

## Purpose

Ensure session continuity by generating structured documentation at the end of significant work sessions. This skill codifies the Sarah Brief format and STATUS/TODO update patterns.

## Memory Framework Context

Session handoff serves **Layer 4** of the Prometheus Memory Framework:

```
Layer 1: Constitution & Architecture (Immutable Authority)
Layer 2: Context Packages (Task-specific anchoring)
Layer 3: PKE Retrieval (Structured long-term knowledge)
Layer 4: Logs & Trace History (Temporal grounding)  ← THIS LAYER
Layer 5: Local State (Ephemeral)
```

## Document Types

### 1. Sarah Brief

**Purpose:** Comprehensive session report for Controller (Sarah) review

**Location:** `docs/briefs/SARAH_BRIEF_{topic}_{date}.md`

**Naming Convention:**
- `SARAH_BRIEF_` prefix (mandatory)
- `{topic}` - kebab-case description of work focus
- `_{date}` - YYYY-MM-DD format
- `.md` extension

**Examples:**
- `SARAH_BRIEF_scalar-bidirectional-sync_2025-01-14.md`
- `SARAH_BRIEF_format-page-implementation_2025-12-30.md`
- `SARAH_BRIEF_status-update_2025-01-09.md`

---

### Sarah Brief Template

```markdown
# Sarah Brief: [Title]

**Date:** [YYYY-MM-DD]
**Session:** Claude Code (CC)
**Type:** [Feature Implementation Report | Status Update | Bug Fix | Refactor]
**Branch:** `[branch-name]`
**Commit:** `[short-hash]`

---

## Executive Summary

[2-3 sentences summarizing what was accomplished and why it matters]

---

## Problem Statement

[What issue/requirement drove this work?]
[Root cause if applicable]

---

## Solution Implemented

### [Solution Name]

[Description of approach]

| Component | Change | Purpose |
|-----------|--------|---------|
| [File/Function] | [What changed] | [Why] |

### Data Flow (if applicable)

```
[ASCII diagram of data flow]
```

---

## Files Modified

### Core Changes ([count] files, +[added] / -[removed] lines)

| File | Lines Changed | Impact |
|------|---------------|--------|
| [file.jsx] | +[n] | [Description] |

### New Components Created

| Component | Purpose |
|-----------|---------|
| [Component.jsx] | [What it does] |

---

## Testing Results

### Automated Testing ([Framework])

| Test | Status | Notes |
|------|--------|-------|
| [Test name] | PASS/FAIL | [Details] |

### Manual Testing Recommended

[List of things to verify manually]

---

## Commit Details

```
commit [hash]
Author: [User]
Date:   [Date]

[Full commit message]
```

---

## Technical Debt Addressed

| Item | Status | Notes |
|------|--------|-------|
| [Debt item] | RESOLVED/DEFERRED | [Details] |

---

## Outstanding Items

### From Previous Sessions

| Item | Status | Priority |
|------|--------|----------|
| [Item] | [Status] | [Priority] |

### New Items

| Item | Priority | Notes |
|------|----------|-------|
| [Item] | [Priority] | [Details] |

---

## Session Metrics

| Metric | Value |
|--------|-------|
| Files Modified | [n] |
| Lines Added | +[n] |
| Lines Removed | -[n] |
| Net Change | +/-[n] |
| New Components | [n] |
| Tests Run | [n] |

---

## Recommendations

### Immediate

1. [Action item]

### Short-Term

1. [Action item]

### Medium-Term

1. [Action item]

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | LOW/MEDIUM/HIGH | LOW/MEDIUM/HIGH | [Mitigation] |

---

## Session Handoff Notes

### Key Context for Next Session

1. [Important context point]

### Files Requiring Attention

- [file.jsx] - [Reason]

---

*Brief prepared by Claude Code for Controller (Sarah) review.*
*Report generated: [Date]*
```

---

### 2. STATUS.md Update

**Purpose:** Maintain authoritative system state

**Location:** `docs/STATUS.md`

**Update Triggers:**
- End of significant session
- Component state change
- Major commit
- Phase completion

#### STATUS.md Sections to Update

| Section | When to Update |
|---------|----------------|
| Quick Summary | Every session |
| Component Status | State changes |
| Recent Changes | Add new row |
| Latest Commit | After commits |
| Technical Debt | Debt addressed/added |
| Session Handoff Notes | Every session |

#### Update Pattern

```markdown
## Recent Changes (Last 5 Sessions)

| Date | Session | Key Changes |
|------|---------|-------------|
| [NEW DATE] | CC | [NEW CHANGES] |
| [Previous] | CC | [Previous changes] |
...
```

**Rule:** Keep only last 5 sessions; archive older to briefs.

---

### 3. TODO.md Update

**Purpose:** Track active task backlog

**Location:** `docs/TODO.md`

**Update Triggers:**
- Task completed → Move to "Completed"
- New task identified → Add to "Active" or "Backlog"
- Priority change → Reorder items
- Task blocked → Note blocker

#### TODO.md Sections

| Section | Content |
|---------|---------|
| Active (Current Focus) | 3-5 highest priority items |
| Backlog (Next Up) | Queued items |
| Completed (Recent) | Last 10 completed items |
| Task Log | Audit trail by session |

#### Task Movement Pattern

```markdown
## Active (Current Focus)

| Task | Priority | Status | Notes |
|------|----------|--------|-------|
| [Task moving to completed] | HIGH | **COMPLETE** | [Notes] |

↓ Move to ↓

## Completed (Recent)

| Task | Completed | Notes |
|------|-----------|-------|
| [Task] | [Date] | [Notes] |
```

---

## Handoff Checklist

Before ending a significant session:

### Documentation

- [ ] Create Sarah Brief if substantial work done
- [ ] Update STATUS.md Quick Summary
- [ ] Update STATUS.md Component Status (if changed)
- [ ] Add entry to Recent Changes
- [ ] Update Session Handoff Notes

### TODO Management

- [ ] Mark completed tasks as COMPLETE
- [ ] Add new tasks discovered during session
- [ ] Add entry to Task Log
- [ ] Review priorities (still correct?)

### Git State

- [ ] All work committed (or documented why not)
- [ ] Commit messages descriptive
- [ ] Branch state documented

### Context Preservation

- [ ] Key decisions documented
- [ ] Files requiring attention noted
- [ ] Blockers/risks identified
- [ ] Next steps clear

---

## Automated Generation (Future)

### Proposed Command

```bash
# Generate Sarah Brief from git state
python scripts/generate_brief.py \
  --topic "scalar-sync" \
  --type "feature" \
  --since "HEAD~5"

# Update STATUS.md
python scripts/update_status.py \
  --component "Design - Scalar" \
  --state "ENHANCED" \
  --notes "Bidirectional sync implemented"

# Update TODO.md
python scripts/update_todo.py \
  --complete "SCALAR Bidirectional Sync" \
  --add "Full CRUD testing for SCALAR" \
  --priority MEDIUM
```

### Brief Data Sources

| Data | Source |
|------|--------|
| Commit details | `git log --oneline -n 10` |
| Files changed | `git diff --stat HEAD~n` |
| Lines changed | `git diff --numstat HEAD~n` |
| Branch name | `git branch --show-current` |
| Date | `date +%Y-%m-%d` |

---

## Quality Standards

### Sarah Brief Quality

| Criteria | Requirement |
|----------|-------------|
| Executive Summary | Clear, 2-3 sentences |
| Problem Statement | Root cause identified |
| Solution | Approach explained, not just listing changes |
| Files Modified | Impact assessed, not just listed |
| Testing | Results documented, gaps noted |
| Recommendations | Actionable, prioritised |
| Handoff Notes | Specific, contextual |

### STATUS.md Quality

| Criteria | Requirement |
|----------|-------------|
| Quick Summary | Current, accurate |
| Component Status | States reflect reality |
| Recent Changes | Chronological, concise |
| Handoff Notes | Useful for next session |

### TODO.md Quality

| Criteria | Requirement |
|----------|-------------|
| Active Section | 3-5 items only |
| Task Descriptions | Clear, actionable |
| Status | Reflects reality |
| Task Log | Maintains audit trail |

---

## Brief Types

| Type | When to Use |
|------|-------------|
| **Feature Implementation Report** | New feature completed |
| **Status Update** | General session work, multiple small changes |
| **Bug Fix** | Specific bug identified and resolved |
| **Refactor** | Code restructuring without feature change |
| **Phase Completion** | Multi-session milestone achieved |
| **Test Report** | SOC or IT results |

---

## File Locations

| Document | Location |
|----------|----------|
| Sarah Briefs | `docs/briefs/SARAH_BRIEF_*.md` |
| STATUS.md | `docs/STATUS.md` |
| TODO.md | `docs/TODO.md` |
| IDEAS.md | `docs/IDEAS.md` |
| Test Logs | `docs/briefs/PHASE*_TEST_LOG.md` |

---

## See Also

- `docs/memory-framework.md` - Memory architecture context
- `/prometheus-testing` - Testing doctrine (SOC reports)
- `CLAUDE_PROTOCOL.md` - Task execution protocol
- `docs/briefs/` - Historical briefs for reference
