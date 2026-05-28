---
name: investigate
description: Investigate connection points between specs, atomic specs, and master specs. Surface inconsistencies in env vars, APIs, data shapes, and deployment assumptions before implementation.
allowed-tools: Read, Glob, Grep, Task
user-invocable: true
---

# /investigate Skill

## Purpose

Investigate and surface connection points between different specs, systems, and components. Identify inconsistencies, conflicting assumptions, and missing contracts before they become implementation bugs.

**Key insight**: This is NOT schema validation. This is intelligent investigation of where systems touch and whether their assumptions align.

## Usage

```
/investigate <spec-group-id>              # Investigate connections within a spec group
/investigate <spec-group-id> --cross      # Include connections to other spec groups
/investigate ms-<id>                      # Investigate all workstreams in a master spec
/investigate --all                        # Investigate all active specs
/investigate <sg1> <sg2> <sg3>            # Investigate specific spec groups together
```

## When to Use

### Mandatory Checkpoints

1. **Before MasterSpec implementation** - After workstream specs written, before any implementation
2. **Before spec group depends on another** - When sg-B references sg-A outputs
3. **After consistency issues found** - When manual review reveals conflicts

### Recommended Checkpoints

1. **After requirements gathering** - Early detection of assumption conflicts
2. **Before atomization** - Ensure parent spec has consistent interfaces
3. **During code review** - Validate implementation matches cross-spec contracts

## Prerequisites

Before running `/investigate`:
1. At least one spec group must exist
2. Spec(s) should have defined interfaces, env vars, or API endpoints
3. For `--cross`, multiple spec groups must exist

## Process

### 1. Scope Determination

Determine what's being investigated:

| Command | Scope |
|---------|-------|
| `/investigate sg-logout` | Single spec group + its declared dependencies |
| `/investigate sg-logout --cross` | sg-logout + all spec groups it touches |
| `/investigate ms-auth-system` | All workstreams in the master spec |
| `/investigate --all` | All active specs in `.claude/specs/groups/` |
| `/investigate sg-a sg-b sg-c` | Exactly those three spec groups |

### 2. Dispatch Interface Investigator

```
Task: interface-investigator
Prompt: |
  Investigate connection points in scope: <scope>

  Spec groups: <list>
  Mode: <single | cross | master>

  Focus on:
  1. Environment variable naming consistency
  2. API endpoint consistency (paths, methods, discovery)
  3. Data shape consistency (field names, types, required/optional)
  4. Deployment assumption consistency (infra, secrets management)
  5. Cross-spec dependencies and their assumptions
```

### 3. Generate Investigation Report

Agent produces a structured report with:
- Connection map (inputs/outputs/assumptions per spec)
- Inconsistencies by severity (Blocker/High/Medium/Low)
- Decisions required (with options and recommendations)
- Proposed canonical contracts

### 4. Report to User

Surface findings for human decision-making:

```
Interface Investigation: sg-auth-system + sg-user-management

Inconsistencies Found:
  Blocker: 1  (must resolve before implementation)
  High: 2     (will cause runtime errors)
  Medium: 1   (technical debt)
  Low: 0

Decisions Required: 3
  DEC-001: SSH key variable naming
  DEC-002: Container image format
  DEC-003: Required env vars set

Full report: .claude/specs/groups/sg-auth-system/investigation-report.md

Next steps:
  1. Review decisions in report
  2. Make canonical decisions
  3. Update affected specs
  4. (Optional) Create contracts in .claude/contracts/
```

## Output

### Clean (No Issues)

```
Interface Investigation: sg-logout-button ✓

Connection Map:
  Inputs: 2 (auth-service session, user context)
  Outputs: 1 (logout API call)
  Assumptions: 3 (all documented)

No inconsistencies found.

Spec group interfaces are consistent and ready for implementation.
```

### Issues Found

```
Interface Investigation: ms-deployment-pipeline ✗

Scope: 3 workstreams (ws-build, ws-deploy, ws-monitor)

Inconsistencies Found:

BLOCKER (1):
  INC-001: Missing .env fields in ws-monitor
    - ws-build defines: HMAC_SECRET, LOG_LEVEL, LOG_MAX_BYTES
    - ws-monitor template missing all three
    - Impact: ws-monitor will fail at runtime
    - Evidence: .claude/specs/groups/ws-build/.env.template:12-15
                .claude/specs/groups/ws-monitor/.env.template (missing)

HIGH (2):
  INC-002: SSH Key naming conflict
    - ws-build: GIT_SSH_KEY_PATH (file path approach)
    - ws-deploy: GIT_SSH_KEY_BASE64 (encoded approach)
    - Evidence: ws-build/spec.md:47, ws-deploy/atomic/as-003.md:23

  INC-003: Container image format conflict
    - ws-build: Split (CONTAINER_IMAGE + CONTAINER_IMAGE_TAG)
    - ws-deploy: Combined (CONTAINER_IMAGE=repo:tag)
    - Evidence: ws-build/spec.md:52-53, ws-deploy/spec.md:31

Decisions Required: 3

  DEC-001: SSH key variable naming
    Options: a) GIT_SSH_KEY_PATH  b) GIT_SSH_KEY_BASE64  c) GIT_SSH_KEY
    Recommendation: (c) - most portable
    Affected: ws-build, ws-deploy

  DEC-002: Container image format
    Options: a) Split  b) Combined
    Recommendation: (b) - simpler, standard
    Affected: ws-build, ws-deploy, CI/CD scripts

  DEC-003: Required env vars
    Options: a) ws-build set  b) ws-monitor set  c) Union
    Recommendation: (a) - more complete
    Affected: ws-monitor

Full report: .claude/specs/groups/ms-deployment-pipeline/investigation-report.md

BLOCKED: Cannot proceed to implementation until Blocker resolved.

Next steps:
  1. Decide on DEC-001, DEC-002, DEC-003
  2. Update affected specs with canonical decisions
  3. Re-run /investigate to confirm resolution
```

## Integration with Workflow

### In oneoff-spec Workflow

```
/route → PM → Spec → Atomize → Enforce
                         ↓
                   /investigate (if dependencies)
                         ↓
                    Implement
```

### In orchestrator Workflow

```
/route → PM → MasterSpec → [Parallel: WorkstreamSpecs]
                                    ↓
                              /investigate ms-<id>  ← MANDATORY
                                    ↓
                           Resolve decisions
                                    ↓
                        [Parallel: Implement per workstream]
```

### Triggered by /route

For complex tasks with multiple workstreams or dependencies, `/route` will recommend `/investigate` before implementation:

```
/route analysis: orchestrator workflow recommended

Before implementation:
  1. Run /investigate ms-<id> to surface cross-workstream conflicts
  2. Resolve any blocking decisions
  3. Then proceed to parallel implementation
```

## State Transitions

After `/investigate`:

**If CLEAN:**
- `manifest.json`:
  - `investigation_status`: "clean"
  - `last_investigated`: <timestamp>
- Ready for implementation

**If ISSUES:**
- `manifest.json`:
  - `investigation_status`: "issues_found"
  - `investigation_blockers`: <count>
  - `investigation_decisions_pending`: <count>
- Creates `investigation-report.md` in spec group
- Implementation blocked until blockers resolved

## Creating Contracts

When investigation surfaces repeated patterns, suggest creating canonical contracts:

```
Recommendation: Create canonical contracts

Based on this investigation, consider creating:

1. .claude/contracts/env-vars.contract.md
   - Canonical names for: GIT_SSH_KEY, CONTAINER_IMAGE, LOG_*
   - Discovery patterns for each

2. .claude/contracts/api-auth.contract.md
   - Canonical endpoint paths
   - Request/response shapes

These would prevent future inconsistencies.

Create contracts now? (run /contract create)
```

## Edge Cases

### No Dependencies Declared

```
Note: Spec group has no declared dependencies
Investigation limited to internal consistency

To investigate cross-spec connections, either:
  1. Add dependencies to manifest.json
  2. Run /investigate sg-a sg-b explicitly
```

### Spec Group Not Found

```
Error: Spec group 'sg-unknown' not found
Available spec groups:
  - sg-logout-button
  - sg-auth-system
  - sg-user-management
```

### MasterSpec Without Workstreams

```
Error: MasterSpec ms-pipeline has no workstream references
Cannot investigate cross-workstream connections

Ensure MasterSpec has workstreams defined in frontmatter.
```

## Comparison with /unify

| Aspect | /investigate | /unify |
|--------|--------------|--------|
| **When** | Before implementation | After implementation |
| **What** | Spec-to-spec consistency | Spec-to-implementation alignment |
| **Focus** | Assumptions, interfaces, contracts | Evidence, tests, traceability |
| **Blocks** | Implementation | Merge |

Think of it as:
- `/investigate` = "Do our specs agree with each other?"
- `/unify` = "Does our code match our specs?"
