# GitHub Issue Mapping Guide

Detailed rules for transforming plan/spec content into GitHub issues.

---

## Content Mapping

### From Plans

**Plan → Initiative:**
- Plan overview → Initiative overview
- Plan context → Initiative scope
- Success criteria → Acceptance criteria

**Plan phases → Features:**
- Each major phase becomes a Feature issue
- Phase tasks become Task issues under Feature

### From Specs

**Spec → Initiative:**
- Spec overview → Initiative overview
- User stories → Initiative scope
- Release criteria → Acceptance criteria

**Spec tasks → Tasks:**
- Task breakdown from spec becomes Task issues

---

## Issue Title Patterns

### Initiative

**Format:** `[ProjectName] - [Major Capability]`

**Examples:**
- `getml-kit - Data Export System`
- `feature-link - Temporal Join Support`
- `api-server - Authentication Overhaul`

**Purpose:** High-level epic representing major capability or feature area

### Feature

**Format:** `[Verb] [feature area]`

**Examples:**
- `Implement data export module`
- `Add temporal join compilation`
- `Refactor authentication middleware`

**Purpose:** Mid-level deliverable, typically part of an Initiative

### Task

**Format:** `[Verb] [specific action]`

**Examples:**
- `Add CSV export handler`
- `Create TemporalJoin IR node`
- `Update JWT validation logic`

**Purpose:** Concrete, completable unit of work

---

## Component Label Detection

Analyze file paths and descriptions to suggest component labels:

**File path patterns:**
- `src/view/` → `component:view`
- `src/api/` → `component:api`
- `src/export/` → `component:export`
- `src/{module}/` → `component:{module}`

**Description keywords:**
- "View", "compile", "IR" → `component:view`
- "API", "endpoint", "route" → `component:api`
- "export", "format", "output" → `component:export`

**Generic fallback:**
- `component:core` for fundamental infrastructure
- `component:tests` for test-only changes
- `component:docs` for documentation

---

## Priority Mapping

**From plan urgency:**
- "Critical", "blocking", "urgent" → Priority: High
- "Important", "needed" → Priority: Medium
- "Nice to have", "future" → Priority: Low

**From dependencies:**
- Task with many dependents → Priority: High
- Task on critical path → Priority: High
- Task with no dependencies → Can be Low

---

## Label Suggestions

**Type labels:**
- `type:feature` - New functionality
- `type:enhancement` - Improvement to existing feature
- `type:bug` - Fix for incorrect behavior
- `type:refactor` - Code restructuring without behavior change
- `type:docs` - Documentation updates
- `type:test` - Test additions or improvements

**Complexity labels:**
- `complexity:low` - < 2 hours, straightforward
- `complexity:medium` - 2-8 hours, moderate complexity
- `complexity:high` - > 8 hours, significant work

**Status labels:**
- `status:blocked` - Cannot proceed (document blocker)
- `status:ready` - Ready to work on
- `status:in-progress` - Currently being worked
- `status:review` - Implementation done, awaiting review

---

## Cross-Linking

**Reference patterns:**
- Initiative mentions all Features: `Includes: #123, #124, #125`
- Features mention parent Initiative: `Part of #122`
- Tasks mention parent Feature: `Implements #123`

**Dependency notation:**
- `Depends on: #120` - Must wait for completion
- `Blocks: #125` - This must complete first
- `Related to: #118` - Conceptually related, no hard dependency
