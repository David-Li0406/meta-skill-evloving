---
title: "Tracking Artifacts Format - Quick Reference Card"
description: "One-page quick reference for creating and querying tracking artifacts in YAML+Markdown format"
audience: [ai-agents, developers]
tags: [quick-reference, format, artifacts]
created: 2025-11-15
updated: 2025-11-15
category: "ai-artifacts"
status: "published"
---

# Tracking Artifacts - Quick Reference

## File Types & Locations

| Type | Location | Purpose |
|------|----------|---------|
| **Progress** | `.claude/progress/[prd]/phase-[N]-progress.md` | Track phase progress, tasks, blockers |
| **Context** | `.claude/worknotes/[prd]/phase-[N]-context.md` | Document decisions, gotchas, integrations |
| **Bug Fixes** | `.claude/worknotes/fixes/bug-fixes-tracking-MM-YY.md` | Monthly bug fix tracking |
| **Observations** | `.claude/worknotes/observations/observation-log-MM-YY.md` | Monthly pattern/learning logs |

---

## YAML Frontmatter Schemas

### Progress File

```yaml
---
type: progress
prd: "string"                               # e.g., "advanced-editing-v2"
phase: number                               # 1, 2, 3, etc.
status: "planning" | "in-progress" | "review" | "complete" | "blocked"
overall_progress: number (0-100)            # Completion percentage
completion_estimate: "on-track" | "at-risk" | "blocked" | "ahead"
total_tasks: number
completed_tasks: number
owners: ["agent1", "agent2"]                # Primary owners
blockers: [{ id: "str", title: "str", status: "active" | "resolved" }]
success_criteria: [{ id: "str", description: "str", status: "pending" | "met" }]
files_modified: ["path/to/file1.ts", "path/to/file2.ts"]
---
```

### Context File

```yaml
---
type: context
prd: "string"
phase: number | null                        # null = all-phases
status: "complete" | "blocked" | "in-progress"
phase_status: [
  { phase: 1, status: "complete" | "blocked", reason: "optional" }
]
blockers: [
  {
    id: "BLK-1",
    title: "str",
    severity: "critical" | "high" | "medium",
    blocking: ["phase-2", "phase-3"],
    solution_path: "str"
  }
]
gotchas: [
  { id: "GOTCHA-1", title: "str", solution: "str", location: "file.ts:45" }
]
decisions: [
  { id: "DEC-1", question: "str", decision: "str", rationale: "str" }
]
integrations: [
  { id: "INT-1", system: "str", component: "str", status: "implemented" }
]
modified_files: [
  { path: "str", changes: "str", phase: 1 }
]
---
```

### Bug Fixes File

```yaml
---
type: bug-fixes
month: "MM"                                 # 01-12
year: "YYYY"
severity_breakdown: { critical: 0, high: 0, medium: 0, low: 0 }
component_breakdown: { editor: 0, blocks: 0, api: 0, ui: 0 }
fixes_by_component: { "editor": ["fix-1", "fix-2"], "blocks": ["fix-3"] }
fixes_by_date: { "YYYY-MM-DD": ["fix-1"], "YYYY-MM-DD": ["fix-2"] }
---
```

### Observations File

```yaml
---
type: observations
month: "MM"
year: "YYYY"
observation_counts: { "pattern-discoveries": 0, "performance-insights": 0 }
observations_by_category: { "pattern-discoveries": ["OBS-1", "OBS-2"] }
observations: {
  "OBS-1": { date: "ISO8601", category: "str", impact: "high" | "medium" | "low" }
}
---
```

---

## Task Entry Template

Use this in progress file body:

```markdown
### TASK-N.M: [Title]

**Status**: planning | in-progress | review | complete | blocked
**Assigned**: agent-name
**Effort**: story-points
**Duration**: "X hours" | "X days" | "X weeks"
**Priority**: critical | high | medium | low

**Description**: [Clear task description]

**Requirements**:
- Requirement 1
- Requirement 2

**Files**:
- `path/to/file.ts`: [What will change]

**Dependencies**: [If blocking other tasks]

**Notes**: [Additional context]
```

---

## Quick Query Examples

### Query 1: Get Pending Tasks for Agent

```javascript
import { getPendingTasksForAgent } from './query-helpers'

const tasks = getPendingTasksForAgent(progressFile, 'ui-engineer')
// Returns: [{ id, title, status, effort, duration, blockers }]
// Token cost: 1.2KB (vs 160KB full file)
```

### Query 2: Get All Critical Blockers

```javascript
import { getAllBlockers } from './query-helpers'

const critical = getAllBlockers(contextFile)
  .filter(b => b.severity === 'critical')
// Returns: [{ id, title, blocking, solution_path }]
// Token cost: 600B (vs 231KB full file)
```

### Query 3: Get Bug Fixes by Component

```javascript
import { getBugFixesByComponent } from './query-helpers'

const editorBugs = getBugFixesByComponent(bugFixFile, 'editor')
// Returns: [{ id, date, issue, severity, commit }]
// Token cost: 1.5KB (vs 294KB full file)
```

### Query 4: Get High-Impact Observations

```javascript
import { getHighImpactObservations } from './query-helpers'

const insights = getHighImpactObservations(obsFile)
// Returns: [{ id, date, category, title, affects }]
// Token cost: 1.5KB (vs 30KB full file)
```

---

## Status Values

### Progress Status
- `planning` - Phase being planned, not started
- `in-progress` - Tasks actively being worked on
- `review` - Waiting for code review/approval
- `complete` - All tasks done, success criteria met
- `blocked` - Cannot proceed, waiting on blocker

### Task Status
- `planning` - Task defined, not started
- `in-progress` - Task actively being worked
- `review` - Waiting for review
- `complete` - Task done, verified
- `blocked` - Task blocked by dependency

### Blocker Status
- `active` - Currently blocking work
- `resolved` - Blocker resolved, work can proceed
- `workaround` - Workaround in place, not ideal solution

### Component Status
- `implemented` - Feature fully built
- `waiting-for-backend` - Frontend ready, waiting on backend
- `waiting-for-frontend` - Backend ready, waiting on frontend
- `not-started` - Not yet implemented
- `complete-with-workarounds` - Works but with temporary fixes

---

## Naming Conventions

| Item | Pattern | Example |
|------|---------|---------|
| Progress file | `phase-[N]-progress.md` | `phase-2-progress.md` |
| Context file | `phase-[N]-context.md` | `phase-2-context.md` |
| Bug tracking | `bug-fixes-tracking-MM-YY.md` | `bug-fixes-tracking-11-25.md` |
| Observations | `observation-log-MM-YY.md` | `observation-log-11-25.md` |
| Task ID | `TASK-[N].[M]` | `TASK-1.2` (phase 1, task 2) |
| Blocker ID | `BLOCKER-[SHORT-DESC]` | `BLOCKER-API-ENDPOINTS` |
| Gotcha ID | `GOTCHA-[N]` | `GOTCHA-1` |
| Decision ID | `DECISION-[N]` | `DECISION-1` |
| Fix ID | `FIX-[N]` | `FIX-1` |
| Observation ID | `OBS-[N]` | `OBS-1` |

---

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| Mixing narrative in frontmatter | Can't parse as YAML | Keep frontmatter structured, narrative in body |
| Multiple progress files per phase | Creates confusion | One file per phase maximum |
| Status not in enum | Can't filter/query | Use only allowed status values |
| Missing required fields | Parsing fails | Always include: type, phase, status |
| Nested arrays in frontmatter | YAML parsing issues | Keep structure flat, arrays of simple objects |
| Prose in gotcha.solution | Can't be parsed | Keep solutions brief, 1-2 sentences |
| Inconsistent date formats | Can't query by date | Use ISO8601 (YYYY-MM-DD or ISO timestamp) |
| Forgetting to update totals | Counts wrong | Recalculate totals when changing task counts |

---

## Token Efficiency Checklist

When creating an artifact, verify:

- [ ] Frontmatter contains all queryable fields (status, dates, IDs)
- [ ] Narrative content is in body, not frontmatter
- [ ] No prose sentences in structured fields (keep values simple)
- [ ] Status values match enum (not custom values)
- [ ] File references are absolute paths
- [ ] IDs are unique (TASK-1.1, TASK-1.2, etc.)
- [ ] Dates are ISO8601 format
- [ ] Total counts match actual entries

---

## File Size Guidelines

| File Type | Frontmatter | Body | Total | Target |
|-----------|------------|------|-------|--------|
| Progress (1 phase) | 300B | 3-5KB | 4-6KB | < 10KB |
| Context (1 phase) | 2-3KB | 5-8KB | 8-12KB | < 15KB |
| Bug fixes (1 month) | 1KB | 5-10KB | 7-12KB | < 15KB |
| Observations (1 month) | 2KB | 5-8KB | 8-10KB | < 12KB |

If file exceeds target, consider splitting into multiple files or moving details to supporting files.

---

## Integration with Query Helpers

```javascript
// 1. Import the helper you need
import {
  getPendingTasksForAgent,
  getAllBlockers,
  getBugFixesByComponent,
  getHighImpactObservations
} from './query-helpers'

// 2. Call with file path
const results = getPendingTasksForAgent(filePath, filterArg)

// 3. Results are structured objects ready to use
console.log(results) // [{ id, title, status, ... }]

// 4. Optional: further filter/map
const highEffort = results.filter(t => t.effort > 5)
```

---

## Examples

### ✅ Good Frontmatter

```yaml
status: "in-progress"
phase: 2
blockers: [
  {
    id: "BLK-1",
    title: "Missing API endpoint",
    severity: "critical",
    blocking: ["phase-3"]
  }
]
```

### ❌ Bad Frontmatter

```yaml
status: "currently in progress, at risk of delay"  # Too verbose
phase: 2
blockers:
  - "We're blocked on the API endpoint that needs to be built for phase 3 because the backend team hasn't started it yet. This is critical."  # Prose, not structured
```

### ✅ Good Body

```markdown
### Blocker 1: Missing API Endpoint

The `/api/v1/prompts/{id}/blocks` endpoint hasn't been implemented yet. The frontend expects this endpoint to return a `PromptBlock[]` array, but the old system returns a different structure.

**Impact**: Block management UI cannot function without this endpoint.

**Solution**: Implement association endpoints as part of Phase 4.
```

### ❌ Bad Body

```markdown
### BLOCKER - API ENDPOINT

This is a major blocker for the entire phase because we need the API endpoint
to work with the frontend and without it nothing will function at all. The
endpoint should return data in a specific format and we need to make sure
that the data structure matches what the frontend expects.
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| YAML parse error | Invalid YAML syntax | Validate with `yaml.parse()` or online validator |
| Query returns empty array | Wrong filter value | Check enum values, use exact matches |
| Query returns all results | Missing filter condition | Add `.filter()` before `.map()` |
| Files show in edit but not in frontmatter | Forgot to add to array | Update `files_modified` array |
| Status not showing in dashboard | Status not in enum | Check allowed status values |
| Date queries fail | Non-ISO date format | Use YYYY-MM-DD or ISO8601 |

---

## Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| **Full Design** | `/ai/TRACKING-ARTIFACTS-DESIGN.md` | Complete specification |
| **Examples** | `/ai/examples/progress-example.md` | Real working examples |
| **Query Helpers** | `/ai/examples/query-helpers.js` | JavaScript query functions |
| **Summary** | `/ai/TRACKING-ARTIFACTS-SUMMARY.md` | Executive overview |
| **This Card** | `/ai/TRACKING-ARTIFACTS-QUICK-REFERENCE.md` | Quick lookup |

---

## Quick Start (5 Minutes)

1. **Copy template** from this card
2. **Fill frontmatter** with your metadata
3. **Write narrative** in body (following examples)
4. **Validate YAML** with online tool or `yaml` module
5. **Use query helpers** to access data efficiently

Done! You've created an optimized artifact.

---

**Print this page or save as reference for creating tracking artifacts!**

Last Updated: 2025-11-15 | Version: 1.0 | Status: Ready for Use
