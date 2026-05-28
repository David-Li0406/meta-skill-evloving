# Plan Exploration Examples

## Basic Exploration

### Show All Plans (Summary)

```bash
/plan-explore
```

**Output:**

```text
Implementation Plans Overview
============================

Status Summary:
  Ready: 2 plan(s)
  In Progress: 1 plan(s)

Active Plans (In Progress):
  • Plan-Design Linking System - Phase 2: Plan Exploration [80%] - 0 day(s) old
    Modules: design-doc-system
    Design: design-doc-system/plan-aware-enhancements.md

Health Insights:
  ✅ No stale plans
  ✅ No orphaned plans
  ✅ No blocked plans
  ✅ All plans healthy
```

## All Available Parameters

### Filtering Options

- `[module]` - Positional argument to filter by module name
- `--status=STATUS` - Filter by plan status (ready|in-progress|blocked|completed|abandoned)
  - Supports comma-separated values: `--status=ready,in-progress`
- `--design-doc=PATH` - Filter by design doc path (partial match)
- `--owner=NAME` - Filter by plan owner

### Health Filters

- `--orphans` - Show only orphaned plans (no design doc links)
- `--stale` - Show only stale plans (not updated in >30 days)
- `--blocked` - Show only blocked plans
- `--age-threshold=DAYS` - Set staleness threshold (default: 30)

### Output Options

- `--format=FORMAT` - Output format (summary|detailed|timeline|json)
  - `summary` - Concise overview with health insights (default)
  - `detailed` - Full plan metadata for each plan
  - `timeline` - Chronological view grouped by date
  - `json` - Machine-readable format
- `--no-health` - Hide health analysis section
- `--show-phases` - Show phase details (not yet implemented)

### Help

- `--help` - Show usage information and all options

## Filtering Plans

### Filter by Status

```bash
/plan-explore --status=in-progress
```

Shows only plans currently being worked on.

```bash
/plan-explore --status=ready,in-progress
```

Shows plans that are ready to start or already in progress.

### Filter by Module

```bash
/plan-explore effect-type-registry
```

Shows all plans for the effect-type-registry module.

**Output:**

```text
Implementation Plans: effect-type-registry
=========================================

Found 3 plans:
  • Cache Optimization Implementation [30%] - in progress
  • Performance Benchmarking [0%] - ready
  • Observability Phase 2 [100%] - completed
```

### Filter by Design Doc

```bash
/plan-explore --design-doc=effect-type-registry/observability.md
```

Shows all plans implementing the observability design doc.

### Filter by Owner

```bash
/plan-explore --owner="Spencer Beggs"
```

Shows all plans owned by Spencer Beggs.

## Health Analysis

### Find Stale Plans

```bash
/plan-explore --stale
```

Shows plans that haven't been updated in >30 days (default threshold).

**Output:**

```text
Stale Plans (>30 days)
=====================

Found 2 stale plans:

⚠️  legacy-migration [25%] - in progress
    Last updated: 45 days ago
    Modules: design-doc-system
    Recommendation: Update progress or mark as abandoned

⚠️  performance-tracking [60%] - in progress
    Last updated: 35 days ago
    Modules: effect-type-registry
    Recommendation: Update status or complete implementation
```

### Custom Staleness Threshold

```bash
/plan-explore --stale --age-threshold=60
```

Shows plans not updated in >60 days.

### Find Orphaned Plans

```bash
/plan-explore --orphans
```

Shows plans not linked to any design docs.

**Output:**

```text
Orphaned Plans (No Design Docs)
===============================

Found 1 orphaned plan:

⚠️  experimental-feature [10%] - in progress
    Last updated: 5 days ago
    Modules: design-doc-system
    Implements: []
    Recommendation: Link to design doc or create design doc first
```

### Find Blocked Plans

```bash
/plan-explore --blocked
```

Shows all blocked plans with blocker details.

**Output:**

```text
Blocked Plans
============

Found 2 blocked plans:

⏸️  performance-phase-2 [30%] - blocked
    Blocked by:
      - Test infrastructure setup
      - Benchmark baseline missing
    Last updated: 3 days ago
    Recommendation: Address blockers or update blocked-by list

⏸️  documentation-generation [0%] - blocked
    Blocked by:
      - cache-optimization-plan (also blocked) ⚠️ cascading block
    Last updated: 1 day ago
    Recommendation: Resolve blocker chain starting with cache-optimization
```

## Output Formats

### Detailed Format

```bash
/plan-explore --format=detailed
```

Shows full metadata for all plans:

```text
Implementation Plans - Detailed View
========================================

🚧 Plan-Design Linking System - Phase 2: Plan Exploration
---
  Name: plan-design-linking-phase-2
  Status: in-progress (80%)
  Created: 2026-01-18
  Updated: 2026-01-18
  Started: 2026-01-18
  Modules: design-doc-system
  Implements: design-doc-system/plan-aware-enhancements.md
  Owner: Spencer Beggs

📅 Subagent Integration Implementation Plan
---
  Name: subagent-integration-plan
  Status: ready (0%)
  Created: 2026-01-18
  Updated: 2026-01-18
  Modules: design-doc-system
  Implements: design-doc-system/subagent-integration.md
              design-doc-system/architecture-proposal.md
```

### Timeline Format

```bash
/plan-explore --format=timeline
```

Chronological view grouped by creation date:

```text
Implementation Plans - Timeline View
======================================

[2026-01-18]
  📅 Subagent Integration Implementation Plan
     Status: ready (0%)
     Module: design-doc-system
  🚧 Plan-Design Linking System - Phase 2: Plan Exploration
     Status: in-progress (80%)
     Module: design-doc-system
  📅 Phase 5: Design Documentation Automation & CI
     Status: ready (0%)
     Module: design-doc-system
```

### JSON Format

```bash
/plan-explore --format=json
```

Machine-readable output:

```json
{
  "plans": [
    {
      "name": "plan-design-linking-phase-2",
      "title": "Plan-Design Linking System - Phase 2: Plan Exploration",
      "status": "in-progress",
      "progress": 80,
      "created": "2026-01-18",
      "updated": "2026-01-18",
      "started": "2026-01-18",
      "modules": [
        "design-doc-system"
      ],
      "implements": [
        "design-doc-system/plan-aware-enhancements.md"
      ]
    }
  ],
  "health": {
    "total_plans": 3,
    "stale_plans": 0,
    "orphan_plans": 0,
    "blocked_plans": 0,
    "overdue_plans": 0,
    "misaligned_plans": 0
  }
}
```

## Combined Filters

### Module + Status

```bash
/plan-explore effect-type-registry --status=in-progress
```

Shows in-progress plans for effect-type-registry module.

### Status + Health Check

```bash
/plan-explore --status=in-progress --stale
```

Shows in-progress plans that are stale.

### Module + Format

```bash
/plan-explore design-doc-system --format=timeline
```

Shows timeline for design-doc-system module.

## Integration with Other Skills

### After Creating Plan

```bash
# Create new plan
/plan-create "New Feature Implementation" --module=effect-type-registry

# Verify it appears
/plan-explore effect-type-registry
```

### Before Starting Work

```bash
# Check what's ready to work on
/plan-explore --status=ready

# Check if anything is blocked
/plan-explore --blocked
```

### During Work Session

```bash
# Update plan status
/plan-update my-feature-plan --status=in-progress --progress=30

# See updated status
/plan-explore --status=in-progress
```

### Health Check Workflow

```bash
# 1. Find all health issues
/plan-explore --stale
/plan-explore --orphans
/plan-explore --blocked

# 2. Fix stale plans
/plan-update stale-plan --status=abandoned

# 3. Fix orphans
/plan-update orphan-plan --implements=module/design-doc.md

# 4. Verify fixed
/plan-explore --format=summary
```

### Pre-Release Audit

```bash
# Check all plan health
/plan-explore --format=detailed

# Focus on problematic plans
/plan-explore --stale --age-threshold=14

# Verify no blockers
/plan-explore --blocked

# Get JSON for reporting
/plan-explore --format=json > plan-report.json
```

## Edge Cases

### No Plans Exist

```bash
/plan-explore
```

**Output:**

```text
No plans found in .claude/plans/

Suggestion: Create a plan with /plan-create
```

### No Plans Match Filters

```bash
/plan-explore nonexistent-module
```

**Output:**

```text
No plans found matching filters:
  Module: nonexistent-module

Available modules:
  - effect-type-registry
  - rspress-plugin-api-extractor
  - design-doc-system

Try:
  - Remove filters
  - Check module name spelling
  - Use /plan-list to see all plans
```

### All Plans Healthy

```bash
/plan-explore
```

**Output:**

```text
Implementation Plans Overview
============================

Status Summary:
  Ready: 2 plans
  In Progress: 3 plans (avg 60% complete)
  Completed: 10 plans

Health Insights:
  ✅ No stale plans
  ✅ No orphaned plans
  ✅ No blocked plans
  ✅ All plans healthy

Next Actions:
  Continue with in-progress work
```

## Advanced Usage

### Finding Plans to Work On

```bash
# Show ready plans sorted by estimated effort
/plan-explore --status=ready --format=detailed
```

Helps prioritize next work based on effort estimates.

### Progress Tracking

```bash
# Show all active work with progress
/plan-explore --status=in-progress --format=detailed
```

See detailed progress breakdown including phases.

### Dependency Analysis

```bash
# Find blocked plans
/plan-explore --blocked

# Check what's blocking them
/plan-explore --format=detailed {blocking-plan-name}
```

Understand blocker chains.

### Module Health Check

```bash
# Check module status
/plan-explore effect-type-registry --format=summary

# Find problems in module
/plan-explore effect-type-registry --stale
/plan-explore effect-type-registry --orphans
```

Focused health check for specific module.

### Historical View

```bash
# See completed plans
/plan-explore --status=completed --format=timeline
```

Review what's been accomplished.
