# Plan List Examples

## Basic Usage

### List All Plans

```bash
/plan-list
```

**Output:**

```text
Plans: 5 total (3 active, 2 completed)

Active Plans (3):
  📋 cache-optimization-plan [in-progress, 45%]
     Module: effect-type-registry
     Updated: 2 days ago

  📋 observability-phase-2 [in-progress, 20%]
     Module: effect-type-registry
     Updated: 1 day ago

  📋 design-linking-phase-1 [ready, 0%]
     Module: design-doc-system
     Updated: 1 hour ago

Completed Plans (2):
  ✅ refactor-type-loading [completed, 100%]
     Completed: 1 week ago

  ✅ api-docs-generation [completed, 100%]
     Completed: 2 weeks ago

Health Summary:
  ✓ All active plans recently updated
  ✓ No blocked plans
```

### List by Status

```bash
/plan-list --status=in-progress
```

**Output:**

```text
In-Progress Plans (2):

  📋 cache-optimization-plan [45%]
     Module: effect-type-registry
     Started: Jan 11 (7 days ago)
     Updated: Jan 16 (2 days ago)
     Target: Jan 31 (13 days remaining)

  📋 observability-phase-2 [20%]
     Module: effect-type-registry
     Started: Jan 12 (6 days ago)
     Updated: Jan 17 (1 day ago)
     Target: Feb 05 (18 days remaining)

Progress Summary:
  Average: 32.5%
  Total Time: 13 days active
```

### List by Module

```bash
/plan-list --module=effect-type-registry
```

**Output:**

```text
Plans for module: effect-type-registry (4 total)

  📋 cache-optimization-plan [in-progress, 45%]
     Implements: effect-type-registry/cache-optimization.md
     Updated: 2 days ago

  📋 observability-phase-2 [in-progress, 20%]
     Implements: effect-type-registry/observability.md
     Updated: 1 day ago

  ✅ refactor-type-loading [completed, 100%]
     Completed: 1 week ago

  📋 performance-benchmarks [ready, 0%]
     Updated: 3 days ago

Module Health:
  ✓ 2 active implementations
  ✓ 1 completed
  ✓ 1 ready to start
```

## Filtering

### Multiple Statuses

```bash
/plan-list --status=ready,in-progress
```

**Output:**

```text
Active Work Plans (4):

Ready to Start (2):
  📋 design-linking-phase-1 [0%]
  📋 performance-benchmarks [0%]

In Progress (2):
  📋 cache-optimization-plan [45%]
  📋 observability-phase-2 [20%]

Recommendation: Start design-linking-phase-1 (all prerequisites met)
```

### Filter by Owner

```bash
/plan-list --owner=@spencerbeggs
```

**Output:**

```text
Plans owned by @spencerbeggs (3):

  📋 cache-optimization-plan [in-progress, 45%]
  📋 observability-phase-2 [in-progress, 20%]
  📋 design-linking-phase-1 [ready, 0%]

Workload Summary:
  Active: 2 plans (avg 32.5% progress)
  Pending: 1 plan
```

### Show Stale Plans

```bash
/plan-list --stale
```

**Output:**

```text
⚠️  Stale Plans (2):

  ⚠️  performance-benchmarks [ready, 0%]
      Last updated: 45 days ago
      Status: ready but not started

  ⚠️  api-refactor-v2 [in-progress, 30%]
      Last updated: 35 days ago
      Status: in-progress but stalled

Recommendations:
  1. Review performance-benchmarks: Still relevant?
  2. Update api-refactor-v2: Unblock or abandon?
  3. Consider archiving abandoned plans
```

## Output Formats

### Summary Format (Default)

```bash
/plan-list --status=in-progress
```

**Output:**

```text
In-Progress Plans (2):

  📋 cache-optimization-plan [45%]
     Module: effect-type-registry
     Updated: 2 days ago

  📋 observability-phase-2 [20%]
     Module: effect-type-registry
     Updated: 1 day ago
```

Clean, compact view for quick scanning.

### Detailed Format

```bash
/plan-list --status=in-progress --format=detailed
```

**Output:**

```text
Plan 1/2: cache-optimization-plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:    Cache Optimization Implementation
Status:   in-progress
Progress: [████████░░░░░░░░░░░░] 45%

Metadata:
  Module:    effect-type-registry
  Owner:     @spencerbeggs
  Estimate:  2-3 weeks
  Implements: effect-type-registry/cache-optimization.md

Timeline:
  Created:   2026-01-10 (8 days ago)
  Started:   2026-01-11 (7 days ago)
  Updated:   2026-01-16 (2 days ago)
  Target:    2026-01-31 (13 days remaining)

Phases:
  ✓ Phase 1: Initial Implementation (100%)
    Completed: 2026-01-14

  → Phase 2: Performance Testing (30%)
    In Progress: 4 days

  ○ Phase 3: Documentation (0%)
    Not Started

Health:
  ✓ On schedule (45% at day 7 of ~18)
  ✓ Recently updated (2 days ago)
  ✓ No blockers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Plan 2/2: observability-phase-2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:    Observability Phase 2 Implementation
Status:   in-progress
Progress: [████░░░░░░░░░░░░░░░░] 20%

Metadata:
  Module:    effect-type-registry
  Owner:     @spencerbeggs
  Estimate:  1-2 weeks
  Implements: effect-type-registry/observability.md

Timeline:
  Created:   2026-01-12 (6 days ago)
  Started:   2026-01-12 (6 days ago)
  Updated:   2026-01-17 (1 day ago)
  Target:    2026-02-05 (18 days remaining)

Phases:
  → Phase 1: Event System (20%)
    In Progress: 6 days

  ○ Phase 2: Metrics Integration (0%)
    Not Started

Health:
  ⚠  Slightly behind (20% at day 6 of ~14)
  ✓ Recently updated (1 day ago)
  ✓ No blockers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Full metadata and phase details for deep inspection.

### Timeline Format

```bash
/plan-list --status=in-progress --format=timeline
```

**Output:**

```text
Timeline View (sorted by started date):

cache-optimization-plan [45%]
Jan 10 ━━━━━━━━━━●━━━━━━━━━━ Jan 31
       ├─ Phase 1: Initial Implementation ✓
       ├─ Phase 2: Performance Testing (active)
       └─ Phase 3: Documentation

observability-phase-2 [20%]
Jan 12 ━━━━●━━━━━━━━━━━━━━━━ Feb 05
       ├─ Phase 1: Event System (active)
       └─ Phase 2: Metrics Integration

Legend:
  ● Current date
  ━ Timeline
  ✓ Completed phase
  (active) Current phase
```

Visual timeline for schedule tracking.

## Sorting

### Sort by Update Date (Default)

```bash
/plan-list --sort=updated --order=desc
```

Shows most recently updated plans first.

### Sort by Progress

```bash
/plan-list --status=in-progress --sort=progress --order=asc
```

**Output:**

```text
In-Progress Plans (sorted by progress, lowest first):

  📋 observability-phase-2 [20%]
  📋 type-loading-refactor [35%]
  📋 cache-optimization-plan [45%]
  📋 api-docs-generation [80%]

Recommendation: Focus on low-progress plans to prevent stalling
```

### Sort by Creation Date

```bash
/plan-list --sort=created --order=desc
```

Shows newest plans first.

### Sort by Name

```bash
/plan-list --sort=name --order=asc
```

Alphabetical order for browsing.

## Advanced Filtering

### Combine Filters

```bash
/plan-list --status=in-progress \
  --module=effect-type-registry \
  --owner=@spencerbeggs
```

**Output:**

```text
Filtered Plans (2):
  Status: in-progress
  Module: effect-type-registry
  Owner: @spencerbeggs

  📋 cache-optimization-plan [45%]
  📋 observability-phase-2 [20%]
```

### Find Blocked Plans

```bash
/plan-list --status=blocked
```

**Output:**

```text
Blocked Plans (1):

  🚫 api-integration-v3 [blocked, 60%]
      Module: rspress-plugin-api-extractor
      Blocked by: Upstream API changes
      Updated: 5 days ago

      Blocker Details:
        - Waiting for API v3 release
        - Expected: Feb 1
        - Action: Monitor upstream repo

Recommendation: Follow up on blocker status weekly
```

### Find Ready Plans

```bash
/plan-list --status=ready
```

**Output:**

```text
Ready to Start (3):

  📋 design-linking-phase-1 [0%]
     Module: design-doc-system
     All prerequisites met
     Priority: High

  📋 performance-benchmarks [0%]
     Module: effect-type-registry
     Depends on: cache-optimization-plan
     Priority: Medium

  📋 api-docs-v2 [0%]
     Module: rspress-plugin-api-extractor
     Priority: Low

Recommendation: Start design-linking-phase-1 (highest priority)
```

## Health Monitoring

### Check All Plans Health

```bash
/plan-list --format=detailed
```

**Output includes health section for each plan:**

```text
Health:
  ✓ On schedule (45% at day 7 of ~18)
  ✓ Recently updated (2 days ago)
  ✓ No blockers

  ⚠  Slightly behind (20% at day 6 of ~14)
  ⚠  Stale (updated > 30 days ago)
  🚫 Blocked by external dependency
```

### Find At-Risk Plans

```bash
/plan-list --status=in-progress --stale
```

Shows in-progress plans that haven't been updated recently (red flag).

### Weekly Review

```bash
# Check all active work
/plan-list --status=ready,in-progress,blocked --format=detailed
```

Comprehensive review of all active plans with health indicators.

## Including Archived Plans

### List Active and Archived

```bash
/plan-list --include-archived
```

**Output:**

```text
Plans: 12 total (5 active, 7 archived)

Active Plans (5):
  [... active plans ...]

Archived Plans (7):
  ✅ old-feature-plan [completed, 100%]
     Archived: 2025-12-01

  ❌ abandoned-feature [abandoned, 40%]
     Archived: 2025-11-15
     Reason: Superseded by new approach
```

### Count Archived Plans

```bash
/plan-list --include-archived --status=completed
```

Shows all completed plans, including archived ones.

## Integration Workflows

### Start of Work Session

```bash
# Check what's in progress
/plan-list --status=in-progress

# Check what's ready to start
/plan-list --status=ready
```

Helps prioritize work for the day.

### Weekly Planning

```bash
# Review all active work
/plan-list --status=ready,in-progress,blocked --format=detailed

# Check for stale plans
/plan-list --stale

# Review completed work
/plan-list --status=completed --sort=completed --order=desc
```

### Module Review

```bash
# Check plans for specific module
/plan-list --module=effect-type-registry --format=detailed

# Find module-specific issues
/plan-list --module=effect-type-registry --stale
```

### Owner Workload

```bash
# Check personal workload
/plan-list --owner=@spencerbeggs --status=in-progress

# Find ready plans to start
/plan-list --owner=@spencerbeggs --status=ready
```

## Empty Results

### No Plans Match Filters

```bash
/plan-list --status=blocked --module=effect-type-registry
```

**Output:**

```text
No plans found matching filters

Filters Applied:
  Status: blocked
  Module: effect-type-registry

Suggestions:
  1. Remove status filter: /plan-list --module=effect-type-registry
  2. Check other statuses: /plan-list --module=effect-type-registry
  3. List all plans: /plan-list
```

### No Plans Exist

```bash
/plan-list
```

**Output (when .claude/plans/ is empty):**

```text
No plans found

The plans directory is empty.

Get started:
  1. Create your first plan: /plan-create "My First Feature"
  2. See templates: ls .claude/plans/_templates/
  3. Read plan docs: cat .claude/design/design-doc-system/...
```

## Statistics Only

### Summary Statistics

```bash
/plan-list
```

**Top of output always shows statistics:**

```text
Plans: 12 total (7 active, 4 completed, 1 abandoned)

Status Breakdown:
  Ready:        3 plans (25%)
  In Progress:  4 plans (33%)
  Blocked:      0 plans (0%)
  Completed:    4 plans (33%)
  Abandoned:    1 plan (8%)

Health:
  On Schedule:  5 plans
  Behind:       2 plans
  Stale:        2 plans

Last Week Activity:
  Created:      2 plans
  Completed:    1 plan
  Updated:      6 plans
```

## Tips

### Quick Status Check

```bash
/plan-list --status=in-progress
```

Fastest way to see what's actively being worked on.

### Find Work to Do

```bash
/plan-list --status=ready --module=my-module
```

Find ready plans for your current focus area.

### Quick Health Check

```bash
/plan-list --stale
```

Regular health check to prevent abandoned work.

### Timeline Planning

```bash
/plan-list --status=in-progress,ready --format=timeline
```

Visual timeline for sprint planning.

### Export to JSON

```bash
/plan-list --format=json > plans.json
```

Machine-readable output for tooling integration.
