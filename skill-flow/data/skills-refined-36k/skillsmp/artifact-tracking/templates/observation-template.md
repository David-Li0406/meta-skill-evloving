---
# === OBSERVATION LOG TEMPLATE ===
# Monthly tracking of patterns, learnings, insights, and discoveries
# One file per month: observation-log-MM-YY.md (e.g., observation-log-11-25.md)

# Metadata: Monthly Organization
type: observations
month: "[MM-YY]"                         # e.g., "11-25" for November 2025
year: [YYYY]                             # e.g., 2025
month_name: "[MONTH_NAME]"               # e.g., "November"

# Observation Counts (for trending)
total_observations: [COUNT]              # Total observations this month, e.g., 12
pattern_discoveries: [COUNT]             # Pattern count, e.g., 3
performance_insights: [COUNT]            # Performance count, e.g., 4
architectural_learnings: [COUNT]         # Architecture count, e.g., 3
tools_techniques: [COUNT]                # Tools/techniques count, e.g., 2

# Categories Covered (for trending analysis)
categories: [
  # e.g., "patterns", "performance", "architecture", "tools", "testing", "security"
]

# Impact Level Distribution (for prioritization)
high_impact: [COUNT]                     # High impact observations
medium_impact: [COUNT]                   # Medium impact observations
low_impact: [COUNT]                      # Low impact observations

# Observation Index (for quick lookups)
observation_index: {
  "[CATEGORY]": [
    # e.g., "patterns": ["OBS-001", "OBS-005", "OBS-009"]
  ]
}
---

# Observation Log: [MONTH_NAME] [YEAR]

**Month**: [MONTH_NAME] [YEAR]
**Total Observations**: [COUNT]
**Pattern Discoveries**: [COUNT] | **Performance**: [COUNT] | **Architecture**: [COUNT] | **Tools**: [COUNT]

---

## Overview

Brief summary of major themes and insights this month. Examples:
- Discovered 3 recurring patterns in block integration
- Identified 2 significant performance opportunities
- Learned critical lessons about RLS and query optimization

---

## Pattern Discoveries

Recurring patterns, conventions, and architectural themes discovered during development.

### OBS-001: [Pattern Name]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Patterns

**Observation**: [Brief description of the pattern]

**Where Found**: [Where in codebase this pattern appears]
- `path/to/file1.tsx`
- `path/to/file2.py`
- [Additional locations]

**Why It Matters**: [Why this pattern is important]

**Implementation Benefit**: [How following this pattern helps]

**Related Observations**: OBS-005, OBS-009

**Action Items**:
- [ ] Refactor [file] to use this pattern
- [ ] Document pattern in [location]

---

### OBS-002: [Pattern Name]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Patterns

**Observation**: [Brief observation]

**Where Found**: [Locations in codebase]

**Why It Matters**: [Importance]

**Implementation Benefit**: [How to apply]

**Related Observations**: OBS-XXX

---

### OBS-003: [Pattern Name]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Patterns

[Follow same structure as OBS-002]

---

## Performance Insights

Performance observations, bottlenecks, optimization opportunities, and efficiency improvements.

### OBS-004: [Performance Insight]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Performance

**Observation**: [What was discovered about performance]

**Measurement**: [How was it measured]
- Metric: [Specific metric]
- Baseline: [Current value]
- Target: [Desired value]
- Gap: [Difference]

**Root Cause**: [Why it's slow/inefficient]

**Optimization Opportunity**: [How to improve]
- Current approach: [What's being done now]
- Proposed approach: [Better way]
- Estimated improvement: [Performance gain, e.g., "50% faster"]
- Effort: [Small|Medium|Large]

**Files Affected**:
- `path/to/file.ts` - [Why this file matters]

**Implementation Priority**: High | Medium | Low

**Related Observations**: OBS-XXX

---

### OBS-005: [Performance Insight]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Performance

**Observation**: [Performance finding]

**Measurement**: [How measured]

**Optimization**: [Improvement opportunity]

**Effort**: [Small|Medium|Large]

---

### OBS-006: [Performance Insight]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Performance

[Follow same structure]

---

### OBS-007: [Performance Insight]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Performance

[Follow same structure]

---

## Architectural Learnings

Insights about system design, component interaction, data flow, and architectural patterns.

### OBS-008: [Architectural Learning]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Architecture

**Learning**: [What was learned about the system]

**Context**: [Situation where this learning was discovered]

**Why It Matters**: [Significance to system design]

**Key Insight**: [Core takeaway]

**Related Decisions**: DECISION-001, DECISION-002 (from context file)

**Implementation Implications**: [How this affects future work]

**Files Demonstrating This**: [Where in codebase can this be seen]
- `path/to/file.ts`

**Related Observations**: OBS-XXX

---

### OBS-009: [Architectural Learning]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Architecture

**Learning**: [What was learned]

**Context**: [Where discovered]

**Key Insight**: [Core takeaway]

**Related Decisions**: DECISION-XXX

**Related Observations**: OBS-XXX

---

### OBS-010: [Architectural Learning]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Architecture

[Follow same structure]

---

## Tools & Techniques

Discoveries about tools, techniques, workflows, and development practices that improve efficiency.

### OBS-011: [Tool or Technique]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Tools & Techniques

**Discovery**: [What tool or technique was discovered/refined]

**Use Case**: [When and why to use it]

**How It Works**: [Brief explanation of how it works]

**Benefit**: [Specific improvement to workflow]
- Time saved: [e.g., "Reduces debug time by 30%"]
- Quality improvement: [e.g., "Catches 5 more errors pre-commit"]
- Learning curve: [Easy|Moderate|Steep]

**Implementation Example**:
```
[Code, command, or process example]
```

**Where Applicable**: [Which parts of codebase or which workflows]

**Related Tools**: [Other tools that work well with this]

**Limitations**: [What doesn't work well]

---

### OBS-012: [Tool or Technique]

**Date**: [YYYY-MM-DD]
**Impact**: High | Medium | Low
**Category**: Tools & Techniques

**Discovery**: [What was discovered]

**Use Case**: [When to use]

**Benefit**: [Specific improvement]

**Implementation Example**:
```
[Example]
```

---

## By Category Summary

### Patterns

| ID | Title | Impact | Implementation Benefit |
|----|-------|--------|----------------------|
| OBS-001 | [Title] | High | [Benefit] |
| OBS-002 | [Title] | Medium | [Benefit] |
| OBS-003 | [Title] | Low | [Benefit] |

### Performance

| ID | Title | Impact | Optimization |
|----|-------|--------|--------------|
| OBS-004 | [Title] | High | [Improvement] |
| OBS-005 | [Title] | Medium | [Improvement] |
| OBS-006 | [Title] | High | [Improvement] |
| OBS-007 | [Title] | Low | [Improvement] |

### Architecture

| ID | Title | Impact | Key Insight |
|----|-------|--------|------------|
| OBS-008 | [Title] | High | [Insight] |
| OBS-009 | [Title] | Medium | [Insight] |
| OBS-010 | [Title] | High | [Insight] |

### Tools & Techniques

| ID | Title | Impact | Benefit |
|----|-------|--------|---------|
| OBS-011 | [Title] | Medium | [Benefit] |
| OBS-012 | [Title] | High | [Benefit] |

---

## High Impact Observations (Priority for Action)

These observations should influence architecture and implementation decisions:

1. **OBS-001**: [Pattern Name]
   - **Action**: [What to do about this]
   - **Timeline**: [When to address]
   - **Owner**: [Who should lead this]

2. **OBS-004**: [Performance Insight]
   - **Action**: [Optimization to implement]
   - **Estimated Gain**: [Performance improvement]
   - **Timeline**: [When to implement]

3. **OBS-008**: [Architectural Learning]
   - **Action**: [Design change to make]
   - **Affected Systems**: [What systems change]
   - **Timeline**: [When to implement]

---

## Medium Impact Observations (Consider for Next Phase)

Observations worth addressing in upcoming phases:

- **OBS-002**: [Pattern] - Suggest refactoring [files]
- **OBS-005**: [Performance] - Consider optimization in Phase 3
- **OBS-009**: [Architecture] - Affects design of [upcoming feature]
- **OBS-011**: [Tool] - Integrate into development workflow

---

## Trend Analysis

### Recurring Themes

Themes that appear multiple times suggest systemic issues or opportunities:

1. **Theme**: [Common pattern/insight appearing in multiple observations]
   - Observations: OBS-XXX, OBS-XXX, OBS-XXX
   - Implication: [What this suggests]
   - Recommendation: [What to do about it]

2. **Theme**: [Another recurring theme]
   - Observations: OBS-XXX, OBS-XXX
   - Implication: [What this suggests]

### Month-over-Month Comparison

**November 2025 vs October 2025**:

| Category | Oct | Nov | Trend | Notes |
|----------|-----|-----|-------|-------|
| Pattern Discoveries | 2 | 3 | ↑ | More patterns emerging |
| Performance Issues | 5 | 4 | ↓ | Improvements from last month |
| Architecture Learnings | 2 | 3 | ↑ | More complex system interactions |
| Tools & Techniques | 1 | 2 | ↑ | More tooling improvements |

---

## Implementation Checklist

### This Month

- [ ] Document OBS-001 pattern in codebase
- [ ] Implement optimization from OBS-004
- [ ] Review architectural decision OBS-008

### Next Month

- [ ] Apply pattern OBS-002 to [files]
- [ ] Measure performance improvement from OBS-005
- [ ] Discuss architecture change from OBS-009

### Backlog

- [ ] Refactor [component] using pattern OBS-003
- [ ] Implement tool/technique OBS-011 in workflow
- [ ] Plan architectural change from OBS-010

---

## Connection to Other Tracking Docs

### Related Progress Files
- `.claude/progress/[prd-name]/phase-N-progress.md` - Implementation progress

### Related Context Files
- `.claude/worknotes/[prd-name]/phase-N-context.md` - Technical decisions and patterns

### Related Bug Fixes
- `.claude/worknotes/fixes/bug-fixes-tracking-11-25.md` - November bug fixes

### Previous Months
- `observation-log-10-25.md` - October observations
- `observation-log-09-25.md` - September observations

---

## Quick Reference for AI Agents

**Query: "What performance opportunities exist?"**
→ See: OBS-004, OBS-005, OBS-006, OBS-007

**Query: "What patterns should we follow?"**
→ See: OBS-001, OBS-002, OBS-003

**Query: "What architectural insights matter?"**
→ See: OBS-008, OBS-009, OBS-010

**Query: "What tools/techniques should we use?"**
→ See: OBS-011, OBS-012

**Query: "What's high impact and should be prioritized?"**
→ See: High Impact Observations section
