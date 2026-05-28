# Claude KM Skill Roadmap

## Overview

A 4-layer knowledge capture system for development sessions with Claude Code.

---

## Timeline

```
Dec 2025                    Jan 2026
   │                           │
   ▼                           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  v1.0                        v1.1 ✓                                          │
│  Initial                     Core Fixes &                                    │
│  Release                     Jira Integration                                │
└──────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  v1.2 (In Progress)                                                          │
│  Knowledge System Expansion                                                  │
│  - Pattern Library, Flow Docs, Cross-Project Sync, Search Index              │
└──────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  v1.3 (Planned)                                                              │
│  Reporting & Examples                                                        │
│  - Session Summaries, Code Examples Library                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Completed

### v1.1 - Core Fixes & Jira Integration ✓

| Issue | Title | Type |
|-------|-------|------|
| #1 | Fix hooks.json schema and configuration | fix |
| #3 | HEREDOC ใน /focus skill ไม่ expand variables | bug |
| #4 | /pr-review ควรสร้าง issue เมื่อ defer งานจาก review | bug |
| #5 | /pr-review ควรใส่ commit hash เมื่อตอบ Fixed | bug |
| #8 | /td ควรตรวจสอบ PR status ก่อน commit docs | fix |
| #10 | Add Jira integration for issue management | feature |
| #12 | Document text search requirements for Jira | docs |
| #14 | Update documentation after Jira integration | docs |
| #17 | pr-review skill should include commit hash in replies | bug |
| #20 | gh pr create ควรระบุ --base branch | fix |
| #21 | GitHub polling daemon สำหรับ monitor PR | feature |
| #24 | /pr skill uses quoted heredoc preventing date substitution | bug |

---

## In Progress

### v1.2 - Knowledge System Expansion

> Expand knowledge management capabilities with patterns, flows, cross-project sync, and search.

| Issue | Title | Status |
|-------|-------|--------|
| [#2](https://github.com/goffity/claude-km-skill/issues/2) | Improve subagents (commit-assistant, pr-review, session-review) | Open |
| [#28](https://github.com/goffity/claude-km-skill/issues/28) | Add Decision Rationale section to /distill template | Open |
| [#29](https://github.com/goffity/claude-km-skill/issues/29) | Add Pattern Library support (patterns/) | Open |
| [#30](https://github.com/goffity/claude-km-skill/issues/30) | Add Flow Documentation support (flows/) | Open |
| [#31](https://github.com/goffity/claude-km-skill/issues/31) | Add Cross-Project Knowledge Sync (knowledge/shared/) | Open |
| [#32](https://github.com/goffity/claude-km-skill/issues/32) | Add Knowledge Search Index | Open |
| [#37](https://github.com/goffity/claude-km-skill/issues/37) | Add retention policy for auto-captured files | Open |
| [#38](https://github.com/goffity/claude-km-skill/issues/38) | Add session consolidation for auto-captured files | Open |
| [#40](https://github.com/goffity/claude-km-skill/issues/40) | Improve notification to show terminal/tab identifier | Open |
| [#48](https://github.com/goffity/claude-km-skill/issues/48) | Add automatic PR review notification with polling daemon | Open |
| [#49](https://github.com/goffity/claude-km-skill/issues/49) | Auto-assign issue when starting work | Open |

**Key Deliverables:**
- Pattern Library (`patterns/`) - Reusable code patterns with context
- Flow Documentation (`flows/`) - Multi-step workflow documentation
- Cross-Project Sync (`knowledge/shared/`) - Share knowledge across projects
- Search Index - Fast lookup across all knowledge artifacts
- Retention Policy - Auto-cleanup old auto-captured files
- Session Consolidation - Merge related sessions for multi-agent setups
- Notification Improvement - Better terminal/tab identification (multi-terminal support)
- PR Review Notification - Automatic polling daemon to notify when PRs are reviewed
- Auto-Assign Issues - Automatically assign user when starting work on an issue

---

## Planned

### v1.3 - Reporting & Examples

> Add session summaries and code examples library for better knowledge retrieval.

| Issue | Title | Status |
|-------|-------|--------|
| [#33](https://github.com/goffity/claude-km-skill/issues/33) | Add Session Summaries (weekly/monthly) | Open |
| [#34](https://github.com/goffity/claude-km-skill/issues/34) | Add Code Examples Library (examples/) | Open |

**Key Deliverables:**
- Session Summaries - Aggregate learnings by week/month
- Code Examples Library (`examples/`) - Searchable code snippets with explanations

---

## Feature Requests

Have an idea? [Open an issue](https://github.com/goffity/claude-km-skill/issues/new)

---

## Progress

| Milestone | Status | Progress |
|-----------|--------|----------|
| v1.1 - Core Fixes & Jira Integration | Done | 12/12 (100%) |
| v1.2 - Knowledge System Expansion | In Progress | 0/11 (0%) |
| v1.3 - Reporting & Examples | Planned | 0/2 (0%) |

**Overall:** 12/25 issues completed (48%)
