---
name: plan-design-linking-phase-2
title: "Plan-Design Linking System - Phase 2: Plan Exploration"
created: 2026-01-18
updated: 2026-01-18
status: in-progress
progress: 60
implements:
  - design-doc-system/plan-aware-enhancements.md
modules:
  - design-doc-system
categories: [feature]
estimated-effort: "1-2 weeks"
actual-effort: null
started: 2026-01-18
completed: null
owner: Spencer Beggs
reviewers: []
blocked-by: []
related-plans:
  - plan-design-linking-phase-1
phases:
  - name: "Day 1: Skill Infrastructure"
    status: completed
    completion: 100
  - name: "Day 2: Query Library"
    status: completed
    completion: 100
  - name: "Day 3: Health Analysis"
    status: completed
    completion: 100
  - name: "Day 4: Output Formats"
    status: pending
    completion: 0
  - name: "Day 5: Testing & Documentation"
    status: pending
    completion: 0
archived: null
archival-reason: null
outcome: null
---

## Overview

Phase 2 implements the `plan-explore` skill, a comprehensive exploration and
navigation tool for the plan ecosystem. This skill enables agents to understand
project status at a glance, discover plans related to current work, identify
bottlenecks and health issues, and navigate relationships between plans and
design docs.

**Key Deliverables:**

1. **plan-explore skill** - Full skill implementation with multiple output formats
2. **Plan query library** - Reusable functions for querying plan metadata
3. **Health analysis** - Algorithms for detecting stale, orphaned, and blocked plans
4. **Comprehensive documentation** - Usage examples and integration guides

## Motivation

With Phase 1 complete, we have the infrastructure for creating, validating,
listing, and completing plans. However, we lack comprehensive exploration
capabilities. Agents need to:

- See project health at a glance
- Discover plans by module, status, or design doc
- Identify problems (stale, orphaned, blocked plans)
- Get actionable recommendations for next steps

The plan-explore skill fills this gap by providing rich querying, filtering,
and health analysis capabilities.

## Design Reference

- [Plan-Aware Enhancements](../design/design-doc-system/plan-aware-enhancements.md)

## Implementation Phases

### Day 1: Skill Infrastructure

**Status:** Pending

**Tasks:**

- [ ] Create `.claude/skills/plan-explore/` directory structure
- [ ] Write `SKILL.md` with skill metadata and overview
- [ ] Create `instructions.md` with detailed implementation steps
- [ ] Create `examples.md` with usage examples
- [ ] Set up basic bash script skeleton `scripts/explore-plans.sh`
- [ ] Add argument parsing (module, status, format, filters)
- [ ] Add plan-explore to design.config.json enabled skills
- [ ] Add plan-explore to design-doc-agent subagent skills

**Success Criteria:**

- Skill directory structure follows Anthropic best practices
- SKILL.md uses progressive disclosure pattern
- Script accepts all planned parameters
- Skill integrated into config

### Day 2: Query Library

**Status:** Pending

**Tasks:**

- [ ] Implement plan metadata parsing (frontmatter extraction)
- [ ] Implement filtering functions (by module, status, design-doc, owner)
- [ ] Implement plan discovery (scan `.claude/plans/` directory)
- [ ] Add caching for plan metadata (5 minute TTL)
- [ ] Implement relationship queries (plans ↔ design docs)
- [ ] Add sorting capabilities (by date, progress, name)
- [ ] Test query performance on multiple plans

**Success Criteria:**

- Can query plans by any frontmatter field
- Filtering works correctly with multiple criteria
- Metadata caching improves performance
- Relationship queries return accurate results

### Day 3: Health Analysis

**Status:** Pending

**Tasks:**

- [ ] Implement staleness detection (>30 days since update)
- [ ] Implement orphan detection (no design-docs references)
- [ ] Implement blocker analysis (cascading blocks, stale blockers)
- [ ] Implement schedule analysis (behind/ahead of target)
- [ ] Implement progress validation (status-progress alignment)
- [ ] Add health scoring algorithm
- [ ] Generate actionable recommendations

**Success Criteria:**

- Staleness detection accurate and configurable
- Orphan detection finds plans without design docs
- Blocker analysis identifies cascading problems
- Schedule analysis uses target-completion dates
- Recommendations are clear and actionable

### Day 4: Output Formats

**Status:** Pending

**Tasks:**

- [ ] Implement summary format (default, concise overview)
- [ ] Implement detailed format (full plan metadata)
- [ ] Implement timeline format (chronological view)
- [ ] Implement JSON format (machine-readable)
- [ ] Add color coding (status indicators, health)
- [ ] Add emoji indicators (✅ ⚠️ 🚧 📋 📅)
- [ ] Format health insights section
- [ ] Format recommendations section

**Success Criteria:**

- Summary format shows essential info in <50 lines
- Detailed format shows all plan metadata
- Timeline format groups by date/month
- JSON format is valid and parseable
- Output is readable and well-formatted

### Day 5: Testing & Documentation

**Status:** Pending

**Tasks:**

- [ ] Test with 0 plans (empty directory)
- [ ] Test with single plan
- [ ] Test with multiple plans (various statuses)
- [ ] Test filtering combinations
- [ ] Test health analysis edge cases
- [ ] Test all output formats
- [ ] Document all parameters in examples.md
- [ ] Add integration examples with other skills
- [ ] Test caching and performance

**Success Criteria:**

- All edge cases handled gracefully
- Error messages are clear and helpful
- Examples cover all major use cases
- Performance acceptable (<500ms for 20 plans)

## Success Criteria (Overall)

- [ ] plan-explore skill fully operational
- [ ] All query modes working (filter by module, status, design-doc, owner)
- [ ] All output formats working (summary, detailed, timeline, JSON)
- [ ] Health analysis detects stale, orphaned, blocked plans
- [ ] Recommendations are actionable and helpful
- [ ] Documentation comprehensive with examples
- [ ] Skill integrated into design-doc-agent
- [ ] Performance acceptable (auto-context <100ms, detailed <500ms)
- [ ] Caching implemented and working

## Blockers

None currently. Phase 1 is complete and provides all necessary infrastructure.

## Notes

**Design Decisions:**

- **Caching Strategy**: 5-minute TTL for plan metadata to balance freshness
  and performance
- **Output Defaults**: Summary format by default to avoid overwhelming output
- **Health Thresholds**: 30 days for staleness (configurable)
- **Filtering**: Support multiple status values for flexible queries

**Future Enhancements (Phase 3+):**

- Plan-aware design skills (design-review, design-sync, etc.)
- Auto-context mode for all design-* skills
- Plan progress estimation from code analysis
- GitHub integration for issue syncing
